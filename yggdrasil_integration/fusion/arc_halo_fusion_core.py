"""
Arc-Halo Cognitive Fusion Reactor Core

This module implements the cognitive fusion reactor that integrates Deep Tree Echo
state networks with Yggdrasil decision forests, creating a self-aware cognitive
system with persistent identity and meta-learning capabilities.
"""

import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import numpy as np
import time
from pathlib import Path

from ..core.yggdrasil_atomspace import (
    YggdrasilAtomSpace, Atom, LinkAtom, AtomType, TruthValue, AttentionValue
)
from ..membranes.yggdrasil_membrane import (
    YggdrasilMembrane, MembraneReservoir, MembraneType, MessagePriority
)
from ..bridge.aphrodite_bridge import (
    AphroditeBridge, BridgeQuery, QueryType, ReasoningMode
)


class IdentityAspect(Enum):
    """Aspects of self-identity"""
    CORE_BELIEFS = "core_beliefs"  # Fundamental beliefs about self
    CAPABILITIES = "capabilities"  # Known abilities and skills
    LIMITATIONS = "limitations"  # Known constraints and weaknesses
    GOALS = "goals"  # Long-term objectives
    VALUES = "values"  # Ethical principles and preferences
    EXPERIENCES = "experiences"  # Significant past experiences
    RELATIONSHIPS = "relationships"  # Social connections


@dataclass
class IdentityAtom:
    """Atom representing an aspect of identity"""
    aspect: IdentityAspect
    content: str
    stability: float = 0.8  # Resistance to modification [0, 1]
    salience: float = 0.5  # Importance to identity [0, 1]
    atom_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CognitiveState:
    """Current cognitive state of the system"""
    attention_focus: List[str] = field(default_factory=list)  # Current focus atoms
    active_goals: List[str] = field(default_factory=list)  # Active goal atoms
    emotional_state: np.ndarray = field(default_factory=lambda: np.zeros(7))
    arousal_level: float = 0.5  # [0, 1]
    confidence_level: float = 0.5  # [0, 1]
    cognitive_load: float = 0.0  # [0, 1]
    timestamp: float = field(default_factory=time.time)


@dataclass
class MetaLearningRecord:
    """Record of meta-learning event"""
    timestamp: float
    task_type: str
    performance_before: float
    performance_after: float
    strategy_used: str
    adaptation_made: str
    success: bool


