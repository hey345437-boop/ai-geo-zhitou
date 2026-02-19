"""
Multi-Armed Bandit Optimizer
Implements Thompson Sampling and contextual bandits for strategy optimization
"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
import random
import math
import logging

logger = logging.getLogger(__name__)


@dataclass
class BanditArm:
    """Bandit arm (strategy/variant)"""
    id: str
    name: str
    description: str
    alpha: float = 1.0  # Beta distribution parameter (successes + 1)
    beta: float = 1.0   # Beta distribution parameter (failures + 1)
    pulls: int = 0
    rewards: float = 0.0
    cost: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class BanditContext:
    """Context for contextual bandit"""
    region: Optional[str] = None
    intent_type: Optional[str] = None
    domain: Optional[str] = None
    language: Optional[str] = None
    time_of_day: Optional[str] = None


@dataclass
class BanditTrial:
    """Single bandit trial record"""
    trial_id: str
    arm_id: str
    context: BanditContext
    reward: float
    cost: float
    timestamp: datetime


class ThompsonSampling:
    """Thompson Sampling for Multi-Armed Bandit"""
    
    def __init__(self):
        self.arms: Dict[str, BanditArm] = {}
        self.trials: List[BanditTrial] = []
    
    def add_arm(
        self,
        arm_id: str,
        name: str,
        description: str,
        cost: float = 0.0
    ) -> BanditArm:
        """Add a new arm to the bandit"""
        arm = BanditArm(
            id=arm_id,
            name=name,
            description=description,
            cost=cost
        )
        
        self.arms[arm_id] = arm
        logger.info(f"Added arm: {arm_id} - {name}")
        
        return arm
    
    def select_arm(
        self,
        context: Optional[BanditContext] = None,
        budget_constraint: Optional[float] = None
    ) -> str:
        """
        Select arm using Thompson Sampling
        
        Args:
            context: Context for contextual bandit
            budget_constraint: Maximum cost constraint
        
        Returns:
            Selected arm ID
        """
        if not self.arms:
            raise ValueError("No arms available")
        
        # Filter arms by budget constraint
        available_arms = {
            arm_id: arm for arm_id, arm in self.arms.items()
            if budget_constraint is None or arm.cost <= budget_constraint
        }
        
        if not available_arms:
            raise ValueError("No arms within budget constraint")
        
        # Sample from Beta distribution for each arm
        samples = {}
        for arm_id, arm in available_arms.items():
            # Thompson Sampling: sample from Beta(alpha, beta)
            sample = self._beta_sample(arm.alpha, arm.beta)
            samples[arm_id] = sample
        
        # Select arm with highest sample
        selected_arm_id = max(samples, key=samples.get)
        
        logger.info(f"Selected arm: {selected_arm_id} (sample: {samples[selected_arm_id]:.4f})")
        
        return selected_arm_id
    
    def update(
        self,
        arm_id: str,
        reward: float,
        cost: float = 0.0,
        context: Optional[BanditContext] = None
    ):
        """
        Update arm statistics after observing reward
        
        Args:
            arm_id: Arm that was pulled
            reward: Observed reward (0-1 for binary, or continuous)
            cost: Cost incurred
            context: Context of the trial
        """
        arm = self.arms.get(arm_id)
        if not arm:
            raise ValueError(f"Arm {arm_id} not found")
        
        # Update Beta distribution parameters
        # For binary rewards: alpha += reward, beta += (1 - reward)
        # For continuous rewards: normalize to [0, 1]
        normalized_reward = max(0, min(1, reward))
        
        arm.alpha += normalized_reward
        arm.beta += (1 - normalized_reward)
        arm.pulls += 1
        arm.rewards += reward
        arm.cost += cost
        
        # Record trial
        trial = BanditTrial(
            trial_id=f"trial_{len(self.trials) + 1}",
            arm_id=arm_id,
            context=context or BanditContext(),
            reward=reward,
            cost=cost,
            timestamp=datetime.now()
        )
        self.trials.append(trial)
        
        logger.info(f"Updated arm {arm_id}: alpha={arm.alpha:.2f}, beta={arm.beta:.2f}")
    
    def get_arm_statistics(self, arm_id: str) -> Dict:
        """Get statistics for an arm"""
        arm = self.arms.get(arm_id)
        if not arm:
            raise ValueError(f"Arm {arm_id} not found")
        
        # Calculate expected value (mean of Beta distribution)
        expected_value = arm.alpha / (arm.alpha + arm.beta)
        
        # Calculate variance
        variance = (arm.alpha * arm.beta) / \
                  ((arm.alpha + arm.beta) ** 2 * (arm.alpha + arm.beta + 1))
        
        # Calculate average reward
        avg_reward = arm.rewards / arm.pulls if arm.pulls > 0 else 0
        
        # Calculate total cost
        total_cost = arm.cost
        
        # Calculate ROI
        roi = (arm.rewards - arm.cost) / arm.cost if arm.cost > 0 else 0
        
        return {
            "arm_id": arm_id,
            "name": arm.name,
            "pulls": arm.pulls,
            "expected_value": round(expected_value, 4),
            "variance": round(variance, 6),
            "avg_reward": round(avg_reward, 4),
            "total_reward": round(arm.rewards, 2),
            "total_cost": round(total_cost, 2),
            "roi": round(roi, 2),
            "alpha": round(arm.alpha, 2),
            "beta": round(arm.beta, 2)
        }
    
    def get_performance_summary(self) -> Dict:
        """Get overall performance summary"""
        if not self.arms:
            return {"total_arms": 0, "total_trials": 0}
        
        arm_stats = [self.get_arm_statistics(arm_id) for arm_id in self.arms.keys()]
        
        # Find best arm
        best_arm = max(arm_stats, key=lambda x: x["expected_value"])
        
        # Calculate total metrics
        total_pulls = sum(arm["pulls"] for arm in arm_stats)
        total_reward = sum(arm["total_reward"] for arm in arm_stats)
        total_cost = sum(arm["total_cost"] for arm in arm_stats)
        
        return {
            "total_arms": len(self.arms),
            "total_trials": len(self.trials),
            "total_pulls": total_pulls,
            "total_reward": round(total_reward, 2),
            "total_cost": round(total_cost, 2),
            "overall_roi": round((total_reward - total_cost) / total_cost, 2) if total_cost > 0 else 0,
            "best_arm": {
                "id": best_arm["arm_id"],
                "name": best_arm["name"],
                "expected_value": best_arm["expected_value"]
            },
            "arm_statistics": arm_stats
        }
    
    def _beta_sample(self, alpha: float, beta: float) -> float:
        """Sample from Beta distribution"""
        if alpha <= 0 or beta <= 0:
            return 0.5
        
        x = random.gammavariate(alpha, 1)
        y = random.gammavariate(beta, 1)
        
        if x + y == 0:
            return 0.5
        
        return x / (x + y)


class ContextualBandit:
    """Contextual Multi-Armed Bandit"""
    
    def __init__(self):
        # Context-specific bandits
        self.context_bandits: Dict[str, ThompsonSampling] = {}
        self.default_bandit = ThompsonSampling()
    
    def add_arm(
        self,
        arm_id: str,
        name: str,
        description: str,
        cost: float = 0.0
    ):
        """Add arm to all context bandits"""
        # Add to default bandit
        self.default_bandit.add_arm(arm_id, name, description, cost)
        
        # Add to all context-specific bandits
        for bandit in self.context_bandits.values():
            bandit.add_arm(arm_id, name, description, cost)
    
    def select_arm(
        self,
        context: BanditContext,
        budget_constraint: Optional[float] = None
    ) -> str:
        """Select arm based on context"""
        # Get or create context-specific bandit
        context_key = self._get_context_key(context)
        
        if context_key not in self.context_bandits:
            # Create new bandit for this context
            self.context_bandits[context_key] = ThompsonSampling()
            
            # Copy arms from default bandit
            for arm_id, arm in self.default_bandit.arms.items():
                self.context_bandits[context_key].add_arm(
                    arm_id, arm.name, arm.description, arm.cost
                )
        
        bandit = self.context_bandits[context_key]
        return bandit.select_arm(context, budget_constraint)
    
    def update(
        self,
        arm_id: str,
        reward: float,
        cost: float,
        context: BanditContext
    ):
        """Update arm statistics for specific context"""
        context_key = self._get_context_key(context)
        
        if context_key in self.context_bandits:
            self.context_bandits[context_key].update(arm_id, reward, cost, context)
        
        # Also update default bandit
        self.default_bandit.update(arm_id, reward, cost, context)
    
    def get_context_performance(self, context: BanditContext) -> Dict:
        """Get performance for specific context"""
        context_key = self._get_context_key(context)
        
        if context_key in self.context_bandits:
            return self.context_bandits[context_key].get_performance_summary()
        
        return {"error": "No data for this context"}
    
    def _get_context_key(self, context: BanditContext) -> str:
        """Generate key from context"""
        parts = []
        if context.region:
            parts.append(f"region:{context.region}")
        if context.intent_type:
            parts.append(f"intent:{context.intent_type}")
        if context.domain:
            parts.append(f"domain:{context.domain}")
        if context.language:
            parts.append(f"lang:{context.language}")
        
        return "|".join(parts) if parts else "default"


class UpliftModeling:
    """Uplift modeling for incremental effect estimation"""
    
    @staticmethod
    def calculate_uplift(
        treatment_outcomes: List[float],
        control_outcomes: List[float]
    ) -> Dict:
        """
        Calculate uplift (incremental effect)
        
        Uplift = P(outcome | treatment) - P(outcome | control)
        """
        if not treatment_outcomes or not control_outcomes:
            return {
                "uplift": 0.0,
                "treatment_rate": 0.0,
                "control_rate": 0.0
            }
        
        treatment_rate = sum(treatment_outcomes) / len(treatment_outcomes)
        control_rate = sum(control_outcomes) / len(control_outcomes)
        
        uplift = treatment_rate - control_rate
        
        return {
            "uplift": round(uplift, 4),
            "treatment_rate": round(treatment_rate, 4),
            "control_rate": round(control_rate, 4),
            "relative_uplift": round(uplift / control_rate * 100, 2) if control_rate > 0 else 0
        }
    
    @staticmethod
    def rank_arms_by_uplift(
        arms_data: Dict[str, Dict]
    ) -> List[Dict]:
        """Rank arms by uplift score"""
        ranked = []
        
        for arm_id, data in arms_data.items():
            uplift = data.get("uplift", 0)
            cost = data.get("cost", 0)
            
            # Calculate uplift per dollar
            uplift_per_dollar = uplift / cost if cost > 0 else 0
            
            ranked.append({
                "arm_id": arm_id,
                "uplift": uplift,
                "cost": cost,
                "uplift_per_dollar": round(uplift_per_dollar, 4)
            })
        
        # Sort by uplift per dollar (descending)
        ranked.sort(key=lambda x: x["uplift_per_dollar"], reverse=True)
        
        return ranked


class DynamicBudgetAllocator:
    """Dynamic budget allocation based on arm performance"""
    
    @staticmethod
    def allocate_budget(
        total_budget: float,
        arm_statistics: List[Dict],
        allocation_strategy: str = "proportional"
    ) -> Dict[str, float]:
        """
        Allocate budget across arms
        
        Strategies:
        - proportional: Allocate proportional to expected value
        - top_k: Allocate to top K arms
        - thompson: Use Thompson Sampling for allocation
        """
        if allocation_strategy == "proportional":
            return DynamicBudgetAllocator._proportional_allocation(
                total_budget, arm_statistics
            )
        elif allocation_strategy == "top_k":
            return DynamicBudgetAllocator._top_k_allocation(
                total_budget, arm_statistics, k=3
            )
        else:
            return DynamicBudgetAllocator._proportional_allocation(
                total_budget, arm_statistics
            )
    
    @staticmethod
    def _proportional_allocation(
        total_budget: float,
        arm_statistics: List[Dict]
    ) -> Dict[str, float]:
        """Allocate proportional to expected value"""
        # Calculate total expected value
        total_ev = sum(arm["expected_value"] for arm in arm_statistics)
        
        if total_ev == 0:
            # Equal allocation if no data
            per_arm = total_budget / len(arm_statistics)
            return {arm["arm_id"]: per_arm for arm in arm_statistics}
        
        # Proportional allocation
        allocation = {}
        for arm in arm_statistics:
            proportion = arm["expected_value"] / total_ev
            allocation[arm["arm_id"]] = round(total_budget * proportion, 2)
        
        return allocation
    
    @staticmethod
    def _top_k_allocation(
        total_budget: float,
        arm_statistics: List[Dict],
        k: int = 3
    ) -> Dict[str, float]:
        """Allocate to top K arms"""
        # Sort by expected value
        sorted_arms = sorted(
            arm_statistics,
            key=lambda x: x["expected_value"],
            reverse=True
        )
        
        # Allocate to top K
        top_k = sorted_arms[:k]
        per_arm = total_budget / len(top_k)
        
        allocation = {arm["arm_id"]: per_arm for arm in top_k}
        
        # Zero allocation for others
        for arm in sorted_arms[k:]:
            allocation[arm["arm_id"]] = 0.0
        
        return allocation


# Global instances
thompson_sampling = ThompsonSampling()
contextual_bandit = ContextualBandit()
