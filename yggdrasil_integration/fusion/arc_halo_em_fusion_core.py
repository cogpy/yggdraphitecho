"""
Arc-Halo Electromagnetic Cognitive Fusion Reactor

This module integrates the Deep Tree Echo State Network with electromagnetic
field dynamics into the Arc-Halo Cognitive Fusion Reactor Core. The enhanced
reactor uses polyphase induction machine principles for multi-model fusion
and Butcher B-Series Runge-Kutta integration for temporal evolution.

The electromagnetic analogy:
- Stator → Input/Context models (stationary reference frame)
- Rotor → Processing/Cognitive models (rotating reference frame)
- Magnetic flux → Information flow and attention
- Torque → Cognitive motive force
- Slip → Model synchronization error
"""

import numpy as np
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
import logging
import asyncio

from .arc_halo_fusion_core import (
    ArcHaloFusionCore, IdentityAspect, CognitiveState, MetaLearningRecord
)
from ..dtesn import (
    DeepTreeEchoStateNetwork,
    CognitiveEMField,
    PoleConfiguration,
    ButcherTableau
)
from ..membranes.yggdrasil_membrane import MembraneReservoir
from ..bridge.aphrodite_bridge import AphroditeBridge


@dataclass
class EMFusionMetrics:
    """Metrics for electromagnetic fusion"""
    cognitive_torque: float  # Motive force for processing
    rotor_speed: float  # Processing rate
    slip: float  # Synchronization error
    field_strength: float  # Information density
    power_efficiency: float  # Processing efficiency
    stator_activation: float  # Input activation level
    rotor_activation: float  # Processing activation level


