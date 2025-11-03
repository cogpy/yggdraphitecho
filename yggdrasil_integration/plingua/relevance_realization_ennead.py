"""
Relevance Realization Ennead (Triad of Triads)

This module implements the complete Ennead structure for Relevance Realization,
representing the 9-fold cognitive architecture as a Triad of Triads:

Ξ^(ℵ₀) = Θ^3_trialectic ⊂ ℂ^(ω×ω×ω)

The three levels:
1. Λ¹_autopoiesis: Self-manufacture (biosynthesis, milieu, transport)
2. Λ²_anticipation: Projective dynamics (models, state, effectors)
3. Λ³_adaptation: Agent-arena dynamics (goals, actions, affordances)

Together they form the hierarchical tangle that enables relevance realization.

References:
- Vervaeke, J. (2019). "Awakening from the Meaning Crisis"
- Varela, F., Thompson, E., & Rosch, E. (1991). "The Embodied Mind"
"""

import numpy as np
from typing import List, Dict, Optional, Any, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
import logging

from .plingua_parser import Triad, TrialecticLevel, LambdaMembrane


class EnneadLevel(Enum):
    """Levels in the Ennead (Triad of Triads)"""
    # Level 1: Autopoiesis
    BIOSYNTHESIS = "μ_biosynthesis"
    MILIEU = "σ_milieu"
    TRANSPORT = "τ_transport"
    
    # Level 2: Anticipation
    MODELS = "π_models"
    STATE = "ς_state"
    EFFECTORS = "ε_effectors"
    
    # Level 3: Adaptation
    GOALS = "γ_goals"
    ACTIONS = "α_actions"
    AFFORDANCES = "φ_affordances"


@dataclass
class AutopoieticTriad:
    """
    Level 1: Autopoiesis (Self-Manufacture)
    
    Λ¹_autopoiesis = {μ_biosynthesis, σ_milieu, τ_transport} ⊗^η ℝ^internal
    
    The impredicative cycle: ∀^ω(x,y,z) ∈ Λ¹: x ⇔^α y ⇔^α z ⇔^α x
    """
    biosynthesis: float  # μ: Creation of complex molecules
    milieu: float  # σ: Maintenance of internal conditions
    transport: float  # τ: Regulated exchange across boundaries
    
    coupling_strength: float = 0.0
    
    def update(self, dt: float = 0.01):
        """Update autopoietic dynamics"""
        # Impredicative cycle: each presupposes and creates the others
        d_bio = self.milieu * self.transport - 0.1 * self.biosynthesis
        d_mil = self.biosynthesis * self.transport - 0.1 * self.milieu
        d_trans = self.biosynthesis * self.milieu - 0.1 * self.transport
        
        self.biosynthesis += d_bio * dt
        self.milieu += d_mil * dt
        self.transport += d_trans * dt
        
        # Compute coupling
        self.coupling_strength = (
            self.biosynthesis * self.milieu +
            self.milieu * self.transport +
            self.transport * self.biosynthesis
        ) / 3.0


@dataclass
class AnticipationTriad:
    """
    Level 2: Anticipation (Projective Dynamics)
    
    Λ²_anticipation = {π_models, ς_state, ε_effectors} ⊗^θ ℂ^projective
    
    The predictive manifold: ∃^κ Ξ: internal → environmental
    """
    models: complex  # π: Internal predictive representations
    state: complex  # ς: Current organismic condition
    effectors: complex  # ε: Action-generating mechanisms
    
    prediction_error: float = 0.0
    
    def update(self, environmental_input: complex, dt: float = 0.01):
        """Update anticipatory dynamics"""
        # Predictive processing
        prediction = self.models * self.state
        self.prediction_error = abs(prediction - environmental_input)
        
        # Update model based on prediction error
        d_models = -self.prediction_error * np.conj(self.state) * dt
        d_state = self.effectors * environmental_input * dt
        d_effectors = self.models * self.state * dt
        
        self.models += d_models
        self.state += d_state
        self.effectors += d_effectors


