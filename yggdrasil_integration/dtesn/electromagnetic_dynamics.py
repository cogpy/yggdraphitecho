"""
Electromagnetic Field Dynamics for Cognitive Fusion

This module implements a neural analogical model of electro-magneto-mechanical
energy conversion based on polyphase induction machine principles. The rotor/stator
pole configurations drive motive forces in the cognitive electromagnetic field,
enabling multi-model interaction dynamics.

The analogy maps:
- Stator windings → Input/context models (stationary reference frame)
- Rotor windings → Processing/cognitive models (rotating reference frame)
- Magnetic flux → Information flow and attention
- Torque → Cognitive motive force
- Slip → Model synchronization error
- Polyphase currents → Multi-model ensemble dynamics
"""

import numpy as np
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import logging


class PoleConfiguration(Enum):
    """Pole pair configurations for induction machine"""
    TWO_POLE = 2  # Single pole pair (high speed)
    FOUR_POLE = 4  # Two pole pairs (medium speed)
    SIX_POLE = 6  # Three pole pairs (low speed, high torque)
    EIGHT_POLE = 8  # Four pole pairs (very low speed, very high torque)


class PhaseConfiguration(Enum):
    """Phase configurations for polyphase systems"""
    SINGLE_PHASE = 1  # Single model
    TWO_PHASE = 2  # Dual model system
    THREE_PHASE = 3  # Triple model ensemble (most common)
    SIX_PHASE = 6  # Six model ensemble (high redundancy)


@dataclass
class ElectromagneticState:
    """
    State of the cognitive electromagnetic field
    
    Attributes:
        stator_flux: Stator (input/context) flux linkage
        rotor_flux: Rotor (processing) flux linkage
        stator_current: Stator current (input activation)
        rotor_current: Rotor current (processing activation)
        rotor_speed: Rotor angular velocity (processing rate)
        torque: Electromagnetic torque (cognitive motive force)
        slip: Slip (synchronization error)
    """
    stator_flux: np.ndarray  # [phases, 2] - α-β components
    rotor_flux: np.ndarray  # [phases, 2] - α-β components
    stator_current: np.ndarray  # [phases, 2]
    rotor_current: np.ndarray  # [phases, 2]
    rotor_speed: float  # rad/s
    torque: float  # N⋅m (cognitive units)
    slip: float  # Dimensionless
    
    def __post_init__(self):
        """Validate dimensions"""
        assert self.stator_flux.shape == self.rotor_flux.shape
        assert self.stator_current.shape == self.rotor_current.shape


@dataclass
class InductionMachineParameters:
    """
    Parameters for the polyphase induction machine model
    
    These parameters define the electromagnetic characteristics of the
    cognitive fusion reactor.
    """
    # Winding parameters
    stator_resistance: float = 1.0  # Ω (information resistance)
    rotor_resistance: float = 0.5  # Ω (processing resistance)
    stator_inductance: float = 0.1  # H (self-inductance)
    rotor_inductance: float = 0.1  # H (self-inductance)
    mutual_inductance: float = 0.09  # H (coupling)
    
    # Mechanical parameters
    inertia: float = 0.01  # kg⋅m² (cognitive inertia)
    friction: float = 0.001  # N⋅m⋅s (damping)
    pole_pairs: int = 2  # Number of pole pairs
    
    # Electrical parameters
    rated_voltage: float = 400.0  # V (peak)
    rated_frequency: float = 50.0  # Hz (synchronous frequency)
    rated_power: float = 1000.0  # W (cognitive power)
    
    def __post_init__(self):
        """Calculate derived parameters"""
        self.synchronous_speed = 2 * np.pi * self.rated_frequency / self.pole_pairs
        self.leakage_inductance = self.stator_inductance - self.mutual_inductance


