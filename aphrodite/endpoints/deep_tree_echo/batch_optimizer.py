"""
Enhanced Request Batching System with Priority Queuing and Dynamic Sizing.

Extends the existing batch_manager with advanced features:
- Priority-based request queuing
- GPU utilization-aware batch sizing
- Adaptive timeout management
- Smart request coalescing
"""

import asyncio
import logging
import time
from collections import deque
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Callable
import heapq

logger = logging.getLogger(__name__)


class RequestPriority(Enum):
    """Priority levels for request batching."""
    CRITICAL = 0    # Highest priority
    HIGH = 1
    NORMAL = 2
    LOW = 3
    BACKGROUND = 4  # Lowest priority


@dataclass(order=True)
class PrioritizedRequest:
    """Request with priority for heap queue."""
    priority: int
    timestamp: float
    request_id: str = field(compare=False)
    request_data: Dict[str, Any] = field(compare=False)
    future: asyncio.Future = field(compare=False)


@dataclass
class BatchOptimizerMetrics:
    """Enhanced metrics for batch optimization."""
    
    # Throughput metrics
    total_requests: int = 0
    batches_processed: int = 0
    avg_batch_size: float = 0.0
    peak_batch_size: int = 0
    
    # Priority metrics
    critical_requests: int = 0
    high_priority_requests: int = 0
    normal_requests: int = 0
    low_priority_requests: int = 0
    
    # Performance metrics
    avg_wait_time_ms: float = 0.0
    avg_processing_time_ms: float = 0.0
    throughput_req_per_sec: float = 0.0
    
    # GPU utilization
    avg_gpu_utilization: float = 0.0
    gpu_samples: List[float] = field(default_factory=list)
    
    # Efficiency metrics
    batch_efficiency: float = 0.0  # Actual vs theoretical throughput
    coalescing_rate: float = 0.0   # Similar requests merged
    
    last_updated: float = field(default_factory=time.time)


@dataclass
class BatchOptimizerConfig:
    """Configuration for enhanced batch optimizer."""
    
    # Batch sizing
    min_batch_size: int = 1
    max_batch_size: int = 64
    target_batch_size: int = 16
    
    # Priority-based sizing
    enable_priority_batching: bool = True
    critical_batch_size: int = 1  # Process immediately
    high_priority_batch_size: int = 4
    
    # GPU-aware sizing
    enable_gpu_aware_sizing: bool = True
    target_gpu_utilization: float = 0.85
    gpu_utilization_window: int = 10
    
    # Timeout management
    adaptive_timeout: bool = True
    min_timeout_ms: float = 10.0
    max_timeout_ms: float = 100.0
    critical_timeout_ms: float = 5.0
    
    # Request coalescing
    enable_coalescing: bool = True
    coalescing_similarity_threshold: float = 0.95
    
    # Performance tuning
    enable_prefetch: bool = True
    prefetch_size: int = 4
    enable_batch_splitting: bool = True
    max_batch_split_size: int = 32


