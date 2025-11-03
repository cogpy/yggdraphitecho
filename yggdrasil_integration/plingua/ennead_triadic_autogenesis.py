"""
Ennead-Triadic-Autogenesis Integration

This module connects the Relevance Realization Ennead with the A000081 triadic
correspondence and autogenesis engine, creating a complete cognitive architecture
where:

1. **Ennead** provides cognitive semantics (9-fold structure)
2. **Triadic Correspondence** provides computational substrate (B-Series/P-Systems/J-Surfaces)
3. **Autogenesis** provides self-modification capability

The integration creates a 4-way correspondence:

OEIS A000081 ↔ B-Series ↔ P-Systems ↔ J-Surfaces ↔ RR Ennead

This enables:
- Cognitive semantics for autogenetic modifications
- Relevance-driven self-modification
- Meaning-preserving structural evolution
"""

import numpy as np
from typing import List, Dict, Optional, Any, Tuple
from dataclasses import dataclass
import logging

from .relevance_realization_ennead import (
    RelevanceRealizationEnnead, EnneadLevel,
    AutopoieticTriad, AnticipationTriad, AdaptationTriad
)
from ..triadic.a000081_correspondence import (
    A000081TriadicSystem, TriadicElement, TriadicDomain
)
from ..triadic.autogenesis_engine import (
    AutogenesisEngine, AutogenesisMode, ModificationType,
    AutogeneticModification
)


@dataclass
class EnneadTriadicMapping:
    """
    Mapping between Ennead levels and triadic structures
    
    This creates the correspondence:
    - Autopoiesis (Λ¹) ↔ Order 1-3 rooted trees
    - Anticipation (Λ²) ↔ Order 4-6 rooted trees  
    - Adaptation (Λ³) ↔ Order 7-9 rooted trees
    """
    autopoiesis_order_range: Tuple[int, int] = (1, 3)
    anticipation_order_range: Tuple[int, int] = (4, 6)
    adaptation_order_range: Tuple[int, int] = (7, 9)


