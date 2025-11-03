#!/usr/bin/env python3.11
"""
Deep Tree Echo Server Runner
Starts the FastAPI server with optimal configuration
"""
import uvicorn
from aphrodite.endpoints.deep_tree_echo.app_factory import create_app
from aphrodite.endpoints.deep_tree_echo.config import DTESNConfig


def main():
    """Start the Deep Tree Echo server"""
    # Create configuration
    config = DTESNConfig(
        max_membrane_depth=8,
        esn_reservoir_size=1024,
        enable_caching=True,
        enable_performance_monitoring=True,
        cache_ttl_seconds=300
    )
    
    # Create FastAPI app
    app = create_app(config=config)
    
    # Print startup info
    print("="*70)
    print("Deep Tree Echo FastAPI Server".center(70))
    print("="*70)
    print(f"\nConfiguration:")
    print(f"  Max Membrane Depth: {config.max_membrane_depth}")
    print(f"  ESN Reservoir Size: {config.esn_reservoir_size}")
    print(f"  Caching Enabled: {config.enable_caching}")
    print(f"  Performance Monitoring: {config.enable_performance_monitoring}")
    print(f"\nServer starting on http://0.0.0.0:8000")
    print(f"API Documentation: http://0.0.0.0:8000/docs")
    print(f"Alternative Docs: http://0.0.0.0:8000/redoc")
    print("="*70)
    print()
    
    # Run server
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
        access_log=True
    )


if __name__ == "__main__":
    main()