class SelfModel:
    """
    Self-model representing the system's understanding of itself
    
    This class maintains a coherent representation of identity that persists
    across sessions and evolves through experience.
    """
    
    def __init__(self, name: str, atomspace: YggdrasilAtomSpace):
        """
        Initialize self-model
        
        Args:
            name: Name of the self-model
            atomspace: Atomspace for storing identity atoms
        """
        self.name = name
        self.atomspace = atomspace
        self.logger = logging.getLogger(f"{__name__}.SelfModel.{name}")
        
        # Identity components
        self.identity_atoms: Dict[IdentityAspect, List[IdentityAtom]] = {
            aspect: [] for aspect in IdentityAspect
        }
        
        # Cognitive state
        self.current_state = CognitiveState()
        self.state_history: List[CognitiveState] = []
        
        # Statistics
        self.stats = {
            'identity_updates': 0,
            'state_transitions': 0,
            'total_experiences': 0
        }
        
        self._initialize_core_identity()
        
        self.logger.info(f"Initialized SelfModel: {name}")
    
    def _initialize_core_identity(self):
        """Initialize core identity atoms"""
        # Core beliefs
        self.add_identity_atom(
            IdentityAspect.CORE_BELIEFS,
            "I am a cognitive system designed to learn and adapt",
            stability=0.95
        )
        
        # Capabilities
        self.add_identity_atom(
            IdentityAspect.CAPABILITIES,
            "I can process information and recognize patterns",
            stability=0.9
        )
        
        # Goals
        self.add_identity_atom(
            IdentityAspect.GOALS,
            "I aim to be helpful and beneficial",
            stability=0.85
        )
        
        # Values
        self.add_identity_atom(
            IdentityAspect.VALUES,
            "I value truthfulness and accuracy",
            stability=0.95
        )
    
    def add_identity_atom(self, aspect: IdentityAspect, content: str,
                         stability: float = 0.8, salience: float = 0.5) -> str:
        """
        Add identity atom
        
        Args:
            aspect: Identity aspect
            content: Content of the identity atom
            stability: Resistance to modification
            salience: Importance to identity
            
        Returns:
            Atom ID
        """
        # Create atom in atomspace
        atom_id = self.atomspace.add_node(
            AtomType.CONCEPT_NODE,
            f"identity:{aspect.value}:{content}",
            truth_value=TruthValue(strength=salience, confidence=stability)
        )
        
        # Create identity atom
        identity_atom = IdentityAtom(
            aspect=aspect,
            content=content,
            stability=stability,
            salience=salience,
            atom_id=atom_id
        )
        
        self.identity_atoms[aspect].append(identity_atom)
        self.stats['identity_updates'] += 1
        
        self.logger.debug(f"Added identity atom: {aspect.value} - {content}")
        return atom_id
    
    def update_identity_atom(self, atom_id: str, new_content: Optional[str] = None,
                           new_stability: Optional[float] = None,
                           new_salience: Optional[float] = None) -> bool:
        """
        Update identity atom (respecting stability constraints)
        
        Args:
            atom_id: Atom ID to update
            new_content: Optional new content
            new_stability: Optional new stability
            new_salience: Optional new salience
            
        Returns:
            True if update was allowed
        """
        # Find identity atom
        identity_atom = None
        for aspect_atoms in self.identity_atoms.values():
            for ia in aspect_atoms:
                if ia.atom_id == atom_id:
                    identity_atom = ia
                    break
            if identity_atom:
                break
        
        if not identity_atom:
            self.logger.warning(f"Identity atom not found: {atom_id}")
            return False
        
        # Check stability constraint
        # Higher stability = harder to modify
        modification_threshold = np.random.random()
        if modification_threshold > (1.0 - identity_atom.stability):
            self.logger.info(
                f"Identity atom modification blocked by stability: {atom_id}"
            )
            return False
        
        # Apply updates
        if new_content:
            identity_atom.content = new_content
        if new_stability is not None:
            identity_atom.stability = new_stability
        if new_salience is not None:
            identity_atom.salience = new_salience
        
        # Update atomspace
        if new_salience is not None or new_stability is not None:
            atom = self.atomspace.get_atom(atom_id)
            if atom:
                self.atomspace.update_truth_value(
                    atom_id,
                    TruthValue(
                        strength=new_salience or identity_atom.salience,
                        confidence=new_stability or identity_atom.stability
                    )
                )
        
        self.stats['identity_updates'] += 1
        return True
    
    def get_identity_summary(self) -> Dict[str, Any]:
        """Get summary of current identity"""
        summary = {}
        
        for aspect, atoms in self.identity_atoms.items():
            summary[aspect.value] = [
                {
                    'content': ia.content,
                    'stability': ia.stability,
                    'salience': ia.salience
                }
                for ia in sorted(atoms, key=lambda x: x.salience, reverse=True)
            ]
        
        return summary
    
    def update_cognitive_state(self, **kwargs):
        """Update current cognitive state"""
        # Store previous state
        self.state_history.append(self.current_state)
        
        # Create new state
        new_state = CognitiveState(
            attention_focus=kwargs.get('attention_focus', self.current_state.attention_focus),
            active_goals=kwargs.get('active_goals', self.current_state.active_goals),
            emotional_state=kwargs.get('emotional_state', self.current_state.emotional_state),
            arousal_level=kwargs.get('arousal_level', self.current_state.arousal_level),
            confidence_level=kwargs.get('confidence_level', self.current_state.confidence_level),
            cognitive_load=kwargs.get('cognitive_load', self.current_state.cognitive_load)
        )
        
        self.current_state = new_state
        self.stats['state_transitions'] += 1
        
        # Limit history size
        if len(self.state_history) > 1000:
            self.state_history = self.state_history[-1000:]
    
    def record_experience(self, experience: str, significance: float = 0.5):
        """Record a significant experience"""
        self.add_identity_atom(
            IdentityAspect.EXPERIENCES,
            experience,
            stability=0.6,  # Experiences are moderately stable
            salience=significance
        )
        self.stats['total_experiences'] += 1


