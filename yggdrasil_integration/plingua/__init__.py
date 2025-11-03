"""
P-Lingua Integration Module

This module provides P-Lingua^{RR} integration with Yggdrasil membrane computing
and Relevance Realization Ennead.

Components:
- PLinguaParser: Parse P-Lingua source code
- PLinguaInterpreter: Execute P-Lingua programs
- RelevanceRealizationEnnead: 9-fold cognitive architecture
- PLinguaMembraneBridge: Integration with Yggdrasil membranes
- EnneadTriadicAutogenesis: Complete cognitive architecture with autogenesis
"""

from .plingua_parser import (
    PLinguaParser,
    PLinguaInterpreter,
    ThetaSystem,
    LambdaMembrane,
    AgentArena,
    Triad,
    TrialecticRule,
    TrialecticLevel,
    TargetDirection,
    Affordance
)

from .relevance_realization_ennead import (
    RelevanceRealizationEnnead,
    EnneadLevel,
    AutopoieticTriad,
    AnticipationTriad,
    AdaptationTriad,
    EnneadFactory
)

from .plingua_membrane_bridge import PLinguaMembraneBridge

from .ennead_triadic_autogenesis import (
    EnneadTriadicAutogenesis,
    EnneadTriadicMapping
)

__all__ = [
    # Parser and interpreter
    'PLinguaParser',
    'PLinguaInterpreter',
    'ThetaSystem',
    'LambdaMembrane',
    'AgentArena',
    'Triad',
    'TrialecticRule',
    'TrialecticLevel',
    'TargetDirection',
    'Affordance',
    
    # Relevance Realization Ennead
    'RelevanceRealizationEnnead',
    'EnneadLevel',
    'AutopoieticTriad',
    'AnticipationTriad',
    'AdaptationTriad',
    'EnneadFactory',
    
    # Integration
    'PLinguaMembraneBridge',
    'EnneadTriadicAutogenesis',
    'EnneadTriadicMapping',
]
