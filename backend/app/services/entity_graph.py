"""
Entity Graph & Structure Scanner Service

Provides entity extraction, relationship mapping, and structure defect detection.
"""

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional, Set, Tuple
from datetime import datetime
from enum import Enum
import re


class EntityType(Enum):
    """Types of entities"""
    PERSON = "person"
    ORGANIZATION = "organization"
    LOCATION = "location"
    PRODUCT = "product"
    BRAND = "brand"
    CONCEPT = "concept"
    EVENT = "event"


class RelationType(Enum):
    """Types of relationships between entities"""
    WORKS_FOR = "works_for"
    LOCATED_IN = "located_in"
    PRODUCES = "produces"
    COMPETES_WITH = "competes_with"
    RELATED_TO = "related_to"
    PART_OF = "part_of"
    MENTIONS = "mentions"


class DefectSeverity(Enum):
    """Severity levels for structure defects"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


@dataclass
class Entity:
    """Entity in the knowledge graph"""
    entity_id: str
    name: str
    type: EntityType
    attributes: Dict[str, Any] = field(default_factory=dict)
    mentions_count: int = 0
    confidence: float = 1.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        data = asdict(self)
        data['type'] = self.type.value
        return data


@dataclass
class Relationship:
    """Relationship between entities"""
    source_id: str
    target_id: str
    type: RelationType
    weight: float = 1.0
    attributes: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        data = asdict(self)
        data['type'] = self.type.value
        return data


@dataclass
class EntityGraph:
    """Complete entity graph"""
    graph_id: str
    entities: List[Entity]
    relationships: List[Relationship]
    created_at: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'graph_id': self.graph_id,
            'entities': [e.to_dict() for e in self.entities],
            'relationships': [r.to_dict() for r in self.relationships],
            'created_at': self.created_at.isoformat(),
            'metadata': self.metadata
        }


@dataclass
class StructureDefect:
    """Structure defect in content"""
    defect_id: str
    type: str
    severity: DefectSeverity
    title: str
    description: str
    location: str
    fix_suggestion: str
    code_example: Optional[str] = None
    expected_improvement: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        data = asdict(self)
        data['severity'] = self.severity.value
        return data


class EntityExtractor:
    """
    Extract entities from content and build knowledge graph
    
    Identifies named entities, normalizes names, and detects relationships.
    """
    
    def __init__(self):
        self.entity_patterns = {
            EntityType.PERSON: [
                r'\b[A-Z][a-z]+ [A-Z][a-z]+\b',  # John Smith
                r'\b(?:Dr|Mr|Ms|Mrs)\. [A-Z][a-z]+\b'  # Dr. Smith
            ],
            EntityType.ORGANIZATION: [
                r'\b[A-Z][a-z]+ (?:Inc|Corp|LLC|Ltd)\b',
                r'\b(?:Google|Microsoft|Apple|Amazon|Meta)\b'
            ],
            EntityType.LOCATION: [
                r'\b[A-Z][a-z]+, [A-Z]{2}\b',  # City, ST
                r'\b(?:New York|Los Angeles|Chicago|Houston)\b'
            ],
            EntityType.BRAND: [
                r'\b[A-Z][a-z]+(?:[A-Z][a-z]+)*\b'  # CamelCase brands
            ]
        }
    
    def extract_entities(
        self,
        content: str,
        content_id: str
    ) -> EntityGraph:
        """
        Extract entities from content
        
        Args:
            content: Text content to analyze
            content_id: Content identifier
            
        Returns:
            EntityGraph with extracted entities and relationships
        """
        entities = []
        entity_map = {}  # name -> entity_id mapping
        
        # Extract entities by type
        for entity_type, patterns in self.entity_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, content)
                for match in matches:
                    entity_name = match.group(0)
                    normalized_name = self._normalize_entity_name(entity_name)
                    
                    # Check if entity already exists
                    if normalized_name not in entity_map:
                        entity_id = f"entity_{len(entities)}_{entity_type.value}"
                        entity = Entity(
                            entity_id=entity_id,
                            name=normalized_name,
                            type=entity_type,
                            mentions_count=1,
                            confidence=0.8
                        )
                        entities.append(entity)
                        entity_map[normalized_name] = entity_id
                    else:
                        # Increment mention count
                        entity_id = entity_map[normalized_name]
                        for entity in entities:
                            if entity.entity_id == entity_id:
                                entity.mentions_count += 1
                                break
        
        # Detect relationships
        relationships = self._detect_relationships(entities, content)
        
        # Create graph
        graph = EntityGraph(
            graph_id=f"graph_{content_id}_{datetime.utcnow().timestamp()}",
            entities=entities,
            relationships=relationships,
            created_at=datetime.utcnow(),
            metadata={
                'content_id': content_id,
                'entity_count': len(entities),
                'relationship_count': len(relationships)
            }
        )
        
        return graph
    
    def _normalize_entity_name(self, name: str) -> str:
        """Normalize entity name"""
        # Remove extra whitespace
        name = ' '.join(name.split())
        # Remove titles
        name = re.sub(r'^(?:Dr|Mr|Ms|Mrs)\.\s*', '', name)
        return name.strip()
    
    def _detect_relationships(
        self,
        entities: List[Entity],
        content: str
    ) -> List[Relationship]:
        """Detect relationships between entities"""
        relationships = []
        
        # Simple co-occurrence based relationship detection
        for i, entity1 in enumerate(entities):
            for entity2 in entities[i+1:]:
                # Check if entities co-occur in same sentence
                if self._entities_cooccur(entity1.name, entity2.name, content):
                    rel_type = self._infer_relationship_type(
                        entity1.type,
                        entity2.type
                    )
                    
                    relationship = Relationship(
                        source_id=entity1.entity_id,
                        target_id=entity2.entity_id,
                        type=rel_type,
                        weight=0.5
                    )
                    relationships.append(relationship)
        
        return relationships
    
    def _entities_cooccur(
        self,
        entity1: str,
        entity2: str,
        content: str,
        window: int = 100
    ) -> bool:
        """Check if two entities co-occur within a window"""
        # Find all positions of entity1
        pos1 = [m.start() for m in re.finditer(re.escape(entity1), content)]
        pos2 = [m.start() for m in re.finditer(re.escape(entity2), content)]
        
        # Check if any positions are within window
        for p1 in pos1:
            for p2 in pos2:
                if abs(p1 - p2) <= window:
                    return True
        
        return False
    
    def _infer_relationship_type(
        self,
        type1: EntityType,
        type2: EntityType
    ) -> RelationType:
        """Infer relationship type based on entity types"""
        # Simple heuristics
        if type1 == EntityType.PERSON and type2 == EntityType.ORGANIZATION:
            return RelationType.WORKS_FOR
        elif type1 == EntityType.ORGANIZATION and type2 == EntityType.LOCATION:
            return RelationType.LOCATED_IN
        elif type1 == EntityType.ORGANIZATION and type2 == EntityType.PRODUCT:
            return RelationType.PRODUCES
        elif type1 == EntityType.BRAND and type2 == EntityType.BRAND:
            return RelationType.COMPETES_WITH
        else:
            return RelationType.RELATED_TO


class StructureDefectScanner:
    """
    Scan content for structure defects
    
    Detects 15+ types of structure issues that can impact LLM visibility.
    """
    
    def __init__(self):
        self.defect_checks = [
            self._check_missing_headings,
            self._check_heading_hierarchy,
            self._check_missing_meta_description,
            self._check_missing_title,
            self._check_duplicate_headings,
            self._check_long_paragraphs,
            self._check_missing_alt_text,
            self._check_broken_links,
            self._check_missing_schema,
            self._check_poor_readability,
            self._check_missing_lists,
            self._check_missing_tables,
            self._check_missing_faq,
            self._check_thin_sections,
            self._check_missing_citations
        ]
    
    def scan_structure(
        self,
        content_id: str,
        html: str,
        text: str
    ) -> List[StructureDefect]:
        """
        Scan content structure for defects
        
        Args:
            content_id: Content identifier
            html: HTML content
            text: Plain text content
            
        Returns:
            List of detected defects
        """
        defects = []
        
        # Run all defect checks
        for check_func in self.defect_checks:
            defect = check_func(content_id, html, text)
            if defect:
                defects.append(defect)
        
        # Sort by severity
        severity_order = ['critical', 'high', 'medium', 'low', 'info']
        defects.sort(key=lambda d: severity_order.index(d.severity.value))
        
        return defects
    
    def _check_missing_headings(
        self,
        content_id: str,
        html: str,
        text: str
    ) -> Optional[StructureDefect]:
        """Check for missing headings"""
        if not re.search(r'<h[1-6]', html, re.IGNORECASE):
            return StructureDefect(
                defect_id=f"defect_{content_id}_no_headings",
                type="missing_headings",
                severity=DefectSeverity.HIGH,
                title="No Headings Found",
                description="Content has no heading tags (H1-H6)",
                location="Document structure",
                fix_suggestion="Add heading tags to organize content hierarchically",
                code_example="<h1>Main Title</h1>\n<h2>Section Title</h2>",
                expected_improvement=15.0
            )
        return None
    
    def _check_heading_hierarchy(
        self,
        content_id: str,
        html: str,
        text: str
    ) -> Optional[StructureDefect]:
        """Check heading hierarchy"""
        headings = re.findall(r'<h([1-6])', html, re.IGNORECASE)
        if headings:
            levels = [int(h) for h in headings]
            # Check if hierarchy is broken (e.g., H1 -> H3)
            for i in range(len(levels) - 1):
                if levels[i+1] - levels[i] > 1:
                    return StructureDefect(
                        defect_id=f"defect_{content_id}_broken_hierarchy",
                        type="broken_heading_hierarchy",
                        severity=DefectSeverity.MEDIUM,
                        title="Broken Heading Hierarchy",
                        description=f"Heading jumps from H{levels[i]} to H{levels[i+1]}",
                        location="Document structure",
                        fix_suggestion="Use sequential heading levels (H1 -> H2 -> H3)",
                        expected_improvement=8.0
                    )
        return None
    
    def _check_missing_meta_description(
        self,
        content_id: str,
        html: str,
        text: str
    ) -> Optional[StructureDefect]:
        """Check for missing meta description"""
        if not re.search(r'<meta\s+name=["\']description["\']', html, re.IGNORECASE):
            return StructureDefect(
                defect_id=f"defect_{content_id}_no_meta_desc",
                type="missing_meta_description",
                severity=DefectSeverity.MEDIUM,
                title="Missing Meta Description",
                description="No meta description tag found",
                location="<head> section",
                fix_suggestion="Add a concise meta description (150-160 characters)",
                code_example='<meta name="description" content="Your description here">',
                expected_improvement=10.0
            )
        return None
    
    def _check_missing_title(
        self,
        content_id: str,
        html: str,
        text: str
    ) -> Optional[StructureDefect]:
        """Check for missing title tag"""
        if not re.search(r'<title>', html, re.IGNORECASE):
            return StructureDefect(
                defect_id=f"defect_{content_id}_no_title",
                type="missing_title",
                severity=DefectSeverity.CRITICAL,
                title="Missing Title Tag",
                description="No <title> tag found in document",
                location="<head> section",
                fix_suggestion="Add a descriptive title tag (50-60 characters)",
                code_example="<title>Your Page Title</title>",
                expected_improvement=20.0
            )
        return None
    
    def _check_duplicate_headings(
        self,
        content_id: str,
        html: str,
        text: str
    ) -> Optional[StructureDefect]:
        """Check for duplicate headings"""
        headings = re.findall(r'<h[1-6][^>]*>(.*?)</h[1-6]>', html, re.IGNORECASE)
        if len(headings) != len(set(headings)):
            return StructureDefect(
                defect_id=f"defect_{content_id}_duplicate_headings",
                type="duplicate_headings",
                severity=DefectSeverity.LOW,
                title="Duplicate Headings",
                description="Multiple headings have identical text",
                location="Document structure",
                fix_suggestion="Make each heading unique and descriptive",
                expected_improvement=5.0
            )
        return None
    
    def _check_long_paragraphs(
        self,
        content_id: str,
        html: str,
        text: str
    ) -> Optional[StructureDefect]:
        """Check for overly long paragraphs"""
        paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', html, re.IGNORECASE | re.DOTALL)
        long_paragraphs = [p for p in paragraphs if len(p.split()) > 150]
        
        if long_paragraphs:
            return StructureDefect(
                defect_id=f"defect_{content_id}_long_paragraphs",
                type="long_paragraphs",
                severity=DefectSeverity.LOW,
                title="Overly Long Paragraphs",
                description=f"{len(long_paragraphs)} paragraphs exceed 150 words",
                location="Content body",
                fix_suggestion="Break long paragraphs into shorter, focused sections",
                expected_improvement=6.0
            )
        return None
    
    def _check_missing_alt_text(
        self,
        content_id: str,
        html: str,
        text: str
    ) -> Optional[StructureDefect]:
        """Check for images without alt text"""
        images = re.findall(r'<img[^>]*>', html, re.IGNORECASE)
        images_without_alt = [img for img in images if 'alt=' not in img.lower()]
        
        if images_without_alt:
            return StructureDefect(
                defect_id=f"defect_{content_id}_missing_alt",
                type="missing_alt_text",
                severity=DefectSeverity.MEDIUM,
                title="Missing Alt Text",
                description=f"{len(images_without_alt)} images lack alt attributes",
                location="Image tags",
                fix_suggestion="Add descriptive alt text to all images",
                code_example='<img src="image.jpg" alt="Descriptive text">',
                expected_improvement=7.0
            )
        return None
    
    def _check_broken_links(
        self,
        content_id: str,
        html: str,
        text: str
    ) -> Optional[StructureDefect]:
        """Check for potentially broken links"""
        # Simple check for empty href
        empty_links = re.findall(r'<a\s+href=["\']["\']', html, re.IGNORECASE)
        
        if empty_links:
            return StructureDefect(
                defect_id=f"defect_{content_id}_empty_links",
                type="empty_links",
                severity=DefectSeverity.MEDIUM,
                title="Empty Links",
                description=f"{len(empty_links)} links have empty href attributes",
                location="Link tags",
                fix_suggestion="Remove empty links or add valid URLs",
                expected_improvement=5.0
            )
        return None
    
    def _check_missing_schema(
        self,
        content_id: str,
        html: str,
        text: str
    ) -> Optional[StructureDefect]:
        """Check for missing schema markup"""
        if 'application/ld+json' not in html and 'schema.org' not in html:
            return StructureDefect(
                defect_id=f"defect_{content_id}_no_schema",
                type="missing_schema",
                severity=DefectSeverity.HIGH,
                title="No Schema Markup",
                description="No structured data (Schema.org) found",
                location="Document",
                fix_suggestion="Add appropriate Schema.org markup",
                expected_improvement=18.0
            )
        return None
    
    def _check_poor_readability(
        self,
        content_id: str,
        html: str,
        text: str
    ) -> Optional[StructureDefect]:
        """Check readability"""
        # Simple check: average sentence length
        sentences = re.split(r'[.!?]+', text)
        if sentences:
            avg_words = sum(len(s.split()) for s in sentences) / len(sentences)
            if avg_words > 25:
                return StructureDefect(
                    defect_id=f"defect_{content_id}_poor_readability",
                    type="poor_readability",
                    severity=DefectSeverity.LOW,
                    title="Poor Readability",
                    description=f"Average sentence length is {avg_words:.1f} words",
                    location="Content body",
                    fix_suggestion="Use shorter sentences (15-20 words average)",
                    expected_improvement=8.0
                )
        return None
    
    def _check_missing_lists(
        self,
        content_id: str,
        html: str,
        text: str
    ) -> Optional[StructureDefect]:
        """Check for missing lists"""
        word_count = len(text.split())
        has_lists = bool(re.search(r'<[ou]l>', html, re.IGNORECASE))
        
        if word_count > 500 and not has_lists:
            return StructureDefect(
                defect_id=f"defect_{content_id}_no_lists",
                type="missing_lists",
                severity=DefectSeverity.LOW,
                title="No Lists Found",
                description="Long content without bullet points or numbered lists",
                location="Content body",
                fix_suggestion="Use lists to organize information",
                expected_improvement=6.0
            )
        return None
    
    def _check_missing_tables(
        self,
        content_id: str,
        html: str,
        text: str
    ) -> Optional[StructureDefect]:
        """Check for missing tables when appropriate"""
        # Check if content mentions comparisons or data
        has_comparison_keywords = any(
            keyword in text.lower()
            for keyword in ['compare', 'versus', 'vs', 'comparison']
        )
        has_tables = bool(re.search(r'<table>', html, re.IGNORECASE))
        
        if has_comparison_keywords and not has_tables:
            return StructureDefect(
                defect_id=f"defect_{content_id}_no_tables",
                type="missing_tables",
                severity=DefectSeverity.INFO,
                title="Consider Adding Tables",
                description="Content discusses comparisons but lacks tables",
                location="Content body",
                fix_suggestion="Use tables to present comparative data",
                expected_improvement=5.0
            )
        return None
    
    def _check_missing_faq(
        self,
        content_id: str,
        html: str,
        text: str
    ) -> Optional[StructureDefect]:
        """Check for missing FAQ section"""
        has_questions = len(re.findall(r'\?', text)) > 3
        has_faq_schema = 'FAQPage' in html
        
        if has_questions and not has_faq_schema:
            return StructureDefect(
                defect_id=f"defect_{content_id}_no_faq",
                type="missing_faq_schema",
                severity=DefectSeverity.MEDIUM,
                title="Missing FAQ Schema",
                description="Content has Q&A format but no FAQ schema",
                location="Document",
                fix_suggestion="Add FAQPage schema markup",
                expected_improvement=12.0
            )
        return None
    
    def _check_thin_sections(
        self,
        content_id: str,
        html: str,
        text: str
    ) -> Optional[StructureDefect]:
        """Check for thin content sections"""
        sections = re.split(r'<h[2-3][^>]*>', html, re.IGNORECASE)
        thin_sections = [s for s in sections if len(s.split()) < 50]
        
        if len(thin_sections) > len(sections) / 2:
            return StructureDefect(
                defect_id=f"defect_{content_id}_thin_sections",
                type="thin_sections",
                severity=DefectSeverity.MEDIUM,
                title="Thin Content Sections",
                description="Many sections have less than 50 words",
                location="Content sections",
                fix_suggestion="Expand sections with more details and examples",
                expected_improvement=10.0
            )
        return None
    
    def _check_missing_citations(
        self,
        content_id: str,
        html: str,
        text: str
    ) -> Optional[StructureDefect]:
        """Check for missing citations"""
        has_links = bool(re.search(r'<a\s+href=', html, re.IGNORECASE))
        word_count = len(text.split())
        
        if word_count > 500 and not has_links:
            return StructureDefect(
                defect_id=f"defect_{content_id}_no_citations",
                type="missing_citations",
                severity=DefectSeverity.MEDIUM,
                title="No External Citations",
                description="Long content without external links or citations",
                location="Content body",
                fix_suggestion="Add citations to authoritative sources",
                expected_improvement=12.0
            )
        return None