class PolyphaseInductionMachine:
    """
    Polyphase induction machine model for cognitive dynamics
    
    This class implements the electromagnetic field dynamics of a polyphase
    induction machine, serving as an analogical model for multi-model
    cognitive fusion.
    """
    
    def __init__(self,
                 phases: PhaseConfiguration = PhaseConfiguration.THREE_PHASE,
                 poles: PoleConfiguration = PoleConfiguration.FOUR_POLE,
                 parameters: Optional[InductionMachineParameters] = None):
        """
        Initialize polyphase induction machine
        
        Args:
            phases: Number of phases (models in ensemble)
            poles: Pole configuration (determines speed/torque characteristics)
            parameters: Machine parameters
        """
        self.phases = phases.value
        self.pole_pairs = poles.value // 2
        self.params = parameters or InductionMachineParameters(pole_pairs=self.pole_pairs)
        
        self.logger = logging.getLogger(f"{__name__}.PolyphaseInductionMachine")
        
        # Initialize state
        self.state = self._initialize_state()
        
        # Park transformation matrices (for α-β-0 transformation)
        self.clarke_matrix = self._compute_clarke_matrix()
        self.inv_clarke_matrix = np.linalg.pinv(self.clarke_matrix)
        
        self.logger.info(
            f"Initialized {self.phases}-phase induction machine "
            f"with {self.pole_pairs} pole pairs"
        )
    
    def _initialize_state(self) -> ElectromagneticState:
        """Initialize electromagnetic state"""
        return ElectromagneticState(
            stator_flux=np.zeros((self.phases, 2)),
            rotor_flux=np.zeros((self.phases, 2)),
            stator_current=np.zeros((self.phases, 2)),
            rotor_current=np.zeros((self.phases, 2)),
            rotor_speed=0.0,
            torque=0.0,
            slip=1.0  # Initially at standstill
        )
    
    def _compute_clarke_matrix(self) -> np.ndarray:
        """
        Compute Clarke transformation matrix for α-β-0 transformation
        
        Returns:
            Clarke matrix for converting phase quantities to α-β components
        """
        if self.phases == 3:
            # Standard 3-phase Clarke transformation
            return (2/3) * np.array([
                [1, -0.5, -0.5],
                [0, np.sqrt(3)/2, -np.sqrt(3)/2],
                [0.5, 0.5, 0.5]
            ])
        else:
            # Generalized Clarke transformation
            angles = 2 * np.pi * np.arange(self.phases) / self.phases
            return (2/self.phases) * np.vstack([
                np.cos(angles),
                np.sin(angles),
                np.ones(self.phases) / np.sqrt(2)
            ])
    
    def clarke_transform(self, phase_quantities: np.ndarray) -> np.ndarray:
        """
        Apply Clarke transformation to convert phase quantities to α-β-0
        
        Args:
            phase_quantities: Phase quantities [phases]
            
        Returns:
            α-β-0 components [3]
        """
        return self.clarke_matrix @ phase_quantities
    
    def inverse_clarke_transform(self, alpha_beta_zero: np.ndarray) -> np.ndarray:
        """
        Apply inverse Clarke transformation
        
        Args:
            alpha_beta_zero: α-β-0 components [3]
            
        Returns:
            Phase quantities [phases]
        """
        return self.inv_clarke_matrix @ alpha_beta_zero
    
    def park_transform(self, alpha_beta: np.ndarray, theta: float) -> np.ndarray:
        """
        Apply Park transformation to convert α-β to d-q (rotating frame)
        
        Args:
            alpha_beta: α-β components [2]
            theta: Rotor angle (rad)
            
        Returns:
            d-q components [2]
        """
        cos_theta = np.cos(theta)
        sin_theta = np.sin(theta)
        
        park_matrix = np.array([
            [cos_theta, sin_theta],
            [-sin_theta, cos_theta]
        ])
        
        return park_matrix @ alpha_beta
    
    def inverse_park_transform(self, dq: np.ndarray, theta: float) -> np.ndarray:
        """
        Apply inverse Park transformation
        
        Args:
            dq: d-q components [2]
            theta: Rotor angle (rad)
            
        Returns:
            α-β components [2]
        """
        cos_theta = np.cos(theta)
        sin_theta = np.sin(theta)
        
        inv_park_matrix = np.array([
            [cos_theta, -sin_theta],
            [sin_theta, cos_theta]
        ])
        
        return inv_park_matrix @ dq
    
    def compute_torque(self, stator_flux: np.ndarray, rotor_current: np.ndarray) -> float:
        """
        Compute electromagnetic torque
        
        T = (3/2) * p * (ψ_s × i_r)
        
        Args:
            stator_flux: Stator flux α-β components
            rotor_current: Rotor current α-β components
            
        Returns:
            Electromagnetic torque (cognitive motive force)
        """
        # Cross product in 2D: ψ_α * i_β - ψ_β * i_α
        cross_product = stator_flux[0] * rotor_current[1] - stator_flux[1] * rotor_current[0]
        
        torque = (3/2) * self.pole_pairs * cross_product
        
        return torque
    
    def dynamics(self, 
                 t: float,
                 state_vector: np.ndarray,
                 stator_voltage: np.ndarray,
                 load_torque: float = 0.0) -> np.ndarray:
        """
        Compute state derivatives for electromagnetic dynamics
        
        State vector: [ψ_s_α, ψ_s_β, ψ_r_α, ψ_r_β, ω_r]
        
        Args:
            t: Time
            state_vector: Current state
            stator_voltage: Stator voltage α-β components
            load_torque: Load torque (external cognitive load)
            
        Returns:
            State derivatives
        """
        # Unpack state
        psi_s_alpha, psi_s_beta = state_vector[0], state_vector[1]
        psi_r_alpha, psi_r_beta = state_vector[2], state_vector[3]
        omega_r = state_vector[4]
        
        # Compute currents from fluxes (inverse inductance relations)
        L_s = self.params.stator_inductance
        L_r = self.params.rotor_inductance
        L_m = self.params.mutual_inductance
        
        sigma = 1 - (L_m**2) / (L_s * L_r)  # Leakage coefficient
        
        i_s_alpha = (psi_s_alpha / L_s) - (L_m / (L_s * L_r)) * psi_r_alpha
        i_s_beta = (psi_s_beta / L_s) - (L_m / (L_s * L_r)) * psi_r_beta
        
        i_r_alpha = (psi_r_alpha / L_r) - (L_m / (L_s * L_r)) * psi_s_alpha
        i_r_beta = (psi_r_beta / L_r) - (L_m / (L_s * L_r)) * psi_s_beta
        
        # Stator flux dynamics
        dpsi_s_alpha_dt = stator_voltage[0] - self.params.stator_resistance * i_s_alpha
        dpsi_s_beta_dt = stator_voltage[1] - self.params.stator_resistance * i_s_beta
        
        # Rotor flux dynamics (in stationary frame)
        omega_slip = omega_r * self.pole_pairs
        
        dpsi_r_alpha_dt = -self.params.rotor_resistance * i_r_alpha + omega_slip * psi_r_beta
        dpsi_r_beta_dt = -self.params.rotor_resistance * i_r_beta - omega_slip * psi_r_alpha
        
        # Mechanical dynamics
        torque = self.compute_torque(
            np.array([psi_s_alpha, psi_s_beta]),
            np.array([i_r_alpha, i_r_beta])
        )
        
        domega_r_dt = (torque - load_torque - self.params.friction * omega_r) / self.params.inertia
        
        return np.array([
            dpsi_s_alpha_dt,
            dpsi_s_beta_dt,
            dpsi_r_alpha_dt,
            dpsi_r_beta_dt,
            domega_r_dt
        ])
    
    def update(self, 
               stator_voltage: np.ndarray,
               load_torque: float,
               dt: float) -> ElectromagneticState:
        """
        Update electromagnetic state
        
        Args:
            stator_voltage: Stator voltage α-β components (input activation)
            load_torque: Load torque (cognitive load)
            dt: Time step
            
        Returns:
            Updated electromagnetic state
        """
        # Pack current state
        state_vector = np.array([
            self.state.stator_flux[0, 0],  # α component
            self.state.stator_flux[0, 1],  # β component
            self.state.rotor_flux[0, 0],
            self.state.rotor_flux[0, 1],
            self.state.rotor_speed
        ])
        
        # Compute derivatives
        derivatives = self.dynamics(0, state_vector, stator_voltage, load_torque)
        
        # Euler integration (can be replaced with RK4 from butcher_series)
        state_vector += derivatives * dt
        
        # Unpack updated state
        self.state.stator_flux[0, 0] = state_vector[0]
        self.state.stator_flux[0, 1] = state_vector[1]
        self.state.rotor_flux[0, 0] = state_vector[2]
        self.state.rotor_flux[0, 1] = state_vector[3]
        self.state.rotor_speed = state_vector[4]
        
        # Compute torque and slip
        self.state.torque = self.compute_torque(
            self.state.stator_flux[0],
            self.state.rotor_current[0]
        )
        
        omega_sync = 2 * np.pi * self.params.rated_frequency / self.pole_pairs
        self.state.slip = (omega_sync - self.state.rotor_speed) / omega_sync
        
        return self.state
    
    def apply_polyphase_voltage(self, 
                                amplitudes: np.ndarray,
                                frequency: float,
                                t: float) -> np.ndarray:
        """
        Generate polyphase voltage waveforms
        
        Args:
            amplitudes: Voltage amplitudes for each phase
            frequency: Electrical frequency (Hz)
            t: Time
            
        Returns:
            Phase voltages
        """
        phase_angles = 2 * np.pi * np.arange(self.phases) / self.phases
        omega = 2 * np.pi * frequency
        
        voltages = amplitudes * np.cos(omega * t + phase_angles)
        
        return voltages
    
    def get_field_strength(self) -> float:
        """
        Get total electromagnetic field strength (information density)
        
        Returns:
            Field strength (magnitude of flux linkage)
        """
        stator_magnitude = np.linalg.norm(self.state.stator_flux)
        rotor_magnitude = np.linalg.norm(self.state.rotor_flux)
        
        return stator_magnitude + rotor_magnitude
    
    def get_power_flow(self) -> Dict[str, float]:
        """
        Compute power flow in the machine
        
        Returns:
            Dictionary with power components
        """
        # Electrical input power
        p_in = np.sum(self.state.stator_current * self.state.stator_flux) * self.params.rated_frequency
        
        # Copper losses
        p_copper_stator = self.params.stator_resistance * np.sum(self.state.stator_current**2)
        p_copper_rotor = self.params.rotor_resistance * np.sum(self.state.rotor_current**2)
        
        # Mechanical output power
        p_mech = self.state.torque * self.state.rotor_speed
        
        # Friction losses
        p_friction = self.params.friction * self.state.rotor_speed**2
        
        # Efficiency
        efficiency = p_mech / p_in if p_in > 0 else 0
        
        return {
            'input_power': p_in,
            'copper_loss_stator': p_copper_stator,
            'copper_loss_rotor': p_copper_rotor,
            'mechanical_power': p_mech,
            'friction_loss': p_friction,
            'efficiency': efficiency
        }


