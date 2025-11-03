"""
Tests for Autogenetic Triadic Correspondence System
"""

import pytest
import numpy as np

from yggdrasil_integration.transformer.transformer_schema import (
    TransformerDatabaseEncoder, ActivationFunction, ArmatureWindingConfig
)
from yggdrasil_integration.bridge.aphrodite_induction_engine import (
    AphroditeInductionEngine, InductionMode
)
from yggdrasil_integration.membranes.agentic_decision_forest import (
    AgenticDecisionForest, AgencyLevel, DecisionType, DecisionContext
)
from yggdrasil_integration.membranes.yggdrasil_membrane import (
    YggdrasilMembrane, MembraneType, MembraneReservoir
)
from yggdrasil_integration.triadic.a000081_correspondence import (
    A000081TriadicSystem, TriadicDomain, A000081
)
from yggdrasil_integration.triadic.autogenesis_engine import (
    AutogenesisEngine, AutogenesisMode, ModificationType
)


# Transformer Schema Tests

def test_armature_winding_config():
    """Test armature winding configuration"""
    config = ArmatureWindingConfig(
        num_windings=4,
        winding_resistance=0.4,
        winding_inductance=0.04,
        air_gap=1.0,
        coupling_coefficient=0.95
    )
    
    # Test impedance computation
    Z = config.compute_impedance(frequency=1.0)
    assert isinstance(Z, complex)
    assert Z.real > 0  # Resistance
    assert Z.imag >= 0  # Inductive reactance


def test_armature_modulation():
    """Test activation modulation through armature"""
    config = ArmatureWindingConfig(
        num_windings=4,
        winding_resistance=0.4,
        winding_inductance=0.04,
        air_gap=1.0,
        coupling_coefficient=0.95,
        amplitude_modulation=1.5,
        phase_shift=np.pi / 4
    )
    
    x = np.array([1.0, 2.0, 3.0])
    x_modulated = config.modulate_activation(x, frequency=1.0)
    
    assert x_modulated.shape == x.shape
    # Modulation should change values
    assert not np.allclose(x, x_modulated)


def test_transformer_encoder():
    """Test transformer database encoder"""
    encoder = TransformerDatabaseEncoder()
    
    # Create simple transformer
    architecture = encoder.encode_transformer_architecture(
        model_name="test_model",
        num_layers=2,
        model_dim=64,
        num_heads=4,
        ff_dim=256,
        vocab_size=1000,
        max_seq_length=128
    )
    
    assert architecture.num_layers == 2
    assert len(architecture.layers) == 2
    assert architecture.model_dim == 64


# Aphrodite Induction Engine Tests

def test_aphrodite_induction_engine():
    """Test Aphrodite induction engine initialization"""
    reservoir = MembraneReservoir(name="test_reservoir")
    engine = AphroditeInductionEngine(reservoir)
    
    assert engine is not None
    assert len(engine.armature_configs) == 6  # 6 activation functions


def test_armature_tuning():
    """Test armature tuning"""
    reservoir = MembraneReservoir(name="test_reservoir")
    engine = AphroditeInductionEngine(reservoir)
    
    # Tune GELU activation
    engine.tune_armature(
        ActivationFunction.GELU,
        air_gap=0.5,
        amplitude_mod=1.2
    )
    
    config = engine.armature_configs[ActivationFunction.GELU]
    assert config.air_gap == 0.5
    assert config.amplitude_modulation == 1.2


def test_infer_with_induction():
    """Test inference with induction machine dynamics"""
    reservoir = MembraneReservoir(name="test_reservoir")
    engine = AphroditeInductionEngine(reservoir)
    
    # Perform inference
    input_activations = np.random.randn(3)
    result = engine.infer_with_induction(
        input_activations,
        activation_fn=ActivationFunction.GELU,
        mode=InductionMode.MOTORING
    )
    
    assert 'output' in result
    assert 'inference_state' in result
    assert 'em_state' in result
    assert result['output'].shape == input_activations.shape


def test_modulated_activations():
    """Test all modulated activation functions"""
    reservoir = MembraneReservoir(name="test_reservoir")
    engine = AphroditeInductionEngine(reservoir)
    
    # Use 3-phase input for EM field compatibility
    x = np.array([-1.0, 0.0, 1.0])
    
    for activation_fn in ActivationFunction:
        result = engine.infer_with_induction(
            x,
            activation_fn=activation_fn
        )
        
        assert result['output'].shape == x.shape


