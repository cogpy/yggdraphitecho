"""
Aphrodite Induction Engine

This module implements the Aphrodite inference engine as a polyphase induction
machine, where activation functions are modulated through armature winding
parameters. This allows continuous fine-tuning of the inference dynamics by
adjusting coupling air gap, winding numbers, amplitude, and phase impedance.

The key insight: The inference engine itself is an electromagnetic system where
activation functions can be dynamically tuned through induction machine principles.
"""

import numpy as np
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass
from enum import Enum
import logging

from .aphrodite_bridge import AphroditeBridge, ReasoningMode
from ..transformer.transformer_schema import (
    ArmatureWindingConfig, ActivationFunction, TransformerDatabaseEncoder
)
from ..dtesn.electromagnetic_dynamics import (
    CognitiveEMField, PoleConfiguration, ElectromagneticState
)


class InductionMode(Enum):
    """Induction machine operating modes"""
    MOTORING = "motoring"  # Normal inference (positive torque)
    GENERATING = "generating"  # Backpropagation (negative torque)
    BRAKING = "braking"  # Regularization (dissipative)
    SYNCHRONOUS = "synchronous"  # Zero slip (perfect alignment)


@dataclass
class InferenceState:
    """State of the inference induction machine"""
    mode: InductionMode
    rotor_speed: float  # Inference rate (tokens/sec)
    slip: float  # Synchronization error
    torque: float  # Computational force
    power_factor: float  # Efficiency metric
    stator_current: np.ndarray  # Input activations
    rotor_current: np.ndarray  # Output activations
    field_strength: float  # Attention strength