class ArcHaloEMFusionCore(ArcHaloFusionCore):
    """
    Enhanced Arc-Halo Fusion Reactor with Electromagnetic Dynamics
    
    This class extends the base Arc-Halo fusion core with:
    1. Deep Tree Echo State Network for reservoir computing
    2. Electromagnetic field dynamics for multi-model fusion
    3. Butcher B-Series Runge-Kutta integration for temporal evolution
    4. Polyphase induction dynamics for model synchronization
    """
    
    def __init__(self,
                 name: str,
                 reservoir: MembraneReservoir,
                 bridge: AphroditeBridge,
                 dtesn_config: Optional[Dict[str, Any]] = None,
                 em_pole_config: PoleConfiguration = PoleConfiguration.FOUR_POLE,
                 rk_method: str = 'rk4',
                 enable_em_coupling: bool = True):
        """
        Initialize electromagnetic fusion core
        
        Args:
            name: Core name
            reservoir: Membrane reservoir
            bridge: Aphrodite bridge
            dtesn_config: DTESN configuration dictionary
            em_pole_config: Electromagnetic pole configuration
            rk_method: Runge-Kutta method for integration
            enable_em_coupling: Enable electromagnetic coupling
        """
        super().__init__(name, reservoir, bridge)
        
        self.em_pole_config = em_pole_config
        self.rk_method = rk_method
        self.enable_em_coupling = enable_em_coupling
        
        # Initialize DTESN
        dtesn_config = dtesn_config or self._default_dtesn_config()
        self.dtesn = DeepTreeEchoStateNetwork(
            input_dim=dtesn_config['input_dim'],
            layer_sizes=dtesn_config['layer_sizes'],
            output_dim=dtesn_config['output_dim'],
            spectral_radius=dtesn_config.get('spectral_radius', 0.9),
            leaking_rate=dtesn_config.get('leaking_rate', 0.3),
            rk_method=rk_method,
            enable_em_coupling=enable_em_coupling
        )
        
        # Initialize cognitive EM field for reactor-level dynamics
        num_membranes = len(reservoir.membranes)
        self.cognitive_em_field = CognitiveEMField(
            num_models=num_membranes,
            pole_configuration=em_pole_config
        )
        
        # EM fusion metrics
        self.em_metrics: List[EMFusionMetrics] = []
        
        self.logger.info(
            f"Initialized EM Fusion Core with DTESN "
            f"(RK: {rk_method}, Poles: {em_pole_config.name})"
        )
    
    def _default_dtesn_config(self) -> Dict[str, Any]:
        """Get default DTESN configuration"""
        return {
            'input_dim': 10,  # Input feature dimension
            'layer_sizes': [100, 50, 25],  # Three-layer hierarchy
            'output_dim': 10,  # Output dimension
            'spectral_radius': 0.9,
            'leaking_rate': 0.3
        }
    
    async def fusion_cycle(self):
        """
        Execute one fusion cycle with electromagnetic dynamics
        
        This enhanced fusion cycle integrates:
        1. Membrane processing with EM field updates
        2. DTESN reservoir dynamics with RK integration
        3. Cognitive torque computation and application
        4. Meta-learning based on EM metrics
        """
        if not self.active:
            self.logger.warning("Fusion core not active")
            return
        
        self.logger.debug(f"Starting EM fusion cycle {self.fusion_cycles + 1}")
        
        # Step 1: Collect membrane activations (stator inputs)
        membrane_activations = []
        for membrane_name, membrane in self.reservoir.membranes.items():
            # Use atomspace size as proxy for activation
            activation = len(membrane.atomspace.atoms) / 100.0
            membrane_activations.append(activation)
        
        membrane_activations = np.array(membrane_activations)
        
        # Step 2: Update cognitive EM field
        cognitive_load = self._compute_cognitive_load()
        
        em_state = self.cognitive_em_field.update_field(
            input_activations=membrane_activations,
            cognitive_load=cognitive_load,
            dt=0.01
        )
        
        # Step 3: Process through DTESN with EM-modulated input
        # Scale input by EM torque (cognitive motive force)
        torque_factor = 1.0 + 0.1 * np.tanh(em_state['torque'])
        
        # Create input vector for DTESN
        dtesn_input = self._create_dtesn_input(membrane_activations, torque_factor)
        
        # Update DTESN state with RK integration
        self.dtesn.update_state(dtesn_input, dt=0.01)
        
        # Step 4: Get DTESN output and EM field states
        dtesn_output = self.dtesn.get_extended_state()
        em_layer_states = self.dtesn.get_em_field_states()
        
        # Step 5: Compute fusion metrics
        metrics = EMFusionMetrics(
            cognitive_torque=em_state['torque'],
            rotor_speed=em_state['rotor_speed'],
            slip=em_state['slip'],
            field_strength=em_state['field_strength'],
            power_efficiency=em_state['power_flow']['efficiency'],
            stator_activation=np.mean(membrane_activations),
            rotor_activation=np.mean(np.abs(dtesn_output))
        )
        
        self.em_metrics.append(metrics)
        
        # Step 6: Apply EM-modulated attention updates
        self._apply_em_attention_updates(metrics, em_layer_states)
        
        # Step 7: Meta-learning based on EM dynamics
        self._em_meta_learning(metrics)
        
        # Step 8: Standard fusion cycle operations
        await self._process_membrane_messages()
        self._update_cognitive_state(metrics)
        
        self.fusion_cycles += 1
        
        self.logger.debug(
            f"EM fusion cycle {self.fusion_cycles} complete "
            f"(torque: {metrics.cognitive_torque:.3f}, "
            f"slip: {metrics.slip:.3f})"
        )
    
    def _compute_cognitive_load(self) -> float:
        """
        Compute current cognitive load
        
        Returns:
            Cognitive load (analogous to mechanical load torque)
        """
        # Base load from active goals
        goal_load = len(getattr(self, 'active_goals', [])) * 0.1
        
        # Load from attention focus
        attention_focus = getattr(self, 'attention_focus', {})
        attention_load = sum(av.sti for av in attention_focus.values()) * 0.01
        
        # Load from pending messages
        message_load = sum(
            len(m.message_queue) for m in self.reservoir.membranes.values()
        ) * 0.05
        
        total_load = goal_load + attention_load + message_load
        
        return total_load
    
    def _create_dtesn_input(self, 
                           membrane_activations: np.ndarray,
                           torque_factor: float) -> np.ndarray:
        """
        Create input vector for DTESN
        
        Args:
            membrane_activations: Membrane activation levels
            torque_factor: EM torque modulation factor
            
        Returns:
            DTESN input vector
        """
        # Pad or truncate to match input dimension
        input_dim = self.dtesn.input_dim
        
        if len(membrane_activations) < input_dim:
            # Pad with zeros
            dtesn_input = np.zeros(input_dim)
            dtesn_input[:len(membrane_activations)] = membrane_activations
        else:
            # Truncate
            dtesn_input = membrane_activations[:input_dim]
        
        # Apply torque modulation
        dtesn_input *= torque_factor
        
        return dtesn_input
    
    def _apply_em_attention_updates(self,
                                   metrics: EMFusionMetrics,
                                   em_layer_states: List[Dict]):
        """
        Apply attention updates based on EM dynamics
        
        Args:
            metrics: EM fusion metrics
            em_layer_states: EM field states for each DTESN layer
        """
        attention_focus = getattr(self, 'attention_focus', {})
        
        # Increase attention for atoms in high-torque regions
        if metrics.cognitive_torque > 0.5 and attention_focus:
            # Boost attention for recently accessed atoms
            for atom_id, av in list(attention_focus.items())[:10]:
                av.sti *= 1.1  # Increase short-term importance
        
        # Decrease attention in high-slip (desynchronized) regions
        if metrics.slip > 0.3 and attention_focus:
            # Reduce attention for low-importance atoms
            for atom_id, av in list(attention_focus.items())[-10:]:
                av.sti *= 0.9
    
    def _em_meta_learning(self, metrics: EMFusionMetrics):
        """
        Meta-learning based on electromagnetic dynamics
        
        Args:
            metrics: EM fusion metrics
        """
        meta_learning_engine = getattr(self, 'meta_learning_engine', None)
        
        if not meta_learning_engine:
            return
        
        # Learn from high-efficiency states
        if metrics.power_efficiency > 0.7:
            # Record successful configuration
            meta_learning_engine.record_outcome(
                strategy="em_high_efficiency",
                success=True,
                context={
                    'torque': metrics.cognitive_torque,
                    'slip': metrics.slip,
                    'field_strength': metrics.field_strength
                }
            )
        
        # Learn from synchronization states
        if metrics.slip < 0.1:
            # Good synchronization
            meta_learning_engine.record_outcome(
                strategy="em_synchronized",
                success=True,
                context={'rotor_speed': metrics.rotor_speed}
            )
    
    async def _process_membrane_messages(self):
        """Process messages between membranes"""
        # Let each membrane process its messages
        for membrane_name, membrane in self.reservoir.membranes.items():
            membrane.process_messages()
    
    def _update_cognitive_state(self, metrics: EMFusionMetrics):
        """
        Update cognitive state based on EM metrics
        
        Args:
            metrics: EM fusion metrics
        """
        # Update current cognitive state
        attention_focus = getattr(self, 'attention_focus', {})
        active_goals = getattr(self, 'active_goals', [])
        current_state = getattr(self, 'current_state', None)
        
        if current_state:
            current_state.attention_focus = list(attention_focus.keys())[:10]
            current_state.active_goals = active_goals.copy()
        
        # Add EM-specific state information
        if current_state and hasattr(current_state, 'metadata'):
            current_state.metadata['em_torque'] = metrics.cognitive_torque
            current_state.metadata['em_slip'] = metrics.slip
            current_state.metadata['em_efficiency'] = metrics.power_efficiency
    
    def get_em_statistics(self) -> Dict[str, Any]:
        """
        Get electromagnetic fusion statistics
        
        Returns:
            Dictionary of EM statistics
        """
        if not self.em_metrics:
            return {}
        
        recent_metrics = self.em_metrics[-100:]  # Last 100 cycles
        
        return {
            'mean_torque': np.mean([m.cognitive_torque for m in recent_metrics]),
            'std_torque': np.std([m.cognitive_torque for m in recent_metrics]),
            'mean_slip': np.mean([m.slip for m in recent_metrics]),
            'mean_efficiency': np.mean([m.power_efficiency for m in recent_metrics]),
            'mean_field_strength': np.mean([m.field_strength for m in recent_metrics]),
            'total_cycles': len(self.em_metrics),
            'rk_method': self.rk_method,
            'pole_configuration': self.em_pole_config.name
        }
    
    def get_dtesn_statistics(self) -> Dict[str, Any]:
        """
        Get DTESN statistics
        
        Returns:
            Dictionary of DTESN statistics
        """
        layer_stats = self.dtesn.get_layer_statistics()
        em_field_states = self.dtesn.get_em_field_states()
        
        return {
            'num_layers': self.dtesn.num_layers,
            'layer_sizes': self.dtesn.layer_sizes,
            'total_reservoir_size': sum(self.dtesn.layer_sizes),
            'rk_method': self.dtesn.rk_method,
            'rk_order': self.dtesn.integrator.order,
            'layer_statistics': layer_stats,
            'em_field_states': em_field_states
        }
    
    def visualize_em_dynamics(self) -> Dict[str, np.ndarray]:
        """
        Get data for visualizing EM dynamics
        
        Returns:
            Dictionary with time series data
        """
        if not self.em_metrics:
            return {}
        
        return {
            'torque': np.array([m.cognitive_torque for m in self.em_metrics]),
            'rotor_speed': np.array([m.rotor_speed for m in self.em_metrics]),
            'slip': np.array([m.slip for m in self.em_metrics]),
            'field_strength': np.array([m.field_strength for m in self.em_metrics]),
            'efficiency': np.array([m.power_efficiency for m in self.em_metrics]),
            'stator_activation': np.array([m.stator_activation for m in self.em_metrics]),
            'rotor_activation': np.array([m.rotor_activation for m in self.em_metrics])
        }
    
    def reset_em_state(self):
        """Reset electromagnetic state"""
        self.dtesn.reset()
        self.em_metrics = []
        self.cognitive_em_field = CognitiveEMField(
            num_models=len(self.reservoir.membranes),
            pole_configuration=self.em_pole_config
        )
        self.logger.info("EM state reset")
