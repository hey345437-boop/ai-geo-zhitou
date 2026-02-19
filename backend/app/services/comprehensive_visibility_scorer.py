"""
Comprehensive Visibility Scoring System
Implements 8-dimension visibility scoring with advanced analytics
"""
from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime
import statistics
import logging

logger = logging.getLogger(__name__)


@dataclass
class VisibilityScore:
    """Comprehensive visibility score"""
    overall: float
    mention_rate: float
    top_k_rate: Dict[str, float]  # top-1, top-3, top-5, top-10
    citation_weighted: float
    position_weighted: float
    sentiment_score: float
    regional_consistency: float
    time_trend: float
    competitive_ranking: float
    hallucination_penalty: float
    
    # Metadata
    total_queries: int
    total_mentions: int
    timestamp: datetime


class ComprehensiveVisibilityScorer:
    """Calculate multi-dimensional visibility scores"""
    
    # Weights for overall score calculation
    DIMENSION_WEIGHTS = {
        'mention_rate': 0.20,
        'top_k_rate': 0.15,
        'citation_weighted': 0.15,
        'position_weighted': 0.15,
        'sentiment_score': 0.10,
        'regional_consistency': 0.10,
        'time_trend': 0.05,
        'competitive_ranking': 0.10,
    }
    
    # Position weights (opening > middle > ending)
    POSITION_WEIGHTS = {
        'opening': 1.0,
        'middle': 0.7,
        'ending': 0.4
    }
    
    def __init__(self):
        self.sentiment_analyzer = None  # Placeholder for sentiment model
    
    def calculate_comprehensive_score(
        self,
        data_points: List[Dict],
        citations: List[Dict] = None,
        competitors: List[str] = None
    ) -> VisibilityScore:
        """Calculate comprehensive visibility score"""
        
        if not data_points:
            return self._empty_score()
        
        # 1. Mention Rate
        mention_rate = self._calculate_mention_rate(data_points)
        
        # 2. Top-k Mention Rate
        top_k_rate = self._calculate_top_k_rate(data_points)
        
        # 3. Citation-Weighted Score
        citation_weighted = self._calculate_citation_weighted_score(
            data_points, citations or []
        )
        
        # 4. Position-Weighted Score
        position_weighted = self._calculate_position_weighted_score(data_points)
        
        # 5. Sentiment Score
        sentiment_score = self._calculate_sentiment_score(data_points)
        
        # 6. Regional Consistency
        regional_consistency = self._calculate_regional_consistency(data_points)
        
        # 7. Time Trend
        time_trend = self._calculate_time_trend(data_points)
        
        # 8. Competitive Ranking
        competitive_ranking = self._calculate_competitive_ranking(
            data_points, competitors or []
        )
        
        # 9. Hallucination Penalty
        hallucination_penalty = self._calculate_hallucination_penalty(data_points)
        
        # Calculate overall score
        overall = self._calculate_overall_score({
            'mention_rate': mention_rate,
            'top_k_rate': top_k_rate['top-3'],  # Use top-3 for overall
            'citation_weighted': citation_weighted,
            'position_weighted': position_weighted,
            'sentiment_score': sentiment_score,
            'regional_consistency': regional_consistency,
            'time_trend': time_trend,
            'competitive_ranking': competitive_ranking,
        })
        
        # Apply hallucination penalty
        overall = max(0, overall - hallucination_penalty)
        
        # Count statistics
        total_queries = len(data_points)
        total_mentions = sum(1 for dp in data_points if dp.get('is_mentioned', False))
        
        return VisibilityScore(
            overall=round(overall, 2),
            mention_rate=round(mention_rate, 2),
            top_k_rate={k: round(v, 2) for k, v in top_k_rate.items()},
            citation_weighted=round(citation_weighted, 2),
            position_weighted=round(position_weighted, 2),
            sentiment_score=round(sentiment_score, 2),
            regional_consistency=round(regional_consistency, 2),
            time_trend=round(time_trend, 2),
            competitive_ranking=round(competitive_ranking, 2),
            hallucination_penalty=round(hallucination_penalty, 2),
            total_queries=total_queries,
            total_mentions=total_mentions,
            timestamp=datetime.now()
        )
    
    def _calculate_mention_rate(self, data_points: List[Dict]) -> float:
        """Calculate basic mention rate"""
        if not data_points:
            return 0.0
        
        mentioned = sum(1 for dp in data_points if dp.get('is_mentioned', False))
        return (mentioned / len(data_points)) * 100
    
    def _calculate_top_k_rate(self, data_points: List[Dict]) -> Dict[str, float]:
        """Calculate Top-k mention rates"""
        if not data_points:
            return {'top-1': 0.0, 'top-3': 0.0, 'top-5': 0.0, 'top-10': 0.0}
        
        top_k_counts = {'top-1': 0, 'top-3': 0, 'top-5': 0, 'top-10': 0}
        
        for dp in data_points:
            position = dp.get('position', -1)
            if position == 1:
                top_k_counts['top-1'] += 1
            if 1 <= position <= 3:
                top_k_counts['top-3'] += 1
            if 1 <= position <= 5:
                top_k_counts['top-5'] += 1
            if 1 <= position <= 10:
                top_k_counts['top-10'] += 1
        
        total = len(data_points)
        return {
            k: (count / total) * 100
            for k, count in top_k_counts.items()
        }
    
    def _calculate_citation_weighted_score(
        self,
        data_points: List[Dict],
        citations: List[Dict]
    ) -> float:
        """Calculate citation-weighted visibility score"""
        if not data_points:
            return 0.0
        
        # Map citations to data points
        citation_map = {}
        for citation in citations:
            response_id = citation.get('response_id')
            if response_id:
                citation_map[response_id] = citation.get('credibility_score', 0.5)
        
        weighted_sum = 0.0
        for dp in data_points:
            if dp.get('is_mentioned', False):
                # Get citation credibility (default 0.5 if no citation)
                credibility = citation_map.get(dp.get('id'), 0.5)
                weighted_sum += credibility
        
        return (weighted_sum / len(data_points)) * 100
    
    def _calculate_position_weighted_score(self, data_points: List[Dict]) -> float:
        """Calculate position-weighted visibility score"""
        if not data_points:
            return 0.0
        
        weighted_sum = 0.0
        
        for dp in data_points:
            if not dp.get('is_mentioned', False):
                continue
            
            position_category = dp.get('position_category', 'middle')
            weight = self.POSITION_WEIGHTS.get(position_category, 0.5)
            
            # Also consider numeric position
            numeric_position = dp.get('position', -1)
            if numeric_position > 0:
                # Higher positions get higher scores
                position_score = max(0, 1 - (numeric_position - 1) * 0.1)
                weighted_sum += weight * position_score
            else:
                weighted_sum += weight * 0.5
        
        return (weighted_sum / len(data_points)) * 100
    
    def _calculate_sentiment_score(self, data_points: List[Dict]) -> float:
        """Calculate sentiment score for brand mentions"""
        if not data_points:
            return 50.0
        
        sentiments = []
        
        for dp in data_points:
            if not dp.get('is_mentioned', False):
                continue
            
            text = dp.get('response_text', '').lower()
            positive_keywords = ['best', 'excellent', 'great', 'top', 'leading', 'innovative']
            negative_keywords = ['worst', 'poor', 'bad', 'avoid', 'disappointing']
            
            positive_count = sum(1 for kw in positive_keywords if kw in text)
            negative_count = sum(1 for kw in negative_keywords if kw in text)
            
            if positive_count > negative_count:
                sentiment = 0.7 + (positive_count * 0.1)
            elif negative_count > positive_count:
                sentiment = 0.3 - (negative_count * 0.1)
            else:
                sentiment = 0.5
            
            sentiments.append(max(0, min(1, sentiment)))
        
        if not sentiments:
            return 50.0
        
        avg_sentiment = statistics.mean(sentiments)
        return avg_sentiment * 100
    
    def _calculate_regional_consistency(self, data_points: List[Dict]) -> float:
        """Calculate regional consistency score"""
        if not data_points:
            return 0.0
        
        # Group by region
        regional_rates = {}
        
        for dp in data_points:
            region = dp.get('region', 'global')
            if region not in regional_rates:
                regional_rates[region] = {'total': 0, 'mentioned': 0}
            
            regional_rates[region]['total'] += 1
            if dp.get('is_mentioned', False):
                regional_rates[region]['mentioned'] += 1
        
        # Calculate mention rate per region
        rates = []
        for region, counts in regional_rates.items():
            rate = counts['mentioned'] / counts['total'] if counts['total'] > 0 else 0
            rates.append(rate)
        
        if len(rates) < 2:
            return 100.0
        
        mean_rate = statistics.mean(rates)
        if mean_rate == 0:
            return 0.0
        
        std_dev = statistics.stdev(rates)
        cv = std_dev / mean_rate
        consistency_score = max(0, 100 - (cv * 100))
        return consistency_score
    
    def _calculate_time_trend(self, data_points: List[Dict]) -> float:
        """Calculate time series trend score"""
        if not data_points:
            return 0.0
        
        sorted_points = sorted(
            data_points,
            key=lambda x: x.get('timestamp', ''),
            reverse=False
        )
        
        mid = len(sorted_points) // 2
        first_half = sorted_points[:mid]
        second_half = sorted_points[mid:]
        first_rate = sum(1 for dp in first_half if dp.get('is_mentioned', False)) / len(first_half) if first_half else 0
        second_rate = sum(1 for dp in second_half if dp.get('is_mentioned', False)) / len(second_half) if second_half else 0
        if first_rate == 0:
            return 0.0 if second_rate == 0 else 100.0
        
        improvement = ((second_rate - first_rate) / first_rate) * 100
        normalized = 50 + improvement
        return max(0, min(100, normalized))
    
    def _calculate_competitive_ranking(
        self,
        data_points: List[Dict],
        competitors: List[str]
    ) -> float:
        """Calculate competitive ranking score"""
        if not data_points or not competitors:
            return 50.0
        
        competitor_mentions = {comp: 0 for comp in competitors}
        brand_mentions = 0
        
        for dp in data_points:
            text = dp.get('response_text', '').lower()
            
            if dp.get('is_mentioned', False):
                brand_mentions += 1
            
            for comp in competitors:
                if comp.lower() in text:
                    competitor_mentions[comp] += 1
        
        all_mentions = [brand_mentions] + list(competitor_mentions.values())
        all_mentions.sort(reverse=True)
        
        if brand_mentions == 0:
            return 0.0
        
        rank = all_mentions.index(brand_mentions) + 1
        total_brands = len(all_mentions)
        score = ((total_brands - rank + 1) / total_brands) * 100
        return score
    
    def _calculate_hallucination_penalty(self, data_points: List[Dict]) -> float:
        """Calculate penalty for hallucinated mentions"""
        if not data_points:
            return 0.0
        
        hallucinated = 0
        
        for dp in data_points:
            if dp.get('is_mentioned', False):
                is_verified = dp.get('is_verified', True)
                if not is_verified:
                    hallucinated += 1
        
        if hallucinated == 0:
            return 0.0
        
        hallucination_rate = hallucinated / len(data_points)
        penalty = hallucination_rate * 50
        return penalty
    
    def _calculate_overall_score(self, dimension_scores: Dict[str, float]) -> float:
        """Calculate weighted overall score"""
        overall = 0.0
        
        for dimension, score in dimension_scores.items():
            weight = self.DIMENSION_WEIGHTS.get(dimension, 0.0)
            overall += score * weight
        
        return overall
    
    def _empty_score(self) -> VisibilityScore:
        """Return empty score"""
        return VisibilityScore(
            overall=0.0,
            mention_rate=0.0,
            top_k_rate={'top-1': 0.0, 'top-3': 0.0, 'top-5': 0.0, 'top-10': 0.0},
            citation_weighted=0.0,
            position_weighted=0.0,
            sentiment_score=50.0,
            regional_consistency=0.0,
            time_trend=0.0,
            competitive_ranking=50.0,
            hallucination_penalty=0.0,
            total_queries=0,
            total_mentions=0,
            timestamp=datetime.now()
        )


# Global instance
comprehensive_scorer = ComprehensiveVisibilityScorer()
