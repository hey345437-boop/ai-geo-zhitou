"""
Vertical Domain Benchmark Service

Provides domain-specific benchmarking and classification for different industry verticals.
"""

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum


class DomainType(Enum):
    """Vertical domain types"""
    ECOMMERCE = "ecommerce"
    HEALTHCARE = "healthcare"
    FINANCE = "finance"
    EDUCATION = "education"
    TRAVEL = "travel"
    FOOD_RESTAURANT = "food_restaurant"
    REAL_ESTATE = "real_estate"
    TECHNOLOGY = "technology"
    LEGAL = "legal"
    AUTOMOTIVE = "automotive"


@dataclass
class DomainMetric:
    """Domain-specific metric"""
    metric_name: str
    value: float
    industry_average: float
    top_performer: float
    percentile: float  # 0-100
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)


@dataclass
class DomainBenchmark:
    """Benchmark data for a domain"""
    domain: DomainType
    brand_id: str
    overall_score: float
    metrics: List[DomainMetric]
    rank: int
    total_competitors: int
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    opportunities: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        data = asdict(self)
        data['domain'] = self.domain.value
        data['created_at'] = self.created_at.isoformat()
        data['metrics'] = [m.to_dict() for m in self.metrics]
        return data


@dataclass
class LocalBenchmark:
    """Vertical × Geographic benchmark"""
    domain: DomainType
    region: str  # country, state, or city
    brand_id: str
    visibility_score: float
    regional_average: float
    regional_rank: int
    total_regional_competitors: int
    top_regional_brands: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        data = asdict(self)
        data['domain'] = self.domain.value
        return data


