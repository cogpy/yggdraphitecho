"""
Transformer Architecture Database Schema

This module extends the Arc-Halo database schema to encode LLM transformer
architecture components directly into the computational database. The schema
represents attention mechanisms, layer normalization, MLP blocks, and tensor
operations as first-class database entities.

The key insight: The database is not just storage, but a computational substrate
that encodes the transformer architecture itself, allowing for dynamic
reconfiguration and meta-learning.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Any
from enum import Enum
import numpy as np


class TransformerComponentType(Enum):
    """Types of transformer components"""
    ATTENTION_HEAD = "attention_head"
    MULTI_HEAD_ATTENTION = "multi_head_attention"
    LAYER_NORM = "layer_norm"
    MLP_BLOCK = "mlp_block"
    FEED_FORWARD = "feed_forward"
    EMBEDDING = "embedding"
    POSITIONAL_ENCODING = "positional_encoding"
    RESIDUAL_CONNECTION = "residual_connection"


class ActivationFunction(Enum):
    """Activation functions with armature winding parameters"""
    GELU = "gelu"
    RELU = "relu"
    SWISH = "swish"
    TANH = "tanh"
    SIGMOID = "sigmoid"
    SOFTMAX = "softmax"


@dataclass
class ArmatureWindingConfig:
    """
    Armature winding configuration for activation function modulation
    
    This represents the electromagnetic coupling parameters that control
    activation function behavior through induction machine principles.
    """
    num_windings: int  # Number of armature windings
    winding_resistance: float  # Resistance per winding (Ω)
    winding_inductance: float  # Inductance per winding (H)
    air_gap: float  # Air gap distance (mm)
    coupling_coefficient: float  # Magnetic coupling coefficient (0-1)
    
    # Modulation parameters
    amplitude_modulation: float = 1.0  # Amplitude scaling factor
    phase_shift: float = 0.0  # Phase shift in radians
    impedance_tuning: float = 1.0  # Impedance adjustment factor
    
    def compute_impedance(self, frequency: float) -> complex:
        """
        Compute complex impedance at given frequency
        
        Z = R + jωL
        
        Args:
            frequency: Operating frequency (Hz)
            
        Returns:
            Complex impedance
        """
        omega = 2 * np.pi * frequency
        resistance = self.winding_resistance * self.impedance_tuning
        reactance = omega * self.winding_inductance
        return complex(resistance, reactance)
    
    def modulate_activation(self, x: np.ndarray, frequency: float = 1.0) -> np.ndarray:
        """
        Modulate activation through armature winding parameters
        
        Args:
            x: Input activation
            frequency: Modulation frequency
            
        Returns:
            Modulated activation
        """
        # Compute impedance effect
        Z = self.compute_impedance(frequency)
        impedance_factor = np.abs(Z) / (self.winding_resistance + 1e-8)
        
        # Apply amplitude modulation
        x_modulated = x * self.amplitude_modulation * impedance_factor
        
        # Apply phase shift
        if self.phase_shift != 0:
            # Phase shift implemented as rotation in complex plane
            phase_factor = np.exp(1j * self.phase_shift)
            x_complex = x_modulated.astype(complex) * phase_factor
            x_modulated = np.real(x_complex)
        
        # Apply air gap attenuation
        air_gap_factor = 1.0 / (1.0 + self.air_gap * 0.1)
        x_modulated *= air_gap_factor * self.coupling_coefficient
        
        return x_modulated


@dataclass
class AttentionHeadSchema:
    """Schema for attention head in database"""
    head_id: int
    layer_id: int
    head_dim: int
    
    # Query, Key, Value weight tensors (stored as references)
    query_weights_id: str
    key_weights_id: str
    value_weights_id: str
    output_weights_id: str
    
    # Armature winding configuration for activation modulation
    armature_config: ArmatureWindingConfig
    
    # Attention statistics
    attention_entropy: float = 0.0
    sparsity: float = 0.0
    max_attention_weight: float = 0.0


@dataclass
class MultiHeadAttentionSchema:
    """Schema for multi-head attention in database"""
    mha_id: int
    layer_id: int
    num_heads: int
    model_dim: int
    
    # Attention heads
    heads: List[AttentionHeadSchema]
    
    # Output projection
    output_projection_id: str
    
    # Layer statistics
    total_parameters: int
    flops_per_token: int


@dataclass
class LayerNormSchema:
    """Schema for layer normalization in database"""
    norm_id: int
    layer_id: int
    normalized_shape: tuple
    
    # Parameters
    gamma_id: str  # Scale parameter
    beta_id: str   # Shift parameter
    
    # Normalization statistics
    eps: float = 1e-5
    mean_activation: float = 0.0
    std_activation: float = 1.0


@dataclass
class MLPBlockSchema:
    """Schema for MLP block in database"""
    mlp_id: int
    layer_id: int
    input_dim: int
    hidden_dim: int
    output_dim: int
    
    # Weight tensors
    fc1_weights_id: str
    fc1_bias_id: str
    fc2_weights_id: str
    fc2_bias_id: str
    
    # Activation function with armature winding
    activation_fn: ActivationFunction
    armature_config: ArmatureWindingConfig
    
    # Statistics
    activation_sparsity: float = 0.0
    gradient_norm: float = 0.0


@dataclass
class TransformerLayerSchema:
    """Schema for complete transformer layer"""
    layer_id: int
    layer_type: str  # "encoder" or "decoder"
    
    # Components
    multi_head_attention: MultiHeadAttentionSchema
    layer_norm1: LayerNormSchema
    mlp_block: MLPBlockSchema
    layer_norm2: LayerNormSchema
    
    # Cross-attention (for decoder)
    cross_attention: Optional[MultiHeadAttentionSchema] = None
    layer_norm_cross: Optional[LayerNormSchema] = None
    
    # Residual connections
    residual_scale: float = 1.0
    
    # Layer statistics
    total_parameters: int = 0
    forward_flops: int = 0
    backward_flops: int = 0


@dataclass
class TransformerArchitectureSchema:
    """Complete transformer architecture schema"""
    model_id: str
    model_name: str
    
    # Architecture parameters
    num_layers: int
    model_dim: int
    num_heads: int
    ff_dim: int
    vocab_size: int
    max_seq_length: int
    
    # Layers
    layers: List[TransformerLayerSchema]
    
    # Embeddings
    token_embedding_id: str
    position_embedding_id: str
    
    # Output
    output_projection_id: str
    
    # Global armature configuration
    global_armature_config: ArmatureWindingConfig
    
    # Model statistics
    total_parameters: int = 0
    memory_footprint_mb: float = 0.0
    inference_flops: int = 0


class TransformerDatabaseEncoder:
    """
    Encodes transformer architecture into Arc-Halo database schema
    
    This class provides methods to encode transformer components as database
    entities, enabling the database to serve as a computational substrate.
    """
    
    def __init__(self, db_connection=None):
        """
        Initialize transformer database encoder
        
        Args:
            db_connection: Database connection (optional)
        """
        self.db_connection = db_connection
        self.architectures: Dict[str, TransformerArchitectureSchema] = {}
    
    def create_armature_config(self,
                              num_windings: int = 4,
                              air_gap: float = 1.0,
                              amplitude_mod: float = 1.0,
                              phase_shift: float = 0.0) -> ArmatureWindingConfig:
        """
        Create armature winding configuration
        
        Args:
            num_windings: Number of windings
            air_gap: Air gap distance
            amplitude_mod: Amplitude modulation factor
            phase_shift: Phase shift in radians
            
        Returns:
            Armature winding configuration
        """
        return ArmatureWindingConfig(
            num_windings=num_windings,
            winding_resistance=0.1 * num_windings,
            winding_inductance=0.01 * num_windings,
            air_gap=air_gap,
            coupling_coefficient=0.95,
            amplitude_modulation=amplitude_mod,
            phase_shift=phase_shift,
            impedance_tuning=1.0
        )
    
    def encode_attention_head(self,
                             head_id: int,
                             layer_id: int,
                             head_dim: int,
                             armature_config: ArmatureWindingConfig) -> AttentionHeadSchema:
        """
        Encode attention head into database schema
        
        Args:
            head_id: Head identifier
            layer_id: Layer identifier
            head_dim: Head dimension
            armature_config: Armature winding configuration
            
        Returns:
            Attention head schema
        """
        return AttentionHeadSchema(
            head_id=head_id,
            layer_id=layer_id,
            head_dim=head_dim,
            query_weights_id=f"attn_l{layer_id}_h{head_id}_q",
            key_weights_id=f"attn_l{layer_id}_h{head_id}_k",
            value_weights_id=f"attn_l{layer_id}_h{head_id}_v",
            output_weights_id=f"attn_l{layer_id}_h{head_id}_o",
            armature_config=armature_config
        )
    
    def encode_mlp_block(self,
                        mlp_id: int,
                        layer_id: int,
                        input_dim: int,
                        hidden_dim: int,
                        activation_fn: ActivationFunction,
                        armature_config: ArmatureWindingConfig) -> MLPBlockSchema:
        """
        Encode MLP block into database schema
        
        Args:
            mlp_id: MLP identifier
            layer_id: Layer identifier
            input_dim: Input dimension
            hidden_dim: Hidden dimension
            activation_fn: Activation function
            armature_config: Armature winding configuration
            
        Returns:
            MLP block schema
        """
        return MLPBlockSchema(
            mlp_id=mlp_id,
            layer_id=layer_id,
            input_dim=input_dim,
            hidden_dim=hidden_dim,
            output_dim=input_dim,
            fc1_weights_id=f"mlp_l{layer_id}_fc1_w",
            fc1_bias_id=f"mlp_l{layer_id}_fc1_b",
            fc2_weights_id=f"mlp_l{layer_id}_fc2_w",
            fc2_bias_id=f"mlp_l{layer_id}_fc2_b",
            activation_fn=activation_fn,
            armature_config=armature_config
        )
    
    def encode_transformer_layer(self,
                                layer_id: int,
                                model_dim: int,
                                num_heads: int,
                                ff_dim: int,
                                layer_type: str = "encoder") -> TransformerLayerSchema:
        """
        Encode complete transformer layer
        
        Args:
            layer_id: Layer identifier
            model_dim: Model dimension
            num_heads: Number of attention heads
            ff_dim: Feed-forward dimension
            layer_type: "encoder" or "decoder"
            
        Returns:
            Transformer layer schema
        """
        head_dim = model_dim // num_heads
        
        # Create attention heads with varying armature configs
        heads = []
        for h in range(num_heads):
            # Vary air gap and phase shift across heads
            air_gap = 0.5 + h * 0.1
            phase_shift = h * np.pi / num_heads
            
            armature_config = self.create_armature_config(
                num_windings=4,
                air_gap=air_gap,
                phase_shift=phase_shift
            )
            
            head = self.encode_attention_head(h, layer_id, head_dim, armature_config)
            heads.append(head)
        
        # Multi-head attention
        mha = MultiHeadAttentionSchema(
            mha_id=layer_id,
            layer_id=layer_id,
            num_heads=num_heads,
            model_dim=model_dim,
            heads=heads,
            output_projection_id=f"mha_l{layer_id}_out",
            total_parameters=4 * model_dim * model_dim,
            flops_per_token=4 * model_dim * model_dim
        )
        
        # Layer norms
        norm1 = LayerNormSchema(
            norm_id=layer_id * 2,
            layer_id=layer_id,
            normalized_shape=(model_dim,),
            gamma_id=f"ln1_l{layer_id}_gamma",
            beta_id=f"ln1_l{layer_id}_beta"
        )
        
        norm2 = LayerNormSchema(
            norm_id=layer_id * 2 + 1,
            layer_id=layer_id,
            normalized_shape=(model_dim,),
            gamma_id=f"ln2_l{layer_id}_gamma",
            beta_id=f"ln2_l{layer_id}_beta"
        )
        
        # MLP block with GELU activation
        mlp_armature = self.create_armature_config(
            num_windings=6,
            air_gap=1.0,
            amplitude_mod=1.0
        )
        
        mlp = self.encode_mlp_block(
            mlp_id=layer_id,
            layer_id=layer_id,
            input_dim=model_dim,
            hidden_dim=ff_dim,
            activation_fn=ActivationFunction.GELU,
            armature_config=mlp_armature
        )
        
        return TransformerLayerSchema(
            layer_id=layer_id,
            layer_type=layer_type,
            multi_head_attention=mha,
            layer_norm1=norm1,
            mlp_block=mlp,
            layer_norm2=norm2,
            total_parameters=4 * model_dim * model_dim + 2 * model_dim * ff_dim
        )
    
    def encode_transformer_architecture(self,
                                       model_name: str,
                                       num_layers: int,
                                       model_dim: int,
                                       num_heads: int,
                                       ff_dim: int,
                                       vocab_size: int,
                                       max_seq_length: int) -> TransformerArchitectureSchema:
        """
        Encode complete transformer architecture
        
        Args:
            model_name: Model name
            num_layers: Number of layers
            model_dim: Model dimension
            num_heads: Number of attention heads
            ff_dim: Feed-forward dimension
            vocab_size: Vocabulary size
            max_seq_length: Maximum sequence length
            
        Returns:
            Complete transformer architecture schema
        """
        model_id = f"transformer_{model_name}"
        
        # Encode all layers
        layers = []
        for layer_id in range(num_layers):
            layer = self.encode_transformer_layer(
                layer_id, model_dim, num_heads, ff_dim
            )
            layers.append(layer)
        
        # Global armature configuration
        global_armature = self.create_armature_config(
            num_windings=8,
            air_gap=0.5,
            amplitude_mod=1.0
        )
        
        # Calculate total parameters
        total_params = (
            vocab_size * model_dim +  # Token embeddings
            max_seq_length * model_dim +  # Position embeddings
            sum(layer.total_parameters for layer in layers) +
            model_dim * vocab_size  # Output projection
        )
        
        architecture = TransformerArchitectureSchema(
            model_id=model_id,
            model_name=model_name,
            num_layers=num_layers,
            model_dim=model_dim,
            num_heads=num_heads,
            ff_dim=ff_dim,
            vocab_size=vocab_size,
            max_seq_length=max_seq_length,
            layers=layers,
            token_embedding_id=f"{model_id}_token_emb",
            position_embedding_id=f"{model_id}_pos_emb",
            output_projection_id=f"{model_id}_output",
            global_armature_config=global_armature,
            total_parameters=total_params,
            memory_footprint_mb=total_params * 4 / (1024 * 1024)  # FP32
        )
        
        self.architectures[model_id] = architecture
        return architecture
    
    def get_sql_schema(self) -> str:
        """
        Generate SQL schema for transformer architecture tables
        
        Returns:
            SQL CREATE TABLE statements
        """
        return """
