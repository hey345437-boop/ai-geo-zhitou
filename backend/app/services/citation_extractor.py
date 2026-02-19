"""
Citation Extraction System
Extracts and analyzes citations from LLM responses
"""
from dataclasses import dataclass
from typing import List, Optional
from enum import Enum
import re
import logging
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


class CitationType(Enum):
    """Types of citations"""
    URL = "url"  # Direct URL
    INLINE_NUMBER = "inline_number"  # [1], (2)
    ATTRIBUTION = "attribution"  # "According to..."
    DIRECT_QUOTE = "direct_quote"  # "..."
    FOOTNOTE = "footnote"  # Footnote reference
    BIBLIOGRAPHY = "bibliography"  # Bibliography entry
    HYPERLINK = "hyperlink"  # Clickable link
    SOURCE_LIST = "source_list"  # Listed sources


class CitationCredibility(Enum):
    """Credibility levels"""
    VERY_HIGH = 5  # Official, authoritative
    HIGH = 4  # Reputable sources
    MEDIUM = 3  # General websites
    LOW = 2  # Questionable sources
    VERY_LOW = 1  # Unreliable sources


@dataclass
class Citation:
    """Citation data structure"""
    text: str
    type: CitationType
    url: Optional[str]
    position: str  # opening, middle, ending
    credibility: CitationCredibility
    domain: Optional[str]
    is_https: bool
    is_official: bool


@dataclass
class CitationMetrics:
    """Citation metrics for a brand"""
    total_citations: int
    citation_rate: float  # Citations per response
    avg_credibility: float
    https_rate: float
    official_domain_rate: float
    position_distribution: dict  # {opening: x, middle: y, ending: z}
    credibility_distribution: dict  # {level: count}


