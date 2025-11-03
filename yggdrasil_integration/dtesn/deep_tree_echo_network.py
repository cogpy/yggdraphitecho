"""
Deep Tree Echo State Network (DTESN)

This module implements a Deep Tree Echo State Network that combines:
1. Butcher B-Series rooted trees for temporal integration
2. Runge-Kutta methods for state evolution
3. Ridge regression for readout optimization
4. Electromagnetic field dynamics for multi-model fusion

The DTESN provides a reservoir computing framework with principled temporal
integration and electromagnetic coupling between reservoir layers.
"""

import numpy as np
from typing import List, Dict, Tuple, Optional, Callable
from dataclasses import dataclass, field
import logging

from .butcher_series import ButcherTableau, TemporalIntegrator
from .electromagnetic_dynamics import CognitiveEMField, PoleConfiguration


@dataclass
class ReservoirLayer:
    """
    Single layer in the Deep Tree Echo State Network
    
    Each layer represents a reservoir with its own dynamics and
    electromagnetic coupling to other layers.
    """
    size: int  # Number of neurons in this layer
    weights: np.ndarray  # Recurrent weight matrix
    input_weights: np.ndarray  # Input weight matrix
    bias: np.ndarray  # Bias vector
    spectral_radius: float = 0.9  # Spectral radius for stability
    leaking_rate: float = 0.3  # Leaking rate (α)
    activation: Callable = np.tanh  # Activation function
    
    # Electromagnetic coupling
    em_field: Optional[CognitiveEMField] = None
    
    def __post_init__(self):
        """Initialize layer"""
        # Ensure spectral radius constraint
        eigenvalues = np.linalg.eigvals(self.weights)
        current_radius = np.max(np.abs(eigenvalues))
        if current_radius > 0:
            self.weights *= self.spectral_radius / current_radius


