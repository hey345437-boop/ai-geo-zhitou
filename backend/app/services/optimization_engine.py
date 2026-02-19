"""
Optimization Engine Service

Generates actionable recommendations for improving LLM visibility,
including content optimization, schema markup, and compliance checking.
"""

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum
import re


class RecommendationType(Enum):
    """Types of optimization recommendations"""
    CONTENT_QUALITY = "content_quality"
    SCHEMA_MARKUP = "schema_markup"
    CITATION_IMPROVEMENT = "citation_improvement"
    STRUCTURE_FIX = "structure_fix"
    KEYWORD_OPTIMIZATION = "keyword_optimization"
    ENTITY_ENHANCEMENT = "entity_enhancement"
    COMPLIANCE_FIX = "compliance_fix"


class RecommendationPriority(Enum):
    """Priority levels for recommendations"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ComplianceIssueType(Enum):
    """Types of compliance issues"""
    HIDDEN_TEXT = "hidden_text"
    KEYWORD_STUFFING = "keyword_stuffing"
    MISLEADING_CONTENT = "misleading_content"
    DUPLICATE_CONTENT = "duplicate_content"
    THIN_CONTENT = "thin_content"


@dataclass
class Recommendation:
    """Single optimization recommendation"""
    recommendation_id: str
    type: RecommendationType
    priority: RecommendationPriority
    title: str
    description: str
    action: str
    expected_impact: float  # 0-100 score improvement
    effort_level: str  # low, medium, high
    code_example: Optional[str] = None
    is_white_hat: bool = True
    compliance_notes: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        data = asdict(self)
        data['type'] = self.type.value
        data['priority'] = self.priority.value
        data['created_at'] = self.created_at.isoformat()
        return data


@dataclass
class ComplianceIssue:
    """Compliance issue detected in content"""
    issue_type: ComplianceIssueType
    severity: str  # low, medium, high, critical
    description: str
    location: str
    fix_suggestion: str
    is_white_hat_violation: bool
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        data = asdict(self)
        data['issue_type'] = self.issue_type.value
        return data


@dataclass
class ComplianceReport:
    """Content compliance report"""
    content_id: str
    compliance_score: float  # 0-100
    issues: List[ComplianceIssue]
    is_compliant: bool
    checked_at: datetime
    recommendations: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'content_id': self.content_id,
            'compliance_score': self.compliance_score,
            'issues': [i.to_dict() for i in self.issues],
            'is_compliant': self.is_compliant,
            'checked_at': self.checked_at.isoformat(),
            'recommendations': self.recommendations
        }


class RecommendationGenerator:
    """
    Generate optimization recommendations based on content analysis
    
    Analyzes content quality, competitive gaps, and generates prioritized
    recommendations for improving LLM visibility.
    """
    
    def __init__(self):
        self.recommendations: Dict[str, List[Recommendation]] = {}
    
    def generate_recommendations(
        self,
        project_id: str,
        content_analysis: Dict[str, Any],
        visibility_score: float,
        competitive_data: Optional[Dict[str, Any]] = None
    ) -> List[Recommendation]:
        """
        Generate optimization recommendations
        
        Args:
            project_id: Project identifier
            content_analysis: Content analysis results
            visibility_score: Current visibility score
            competitive_data: Competitive analysis data
            
        Returns:
            List of prioritized recommendations
        """
        recommendations = []
        
        # Content quality recommendations
        if content_analysis.get('relevance_score', 100) < 70:
            recommendations.append(self._create_content_quality_recommendation(
                content_analysis
            ))
        
        # Schema markup recommendations
        if not content_analysis.get('has_schema', False):
            recommendations.append(self._create_schema_recommendation(
                content_analysis.get('content_type', 'article')
            ))
        
        # Citation improvement recommendations
        if content_analysis.get('authority_score', 100) < 60:
            recommendations.append(self._create_citation_recommendation())
        
        # Structure recommendations
        if content_analysis.get('structure_score', 100) < 70:
            recommendations.append(self._create_structure_recommendation(
                content_analysis
            ))
        
        # Keyword optimization
        if visibility_score < 50:
            recommendations.append(self._create_keyword_recommendation(
                competitive_data
            ))
        
        # Entity enhancement
        if content_analysis.get('entity_count', 0) < 5:
            recommendations.append(self._create_entity_recommendation())
        
        # Sort by priority and expected impact
        recommendations.sort(
            key=lambda r: (
                ['critical', 'high', 'medium', 'low'].index(r.priority.value),
                -r.expected_impact
            )
        )
        
        self.recommendations[project_id] = recommendations
        return recommendations
    
    def _create_content_quality_recommendation(
        self,
        content_analysis: Dict[str, Any]
    ) -> Recommendation:
        """Create content quality recommendation"""
        return Recommendation(
            recommendation_id=f"rec_{datetime.utcnow().timestamp()}_content",
            type=RecommendationType.CONTENT_QUALITY,
            priority=RecommendationPriority.HIGH,
            title="Improve Content Relevance",
            description=(
                f"Content relevance score is {content_analysis.get('relevance_score', 0):.1f}%. "
                "Enhance content to better match user intent and search queries."
            ),
            action=(
                "1. Add more specific details and examples\n"
                "2. Include relevant statistics and data\n"
                "3. Answer common user questions directly\n"
                "4. Use clear, concise language"
            ),
            expected_impact=15.0,
            effort_level="medium",
            is_white_hat=True,
            compliance_notes="Focus on providing genuine value to users"
        )
    
    def _create_schema_recommendation(self, content_type: str) -> Recommendation:
        """Create schema markup recommendation"""
        schema_type = self._get_schema_type(content_type)
        schema_example = self._generate_schema_example(schema_type)
        
        return Recommendation(
            recommendation_id=f"rec_{datetime.utcnow().timestamp()}_schema",
            type=RecommendationType.SCHEMA_MARKUP,
            priority=RecommendationPriority.HIGH,
            title=f"Add {schema_type} Schema Markup",
            description=(
                f"No structured data detected. Adding {schema_type} schema can improve "
                "how LLMs understand and cite your content."
            ),
            action=(
                f"Add {schema_type} JSON-LD schema to your page's <head> section. "
                "This helps LLMs extract accurate information."
            ),
            expected_impact=20.0,
            effort_level="low",
            code_example=schema_example,
            is_white_hat=True,
            compliance_notes="Use accurate, truthful information in schema markup"
        )
    
    def _create_citation_recommendation(self) -> Recommendation:
        """Create citation improvement recommendation"""
        return Recommendation(
            recommendation_id=f"rec_{datetime.utcnow().timestamp()}_citation",
            type=RecommendationType.CITATION_IMPROVEMENT,
            priority=RecommendationPriority.MEDIUM,
            title="Enhance Content Authority",
            description=(
                "Low authority score detected. Add credible citations and references "
                "to improve trustworthiness."
            ),
            action=(
                "1. Cite authoritative sources (research papers, official docs)\n"
                "2. Link to reputable external resources\n"
                "3. Include expert quotes and testimonials\n"
                "4. Add statistics from credible sources"
            ),
            expected_impact=12.0,
            effort_level="medium",
            is_white_hat=True,
            compliance_notes="Only cite accurate, verifiable sources"
        )
    
    def _create_structure_recommendation(
        self,
        content_analysis: Dict[str, Any]
    ) -> Recommendation:
        """Create structure improvement recommendation"""
        return Recommendation(
            recommendation_id=f"rec_{datetime.utcnow().timestamp()}_structure",
            type=RecommendationType.STRUCTURE_FIX,
            priority=RecommendationPriority.MEDIUM,
            title="Improve Content Structure",
            description=(
                "Content structure needs improvement. Better organization helps "
                "LLMs extract and cite information accurately."
            ),
            action=(
                "1. Use clear heading hierarchy (H1, H2, H3)\n"
                "2. Add bullet points and numbered lists\n"
                "3. Include a table of contents for long content\n"
                "4. Use descriptive subheadings"
            ),
            expected_impact=10.0,
            effort_level="low",
            code_example=(
                "<article>\n"
                "  <h1>Main Title</h1>\n"
                "  <h2>Section 1</h2>\n"
                "  <p>Content...</p>\n"
                "  <h3>Subsection 1.1</h3>\n"
                "  <ul>\n"
                "    <li>Point 1</li>\n"
                "    <li>Point 2</li>\n"
                "  </ul>\n"
                "</article>"
            ),
            is_white_hat=True
        )
    
    def _create_keyword_recommendation(
        self,
        competitive_data: Optional[Dict[str, Any]]
    ) -> Recommendation:
        """Create keyword optimization recommendation"""
        return Recommendation(
            recommendation_id=f"rec_{datetime.utcnow().timestamp()}_keyword",
            type=RecommendationType.KEYWORD_OPTIMIZATION,
            priority=RecommendationPriority.HIGH,
            title="Optimize Target Keywords",
            description=(
                "Low visibility score suggests keyword optimization opportunities. "
                "Align content with high-value search queries."
            ),
            action=(
                "1. Research competitor keyword usage\n"
                "2. Include keywords naturally in headings\n"
                "3. Use semantic variations and related terms\n"
                "4. Focus on user intent, not keyword density"
            ),
            expected_impact=18.0,
            effort_level="medium",
            is_white_hat=True,
            compliance_notes=(
                "WARNING: Avoid keyword stuffing. Use keywords naturally and "
                "focus on providing value to users."
            )
        )
    
    def _create_entity_recommendation(self) -> Recommendation:
        """Create entity enhancement recommendation"""
        return Recommendation(
            recommendation_id=f"rec_{datetime.utcnow().timestamp()}_entity",
            type=RecommendationType.ENTITY_ENHANCEMENT,
            priority=RecommendationPriority.LOW,
            title="Add More Named Entities",
            description=(
                "Low entity count detected. Adding relevant entities (people, places, "
                "organizations) helps LLMs understand context."
            ),
            action=(
                "1. Mention relevant people and experts\n"
                "2. Reference specific locations\n"
                "3. Name organizations and brands\n"
                "4. Include product names and models"
            ),
            expected_impact=8.0,
            effort_level="low",
            is_white_hat=True
        )
    
    def _get_schema_type(self, content_type: str) -> str:
        """Determine appropriate schema type"""
        schema_map = {
            'article': 'Article',
            'product': 'Product',
            'recipe': 'Recipe',
            'event': 'Event',
            'local_business': 'LocalBusiness',
            'faq': 'FAQPage',
            'how_to': 'HowTo'
        }
        return schema_map.get(content_type, 'Article')
    
    def _generate_schema_example(self, schema_type: str) -> str:
        """Generate schema markup example"""
        if schema_type == 'Article':
            return '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Your Article Title",
  "author": {
    "@type": "Person",
    "name": "Author Name"
  },
  "datePublished": "2024-01-01",
  "description": "Article description"
}
</script>'''
        elif schema_type == 'LocalBusiness':
            return '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Business Name",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "123 Main St",
    "addressLocality": "City",
    "addressRegion": "State",
    "postalCode": "12345"
  },
  "telephone": "+1-555-0123"
}
</script>'''
        elif schema_type == 'FAQPage':
            return '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "Question text?",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "Answer text"
    }
  }]
}
</script>'''
        else:
            return f'<!-- {schema_type} schema example -->'


class ComplianceChecker:
    """
    Check content compliance with white-hat SEO practices
    
    Detects potential violations like hidden text, keyword stuffing,
    and misleading content.
    """
    
    def __init__(self):
        self.keyword_density_threshold = 0.03  # 3%
        self.min_content_length = 300  # words
    
    def check_compliance(
        self,
        content_id: str,
        content: str,
        html: Optional[str] = None
    ) -> ComplianceReport:
        """
        Check content compliance
        
        Args:
            content_id: Content identifier
            content: Plain text content
            html: HTML content (optional)
            
        Returns:
            ComplianceReport with detected issues
        """
        issues = []
        
        # Check for hidden text
        if html:
            hidden_text_issues = self._detect_hidden_text(html)
            issues.extend(hidden_text_issues)
        
        # Check for keyword stuffing
        keyword_stuffing_issues = self._detect_keyword_stuffing(content)
        issues.extend(keyword_stuffing_issues)
        
        # Check for thin content
        thin_content_issues = self._detect_thin_content(content)
        issues.extend(thin_content_issues)
        
        # Check for misleading content
        misleading_issues = self._detect_misleading_content(content)
        issues.extend(misleading_issues)
        
        # Calculate compliance score
        compliance_score = self._calculate_compliance_score(issues)
        is_compliant = compliance_score >= 80
        
        # Generate recommendations
        recommendations = self._generate_compliance_recommendations(issues)
        
        return ComplianceReport(
            content_id=content_id,
            compliance_score=compliance_score,
            issues=issues,
            is_compliant=is_compliant,
            checked_at=datetime.utcnow(),
            recommendations=recommendations
        )
    
    def _detect_hidden_text(self, html: str) -> List[ComplianceIssue]:
        """Detect hidden text in HTML"""
        issues = []
        
        # Check for display:none or visibility:hidden
        hidden_patterns = [
            r'display\s*:\s*none',
            r'visibility\s*:\s*hidden',
            r'font-size\s*:\s*0',
            r'color\s*:\s*#ffffff.*background.*#ffffff'
        ]
        
        for pattern in hidden_patterns:
            if re.search(pattern, html, re.IGNORECASE):
                issues.append(ComplianceIssue(
                    issue_type=ComplianceIssueType.HIDDEN_TEXT,
                    severity="high",
                    description="Hidden text detected in HTML",
                    location="HTML styles",
                    fix_suggestion="Remove hidden text. All content should be visible to users.",
                    is_white_hat_violation=True
                ))
                break
        
        return issues
    
    def _detect_keyword_stuffing(self, content: str) -> List[ComplianceIssue]:
        """Detect keyword stuffing"""
        issues = []
        words = content.lower().split()
        
        if not words:
            return issues
        
        # Count word frequencies
        word_freq = {}
        for word in words:
            if len(word) > 3:  # Only count meaningful words
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Check for excessive repetition
        total_words = len(words)
        for word, count in word_freq.items():
            density = count / total_words
            if density > self.keyword_density_threshold:
                issues.append(ComplianceIssue(
                    issue_type=ComplianceIssueType.KEYWORD_STUFFING,
                    severity="medium",
                    description=f"Keyword '{word}' appears {count} times ({density*100:.1f}% density)",
                    location="Content body",
                    fix_suggestion=(
                        f"Reduce usage of '{word}'. Use synonyms and natural language. "
                        "Aim for keyword density below 3%."
                    ),
                    is_white_hat_violation=True
                ))
        
        return issues
    
    def _detect_thin_content(self, content: str) -> List[ComplianceIssue]:
        """Detect thin content"""
        issues = []
        word_count = len(content.split())
        
        if word_count < self.min_content_length:
            issues.append(ComplianceIssue(
                issue_type=ComplianceIssueType.THIN_CONTENT,
                severity="medium",
                description=f"Content is too short ({word_count} words)",
                location="Content body",
                fix_suggestion=(
                    f"Expand content to at least {self.min_content_length} words. "
                    "Add more details, examples, and valuable information."
                ),
                is_white_hat_violation=False
            ))
        
        return issues
    
    def _detect_misleading_content(self, content: str) -> List[ComplianceIssue]:
        """Detect potentially misleading content"""
        issues = []
        
        # Check for excessive superlatives
        superlatives = ['best', 'greatest', 'perfect', 'ultimate', 'guaranteed']
        superlative_count = sum(
            content.lower().count(word) for word in superlatives
        )
        
        if superlative_count > 5:
            issues.append(ComplianceIssue(
                issue_type=ComplianceIssueType.MISLEADING_CONTENT,
                severity="low",
                description=f"Excessive use of superlatives ({superlative_count} instances)",
                location="Content body",
                fix_suggestion=(
                    "Reduce use of superlatives. Use specific, verifiable claims "
                    "instead of exaggerated language."
                ),
                is_white_hat_violation=False
            ))
        
        return issues
    
    def _calculate_compliance_score(self, issues: List[ComplianceIssue]) -> float:
        """Calculate overall compliance score"""
        if not issues:
            return 100.0
        
        # Deduct points based on severity
        severity_penalties = {
            'critical': 30,
            'high': 20,
            'medium': 10,
            'low': 5
        }
        
        total_penalty = sum(
            severity_penalties.get(issue.severity, 0) for issue in issues
        )
        
        score = max(0, 100 - total_penalty)
        return round(score, 1)
    
    def _generate_compliance_recommendations(
        self,
        issues: List[ComplianceIssue]
    ) -> List[str]:
        """Generate compliance recommendations"""
        if not issues:
            return ["Content is compliant with white-hat SEO practices."]
        
        recommendations = []
        
        # Group by severity
        critical_issues = [i for i in issues if i.severity == 'critical']
        high_issues = [i for i in issues if i.severity == 'high']
        
        if critical_issues:
            recommendations.append(
                f"CRITICAL: Fix {len(critical_issues)} critical compliance issues immediately."
            )
        
        if high_issues:
            recommendations.append(
                f"HIGH PRIORITY: Address {len(high_issues)} high-severity issues."
            )
        
        # Add specific recommendations
        for issue in issues[:3]:  # Top 3 issues
            recommendations.append(f"• {issue.fix_suggestion}")
        
        return recommendations