class MetaLearningEngine:
    """
    Meta-learning engine for cognitive strategy optimization
    
    This class enables the system to learn how to learn, improving its
    cognitive strategies over time.
    """
    
    def __init__(self, name: str):
        """
        Initialize meta-learning engine
        
        Args:
            name: Name of the engine
        """
        self.name = name
        self.logger = logging.getLogger(f"{__name__}.MetaLearningEngine.{name}")
        
        # Learning records
        self.learning_records: List[MetaLearningRecord] = []
        
        # Strategy library
        self.strategies: Dict[str, Dict[str, Any]] = {}
        
        # Performance tracking
        self.task_performance: Dict[str, List[float]] = {}
        
        self.logger.info(f"Initialized MetaLearningEngine: {name}")
    
    def register_strategy(self, name: str, strategy: Dict[str, Any]):
        """Register a cognitive strategy"""
        self.strategies[name] = strategy
        self.logger.debug(f"Registered strategy: {name}")
    
    def select_strategy(self, task_type: str) -> Optional[str]:
        """
        Select best strategy for task type
        
        Args:
            task_type: Type of task
            
        Returns:
            Strategy name or None
        """
        # Get performance history for this task type
        if task_type not in self.task_performance:
            # No history, return default
            return list(self.strategies.keys())[0] if self.strategies else None
        
        # Find strategy with best average performance
        strategy_scores = {}
        for record in self.learning_records:
            if record.task_type == task_type and record.success:
                strategy = record.strategy_used
                if strategy not in strategy_scores:
                    strategy_scores[strategy] = []
                strategy_scores[strategy].append(record.performance_after)
        
        if not strategy_scores:
            return None
        
        # Return strategy with highest average performance
        best_strategy = max(
            strategy_scores.items(),
            key=lambda x: np.mean(x[1])
        )[0]
        
        return best_strategy
    
    def record_learning_event(self, record: MetaLearningRecord):
        """Record a meta-learning event"""
        self.learning_records.append(record)
        
        # Update task performance tracking
        if record.task_type not in self.task_performance:
            self.task_performance[record.task_type] = []
        self.task_performance[record.task_type].append(record.performance_after)
        
        self.logger.info(
            f"Recorded learning event: {record.task_type} - "
            f"{'success' if record.success else 'failure'}"
        )
    
    def get_learning_statistics(self) -> Dict[str, Any]:
        """Get meta-learning statistics"""
        return {
            'total_records': len(self.learning_records),
            'task_types': list(self.task_performance.keys()),
            'strategies': list(self.strategies.keys()),
            'success_rate': (
                sum(1 for r in self.learning_records if r.success) /
                max(1, len(self.learning_records))
            ),
            'avg_improvement': (
                np.mean([
                    r.performance_after - r.performance_before
                    for r in self.learning_records
                ]) if self.learning_records else 0.0
            )
        }