-- Transformer Architecture Tables

CREATE TABLE IF NOT EXISTS transformer_models (
    model_id VARCHAR(255) PRIMARY KEY,
    model_name VARCHAR(255) NOT NULL,
    num_layers INTEGER NOT NULL,
    model_dim INTEGER NOT NULL,
    num_heads INTEGER NOT NULL,
    ff_dim INTEGER NOT NULL,
    vocab_size INTEGER NOT NULL,
    max_seq_length INTEGER NOT NULL,
    total_parameters BIGINT,
    memory_footprint_mb FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS transformer_layers (
    layer_id INTEGER PRIMARY KEY,
    model_id VARCHAR(255) REFERENCES transformer_models(model_id),
    layer_type VARCHAR(50),
    total_parameters INTEGER,
    forward_flops BIGINT,
    residual_scale FLOAT DEFAULT 1.0
);

CREATE TABLE IF NOT EXISTS attention_heads (
    head_id INTEGER,
    layer_id INTEGER REFERENCES transformer_layers(layer_id),
    head_dim INTEGER,
    query_weights_id VARCHAR(255),
    key_weights_id VARCHAR(255),
    value_weights_id VARCHAR(255),
    output_weights_id VARCHAR(255),
    attention_entropy FLOAT DEFAULT 0.0,
    sparsity FLOAT DEFAULT 0.0,
    PRIMARY KEY (layer_id, head_id)
);

CREATE TABLE IF NOT EXISTS armature_windings (
    component_id VARCHAR(255) PRIMARY KEY,
    component_type VARCHAR(50),
    num_windings INTEGER,
    winding_resistance FLOAT,
    winding_inductance FLOAT,
    air_gap FLOAT,
    coupling_coefficient FLOAT,
    amplitude_modulation FLOAT DEFAULT 1.0,
    phase_shift FLOAT DEFAULT 0.0,
    impedance_tuning FLOAT DEFAULT 1.0
);

CREATE TABLE IF NOT EXISTS mlp_blocks (
    mlp_id INTEGER PRIMARY KEY,
    layer_id INTEGER REFERENCES transformer_layers(layer_id),
    input_dim INTEGER,
    hidden_dim INTEGER,
    output_dim INTEGER,
    activation_fn VARCHAR(50),
    activation_sparsity FLOAT DEFAULT 0.0,
    gradient_norm FLOAT DEFAULT 0.0
);

CREATE TABLE IF NOT EXISTS layer_norms (
    norm_id INTEGER PRIMARY KEY,
    layer_id INTEGER REFERENCES transformer_layers(layer_id),
    normalized_shape VARCHAR(100),
    gamma_id VARCHAR(255),
    beta_id VARCHAR(255),
    eps FLOAT DEFAULT 1e-5,
    mean_activation FLOAT DEFAULT 0.0,
    std_activation FLOAT DEFAULT 1.0
);
"""