class CitationExtractor:
    """Extract citations from LLM responses"""
    
    # Patterns for different citation types
    URL_PATTERN = r'https?://[^\s<>"{}|\\^`\[\]]+'
    INLINE_NUMBER_PATTERN = r'\[(\d+)\]|\((\d+)\)'
    ATTRIBUTION_PATTERN = r'(?:according to|as per|based on|source:|from)\s+([^.]+)'
    DIRECT_QUOTE_PATTERN = r'"([^"]+)"'
    
    # Authoritative domains
    OFFICIAL_DOMAINS = {
        'gov', 'edu', 'org',  # TLDs
        'wikipedia.org', 'britannica.com',  # Encyclopedias
        'nature.com', 'science.org',  # Academic
        'who.int', 'cdc.gov',  # Health authorities
    }
    
    def __init__(self):
        self.domain_credibility_cache = {}
    
    def extract_citations(self, response_text: str) -> List[Citation]:
        """Extract all citations from response"""
        citations = []
        
        # Extract URLs
        citations.extend(self._extract_urls(response_text))
        
        # Extract inline numbers
        citations.extend(self._extract_inline_numbers(response_text))
        
        # Extract attributions
        citations.extend(self._extract_attributions(response_text))
        
        # Extract direct quotes
        citations.extend(self._extract_quotes(response_text))
        
        logger.info(f"Extracted {len(citations)} citations")
        return citations
    
    def _extract_urls(self, text: str) -> List[Citation]:
        """Extract URL citations"""
        citations = []
        urls = re.findall(self.URL_PATTERN, text)
        
        for url in urls:
            domain = self._extract_domain(url)
            credibility = self._assess_credibility(url, domain)
            position = self._determine_position(text, url)
            
            citation = Citation(
                text=url,
                type=CitationType.URL,
                url=url,
                position=position,
                credibility=credibility,
                domain=domain,
                is_https=url.startswith('https://'),
                is_official=self._is_official_domain(domain)
            )
            citations.append(citation)
        
        return citations
    
    def _extract_inline_numbers(self, text: str) -> List[Citation]:
        """Extract inline number citations like [1], (2)"""
        citations = []
        matches = re.finditer(self.INLINE_NUMBER_PATTERN, text)
        
        for match in matches:
            number = match.group(1) or match.group(2)
            position = self._determine_position(text, match.group(0))
            
            citation = Citation(
                text=f"[{number}]",
                type=CitationType.INLINE_NUMBER,
                url=None,
                position=position,
                credibility=CitationCredibility.MEDIUM,
                domain=None,
                is_https=False,
                is_official=False
            )
            citations.append(citation)
        
        return citations
    
    def _extract_attributions(self, text: str) -> List[Citation]:
        """Extract attribution statements"""
        citations = []
        matches = re.finditer(self.ATTRIBUTION_PATTERN, text, re.IGNORECASE)
        
        for match in matches:
            attribution = match.group(1).strip()
            position = self._determine_position(text, match.group(0))
            
            citation = Citation(
                text=attribution,
                type=CitationType.ATTRIBUTION,
                url=None,
                position=position,
                credibility=CitationCredibility.MEDIUM,
                domain=None,
                is_https=False,
                is_official=False
            )
            citations.append(citation)
        
        return citations
    
    def _extract_quotes(self, text: str) -> List[Citation]:
        """Extract direct quotes"""
        citations = []
        matches = re.finditer(self.DIRECT_QUOTE_PATTERN, text)
        
        for match in matches:
            quote = match.group(1)
            if len(quote) > 20:  # Only meaningful quotes
                position = self._determine_position(text, match.group(0))
                
                citation = Citation(
                    text=quote,
                    type=CitationType.DIRECT_QUOTE,
                    url=None,
                    position=position,
                    credibility=CitationCredibility.MEDIUM,
                    domain=None,
                    is_https=False,
                    is_official=False
                )
                citations.append(citation)
        
        return citations
    
    def _extract_domain(self, url: str) -> Optional[str]:
        """Extract domain from URL"""
        try:
            parsed = urlparse(url)
            return parsed.netloc
        except Exception:
            return None
    
    def _assess_credibility(self, url: str, domain: Optional[str]) -> CitationCredibility:
        """Assess citation credibility"""
        if not domain:
            return CitationCredibility.LOW
        
        # Check cache
        if domain in self.domain_credibility_cache:
            return self.domain_credibility_cache[domain]
        
        # Assess credibility
        credibility = CitationCredibility.MEDIUM
        
        if self._is_official_domain(domain):
            credibility = CitationCredibility.VERY_HIGH
        elif any(tld in domain for tld in ['.edu', '.gov']):
            credibility = CitationCredibility.VERY_HIGH
        elif any(site in domain for site in ['wikipedia', 'britannica', 'nature', 'science']):
            credibility = CitationCredibility.HIGH
        elif not url.startswith('https://'):
            credibility = CitationCredibility.LOW
        
        # Cache result
        self.domain_credibility_cache[domain] = credibility
        return credibility
    
    def _is_official_domain(self, domain: Optional[str]) -> bool:
        """Check if domain is official/authoritative"""
        if not domain:
            return False
        return any(official in domain for official in self.OFFICIAL_DOMAINS)
    
    def _determine_position(self, text: str, citation_text: str) -> str:
        """Determine citation position in text"""
        index = text.find(citation_text)
        if index == -1:
            return "unknown"
        
        text_length = len(text)
        relative_position = index / text_length
        
        if relative_position < 0.33:
            return "opening"
        elif relative_position < 0.67:
            return "middle"
        else:
            return "ending"
    
    def calculate_metrics(self, citations: List[Citation], total_responses: int) -> CitationMetrics:
        """Calculate citation metrics"""
        if not citations:
            return CitationMetrics(
                total_citations=0,
                citation_rate=0.0,
                avg_credibility=0.0,
                https_rate=0.0,
                official_domain_rate=0.0,
                position_distribution={},
                credibility_distribution={}
            )
        
        # Calculate rates
        citation_rate = len(citations) / max(total_responses, 1)
        
        # Average credibility
        avg_credibility = sum(c.credibility.value for c in citations) / len(citations)
        
        # HTTPS rate
        https_count = sum(1 for c in citations if c.is_https)
        https_rate = https_count / len(citations)
        
        # Official domain rate
        official_count = sum(1 for c in citations if c.is_official)
        official_domain_rate = official_count / len(citations)
        
        # Position distribution
        position_dist = {}
        for c in citations:
            position_dist[c.position] = position_dist.get(c.position, 0) + 1
        
        # Credibility distribution
        credibility_dist = {}
        for c in citations:
            level = c.credibility.name
            credibility_dist[level] = credibility_dist.get(level, 0) + 1
        
        return CitationMetrics(
            total_citations=len(citations),
            citation_rate=citation_rate,
            avg_credibility=avg_credibility,
            https_rate=https_rate,
            official_domain_rate=official_domain_rate,
            position_distribution=position_dist,
            credibility_distribution=credibility_dist
        )