class AphroditeInductionEngine(AphroditeBridge):
    """
    Enhanced Aphrodite bridge with induction machine dynamics
    
    This class extends the base Aphrodite bridge to model the inference
    engine as a polyphase induction machine, enabling dynamic tuning of
    activation functions through armature winding modulation.
    """
    
    def __init__(self, reservoir, transformer_encoder: Optional[TransformerDatabaseEncoder] = None):
        """
        Initialize Aphrodite induction engine
        
        Args:
            reservoir: Membrane reservoir
            transformer_encoder: Transformer database encoder (optional)
        """
        super().__init__(reservoir)
        
        self.logger = logging.getLogger(f"{__name__}.AphroditeInductionEngine")
        
        # Transformer encoder for architecture access
        self.transformer_encoder = transformer_encoder or TransformerDatabaseEncoder()
        
        # Induction machine components
        self.em_field = CognitiveEMField(
            num_models=3,
            pole_configuration=PoleConfiguration.FOUR_POLE
        )
        
        # Armature winding configurations for different activation functions
        self.armature_configs: Dict[ActivationFunction, ArmatureWindingConfig] = {}
        self._initialize_armature_configs()
        
        # Current inference state
        self.inference_state: Optional[InferenceState] = None
        
        # Activation function registry with induction modulation
        self.activation_functions: Dict[ActivationFunction, Callable] = {
            ActivationFunction.GELU: self._gelu_modulated,
            ActivationFunction.RELU: self._relu_modulated,
            ActivationFunction.SWISH: self._swish_modulated,
            ActivationFunction.TANH: self._tanh_modulated,
            ActivationFunction.SIGMOID: self._sigmoid_modulated,
            ActivationFunction.SOFTMAX: self._softmax_modulated
        }
        
        self.logger.info("Initialized Aphrodite Induction Engine")
    
    def _initialize_armature_configs(self):
        """Initialize armature winding configurations for activation functions"""
        
        # GELU: High winding count, moderate air gap
        self.armature_configs[ActivationFunction.GELU] = ArmatureWindingConfig(
            num_windings=8,
            winding_resistance=0.8,
            winding_inductance=0.08,
            air_gap=1.0,
            coupling_coefficient=0.95,
            amplitude_modulation=1.0,
            phase_shift=0.0,
            impedance_tuning=1.0
        )
        
        # ReLU: Low winding count, large air gap (sharp cutoff)
        self.armature_configs[ActivationFunction.RELU] = ArmatureWindingConfig(
            num_windings=2,
            winding_resistance=0.2,
            winding_inductance=0.02,
            air_gap=2.0,
            coupling_coefficient=0.85,
            amplitude_modulation=1.0,
            phase_shift=0.0,
            impedance_tuning=1.0
        )
        
        # Swish: Medium winding count, small air gap (smooth)
        self.armature_configs[ActivationFunction.SWISH] = ArmatureWindingConfig(
            num_windings=6,
            winding_resistance=0.6,
            winding_inductance=0.06,
            air_gap=0.5,
            coupling_coefficient=0.98,
            amplitude_modulation=1.0,
            phase_shift=0.0,
            impedance_tuning=1.0
        )
        
        # Tanh: Medium winding count, moderate air gap
        self.armature_configs[ActivationFunction.TANH] = ArmatureWindingConfig(
            num_windings=4,
            winding_resistance=0.4,
            winding_inductance=0.04,
            air_gap=1.0,
            coupling_coefficient=0.90,
            amplitude_modulation=1.0,
            phase_shift=0.0,
            impedance_tuning=1.0
        )
        
        # Sigmoid: Similar to tanh but with phase shift
        self.armature_configs[ActivationFunction.SIGMOID] = ArmatureWindingConfig(
            num_windings=4,
            winding_resistance=0.4,
            winding_inductance=0.04,
            air_gap=1.0,
            coupling_coefficient=0.90,
            amplitude_modulation=1.0,
            phase_shift=np.pi / 4,
            impedance_tuning=1.0
        )
        
        # Softmax: High winding count, small air gap (strong coupling)
        self.armature_configs[ActivationFunction.SOFTMAX] = ArmatureWindingConfig(
            num_windings=10,
            winding_resistance=1.0,
            winding_inductance=0.10,
            air_gap=0.3,
            coupling_coefficient=0.99,
            amplitude_modulation=1.0,
            phase_shift=0.0,
            impedance_tuning=1.0
        )
    
    def tune_armature(self,
                     activation_fn: ActivationFunction,
                     air_gap: Optional[float] = None,
                     amplitude_mod: Optional[float] = None,
                     phase_shift: Optional[float] = None,
                     impedance_tuning: Optional[float] = None):
        """
        Tune armature winding parameters for an activation function
        
        This allows dynamic adjustment of activation function behavior
        through electromagnetic coupling parameters.
        
        Args:
            activation_fn: Activation function to tune
            air_gap: New air gap distance (mm)
            amplitude_mod: New amplitude modulation factor
            phase_shift: New phase shift (radians)
            impedance_tuning: New impedance tuning factor
        """
        config = self.armature_configs[activation_fn]
        
        if air_gap is not None:
            config.air_gap = air_gap
            self.logger.info(f"Tuned {activation_fn.value} air gap to {air_gap:.3f} mm")
        
        if amplitude_mod is not None:
            config.amplitude_modulation = amplitude_mod
            self.logger.info(f"Tuned {activation_fn.value} amplitude to {amplitude_mod:.3f}")
        
        if phase_shift is not None:
            config.phase_shift = phase_shift
            self.logger.info(f"Tuned {activation_fn.value} phase shift to {phase_shift:.3f} rad")
        
        if impedance_tuning is not None:
            config.impedance_tuning = impedance_tuning
            self.logger.info(f"Tuned {activation_fn.value} impedance to {impedance_tuning:.3f}")
    
    def _gelu_modulated(self, x: np.ndarray, frequency: float = 1.0) -> np.ndarray:
        """GELU activation with armature winding modulation"""
        config = self.armature_configs[ActivationFunction.GELU]
        
        # Standard GELU
        gelu = 0.5 * x * (1 + np.tanh(np.sqrt(2 / np.pi) * (x + 0.044715 * x**3)))
        
        # Apply armature modulation
        return config.modulate_activation(gelu, frequency)
    
    def _relu_modulated(self, x: np.ndarray, frequency: float = 1.0) -> np.ndarray:
        """ReLU activation with armature winding modulation"""
        config = self.armature_configs[ActivationFunction.RELU]
        
        # Standard ReLU
        relu = np.maximum(0, x)
        
        # Apply armature modulation
        return config.modulate_activation(relu, frequency)
    
    def _swish_modulated(self, x: np.ndarray, frequency: float = 1.0) -> np.ndarray:
        """Swish activation with armature winding modulation"""
        config = self.armature_configs[ActivationFunction.SWISH]
        
        # Standard Swish (SiLU)
        swish = x / (1 + np.exp(-x))
        
        # Apply armature modulation
        return config.modulate_activation(swish, frequency)
    
    def _tanh_modulated(self, x: np.ndarray, frequency: float = 1.0) -> np.ndarray:
        """Tanh activation with armature winding modulation"""
        config = self.armature_configs[ActivationFunction.TANH]
        
        # Standard tanh
        tanh = np.tanh(x)
        
        # Apply armature modulation
        return config.modulate_activation(tanh, frequency)
    
    def _sigmoid_modulated(self, x: np.ndarray, frequency: float = 1.0) -> np.ndarray:
        """Sigmoid activation with armature winding modulation"""
        config = self.armature_configs[ActivationFunction.SIGMOID]
        
        # Standard sigmoid
        sigmoid = 1 / (1 + np.exp(-x))
        
        # Apply armature modulation
        return config.modulate_activation(sigmoid, frequency)
    
    def _softmax_modulated(self, x: np.ndarray, frequency: float = 1.0) -> np.ndarray:
        """Softmax activation with armature winding modulation"""
        config = self.armature_configs[ActivationFunction.SOFTMAX]
        
        # Standard softmax with numerical stability
        if x.ndim == 1:
            x_shifted = x - np.max(x)
            exp_x = np.exp(x_shifted)
            softmax = exp_x / np.sum(exp_x)
        else:
            x_shifted = x - np.max(x, axis=-1, keepdims=True)
            exp_x = np.exp(x_shifted)
            softmax = exp_x / np.sum(exp_x, axis=-1, keepdims=True)
        
        # Apply armature modulation
        return config.modulate_activation(softmax, frequency)
    
    def infer_with_induction(self,
                            input_activations: np.ndarray,
                            activation_fn: ActivationFunction = ActivationFunction.GELU,
                            target_speed: float = 1.0,
                            mode: InductionMode = InductionMode.MOTORING) -> Dict[str, Any]:
        """
        Perform inference using induction machine dynamics
        
        Args:
            input_activations: Input activation tensor
            activation_fn: Activation function to use
            target_speed: Target inference speed (relative)
            mode: Induction machine mode
            
        Returns:
            Dictionary with inference results and EM state
        """
        # Update EM field with input activations
        cognitive_load = np.linalg.norm(input_activations) * 0.1
        
        em_state = self.em_field.update_field(
            input_activations=input_activations,
            cognitive_load=cognitive_load,
            dt=0.01
        )
        
        # Apply activation function with modulation
        frequency = em_state['rotor_speed'] / (2 * np.pi)  # Convert to Hz
        output_activations = self.activation_functions[activation_fn](
            input_activations, frequency
        )
        
        # Compute inference state
        slip = (target_speed - em_state['rotor_speed']) / target_speed if target_speed > 0 else 0
        
        self.inference_state = InferenceState(
            mode=mode,
            rotor_speed=em_state['rotor_speed'],
            slip=slip,
            torque=em_state['torque'],
            power_factor=em_state['power_flow']['efficiency'],
            stator_current=input_activations,
            rotor_current=output_activations,
            field_strength=em_state['field_strength']
        )
        
        return {
            'output': output_activations,
            'inference_state': self.inference_state,
            'em_state': em_state,
            'activation_fn': activation_fn.value
        }
    
    def adaptive_tuning(self, target_metric: str = 'efficiency', target_value: float = 0.9):
        """
        Adaptively tune armature windings to achieve target metric
        
        Args:
            target_metric: Metric to optimize ('efficiency', 'speed', 'torque')
            target_value: Target value for the metric
        """
        if not self.inference_state:
            self.logger.warning("No inference state available for adaptive tuning")
            return
        
        current_value = {
            'efficiency': self.inference_state.power_factor,
            'speed': self.inference_state.rotor_speed,
            'torque': abs(self.inference_state.torque)
        }.get(target_metric, 0)
        
        error = target_value - current_value
        
        # Simple proportional tuning
        if abs(error) > 0.1:
            # Adjust air gap inversely with error
            for activation_fn, config in self.armature_configs.items():
                config.air_gap *= (1 - 0.1 * np.sign(error))
                config.air_gap = np.clip(config.air_gap, 0.1, 5.0)
            
            self.logger.info(
                f"Adaptive tuning: {target_metric} error = {error:.3f}, "
                f"adjusted air gaps"
            )
    
    def get_armature_statistics(self) -> Dict[str, Dict[str, float]]:
        """
        Get statistics for all armature configurations
        
        Returns:
            Dictionary of armature statistics by activation function
        """
        stats = {}
        
        for activation_fn, config in self.armature_configs.items():
            impedance = config.compute_impedance(1.0)  # At 1 Hz
            
            stats[activation_fn.value] = {
                'num_windings': config.num_windings,
                'air_gap': config.air_gap,
                'coupling_coefficient': config.coupling_coefficient,
                'amplitude_modulation': config.amplitude_modulation,
                'phase_shift': config.phase_shift,
                'impedance_magnitude': abs(impedance),
                'impedance_phase': np.angle(impedance),
                'impedance_tuning': config.impedance_tuning
            }
        
        return stats
    
    def visualize_activation_modulation(self,
                                       activation_fn: ActivationFunction,
                                       x_range: tuple = (-5, 5),
                                       num_points: int = 1000) -> Dict[str, np.ndarray]:
        """
        Generate data for visualizing activation function modulation
        
        Args:
            activation_fn: Activation function to visualize
            x_range: Input range
            num_points: Number of points
            
        Returns:
            Dictionary with x values and modulated/unmodulated outputs
        """
        x = np.linspace(x_range[0], x_range[1], num_points)
        
        # Get modulated activation
        y_modulated = self.activation_functions[activation_fn](x, frequency=1.0)
        
        # Get unmodulated activation (temporarily set modulation to identity)
        config = self.armature_configs[activation_fn]
        original_amp = config.amplitude_modulation
        original_phase = config.phase_shift
        original_gap = config.air_gap
        
        config.amplitude_modulation = 1.0
        config.phase_shift = 0.0
        config.air_gap = 0.0
        
        y_unmodulated = self.activation_functions[activation_fn](x, frequency=1.0)
        
        # Restore original config
        config.amplitude_modulation = original_amp
        config.phase_shift = original_phase
        config.air_gap = original_gap
        
        return {
            'x': x,
            'y_modulated': y_modulated,
            'y_unmodulated': y_unmodulated,
            'difference': y_modulated - y_unmodulated
        }
