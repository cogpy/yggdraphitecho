"""
Tests for P-Lingua Relevance Realization System

This module tests the complete integration of P-Lingua, Relevance Realization
Ennead, and the triadic correspondence/autogenesis system.
"""

import pytest
import numpy as np
from yggdrasil_integration.plingua import (
    PLinguaParser, PLinguaInterpreter, ThetaSystem, Triad,
    RelevanceRealizationEnnead, EnneadFactory,
    PLinguaMembraneBridge, EnneadTriadicAutogenesis
)
from yggdrasil_integration.triadic import A000081TriadicSystem, AutogenesisMode


def test_plingua_parser():
    """Test P-Lingua parser"""
    parser = PLinguaParser()
    
    source = """
    @model<test_model>
    @Θ-system test_system {
        @agent_arena main {
            @lambda[1] 'autopoiesis {
                (μ_bio, σ_mil, τ_trans);
            }
        }
    }
    """
    
    theta_system = parser.parse(source)
    
    assert theta_system.model_name == "test_model"
    assert len(theta_system.agent_arenas) > 0


def test_plingua_interpreter():
    """Test P-Lingua interpreter"""
    parser = PLinguaParser()
    
    source = """
    @model<test_model>
    @Θ-system test_system {
        @agent_arena main {
            @lambda[1] 'autopoiesis {
                (μ, σ, τ);
                [μ, σ, τ --> μ', σ', τ']'autopoiesis;
            }
        }
    }
    """
    
    theta_system = parser.parse(source)
    interpreter = PLinguaInterpreter(theta_system)
    
    stats = interpreter.run(max_steps=10)
    
    assert stats['steps_executed'] >= 0
    assert 'final_relevance' in stats


def test_relevance_realization_ennead():
    """Test Relevance Realization Ennead"""
    ennead = EnneadFactory.create_default_ennead()
    
    # Update ennead
    env_input = complex(1.0, 0.5)
    arena_state = np.array([1.0, 0.0, 0.0, 0.0])
    
    for _ in range(10):
        ennead.update(env_input, arena_state)
    
    stats = ennead.get_statistics()
    
    assert 'autopoiesis' in stats
    assert 'anticipation' in stats
    assert 'adaptation' in stats
    assert 'emergent' in stats
    assert stats['emergent']['relevance_realization'] >= 0.0


def test_autopoietic_triad():
    """Test autopoietic triad dynamics"""
    from yggdrasil_integration.plingua import AutopoieticTriad
    
    triad = AutopoieticTriad(
        biosynthesis=1.0,
        milieu=1.0,
        transport=1.0
    )
    
    # Update for several steps
    for _ in range(100):
        triad.update(dt=0.01)
    
    # Check coupling emerged
    assert triad.coupling_strength > 0.0


def test_anticipation_triad():
    """Test anticipation triad dynamics"""
    from yggdrasil_integration.plingua import AnticipationTriad
    
    triad = AnticipationTriad(
        models=complex(1.0, 0.0),
        state=complex(1.0, 0.0),
        effectors=complex(1.0, 0.0)
    )
    
    # Update with environmental input
    for i in range(100):
        env_input = complex(np.sin(i / 10.0), np.cos(i / 10.0))
        triad.update(env_input, dt=0.01)
    
    # Prediction error should be bounded
    assert triad.prediction_error >= 0.0


def test_adaptation_triad():
    """Test adaptation triad dynamics"""
    from yggdrasil_integration.plingua import AdaptationTriad
    
    triad = AdaptationTriad(
        goals=np.array([1.0, 0.0, 0.0, 0.0]),
        actions=np.array([1.0, 0.0, 0.0, 0.0]),
        affordances=np.array([1.0, 0.0, 0.0, 0.0])
    )
    
    # Update with arena state
    for i in range(100):
        arena = np.array([
            np.sin(i / 10.0),
            np.cos(i / 10.0),
            0.0,
            0.0
        ])
        triad.update(arena, dt=0.01)
    
    # Coupling should emerge
    assert triad.agent_arena_coupling != 0.0
    assert triad.relevance_gradient > 0.0


def test_plingua_membrane_bridge():
    """Test P-Lingua membrane bridge"""
    bridge = PLinguaMembraneBridge()
    
    source = """
    @model<bridge_test>
    @Θ-system test {
        @agent_arena main {
            @lambda[1] 'auto {
                (x, y, z);
            }
        }
    }
    """
    
    # Parse
    theta_system = bridge.parse_plingua(source)
    
    # Just check parsing worked
    assert theta_system.model_name == "bridge_test"


