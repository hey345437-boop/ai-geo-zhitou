"""
Cost Controller & Budget Gate
Tracks API costs and enforces budget limits
"""
from dataclasses import dataclass
from typing import Dict, Optional, List
from datetime import datetime, timedelta
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class UserTier(Enum):
    """User subscription tiers"""
    FREE = "free"
    BASIC = "basic"
    PRO = "pro"
    ENTERPRISE = "enterprise"


@dataclass
class BudgetLimit:
    """Budget limits by tier"""
    tier: UserTier
    monthly_limit: float  # USD
    daily_limit: float  # USD
    per_query_limit: float  # USD


@dataclass
class CostRecord:
    """Cost tracking record"""
    user_id: str
    timestamp: datetime
    engine: str
    tokens: int
    cost: float
    query_type: str


@dataclass
class BudgetStatus:
    """Current budget status"""
    tier: UserTier
    monthly_limit: float
    monthly_used: float
    monthly_remaining: float
    daily_used: float
    daily_remaining: float
    is_exceeded: bool
    warning_level: str  # none, low, medium, high


class CostTracker:
    """Track API costs per user"""
    
    # Budget limits by tier
    BUDGET_LIMITS = {
        UserTier.FREE: BudgetLimit(
            tier=UserTier.FREE,
            monthly_limit=10.0,
            daily_limit=1.0,
            per_query_limit=0.1
        ),
        UserTier.BASIC: BudgetLimit(
            tier=UserTier.BASIC,
            monthly_limit=100.0,
            daily_limit=10.0,
            per_query_limit=1.0
        ),
        UserTier.PRO: BudgetLimit(
            tier=UserTier.PRO,
            monthly_limit=500.0,
            daily_limit=50.0,
            per_query_limit=5.0
        ),
        UserTier.ENTERPRISE: BudgetLimit(
            tier=UserTier.ENTERPRISE,
            monthly_limit=10000.0,
            daily_limit=1000.0,
            per_query_limit=100.0
        ),
    }
    
    def __init__(self):
        # In-memory storage (replace with database in production)
        self.cost_records: Dict[str, List[CostRecord]] = {}
    
    def record_cost(self, user_id: str, engine: str, tokens: int, cost: float, query_type: str = "probe"):
        """Record API cost"""
        record = CostRecord(
            user_id=user_id,
            timestamp=datetime.now(),
            engine=engine,
            tokens=tokens,
            cost=cost,
            query_type=query_type
        )
        
        if user_id not in self.cost_records:
            self.cost_records[user_id] = []
        
        self.cost_records[user_id].append(record)
        logger.info(f"Recorded cost for user {user_id}: ${cost:.4f} ({engine})")
    
    def get_monthly_cost(self, user_id: str) -> float:
        """Get total cost for current month"""
        if user_id not in self.cost_records:
            return 0.0
        
        now = datetime.now()
        month_start = datetime(now.year, now.month, 1)
        
        monthly_records = [
            r for r in self.cost_records[user_id]
            if r.timestamp >= month_start
        ]
        
        return sum(r.cost for r in monthly_records)
    
    def get_daily_cost(self, user_id: str) -> float:
        """Get total cost for today"""
        if user_id not in self.cost_records:
            return 0.0
        
        today = datetime.now().date()
        
        daily_records = [
            r for r in self.cost_records[user_id]
            if r.timestamp.date() == today
        ]
        
        return sum(r.cost for r in daily_records)
    
    def get_budget_status(self, user_id: str, tier: UserTier) -> BudgetStatus:
        """Get current budget status"""
        limit = self.BUDGET_LIMITS[tier]
        monthly_used = self.get_monthly_cost(user_id)
        daily_used = self.get_daily_cost(user_id)
        
        monthly_remaining = max(0, limit.monthly_limit - monthly_used)
        daily_remaining = max(0, limit.daily_limit - daily_used)
        
        is_exceeded = monthly_used >= limit.monthly_limit or daily_used >= limit.daily_limit
        
        # Determine warning level
        monthly_usage_pct = monthly_used / limit.monthly_limit
        if monthly_usage_pct >= 1.0:
            warning_level = "critical"
        elif monthly_usage_pct >= 0.9:
            warning_level = "high"
        elif monthly_usage_pct >= 0.8:
            warning_level = "medium"
        elif monthly_usage_pct >= 0.5:
            warning_level = "low"
        else:
            warning_level = "none"
        
        return BudgetStatus(
            tier=tier,
            monthly_limit=limit.monthly_limit,
            monthly_used=monthly_used,
            monthly_remaining=monthly_remaining,
            daily_used=daily_used,
            daily_remaining=daily_remaining,
            is_exceeded=is_exceeded,
            warning_level=warning_level
        )
    
    def check_budget(self, user_id: str, tier: UserTier, estimated_cost: float) -> tuple[bool, str]:
        """Check if user has budget for query"""
        status = self.get_budget_status(user_id, tier)
        limit = self.BUDGET_LIMITS[tier]
        
        # Check if already exceeded
        if status.is_exceeded:
            return False, f"Budget exceeded. Monthly: ${status.monthly_used:.2f}/${status.monthly_limit:.2f}"
        
        # Check if this query would exceed limits
        if status.monthly_used + estimated_cost > limit.monthly_limit:
            return False, f"Query would exceed monthly budget (${estimated_cost:.2f} + ${status.monthly_used:.2f} > ${limit.monthly_limit:.2f})"
        
        if status.daily_used + estimated_cost > limit.daily_limit:
            return False, f"Query would exceed daily budget (${estimated_cost:.2f} + ${status.daily_used:.2f} > ${limit.daily_limit:.2f})"
        
        if estimated_cost > limit.per_query_limit:
            return False, f"Query cost too high (${estimated_cost:.2f} > ${limit.per_query_limit:.2f})"
        
        return True, "Budget OK"
    
    def get_cost_breakdown(self, user_id: str, days: int = 30) -> Dict[str, float]:
        """Get cost breakdown by engine"""
        if user_id not in self.cost_records:
            return {}
        
        cutoff = datetime.now() - timedelta(days=days)
        recent_records = [
            r for r in self.cost_records[user_id]
            if r.timestamp >= cutoff
        ]
        
        breakdown = {}
        for record in recent_records:
            breakdown[record.engine] = breakdown.get(record.engine, 0.0) + record.cost
        
        return breakdown
    
    def forecast_monthly_cost(self, user_id: str) -> float:
        """Forecast end-of-month cost based on current usage"""
        monthly_cost = self.get_monthly_cost(user_id)
        
        now = datetime.now()
        days_in_month = (datetime(now.year, now.month + 1, 1) - timedelta(days=1)).day
        days_elapsed = now.day
        
        if days_elapsed == 0:
            return 0.0
        
        daily_average = monthly_cost / days_elapsed
        forecast = daily_average * days_in_month
        
        return forecast


