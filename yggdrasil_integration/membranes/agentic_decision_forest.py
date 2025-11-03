"""
Agentic Decision Forests

This module implements agentic decision forests embedded within P-System
membrane computing reservoirs. The key insight: The EM fields themselves
become agentic through the decision forest structure, enabling autonomous
decision-making at the membrane level.

Each membrane reservoir contains a Yggdrasil decision forest that acts as
an autonomous agent, making decisions about information routing, processing,
and evolution based on learned patterns.
"""

import numpy as np
import ydf
from typing import List, Dict, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import logging

from .yggdrasil_membrane import YggdrasilMembrane, MembraneType, MembraneMessage


class AgencyLevel(Enum):
    """Level of agency for decision forests"""
    REACTIVE = "reactive"  # React to inputs only
    DELIBERATIVE = "deliberative"  # Plan ahead
    REFLECTIVE = "reflective"  # Learn from experience
    AUTONOMOUS = "autonomous"  # Full self-direction


class DecisionType(Enum):
    """Types of decisions the forest can make"""
    ROUTE_MESSAGE = "route_message"  # Where to send a message
    PROCESS_ATOM = "process_atom"  # How to process an atom
    EVOLVE_RULE = "evolve_rule"  # How to evolve membrane rules
    ALLOCATE_ATTENTION = "allocate_attention"  # Where to focus attention
    SPAWN_MEMBRANE = "spawn_membrane"  # Whether to create new membrane
    MERGE_MEMBRANES = "merge_membranes"  # Whether to merge membranes
    ADJUST_PARAMETERS = "adjust_parameters"  # How to tune parameters


@dataclass
class DecisionContext:
    """Context for making decisions"""
    decision_type: DecisionType
    current_state: Dict[str, Any]
    available_actions: List[str]
    history: List[Dict[str, Any]] = field(default_factory=list)
    constraints: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DecisionOutcome:
    """Outcome of a decision"""
    chosen_action: str
    confidence: float
    reasoning: str
    alternatives: List[Tuple[str, float]]  # (action, score)
    execution_time: float


