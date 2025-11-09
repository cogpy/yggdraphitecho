"""
Agent-Arena-Relation (AAR) Core - Core Implementation

Location: core/aar/ (moved from root aar_core/ for consistency)

Multi-agent orchestration and simulation framework for Deep Tree Echo.

This is the core AAR implementation providing:
- Multi-agent orchestration and coordination
- Arena simulation and environment coupling  
- Embodied AI with hardware abstraction
- Relation graph and communication protocols

For Aphrodite-specific AAR integration (API gateway, function registry),
see aphrodite/aar_core/
"""

__version__ = "0.1.0"
__author__ = "EchoCog Deep Tree Echo Team"

from .orchestration.core_orchestrator import AARCoreOrchestrator
from .agents.agent_manager import AgentManager
from .arena.simulation_engine import SimulationEngine  
from .relations.relation_graph import RelationGraph
from .embodied import VirtualBody, EmbodiedAgent, ProprioceptiveSystem

__all__ = [
    'AARCoreOrchestrator',
    'AgentManager',
    'SimulationEngine', 
    'RelationGraph',
    'VirtualBody',
    'EmbodiedAgent',
    'ProprioceptiveSystem'
]

# Configuration defaults
DEFAULT_CONFIG = {
    'max_concurrent_agents': 1000,
    'arena_simulation_enabled': True,
    'relation_graph_depth': 3,
    'resource_allocation_strategy': 'adaptive'
}

def get_default_config():
    """Get default AAR configuration."""
    return DEFAULT_CONFIG.copy()
