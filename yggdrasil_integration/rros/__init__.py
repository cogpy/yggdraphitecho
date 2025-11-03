"""
RROS Integration Module

This module provides integration between the RROS (Relevance Realization
Operating System) kernel and the Yggdrasil cognitive architecture.

Components:
- RROSKernelBridge: Python interface to C++ RROS kernel
- RROSEnneadIntegration: Integration with Relevance Realization Ennead
- SiliconSageAGI: Complete AGI system

Usage:
    from yggdrasil_integration.rros import create_silicon_sage
    
    # Create Silicon Sage AGI
    sage = create_silicon_sage()
    
    # Activate and evolve
    await sage.activate()
    results = await sage.evolve(generations=100)
    
    # Get wisdom assessment
    wisdom = sage.get_wisdom_assessment()
"""

from .rros_kernel_bridge import (
    RROSKernelBridge,
    Episode,
    CognitiveMode,
    TimeScale,
    CognitiveLevel,
    CognitiveState,
    MultiScaleRelevance,
    AttentionDirective
)

from .rros_ennead_integration import RROSEnneadIntegration

from .silicon_sage_agi import (
    SiliconSageAGI,
    SiliconSageConfig,
    create_silicon_sage
)

__all__ = [
    # Kernel bridge
    'RROSKernelBridge',
    'Episode',
    'CognitiveMode',
    'TimeScale',
    'CognitiveLevel',
    'CognitiveState',
    'MultiScaleRelevance',
    'AttentionDirective',
    
    # Integration
    'RROSEnneadIntegration',
    
    # Silicon Sage AGI
    'SiliconSageAGI',
    'SiliconSageConfig',
    'create_silicon_sage'
]