class DomainClassifier:
    """
    Classify content into vertical domains
    
    Uses keyword matching and pattern recognition to determine
    the industry vertical of content.
    """
    
    def __init__(self):
        # Domain-specific keywords
        self.domain_keywords = {
            DomainType.ECOMMERCE: [
                'shop', 'buy', 'cart', 'checkout', 'product', 'price',
                'shipping', 'order', 'payment', 'discount', 'sale'
            ],
            DomainType.HEALTHCARE: [
                'health', 'medical', 'doctor', 'patient', 'treatment',
                'diagnosis', 'hospital', 'clinic', 'medicine', 'symptoms'
            ],
            DomainType.FINANCE: [
                'bank', 'loan', 'credit', 'investment', 'insurance',
                'mortgage', 'savings', 'interest', 'financial', 'account'
            ],
            DomainType.EDUCATION: [
                'school', 'university', 'course', 'student', 'teacher',
                'learning', 'education', 'degree', 'class', 'tuition'
            ],
            DomainType.TRAVEL: [
                'hotel', 'flight', 'booking', 'vacation', 'destination',
                'travel', 'tourism', 'trip', 'resort', 'airline'
            ],
            DomainType.FOOD_RESTAURANT: [
                'restaurant', 'menu', 'food', 'dining', 'cuisine',
                'chef', 'recipe', 'meal', 'delivery', 'reservation'
            ],
            DomainType.REAL_ESTATE: [
                'property', 'house', 'apartment', 'rent', 'buy',
                'real estate', 'mortgage', 'listing', 'agent', 'home'
            ],
            DomainType.TECHNOLOGY: [
                'software', 'app', 'technology', 'digital', 'platform',
                'cloud', 'api', 'data', 'system', 'solution'
            ],
            DomainType.LEGAL: [
                'law', 'legal', 'attorney', 'lawyer', 'court',
                'case', 'contract', 'litigation', 'compliance', 'regulation'
            ],
            DomainType.AUTOMOTIVE: [
                'car', 'vehicle', 'auto', 'dealer', 'automotive',
                'engine', 'repair', 'service', 'parts', 'driving'
            ]
        }
    
    def classify(
        self,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> DomainType:
        """
        Classify content into a domain
        
        Args:
            content: Text content to classify
            metadata: Optional metadata (e.g., category, tags)
            
        Returns:
            Classified DomainType
        """
        content_lower = content.lower()
        
        # Count keyword matches for each domain
        domain_scores = {}
        for domain, keywords in self.domain_keywords.items():
            score = sum(
                content_lower.count(keyword) for keyword in keywords
            )
            domain_scores[domain] = score
        
        # Return domain with highest score
        if domain_scores:
            best_domain = max(domain_scores.items(), key=lambda x: x[1])
            if best_domain[1] > 0:
                return best_domain[0]
        
        # Default to technology if no clear match
        return DomainType.TECHNOLOGY


class DomainBenchmarkSystem:
    """
    Domain-specific benchmarking system
    
    Provides industry-specific metrics and comparisons.
    """
    
    def __init__(self):
        self.industry_averages = {
            DomainType.ECOMMERCE: {
                'visibility_score': 65.0,
                'mention_rate': 45.0,
                'citation_rate': 35.0,
                'conversion_attribution': 12.0
            },
            DomainType.HEALTHCARE: {
                'visibility_score': 70.0,
                'mention_rate': 50.0,
                'citation_rate': 60.0,
                'trust_score': 75.0
            },
            DomainType.FINANCE: {
                'visibility_score': 68.0,
                'mention_rate': 48.0,
                'citation_rate': 55.0,
                'compliance_score': 85.0
            },
            DomainType.FOOD_RESTAURANT: {
                'visibility_score': 60.0,
                'mention_rate': 40.0,
                'citation_rate': 30.0,
                'review_score': 70.0
            }
        }
        
        self.top_performers = {
            domain: {
                metric: value * 1.4
                for metric, value in metrics.items()
            }
            for domain, metrics in self.industry_averages.items()
        }
    
    def calculate_benchmark(
        self,
        brand_id: str,
        domain: DomainType,
        brand_metrics: Dict[str, float]
    ) -> DomainBenchmark:
        """
        Calculate domain-specific benchmark
        
        Args:
            brand_id: Brand identifier
            domain: Domain type
            brand_metrics: Brand's current metrics
            
        Returns:
            DomainBenchmark with comparison data
        """
        # Get industry averages for this domain
        industry_avg = self.industry_averages.get(
            domain,
            self.industry_averages[DomainType.ECOMMERCE]
        )
        top_perf = self.top_performers.get(
            domain,
            self.top_performers[DomainType.ECOMMERCE]
        )
        
        # Calculate domain-specific metrics
        metrics = []
        total_percentile = 0
        
        for metric_name, brand_value in brand_metrics.items():
            industry_value = industry_avg.get(metric_name, 50.0)
            top_value = top_perf.get(metric_name, 80.0)
            
            # Calculate percentile (0-100)
            if top_value > industry_value:
                percentile = min(
                    100,
                    ((brand_value - industry_value) / (top_value - industry_value)) * 100
                )
            else:
                percentile = 50.0
            
            percentile = max(0, percentile)
            total_percentile += percentile
            metric = DomainMetric(
                metric_name=metric_name,
                value=brand_value,
                industry_average=industry_value,
                top_performer=top_value,
                percentile=round(percentile, 1)
            )
            metrics.append(metric)
        
        # Calculate overall score
        overall_score = total_percentile / len(metrics) if metrics else 50.0
        rank = max(1, int(100 - overall_score))
        total_competitors = 100
        
        # Identify strengths and weaknesses
        strengths = [
            m.metric_name for m in metrics
            if m.percentile >= 75
        ]
        weaknesses = [
            m.metric_name for m in metrics
            if m.percentile < 50
        ]
        
        # Generate opportunities
        opportunities = self._generate_opportunities(domain, metrics)
        
        return DomainBenchmark(
            domain=domain,
            brand_id=brand_id,
            overall_score=round(overall_score, 1),
            metrics=metrics,
            rank=rank,
            total_competitors=total_competitors,
            strengths=strengths,
            weaknesses=weaknesses,
            opportunities=opportunities
        )
    
    def _generate_opportunities(
        self,
        domain: DomainType,
        metrics: List[DomainMetric]
    ) -> List[str]:
        """Generate improvement opportunities"""
        opportunities = []
        
        # Domain-specific opportunities
        domain_opportunities = {
            DomainType.ECOMMERCE: [
                "Optimize product descriptions for LLM queries",
                "Add detailed specification tables",
                "Include customer review highlights",
                "Create comparison guides"
            ],
            DomainType.HEALTHCARE: [
                "Add medical credentials and certifications",
                "Include evidence-based citations",
                "Create symptom checker content",
                "Add FAQ sections for common conditions"
            ],
            DomainType.FINANCE: [
                "Add financial calculators and tools",
                "Include regulatory compliance information",
                "Create educational content on financial topics",
                "Add expert analysis and insights"
            ],
            DomainType.FOOD_RESTAURANT: [
                "Add detailed menu with ingredients",
                "Include chef profiles and expertise",
                "Create recipe content",
                "Add dietary information and allergens"
            ]
        }
        
        # Get domain-specific opportunities
        base_opportunities = domain_opportunities.get(
            domain,
            ["Improve content quality", "Add structured data", "Enhance citations"]
        )
        
        # Add metric-specific opportunities
        for metric in metrics:
            if metric.percentile < 50:
                opportunities.append(
                    f"Improve {metric.metric_name} (currently at {metric.percentile:.0f}th percentile)"
                )
        
        # Combine and limit to top 5
        all_opportunities = base_opportunities + opportunities
        return all_opportunities[:5]
    
    def calculate_local_benchmark(
        self,
        brand_id: str,
        domain: DomainType,
        region: str,
        visibility_score: float
    ) -> LocalBenchmark:
        """
        Calculate vertical × geographic benchmark
        
        Args:
            brand_id: Brand identifier
            domain: Domain type
            region: Geographic region
            visibility_score: Brand's visibility score
            
        Returns:
            LocalBenchmark with regional comparison
        """
        regional_multiplier = {
            'US': 1.0,
            'UK': 0.95,
            'CA': 0.90,
            'AU': 0.85,
            'CN': 0.80
        }
        
        base_avg = self.industry_averages.get(
            domain,
            self.industry_averages[DomainType.ECOMMERCE]
        )['visibility_score']
        
        region_code = region.split('-')[0] if '-' in region else region[:2].upper()
        multiplier = regional_multiplier.get(region_code, 0.85)
        regional_average = base_avg * multiplier
        
        # Calculate regional rank
        if visibility_score >= regional_average * 1.2:
            regional_rank = 5
        elif visibility_score >= regional_average:
            regional_rank = 15
        elif visibility_score >= regional_average * 0.8:
            regional_rank = 35
        else:
            regional_rank = 60
        
        top_brands = [f"Regional Leader {i}" for i in range(1, 4)]
        
        return LocalBenchmark(
            domain=domain,
            region=region,
            brand_id=brand_id,
            visibility_score=visibility_score,
            regional_average=round(regional_average, 1),
            regional_rank=regional_rank,
            total_regional_competitors=100,
            top_regional_brands=top_brands
        )
    
    def get_best_practices(self, domain: DomainType) -> List[str]:
        """Get domain-specific best practices"""
        best_practices = {
            DomainType.ECOMMERCE: [
                "Include detailed product specifications",
                "Add high-quality product images with alt text",
                "Create comparison tables for similar products",
                "Include customer reviews and ratings",
                "Add shipping and return policy information",
                "Use Product schema markup"
            ],
            DomainType.HEALTHCARE: [
                "Cite medical research and studies",
                "Include doctor credentials and expertise",
                "Add medical disclaimers where appropriate",
                "Use MedicalWebPage schema markup",
                "Provide evidence-based information",
                "Include symptom and treatment details"
            ],
            DomainType.FINANCE: [
                "Include regulatory disclosures",
                "Cite financial data sources",
                "Add financial calculators",
                "Use FinancialService schema markup",
                "Provide clear fee structures",
                "Include risk warnings"
            ],
            DomainType.FOOD_RESTAURANT: [
                "Add detailed menu with prices",
                "Include ingredient lists",
                "Add chef profiles and expertise",
                "Use Restaurant schema markup",
                "Include dietary information",
                "Add reservation information"
            ]
        }
        
        return best_practices.get(
            domain,
            [
                "Add structured data markup",
                "Include authoritative citations",
                "Create comprehensive content",
                "Optimize for user intent"
            ]
        )