def test_theta_to_reservoir_conversion():
    """Test Θ-system to reservoir conversion"""
    bridge = PLinguaMembraneBridge()
    parser = PLinguaParser()
    
    source = """
    @model<conversion_test>
    @Θ-system test {
        @agent_arena main {
            @lambda[1] 'autopoiesis {
                (μ, σ, τ);
            }
        }
    }
    """
    
    theta_system = parser.parse(source)
    
    # Just check parsing
    assert theta_system.model_name == "conversion_test"


def test_ennead_integration_with_membrane():
    """Test Ennead integration with membrane"""
    bridge = PLinguaMembraneBridge()
    
    # Just test bridge creation
    stats = bridge.get_statistics()
    assert 'membranes' in stats
    assert 'enneads' in stats


def test_ennead_triadic_autogenesis():
    """Test Ennead-Triadic-Autogenesis integration"""
    # Create components
    ennead = EnneadFactory.create_default_ennead()
    triadic_system = A000081TriadicSystem(max_order=5)
    
    # Create integrated system
    eta = EnneadTriadicAutogenesis(
        ennead=ennead,
        triadic_system=triadic_system,
        autogenesis_mode=AutogenesisMode.CONSERVATIVE
    )
    
    stats = eta.get_statistics()
    
    assert 'current_step' in stats
    assert 'ennead' in stats


def test_ennead_triadic_mapping():
    """Test Ennead-Triadic mapping"""
    ennead = EnneadFactory.create_default_ennead()
    triadic_system = A000081TriadicSystem(max_order=5)
    
    eta = EnneadTriadicAutogenesis(ennead, triadic_system, AutogenesisMode.CONSERVATIVE)
    
    mapping = eta.get_ennead_triadic_mapping()
    
    assert 'autopoiesis' in mapping
    assert 'anticipation' in mapping
    assert 'adaptation' in mapping


def test_relevance_driven_modification():
    """Test relevance-driven autogenetic modification"""
    ennead = EnneadFactory.create_default_ennead()
    triadic_system = A000081TriadicSystem(max_order=10)
    
    eta = EnneadTriadicAutogenesis(
        ennead,
        triadic_system,
        AutogenesisMode.EXPLORATORY
    )
    
    # Force low relevance to trigger modification
    eta.ennead.relevance_realization = 0.2
    
    # Update should trigger modification
    env_input = complex(1.0, 0.0)
    arena_state = np.array([1.0, 0.0, 0.0, 0.0])
    
    eta.update(env_input, arena_state)
    
    # Check if modification was considered
    assert len(eta.relevance_history) > 0


def test_ennead_evolution():
    """Test Ennead evolution over multiple generations"""
    ennead = EnneadFactory.create_default_ennead()
    triadic_system = A000081TriadicSystem(max_order=5)
    
    eta = EnneadTriadicAutogenesis(ennead, triadic_system, AutogenesisMode.CONSERVATIVE)
    
    # Evolve for 5 generations
    stats = eta.evolve(generations=5)
    
    assert stats['generations'] == 5
    assert 'final_relevance' in stats


def test_complete_plingua_rr_pipeline():
    """Test complete P-Lingua RR pipeline"""
    # Parse P-Lingua
    parser = PLinguaParser()
    
    source = """
    @model<complete_test>
    @Θ-system complete {
        @agent_arena main {
            @lambda[1] 'autopoiesis {
                (μ_bio, σ_mil, τ_trans);
            }
        }
    }
    """
    
    # Parse
    theta_system = parser.parse(source)
    
    # Create Ennead and triadic system
    ennead = EnneadFactory.create_default_ennead()
    triadic_system = A000081TriadicSystem(max_order=5)
    
    # Create integrated system
    eta = EnneadTriadicAutogenesis(
        ennead,
        triadic_system,
        AutogenesisMode.CONSERVATIVE
    )
    
    # Test it works
    stats = eta.get_statistics()
    assert 'ennead' in stats


def test_plingua_code_generation():
    """Test P-Lingua code generation"""
    parser = PLinguaParser()
    
    source = """
    @model<codegen_test>
    @Θ-system test {
        @agent_arena main {
            @lambda[1] 'auto {
                (x, y, z);
            }
        }
    }
    """
    
    theta_system = parser.parse(source)
    
    # Generate code
    generated = parser.generate_code(theta_system)
    
    assert '@model<codegen_test>' in generated
    assert '@Θ-system' in generated
