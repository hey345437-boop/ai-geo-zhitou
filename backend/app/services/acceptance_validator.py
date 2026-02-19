"""
Acceptance Criteria Validator

Validates that the system meets all acceptance criteria defined in requirements.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum
import time


class CriteriaStatus(Enum):
    """Status of acceptance criteria"""
    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"
    NOT_TESTED = "not_tested"


@dataclass
class AcceptanceCriteria:
    """Single acceptance criteria"""
    criteria_id: str
    category: str
    name: str
    threshold: float
    current_value: Optional[float] = None
    status: CriteriaStatus = CriteriaStatus.NOT_TESTED
    message: str = ""
    tested_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'criteria_id': self.criteria_id,
            'category': self.category,
            'name': self.name,
            'threshold': self.threshold,
            'current_value': self.current_value,
            'status': self.status.value,
            'message': self.message,
            'tested_at': self.tested_at.isoformat() if self.tested_at else None
        }


@dataclass
class AcceptanceReport:
    """Complete acceptance test report"""
    report_id: str
    criteria: List[AcceptanceCriteria]
    overall_status: CriteriaStatus
    passed_count: int
    failed_count: int
    warning_count: int
    generated_at: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'report_id': self.report_id,
            'criteria': [c.to_dict() for c in self.criteria],
            'overall_status': self.overall_status.value,
            'passed_count': self.passed_count,
            'failed_count': self.failed_count,
            'warning_count': self.warning_count,
            'pass_rate': round(self.passed_count / len(self.criteria) * 100, 1) if self.criteria else 0,
            'generated_at': self.generated_at.isoformat()
        }


class AcceptanceCriteriaValidator:
    """
    Validates system against acceptance criteria
    
    Checks:
    - Performance requirements (P95, P99, throughput, concurrency)
    - Accuracy requirements (precision, recall, F1)
    - Security requirements (HTTPS, CSRF, XSS, SQL injection)
    - Compliance requirements (GDPR, data retention)
    """
    
    def __init__(self):
        self.criteria = self._define_criteria()
    
    def _define_criteria(self) -> List[AcceptanceCriteria]:
        """Define all acceptance criteria"""
        return [
            # Performance criteria
            AcceptanceCriteria(
                criteria_id="perf_001",
                category="performance",
                name="API P95 Response Time",
                threshold=2.0,  # seconds
            ),
            AcceptanceCriteria(
                criteria_id="perf_002",
                category="performance",
                name="API P99 Response Time",
                threshold=5.0,  # seconds
            ),
            AcceptanceCriteria(
                criteria_id="perf_003",
                category="performance",
                name="Concurrent Users",
                threshold=1000,  # users
            ),
            AcceptanceCriteria(
                criteria_id="perf_004",
                category="performance",
                name="Throughput (QPS)",
                threshold=100,  # queries per second
            ),
            AcceptanceCriteria(
                criteria_id="perf_005",
                category="performance",
                name="Cache Hit Rate",
                threshold=0.80,  # 80%
            ),
            
            # Accuracy criteria
            AcceptanceCriteria(
                criteria_id="acc_001",
                category="accuracy",
                name="Citation Extraction Precision",
                threshold=0.85,  # 85%
            ),
            AcceptanceCriteria(
                criteria_id="acc_002",
                category="accuracy",
                name="Citation Extraction Recall",
                threshold=0.80,  # 80%
            ),
            AcceptanceCriteria(
                criteria_id="acc_003",
                category="accuracy",
                name="Brand Recognition Accuracy",
                threshold=0.90,  # 90%
            ),
            AcceptanceCriteria(
                criteria_id="acc_004",
                category="accuracy",
                name="Sentiment Analysis Accuracy",
                threshold=0.85,  # 85%
            ),
            
            # Security criteria
            AcceptanceCriteria(
                criteria_id="sec_001",
                category="security",
                name="HTTPS Enforcement",
                threshold=1.0,  # 100%
            ),
            AcceptanceCriteria(
                criteria_id="sec_002",
                category="security",
                name="CSRF Protection",
                threshold=1.0,  # 100%
            ),
            AcceptanceCriteria(
                criteria_id="sec_003",
                category="security",
                name="XSS Protection",
                threshold=1.0,  # 100%
            ),
            AcceptanceCriteria(
                criteria_id="sec_004",
                category="security",
                name="SQL Injection Protection",
                threshold=1.0,  # 100%
            ),
            AcceptanceCriteria(
                criteria_id="sec_005",
                category="security",
                name="Audit Logging",
                threshold=1.0,  # 100%
            ),
            
            # Compliance criteria
            AcceptanceCriteria(
                criteria_id="comp_001",
                category="compliance",
                name="Data Retention Enforcement",
                threshold=1.0,  # 100%
            ),
            AcceptanceCriteria(
                criteria_id="comp_002",
                category="compliance",
                name="Data Deletion (GDPR)",
                threshold=1.0,  # 100%
            ),
            AcceptanceCriteria(
                criteria_id="comp_003",
                category="compliance",
                name="Data Export (GDPR)",
                threshold=1.0,  # 100%
            ),
            AcceptanceCriteria(
                criteria_id="comp_004",
                category="compliance",
                name="Data Anonymization",
                threshold=1.0,  # 100%
            ),
        ]
    
    def validate_performance(
        self,
        p95_response_time: float,
        p99_response_time: float,
        concurrent_users: int,
        throughput_qps: float,
        cache_hit_rate: float
    ) -> List[AcceptanceCriteria]:
        """Validate performance criteria"""
        results = []
        
        # P95 response time
        criteria = self._get_criteria("perf_001")
        criteria.current_value = p95_response_time
        criteria.tested_at = datetime.utcnow()
        if p95_response_time <= criteria.threshold:
            criteria.status = CriteriaStatus.PASSED
            criteria.message = f"P95 response time {p95_response_time:.2f}s meets threshold"
        else:
            criteria.status = CriteriaStatus.FAILED
            criteria.message = f"P95 response time {p95_response_time:.2f}s exceeds threshold {criteria.threshold}s"
        results.append(criteria)
        
        # P99 response time
        criteria = self._get_criteria("perf_002")
        criteria.current_value = p99_response_time
        criteria.tested_at = datetime.utcnow()
        if p99_response_time <= criteria.threshold:
            criteria.status = CriteriaStatus.PASSED
            criteria.message = f"P99 response time {p99_response_time:.2f}s meets threshold"
        else:
            criteria.status = CriteriaStatus.FAILED
            criteria.message = f"P99 response time {p99_response_time:.2f}s exceeds threshold {criteria.threshold}s"
        results.append(criteria)
        
        # Concurrent users
        criteria = self._get_criteria("perf_003")
        criteria.current_value = concurrent_users
        criteria.tested_at = datetime.utcnow()
        if concurrent_users >= criteria.threshold:
            criteria.status = CriteriaStatus.PASSED
            criteria.message = f"Supports {concurrent_users} concurrent users"
        else:
            criteria.status = CriteriaStatus.FAILED
            criteria.message = f"Only supports {concurrent_users} concurrent users, need {criteria.threshold}"
        results.append(criteria)
        
        # Throughput
        criteria = self._get_criteria("perf_004")
        criteria.current_value = throughput_qps
        criteria.tested_at = datetime.utcnow()
        if throughput_qps >= criteria.threshold:
            criteria.status = CriteriaStatus.PASSED
            criteria.message = f"Throughput {throughput_qps:.1f} QPS meets threshold"
        else:
            criteria.status = CriteriaStatus.FAILED
            criteria.message = f"Throughput {throughput_qps:.1f} QPS below threshold {criteria.threshold}"
        results.append(criteria)
        
        # Cache hit rate
        criteria = self._get_criteria("perf_005")
        criteria.current_value = cache_hit_rate
        criteria.tested_at = datetime.utcnow()
        if cache_hit_rate >= criteria.threshold:
            criteria.status = CriteriaStatus.PASSED
            criteria.message = f"Cache hit rate {cache_hit_rate:.1%} meets threshold"
        else:
            criteria.status = CriteriaStatus.WARNING
            criteria.message = f"Cache hit rate {cache_hit_rate:.1%} below threshold {criteria.threshold:.1%}"
        results.append(criteria)
        
        return results
    
    def validate_accuracy(
        self,
        citation_precision: float,
        citation_recall: float,
        brand_accuracy: float,
        sentiment_accuracy: float
    ) -> List[AcceptanceCriteria]:
        """Validate accuracy criteria"""
        results = []
        
        # Citation precision
        criteria = self._get_criteria("acc_001")
        criteria.current_value = citation_precision
        criteria.tested_at = datetime.utcnow()
        if citation_precision >= criteria.threshold:
            criteria.status = CriteriaStatus.PASSED
            criteria.message = f"Citation precision {citation_precision:.1%} meets threshold"
        else:
            criteria.status = CriteriaStatus.FAILED
            criteria.message = f"Citation precision {citation_precision:.1%} below threshold {criteria.threshold:.1%}"
        results.append(criteria)
        
        # Citation recall
        criteria = self._get_criteria("acc_002")
        criteria.current_value = citation_recall
        criteria.tested_at = datetime.utcnow()
        if citation_recall >= criteria.threshold:
            criteria.status = CriteriaStatus.PASSED
            criteria.message = f"Citation recall {citation_recall:.1%} meets threshold"
        else:
            criteria.status = CriteriaStatus.FAILED
            criteria.message = f"Citation recall {citation_recall:.1%} below threshold {criteria.threshold:.1%}"
        results.append(criteria)
        
        # Brand accuracy
        criteria = self._get_criteria("acc_003")
        criteria.current_value = brand_accuracy
        criteria.tested_at = datetime.utcnow()
        if brand_accuracy >= criteria.threshold:
            criteria.status = CriteriaStatus.PASSED
            criteria.message = f"Brand accuracy {brand_accuracy:.1%} meets threshold"
        else:
            criteria.status = CriteriaStatus.FAILED
            criteria.message = f"Brand accuracy {brand_accuracy:.1%} below threshold {criteria.threshold:.1%}"
        results.append(criteria)
        
        # Sentiment accuracy
        criteria = self._get_criteria("acc_004")
        criteria.current_value = sentiment_accuracy
        criteria.tested_at = datetime.utcnow()
        if sentiment_accuracy >= criteria.threshold:
            criteria.status = CriteriaStatus.PASSED
            criteria.message = f"Sentiment accuracy {sentiment_accuracy:.1%} meets threshold"
        else:
            criteria.status = CriteriaStatus.FAILED
            criteria.message = f"Sentiment accuracy {sentiment_accuracy:.1%} below threshold {criteria.threshold:.1%}"
        results.append(criteria)
        
        return results
    
    def validate_security(
        self,
        https_enforced: bool,
        csrf_protected: bool,
        xss_protected: bool,
        sql_injection_protected: bool,
        audit_logging_enabled: bool
    ) -> List[AcceptanceCriteria]:
        """Validate security criteria"""
        results = []
        
        security_checks = [
            ("sec_001", https_enforced, "HTTPS enforcement"),
            ("sec_002", csrf_protected, "CSRF protection"),
            ("sec_003", xss_protected, "XSS protection"),
            ("sec_004", sql_injection_protected, "SQL injection protection"),
            ("sec_005", audit_logging_enabled, "Audit logging"),
        ]
        
        for criteria_id, is_enabled, name in security_checks:
            criteria = self._get_criteria(criteria_id)
            criteria.current_value = 1.0 if is_enabled else 0.0
            criteria.tested_at = datetime.utcnow()
            if is_enabled:
                criteria.status = CriteriaStatus.PASSED
                criteria.message = f"{name} is enabled"
            else:
                criteria.status = CriteriaStatus.FAILED
                criteria.message = f"{name} is NOT enabled"
            results.append(criteria)
        
        return results
    
    def validate_compliance(
        self,
        retention_enforced: bool,
        deletion_working: bool,
        export_working: bool,
        anonymization_working: bool
    ) -> List[AcceptanceCriteria]:
        """Validate compliance criteria"""
        results = []
        
        compliance_checks = [
            ("comp_001", retention_enforced, "Data retention enforcement"),
            ("comp_002", deletion_working, "Data deletion (GDPR)"),
            ("comp_003", export_working, "Data export (GDPR)"),
            ("comp_004", anonymization_working, "Data anonymization"),
        ]
        
        for criteria_id, is_working, name in compliance_checks:
            criteria = self._get_criteria(criteria_id)
            criteria.current_value = 1.0 if is_working else 0.0
            criteria.tested_at = datetime.utcnow()
            if is_working:
                criteria.status = CriteriaStatus.PASSED
                criteria.message = f"{name} is working"
            else:
                criteria.status = CriteriaStatus.FAILED
                criteria.message = f"{name} is NOT working"
            results.append(criteria)
        
        return results
    
    def generate_report(self) -> AcceptanceReport:
        """Generate complete acceptance report"""
        passed = sum(1 for c in self.criteria if c.status == CriteriaStatus.PASSED)
        failed = sum(1 for c in self.criteria if c.status == CriteriaStatus.FAILED)
        warning = sum(1 for c in self.criteria if c.status == CriteriaStatus.WARNING)
        
        # Determine overall status
        if failed > 0:
            overall_status = CriteriaStatus.FAILED
        elif warning > 0:
            overall_status = CriteriaStatus.WARNING
        else:
            overall_status = CriteriaStatus.PASSED
        
        report = AcceptanceReport(
            report_id=f"report_{datetime.utcnow().timestamp()}",
            criteria=self.criteria,
            overall_status=overall_status,
            passed_count=passed,
            failed_count=failed,
            warning_count=warning,
            generated_at=datetime.utcnow()
        )
        
        return report
    
    def _get_criteria(self, criteria_id: str) -> AcceptanceCriteria:
        """Get criteria by ID"""
        for criteria in self.criteria:
            if criteria.criteria_id == criteria_id:
                return criteria
        raise ValueError(f"Criteria {criteria_id} not found")