@dataclass
class AdaptationTriad:
    """
    Level 3: Adaptation (Agent-Arena Dynamics)
    
    Λ³_adaptation = {γ_goals, α_actions, φ_affordances} ⊗^ζ ℍ^transjective
    
    The co-construction dynamic: agent ↔^δ arena ∈ ℝ^(∞×∞)
    """
    goals: np.ndarray  # γ: Intrinsic purposes (quaternion-like)
    actions: np.ndarray  # α: Behavioral repertoire
    affordances: np.ndarray  # φ: Environmental opportunities
    
    agent_arena_coupling: float = 0.0
    relevance_gradient: float = 0.0
    
    def __post_init__(self):
        """Initialize quaternion-like structures"""
        if not isinstance(self.goals, np.ndarray):
            self.goals = np.array([1.0, 0.0, 0.0, 0.0])
        if not isinstance(self.actions, np.ndarray):
            self.actions = np.array([1.0, 0.0, 0.0, 0.0])
        if not isinstance(self.affordances, np.ndarray):
            self.affordances = np.array([1.0, 0.0, 0.0, 0.0])
    
    def update(self, arena_state: np.ndarray, dt: float = 0.01):
        """Update adaptive dynamics"""
        # Agent-arena co-construction
        # Quaternion-like multiplication for transjective space
        
        # Update affordances based on arena
        self.affordances = 0.9 * self.affordances + 0.1 * arena_state
        
        # Update actions based on goals and affordances
        goal_affordance_product = self._quaternion_product(self.goals, self.affordances)
        self.actions = 0.8 * self.actions + 0.2 * goal_affordance_product
        
        # Update goals based on realized affordances
        action_affordance_product = self._quaternion_product(self.actions, self.affordances)
        self.goals = 0.95 * self.goals + 0.05 * action_affordance_product
        
        # Compute coupling
        self.agent_arena_coupling = np.dot(self.actions, self.affordances)
        
        # Compute relevance gradient: ∇relevance = ∂(grip)/∂(reality)
        grip = np.linalg.norm(self.actions)
        reality = np.linalg.norm(arena_state)
        self.relevance_gradient = grip / (reality + 1e-8)
    
    def _quaternion_product(self, q1: np.ndarray, q2: np.ndarray) -> np.ndarray:
        """Simplified quaternion-like product"""
        # Simplified version - full quaternion multiplication would be more complex
        result = np.zeros(4)
        result[0] = q1[0] * q2[0] - np.dot(q1[1:], q2[1:])
        result[1:] = q1[0] * q2[1:] + q2[0] * q1[1:] + np.cross(q1[1:], q2[1:])
        return result