class CognitiveEMField:
    """
    Cognitive electromagnetic field for multi-model fusion
    
    This class extends the polyphase induction machine model to represent
    cognitive dynamics, where each phase corresponds to a model in the ensemble.
    """
    
    def __init__(self,
                 num_models: int = 3,
                 pole_configuration: PoleConfiguration = PoleConfiguration.FOUR_POLE):
        """
        Initialize cognitive EM field
        
        Args:
            num_models: Number of models in the ensemble
            pole_configuration: Pole configuration
        """
        # Map number of models to phase configuration
        if num_models == 1:
            phase_config = PhaseConfiguration.SINGLE_PHASE
        elif num_models == 2:
            phase_config = PhaseConfiguration.TWO_PHASE
        elif num_models <= 3:
            phase_config = PhaseConfiguration.THREE_PHASE
        else:
            phase_config = PhaseConfiguration.SIX_PHASE
        
        self.machine = PolyphaseInductionMachine(
            phases=phase_config,
            poles=pole_configuration
        )
        
        self.num_models = num_models
        self.logger = logging.getLogger(f"{__name__}.CognitiveEMField")
        
        # Model-specific parameters
        self.model_activations = np.zeros(num_models)
        self.model_weights = np.ones(num_models) / num_models
        
        self.logger.info(f"Initialized cognitive EM field with {num_models} models")
    
    def set_model_activations(self, activations: np.ndarray):
        """
        Set model activation levels (stator voltages)
        
        Args:
            activations: Activation levels for each model
        """
        self.model_activations = np.array(activations)
    
    def compute_cognitive_torque(self) -> float:
        """
        Compute cognitive motive force (torque)
        
        Returns:
            Cognitive torque (drive for information processing)
        """
        return self.machine.state.torque
    
    def get_synchronization_error(self) -> float:
        """
        Get model synchronization error (slip)
        
        Returns:
            Slip (0 = perfect synchronization, 1 = no synchronization)
        """
        return self.machine.state.slip
    
    def update_field(self, 
                     input_activations: np.ndarray,
                     cognitive_load: float,
                     dt: float) -> Dict[str, Any]:
        """
        Update cognitive electromagnetic field
        
        Args:
            input_activations: Input activations for each model
            cognitive_load: External cognitive load
            dt: Time step
            
        Returns:
            Field state dictionary
        """
        # Convert activations to α-β voltage
        stator_voltage = self.machine.clarke_transform(
            np.pad(input_activations, (0, max(0, 3 - len(input_activations))))
        )[:2]
        
        # Update machine state
        state = self.machine.update(stator_voltage, cognitive_load, dt)
        
        return {
            'torque': state.torque,
            'rotor_speed': state.rotor_speed,
            'slip': state.slip,
            'field_strength': self.machine.get_field_strength(),
            'power_flow': self.machine.get_power_flow()
        }
