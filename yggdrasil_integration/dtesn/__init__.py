"""
Deep Tree Echo State Network (DTESN) Module

This module provides a complete implementation of Deep Tree Echo State Networks
with Butcher B-Series temporal integration and electromagnetic field dynamics.
"""

from .butcher_series import (
    RootedTree,
    ButcherTableau,
    ButcherBSeries,
    TemporalIntegrator,
    TreeOrder
)

from .electromagnetic_dynamics import (
    ElectromagneticState,
    InductionMachineParameters,
    PolyphaseInductionMachine,
    CognitiveEMField,
    PoleConfiguration,
    PhaseConfiguration
)

from .deep_tree_echo_network import (
    ReservoirLayer,
    DeepTreeEchoStateNetwork
)

__all__ = [
    # Butcher series
    'RootedTree',
    'ButcherTableau',
    'ButcherBSeries',
    'TemporalIntegrator',
    'TreeOrder',
    
    # Electromagnetic dynamics
    'ElectromagneticState',
    'InductionMachineParameters',
    'PolyphaseInductionMachine',
    'CognitiveEMField',
    'PoleConfiguration',
    'PhaseConfiguration',
    
    # Deep Tree Echo Network
    'ReservoirLayer',
    'DeepTreeEchoStateNetwork'
]
