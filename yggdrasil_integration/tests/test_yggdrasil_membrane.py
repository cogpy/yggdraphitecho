import pytest
from yggdrasil_integration.membranes.yggdrasil_membrane import (
    YggdrasilMembrane, MembraneReservoir, MembraneType, MembraneMessage, MessagePriority
)

@pytest.fixture
def reservoir():
    """Fixture for creating a MembraneReservoir instance."""
    return MembraneReservoir(name="test_reservoir")

@pytest.fixture
def membranes(reservoir):
    """Fixture for creating a set of membranes."""
    root_membrane = YggdrasilMembrane(name="root", membrane_type=MembraneType.COGNITIVE)
    child1_membrane = YggdrasilMembrane(name="child1", membrane_type=MembraneType.SENSORY)
    child2_membrane = YggdrasilMembrane(name="child2", membrane_type=MembraneType.MOTOR)
    
    reservoir.add_membrane(root_membrane)
    reservoir.add_membrane(child1_membrane, parent_name="root")
    reservoir.add_membrane(child2_membrane, parent_name="root")
    
    return {
        "root": root_membrane,
        "child1": child1_membrane,
        "child2": child2_membrane
    }

def test_add_membrane(reservoir):
    """Test adding a membrane to the reservoir."""
    membrane = YggdrasilMembrane(name="test_membrane", membrane_type=MembraneType.COGNITIVE)
    reservoir.add_membrane(membrane)
    assert reservoir.get_membrane("test_membrane") is not None
    assert len(reservoir.membranes) == 1

def test_send_and_receive_message(membranes):
    """Test sending and receiving a message between membranes."""
    root = membranes["root"]
    child1 = membranes["child1"]
    
    # Allow communication
    root.allow_target("child1")
    child1.allow_source("root")
    
    success = root.send_message("child1", "test_message", {"data": "hello"})
    assert success is True
    assert len(child1.message_queue) == 1
    
    message = child1.message_queue[0]
    assert message.source_membrane == "root"
    assert message.data["data"] == "hello"

def test_process_messages(membranes):
    """Test processing messages in a membrane."""
    child1 = membranes["child1"]
    message = MembraneMessage(
        source_membrane="external",
        target_membrane="child1",
        message_type="notification",
        data="test"
    )
    child1.receive_message(message)
    
    processed_count = child1.process_messages()
    assert processed_count == 1
    assert len(child1.message_queue) == 0

def test_membrane_rules(membranes):
    """Test membrane processing rules."""
    from yggdrasil_integration.core.yggdrasil_atomspace import Atom, AtomType
    from yggdrasil_integration.membranes.yggdrasil_membrane import MembraneRule

    child1 = membranes["child1"]
    
    # Add a rule
    def condition(atom):
        return atom.name == "test_atom"
    
    def action(atom, membrane):
        membrane.logger.info(f"Rule executed for atom: {atom.name}")
        membrane.stats["rule_action_executed"] = True

    rule = MembraneRule(name="test_rule", condition=condition, action=action)
    child1.add_rule(rule)
    
    # Add an atom that triggers the rule
    child1.atomspace.add_node(AtomType.CONCEPT_NODE, "test_atom")
    
    # Process atoms
    child1.process_atoms()
    
    assert child1.stats.get("rule_action_executed") is True

def test_reservoir_step(reservoir, membranes):
    """Test a full processing step in the reservoir."""
    root = membranes["root"]
    child1 = membranes["child1"]
    
    # Allow communication
    root.allow_target("child1")
    child1.allow_source("root")
    
    # Send a message
    root.send_message("child1", "notification", "step_test")
    
    # Execute step
    reservoir.step()
    
    # Message should be processed
    assert len(child1.message_queue) == 0
    assert child1.stats["messages_processed"] == 1