# Agentic Decision Forest Tests

def test_agentic_decision_forest():
    """Test agentic decision forest initialization"""
    membrane = YggdrasilMembrane(
        name="test_membrane",
        membrane_type=MembraneType.COGNITIVE
    )
    
    forest = AgenticDecisionForest(
        membrane,
        agency_level=AgencyLevel.DELIBERATIVE
    )
    
    assert forest.agency_level == AgencyLevel.DELIBERATIVE
    assert forest.total_decisions == 0


def test_make_decision():
    """Test decision making"""
    membrane = YggdrasilMembrane(
        name="test_membrane",
        membrane_type=MembraneType.COGNITIVE
    )
    
    forest = AgenticDecisionForest(membrane)
    
    # Create decision context
    context = DecisionContext(
        decision_type=DecisionType.ROUTE_MESSAGE,
        current_state={'queue_size': 5},
        available_actions=['membrane_a', 'membrane_b', 'membrane_c']
    )
    
    # Make decision
    outcome = forest.make_decision(context)
    
    assert outcome.chosen_action in context.available_actions
    assert 0 <= outcome.confidence <= 1.0
    assert forest.total_decisions == 1


def test_learn_from_outcome():
    """Test learning from decision outcomes"""
    membrane = YggdrasilMembrane(
        name="test_membrane",
        membrane_type=MembraneType.COGNITIVE
    )
    
    forest = AgenticDecisionForest(membrane)
    
    context = DecisionContext(
        decision_type=DecisionType.ALLOCATE_ATTENTION,
        current_state={},
        available_actions=['action_a', 'action_b']
    )
    
    outcome = forest.make_decision(context)
    
    # Learn from outcome
    forest.learn_from_outcome(context, outcome, reward=0.8)
    
    assert len(forest.training_data[DecisionType.ALLOCATE_ATTENTION]) == 1


def test_agency_elevation():
    """Test agency level elevation"""
    membrane = YggdrasilMembrane(
        name="test_membrane",
        membrane_type=MembraneType.COGNITIVE
    )
    
    forest = AgenticDecisionForest(
        membrane,
        agency_level=AgencyLevel.REACTIVE
    )
    
    # Elevate agency
    forest.elevate_agency()
    
    assert forest.agency_level == AgencyLevel.DELIBERATIVE


# A000081 Triadic Correspondence Tests

def test_a000081_triadic_system():
    """Test A000081 triadic system initialization"""
    system = A000081TriadicSystem(max_order=5)
    
    assert system.max_order == 5
    assert len(system.correspondence.elements) == 5


def test_enumeration_verification():
    """Test that enumeration matches A000081"""
    system = A000081TriadicSystem(max_order=10)
    
    verification = system.verify_enumeration()
    
    # Check first few orders (Butcher series only generates up to order 4 by default)
    for order in range(1, 5):
        assert verification[order], f"Order {order} enumeration mismatch"


def test_triadic_element_retrieval():
    """Test retrieving triadic elements"""
    system = A000081TriadicSystem(max_order=5)
    
    # Get element at order 3, index 0
    element = system.get_element(3, 0)
    
    assert element is not None
    assert element.order == 3
    assert element.index == 0
    assert element.butcher_tree is not None


def test_domain_translation():
    """Test translation between domains"""
    system = A000081TriadicSystem(max_order=5)
    
    # Get a B-Series representation
    element = system.get_element(2, 0)
    b_series_repr = element.butcher_tree.structure
    
    # Translate to P-System
    p_system_repr = system.translate_between_domains(
        TriadicDomain.B_SERIES,
        TriadicDomain.P_SYSTEM,
        b_series_repr
    )
    
    assert p_system_repr is not None
    assert p_system_repr == element.membrane_structure


def test_code_generation():
    """Test autogenetic code generation"""
    system = A000081TriadicSystem(max_order=5)
    
    # Generate code for order 3, index 0
    code = system.generate_autogenetic_code(3, 0)
    
    assert 'b_series' in code
    assert 'p_system' in code
    assert 'j_surface' in code
    assert len(code['b_series']) > 0


# Autogenesis Engine Tests

def test_autogenesis_engine():
    """Test autogenesis engine initialization"""
    triadic_system = A000081TriadicSystem(max_order=8)
    engine = AutogenesisEngine(
        triadic_system,
        initial_order=4,
        mode=AutogenesisMode.EXPLORATORY
    )
    
    assert engine.state.current_order == 4
    assert engine.state.generation == 0
    assert engine.mode == AutogenesisMode.EXPLORATORY