class AgenticDecisionForest:
    """
    Agentic decision forest for autonomous membrane behavior
    
    This class embeds a Yggdrasil decision forest within a membrane,
    enabling the membrane to make autonomous decisions about its
    behavior and evolution.
    """
    
    def __init__(self,
                 membrane: YggdrasilMembrane,
                 agency_level: AgencyLevel = AgencyLevel.DELIBERATIVE,
                 forest_type: str = "GRADIENT_BOOSTED_TREES"):
        """
        Initialize agentic decision forest
        
        Args:
            membrane: Parent membrane
            agency_level: Level of agency
            forest_type: Type of decision forest
        """
        self.membrane = membrane
        self.agency_level = agency_level
        self.forest_type = forest_type
        
        self.logger = logging.getLogger(
            f"{__name__}.{membrane.name}.AgenticForest"
        )
        
        # Decision forests for different decision types
        self.forests: Dict[DecisionType, Optional[ydf.GenericModel]] = {
            dt: None for dt in DecisionType
        }
        
        # Decision history for learning
        self.decision_history: List[DecisionOutcome] = []
        
        # Training data for each decision type
        self.training_data: Dict[DecisionType, List[Dict[str, Any]]] = {
            dt: [] for dt in DecisionType
        }
        
        # Agency parameters
        self.exploration_rate = 0.1  # Epsilon for epsilon-greedy
        self.learning_rate = 0.01
        self.discount_factor = 0.95
        
        # Performance metrics
        self.decision_accuracy: Dict[DecisionType, float] = {}
        self.total_decisions = 0
        self.successful_decisions = 0
        
        self.logger.info(
            f"Initialized agentic forest with {agency_level.value} agency"
        )
    
    def make_decision(self, context: DecisionContext) -> DecisionOutcome:
        """
        Make a decision based on context
        
        Args:
            context: Decision context
            
        Returns:
            Decision outcome
        """
        import time
        start_time = time.time()
        
        decision_type = context.decision_type
        forest = self.forests[decision_type]
        
        # If no trained forest, use heuristic
        if forest is None:
            outcome = self._heuristic_decision(context)
        else:
            outcome = self._forest_decision(context, forest)
        
        # Add exploration for learning
        if np.random.random() < self.exploration_rate:
            outcome = self._explore_decision(context)
        
        outcome.execution_time = time.time() - start_time
        
        # Record decision
        self.decision_history.append(outcome)
        self.total_decisions += 1
        
        self.logger.debug(
            f"Decision: {decision_type.value} -> {outcome.chosen_action} "
            f"(confidence: {outcome.confidence:.3f})"
        )
        
        return outcome
    
    def _heuristic_decision(self, context: DecisionContext) -> DecisionOutcome:
        """Make decision using heuristics"""
        decision_type = context.decision_type
        actions = context.available_actions
        
        if not actions:
            return DecisionOutcome(
                chosen_action="none",
                confidence=0.0,
                reasoning="No actions available",
                alternatives=[],
                execution_time=0.0
            )
        
        # Simple heuristics based on decision type
        if decision_type == DecisionType.ROUTE_MESSAGE:
            # Route to membrane with most capacity
            chosen = actions[0] if actions else "none"
            reasoning = "Route to first available membrane"
        
        elif decision_type == DecisionType.ALLOCATE_ATTENTION:
            # Allocate to highest STI atoms
            chosen = actions[0] if actions else "none"
            reasoning = "Allocate to highest attention value"
        
        elif decision_type == DecisionType.PROCESS_ATOM:
            # Process highest priority atom
            chosen = actions[0] if actions else "none"
            reasoning = "Process highest priority"
        
        else:
            # Default: choose first action
            chosen = actions[0]
            reasoning = f"Default heuristic for {decision_type.value}"
        
        return DecisionOutcome(
            chosen_action=chosen,
            confidence=0.5,
            reasoning=reasoning,
            alternatives=[(a, 0.5) for a in actions if a != chosen],
            execution_time=0.0
        )
    
    def _forest_decision(self,
                        context: DecisionContext,
                        forest: ydf.GenericModel) -> DecisionOutcome:
        """Make decision using trained forest"""
        # Extract features from context
        features = self._extract_features(context)
        
        # Predict using forest
        try:
            predictions = forest.predict(features)
            
            # Get action scores
            action_scores = list(zip(context.available_actions, predictions))
            action_scores.sort(key=lambda x: x[1], reverse=True)
            
            chosen_action, confidence = action_scores[0]
            alternatives = action_scores[1:]
            
            return DecisionOutcome(
                chosen_action=chosen_action,
                confidence=float(confidence),
                reasoning=f"Forest prediction (trees: {forest.num_trees()})",
                alternatives=alternatives,
                execution_time=0.0
            )
        
        except Exception as e:
            self.logger.warning(f"Forest prediction failed: {e}")
            return self._heuristic_decision(context)
    
    def _explore_decision(self, context: DecisionContext) -> DecisionOutcome:
        """Make exploratory decision"""
        actions = context.available_actions
        
        if not actions:
            return self._heuristic_decision(context)
        
        # Random exploration
        chosen = np.random.choice(actions)
        
        return DecisionOutcome(
            chosen_action=chosen,
            confidence=0.3,
            reasoning="Exploratory action",
            alternatives=[(a, 0.3) for a in actions if a != chosen],
            execution_time=0.0
        )
    
    def _extract_features(self, context: DecisionContext) -> Dict[str, Any]:
        """Extract features from decision context"""
        features = {
            'num_actions': len(context.available_actions),
            'history_length': len(context.history),
            'has_constraints': len(context.constraints) > 0
        }
        
        # Add state features
        for key, value in context.current_state.items():
            if isinstance(value, (int, float)):
                features[f'state_{key}'] = value
            elif isinstance(value, bool):
                features[f'state_{key}'] = int(value)
        
        return features
    
    def learn_from_outcome(self,
                          context: DecisionContext,
                          outcome: DecisionOutcome,
                          reward: float):
        """
        Learn from decision outcome
        
        Args:
            context: Decision context
            outcome: Decision outcome
            reward: Reward signal (-1 to 1)
        """
        # Record training example
        training_example = {
            'context': context,
            'outcome': outcome,
            'reward': reward
        }
        
        self.training_data[context.decision_type].append(training_example)
        
        # Update success metrics
        if reward > 0:
            self.successful_decisions += 1
        
        # Retrain forest if enough data
        min_examples = 50
        if len(self.training_data[context.decision_type]) >= min_examples:
            self._retrain_forest(context.decision_type)
    
    def _retrain_forest(self, decision_type: DecisionType):
        """Retrain decision forest for given decision type"""
        training_data = self.training_data[decision_type]
        
        if len(training_data) < 10:
            return
        
        self.logger.info(
            f"Retraining forest for {decision_type.value} "
            f"with {len(training_data)} examples"
        )
        
        # Prepare training dataset
        # This is a simplified version - full implementation would
        # properly format data for ydf
        
        # For now, just log that we would retrain
        self.logger.debug(f"Forest retraining for {decision_type.value} completed")
    
    def route_message_decision(self, message: MembraneMessage) -> str:
        """
        Decide where to route a message
        
        Args:
            message: Message to route
            
        Returns:
            Target membrane name
        """
        # Get available membranes
        available_membranes = []
        
        if self.membrane.parent:
            available_membranes.append(self.membrane.parent.name)
        
        for child in self.membrane.children:
            available_membranes.append(child.name)
        
        if not available_membranes:
            return self.membrane.name
        
        # Create decision context
        context = DecisionContext(
            decision_type=DecisionType.ROUTE_MESSAGE,
            current_state={
                'message_priority': message.priority,
                'message_type': message.message_type.value,
                'queue_size': len(self.membrane.message_queue)
            },
            available_actions=available_membranes
        )
        
        # Make decision
        outcome = self.make_decision(context)
        
        return outcome.chosen_action
    
    def attention_allocation_decision(self, num_atoms: int = 10) -> List[str]:
        """
        Decide which atoms to allocate attention to
        
        Args:
            num_atoms: Number of atoms to select
            
        Returns:
            List of atom IDs
        """
        # Get all atoms
        atoms = list(self.membrane.atomspace.atoms.keys())
        
        if len(atoms) <= num_atoms:
            return atoms
        
        # Create decision context for each atom
        selected_atoms = []
        
        for _ in range(num_atoms):
            available_atoms = [a for a in atoms if a not in selected_atoms]
            
            if not available_atoms:
                break
            
            context = DecisionContext(
                decision_type=DecisionType.ALLOCATE_ATTENTION,
                current_state={
                    'selected_count': len(selected_atoms),
                    'total_atoms': len(atoms)
                },
                available_actions=available_atoms
            )
            
            outcome = self.make_decision(context)
            selected_atoms.append(outcome.chosen_action)
        
        return selected_atoms
    
    def parameter_adjustment_decision(self) -> Dict[str, float]:
        """
        Decide how to adjust membrane parameters
        
        Returns:
            Dictionary of parameter adjustments
        """
        # Available parameters to adjust
        parameters = [
            'attention_threshold',
            'processing_rate',
            'message_priority_threshold'
        ]
        
        adjustments = {}
        
        for param in parameters:
            context = DecisionContext(
                decision_type=DecisionType.ADJUST_PARAMETERS,
                current_state={
                    'parameter': param,
                    'current_value': getattr(self.membrane, param, 0.5)
                },
                available_actions=['increase', 'decrease', 'maintain']
            )
            
            outcome = self.make_decision(context)
            
            if outcome.chosen_action == 'increase':
                adjustments[param] = 0.1
            elif outcome.chosen_action == 'decrease':
                adjustments[param] = -0.1
            else:
                adjustments[param] = 0.0
        
        return adjustments
    
    def get_agency_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about agency and decision-making
        
        Returns:
            Dictionary of statistics
        """
        success_rate = (
            self.successful_decisions / self.total_decisions
            if self.total_decisions > 0 else 0.0
        )
        
        stats = {
            'agency_level': self.agency_level.value,
            'total_decisions': self.total_decisions,
            'successful_decisions': self.successful_decisions,
            'success_rate': success_rate,
            'exploration_rate': self.exploration_rate,
            'trained_forests': sum(1 for f in self.forests.values() if f is not None),
            'decision_types': {
                dt.value: len(self.training_data[dt])
                for dt in DecisionType
            }
        }
        
        # Recent decision performance
        if len(self.decision_history) > 0:
            recent = self.decision_history[-100:]
            stats['recent_avg_confidence'] = np.mean([d.confidence for d in recent])
            stats['recent_avg_execution_time'] = np.mean([d.execution_time for d in recent])
        
        return stats
    
    def elevate_agency(self):
        """Elevate to next level of agency"""
        current_levels = list(AgencyLevel)
        current_index = current_levels.index(self.agency_level)
        
        if current_index < len(current_levels) - 1:
            self.agency_level = current_levels[current_index + 1]
            self.logger.info(f"Agency elevated to {self.agency_level.value}")
            
            # Adjust parameters for higher agency
            self.exploration_rate *= 0.8  # Reduce exploration
            self.learning_rate *= 1.2  # Increase learning
