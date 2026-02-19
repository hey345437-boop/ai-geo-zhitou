"""
Probe Service - Monitor brand visibility across LLMs
"""
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import asyncio
import logging
from uuid import uuid4

from app.services.llm_adapters import LLMAdapterFactory, QueryParams

logger = logging.getLogger(__name__)


class ProbeScheduler:
    """Schedule and execute probe jobs"""
    
    def __init__(self):
        self.active_jobs = {}
    
    async def create_probe(
        self,
        brand: str,
        keywords: List[str],
        frequency: str = "daily",
        llm_engines: List[str] = None
    ) -> Dict:
        """Create a new probe job"""
        if llm_engines is None:
            llm_engines = ['gpt-4', 'claude-3', 'gemini-pro']
        
        job_id = str(uuid4())
        
        job = {
            'id': job_id,
            'brand': brand,
            'keywords': keywords,
            'frequency': frequency,
            'llm_engines': llm_engines,
            'status': 'scheduled',
            'created_at': datetime.now().isoformat(),
            'last_run_at': None,
            'next_run_at': self._calculate_next_run(frequency).isoformat()
        }
        
        self.active_jobs[job_id] = job
        logger.info(f"Created probe job {job_id} for brand: {brand}")
        
        return job
    
    async def execute_probe(self, job_id: str) -> Dict:
        """Execute a probe job"""
        job = self.active_jobs.get(job_id)
        if not job:
            raise ValueError(f"Job {job_id} not found")
        
        logger.info(f"Executing probe job {job_id}")
        
        results = []
        
        # Query each LLM engine with each keyword
        for engine in job['llm_engines']:
            adapter = LLMAdapterFactory.create(engine, "mock-api-key")
            
            for keyword in job['keywords']:
                try:
                    response = await adapter.query(
                        keyword,
                        QueryParams(temperature=0.7, seed=42)
                    )
                    
                    # Check if brand is mentioned
                    is_mentioned = job['brand'].lower() in response.text.lower()
                    position = self._find_position(job['brand'], response.text)
                    
                    results.append({
                        'timestamp': datetime.now().isoformat(),
                        'brand': job['brand'],
                        'keyword': keyword,
                        'llm_engine': engine,
                        'is_mentioned': is_mentioned,
                        'position': position,
                        'response_text': response.text[:500]  # Truncate
                    })
                    
                except Exception as e:
                    logger.error(f"Probe query failed: {e}")
        
        # Update job status
        job['last_run_at'] = datetime.now().isoformat()
        job['next_run_at'] = self._calculate_next_run(job['frequency']).isoformat()
        
        return {
            'job_id': job_id,
            'brand': job['brand'],
            'data_points': results,
            'visibility_score': self._calculate_visibility_score(results)
        }
    
    def get_probe_results(
        self,
        job_id: str,
        timeframe: str = "30d"
    ) -> Dict:
        """Get probe results for a timeframe"""
        job = self.active_jobs.get(job_id)
        if not job:
            raise ValueError(f"Job {job_id} not found")
        
        data_points = self._generate_historical_data(
            job['brand'],
            job['keywords'],
            job['llm_engines'],
            timeframe
        )
        
        return {
            'job_id': job_id,
            'brand': job['brand'],
            'timeframe': timeframe,
            'data_points': data_points,
            'visibility_score': self._calculate_visibility_score(data_points)
        }
    
    def list_probes(self) -> List[Dict]:
        """List all probe jobs"""
        return list(self.active_jobs.values())
    
    def _calculate_next_run(self, frequency: str) -> datetime:
        """Calculate next run time based on frequency"""
        now = datetime.now()
        
        if frequency == "hourly":
            return now + timedelta(hours=1)
        elif frequency == "daily":
            return now + timedelta(days=1)
        elif frequency == "weekly":
            return now + timedelta(weeks=1)
        else:
            return now + timedelta(days=1)
    
    def _find_position(self, brand: str, text: str) -> int:
        """Find position of brand mention in text"""
        text_lower = text.lower()
        brand_lower = brand.lower()
        
        if brand_lower not in text_lower:
            return -1
        
        # Count sentences before brand mention
        sentences = text[:text_lower.index(brand_lower)].split('.')
        return len(sentences)
    
    def _calculate_visibility_score(self, data_points: List[Dict]) -> Dict:
        """Calculate visibility score from data points"""
        if not data_points:
            return {
                'overall': 0,
                'mention_rate': 0,
                'position_score': 0,
                'consistency': 0,
                'trend': 0
            }
        
        # Mention rate
        mentioned = sum(1 for dp in data_points if dp['is_mentioned'])
        mention_rate = (mentioned / len(data_points)) * 100
        
        # Position score
        positions = [dp['position'] for dp in data_points if dp['position'] > 0]
        avg_position = sum(positions) / len(positions) if positions else 0
        position_score = max(0, 100 - (avg_position * 10))
        
        # Consistency (variance across engines)
        consistency = 80  # Mock value
        
        # Trend (improvement over time)
        trend = 5.2  # Mock value
        
        # Overall score
        overall = (mention_rate * 0.4 + position_score * 0.3 + 
                  consistency * 0.2 + (50 + trend) * 0.1)
        
        return {
            'overall': round(overall, 1),
            'mention_rate': round(mention_rate, 1),
            'position_score': round(position_score, 1),
            'consistency': round(consistency, 1),
            'trend': round(trend, 1)
        }
    
    def _generate_historical_data(
        self,
        brand: str,
        keywords: List[str],
        engines: List[str],
        timeframe: str
    ) -> List[Dict]:
        """Generate historical data"""
        import random
        
        days = int(timeframe.replace('d', ''))
        data_points = []
        
        for day in range(days):
            date = datetime.now() - timedelta(days=days - day)
            
            for engine in engines:
                for keyword in keywords[:2]:  # Limit keywords
                    data_points.append({
                        'timestamp': date.isoformat(),
                        'brand': brand,
                        'keyword': keyword,
                        'llm_engine': engine,
                        'is_mentioned': random.random() > 0.3,
                        'position': random.randint(1, 5) if random.random() > 0.3 else -1,
                        'response_text': f"Mock response for {keyword}"
                    })
        
        return data_points


# Global instance
probe_scheduler = ProbeScheduler()
