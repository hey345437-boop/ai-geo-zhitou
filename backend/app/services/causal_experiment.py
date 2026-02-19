"""
Causal Experiment Platform
Implements A/B testing and causal inference for GEO optimization
"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
from enum import Enum
import statistics
import math
import logging

logger = logging.getLogger(__name__)


class ExperimentStatus(Enum):
    """Experiment status"""
    DRAFT = "draft"
    RUNNING = "running"
    COMPLETED = "completed"
    STOPPED = "stopped"
    FAILED = "failed"


@dataclass
class ExperimentPlan:
    """Experiment design plan"""
    id: str
    name: str
    description: str
    hypothesis: str
    treatment_variant: str
    control_variant: str
    sample_size: int
    duration_days: int
    metrics: List[str]
    created_at: datetime
    status: ExperimentStatus = ExperimentStatus.DRAFT
    metadata: Dict = field(default_factory=dict)


@dataclass
class ExperimentResult:
    """Experiment execution result"""
    experiment_id: str
    treatment_group: Dict
    control_group: Dict
    causal_effect: 'CausalEffect'
    completed_at: datetime
    duration_actual: int
    sample_size_actual: int


@dataclass
class CausalEffect:
    """Causal effect estimation"""
    ate: float  # Average Treatment Effect
    ate_ci_lower: float  # 95% CI lower bound
    ate_ci_upper: float  # 95% CI upper bound
    p_value: float
    is_significant: bool
    effect_size: str  # small, medium, large
    relative_lift: float  # Percentage improvement


class CausalExperiment:
    """Causal experiment design and analysis"""
    
    def __init__(self):
        self.experiments = {}
        self.results = {}
    
    def design_experiment(
        self,
        name: str,
        hypothesis: str,
        treatment_variant: str,
        control_variant: str,
        baseline_rate: float,
        mde: float = 0.05,  # Minimum Detectable Effect
        alpha: float = 0.05,  # Significance level
        power: float = 0.80,  # Statistical power
        duration_days: int = 14
    ) -> ExperimentPlan:
        """
        Design experiment with power analysis
        
        Args:
            name: Experiment name
            hypothesis: Hypothesis statement
            treatment_variant: Treatment description
            control_variant: Control description
            baseline_rate: Baseline conversion/success rate
            mde: Minimum detectable effect (e.g., 0.05 = 5% relative improvement)
            alpha: Type I error rate (false positive)
            power: Statistical power (1 - Type II error rate)
            duration_days: Experiment duration
        """
        # Calculate required sample size
        sample_size = self._calculate_sample_size(
            baseline_rate, mde, alpha, power
        )
        
        experiment_id = f"exp_{len(self.experiments) + 1}"
        
        plan = ExperimentPlan(
            id=experiment_id,
            name=name,
            description=f"Testing: {treatment_variant} vs {control_variant}",
            hypothesis=hypothesis,
            treatment_variant=treatment_variant,
            control_variant=control_variant,
            sample_size=sample_size,
            duration_days=duration_days,
            metrics=["visibility_score", "mention_rate", "position_score"],
            created_at=datetime.now(),
            status=ExperimentStatus.DRAFT,
            metadata={
                "baseline_rate": baseline_rate,
                "mde": mde,
                "alpha": alpha,
                "power": power
            }
        )
        
        self.experiments[experiment_id] = plan
        logger.info(f"Designed experiment {experiment_id}: {name}")
        logger.info(f"Required sample size: {sample_size} per group")
        
        return plan
    
    def run_experiment(
        self,
        experiment_id: str,
        treatment_data: List[Dict],
        control_data: List[Dict]
    ) -> ExperimentResult:
        """
        Execute experiment and analyze results
        
        Args:
            experiment_id: Experiment ID
            treatment_data: Treatment group data points
            control_data: Control group data points
        """
        plan = self.experiments.get(experiment_id)
        if not plan:
            raise ValueError(f"Experiment {experiment_id} not found")
        
        # Update status
        plan.status = ExperimentStatus.RUNNING
        
        # Extract metrics
        treatment_metrics = self._extract_metrics(treatment_data)
        control_metrics = self._extract_metrics(control_data)
        
        # Calculate causal effect
        causal_effect = self._calculate_causal_effect(
            treatment_metrics,
            control_metrics,
            plan.metadata.get("alpha", 0.05)
        )
        
        # Create result
        result = ExperimentResult(
            experiment_id=experiment_id,
            treatment_group={
                "size": len(treatment_data),
                "metrics": treatment_metrics
            },
            control_group={
                "size": len(control_data),
                "metrics": control_metrics
            },
            causal_effect=causal_effect,
            completed_at=datetime.now(),
            duration_actual=plan.duration_days,
            sample_size_actual=len(treatment_data) + len(control_data)
        )
        
        # Update status
        plan.status = ExperimentStatus.COMPLETED
        self.results[experiment_id] = result
        
        logger.info(f"Experiment {experiment_id} completed")
        logger.info(f"ATE: {causal_effect.ate:.4f}, p-value: {causal_effect.p_value:.4f}")
        
        return result
    
    def difference_in_differences(
        self,
        treatment_before: List[float],
        treatment_after: List[float],
        control_before: List[float],
        control_after: List[float]
    ) -> Dict:
        """Difference-in-Differences (DiD) analysis"""
        treatment_before_mean = statistics.mean(treatment_before)
        treatment_after_mean = statistics.mean(treatment_after)
        control_before_mean = statistics.mean(control_before)
        control_after_mean = statistics.mean(control_after)
        treatment_diff = treatment_after_mean - treatment_before_mean
        control_diff = control_after_mean - control_before_mean
        did = treatment_diff - control_diff
        
        # Calculate standard error (simplified)
        treatment_var = statistics.variance(treatment_after + treatment_before)
        control_var = statistics.variance(control_after + control_before)
        n_treatment = len(treatment_after) + len(treatment_before)
        n_control = len(control_after) + len(control_before)
        
        se = math.sqrt(treatment_var / n_treatment + control_var / n_control)
        z_score = 1.96
        ci_lower = did - z_score * se
        ci_upper = did + z_score * se
        z_stat = did / se if se > 0 else 0
        p_value = 2 * (1 - self._normal_cdf(abs(z_stat)))
        
        return {
            "did_estimate": did,
            "treatment_diff": treatment_diff,
            "control_diff": control_diff,
            "standard_error": se,
            "ci_lower": ci_lower,
            "ci_upper": ci_upper,
            "p_value": p_value,
            "is_significant": p_value < 0.05
        }
    
    def propensity_score_matching(
        self,
        treatment_units: List[Dict],
        control_units: List[Dict],
        covariates: List[str]
    ) -> Tuple[List[Tuple], float]:
        """Propensity Score Matching (PSM)"""
        treatment_scores = self._calculate_propensity_scores(
            treatment_units, covariates, is_treatment=True
        )
        control_scores = self._calculate_propensity_scores(
            control_units, covariates, is_treatment=False
        )
        matches = []
        used_control = set()
        
        for i, t_unit in enumerate(treatment_units):
            t_score = treatment_scores[i]
            best_match = None
            best_distance = float('inf')
            
            for j, c_unit in enumerate(control_units):
                if j in used_control:
                    continue
                
                c_score = control_scores[j]
                distance = abs(t_score - c_score)
                
                if distance < best_distance:
                    best_distance = distance
                    best_match = j
            
            if best_match is not None:
                matches.append((i, best_match))
                used_control.add(best_match)
        
        treatment_outcomes = []
        control_outcomes = []
        
        for t_idx, c_idx in matches:
            treatment_outcomes.append(treatment_units[t_idx].get('outcome', 0))
            control_outcomes.append(control_units[c_idx].get('outcome', 0))
        
        if treatment_outcomes and control_outcomes:
            ate = statistics.mean(treatment_outcomes) - statistics.mean(control_outcomes)
        else:
            ate = 0.0
        
        logger.info(f"PSM: Matched {len(matches)} pairs, ATE = {ate:.4f}")
        
        return matches, ate
    
    def _calculate_sample_size(
        self,
        baseline_rate: float,
        mde: float,
        alpha: float,
        power: float
    ) -> int:
        """Calculate required sample size per group"""
        z_alpha = 1.96
        z_beta = 0.84   # For power = 0.80
        
        # Expected rates
        p1 = baseline_rate
        p2 = baseline_rate * (1 + mde)
        
        p_pooled = (p1 + p2) / 2
        numerator = (z_alpha * math.sqrt(2 * p_pooled * (1 - p_pooled)) +
                    z_beta * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2
        denominator = (p2 - p1) ** 2
        
        n = math.ceil(numerator / denominator)
        return max(n, 100)
    
    def _extract_metrics(self, data: List[Dict]) -> Dict:
        """Extract metrics from data points"""
        if not data:
            return {
                "mean": 0.0,
                "std": 0.0,
                "count": 0
            }
        
        values = [dp.get('value', 0) for dp in data]
        
        return {
            "mean": statistics.mean(values),
            "std": statistics.stdev(values) if len(values) > 1 else 0.0,
            "count": len(values),
            "values": values
        }
    
    def _calculate_causal_effect(
        self,
        treatment_metrics: Dict,
        control_metrics: Dict,
        alpha: float
    ) -> CausalEffect:
        """Calculate Average Treatment Effect (ATE)"""
        # ATE = Mean(Treatment) - Mean(Control)
        ate = treatment_metrics["mean"] - control_metrics["mean"]
        
        # Calculate standard error
        n_treatment = treatment_metrics["count"]
        n_control = control_metrics["count"]
        
        if n_treatment == 0 or n_control == 0:
            return CausalEffect(
                ate=0.0,
                ate_ci_lower=0.0,
                ate_ci_upper=0.0,
                p_value=1.0,
                is_significant=False,
                effect_size="none",
                relative_lift=0.0
            )
        
        var_treatment = treatment_metrics["std"] ** 2
        var_control = control_metrics["std"] ** 2
        
        se = math.sqrt(var_treatment / n_treatment + var_control / n_control)
        
        # Calculate confidence interval
        z_score = 1.96  # 95% CI
        ci_lower = ate - z_score * se
        ci_upper = ate + z_score * se
        z_stat = ate / se if se > 0 else 0
        p_value = 2 * (1 - self._normal_cdf(abs(z_stat)))
        pooled_std = math.sqrt((var_treatment + var_control) / 2)
        cohens_d = ate / pooled_std if pooled_std > 0 else 0
        
        if abs(cohens_d) < 0.2:
            effect_size = "small"
        elif abs(cohens_d) < 0.5:
            effect_size = "medium"
        else:
            effect_size = "large"
        
        relative_lift = (ate / control_metrics["mean"] * 100) if control_metrics["mean"] > 0 else 0
        
        return CausalEffect(
            ate=round(ate, 4),
            ate_ci_lower=round(ci_lower, 4),
            ate_ci_upper=round(ci_upper, 4),
            p_value=round(p_value, 4),
            is_significant=p_value < alpha,
            effect_size=effect_size,
            relative_lift=round(relative_lift, 2)
        )
    
    def _calculate_propensity_scores(
        self,
        units: List[Dict],
        covariates: List[str],
        is_treatment: bool
    ) -> List[float]:
        """Calculate propensity scores"""
        scores = []
        
        for unit in units:
            score = 0.5
            for covariate in covariates:
                value = unit.get(covariate, 0)
                score += value * 0.1
            score = 1 / (1 + math.exp(-score))
            scores.append(score)
        
        return scores
    
    def _normal_cdf(self, x: float) -> float:
        """Cumulative distribution function for standard normal distribution"""
        return (1.0 + math.erf(x / math.sqrt(2.0))) / 2.0


# Global instance
causal_experiment = CausalExperiment()
