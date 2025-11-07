"""
Advanced Multi-Level Caching System for Deep Tree Echo Operations.

Implements intelligent caching with Redis backend, in-memory LRU cache,
semantic similarity matching, and adaptive cache warming strategies.
"""

import asyncio
import hashlib
import json
import logging
import time
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple, Callable
import numpy as np

logger = logging.getLogger(__name__)


@dataclass
class CacheMetrics:
    """Comprehensive cache performance metrics."""
    
    # Hit/Miss statistics
    total_requests: int = 0
    cache_hits: int = 0
    cache_misses: int = 0
    semantic_hits: int = 0
    
    # Performance metrics
    avg_hit_latency_ms: float = 0.0
    avg_miss_latency_ms: float = 0.0
    total_time_saved_ms: float = 0.0
    
    # Memory metrics
    l1_cache_size: int = 0
    l2_cache_size: int = 0
    total_memory_bytes: int = 0
    
    # Efficiency metrics
    hit_rate: float = 0.0
    memory_efficiency: float = 0.0
    eviction_count: int = 0
    
    last_updated: float = field(default_factory=time.time)
    
    def update_hit_rate(self):
        """Calculate current cache hit rate."""
        if self.total_requests > 0:
            self.hit_rate = (self.cache_hits + self.semantic_hits) / self.total_requests
        else:
            self.hit_rate = 0.0


@dataclass
class CacheConfiguration:
    """Configuration for multi-level caching system."""
    
    # L1 Cache (In-Memory LRU)
    l1_max_size: int = 1000
    l1_ttl_seconds: int = 300  # 5 minutes
    
    # L2 Cache (Redis/Distributed)
    l2_enabled: bool = True
    l2_ttl_seconds: int = 3600  # 1 hour
    l2_max_size: int = 10000
    
    # Semantic similarity caching
    enable_semantic_cache: bool = True
    semantic_similarity_threshold: float = 0.85
    embedding_dimension: int = 768
    
    # Cache warming
    enable_cache_warming: bool = True
    warm_cache_on_startup: bool = True
    popular_queries_threshold: int = 5
    
    # Invalidation strategies
    enable_smart_invalidation: bool = True
    invalidation_batch_size: int = 100
    
    # Performance tuning
    async_write_enabled: bool = True
    compression_enabled: bool = True
    compression_threshold_bytes: int = 1024


