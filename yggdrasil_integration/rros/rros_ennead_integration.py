"""
RROS-Ennead Integration

This module integrates the RROS (Relevance Realization Operating System) kernel
with the Relevance Realization Ennead, creating a complete cognitive system where:

- RROS Episodes 1-17 → Λ¹ Autopoiesis (Self-manufacture)
- RROS Episodes 18-34 → Λ² Anticipation (Projective dynamics)
- RROS Episodes 35-50 → Λ³ Adaptation (Agent-arena dynamics)

This enables episode-driven cognitive processing with full relevance realization
semantics across all three trialectic levels.
"""

import numpy as np
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
import logging

from .rros_kernel_bridge import (
    RROSKernelBridge, Episode, CognitiveState, CognitiveMode
)
from ..plingua.relevance_realization_ennead import (
    RelevanceRealizationEnnead,
    AutopoieticTriad, AnticipationTriad, AdaptationTriad
)
from enum import Enum


class TriadLevel(Enum):
    """Triad levels for episode mapping"""
    AUTOPOIESIS = "autopoiesis"
    ANTICIPATION = "anticipation"
    ADAPTATION = "adaptation"


class RROSEnneadIntegration:
    """
    Integration between RROS Kernel and Relevance Realization Ennead
    
    This class creates a bidirectional mapping:
    - RROS episodes activate corresponding Ennead levels
    - Ennead states influence RROS episode weights
    - Relevance flows between both systems
    """
    
    def __init__(self,
                 rros_kernel: RROSKernelBridge,
                 ennead: RelevanceRealizationEnnead):
        """
        Initialize RROS-Ennead integration
        
        Args:
            rros_kernel: RROS kernel bridge
            ennead: Relevance Realization Ennead
        """
        self.rros = rros_kernel
        self.ennead = ennead
        self.logger = logging.getLogger(f"{__name__}.RROSEnneadIntegration")
        
        # Episode-to-Ennead mapping
        self.episode_to_level = self._create_episode_mapping()
        
        # Integration state
        self.integration_history: List[Dict[str, Any]] = []
        self.current_step = 0
        
        self.logger.info("RROS-Ennead integration initialized")
    
    def _create_episode_mapping(self) -> Dict[Episode, TriadLevel]:
        """
        Create mapping from RROS episodes to Ennead levels
        
        Returns:
            Episode-to-level mapping
        """
        mapping = {}
        
        # Autopoiesis (Λ¹): Episodes 0-17
        autopoiesis_episodes = [
            Episode.INTRO, Episode.FLOW_MYSTICISM, Episode.CONTINUOUS_COSMOS,
            Episode.AXIAL_REVOLUTION, Episode.ISRAEL_PROPHETS, Episode.PLATO_CAVE,
            Episode.ARISTOTLE_WISDOM, Episode.ARISTOTLE_WORLDVIEW,
            Episode.SIDDHARTHA_PATH, Episode.MINDFULNESS_INSIGHT,
            Episode.HIGHER_ORDER_THOUGHT, Episode.SELF_DECEPTION,
            Episode.CHRISTIANITY_NARRATIVE, Episode.NEOPLATONISM,
            Episode.AUGUSTINE_WORLD, Episode.AQUINAS_ARISTOTLE,
            Episode.AVERROES_MAIMONIDES, Episode.SCHOLASTICISM
        ]
        
        for ep in autopoiesis_episodes:
            mapping[ep] = TriadLevel.AUTOPOIESIS
        
        # Anticipation (Λ²): Episodes 18-34
        anticipation_episodes = [
            Episode.LUTHER_MEANING, Episode.EMERGENCE_OVERVIEW,
            Episode.DESCARTES_SCIENTIFIC, Episode.BACON_GALILEO,
            Episode.SCIENTIFIC_REVOLUTION, Episode.ROMANTICISM_HORROR,
            Episode.HEGEL_HISTORY, Episode.SCHOPENHAUER_NIETZSCHE,
            Episode.EVOLUTION_MEANING, Episode.COGNITIVE_REVOLUTION,
            Episode.EMBODIED_COGNITION, Episode.OPPONENT_PROCESSING,
            Episode.RELEVANCE_REALIZATION, Episode.EXAPTATION_COOPTION,
            Episode.SHAMANISM_INTEGRATION, Episode.FLOW_METAPHOR,
            Episode.PSYCHEDELICS_INSIGHTS
        ]
        
        for ep in anticipation_episodes:
            mapping[ep] = TriadLevel.ANTICIPATION
        
        # Adaptation (Λ³): Episodes 35-50
        adaptation_episodes = [
            Episode.MYSTICAL_EXPERIENCES, Episode.GNOSIS_ANAGOGE,
            Episode.MARTIAL_ARTS, Episode.MEDITATION_WISDOM,
            Episode.CONSCIOUSNESS_MYSTERY, Episode.DEATH_MEANING,
            Episode.WISDOM_CONTEMPLATION, Episode.INTELLIGENCE_RATIONALITY,
            Episode.ECOLOGY_PRACTICES, Episode.LOVE_WISDOM,
            Episode.WONDER_CURIOSITY, Episode.PHILOSOPHY_RELIGION,
            Episode.PANPSYCHISM_EMERGENCE, Episode.RESPONSE_MEANING,
            Episode.CORBIN_JUNG, Episode.TILLICH_BARFIELD
        ]
        
        for ep in adaptation_episodes:
            mapping[ep] = TriadLevel.ADAPTATION
        
        return mapping
    
    def integrated_update(self,
                         environmental_input: complex,
                         arena_state: np.ndarray,
                         dt: float = 0.01):
        """
        Perform integrated update of both RROS and Ennead
        
        Args:
            environmental_input: Environmental signal
            arena_state: Arena state
            dt: Time step
        """
        # 1. Convert inputs for RROS
        rros_input = self._convert_to_rros_input(environmental_input, arena_state)
        
        # 2. Execute RROS cognitive cycle
        cognitive_state = self.rros.cognitive_cycle(rros_input)
        
        # 3. Activate episodes based on Ennead state
        self._activate_episodes_from_ennead()
        
        # 4. Update Ennead with RROS relevance
        self._update_ennead_from_rros(cognitive_state, environmental_input, arena_state, dt)
        
        # 5. Record integration state
        self._record_integration_state(cognitive_state)
        
        self.current_step += 1
    
    def _convert_to_rros_input(self,
                               environmental_input: complex,
                               arena_state: np.ndarray) -> np.ndarray:
        """
        Convert Ennead inputs to RROS format
        
        Args:
            environmental_input: Complex environmental signal
            arena_state: Arena state vector
            
        Returns:
            RROS input vector
        """
        # Combine real/imag parts of environmental input with arena state
        env_real = environmental_input.real
        env_imag = environmental_input.imag
        
        rros_input = np.concatenate([
            [env_real, env_imag],
            arena_state
        ])
        
        return rros_input
    
    def _activate_episodes_from_ennead(self):
        """Activate RROS episodes based on Ennead state"""
        # Autopoiesis level → Activate episodes 0-17
        autopoiesis_strength = self.ennead.autopoiesis.coupling_strength
        for ep in self.episode_to_level:
            if self.episode_to_level[ep] == TriadLevel.AUTOPOIESIS:
                self.rros.activate_episode(ep, autopoiesis_strength)
        
        # Anticipation level → Activate episodes 18-34
        anticipation_strength = 1.0 - self.ennead.anticipation.prediction_error / 2.0
        anticipation_strength = np.clip(anticipation_strength, 0.0, 1.0)
        for ep in self.episode_to_level:
            if self.episode_to_level[ep] == TriadLevel.ANTICIPATION:
                self.rros.activate_episode(ep, anticipation_strength)
        
        # Adaptation level → Activate episodes 35-50
        adaptation_strength = self.ennead.adaptation.agent_arena_coupling
        for ep in self.episode_to_level:
            if self.episode_to_level[ep] == TriadLevel.ADAPTATION:
                self.rros.activate_episode(ep, adaptation_strength)
    
    def _update_ennead_from_rros(self,
                                cognitive_state: CognitiveState,
                                environmental_input: complex,
                                arena_state: np.ndarray,
                                dt: float):
        """
        Update Ennead using RROS cognitive state
        
        Args:
            cognitive_state: RROS cognitive state
            environmental_input: Environmental signal
            arena_state: Arena state
            dt: Time step
        """
        # Modulate Ennead update with RROS relevance
        relevance_modulation = cognitive_state.global_relevance
        
        # Update Ennead with modulated inputs
        self.ennead.update(
            environmental_input * (1.0 + relevance_modulation),
            arena_state * (1.0 + relevance_modulation),
            dt
        )
        
        # Apply RROS attention to Ennead components
        self._apply_rros_attention(cognitive_state)
    
    def _apply_rros_attention(self, cognitive_state: CognitiveState):
        """
        Apply RROS attention allocation to Ennead
        
        Args:
            cognitive_state: RROS cognitive state
        """
        attention_focus = cognitive_state.attention_focus
        
        # Modulate Ennead coupling strengths based on RROS attention
        # Higher attention → stronger coupling
        
        # Autopoiesis
        if hasattr(self.ennead.autopoiesis, 'coupling_strength'):
            self.ennead.autopoiesis.coupling_strength *= (1.0 + 0.1 * attention_focus)
            self.ennead.autopoiesis.coupling_strength = np.clip(
                self.ennead.autopoiesis.coupling_strength, 0.0, 1.0
            )
        
        # Anticipation (reduce prediction error with attention)
        if hasattr(self.ennead.anticipation, 'prediction_error'):
            self.ennead.anticipation.prediction_error *= (1.0 - 0.1 * attention_focus)
            self.ennead.anticipation.prediction_error = max(
                self.ennead.anticipation.prediction_error, 0.0
            )
        
        # Adaptation (increase coupling with attention)
        if hasattr(self.ennead.adaptation, 'agent_arena_coupling'):
            self.ennead.adaptation.agent_arena_coupling *= (1.0 + 0.1 * attention_focus)
            self.ennead.adaptation.agent_arena_coupling = np.clip(
                self.ennead.adaptation.agent_arena_coupling, 0.0, 1.0
            )
    
    def _record_integration_state(self, cognitive_state: CognitiveState):
        """Record current integration state"""
        state = {
            'step': self.current_step,
            'rros_relevance': cognitive_state.global_relevance,
            'rros_attention': cognitive_state.attention_focus,
            'rros_confidence': cognitive_state.confidence,
            'ennead_relevance': self.ennead.relevance_realization,
            'autopoiesis_coupling': self.ennead.autopoiesis.coupling_strength,
            'anticipation_error': self.ennead.anticipation.prediction_error,
            'adaptation_coupling': self.ennead.adaptation.agent_arena_coupling
        }
        
        self.integration_history.append(state)
    
    def get_episode_level_activations(self) -> Dict[TriadLevel, float]:
        """
        Get average episode activation for each Ennead level
        
        Returns:
            Level-to-activation mapping
        """
        level_activations = {
            TriadLevel.AUTOPOIESIS: 0.0,
            TriadLevel.ANTICIPATION: 0.0,
            TriadLevel.ADAPTATION: 0.0
        }
        
        level_counts = {
            TriadLevel.AUTOPOIESIS: 0,
            TriadLevel.ANTICIPATION: 0,
            TriadLevel.ADAPTATION: 0
        }
        
        # Sum activations by level
        for episode, level in self.episode_to_level.items():
            activation = self.rros.episode_activations[episode]
            level_activations[level] += activation
            level_counts[level] += 1
        
        # Average
        for level in level_activations:
            if level_counts[level] > 0:
                level_activations[level] /= level_counts[level]
        
        return level_activations
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get integration statistics"""
        level_activations = self.get_episode_level_activations()
        
        stats = {
            'current_step': self.current_step,
            'rros_metrics': self.rros.get_performance_metrics(),
            'ennead_stats': self.ennead.get_statistics(),
            'level_activations': {
            'autopoiesis': level_activations[TriadLevel.AUTOPOIESIS],
            'anticipation': level_activations[TriadLevel.ANTICIPATION],
            'adaptation': level_activations[TriadLevel.ADAPTATION]
            },
            'integration_history_length': len(self.integration_history)
        }
        
        # Add recent integration metrics
        if self.integration_history:
            recent = self.integration_history[-1]
            stats['recent_state'] = recent
        
        return stats
    
    def evolve(self,
               generations: int,
               environmental_signal: Optional[complex] = None,
               arena_signal: Optional[np.ndarray] = None) -> Dict[str, Any]:
        """
        Evolve integrated system over multiple generations
        
        Args:
            generations: Number of generations
            environmental_signal: Environmental input
            arena_signal: Arena state
            
        Returns:
            Evolution statistics
        """
        self.logger.info(f"Evolving RROS-Ennead system for {generations} generations")
        
        # Default signals
        if environmental_signal is None:
            environmental_signal = complex(1.0, 0.0)
        
        if arena_signal is None:
            arena_signal = np.array([1.0, 0.0, 0.0, 0.0])
        
        # Evolution loop
        for gen in range(generations):
            # Vary signals over time
            env = environmental_signal * (1.0 + 0.1 * np.sin(gen / 10.0))
            arena = arena_signal * (1.0 + 0.1 * np.cos(gen / 10.0))
            
            self.integrated_update(env, arena)
        
        # Get final statistics
        stats = self.get_statistics()
        stats['generations'] = generations
        
        self.logger.info(
            f"Evolution complete: {generations} generations, "
            f"final relevance = {stats['ennead_stats']['emergent']['relevance_realization']:.3f}"
        )
        
        return stats
