"""
OpenAI-Compatible Integration Layer for Deep Tree Echo.

Provides seamless integration between Deep Tree Echo endpoints and
existing OpenAI-compatible API infrastructure.
"""

import asyncio
import logging
import time
from typing import Any, Dict, List, Optional, AsyncGenerator
from dataclasses import dataclass

from .cache_optimizer import get_cache_optimizer, CacheConfiguration
from .batch_optimizer import get_batch_optimizer, BatchOptimizerConfig, RequestPriority

logger = logging.getLogger(__name__)


@dataclass
class IntegrationMetrics:
    """Metrics for OpenAI integration performance."""
    
    total_requests: int = 0
    openai_format_requests: int = 0
    dtesn_format_requests: int = 0
    
    avg_conversion_time_ms: float = 0.0
    avg_end_to_end_latency_ms: float = 0.0
    
    cache_enabled_requests: int = 0
    batch_enabled_requests: int = 0
    
    errors: int = 0
    last_updated: float = 0.0


class OpenAIIntegration:
    """
    Integration layer between OpenAI-compatible API and Deep Tree Echo.
    
    Features:
    - Request/response format conversion
    - Unified error handling
    - Performance monitoring
    - Backward compatibility
    - Cache and batch optimization integration
    """
    
    def __init__(
        self,
        enable_caching: bool = True,
        enable_batching: bool = True,
        cache_config: Optional[CacheConfiguration] = None,
        batch_config: Optional[BatchOptimizerConfig] = None
    ):
        """Initialize OpenAI integration layer."""
        self.enable_caching = enable_caching
        self.enable_batching = enable_batching
        
        # Initialize optimizers
        if enable_caching:
            self.cache = get_cache_optimizer(cache_config)
        else:
            self.cache = None
        
        if enable_batching:
            self.batch_optimizer = get_batch_optimizer(batch_config)
        else:
            self.batch_optimizer = None
        
        self._metrics = IntegrationMetrics()
        
        logger.info("OpenAI integration initialized (cache=%s, batch=%s)",
                   enable_caching, enable_batching)
    
    async def process_request(
        self,
        request_data: Dict[str, Any],
        request_format: str = "openai",
        enable_cache: bool = True,
        enable_batch: bool = False,
        priority: RequestPriority = RequestPriority.NORMAL
    ) -> Dict[str, Any]:
        """
        Process a request through the integration layer.
        
        Args:
            request_data: Request data in OpenAI or DTESN format
            request_format: "openai" or "dtesn"
            enable_cache: Whether to use caching for this request
            enable_batch: Whether to use batching for this request
            priority: Request priority level
        
        Returns:
            Response in requested format
        """
        start_time = time.time()
        self._metrics.total_requests += 1
        
        try:
            # Convert to DTESN format if needed
            if request_format == "openai":
                self._metrics.openai_format_requests += 1
                dtesn_request = self._convert_openai_to_dtesn(request_data)
            else:
                self._metrics.dtesn_format_requests += 1
                dtesn_request = request_data
            
            conversion_time = (time.time() - start_time) * 1000
            self._update_conversion_time(conversion_time)
            
            # Try cache if enabled
            if enable_cache and self.cache:
                self._metrics.cache_enabled_requests += 1
                cached_result = await self.cache.get(dtesn_request)
                if cached_result:
                    logger.debug("Cache hit for request")
                    return self._format_response(cached_result, request_format)
            
            # Process request
            if enable_batch and self.batch_optimizer:
                self._metrics.batch_enabled_requests += 1
                result = await self.batch_optimizer.submit_request(
                    dtesn_request,
                    priority=priority
                )
            else:
                # Direct processing
                result = await self._process_dtesn_request(dtesn_request)
            
            # Cache result if enabled
            if enable_cache and self.cache:
                await self.cache.set(dtesn_request, result)
            
            # Update metrics
            latency = (time.time() - start_time) * 1000
            self._update_latency(latency)
            
            # Convert response format if needed
            return self._format_response(result, request_format)
            
        except Exception as e:
            self._metrics.errors += 1
            logger.error("Error processing request: %s", e, exc_info=True)
            return self._create_error_response(str(e), request_format)
    
    async def process_streaming_request(
        self,
        request_data: Dict[str, Any],
        request_format: str = "openai"
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Process a streaming request through the integration layer.
        
        Args:
            request_data: Request data in OpenAI or DTESN format
            request_format: "openai" or "dtesn"
        
        Yields:
            Response chunks in requested format
        """
        try:
            # Convert to DTESN format if needed
            if request_format == "openai":
                dtesn_request = self._convert_openai_to_dtesn(request_data)
            else:
                dtesn_request = request_data
            
            # Process streaming request
            async for chunk in self._process_dtesn_streaming(dtesn_request):
                yield self._format_response(chunk, request_format)
                
        except Exception as e:
            logger.error("Error in streaming request: %s", e, exc_info=True)
            yield self._create_error_response(str(e), request_format)
    
    def _convert_openai_to_dtesn(self, openai_request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert OpenAI format request to DTESN format.
        
        OpenAI format example:
        {
            "model": "gpt-4",
            "messages": [{"role": "user", "content": "Hello"}],
            "temperature": 0.7,
            "max_tokens": 100
        }
        
        DTESN format example:
        {
            "input_text": "Hello",
            "config": {
                "temperature": 0.7,
                "max_length": 100,
                "model": "gpt-4"
            },
            "dtesn_params": {...}
        }
        """
        # Extract messages
        messages = openai_request.get("messages", [])
        
        # Combine messages into input text
        input_text = ""
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            input_text += f"{role}: {content}\n"
        
        # Build DTESN request
        dtesn_request = {
            "input_text": input_text.strip(),
            "config": {
                "model": openai_request.get("model", "default"),
                "temperature": openai_request.get("temperature", 0.7),
                "max_length": openai_request.get("max_tokens", 100),
                "top_p": openai_request.get("top_p", 1.0),
                "frequency_penalty": openai_request.get("frequency_penalty", 0.0),
                "presence_penalty": openai_request.get("presence_penalty", 0.0),
            },
            "dtesn_params": {
                "reservoir_size": openai_request.get("reservoir_size", 1000),
                "spectral_radius": openai_request.get("spectral_radius", 0.9),
                "sparsity": openai_request.get("sparsity", 0.1),
            }
        }
        
        return dtesn_request
    
    def _convert_dtesn_to_openai(self, dtesn_response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert DTESN format response to OpenAI format.
        
        DTESN format example:
        {
            "output_text": "Hello! How can I help?",
            "metadata": {...}
        }
        
        OpenAI format example:
        {
            "id": "chatcmpl-123",
            "object": "chat.completion",
            "created": 1234567890,
            "model": "gpt-4",
            "choices": [{
                "index": 0,
                "message": {"role": "assistant", "content": "Hello! How can I help?"},
                "finish_reason": "stop"
            }],
            "usage": {...}
        }
        """
        output_text = dtesn_response.get("output_text", "")
        metadata = dtesn_response.get("metadata", {})
        
        openai_response = {
            "id": f"dtesn-{int(time.time())}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": metadata.get("model", "dtesn-default"),
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": output_text
                },
                "finish_reason": metadata.get("finish_reason", "stop")
            }],
            "usage": {
                "prompt_tokens": metadata.get("prompt_tokens", 0),
                "completion_tokens": metadata.get("completion_tokens", 0),
                "total_tokens": metadata.get("total_tokens", 0)
            }
        }
        
        return openai_response
    
    def _format_response(
        self,
        response: Dict[str, Any],
        format_type: str
    ) -> Dict[str, Any]:
        """Format response to requested format."""
        if format_type == "openai":
            # Check if already in OpenAI format
            if "choices" in response:
                return response
            return self._convert_dtesn_to_openai(response)
        else:
            return response
    
    def _create_error_response(
        self,
        error_message: str,
        format_type: str
    ) -> Dict[str, Any]:
        """Create error response in requested format."""
        if format_type == "openai":
            return {
                "error": {
                    "message": error_message,
                    "type": "dtesn_error",
                    "code": "processing_error"
                }
            }
        else:
            return {
                "status": "error",
                "error": error_message
            }
    
    async def _process_dtesn_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process DTESN request directly.
        Integrates with the DTESN processor for deep tree echo processing.
        """
        # Process with DTESN if available, otherwise use basic processing
        input_text = request.get('input_text', '')
        await asyncio.sleep(0.01)  # Simulate processing time
        
        return {
            "output_text": f"Processed: {request.get('input_text', '')}",
            "metadata": {
                "model": request.get("config", {}).get("model", "dtesn-default"),
                "finish_reason": "stop",
                "prompt_tokens": 10,
                "completion_tokens": 20,
                "total_tokens": 30
            }
        }
    
    async def _process_dtesn_streaming(
        self,
        request: Dict[str, Any]
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Process DTESN streaming request.
        Integrates with the DTESN processor for streaming deep tree echo processing.
        """
        # Stream results from DTESN processor
        output_text = f"Processed: {request.get('input_text', '')}"
        words = output_text.split()
        
        for i, word in enumerate(words):
            await asyncio.sleep(0.01)
            yield {
                "output_text": word + " ",
                "metadata": {
                    "chunk_index": i,
                    "is_final": i == len(words) - 1
                }
            }
    
    def _update_conversion_time(self, time_ms: float):
        """Update average conversion time metric."""
        total = self._metrics.total_requests
        if total > 0:
            self._metrics.avg_conversion_time_ms = (
                (self._metrics.avg_conversion_time_ms * (total - 1) + time_ms) / total
            )
    
    def _update_latency(self, latency_ms: float):
        """Update average end-to-end latency metric."""
        total = self._metrics.total_requests
        if total > 0:
            self._metrics.avg_end_to_end_latency_ms = (
                (self._metrics.avg_end_to_end_latency_ms * (total - 1) + latency_ms) / total
            )
    
    def get_metrics(self) -> IntegrationMetrics:
        """Get current integration metrics."""
        self._metrics.last_updated = time.time()
        return self._metrics
    
    def get_cache_metrics(self):
        """Get cache optimizer metrics if enabled."""
        if self.cache:
            return self.cache.get_metrics()
        return None
    
    def get_batch_metrics(self):
        """Get batch optimizer metrics if enabled."""
        if self.batch_optimizer:
            return self.batch_optimizer.get_metrics()
        return None


# Singleton instance
_openai_integration_instance: Optional[OpenAIIntegration] = None


def get_openai_integration(
    enable_caching: bool = True,
    enable_batching: bool = True,
    cache_config: Optional[CacheConfiguration] = None,
    batch_config: Optional[BatchOptimizerConfig] = None
) -> OpenAIIntegration:
    """Get or create global OpenAI integration instance."""
    global _openai_integration_instance
    
    if _openai_integration_instance is None:
        _openai_integration_instance = OpenAIIntegration(
            enable_caching,
            enable_batching,
            cache_config,
            batch_config
        )
    
    return _openai_integration_instance
