"""
LLM Visibility Research Service
Analyzes category performance across LLMs
"""
from typing import List, Dict
import asyncio
import logging
from collections import defaultdict
import random

from app.services.llm_adapters import LLMAdapterFactory, QueryParams

logger = logging.getLogger(__name__)


class QuestionGenerator:
    """Generate test questions for LLM research"""
    
    QUESTION_TEMPLATES = {
        'informational': [
            "什么是{category}？",
            "{category}有哪些类型？",
            "如何选择{category}？",
            "What is {category}?",
            "What are the types of {category}?",
        ],
        'transactional': [
            "推荐几家{category}",
            "哪些{category}值得去？",
            "最好的{category}是哪家？",
            "Recommend some {category}",
            "Which {category} are worth visiting?",
        ],
        'comparison': [
            "{category}中，哪个品牌最好？",
            "高端{category}有哪些？",
            "Which brand of {category} is the best?",
            "What are the premium {category} brands?",
        ],
    }
    
    def generate(self, category: str, count: int = 20) -> List[str]:
        """Generate questions for category"""
        questions = []
        
        for intent, templates in self.QUESTION_TEMPLATES.items():
            for template in templates:
                question = template.format(category=category)
                questions.append(question)
                
                if len(questions) >= count:
                    return questions[:count]
        
        return questions


class BrandExtractor:
    """Extract brand mentions from LLM responses"""
    
    def extract(self, responses: List[str]) -> Dict[str, int]:
        """Extract brand mentions and count occurrences"""
        # Simplified brand extraction - in production, use NER
        brand_counts = defaultdict(int)
        
        # Mock brand extraction
        mock_brands = [
            "海底捞", "呷哺呷哺", "小龙坎", "大龙燚", "蜀大侠",
            "Brand A", "Brand B", "Brand C", "Brand D", "Brand E"
        ]
        
        for response in responses:
            # Simulate brand detection
            for brand in mock_brands:
                if brand.lower() in response.lower() or random.random() > 0.7:
                    brand_counts[brand] += random.randint(1, 3)
        
        return dict(brand_counts)


class VisibilityResearchService:
    """Main service for LLM visibility research"""
    
    def __init__(self):
        self.question_generator = QuestionGenerator()
        self.brand_extractor = BrandExtractor()
    
    async def analyze_category(
        self,
        category: str,
        question_count: int = 100,
        llm_engines: List[str] = None
    ) -> Dict:
        """
        Analyze category visibility across LLMs
        
        Returns:
            Dict containing:
            - maturity: Category maturity level
            - brand_shares: Share of Model for each brand
            - cognitive_gaps: Identified gaps
            - strategies: Recommended strategies
        """
        if llm_engines is None:
            llm_engines = ['gpt-4', 'claude-3', 'gemini-pro']
        
        logger.info(f"Starting visibility research for category: {category}")
        
        # 1. Generate test questions
        questions = self.question_generator.generate(category, question_count)
        logger.info(f"Generated {len(questions)} test questions")
        
        # 2. Query multiple LLMs
        responses = await self._query_llms(questions, llm_engines)
        logger.info(f"Collected {len(responses)} LLM responses")
        
        # 3. Extract brand mentions
        brand_mentions = self.brand_extractor.extract(responses)
        logger.info(f"Extracted {len(brand_mentions)} brand mentions")
        
        # 4. Calculate Share of Model
        share_of_model = self._calculate_share_of_model(brand_mentions)
        
        # 5. Assess maturity
        maturity = self._assess_maturity(responses, brand_mentions)
        
        # 6. Identify cognitive gaps
        cognitive_gaps = self._identify_gaps(category, brand_mentions)
        
        # 7. Generate strategies
        strategies = self._generate_strategies(maturity, cognitive_gaps)
        
        return {
            'report_id': f"report-{category}-{random.randint(1000, 9999)}",
            'category': category,
            'maturity': maturity,
            'brand_shares': share_of_model,
            'cognitive_gaps': cognitive_gaps,
            'strategies': strategies,
        }
    
    async def _query_llms(
        self,
        questions: List[str],
        engines: List[str]
    ) -> List[str]:
        """Query multiple LLMs with questions"""
        responses = []
        
        # Use mock API keys for now
        api_key = "mock-api-key"
        
        # Query each engine
        for engine in engines:
            try:
                adapter = LLMAdapterFactory.create(engine, api_key)
                
                # Query subset of questions per engine
                engine_questions = questions[:10]  # Limit for demo
                
                for question in engine_questions:
                    try:
                        response = await adapter.query(
                            question,
                            QueryParams(temperature=0.7, seed=42)
                        )
                        responses.append(response.text)
                    except Exception as e:
                        logger.error(f"Query failed for {engine}: {e}")
                        
            except Exception as e:
                logger.error(f"Failed to create adapter for {engine}: {e}")
        
        return responses
    
    def _calculate_share_of_model(
        self,
        brand_mentions: Dict[str, int]
    ) -> Dict[str, float]:
        """Calculate Share of Model percentages"""
        total_mentions = sum(brand_mentions.values())
        
        if total_mentions == 0:
            return {}
        
        share_of_model = {
            brand: (count / total_mentions) * 100
            for brand, count in brand_mentions.items()
        }
        
        # Sort by share
        return dict(sorted(
            share_of_model.items(),
            key=lambda x: x[1],
            reverse=True
        ))
    
    def _assess_maturity(
        self,
        responses: List[str],
        brand_mentions: Dict[str, int]
    ) -> str:
        """Assess category maturity level"""
        total_mentions = sum(brand_mentions.values())
        avg_mentions_per_response = total_mentions / len(responses) if responses else 0
        
        if avg_mentions_per_response < 0.5:
            return 'low'
        elif avg_mentions_per_response < 2.0:
            return 'medium'
        else:
            return 'high'
    
    def _identify_gaps(
        self,
        category: str,
        brand_mentions: Dict[str, int]
    ) -> List[Dict]:
        """Identify cognitive gaps and opportunities"""
        # Mock gap identification
        gaps = [
            {
                'topic': f'素食{category}' if '火锅' in category else f'Premium {category}',
                'opportunity_score': 0.85,
                'current_leaders': [],
                'description': 'Low competition in this niche segment'
            },
            {
                'topic': f'{category}配送服务',
                'opportunity_score': 0.72,
                'current_leaders': list(brand_mentions.keys())[:2] if brand_mentions else [],
                'description': 'Growing demand for delivery options'
            },
        ]
        
        return gaps
    
    def _generate_strategies(
        self,
        maturity: str,
        cognitive_gaps: List[Dict]
    ) -> List[Dict]:
        """Generate GEO strategy recommendations"""
        strategies = []
        
        if maturity == 'low':
            strategies.append({
                'type': 'early_positioning',
                'priority': 'high',
                'title': 'Early Market Positioning',
                'description': 'Establish authority in this emerging category',
                'expected_impact': 0.35
            })
        
        for gap in cognitive_gaps:
            strategies.append({
                'type': 'content_creation',
                'priority': 'high' if gap['opportunity_score'] > 0.8 else 'medium',
                'title': f'Create content for: {gap["topic"]}',
                'description': gap['description'],
                'expected_impact': gap['opportunity_score'] * 0.3
            })
        
        strategies.append({
            'type': 'authority_building',
            'priority': 'medium',
            'title': 'Build Content Authority',
            'description': 'Add citations, data, and expert opinions',
            'expected_impact': 0.15
        })
        
        return strategies