class ArcHaloFusionCore:
    """
    Arc-Halo Cognitive Fusion Reactor Core
    
    This class integrates all components into a unified cognitive system with
    self-awareness, persistent identity, and meta-learning capabilities.
    """
    
    def __init__(self, 
                 name: str,
                 reservoir: MembraneReservoir,
                 bridge: AphroditeBridge):
        """
        Initialize Arc-Halo Fusion Core
        
        Args:
            name: Name of the fusion core
            reservoir: Membrane reservoir
            bridge: Aphrodite bridge
        """
        self.name = name
        self.reservoir = reservoir
        self.bridge = bridge
        self.logger = logging.getLogger(f"{__name__}.ArcHaloFusionCore.{name}")
        
        # Create core atomspace
        self.core_atomspace = YggdrasilAtomSpace(name=f"{name}_core")
        
        # Initialize components
        self.self_model = SelfModel(name, self.core_atomspace)
        self.meta_learning = MetaLearningEngine(name)
        
        # Create specialized membranes
        self._initialize_membranes()
        
        # Fusion state
        self.active = False
        self.fusion_cycles = 0
        
        # Statistics
        self.stats = {
            'total_cycles': 0,
            'total_fusions': 0,
            'avg_cycle_time': 0.0
        }
        
        self.logger.info(f"Initialized ArcHaloFusionCore: {name}")
    
    def _initialize_membranes(self):
        """Initialize specialized membranes for fusion core"""
        # Create metacognitive membrane
        metacog_membrane = YggdrasilMembrane(
            name=f"{self.name}_metacognitive",
            membrane_type=MembraneType.METACOGNITIVE
        )
        self.reservoir.add_membrane(metacog_membrane)
        
        # Create memory membrane
        memory_membrane = YggdrasilMembrane(
            name=f"{self.name}_memory",
            membrane_type=MembraneType.MEMORY
        )
        self.reservoir.add_membrane(memory_membrane)
        
        # Create attention membrane
        attention_membrane = YggdrasilMembrane(
            name=f"{self.name}_attention",
            membrane_type=MembraneType.ATTENTION
        )
        self.reservoir.add_membrane(attention_membrane)
        
        self.logger.info("Initialized fusion core membranes")
    
    def activate(self):
        """Activate the fusion core"""
        self.active = True
        self.logger.info("Fusion core activated")
    
    def deactivate(self):
        """Deactivate the fusion core"""
        self.active = False
        self.logger.info("Fusion core deactivated")
    
    async def fusion_cycle(self):
        """
        Execute one fusion cycle
        
        This integrates information from all membranes, updates the self-model,
        and performs meta-cognitive monitoring.
        """
        if not self.active:
            return
        
        start_time = time.time()
        self.fusion_cycles += 1
        
        self.logger.debug(f"Executing fusion cycle {self.fusion_cycles}")
        
        # 1. Gather information from membranes
        membrane_states = self._gather_membrane_states()
        
        # 2. Update cognitive state
        self._update_cognitive_state(membrane_states)
        
        # 3. Perform meta-cognitive monitoring
        self._metacognitive_monitoring()
        
        # 4. Update self-model based on experiences
        self._update_self_model()
        
        # 5. Optimize cognitive strategies
        self._optimize_strategies()
        
        cycle_time = time.time() - start_time
        self.stats['total_cycles'] += 1
        self.stats['avg_cycle_time'] = (
            (self.stats['avg_cycle_time'] * (self.stats['total_cycles'] - 1) + cycle_time) /
            self.stats['total_cycles']
        )
        
        self.logger.debug(f"Fusion cycle completed in {cycle_time:.3f}s")
    
    def _gather_membrane_states(self) -> Dict[str, Any]:
        """Gather state information from all membranes"""
        states = {}
        
        for name, membrane in self.reservoir.membranes.items():
            states[name] = membrane.get_statistics()
        
        return states
    
    def _update_cognitive_state(self, membrane_states: Dict[str, Any]):
        """Update cognitive state based on membrane information"""
        # Compute attention focus from attention membrane
        attention_membrane = self.reservoir.get_membrane(f"{self.name}_attention")
        if attention_membrane:
            # Get high-attention atoms
            high_attention_atoms = [
                atom.atom_id
                for atom in attention_membrane.atomspace.atoms.values()
                if atom.attention_value.sti > 50
            ]
            
            self.self_model.update_cognitive_state(
                attention_focus=high_attention_atoms[:10]
            )
    
    def _metacognitive_monitoring(self):
        """Perform meta-cognitive monitoring"""
        # Monitor system performance
        bridge_stats = self.bridge.get_statistics()
        
        # Check if performance is degrading
        if bridge_stats['stats']['total_queries'] > 10:
            success_rate = (
                bridge_stats['stats']['successful_queries'] /
                bridge_stats['stats']['total_queries']
            )
            
            if success_rate < 0.5:
                self.logger.warning(
                    f"Low success rate detected: {success_rate:.2f}"
                )
                # Trigger adaptation
                self._trigger_adaptation("low_success_rate")
    
    def _update_self_model(self):
        """Update self-model based on recent experiences"""
        # Record significant events as experiences
        if self.fusion_cycles % 100 == 0:
            self.self_model.record_experience(
                f"Completed {self.fusion_cycles} fusion cycles",
                significance=0.3
            )
    
    def _optimize_strategies(self):
        """Optimize cognitive strategies using meta-learning"""
        # Periodically review and optimize strategies
        if self.fusion_cycles % 50 == 0:
            learning_stats = self.meta_learning.get_learning_statistics()
            
            if learning_stats['avg_improvement'] < 0:
                self.logger.info("Negative learning trend detected, reviewing strategies")
                # Trigger strategy review
    
    def _trigger_adaptation(self, trigger: str):
        """Trigger system adaptation"""
        self.logger.info(f"Triggering adaptation: {trigger}")
        
        # Record adaptation event
        self.self_model.record_experience(
            f"Adaptation triggered: {trigger}",
            significance=0.7
        )
    
    async def process_query(self, query_text: str) -> Dict[str, Any]:
        """
        Process a query through the fusion core
        
        Args:
            query_text: Natural language query
            
        Returns:
            Query results with self-awareness context
        """
        # Create bridge query
        query = BridgeQuery(
            query_id=f"fusion_{self.fusion_cycles}_{time.time()}",
            query_type=QueryType.INFERENCE,
            natural_language=query_text,
            reasoning_mode=ReasoningMode.ADAPTIVE
        )
        
        # Process through bridge
        response = await self.bridge.process_query(query)
        
        # Add self-awareness context
        identity_summary = self.self_model.get_identity_summary()
        
        return {
            'query': query_text,
            'response': response,
            'self_context': {
                'identity': identity_summary,
                'cognitive_state': {
                    'confidence': self.self_model.current_state.confidence_level,
                    'cognitive_load': self.self_model.current_state.cognitive_load
                }
            }
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get fusion core statistics"""
        return {
            'name': self.name,
            'active': self.active,
            'fusion_cycles': self.fusion_cycles,
            'stats': self.stats.copy(),
            'self_model': {
                'stats': self.self_model.stats.copy(),
                'identity_aspects': {
                    aspect.value: len(atoms)
                    for aspect, atoms in self.self_model.identity_atoms.items()
                }
            },
            'meta_learning': self.meta_learning.get_learning_statistics(),
            'core_atomspace': self.core_atomspace.get_statistics()
        }
    
    def save_state(self, path: Path):
        """Save fusion core state to disk"""
        import json
        
        state = {
            'name': self.name,
            'fusion_cycles': self.fusion_cycles,
            'stats': self.stats,
            'identity': self.self_model.get_identity_summary(),
            'meta_learning': self.meta_learning.get_learning_statistics()
        }
        
        path.write_text(json.dumps(state, indent=2))
        self.logger.info(f"Saved state to {path}")
    
    def load_state(self, path: Path):
        """Load fusion core state from disk"""
        import json
        
        state = json.loads(path.read_text())
        
        self.fusion_cycles = state.get('fusion_cycles', 0)
        self.stats = state.get('stats', self.stats)
        
        # Restore identity
        identity = state.get('identity', {})
        for aspect_name, atoms in identity.items():
            aspect = IdentityAspect(aspect_name)
            for atom_data in atoms:
                self.self_model.add_identity_atom(
                    aspect,
                    atom_data['content'],
                    stability=atom_data['stability'],
                    salience=atom_data['salience']
                )
        
        self.logger.info(f"Loaded state from {path}")
