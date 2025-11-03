"""
P-Lingua Membrane Bridge

This module integrates P-Lingua^{RR} with the existing Yggdrasil membrane
computing system, creating a unified architecture where:

- P-Lingua provides the formal language for membrane specification
- Yggdrasil provides the decision forest-backed atomspace
- Relevance Realization provides the cognitive semantics

The bridge enables:
1. Translation between P-Lingua and Yggdrasil membranes
2. Execution of P-Lingua programs in Yggdrasil environment
3. Integration of RR Ennead with triadic correspondence
"""

import numpy as np
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
import logging

from .plingua_parser import (
    PLinguaParser, PLinguaInterpreter, ThetaSystem, LambdaMembrane,
    AgentArena, Triad, TrialecticRule, TrialecticLevel
)
from .relevance_realization_ennead import (
    RelevanceRealizationEnnead, EnneadFactory,
    AutopoieticTriad, AnticipationTriad, AdaptationTriad
)
from ..membranes.yggdrasil_membrane import (
    YggdrasilMembrane, MembraneType, MembraneReservoir, MembraneMessage
)
from ..core.yggdrasil_atomspace import YggdrasilAtomSpace, Atom


class PLinguaMembraneBridge:
    """
    Bridge between P-Lingua and Yggdrasil membranes
    
    This class provides bidirectional translation and integration between
    the formal P-Lingua language and the Yggdrasil membrane system.
    """
    
    def __init__(self):
        """Initialize P-Lingua membrane bridge"""
        self.logger = logging.getLogger(f"{__name__}.PLinguaMembraneBridge")
        
        # Parser and interpreter
        self.parser = PLinguaParser()
        self.interpreter: Optional[PLinguaInterpreter] = None
        
        # Mapping between P-Lingua and Yggdrasil structures
        self.membrane_map: Dict[str, YggdrasilMembrane] = {}
        self.ennead_map: Dict[str, RelevanceRealizationEnnead] = {}
        
        self.logger.info("Initialized P-Lingua membrane bridge")
    
    def parse_plingua(self, source: str) -> ThetaSystem:
        """
        Parse P-Lingua source code
        
        Args:
            source: P-Lingua source code
            
        Returns:
            Parsed Θ-system
        """
        return self.parser.parse(source)
    
    def theta_to_reservoir(self, theta_system: ThetaSystem) -> MembraneReservoir:
        """
        Convert Θ-system to Yggdrasil membrane reservoir
        
        Args:
            theta_system: Parsed Θ-system
            
        Returns:
            Membrane reservoir
        """
        self.logger.info(f"Converting Θ-system '{theta_system.model_name}' to reservoir")
        
        # Create reservoir
        reservoir = MembraneReservoir(name=theta_system.model_name)
        
        # Convert each agent-arena to membranes
        for agent_arena in theta_system.agent_arenas:
            for lambda_membrane in agent_arena.membranes:
                # Convert lambda membrane to Yggdrasil membrane
                ygg_membrane = self._lambda_to_yggdrasil(lambda_membrane)
                
                # Add to reservoir
                reservoir.add_membrane(ygg_membrane)
                
                # Store mapping
                self.membrane_map[lambda_membrane.name] = ygg_membrane
                
                # Create Ennead for this membrane
                ennead = EnneadFactory.create_from_membrane(lambda_membrane)
                self.ennead_map[lambda_membrane.name] = ennead
        
        self.logger.info(
            f"Created reservoir with {len(reservoir.membranes)} membranes"
        )
        
        return reservoir
    
    def _lambda_to_yggdrasil(self, lambda_membrane: LambdaMembrane) -> YggdrasilMembrane:
        """
        Convert lambda membrane to Yggdrasil membrane
        
        Args:
            lambda_membrane: P-Lingua lambda membrane
            
        Returns:
            Yggdrasil membrane
        """
        # Map trialectic level to membrane type
        type_map = {
            TrialecticLevel.AUTOPOIESIS: MembraneType.MEMORY,
            TrialecticLevel.ANTICIPATION: MembraneType.COGNITIVE,
            TrialecticLevel.ADAPTATION: MembraneType.METACOGNITIVE
        }
        
        membrane_type = type_map.get(
            lambda_membrane.level,
            MembraneType.COGNITIVE
        )
        
        # Create Yggdrasil membrane
        ygg_membrane = YggdrasilMembrane(
            name=lambda_membrane.name,
            membrane_type=membrane_type
        )
        
        # Convert triads to atoms
        for triad in lambda_membrane.triads:
            self._add_triad_to_atomspace(triad, ygg_membrane.atomspace)
        
        # Convert rules to membrane rules
        for rule in lambda_membrane.rules:
            self._add_rule_to_membrane(rule, ygg_membrane)
        
        return ygg_membrane
    
    def _add_triad_to_atomspace(self, triad: Triad, atomspace: YggdrasilAtomSpace):
        """Add triadic structure to atomspace"""
        # Create atoms for each element
        from ..core.yggdrasil_atomspace import AtomType, AttentionValue
        
        atom_x = Atom(
            atom_id=f"{triad.x}_atom",
            atom_type=AtomType.CONCEPT_NODE,
            name=triad.x,
            attention_value=AttentionValue(sti=100.0, lti=50.0)
        )
        
        atom_y = Atom(
            atom_id=f"{triad.y}_atom",
            atom_type=AtomType.CONCEPT_NODE,
            name=triad.y,
            attention_value=AttentionValue(sti=100.0, lti=50.0)
        )
        
        atom_z = Atom(
            atom_id=f"{triad.z}_atom",
            atom_type=AtomType.CONCEPT_NODE,
            name=triad.z,
            attention_value=AttentionValue(sti=100.0, lti=50.0)
        )
        
        # Add to atomspace
        atomspace.add_atom(atom_x)
        atomspace.add_atom(atom_y)
        atomspace.add_atom(atom_z)
        
        # Create triadic link
        # This represents the mutual constitution: x ⇔^α y ⇔^α z ⇔^α x
        triad_link = Atom(
            atom_id=f"triad_{triad.x}_{triad.y}_{triad.z}",
            atom_type=AtomType.LINK,
            name=f"({triad.x}, {triad.y}, {triad.z})",
            attention_value=AttentionValue(sti=150.0, lti=100.0)
        )
        
        atomspace.add_atom(triad_link)
    
    def _add_rule_to_membrane(self, rule: TrialecticRule, membrane: YggdrasilMembrane):
        """Add trialectic rule to membrane"""
        # Convert rule to membrane processing function
        def rule_processor(membrane_state):
            """Process trialectic transformation"""
            # This would implement the actual rule logic
            return membrane_state
        
        # Store rule in membrane metadata
        if not hasattr(membrane, 'trialectic_rules'):
            membrane.trialectic_rules = []
        
        membrane.trialectic_rules.append(rule)
    
    def reservoir_to_theta(self, reservoir: MembraneReservoir) -> ThetaSystem:
        """
        Convert Yggdrasil reservoir to Θ-system
        
        Args:
            reservoir: Membrane reservoir
            
        Returns:
            Θ-system
        """
        theta_system = ThetaSystem(model_name=reservoir.name)
        
        # Create agent-arena
        agent_arena = AgentArena(name=f"{reservoir.name}_arena")
        
        # Convert each membrane
        for membrane_name, ygg_membrane in reservoir.membranes.items():
            lambda_membrane = self._yggdrasil_to_lambda(ygg_membrane)
            agent_arena.membranes.append(lambda_membrane)
        
        theta_system.agent_arenas.append(agent_arena)
        
        return theta_system
    
    def _yggdrasil_to_lambda(self, ygg_membrane: YggdrasilMembrane) -> LambdaMembrane:
        """
        Convert Yggdrasil membrane to lambda membrane
        
        Args:
            ygg_membrane: Yggdrasil membrane
            
        Returns:
            Lambda membrane
        """
        # Map membrane type to trialectic level
        level_map = {
            MembraneType.MEMORY: TrialecticLevel.AUTOPOIESIS,
            MembraneType.COGNITIVE: TrialecticLevel.ANTICIPATION,
            MembraneType.METACOGNITIVE: TrialecticLevel.ADAPTATION
        }
        
        level = level_map.get(
            ygg_membrane.membrane_type,
            TrialecticLevel.AUTOPOIESIS
        )
        
        lambda_membrane = LambdaMembrane(
            level=level,
            name=ygg_membrane.name
        )
        
        # Extract triads from atomspace
        triads = self._extract_triads_from_atomspace(ygg_membrane.atomspace)
        lambda_membrane.triads = triads
        
        # Extract rules
        if hasattr(ygg_membrane, 'trialectic_rules'):
            lambda_membrane.rules = ygg_membrane.trialectic_rules
        
        return lambda_membrane
    
    def _extract_triads_from_atomspace(self, atomspace: YggdrasilAtomSpace) -> List[Triad]:
        """Extract triadic structures from atomspace"""
        triads = []
        
        # Look for TriadicLink atoms
        from ..core.yggdrasil_atomspace import AtomType
        
        for atom_id, atom in atomspace.atoms.items():
            if atom.atom_type == AtomType.LINK and 'triad_' in atom.atom_id:
                # Parse triad from name
                # Format: "(x, y, z)"
                name = atom.name.strip("()")
                parts = [p.strip() for p in name.split(",")]
                
                if len(parts) >= 3:
                    triad = Triad(x=parts[0], y=parts[1], z=parts[2])
                    triads.append(triad)
        
        return triads
    
    def integrate_ennead_with_membrane(self,
                                      membrane_name: str,
                                      environmental_input: complex,
                                      arena_state: np.ndarray,
                                      dt: float = 0.01):
        """
        Integrate Relevance Realization Ennead with membrane dynamics
        
        Args:
            membrane_name: Name of membrane
            environmental_input: Environmental signal
            arena_state: Arena state vector
            dt: Time step
        """
        # Get Ennead for this membrane
        ennead = self.ennead_map.get(membrane_name)
        if not ennead:
            self.logger.warning(f"No Ennead found for membrane '{membrane_name}'")
            return
        
        # Update Ennead
        ennead.update(environmental_input, arena_state, dt)
        
        # Get Yggdrasil membrane
        ygg_membrane = self.membrane_map.get(membrane_name)
        if not ygg_membrane:
            return
        
        # Update membrane based on Ennead state
        self._sync_ennead_to_membrane(ennead, ygg_membrane)
    
    def _sync_ennead_to_membrane(self,
                                ennead: RelevanceRealizationEnnead,
                                membrane: YggdrasilMembrane):
        """Synchronize Ennead state to membrane"""
        # Update membrane coherence based on Ennead
        membrane.coherence = ennead.overall_coherence
        
        # Update attention allocation based on relevance realization
        # Higher relevance → more attention
        if ennead.relevance_realization > 0.5:
            # Boost STI of atoms in this membrane
            for atom in membrane.atomspace.atoms.values():
                atom.sti *= 1.1
    
    def execute_plingua(self,
                       source: str,
                       max_steps: int = 100) -> Dict[str, Any]:
        """
        Execute P-Lingua program
        
        Args:
            source: P-Lingua source code
            max_steps: Maximum execution steps
            
        Returns:
            Execution statistics
        """
        # Parse source
        theta_system = self.parse_plingua(source)
        
        # Create interpreter
        self.interpreter = PLinguaInterpreter(theta_system)
        
        # Run interpreter
        stats = self.interpreter.run(max_steps=max_steps)
        
        return stats
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get bridge statistics"""
        stats = {
            'membranes': len(self.membrane_map),
            'enneads': len(self.ennead_map),
            'ennead_stats': {}
        }
        
        # Get Ennead statistics
        for name, ennead in self.ennead_map.items():
            stats['ennead_stats'][name] = ennead.get_statistics()
        
        return stats
