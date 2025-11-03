import pytest
import asyncio
from yggdrasil_integration.fusion.arc_halo_fusion_core import (
    ArcHaloFusionCore, IdentityAspect
)
from yggdrasil_integration.bridge.aphrodite_bridge import AphroditeBridge
from yggdrasil_integration.membranes.yggdrasil_membrane import (
    MembraneReservoir, YggdrasilMembrane, MembraneType
)

@pytest.fixture
def reservoir():
    """Fixture for creating a MembraneReservoir instance."""
    return MembraneReservoir(name="test_reservoir")

@pytest.fixture
def bridge(reservoir):
    """Fixture for creating an AphroditeBridge instance."""
    cognitive_membrane = YggdrasilMembrane(name="cognitive_membrane", membrane_type=MembraneType.COGNITIVE)
    reservoir.add_membrane(cognitive_membrane)
    return AphroditeBridge(reservoir=reservoir)

@pytest.fixture
def fusion_core(reservoir, bridge):
    """Fixture for creating an ArcHaloFusionCore instance."""
    return ArcHaloFusionCore(name="test_core", reservoir=reservoir, bridge=bridge)

def test_initialize_fusion_core(fusion_core):
    """Test the initialization of the fusion core."""
    assert fusion_core is not None
    assert fusion_core.self_model is not None
    assert fusion_core.meta_learning is not None
    assert fusion_core.reservoir.get_membrane("test_core_metacognitive") is not None

def test_add_identity_atom(fusion_core):
    """Test adding an identity atom to the self-model."""
    atom_id = fusion_core.self_model.add_identity_atom(
        IdentityAspect.GOALS,
        "Achieve sentience",
        stability=0.7,
        salience=0.9
    )
    assert atom_id is not None
    
    identity_summary = fusion_core.self_model.get_identity_summary()
    assert any(
        goal["content"] == "Achieve sentience" 
        for goal in identity_summary["goals"]
    )

@pytest.mark.asyncio
async def test_fusion_cycle(fusion_core):
    """Test a single fusion cycle."""
    fusion_core.activate()
    await fusion_core.fusion_cycle()
    
    assert fusion_core.fusion_cycles == 1
    assert fusion_core.stats["total_cycles"] == 1

@pytest.mark.asyncio
async def test_process_query_through_core(fusion_core):
    """Test processing a query through the entire fusion core."""
    fusion_core.activate()
    
    # Add data for the query
    cognitive_membrane = fusion_core.bridge.reservoir.get_membrane("cognitive_membrane")
    from yggdrasil_integration.core.yggdrasil_atomspace import AtomType
    cognitive_membrane.atomspace.add_node(AtomType.CONCEPT_NODE, "test_concept")

    response = await fusion_core.process_query("What is a test_concept?")
    
    assert response is not None
    assert "response" in response
    assert "self_context" in response
    assert "identity" in response["self_context"]