class CostOptimizer:
    """Optimize query costs"""
    
    # Engine costs (per 1k tokens)
    ENGINE_COSTS = {
        'gpt-4': 0.03,
        'claude-3': 0.015,
        'gemini-pro': 0.001,
        'perplexity': 0.005,
        'bing-chat': 0.002,
        'you-chat': 0.003,
        'qwen': 0.002,
        'ernie-bot': 0.002,
    }
    
    @classmethod
    def estimate_cost(cls, engine: str, estimated_tokens: int) -> float:
        """Estimate cost before execution"""
        cost_per_1k = cls.ENGINE_COSTS.get(engine, 0.01)
        return (estimated_tokens / 1000) * cost_per_1k
    
    @classmethod
    def select_cheapest_engine(cls, required_capability: str = "general") -> str:
        """Select cheapest engine for capability"""
        # Simplified: return cheapest overall
        sorted_engines = sorted(cls.ENGINE_COSTS.items(), key=lambda x: x[1])
        return sorted_engines[0][0]
    
    @classmethod
    def optimize_query_cost(cls, engines: List[str], budget: float, estimated_tokens: int) -> List[str]:
        """Select engines within budget"""
        affordable_engines = []
        
        for engine in engines:
            cost = cls.estimate_cost(engine, estimated_tokens)
            if cost <= budget:
                affordable_engines.append(engine)
        
        # Sort by cost (cheapest first)
        affordable_engines.sort(key=lambda e: cls.ENGINE_COSTS.get(e, 0.01))
        
        return affordable_engines


# Global cost tracker instance
cost_tracker = CostTracker()