class LRUCache:
    """
    High-performance in-memory LRU cache with TTL support.
    """
    
    def __init__(self, max_size: int = 1000, ttl_seconds: int = 300):
        """Initialize LRU cache."""
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        self._cache: OrderedDict = OrderedDict()
        self._timestamps: Dict[str, float] = {}
        self._lock = asyncio.Lock()
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache with TTL check."""
        async with self._lock:
            if key not in self._cache:
                return None
            
            # Check TTL
            if time.time() - self._timestamps[key] > self.ttl_seconds:
                del self._cache[key]
                del self._timestamps[key]
                return None
            
            # Move to end (most recently used)
            self._cache.move_to_end(key)
            return self._cache[key]
    
    async def set(self, key: str, value: Any) -> None:
        """Set value in cache with LRU eviction."""
        async with self._lock:
            # Remove if exists (to update position)
            if key in self._cache:
                del self._cache[key]
            
            # Add to cache
            self._cache[key] = value
            self._timestamps[key] = time.time()
            
            # Evict oldest if over capacity
            if len(self._cache) > self.max_size:
                oldest_key = next(iter(self._cache))
                del self._cache[oldest_key]
                del self._timestamps[oldest_key]
    
    async def invalidate(self, key: str) -> bool:
        """Remove key from cache."""
        async with self._lock:
            if key in self._cache:
                del self._cache[key]
                del self._timestamps[key]
                return True
            return False
    
    async def clear(self) -> None:
        """Clear entire cache."""
        async with self._lock:
            self._cache.clear()
            self._timestamps.clear()
    
    def size(self) -> int:
        """Get current cache size."""
        return len(self._cache)


class SemanticCache:
    """
    Semantic similarity-based caching for DTESN queries.
    Uses embedding similarity to match semantically similar queries.
    """
    
    def __init__(
        self,
        similarity_threshold: float = 0.85,
        embedding_dim: int = 768,
        max_entries: int = 1000
    ):
        """Initialize semantic cache."""
        self.similarity_threshold = similarity_threshold
        self.embedding_dim = embedding_dim
        self.max_entries = max_entries
        
        self._embeddings: List[np.ndarray] = []
        self._cache_keys: List[str] = []
        self._cache_values: List[Any] = []
        self._lock = asyncio.Lock()
    
    def _compute_embedding(self, query: str) -> np.ndarray:
        """
        Compute simple embedding for query.
        In production, use a proper embedding model.
        """
        # Simple hash-based embedding for demonstration
        hash_val = hashlib.sha256(query.encode()).digest()
        embedding = np.frombuffer(hash_val, dtype=np.uint8)[:self.embedding_dim]
        # Normalize
        embedding = embedding.astype(np.float32)
        embedding = embedding / (np.linalg.norm(embedding) + 1e-8)
        return embedding
    
    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        """Compute cosine similarity between two embeddings."""
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-8))
    
    async def get(self, query: str) -> Optional[Tuple[Any, float]]:
        """
        Get cached value for semantically similar query.
        Returns (value, similarity_score) or None.
        """
        async with self._lock:
            if not self._embeddings:
                return None
            
            query_embedding = self._compute_embedding(query)
            
            # Find most similar cached query
            max_similarity = 0.0
            best_idx = -1
            
            for idx, cached_embedding in enumerate(self._embeddings):
                similarity = self._cosine_similarity(query_embedding, cached_embedding)
                if similarity > max_similarity:
                    max_similarity = similarity
                    best_idx = idx
            
            # Return if above threshold
            if max_similarity >= self.similarity_threshold and best_idx >= 0:
                return (self._cache_values[best_idx], max_similarity)
            
            return None
    
    async def set(self, query: str, value: Any) -> None:
        """Cache value with query embedding."""
        async with self._lock:
            query_embedding = self._compute_embedding(query)
            
            # Evict oldest if at capacity
            if len(self._embeddings) >= self.max_entries:
                self._embeddings.pop(0)
                self._cache_keys.pop(0)
                self._cache_values.pop(0)
            
            self._embeddings.append(query_embedding)
            self._cache_keys.append(query)
            self._cache_values.append(value)
    
    async def clear(self) -> None:
        """Clear semantic cache."""
        async with self._lock:
            self._embeddings.clear()
            self._cache_keys.clear()
            self._cache_values.clear()
    
    def size(self) -> int:
        """Get current cache size."""
        return len(self._embeddings)


class CacheOptimizer:
    """
    Advanced multi-level caching system for DTESN operations.
    
    Implements:
    - L1: In-memory LRU cache for hot data
    - L2: Distributed Redis cache (simulated)
    - Semantic similarity matching for related queries
    - Intelligent cache warming and invalidation
    - Comprehensive performance metrics
    """
    
    def __init__(
        self,
        config: Optional[CacheConfiguration] = None,
        redis_client: Optional[Any] = None
    ):
        """Initialize cache optimizer."""
        self.config = config or CacheConfiguration()
        self.redis_client = redis_client
        
        # Initialize cache layers
        self.l1_cache = LRUCache(
            max_size=self.config.l1_max_size,
            ttl_seconds=self.config.l1_ttl_seconds
        )
        
        self.semantic_cache = None
        if self.config.enable_semantic_cache:
            self.semantic_cache = SemanticCache(
                similarity_threshold=self.config.semantic_similarity_threshold,
                embedding_dim=self.config.embedding_dimension,
                max_entries=self.config.l1_max_size // 2
            )
        
        # Metrics tracking
        self._metrics = CacheMetrics()
        self._popular_queries: Dict[str, int] = {}
        
        logger.info("CacheOptimizer initialized with L1 size=%d, semantic=%s",
                   self.config.l1_max_size, self.config.enable_semantic_cache)
    
    def _generate_cache_key(self, request_data: Dict[str, Any]) -> str:
        """Generate deterministic cache key from request data."""
        # Sort keys for consistency
        sorted_data = json.dumps(request_data, sort_keys=True)
        return hashlib.sha256(sorted_data.encode()).hexdigest()
    
    async def get(self, request_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Get cached result for request.
        Checks L1 -> Semantic -> L2 in order.
        """
        start_time = time.time()
        cache_key = self._generate_cache_key(request_data)
        
        self._metrics.total_requests += 1
        
        # Try L1 cache
        result = await self.l1_cache.get(cache_key)
        if result is not None:
            self._metrics.cache_hits += 1
            latency_ms = (time.time() - start_time) * 1000
            self._update_hit_latency(latency_ms)
            logger.debug("L1 cache hit for key=%s (%.2fms)", cache_key[:8], latency_ms)
            return result
        
        # Try semantic cache if enabled
        if self.semantic_cache:
            query_str = json.dumps(request_data, sort_keys=True)
            semantic_result = await self.semantic_cache.get(query_str)
            if semantic_result:
                result, similarity = semantic_result
                self._metrics.semantic_hits += 1
                latency_ms = (time.time() - start_time) * 1000
                self._update_hit_latency(latency_ms)
                logger.debug("Semantic cache hit (similarity=%.3f, %.2fms)", 
                           similarity, latency_ms)
                # Promote to L1
                await self.l1_cache.set(cache_key, result)
                return result
        
        # Try L2 cache (Redis) if enabled
        if self.config.l2_enabled and self.redis_client:
            try:
                l2_result = await self._get_from_l2(cache_key)
                if l2_result is not None:
                    self._metrics.cache_hits += 1
                    latency_ms = (time.time() - start_time) * 1000
                    self._update_hit_latency(latency_ms)
                    logger.debug("L2 cache hit for key=%s (%.2fms)", cache_key[:8], latency_ms)
                    # Promote to L1
                    await self.l1_cache.set(cache_key, l2_result)
                    return l2_result
            except Exception as e:
                logger.warning("L2 cache error: %s", e)
        
        # Cache miss
        self._metrics.cache_misses += 1
        latency_ms = (time.time() - start_time) * 1000
        self._update_miss_latency(latency_ms)
        self._metrics.update_hit_rate()
        
        return None
    
    async def set(
        self,
        request_data: Dict[str, Any],
        result: Dict[str, Any],
        ttl_override: Optional[int] = None
    ) -> None:
        """
        Cache result for request across all cache layers.
        """
        cache_key = self._generate_cache_key(request_data)
        
        # Track popular queries
        self._popular_queries[cache_key] = self._popular_queries.get(cache_key, 0) + 1
        
        # Store in L1
        await self.l1_cache.set(cache_key, result)
        
        # Store in semantic cache if enabled
        if self.semantic_cache:
            query_str = json.dumps(request_data, sort_keys=True)
            await self.semantic_cache.set(query_str, result)
        
        # Store in L2 (async if enabled)
        if self.config.l2_enabled and self.redis_client:
            if self.config.async_write_enabled:
                asyncio.create_task(self._set_to_l2(cache_key, result, ttl_override))
            else:
                await self._set_to_l2(cache_key, result, ttl_override)
        
        # Update metrics
        self._metrics.l1_cache_size = self.l1_cache.size()
        if self.semantic_cache:
            self._metrics.l2_cache_size = self.semantic_cache.size()
    
    async def invalidate(self, request_data: Dict[str, Any]) -> None:
        """Invalidate cached result for request."""
        cache_key = self._generate_cache_key(request_data)
        
        await self.l1_cache.invalidate(cache_key)
        
        if self.config.l2_enabled and self.redis_client:
            await self._delete_from_l2(cache_key)
        
        self._metrics.eviction_count += 1
    
    async def warm_cache(self, popular_requests: List[Dict[str, Any]]) -> int:
        """
        Warm cache with popular requests.
        Returns number of entries warmed.
        """
        if not self.config.enable_cache_warming:
            return 0
        
        warmed_count = 0
        for request_data in popular_requests:
            cache_key = self._generate_cache_key(request_data)
            # Check if already cached
            if await self.l1_cache.get(cache_key) is None:
                # Pre-populate cache with empty result to mark as warmed
                # Actual data will be populated on first request
                await self.l1_cache.set(cache_key, {"warmed": True, "data": None})
                warmed_count += 1
        
        logger.info("Cache warming completed: %d entries", warmed_count)
        return warmed_count
    
    async def _get_from_l2(self, key: str) -> Optional[Dict[str, Any]]:
        """Get value from L2 (Redis) cache."""
        if not self.config.l2_enabled or not self.redis_client:
            return None
        
        try:
            value = await self.redis_client.get(key)
            if value:
                return json.loads(value)
        except Exception as e:
            logger.warning(f"Redis get failed for key {key}: {e}")
        return None
    
    async def _set_to_l2(
        self,
        key: str,
        value: Dict[str, Any],
        ttl: Optional[int] = None
    ) -> None:
        """Set value in L2 (Redis) cache."""
        if not self.config.l2_enabled or not self.redis_client:
            return
        
        try:
            serialized_value = json.dumps(value)
            ttl_seconds = ttl or self.config.l2_ttl_seconds
            await self.redis_client.setex(key, ttl_seconds, serialized_value)
        except Exception as e:
            logger.warning(f"Redis set failed for key {key}: {e}")
    
    async def _delete_from_l2(self, key: str) -> None:
        """Delete value from L2 (Redis) cache."""
        if not self.config.l2_enabled or not self.redis_client:
            return
        
        try:
            await self.redis_client.delete(key)
        except Exception as e:
            logger.warning(f"Redis delete failed for key {key}: {e}")
    
    def _update_hit_latency(self, latency_ms: float) -> None:
        """Update average hit latency metric."""
        total_hits = self._metrics.cache_hits + self._metrics.semantic_hits
        if total_hits > 0:
            self._metrics.avg_hit_latency_ms = (
                (self._metrics.avg_hit_latency_ms * (total_hits - 1) + latency_ms) / total_hits
            )
    
    def _update_miss_latency(self, latency_ms: float) -> None:
        """Update average miss latency metric."""
        if self._metrics.cache_misses > 0:
            self._metrics.avg_miss_latency_ms = (
                (self._metrics.avg_miss_latency_ms * (self._metrics.cache_misses - 1) + latency_ms) 
                / self._metrics.cache_misses
            )
    
    def get_metrics(self) -> CacheMetrics:
        """Get current cache metrics."""
        self._metrics.update_hit_rate()
        self._metrics.last_updated = time.time()
        return self._metrics
    
    def get_popular_queries(self, top_n: int = 10) -> List[Tuple[str, int]]:
        """Get most popular cached queries."""
        sorted_queries = sorted(
            self._popular_queries.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return sorted_queries[:top_n]
    
    async def clear_all_caches(self) -> None:
        """Clear all cache layers."""
        await self.l1_cache.clear()
        if self.semantic_cache:
            await self.semantic_cache.clear()
        self._popular_queries.clear()
        logger.info("All caches cleared")


# Singleton instance for global access
_cache_optimizer_instance: Optional[CacheOptimizer] = None


def get_cache_optimizer(
    config: Optional[CacheConfiguration] = None,
    redis_client: Optional[Any] = None
) -> CacheOptimizer:
    """Get or create global cache optimizer instance."""
    global _cache_optimizer_instance
    
    if _cache_optimizer_instance is None:
        _cache_optimizer_instance = CacheOptimizer(config, redis_client)
    
    return _cache_optimizer_instance
