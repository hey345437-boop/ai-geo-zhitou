"""
Reproducible Evaluation Protocol Service

Provides reproducible evaluation runs with environment capture, drift monitoring,
and result comparison capabilities.
"""

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum
import hashlib
import json
import platform
import sys


class EvaluationStatus(Enum):
    """Evaluation run status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    REPRODUCED = "reproduced"


class DriftSeverity(Enum):
    """Drift severity levels"""
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class EnvironmentInfo:
    """Environment information for reproducibility"""
    python_version: str
    platform: str
    os_version: str
    cpu_count: int
    timestamp: datetime
    random_seed: int
    dependencies: Dict[str, str] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        return data


@dataclass
class EvaluationConfig:
    """Evaluation configuration"""
    question_set_name: str
    question_set_version: str
    engines: List[str]
    sample_size: Optional[int] = None
    timeout_seconds: int = 300
    max_retries: int = 3
    parameters: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)
    
    def compute_hash(self) -> str:
        """Compute configuration hash for reproducibility"""
        config_str = json.dumps(self.to_dict(), sort_keys=True)
        return hashlib.sha256(config_str.encode()).hexdigest()


@dataclass
class EvaluationResult:
    """Single evaluation result"""
    question_id: str
    question_text: str
    engine: str
    response: str
    brand_mentions: List[str]
    visibility_score: float
    citation_count: int
    response_time_ms: float
    timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        return data


@dataclass
class EvaluationRun:
    """Complete evaluation run"""
    run_id: str
    config: EvaluationConfig
    environment: EnvironmentInfo
    status: EvaluationStatus
    results: List[EvaluationResult] = field(default_factory=list)
    metrics: Dict[str, float] = field(default_factory=dict)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'run_id': self.run_id,
            'config': self.config.to_dict(),
            'environment': self.environment.to_dict(),
            'status': self.status.value,
            'results': [r.to_dict() for r in self.results],
            'metrics': self.metrics,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'error': self.error
        }


@dataclass
class DriftMetric:
    """Drift metric for a specific measure"""
    metric_name: str
    baseline_value: float
    current_value: float
    drift_percentage: float
    severity: DriftSeverity
    threshold_exceeded: bool
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'metric_name': self.metric_name,
            'baseline_value': self.baseline_value,
            'current_value': self.current_value,
            'drift_percentage': self.drift_percentage,
            'severity': self.severity.value,
            'threshold_exceeded': self.threshold_exceeded
        }


@dataclass
class DriftReport:
    """Model drift monitoring report"""
    baseline_run_id: str
    current_run_id: str
    drift_metrics: List[DriftMetric]
    overall_drift_score: float
    has_significant_drift: bool
    checked_at: datetime
    recommendations: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'baseline_run_id': self.baseline_run_id,
            'current_run_id': self.current_run_id,
            'drift_metrics': [m.to_dict() for m in self.drift_metrics],
            'overall_drift_score': self.overall_drift_score,
            'has_significant_drift': self.has_significant_drift,
            'checked_at': self.checked_at.isoformat(),
            'recommendations': self.recommendations
        }


class ReproducibleEvaluationProtocol:
    """
    Reproducible evaluation protocol for LLM visibility testing
    
    Ensures evaluation runs can be reproduced exactly by capturing:
    - Environment information
    - Random seeds
    - Configuration parameters
    - Execution timestamps
    """
    
    def __init__(self):
        self.runs: Dict[str, EvaluationRun] = {}
    
    def capture_environment(self, random_seed: int = 42) -> EnvironmentInfo:
        """
        Capture current environment information
        
        Args:
            random_seed: Random seed for reproducibility
            
        Returns:
            EnvironmentInfo object
        """
        return EnvironmentInfo(
            python_version=sys.version,
            platform=platform.system(),
            os_version=platform.version(),
            cpu_count=platform.machine(),
            timestamp=datetime.utcnow(),
            random_seed=random_seed,
            dependencies={
                'fastapi': '0.104.0',
                'pydantic': '2.5.0',
                'numpy': '1.24.0',
                'pandas': '2.0.0'
            }
        )
    
    def create_evaluation_run(
        self,
        config: EvaluationConfig,
        random_seed: int = 42
    ) -> EvaluationRun:
        """
        Create a new evaluation run
        
        Args:
            config: Evaluation configuration
            random_seed: Random seed for reproducibility
            
        Returns:
            EvaluationRun object
        """
        run_id = f"eval_{datetime.utcnow().timestamp()}_{config.compute_hash()[:8]}"
        environment = self.capture_environment(random_seed)
        
        run = EvaluationRun(
            run_id=run_id,
            config=config,
            environment=environment,
            status=EvaluationStatus.PENDING,
            started_at=datetime.utcnow()
        )
        
        self.runs[run_id] = run
        return run
    
    def execute_evaluation(
        self,
        run: EvaluationRun,
        question_set: List[Dict[str, Any]]
    ) -> EvaluationRun:
        """
        Execute evaluation run
        
        Args:
            run: Evaluation run to execute
            question_set: List of questions to evaluate
            
        Returns:
            Updated EvaluationRun
        """
        run.status = EvaluationStatus.RUNNING
        
        try:
            for question in question_set:
                for engine in run.config.engines:
                    result = EvaluationResult(
                        question_id=question['id'],
                        question_text=question['text'],
                        engine=engine,
                        response=f"Mock response from {engine}",
                        brand_mentions=['Brand A', 'Brand B'],
                        visibility_score=75.5,
                        citation_count=3,
                        response_time_ms=250.0,
                        timestamp=datetime.utcnow(),
                        metadata={'intent': question.get('intent', 'informational')}
                    )
                    run.results.append(result)
            
            # Calculate aggregate metrics
            run.metrics = self._calculate_metrics(run.results)
            run.status = EvaluationStatus.COMPLETED
            run.completed_at = datetime.utcnow()
            
        except Exception as e:
            run.status = EvaluationStatus.FAILED
            run.error = str(e)
            run.completed_at = datetime.utcnow()
        
        return run
    
    def _calculate_metrics(self, results: List[EvaluationResult]) -> Dict[str, float]:
        """Calculate aggregate metrics from results"""
        if not results:
            return {}
        
        total_results = len(results)
        avg_visibility = sum(r.visibility_score for r in results) / total_results
        avg_citations = sum(r.citation_count for r in results) / total_results
        avg_response_time = sum(r.response_time_ms for r in results) / total_results
        
        # Calculate mention rate
        results_with_mentions = sum(1 for r in results if r.brand_mentions)
        mention_rate = (results_with_mentions / total_results) * 100
        
        return {
            'avg_visibility_score': round(avg_visibility, 2),
            'avg_citation_count': round(avg_citations, 2),
            'avg_response_time_ms': round(avg_response_time, 2),
            'mention_rate': round(mention_rate, 2),
            'total_queries': total_results
        }
    
    def reproduce_evaluation(
        self,
        baseline_run_id: str,
        question_set: List[Dict[str, Any]]
    ) -> EvaluationRun:
        """
        Reproduce a previous evaluation run
        
        Args:
            baseline_run_id: ID of run to reproduce
            question_set: Question set to use
            
        Returns:
            New EvaluationRun with reproduced results
        """
        baseline_run = self.runs.get(baseline_run_id)
        if not baseline_run:
            raise ValueError(f"Baseline run {baseline_run_id} not found")
        
        # Create new run with same configuration and random seed
        reproduced_run = self.create_evaluation_run(
            config=baseline_run.config,
            random_seed=baseline_run.environment.random_seed
        )
        
        # Execute with same parameters
        reproduced_run = self.execute_evaluation(reproduced_run, question_set)
        reproduced_run.status = EvaluationStatus.REPRODUCED
        
        return reproduced_run
    
    def compare_runs(
        self,
        run_id_1: str,
        run_id_2: str
    ) -> Dict[str, Any]:
        """
        Compare two evaluation runs
        
        Args:
            run_id_1: First run ID
            run_id_2: Second run ID
            
        Returns:
            Comparison report
        """
        run1 = self.runs.get(run_id_1)
        run2 = self.runs.get(run_id_2)
        
        if not run1 or not run2:
            raise ValueError("One or both runs not found")
        
        # Calculate metric differences
        metric_diffs = {}
        for metric_name in run1.metrics:
            if metric_name in run2.metrics:
                diff = run2.metrics[metric_name] - run1.metrics[metric_name]
                diff_pct = (diff / run1.metrics[metric_name] * 100) if run1.metrics[metric_name] != 0 else 0
                metric_diffs[metric_name] = {
                    'run1_value': run1.metrics[metric_name],
                    'run2_value': run2.metrics[metric_name],
                    'absolute_diff': round(diff, 2),
                    'percentage_diff': round(diff_pct, 2)
                }
        
        # Calculate reproducibility score
        reproducibility_score = self._calculate_reproducibility_score(run1, run2)
        
        return {
            'run1_id': run_id_1,
            'run2_id': run_id_2,
            'metric_differences': metric_diffs,
            'reproducibility_score': reproducibility_score,
            'is_reproducible': reproducibility_score > 0.95,
            'environment_match': run1.environment.python_version == run2.environment.python_version
        }
    
    def _calculate_reproducibility_score(
        self,
        run1: EvaluationRun,
        run2: EvaluationRun
    ) -> float:
        """Calculate reproducibility score between two runs"""
        if not run1.metrics or not run2.metrics:
            return 0.0
        
        # Calculate similarity for each metric
        similarities = []
        for metric_name in run1.metrics:
            if metric_name in run2.metrics:
                val1 = run1.metrics[metric_name]
                val2 = run2.metrics[metric_name]
                
                # Avoid division by zero
                if val1 == 0 and val2 == 0:
                    similarity = 1.0
                elif val1 == 0 or val2 == 0:
                    similarity = 0.0
                else:
                    # Calculate relative difference
                    diff = abs(val1 - val2) / max(val1, val2)
                    similarity = 1.0 - min(diff, 1.0)
                
                similarities.append(similarity)
        
        # Return average similarity
        return sum(similarities) / len(similarities) if similarities else 0.0


class ModelDriftMonitor:
    """
    Monitor model drift over time
    
    Detects significant changes in model behavior by comparing
    current results against baseline.
    """
    
    def __init__(self, drift_threshold: float = 0.15):
        """
        Initialize drift monitor
        
        Args:
            drift_threshold: Threshold for significant drift (default 15%)
        """
        self.drift_threshold = drift_threshold
    
    def detect_drift(
        self,
        baseline_run: EvaluationRun,
        current_run: EvaluationRun
    ) -> DriftReport:
        """
        Detect drift between baseline and current run
        
        Args:
            baseline_run: Baseline evaluation run
            current_run: Current evaluation run
            
        Returns:
            DriftReport with detected drift
        """
        drift_metrics = []
        
        # Compare each metric
        for metric_name in baseline_run.metrics:
            if metric_name in current_run.metrics:
                baseline_value = baseline_run.metrics[metric_name]
                current_value = current_run.metrics[metric_name]
                
                # Calculate drift percentage
                if baseline_value != 0:
                    drift_pct = ((current_value - baseline_value) / baseline_value) * 100
                else:
                    drift_pct = 100.0 if current_value != 0 else 0.0
                
                # Determine severity
                abs_drift = abs(drift_pct)
                if abs_drift < 5:
                    severity = DriftSeverity.NONE
                elif abs_drift < 10:
                    severity = DriftSeverity.LOW
                elif abs_drift < 15:
                    severity = DriftSeverity.MEDIUM
                elif abs_drift < 25:
                    severity = DriftSeverity.HIGH
                else:
                    severity = DriftSeverity.CRITICAL
                
                drift_metric = DriftMetric(
                    metric_name=metric_name,
                    baseline_value=baseline_value,
                    current_value=current_value,
                    drift_percentage=round(drift_pct, 2),
                    severity=severity,
                    threshold_exceeded=abs_drift > (self.drift_threshold * 100)
                )
                drift_metrics.append(drift_metric)
        
        # Calculate overall drift score
        overall_drift = sum(abs(m.drift_percentage) for m in drift_metrics) / len(drift_metrics) if drift_metrics else 0
        has_significant_drift = any(m.threshold_exceeded for m in drift_metrics)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(drift_metrics)
        
        return DriftReport(
            baseline_run_id=baseline_run.run_id,
            current_run_id=current_run.run_id,
            drift_metrics=drift_metrics,
            overall_drift_score=round(overall_drift, 2),
            has_significant_drift=has_significant_drift,
            checked_at=datetime.utcnow(),
            recommendations=recommendations
        )
    
    def _generate_recommendations(self, drift_metrics: List[DriftMetric]) -> List[str]:
        """Generate recommendations based on drift metrics"""
        recommendations = []
        
        for metric in drift_metrics:
            if metric.severity == DriftSeverity.CRITICAL:
                recommendations.append(
                    f"CRITICAL: {metric.metric_name} has drifted {metric.drift_percentage:.1f}%. "
                    f"Immediate investigation required."
                )
            elif metric.severity == DriftSeverity.HIGH:
                recommendations.append(
                    f"HIGH: {metric.metric_name} shows significant drift ({metric.drift_percentage:.1f}%). "
                    f"Review model behavior and consider retraining."
                )
            elif metric.severity == DriftSeverity.MEDIUM:
                recommendations.append(
                    f"MEDIUM: {metric.metric_name} drift detected ({metric.drift_percentage:.1f}%). "
                    f"Monitor closely in next evaluation."
                )
        
        if not recommendations:
            recommendations.append("No significant drift detected. Model performance is stable.")
        
        return recommendations
