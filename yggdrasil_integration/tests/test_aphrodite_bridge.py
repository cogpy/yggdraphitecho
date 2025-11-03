import pytest
import asyncio
from yggdrasil_integration.bridge.aphrodite_bridge import (
    AphroditeBridge, BridgeQuery, QueryType, ReasoningMode
)
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
    # Add a cognitive membrane for the bridge to use
    cognitive_membrane = YggdrasilMembrane(name="cognitive_membrane", membrane_type=MembraneType.COGNITIVE)
    reservoir.add_membrane(cognitive_membrane)
    return AphroditeBridge(reservoir=reservoir)

@pytest.mark.asyncio
async def test_process_symbolic_query(bridge):
    """Test processing a symbolic query."""
    # Add some data to the atomspace
    cognitive_membrane = bridge.reservoir.get_membrane("cognitive_membrane")
    from yggdrasil_integration.core.yggdrasil_atomspace import AtomType
    cognitive_membrane.atomspace.add_node(AtomType.CONCEPT_NODE, "test_entity")

    query = BridgeQuery(
        query_id="test_query_1",
        query_type=QueryType.PATTERN_MATCH,
        natural_language="Find test_entity",
        reasoning_mode=ReasoningMode.SYMBOLIC
    )
    
    response = await bridge.process_query(query)
    
    assert response is not None
    assert response.reasoning_mode_used == ReasoningMode.SYMBOLIC
    assert len(response.results) > 0
    assert response.results[0]["name"] == "test_entity"

@pytest.mark.asyncio
async def test_process_neural_query(bridge):
    """Test processing a neural query."""
    query = BridgeQuery(
        query_id="test_query_2",
        query_type=QueryType.EXPLANATION,
        natural_language="Explain the meaning of life",
        reasoning_mode=ReasoningMode.NEURAL
    )
    
    response = await bridge.process_query(query)
    
    assert response is not None
    assert response.reasoning_mode_used == ReasoningMode.NEURAL
    assert len(response.results) > 0
    assert "Neural reasoning result" in response.results[0]["content"]

@pytest.mark.asyncio
async def test_process_hybrid_query(bridge):
    """Test processing a hybrid query."""
    # Add data for symbolic part
    cognitive_membrane = bridge.reservoir.get_membrane("cognitive_membrane")
    from yggdrasil_integration.core.yggdrasil_atomspace import AtomType
    cognitive_membrane.atomspace.add_node(AtomType.CONCEPT_NODE, "hybrid_entity")

    query = BridgeQuery(
        query_id="test_query_3",
        query_type=QueryType.INFERENCE,
        natural_language="What can be inferred from hybrid_entity?",
        reasoning_mode=ReasoningMode.HYBRID
    )
    
    response = await bridge.process_query(query)
    
    assert response is not None
    assert response.reasoning_mode_used == ReasoningMode.HYBRID
    assert len(response.results) > 0
    # Check for merged results
    assert any(r.get("source") == "symbolic" for r in response.results)
    assert any(r.get("source") == "neural" for r in response.results)

def test_query_translator(bridge):
    """Test the query translator."""
    query = BridgeQuery(
        query_id="test_query_4",
        query_type=QueryType.CAUSAL,
        natural_language="What causes rain?"
    )
    
    cognitive_membrane = bridge.reservoir.get_membrane("cognitive_membrane")
    pattern = bridge.translator.translate_query(query, cognitive_membrane.atomspace)
    
    assert pattern is not None
    assert "rain" in pattern["entities"]
    assert "causes" in pattern["relationships"]