@dataclass
class RelevanceRealizationEnnead:
    """
    Complete Ennead: Triad of Triads
    
    Ξ^(ℵ₀) = Θ^3_trialectic ⊂ ℂ^(ω×ω×ω)
    
    The hierarchical tangle:
    Ω^evolution = ⋃_{i=1}^{ω} Λ^i ∘ Λ^{i+1}
    """
    autopoiesis: AutopoieticTriad
    anticipation: AnticipationTriad
    adaptation: AdaptationTriad
    
    # Emergent properties
    overall_coherence: float = 0.0
    grip_on_reality: float = 0.0
    relevance_realization: float = 0.0
    
    # History for temporal dynamics
    history: List[Dict[str, Any]] = field(default_factory=list)
    
    def update(self, environmental_input: complex, arena_state: np.ndarray, dt: float = 0.01):
        """
        Update complete Ennead dynamics
        
        Args:
            environmental_input: Complex environmental signal
            arena_state: Arena state vector (quaternion-like)
            dt: Time step
        """
        # Update Level 1: Autopoiesis
        self.autopoiesis.update(dt)
        
        # Update Level 2: Anticipation
        # Couple to autopoietic state
        autopoietic_signal = complex(
            self.autopoiesis.biosynthesis,
            self.autopoiesis.milieu
        )
        self.anticipation.update(environmental_input + autopoietic_signal, dt)
        
        # Update Level 3: Adaptation
        # Couple to anticipatory state
        anticipatory_influence = np.array([
            abs(self.anticipation.models),
            abs(self.anticipation.state),
            abs(self.anticipation.effectors),
            0.0
        ])
        self.adaptation.update(arena_state + anticipatory_influence, dt)
        
        # Compute emergent properties
        self._compute_emergent_properties()
        
        # Record history
        self._record_state()
    
    def _compute_emergent_properties(self):
        """Compute emergent properties of the Ennead"""
        # Overall coherence: How well the three levels are coupled
        autopoietic_coherence = self.autopoiesis.coupling_strength
        anticipatory_coherence = 1.0 / (1.0 + self.anticipation.prediction_error)
        adaptive_coherence = self.adaptation.agent_arena_coupling
        
        self.overall_coherence = (
            autopoietic_coherence +
            anticipatory_coherence +
            adaptive_coherence
        ) / 3.0
        
        # Grip on reality: Integration across all levels
        self.grip_on_reality = (
            self.autopoiesis.coupling_strength *
            (1.0 / (1.0 + self.anticipation.prediction_error)) *
            self.adaptation.agent_arena_coupling
        )
        
        # Relevance realization: The limit of the infinite product
        # ℜ_relevance ≡ lim_{n→ω} Π_{i=1}^n Λ^i
        self.relevance_realization = (
            self.overall_coherence * self.grip_on_reality
        )
    
    def _record_state(self):
        """Record current state in history"""
        state = {
            'autopoiesis': {
                'biosynthesis': self.autopoiesis.biosynthesis,
                'milieu': self.autopoiesis.milieu,
                'transport': self.autopoiesis.transport,
                'coupling': self.autopoiesis.coupling_strength
            },
            'anticipation': {
                'models': abs(self.anticipation.models),
                'state': abs(self.anticipation.state),
                'effectors': abs(self.anticipation.effectors),
                'prediction_error': self.anticipation.prediction_error
            },
            'adaptation': {
                'goals': self.adaptation.goals.copy(),
                'actions': self.adaptation.actions.copy(),
                'affordances': self.adaptation.affordances.copy(),
                'coupling': self.adaptation.agent_arena_coupling,
                'relevance_gradient': self.adaptation.relevance_gradient
            },
            'emergent': {
                'coherence': self.overall_coherence,
                'grip': self.grip_on_reality,
                'relevance': self.relevance_realization
            }
        }
        
        self.history.append(state)
        
        # Keep history bounded
        if len(self.history) > 1000:
            self.history = self.history[-1000:]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about Ennead state"""
        return {
            'autopoiesis': {
                'biosynthesis': self.autopoiesis.biosynthesis,
                'milieu': self.autopoiesis.milieu,
                'transport': self.autopoiesis.transport,
                'coupling_strength': self.autopoiesis.coupling_strength
            },
            'anticipation': {
                'models_magnitude': abs(self.anticipation.models),
                'state_magnitude': abs(self.anticipation.state),
                'effectors_magnitude': abs(self.anticipation.effectors),
                'prediction_error': self.anticipation.prediction_error
            },
            'adaptation': {
                'goals_norm': np.linalg.norm(self.adaptation.goals),
                'actions_norm': np.linalg.norm(self.adaptation.actions),
                'affordances_norm': np.linalg.norm(self.adaptation.affordances),
                'agent_arena_coupling': self.adaptation.agent_arena_coupling,
                'relevance_gradient': self.adaptation.relevance_gradient
            },
            'emergent': {
                'overall_coherence': self.overall_coherence,
                'grip_on_reality': self.grip_on_reality,
                'relevance_realization': self.relevance_realization
            },
            'history_length': len(self.history)
        }


class EnneadFactory:
    """Factory for creating Relevance Realization Enneads"""
    
    @staticmethod
    def create_default_ennead() -> RelevanceRealizationEnnead:
        """Create Ennead with default initialization"""
        autopoiesis = AutopoieticTriad(
            biosynthesis=1.0,
            milieu=1.0,
            transport=1.0
        )
        
        anticipation = AnticipationTriad(
            models=complex(1.0, 0.0),
            state=complex(1.0, 0.0),
            effectors=complex(1.0, 0.0)
        )
        
        adaptation = AdaptationTriad(
            goals=np.array([1.0, 0.0, 0.0, 0.0]),
            actions=np.array([1.0, 0.0, 0.0, 0.0]),
            affordances=np.array([1.0, 0.0, 0.0, 0.0])
        )
        
        return RelevanceRealizationEnnead(
            autopoiesis=autopoiesis,
            anticipation=anticipation,
            adaptation=adaptation
        )
    
    @staticmethod
    def create_from_membrane(membrane: LambdaMembrane) -> RelevanceRealizationEnnead:
        """
        Create Ennead from P-Lingua membrane
        
        Args:
            membrane: Lambda membrane with triadic content
            
        Returns:
            Relevance Realization Ennead
        """
        # Extract triads from membrane
        triads = membrane.triads
        
        # Initialize based on membrane level
        if membrane.level == TrialecticLevel.AUTOPOIESIS:
            # Extract autopoietic values
            bio = float(len([t for t in triads if 'bio' in t.x.lower()])) / max(len(triads), 1)
            mil = float(len([t for t in triads if 'mil' in t.y.lower()])) / max(len(triads), 1)
            trans = float(len([t for t in triads if 'trans' in t.z.lower()])) / max(len(triads), 1)
            
            autopoiesis = AutopoieticTriad(
                biosynthesis=bio,
                milieu=mil,
                transport=trans
            )
        else:
            autopoiesis = AutopoieticTriad(1.0, 1.0, 1.0)
        
        # Default anticipation and adaptation
        anticipation = AnticipationTriad(
            models=complex(1.0, 0.0),
            state=complex(1.0, 0.0),
            effectors=complex(1.0, 0.0)
        )
        
        adaptation = AdaptationTriad(
            goals=np.array([1.0, 0.0, 0.0, 0.0]),
            actions=np.array([1.0, 0.0, 0.0, 0.0]),
            affordances=np.array([1.0, 0.0, 0.0, 0.0])
        )
        
        return RelevanceRealizationEnnead(
            autopoiesis=autopoiesis,
            anticipation=anticipation,
            adaptation=adaptation
        )
