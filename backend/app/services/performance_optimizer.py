"""
Performance Optimization Service

Provides caching, batch processing, and performance monitoring capabilities.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Callable
from datetime import datetime, timedelta
import hashlib
import time
from enum import Enum


class CacheLevel(Enum):
    """Cache levels"""
    MEMORY = "memory"
    REDIS = "redis"
    BOTH = "both"


@dataclass
class CacheEntry:
    """Cache entry with metadata"""
    key: str
    value: Any
    created_at: datetime
    expires_at: Optional[datetime]
    hit_count: int = 0
    size_bytes: int = 0
    
    def is_expired(self) -> bool:
        """Check if entry is expired"""
        if self.expires_at is None:
            return False
        return datetime.utcnow() > self.expires_at


@dataclass
class CacheStats:
    """Cache statistics"""
    total_requests: int = 0
    cache_hits: int = 0
    cache_misses: int = 0
    evictions: int = 0
    total_size_bytes: int = 0
    
    @property
    def hit_rate(self) -> float:
        """Calculate cache hit rate"""
        if self.total_requests == 0:
            return 0.0
        return self.cache_hits / self.total_requests
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'total_requests': self.total_requests,
            'cache_hits': self.cache_hits,
            'cache_misses': self.cache_misses,
            'hit_rate': round(self.hit_rate, 3),
            'evictions': self.evictions,
            'total_size_bytes': self.total_size_bytes
        }


class CacheManager:
    """
    Multi-layer cache manager
    
    Implements:
    - Local memory cache (L1)
    - Redis cache (L2)
    - Cache invalidation
    - TTL management
    - LRU eviction
    """
    
    def __init__(
        self,
        max_memory_size: int = 100 * 1024 * 1024,  # 100MB
        default_ttl: int = 3600  # 1 hour
    ):
        self.max_memory_size = max_memory_size
        self.default_ttl = default_ttl
        
        # Memory cache (L1)
        self.memory_cache: Dict[str, CacheEntry] = {}
        
        # Statistics
        self.stats = CacheStats()
    
    def get(
        self,
        key: str,
        level: CacheLevel = CacheLevel.BOTH
    ) -> Optional[Any]:
        """
        Get value from cache
        
        Args:
            key: Cache key
            level: Cache level to check
            
        Returns:
            Cached value or None
        """
        self.stats.total_requests += 1
        
        # Check memory cache first
        if level in [CacheLevel.MEMORY, CacheLevel.BOTH]:
            entry = self.memory_cache.get(key)
            if entry and not entry.is_expired():
                entry.hit_count += 1
                self.stats.cache_hits += 1
                return entry.value
        
        # Check Redis cache (mock)
        if level in [CacheLevel.REDIS, CacheLevel.BOTH]:
            # In production, check Redis here
            pass
        
        self.stats.cache_misses += 1
        return None
    
    def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None,
        level: CacheLevel = CacheLevel.BOTH
    ) -> bool:
        """
        Set value in cache
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds
            level: Cache level to use
            
        Returns:
            True if successful
        """
        ttl = ttl or self.default_ttl
        expires_at = datetime.utcnow() + timedelta(seconds=ttl)
        
        # Estimate size
        size_bytes = len(str(value).encode('utf-8'))
        
        # Set in memory cache
        if level in [CacheLevel.MEMORY, CacheLevel.BOTH]:
            # Check if we need to evict
            if self._should_evict(size_bytes):
                self._evict_lru()
            
            entry = CacheEntry(
                key=key,
                value=value,
                created_at=datetime.utcnow(),
                expires_at=expires_at,
                size_bytes=size_bytes
            )
            self.memory_cache[key] = entry
            self.stats.total_size_bytes += size_bytes
        
        # Set in Redis cache (mock)
        if level in [CacheLevel.REDIS, CacheLevel.BOTH]:
            # In production, set in Redis here
            pass
        
        return True
    
    def delete(self, key: str) -> bool:
        """Delete key from cache"""
        if key in self.memory_cache:
            entry = self.memory_cache[key]
            self.stats.total_size_bytes -= entry.size_bytes
            del self.memory_cache[key]
            return True
        return False
    
    def clear(self) -> None:
        """Clear all cache"""
        self.memory_cache.clear()
        self.stats = CacheStats()
    
    def _should_evict(self, new_size: int) -> bool:
        """Check if eviction is needed"""
        return self.stats.total_size_bytes + new_size > self.max_memory_size
    
    def _evict_lru(self) -> None:
        """Evict least recently used entry"""
        if not self.memory_cache:
            return
        
        # Find LRU entry (lowest hit_count)
        lru_key = min(
            self.memory_cache.keys(),
            key=lambda k: self.memory_cache[k].hit_count
        )
        
        entry = self.memory_cache[lru_key]
        self.stats.total_size_bytes -= entry.size_bytes
        self.stats.evictions += 1
        del self.memory_cache[lru_key]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        return self.stats.to_dict()


class BatchProcessor:
    """
    Batch processor for efficient API calls
    
    Batches multiple requests together to reduce overhead.
    """
    
    def __init__(
        self,
        batch_size: int = 10,
        max_wait_time: float = 1.0  # seconds
    ):
        self.batch_size = batch_size
        self.max_wait_time = max_wait_time
        self.pending_requests: List[Dict[str, Any]] = []
        self.batch_start_time: Optional[float] = None
    
    def add_request(
        self,
        request_id: str,
        data: Dict[str, Any]
    ) -> None:
        """Add request to batch"""
        if not self.pending_requests:
            self.batch_start_time = time.time()
        
        self.pending_requests.append({
            'request_id': request_id,
            'data': data,
            'added_at': time.time()
        })
    
    def should_process(self) -> bool:
        """Check if batch should be processed"""
        if not self.pending_requests:
            return False
        
        # Process if batch is full
        if len(self.pending_requests) >= self.batch_size:
            return True
        
        # Process if max wait time exceeded
        if self.batch_start_time:
            elapsed = time.time() - self.batch_start_time
            if elapsed >= self.max_wait_time:
                return True
        
        return False
    
    def process_batch(
        self,
        processor_func: Callable[[List[Dict[str, Any]]], List[Any]]
    ) -> List[Any]:
        """
        Process current batch
        
        Args:
            processor_func: Function to process batch
            
        Returns:
            List of results
        """
        if not self.pending_requests:
            return []
        
        # Process batch
        results = processor_func(self.pending_requests)
        
        # Clear batch
        self.pending_requests.clear()
        self.batch_start_time = None
        
        return results
    
    def get_batch_size(self) -> int:
        """Get current batch size"""
        return len(self.pending_requests)


@dataclass
class PerformanceMetrics:
    """Performance metrics"""
    endpoint: str
    request_count: int = 0
    total_time: float = 0.0
    min_time: float = float('inf')
    max_time: float = 0.0
    error_count: int = 0
    
    @property
    def avg_time(self) -> float:
        """Calculate average response time"""
        if self.request_count == 0:
            return 0.0
        return self.total_time / self.request_count
    
    @property
    def error_rate(self) -> float:
        """Calculate error rate"""
        if self.request_count == 0:
            return 0.0
        return self.error_count / self.request_count
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'endpoint': self.endpoint,
            'request_count': self.request_count,
            'avg_time_ms': round(self.avg_time * 1000, 2),
            'min_time_ms': round(self.min_time * 1000, 2) if self.min_time != float('inf') else 0,
            'max_time_ms': round(self.max_time * 1000, 2),
            'error_count': self.error_count,
            'error_rate': round(self.error_rate, 3)
        }


class PerformanceMonitor:
    """
    Performance monitoring
    
    Tracks API response times and identifies slow endpoints.
    """
    
    def __init__(self):
        self.metrics: Dict[str, PerformanceMetrics] = {}
    
    def record_request(
        self,
        endpoint: str,
        response_time: float,
        is_error: bool = False
    ) -> None:
        """
        Record request metrics
        
        Args:
            endpoint: API endpoint
            response_time: Response time in seconds
            is_error: Whether request resulted in error
        """
        if endpoint not in self.metrics:
            self.metrics[endpoint] = PerformanceMetrics(endpoint=endpoint)
        
        metrics = self.metrics[endpoint]
        metrics.request_count += 1
        metrics.total_time += response_time
        metrics.min_time = min(metrics.min_time, response_time)
        metrics.max_time = max(metrics.max_time, response_time)
        
        if is_error:
            metrics.error_count += 1
    
    def get_metrics(self, endpoint: Optional[str] = None) -> Dict[str, Any]:
        """Get performance metrics"""
        if endpoint:
            metrics = self.metrics.get(endpoint)
            return metrics.to_dict() if metrics else {}
        
        return {
            endpoint: metrics.to_dict()
            for endpoint, metrics in self.metrics.items()
        }
    
    def get_slow_endpoints(
        self,
        threshold_ms: float = 2000
    ) -> List[Dict[str, Any]]:
        """Get endpoints slower than threshold"""
        threshold_s = threshold_ms / 1000
        slow_endpoints = []
        
        for endpoint, metrics in self.metrics.items():
            if metrics.avg_time > threshold_s:
                slow_endpoints.append(metrics.to_dict())
        
        # Sort by average time (slowest first)
        slow_endpoints.sort(key=lambda x: x['avg_time_ms'], reverse=True)
        
        return slow_endpoints
    
    def calculate_percentiles(
        self,
        endpoint: str,
        response_times: List[float]
    ) -> Dict[str, float]:
        """
        Calculate response time percentiles
        
        Args:
            endpoint: API endpoint
            response_times: List of response times
            
        Returns:
            Dictionary with P50, P95, P99
        """
        if not response_times:
            return {'p50': 0, 'p95': 0, 'p99': 0}
        
        sorted_times = sorted(response_times)
        n = len(sorted_times)
        
        p50_idx = int(n * 0.50)
        p95_idx = int(n * 0.95)
        p99_idx = int(n * 0.99)
        
        return {
            'p50': round(sorted_times[p50_idx] * 1000, 2),
            'p95': round(sorted_times[p95_idx] * 1000, 2),
            'p99': round(sorted_times[p99_idx] * 1000, 2)
        }


class QueryOptimizer:
    """
    Database query optimizer
    
    Provides query optimization recommendations.
    """
    
    def __init__(self):
        self.slow_queries: List[Dict[str, Any]] = []
    
    def analyze_query(
        self,
        query: str,
        execution_time: float,
        rows_examined: int
    ) -> Dict[str, Any]:
        """
        Analyze query performance
        
        Args:
            query: SQL query
            execution_time: Execution time in seconds
            rows_examined: Number of rows examined
            
        Returns:
            Analysis with recommendations
        """
        recommendations = []
        
        # Check for missing indexes
        if 'WHERE' in query.upper() and execution_time > 0.1:
            recommendations.append("Consider adding index on WHERE clause columns")
        
        # Check for SELECT *
        if 'SELECT *' in query.upper():
            recommendations.append("Avoid SELECT *, specify needed columns")
        
        # Check for N+1 queries
        if rows_examined > 1000:
            recommendations.append("Consider using JOIN instead of multiple queries")
        
        # Check for missing LIMIT
        if 'LIMIT' not in query.upper() and 'SELECT' in query.upper():
            recommendations.append("Add LIMIT clause to prevent large result sets")
        
        analysis = {
            'query': query[:100],  # Truncate for display
            'execution_time_ms': round(execution_time * 1000, 2),
            'rows_examined': rows_examined,
            'is_slow': execution_time > 0.5,
            'recommendations': recommendations
        }
        
        if analysis['is_slow']:
            self.slow_queries.append(analysis)
        
        return analysis
    
    def get_slow_queries(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get slowest queries"""
        sorted_queries = sorted(
            self.slow_queries,
            key=lambda x: x['execution_time_ms'],
            reverse=True
        )
        return sorted_queries[:limit]
    
    def suggest_indexes(self, table: str, columns: List[str]) -> str:
        """Generate index creation SQL"""
        index_name = f"idx_{table}_{'_'.join(columns)}"
        columns_str = ', '.join(columns)
        return f"CREATE INDEX {index_name} ON {table} ({columns_str});"