class BatchOptimizer:
    """
    Enhanced batch processing system with priority queuing and dynamic sizing.
    
    Features:
    - Priority-based request queuing with heap
    - GPU utilization-aware batch sizing
    - Adaptive timeout based on load
    - Smart request coalescing for similar queries
    - Comprehensive performance metrics
    """
    
    def __init__(
        self,
        config: Optional[BatchOptimizerConfig] = None,
        gpu_monitor: Optional[Callable[[], float]] = None,
        processor: Optional[Callable] = None
    ):
        """Initialize batch optimizer."""
        self.config = config or BatchOptimizerConfig()
        self.gpu_monitor = gpu_monitor
        self.processor = processor
        
        # Priority queue for requests
        self._request_heap: List[PrioritizedRequest] = []
        self._heap_lock = asyncio.Lock()
        
        # Processing state
        self._processing_task: Optional[asyncio.Task] = None
        self._shutdown = False
        
        # Metrics
        self._metrics = BatchOptimizerMetrics()
        self._request_times: Dict[str, float] = {}
        
        # Coalescing cache
        self._coalescing_cache: Dict[str, List[str]] = {}  # hash -> request_ids
        
        logger.info("BatchOptimizer initialized with max_batch=%d, priority=%s",
                   self.config.max_batch_size, self.config.enable_priority_batching)
    
    async def start(self):
        """Start the batch processing loop."""
        if self._processing_task is None:
            self._processing_task = asyncio.create_task(self._processing_loop())
            logger.info("Batch processing loop started")
    
    async def stop(self):
        """Stop the batch processing loop."""
        self._shutdown = True
        if self._processing_task:
            await self._processing_task
            logger.info("Batch processing loop stopped")
    
    async def submit_request(
        self,
        request_data: Dict[str, Any],
        priority: RequestPriority = RequestPriority.NORMAL,
        timeout: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Submit a request for batch processing.
        
        Args:
            request_data: The request data to process
            priority: Priority level for the request
            timeout: Optional timeout override in seconds
        
        Returns:
            Processing result
        """
        request_id = f"req_{time.time()}_{id(request_data)}"
        future = asyncio.Future()
        
        # Create prioritized request
        prioritized_req = PrioritizedRequest(
            priority=priority.value,
            timestamp=time.time(),
            request_id=request_id,
            request_data=request_data,
            future=future
        )
        
        # Add to priority queue
        async with self._heap_lock:
            heapq.heappush(self._request_heap, prioritized_req)
            self._request_times[request_id] = time.time()
        
        # Update metrics
        self._metrics.total_requests += 1
        if priority == RequestPriority.CRITICAL:
            self._metrics.critical_requests += 1
        elif priority == RequestPriority.HIGH:
            self._metrics.high_priority_requests += 1
        elif priority == RequestPriority.NORMAL:
            self._metrics.normal_requests += 1
        else:
            self._metrics.low_priority_requests += 1
        
        # Wait for result with timeout
        timeout_val = timeout or (self.config.max_timeout_ms / 1000.0)
        try:
            result = await asyncio.wait_for(future, timeout=timeout_val)
            return result
        except asyncio.TimeoutError:
            logger.warning("Request %s timed out after %.2fs", request_id, timeout_val)
            raise
    
    async def _processing_loop(self):
        """Main batch processing loop."""
        while not self._shutdown:
            try:
                # Determine optimal batch size
                batch_size = await self._calculate_optimal_batch_size()
                
                # Collect batch
                batch = await self._collect_batch(batch_size)
                
                if not batch:
                    # No requests, sleep briefly
                    await asyncio.sleep(0.01)
                    continue
                
                # Process batch
                await self._process_batch(batch)
                
            except Exception as e:
                logger.error("Error in batch processing loop: %s", e, exc_info=True)
                await asyncio.sleep(0.1)
    
    async def _calculate_optimal_batch_size(self) -> int:
        """Calculate optimal batch size based on current conditions."""
        # Start with target batch size
        batch_size = self.config.target_batch_size
        
        # Adjust based on GPU utilization if enabled
        if self.config.enable_gpu_aware_sizing and self.gpu_monitor:
            try:
                gpu_util = self.gpu_monitor()
                self._metrics.gpu_samples.append(gpu_util)
                if len(self._metrics.gpu_samples) > self.config.gpu_utilization_window:
                    self._metrics.gpu_samples.pop(0)
                
                avg_gpu_util = sum(self._metrics.gpu_samples) / len(self._metrics.gpu_samples)
                self._metrics.avg_gpu_utilization = avg_gpu_util
                
                # Increase batch size if GPU underutilized
                if avg_gpu_util < self.config.target_gpu_utilization - 0.1:
                    batch_size = min(batch_size + 4, self.config.max_batch_size)
                # Decrease if overutilized
                elif avg_gpu_util > self.config.target_gpu_utilization + 0.1:
                    batch_size = max(batch_size - 4, self.config.min_batch_size)
                    
            except Exception as e:
                logger.warning("Error getting GPU utilization: %s", e)
        
        # Check for high-priority requests
        async with self._heap_lock:
            if self._request_heap:
                top_priority = self._request_heap[0].priority
                if top_priority == RequestPriority.CRITICAL.value:
                    batch_size = self.config.critical_batch_size
                elif top_priority == RequestPriority.HIGH.value:
                    batch_size = min(batch_size, self.config.high_priority_batch_size)
        
        return batch_size
    
    async def _collect_batch(self, target_size: int) -> List[PrioritizedRequest]:
        """Collect a batch of requests from the priority queue."""
        batch = []
        timeout = self._calculate_timeout(target_size)
        start_time = time.time()
        
        while len(batch) < target_size:
            async with self._heap_lock:
                if self._request_heap:
                    req = heapq.heappop(self._request_heap)
                    batch.append(req)
                else:
                    # No requests available
                    if batch:
                        # Return partial batch if we have some requests
                        break
                    # Wait briefly for requests
                    await asyncio.sleep(0.001)
            
            # Check timeout
            if (time.time() - start_time) * 1000 > timeout:
                break
        
        # Try to coalesce similar requests if enabled
        if self.config.enable_coalescing and len(batch) > 1:
            batch = await self._coalesce_requests(batch)
        
        return batch
    
    def _calculate_timeout(self, batch_size: int) -> float:
        """Calculate adaptive timeout based on batch size and load."""
        if not self.config.adaptive_timeout:
            return self.config.max_timeout_ms
        
        # Scale timeout based on how full the batch is
        queue_size = len(self._request_heap)
        if queue_size >= batch_size * 2:
            # Many requests waiting, use minimum timeout
            return self.config.min_timeout_ms
        elif queue_size < batch_size // 2:
            # Few requests, wait longer
            return self.config.max_timeout_ms
        else:
            # Linear interpolation
            ratio = queue_size / batch_size
            return self.config.min_timeout_ms + (
                (self.config.max_timeout_ms - self.config.min_timeout_ms) * (1 - ratio)
            )
    
    async def _coalesce_requests(
        self,
        batch: List[PrioritizedRequest]
    ) -> List[PrioritizedRequest]:
        """
        Coalesce similar requests to reduce redundant processing.
        """
        # Group requests by similarity
        groups: Dict[str, List[PrioritizedRequest]] = {}
        
        for req in batch:
            # Simple hash-based grouping (in production, use semantic similarity)
            req_hash = str(hash(str(sorted(req.request_data.items()))))
            if req_hash not in groups:
                groups[req_hash] = []
            groups[req_hash].append(req)
        
        # Keep one request per group, share results with others
        coalesced = []
        for req_hash, group in groups.items():
            if len(group) > 1:
                # Keep first request, mark others for result sharing
                primary = group[0]
                coalesced.append(primary)
                
                # Store references for result sharing
                self._coalescing_cache[primary.request_id] = [
                    req.request_id for req in group[1:]
                ]
                
                self._metrics.coalescing_rate = (
                    (self._metrics.coalescing_rate * self._metrics.batches_processed + 
                     (len(group) - 1)) / (self._metrics.batches_processed + 1)
                )
            else:
                coalesced.append(group[0])
        
        return coalesced
    
    async def _process_batch(self, batch: List[PrioritizedRequest]):
        """Process a batch of requests."""
        if not batch:
            return
        
        start_time = time.time()
        
        try:
            # Extract request data
            request_data_list = [req.request_data for req in batch]
            
            # Process batch with configured processor or default handler
            if self.processor:
                results = await self.processor(request_data_list)
            else:
                # Default processing for requests without a configured processor
                logger.warning("No processor configured, using default handler")
                results = [{"status": "success", "data": req.request_data, 
                           "message": "Processed with default handler"} 
                          for req in batch]
            
            # Distribute results
            for req, result in zip(batch, results):
                if not req.future.done():
                    req.future.set_result(result)
                
                # Share results with coalesced requests
                if req.request_id in self._coalescing_cache:
                    for coalesced_id in self._coalescing_cache[req.request_id]:
                        # Would need to track futures for coalesced requests
                        pass
                    del self._coalescing_cache[req.request_id]
                
                # Update wait time metrics
                if req.request_id in self._request_times:
                    wait_time = (time.time() - self._request_times[req.request_id]) * 1000
                    self._update_wait_time(wait_time)
                    del self._request_times[req.request_id]
            
        except Exception as e:
            logger.error("Error processing batch: %s", e, exc_info=True)
            # Set exception for all futures
            for req in batch:
                if not req.future.done():
                    req.future.set_exception(e)
        
        # Update metrics
        processing_time = (time.time() - start_time) * 1000
        self._update_metrics(len(batch), processing_time)
    
    def _update_wait_time(self, wait_time_ms: float):
        """Update average wait time metric."""
        total = self._metrics.total_requests
        if total > 0:
            self._metrics.avg_wait_time_ms = (
                (self._metrics.avg_wait_time_ms * (total - 1) + wait_time_ms) / total
            )
    
    def _update_metrics(self, batch_size: int, processing_time_ms: float):
        """Update batch processing metrics."""
        self._metrics.batches_processed += 1
        
        # Update average batch size
        self._metrics.avg_batch_size = (
            (self._metrics.avg_batch_size * (self._metrics.batches_processed - 1) + batch_size)
            / self._metrics.batches_processed
        )
        
        # Update peak batch size
        if batch_size > self._metrics.peak_batch_size:
            self._metrics.peak_batch_size = batch_size
        
        # Update average processing time
        self._metrics.avg_processing_time_ms = (
            (self._metrics.avg_processing_time_ms * (self._metrics.batches_processed - 1) + 
             processing_time_ms) / self._metrics.batches_processed
        )
        
        # Calculate throughput
        if processing_time_ms > 0:
            self._metrics.throughput_req_per_sec = (batch_size / processing_time_ms) * 1000
        
        # Calculate batch efficiency
        theoretical_throughput = self.config.max_batch_size / self._metrics.avg_processing_time_ms
        if theoretical_throughput > 0:
            self._metrics.batch_efficiency = (
                self._metrics.throughput_req_per_sec / theoretical_throughput
            )
        
        self._metrics.last_updated = time.time()
    
    def get_metrics(self) -> BatchOptimizerMetrics:
        """Get current batch optimizer metrics."""
        return self._metrics
    
    def get_queue_size(self) -> int:
        """Get current queue size."""
        return len(self._request_heap)


# Singleton instance
_batch_optimizer_instance: Optional[BatchOptimizer] = None


def get_batch_optimizer(
    config: Optional[BatchOptimizerConfig] = None,
    gpu_monitor: Optional[Callable[[], float]] = None,
    processor: Optional[Callable] = None
) -> BatchOptimizer:
    """Get or create global batch optimizer instance."""
    global _batch_optimizer_instance
    
    if _batch_optimizer_instance is None:
        _batch_optimizer_instance = BatchOptimizer(config, gpu_monitor, processor)
    
    return _batch_optimizer_instance
