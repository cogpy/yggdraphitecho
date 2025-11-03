import pytest
import numpy as np
from yggdrasil_integration.core.yggdrasil_atomspace import (
    YggdrasilAtomSpace, AtomType, TruthValue, AttentionValue
)

@pytest.fixture
def atomspace():
    """Fixture for creating a YggdrasilAtomSpace instance."""
    return YggdrasilAtomSpace(name="test_atomspace")

def test_add_node(atomspace):
    """Test adding a node to the atomspace."""
    atom_id = atomspace.add_node(AtomType.CONCEPT_NODE, "test_node")
    assert atom_id is not None
    assert atomspace.get_atom(atom_id) is not None
    assert atomspace.stats['total_atoms'] == 1

def test_add_link(atomspace):
    """Test adding a link to the atomspace."""
    node1_id = atomspace.add_node(AtomType.CONCEPT_NODE, "node1")
    node2_id = atomspace.add_node(AtomType.CONCEPT_NODE, "node2")
    link_id = atomspace.add_link(AtomType.SIMILARITY_LINK, [node1_id, node2_id])
    assert link_id is not None
    assert atomspace.get_atom(link_id) is not None
    assert atomspace.stats['total_atoms'] == 3
    assert len(atomspace.get_incoming_set(node1_id)) == 1
    assert len(atomspace.get_incoming_set(node2_id)) == 1

def test_remove_atom(atomspace):
    """Test removing an atom from the atomspace."""
    node_id = atomspace.add_node(AtomType.CONCEPT_NODE, "test_node")
    assert atomspace.remove_atom(node_id) is True
    assert atomspace.get_atom(node_id) is None
    assert atomspace.stats['total_atoms'] == 0

def test_get_atoms_by_type(atomspace):
    """Test retrieving atoms by type."""
    atomspace.add_node(AtomType.CONCEPT_NODE, "concept1")
    atomspace.add_node(AtomType.CONCEPT_NODE, "concept2")
    atomspace.add_node(AtomType.PREDICATE_NODE, "predicate1")
    concept_nodes = atomspace.get_atoms_by_type(AtomType.CONCEPT_NODE)
    assert len(concept_nodes) == 2

def test_update_truth_value(atomspace):
    """Test updating the truth value of an atom."""
    node_id = atomspace.add_node(AtomType.CONCEPT_NODE, "test_node")
    new_truth_value = TruthValue(strength=0.9, confidence=0.8)
    atomspace.update_truth_value(node_id, new_truth_value)
    updated_atom = atomspace.get_atom(node_id)
    assert updated_atom.truth_value.strength == 0.9
    assert updated_atom.truth_value.confidence == 0.8

def test_feature_matrix(atomspace):
    """Test feature matrix generation."""
    atomspace.add_node(AtomType.CONCEPT_NODE, "node1")
    atomspace.add_node(AtomType.CONCEPT_NODE, "node2")
    feature_matrix = atomspace.get_feature_matrix()
    assert feature_matrix.shape[0] == 2

def test_train_and_query_forest(atomspace):
    """Test training and querying a decision forest model."""
    # Add some data
    atom_ids = []
    for i in range(10):
        atom_ids.append(atomspace.add_node(AtomType.CONCEPT_NODE, f"node_{i}"))
    
    # Create labels
    labels = np.array([0, 1, 0, 1, 0, 1, 0, 1, 0, 1])
    
    # Train model
    atomspace.train_forest_model("test_domain", atom_ids, labels)
    assert "test_domain" in atomspace.forest_models
    
    # Query model
    query_features = atomspace.get_feature_matrix([atom_ids[0]])
    predictions = atomspace.query_forest("test_domain", query_features)
    assert predictions is not None

def test_find_similar_atoms(atomspace):
    """Test finding similar atoms."""
    atom_ids = []
    for i in range(10):
        atom_ids.append(atomspace.add_node(AtomType.CONCEPT_NODE, f"node_{i}"))
    
    similar_atoms = atomspace.find_similar_atoms(atom_ids[0], top_k=5)
    assert len(similar_atoms) == 5
    assert similar_atoms[0][1] > 0 # Similarity score should be positive