def test_propose_modification():
    """Test modification proposal"""
    triadic_system = A000081TriadicSystem(max_order=8)
    engine = AutogenesisEngine(triadic_system, initial_order=4)
    
    # Propose modification
    modification = engine.propose_modification(ModificationType.TRIADIC)
    
    assert modification is not None
    assert modification.modification_type == ModificationType.TRIADIC
    assert modification.source_order == 4


def test_execute_modification():
    """Test modification execution"""
    triadic_system = A000081TriadicSystem(max_order=8)
    engine = AutogenesisEngine(triadic_system, initial_order=4)
    
    # Propose and execute
    modification = engine.propose_modification(ModificationType.TEMPORAL)
    success = engine.execute_modification(modification)
    
    assert modification.executed
    assert engine.state.total_modifications == 1


def test_autogenetic_cycle():
    """Test autogenetic cycle"""
    triadic_system = A000081TriadicSystem(max_order=8)
    engine = AutogenesisEngine(triadic_system, initial_order=4)
    
    # Run one cycle
    modifications = engine.autogenetic_cycle(num_modifications=3)
    
    assert len(modifications) == 3
    assert engine.state.total_modifications == 3


def test_autogenetic_evolution():
    """Test multi-generation evolution"""
    triadic_system = A000081TriadicSystem(max_order=8)
    engine = AutogenesisEngine(
        triadic_system,
        initial_order=4,
        mode=AutogenesisMode.CONSERVATIVE
    )
    
    # Evolve for 5 generations
    engine.evolve(generations=5, modifications_per_generation=2)
    
    assert engine.state.generation >= 1
    assert engine.state.total_modifications == 10


def test_autogenesis_statistics():
    """Test autogenesis statistics"""
    triadic_system = A000081TriadicSystem(max_order=8)
    engine = AutogenesisEngine(triadic_system, initial_order=4)
    
    # Run some modifications
    engine.autogenetic_cycle(num_modifications=5)
    
    # Get statistics
    stats = engine.get_statistics()
    
    assert 'mode' in stats
    assert 'generation' in stats
    assert 'fitness' in stats
    assert stats['total_modifications'] == 5


# Integration Tests

def test_full_autogenetic_pipeline():
    """Test complete autogenetic pipeline"""
    # Create triadic system
    triadic_system = A000081TriadicSystem(max_order=8)
    
    # Create autogenesis engine
    engine = AutogenesisEngine(
        triadic_system,
        initial_order=4,
        mode=AutogenesisMode.EXPLORATORY
    )
    
    # Create transformer encoder
    transformer_encoder = TransformerDatabaseEncoder()
    
    # Create Aphrodite induction engine
    reservoir = MembraneReservoir(name="autogenetic_reservoir")
    aphrodite = AphroditeInductionEngine(reservoir, transformer_encoder)
    
    # Create agentic membrane
    membrane = YggdrasilMembrane(
        name="autogenetic_membrane",
        membrane_type=MembraneType.COGNITIVE
    )
    forest = AgenticDecisionForest(membrane, agency_level=AgencyLevel.AUTONOMOUS)
    
    # Run autogenetic evolution
    engine.evolve(generations=3, modifications_per_generation=2)
    
    # Verify system state
    assert engine.state.generation >= 1
    assert engine.state.total_modifications == 6
    
    # Get comprehensive statistics
    autogenesis_stats = engine.get_statistics()
    triadic_stats = triadic_system.get_statistics()
    agency_stats = forest.get_agency_statistics()
    armature_stats = aphrodite.get_armature_statistics()
    
    assert autogenesis_stats['total_modifications'] == 6
    assert triadic_stats['total_elements'] > 0
    assert agency_stats['agency_level'] == 'autonomous'
    assert len(armature_stats) == 6


def test_triadic_correspondence_consistency():
    """Test consistency across triadic correspondence"""
    system = A000081TriadicSystem(max_order=6)
    
    # For each order, verify all three representations exist
    for order in range(1, 7):
        elements = system.enumerate_order(order)
        
        for element in elements:
            # Check B-Series
            assert element.butcher_tree is not None
            
            # Check P-System
            assert element.membrane_structure is not None
            assert element.evolution_rule is not None
            
            # Check J-Surface
            assert element.differential_operator is not None
            assert element.julia_code is not None