class DeepTreeEchoStateNetwork:
    """
    Deep Tree Echo State Network with Butcher series integration
    
    This network implements a hierarchical reservoir computing architecture
    with principled temporal integration using Runge-Kutta methods derived
    from Butcher B-Series rooted trees.
    """
    
    def __init__(self,
                 input_dim: int,
                 layer_sizes: List[int],
                 output_dim: int,
                 spectral_radius: float = 0.9,
                 leaking_rate: float = 0.3,
                 input_scaling: float = 1.0,
                 rk_method: str = 'rk4',
                 ridge_lambda: float = 1e-6,
                 enable_em_coupling: bool = True):
        """
        Initialize Deep Tree Echo State Network
        
        Args:
            input_dim: Input dimension
            layer_sizes: List of reservoir sizes for each layer
            output_dim: Output dimension
            spectral_radius: Spectral radius for reservoir stability
            leaking_rate: Leaking rate for reservoir dynamics
            input_scaling: Input scaling factor
            rk_method: Runge-Kutta method ('euler', 'heun', 'rk4', 'rk38')
            ridge_lambda: Ridge regression regularization parameter
            enable_em_coupling: Enable electromagnetic coupling between layers
        """
        self.input_dim = input_dim
        self.layer_sizes = layer_sizes
        self.output_dim = output_dim
        self.num_layers = len(layer_sizes)
        
        self.spectral_radius = spectral_radius
        self.leaking_rate = leaking_rate
        self.input_scaling = input_scaling
        self.ridge_lambda = ridge_lambda
        self.enable_em_coupling = enable_em_coupling
        
        self.logger = logging.getLogger(f"{__name__}.DeepTreeEchoStateNetwork")
        
        # Initialize Runge-Kutta integrator
        self.rk_method = rk_method
        self.integrator = self._create_integrator(rk_method)
        
        # Initialize layers
        self.layers: List[ReservoirLayer] = []
        self._initialize_layers()
        
        # Initialize readout weights (to be trained)
        total_reservoir_size = sum(layer_sizes)
        self.readout_weights = np.zeros((output_dim, total_reservoir_size + 1))  # +1 for bias
        
        # Current state
        self.states = [np.zeros(size) for size in layer_sizes]
        
        self.logger.info(
            f"Initialized DTESN: {input_dim} → {layer_sizes} → {output_dim} "
            f"(RK: {rk_method}, EM coupling: {enable_em_coupling})"
        )
    
    def _create_integrator(self, method: str) -> TemporalIntegrator:
        """Create Runge-Kutta integrator"""
        tableau_map = {
            'euler': ButcherTableau.explicit_euler(),
            'heun': ButcherTableau.heun(),
            'midpoint': ButcherTableau.midpoint(),
            'rk4': ButcherTableau.rk4(),
            'rk38': ButcherTableau.rk38()
        }
        
        tableau = tableau_map.get(method, ButcherTableau.rk4())
        return TemporalIntegrator(tableau)
    
    def _initialize_layers(self):
        """Initialize reservoir layers"""
        prev_size = self.input_dim
        
        for i, size in enumerate(self.layer_sizes):
            # Random recurrent weights
            weights = np.random.randn(size, size) * 0.5
            
            # Random input weights
            input_weights = np.random.randn(size, prev_size) * self.input_scaling
            
            # Random bias
            bias = np.random.randn(size) * 0.1
            
            # Create electromagnetic field for this layer
            em_field = None
            if self.enable_em_coupling:
                # Use different pole configurations for different layers
                pole_configs = [
                    PoleConfiguration.TWO_POLE,
                    PoleConfiguration.FOUR_POLE,
                    PoleConfiguration.SIX_POLE,
                    PoleConfiguration.EIGHT_POLE
                ]
                pole_config = pole_configs[min(i, len(pole_configs) - 1)]
                em_field = CognitiveEMField(num_models=3, pole_configuration=pole_config)
            
            # Create layer
            layer = ReservoirLayer(
                size=size,
                weights=weights,
                input_weights=input_weights,
                bias=bias,
                spectral_radius=self.spectral_radius,
                leaking_rate=self.leaking_rate,
                activation=np.tanh,
                em_field=em_field
            )
            
            self.layers.append(layer)
            prev_size = size
    
    def _reservoir_dynamics(self, layer_idx: int, t: float, state: np.ndarray, 
                           input_signal: np.ndarray) -> np.ndarray:
        """
        Compute reservoir dynamics for RK integration
        
        dx/dt = -α*x + α*f(W*x + W_in*u + b)
        
        Args:
            layer_idx: Layer index
            t: Time (not used in autonomous system)
            state: Current state
            input_signal: Input signal
            
        Returns:
            State derivative
        """
        layer = self.layers[layer_idx]
        
        # Pre-activation
        pre_activation = (
            layer.weights @ state +
            layer.input_weights @ input_signal +
            layer.bias
        )
        
        # Apply activation
        activated = layer.activation(pre_activation)
        
        # Leaky integrator dynamics
        derivative = -layer.leaking_rate * state + layer.leaking_rate * activated
        
        return derivative
    
    def update_state(self, input_signal: np.ndarray, dt: float = 0.01) -> List[np.ndarray]:
        """
        Update reservoir states using Runge-Kutta integration
        
        Args:
            input_signal: Input signal
            dt: Time step
            
        Returns:
            Updated states for all layers
        """
        current_input = input_signal
        
        for i, layer in enumerate(self.layers):
            # Define dynamics function for this layer
            def dynamics(t, state):
                return self._reservoir_dynamics(i, t, state, current_input)
            
            # Integrate using RK method
            _, new_state = self.integrator.step(
                dynamics,
                t=0.0,
                y=self.states[i],
                h=dt
            )
            
            self.states[i] = new_state
            
            # Apply electromagnetic coupling if enabled
            if self.enable_em_coupling and layer.em_field is not None:
                # Use reservoir state as model activations
                activations = self.states[i][:min(3, len(self.states[i]))]
                
                # Compute cognitive load from state magnitude
                cognitive_load = np.linalg.norm(self.states[i]) * 0.1
                
                # Update EM field
                em_state = layer.em_field.update_field(
                    activations,
                    cognitive_load,
                    dt
                )
                
                # Modulate state based on EM torque (cognitive motive force)
                torque_factor = 1.0 + 0.1 * np.tanh(em_state['torque'])
                self.states[i] *= torque_factor
            
            # Use current layer output as input to next layer
            current_input = self.states[i]
        
        return self.states
    
    def get_extended_state(self) -> np.ndarray:
        """
        Get extended state vector (concatenation of all layer states + bias)
        
        Returns:
            Extended state vector
        """
        concatenated = np.concatenate(self.states)
        return np.append(concatenated, 1.0)  # Add bias
    
    def train_readout(self, 
                     inputs: np.ndarray,
                     targets: np.ndarray,
                     dt: float = 0.01,
                     washout: int = 100) -> Dict[str, float]:
        """
        Train readout layer using ridge regression
        
        Args:
            inputs: Input sequences [num_samples, time_steps, input_dim]
            targets: Target sequences [num_samples, time_steps, output_dim]
            dt: Time step for integration
            washout: Number of initial steps to discard
            
        Returns:
            Training metrics
        """
        self.logger.info("Training readout layer with ridge regression...")
        
        # Collect reservoir states
        all_states = []
        all_targets = []
        
        for sample_idx in range(len(inputs)):
            # Reset reservoir
            self.reset()
            
            # Run through sequence
            for t in range(len(inputs[sample_idx])):
                self.update_state(inputs[sample_idx][t], dt)
                
                # Collect states after washout
                if t >= washout:
                    all_states.append(self.get_extended_state())
                    all_targets.append(targets[sample_idx][t])
        
        # Convert to arrays
        X = np.array(all_states)  # [num_samples, reservoir_size + 1]
        Y = np.array(all_targets)  # [num_samples, output_dim]
        
        # Ridge regression: W = (X^T X + λI)^{-1} X^T Y
        XTX = X.T @ X
        XTY = X.T @ Y
        
        regularization = self.ridge_lambda * np.eye(XTX.shape[0])
        
        try:
            self.readout_weights = np.linalg.solve(XTX + regularization, XTY).T
        except np.linalg.LinAlgError:
            self.logger.warning("Ridge regression failed, using pseudo-inverse")
            self.readout_weights = (np.linalg.pinv(XTX + regularization) @ XTY).T
        
        # Compute training error
        predictions = X @ self.readout_weights.T
        mse = np.mean((predictions - Y)**2)
        rmse = np.sqrt(mse)
        
        self.logger.info(f"Training complete. RMSE: {rmse:.6f}")
        
        return {
            'mse': mse,
            'rmse': rmse,
            'num_samples': len(all_states)
        }
    
    def predict(self, input_signal: np.ndarray, dt: float = 0.01) -> np.ndarray:
        """
        Predict output for given input
        
        Args:
            input_signal: Input signal
            dt: Time step
            
        Returns:
            Output prediction
        """
        self.update_state(input_signal, dt)
        extended_state = self.get_extended_state()
        output = self.readout_weights @ extended_state
        return output
    
    def reset(self):
        """Reset reservoir states to zero"""
        self.states = [np.zeros(size) for size in self.layer_sizes]
        
        # Reset EM fields
        if self.enable_em_coupling:
            for layer in self.layers:
                if layer.em_field is not None:
                    layer.em_field = CognitiveEMField(
                        num_models=3,
                        pole_configuration=PoleConfiguration.FOUR_POLE
                    )
    
    def get_em_field_states(self) -> List[Dict]:
        """
        Get electromagnetic field states for all layers
        
        Returns:
            List of EM field state dictionaries
        """
        em_states = []
        
        for i, layer in enumerate(self.layers):
            if layer.em_field is not None:
                state = {
                    'layer': i,
                    'torque': layer.em_field.machine.state.torque,
                    'rotor_speed': layer.em_field.machine.state.rotor_speed,
                    'slip': layer.em_field.machine.state.slip,
                    'field_strength': layer.em_field.machine.get_field_strength()
                }
                em_states.append(state)
        
        return em_states
    
    def get_layer_statistics(self) -> List[Dict]:
        """
        Get statistics for each layer
        
        Returns:
            List of layer statistics
        """
        stats = []
        
        for i, (layer, state) in enumerate(zip(self.layers, self.states)):
            layer_stats = {
                'layer': i,
                'size': layer.size,
                'mean_activation': np.mean(state),
                'std_activation': np.std(state),
                'max_activation': np.max(np.abs(state)),
                'spectral_radius': layer.spectral_radius,
                'leaking_rate': layer.leaking_rate
            }
            
            # Add EM field stats if available
            if layer.em_field is not None:
                layer_stats.update({
                    'em_torque': layer.em_field.machine.state.torque,
                    'em_slip': layer.em_field.machine.state.slip
                })
            
            stats.append(layer_stats)
        
        return stats
