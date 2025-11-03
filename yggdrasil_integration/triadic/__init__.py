"""
Triadic Correspondence Module

This module provides the A000081 triadic correspondence between
B-Series, P-Systems, and J-Surfaces, along with the autogenesis engine.
"""

from .a000081_correspondence import (
    A000081TriadicSystem,
    TriadicElement,
    TriadicDomain,
    TriadicCorrespondence
)

from .autogenesis_engine import (
    AutogenesisEngine,
    AutogenesisMode,
    ModificationType,
    AutogeneticModification,
    AutogeneticState
)

__all__ = [
    'A000081TriadicSystem',
    'TriadicElement',
    'TriadicDomain',
    'TriadicCorrespondence',
    'AutogenesisEngine',
    'AutogenesisMode',
    'ModificationType',
    'AutogeneticModification',
    'AutogeneticState',
]