class EnneadTriadicAutogenesis:
    """
    Complete integration of Ennead, Triadic Correspondence, and Autogenesis
    
    This class provides the final piece of the cognitive architecture,
    enabling relevance-driven self-modification across all levels.
    """
    
    def __init__(self,
                 ennead: RelevanceRealizationEnnead,
                 triadic_system: A000081TriadicSystem,
                 autogenesis_mode: AutogenesisMode = AutogenesisMode.EXPLORATORY):
        """
        Initialize Ennead-Triadic-Autogenesis system
        
        Args:
            ennead: Relevance Realization Ennead
            triadic_system: A000081 triadic correspondence system
            autogenesis_mode: Mode for autogenetic modifications
        """
        self.ennead = ennead
        self.triadic_system = triadic_system
        
        # Create autogenesis engine
        self.autogenesis = AutogenesisEngine(
            triadic_system=triadic_system,
            initial_order=4,  # Start at anticipation level
            mode=autogenesis_mode
        )
        
        self.mapping = EnneadTriadicMapping()
        self.logger = logging.getLogger(f"{__name__}.EnneadTriadicAutogenesis")
        
        # Integration state
        self.current_step = 0
        self.relevance_history: List[float] = []
        self.modification_history: List[Dict[str, Any]] = []
        
        self.logger.info(
            f"Initialized Ennead-Triadic-Autogenesis system in "
            f"{autogenesis_mode.value} mode"
        )
    
    def update(self,
               environmental_input: complex,
               arena_state: np.ndarray,
               dt: float = 0.01):
        """
        Update complete integrated system
        
        Args:
            environmental_input: Environmental signal
            arena_state: Arena state
            dt: Time step
        """
        # Update Ennead
        self.ennead.update(environmental_input, arena_state, dt)
        
        # Check if relevance realization suggests modification
        if self._should_modify():
            self._perform_relevance_driven_modification()
        
        # Record state
        self.relevance_history.append(self.ennead.relevance_realization)
        self.current_step += 1
    
    def _should_modify(self) -> bool:
        """
        Determine if autogenetic modification should occur
        
        Modification is triggered when:
        1. Relevance realization is low (need to adapt)
        2. Relevance realization is very high (can transcend)
        3. Prediction error is high (need better models)
        """
        # Low relevance → need adaptation
        if self.ennead.relevance_realization < 0.3:
            self.logger.debug("Low relevance - considering modification")
            return True
        
        # Very high relevance → can transcend
        if self.ennead.relevance_realization > 0.9:
            self.logger.debug("High relevance - considering transcendence")
            return True
        
        # High prediction error → need better models
        if self.ennead.anticipation.prediction_error > 1.0:
            self.logger.debug("High prediction error - considering modification")
            return True
        
        return False
    
    def _perform_relevance_driven_modification(self):
        """Perform autogenetic modification driven by relevance realization"""
        # Determine modification type based on Ennead state
        mod_type = self._determine_modification_type()
        
        # Propose modification
        modification = self.autogenesis.propose_modification(mod_type)
        
        # Evaluate modification using relevance realization
        relevance_score = self._evaluate_modification_relevance(modification)
        
        # Execute if relevant
        if relevance_score > 0.5:
            success = self.autogenesis.execute_modification(modification)
            
            if success:
                self.logger.info(
                    f"Executed {mod_type.value} modification "
                    f"(relevance score: {relevance_score:.3f})"
                )
                
                # Record modification
                self.modification_history.append({
                    'step': self.current_step,
                    'type': mod_type.value,
                    'relevance_score': relevance_score,
                    'ennead_state': self.ennead.get_statistics()
                })
    
    def _determine_modification_type(self) -> ModificationType:
        """
        Determine modification type based on Ennead state
        
        Returns:
            Modification type
        """
        # Low autopoietic coupling → modify temporal (B-Series)
        if self.ennead.autopoiesis.coupling_strength < 0.5:
            return ModificationType.TEMPORAL
        
        # High prediction error → modify continuum (J-Surfaces)
        if self.ennead.anticipation.prediction_error > 0.8:
            return ModificationType.CONTINUUM
        
        # Low agent-arena coupling → modify spatial (P-Systems)
        if self.ennead.adaptation.agent_arena_coupling < 0.5:
            return ModificationType.SPATIAL
        
        # Otherwise, modify all three (triadic)
        return ModificationType.TRIADIC
    
    def _evaluate_modification_relevance(self,
                                        modification: AutogeneticModification) -> float:
        """
        Evaluate modification using relevance realization
        
        Args:
            modification: Proposed modification
            
        Returns:
            Relevance score (0-1)
        """
        # Simulate modification impact on Ennead
        # This is a simplified evaluation - full version would actually
        # apply the modification and measure relevance change
        
        # Base relevance on current state
        base_relevance = self.ennead.relevance_realization
        
        # Modification to higher order → potential for transcendence
        if modification.target_order > modification.source_order:
            transcendence_bonus = 0.2
        else:
            transcendence_bonus = 0.0
        
        # Modification type alignment with Ennead needs
        if modification.modification_type == ModificationType.TEMPORAL:
            # Helps autopoiesis
            type_alignment = 1.0 - self.ennead.autopoiesis.coupling_strength
        elif modification.modification_type == ModificationType.CONTINUUM:
            # Helps anticipation
            type_alignment = self.ennead.anticipation.prediction_error / 2.0
        elif modification.modification_type == ModificationType.SPATIAL:
            # Helps adaptation
            type_alignment = 1.0 - self.ennead.adaptation.agent_arena_coupling
        else:
            # Triadic helps all
            type_alignment = 0.7
        
        # Compute relevance score
        relevance_score = (
            0.4 * base_relevance +
            0.3 * type_alignment +
            0.3 * transcendence_bonus
        )
        
        return np.clip(relevance_score, 0.0, 1.0)
    
    def get_ennead_triadic_mapping(self) -> Dict[str, Any]:
        """
        Get mapping between Ennead levels and triadic orders
        
        Returns:
            Mapping information
        """
        mapping = {
            'autopoiesis': {
                'level': 'Λ¹',
                'order_range': self.mapping.autopoiesis_order_range,
                'current_state': {
                    'biosynthesis': self.ennead.autopoiesis.biosynthesis,
                    'milieu': self.ennead.autopoiesis.milieu,
                    'transport': self.ennead.autopoiesis.transport,
                    'coupling': self.ennead.autopoiesis.coupling_strength
                }
            },
            'anticipation': {
                'level': 'Λ²',
                'order_range': self.mapping.anticipation_order_range,
                'current_state': {
                    'models': abs(self.ennead.anticipation.models),
                    'state': abs(self.ennead.anticipation.state),
                    'effectors': abs(self.ennead.anticipation.effectors),
                    'prediction_error': self.ennead.anticipation.prediction_error
                }
            },
            'adaptation': {
                'level': 'Λ³',
                'order_range': self.mapping.adaptation_order_range,
                'current_state': {
                    'goals_norm': np.linalg.norm(self.ennead.adaptation.goals),
                    'actions_norm': np.linalg.norm(self.ennead.adaptation.actions),
                    'affordances_norm': np.linalg.norm(self.ennead.adaptation.affordances),
                    'coupling': self.ennead.adaptation.agent_arena_coupling,
                    'relevance_gradient': self.ennead.adaptation.relevance_gradient
                }
            },
            'triadic_system': {
                'max_order': self.triadic_system.max_order,
                'current_order': self.autogenesis.state.current_order
            }
        }
        
        return mapping
    
    def evolve(self,
               generations: int,
               environmental_signal: Optional[complex] = None,
               arena_signal: Optional[np.ndarray] = None) -> Dict[str, Any]:
        """
        Evolve system through multiple generations
        
        Args:
            generations: Number of generations
            environmental_signal: Environmental input signal
            arena_signal: Arena state signal
            
        Returns:
            Evolution statistics
        """
        self.logger.info(f"Evolving system for {generations} generations")
        
        # Default signals
        if environmental_signal is None:
            environmental_signal = complex(1.0, 0.0)
        
        if arena_signal is None:
            arena_signal = np.array([1.0, 0.0, 0.0, 0.0])
        
        # Evolution loop
        for gen in range(generations):
            # Update with varying signals
            env_signal = environmental_signal * (1.0 + 0.1 * np.sin(gen / 10.0))
            arena = arena_signal * (1.0 + 0.1 * np.cos(gen / 10.0))
            
            self.update(env_signal, arena)
        
        # Get statistics
        stats = {
            'generations': generations,
            'final_relevance': self.ennead.relevance_realization,
            'mean_relevance': np.mean(self.relevance_history) if self.relevance_history else 0.0,
            'modifications_performed': len(self.modification_history),
            'ennead_state': self.ennead.get_statistics(),
            'autogenesis_state': self.autogenesis.get_statistics(),
            'mapping': self.get_ennead_triadic_mapping()
        }
        
        self.logger.info(
            f"Evolution complete: {generations} generations, "
            f"{len(self.modification_history)} modifications, "
            f"final relevance = {self.ennead.relevance_realization:.3f}"
        )
        
        return stats
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get complete system statistics"""
        return {
            'current_step': self.current_step,
            'relevance_history_length': len(self.relevance_history),
            'modifications_performed': len(self.modification_history),
            'current_relevance': self.ennead.relevance_realization,
            'ennead': self.ennead.get_statistics(),
            'autogenesis': self.autogenesis.get_statistics(),
            'mapping': self.get_ennead_triadic_mapping()
        }
