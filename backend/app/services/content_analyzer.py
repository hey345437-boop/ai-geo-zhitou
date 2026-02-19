"""
Content Analysis Service
Analyzes content quality for GEO optimization
"""
from typing import Dict, List
import re
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class ContentAnalyzer:
    """Analyze content for GEO optimization"""
    
    def analyze(self, content: str, category: str, url: str = None) -> Dict:
        """
        Comprehensive content analysis
        
        Returns scores for:
        - Relevance
        - Authority
        - Freshness
        - Structure
        - Entity coverage
        """
        logger.info(f"Analyzing content for category: {category}")
        
        # Calculate individual scores
        relevance = self._calculate_relevance(content, category)
        authority = self._calculate_authority(content)
        freshness = self._calculate_freshness(content)
        structure = self._analyze_structure(content)
        entities = self._extract_entities(content)
        
        # Calculate overall score
        overall = (
            relevance * 0.3 +
            authority * 0.25 +
            freshness * 0.2 +
            structure * 0.15 +
            (len(entities) / 10) * 0.1  # Entity coverage
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            relevance, authority, freshness, structure, entities
        )
        
        return {
            'analysis_id': f"analysis-{hash(content) % 10000}",
            'scores': {
                'relevance': round(relevance, 2),
                'authority': round(authority, 2),
                'freshness': round(freshness, 2),
                'structure': round(structure, 2),
                'overall': round(overall, 2)
            },
            'entities': entities,
            'recommendations': recommendations,
            'word_count': len(content.split()),
            'analyzed_at': datetime.now().isoformat()
        }
    
    def _calculate_relevance(self, content: str, category: str) -> float:
        """Calculate semantic relevance to category"""
        content_lower = content.lower()
        category_lower = category.lower()
        category_count = content_lower.count(category_lower)
        words = content.split()
        if not words:
            return 0.0
        
        density = (category_count / len(words)) * 100
        relevance = min(density * 10, 1.0)
        
        return relevance
    
    def _calculate_authority(self, content: str) -> float:
        """
        Extract authority signals from content
        
        Signals:
        - Citations and references
        - Expert quotes
        - Data and statistics
        - Credentials mentioned
        """
        score = 0.0
        
        # Check for citations
        citation_patterns = [
            r'\[\d+\]',  # [1], [2]
            r'\(\d{4}\)',  # (2024)
            r'according to',
            r'研究表明',
            r'数据显示'
        ]
        
        for pattern in citation_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                score += 0.15
        
        # Check for statistics
        if re.search(r'\d+%|\d+\s*(million|billion|thousand|万|亿)', content):
            score += 0.25
        
        # Check for expert mentions
        expert_terms = ['博士', '教授', '专家', '研究员', 'Dr.', 'Professor', 'Expert']
        if any(term in content for term in expert_terms):
            score += 0.25
        
        # Check for data sources
        source_terms = ['来源', 'source', '数据来源', 'data from']
        if any(term in content.lower() for term in source_terms):
            score += 0.20
        
        return min(score, 1.0)
    
    def _calculate_freshness(self, content: str) -> float:
        """
        Assess content freshness
        Looks for recent dates and time-sensitive information
        """
        score = 0.5  # Base score
        
        # Look for recent years
        current_year = datetime.now().year
        recent_years = [str(year) for year in range(current_year - 2, current_year + 1)]
        
        for year in recent_years:
            if year in content:
                score += 0.2
                break
        
        # Look for freshness indicators
        fresh_terms = [
            '最新', '最近', '今年', '本月', 'latest', 'recent', 'new', 'updated'
        ]
        
        if any(term in content.lower() for term in fresh_terms):
            score += 0.3
        
        return min(score, 1.0)
    
    def _analyze_structure(self, content: str) -> float:
        """
        Analyze content structure quality
        
        Checks for:
        - Proper paragraphs
        - Headings
        - Lists
        - Length appropriateness
        """
        score = 0.0
        
        # Check word count (ideal: 300-2000 words)
        word_count = len(content.split())
        if 300 <= word_count <= 2000:
            score += 0.3
        elif word_count > 100:
            score += 0.15
        
        # Check for paragraphs
        paragraphs = content.split('\n\n')
        if len(paragraphs) >= 3:
            score += 0.2
        
        # Check for headings (# or ##)
        if re.search(r'^#{1,3}\s+.+$', content, re.MULTILINE):
            score += 0.2
        
        # Check for lists
        if re.search(r'^\s*[-*•]\s+', content, re.MULTILINE):
            score += 0.15
        
        # Check for proper sentence structure
        sentences = re.split(r'[.!?。！？]', content)
        if len(sentences) >= 5:
            score += 0.15
        
        return min(score, 1.0)
    
    def _extract_entities(self, content: str) -> List[str]:
        """Extract named entities from content"""
        entities = []
        words = content.split()
        for i, word in enumerate(words):
            if word and word[0].isupper() and len(word) > 2:
                if i > 0 and not words[i-1].endswith(('.', '!', '?', '。', '！', '？')):
                    entities.append(word)
        
        entities = list(set(entities))[:10]
        
        return entities
    
    def _generate_recommendations(
        self,
        relevance: float,
        authority: float,
        freshness: float,
        structure: float,
        entities: List[str]
    ) -> List[Dict]:
        """Generate actionable recommendations"""
        recommendations = []
        
        if relevance < 0.6:
            recommendations.append({
                'type': 'relevance',
                'priority': 'high',
                'title': '提升内容相关性',
                'description': '内容与目标品类的相关性较低',
                'action': '增加品类关键词密度，添加更多相关实体和概念',
                'expected_impact': 0.25
            })
        
        if authority < 0.5:
            recommendations.append({
                'type': 'authority',
                'priority': 'medium',
                'title': '增强权威性信号',
                'description': '缺少权威性标记（引用、数据、专家观点）',
                'action': '添加行业数据、专家引用、第三方认证',
                'expected_impact': 0.15
            })
        
        if freshness < 0.6:
            recommendations.append({
                'type': 'freshness',
                'priority': 'medium',
                'title': '更新内容时效性',
                'description': '内容缺少最新信息和时间标记',
                'action': '添加最新数据、更新日期、当前趋势',
                'expected_impact': 0.12
            })
        
        if structure < 0.6:
            recommendations.append({
                'type': 'structure',
                'priority': 'low',
                'title': '优化内容结构',
                'description': '内容结构可以改进',
                'action': '添加标题、段落、列表，改善可读性',
                'expected_impact': 0.10
            })
        
        if len(entities) < 5:
            recommendations.append({
                'type': 'entities',
                'priority': 'low',
                'title': '丰富实体覆盖',
                'description': '内容中提及的实体较少',
                'action': '添加更多相关品牌、产品、地点等实体',
                'expected_impact': 0.08
            })
        
        return recommendations


# Global instance
content_analyzer = ContentAnalyzer()
