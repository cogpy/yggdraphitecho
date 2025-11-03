"""
Yggdrasil Membrane Reservoir Implementation

This module implements P-System membrane computing using Yggdrasil decision
forests as computational substrates. Each membrane is a decision forest that
processes atoms and communicates with other membranes.
"""

import logging
from typing import Dict, List, Optional, Any, Callable, Set
from dataclasses import dataclass, field
from enum import Enum
from collections import deque
import numpy as np
import time

from ..core.yggdrasil_atomspace import (
    YggdrasilAtomSpace, Atom, AtomType, TruthValue, AttentionValue
)


class MembraneType(Enum):
    """Types of computational membranes"""
    SENSORY = "sensory"  # Process sensory input
    MOTOR = "motor"  # Generate motor output
    COGNITIVE = "cognitive"  # Reasoning and planning
    EMOTIONAL = "emotional"  # Affective processing
    METACOGNITIVE = "metacognitive"  # Self-monitoring
    MEMORY = "memory"  # Long-term storage
    ATTENTION = "attention"  # Attention allocation


class MessagePriority(Enum):
    """Message priority levels"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class MembraneMessage:
    """Message passed between membranes"""
    source_membrane: str
    target_membrane: str
    message_type: str
    data: Any
    timestamp: float = field(default_factory=time.time)
    priority: MessagePriority = MessagePriority.MEDIUM
    security_level: str = "standard"
    ttl: int = 10  # Time to live (hops)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'source': self.source_membrane,
            'target': self.target_membrane,
            'type': self.message_type,
            'data': self.data,
            'timestamp': self.timestamp,
            'priority': self.priority.value,
            'security_level': self.security_level,
            'ttl': self.ttl
        }


@dataclass
class MembraneRule:
    """Processing rule for membrane computing"""
    name: str
    condition: Callable[[Atom], bool]
    action: Callable[[Atom, 'YggdrasilMembrane'], None]
    priority: int = 1
    enabled: bool = True


class YggdrasilMembrane:
    """
    Membrane computing unit backed by Yggdrasil decision forests
    
    Each membrane maintains a local atomspace and decision forest model,
    processes atoms according to rules, and communicates with other membranes.
    """
    
    def __init__(self, 
                 name: str,
                 membrane_type: MembraneType,
                 parent: Optional['YggdrasilMembrane'] = None,
                 security_level: str = "standard"):
        """
        Initialize Yggdrasil Membrane
        
        Args:
            name: Unique membrane identifier
            membrane_type: Type of membrane
            parent: Optional parent membrane
            security_level: Security level (standard, secure, encrypted)
        """
        self.name = name
        self.membrane_type = membrane_type
        self.parent = parent
        self.security_level = security_level
        self.logger = logging.getLogger(f"{__name__}.{name}")
        
        # Local atomspace
        self.atomspace = YggdrasilAtomSpace(name=f"{name}_atomspace")
        
        # Child membranes
        self.children: List['YggdrasilMembrane'] = []
        
        # Message queue
        self.message_queue: deque = deque(maxlen=1000)
        self.sent_messages: List[MembraneMessage] = []
        self.received_messages: List[MembraneMessage] = []
        
        # Processing rules
        self.rules: List[MembraneRule] = []
        
        # State and resources
        self.state = "initialized"
        self.resources = {
            'memory': 0.0,
            'cpu': 0.0,
            'io': 0.0,
            'attention': 100.0  # ECAN attention budget
        }
        
        # Permissions and access control
        self.permissions: Set[str] = set()
        self.allowed_sources: Set[str] = set()
        self.allowed_targets: Set[str] = set()
        
        # Statistics
        self.stats = {
            'messages_sent': 0,
            'messages_received': 0,
            'messages_processed': 0,
            'messages_rejected': 0,
            'atoms_processed': 0,
            'rules_executed': 0
        }
        
        self.logger.info(f"Initialized {membrane_type.value} membrane: {name}")
    
    def add_child(self, child: 'YggdrasilMembrane'):
        """Add child membrane"""
        if child not in self.children:
            self.children.append(child)
            child.parent = self
            self.logger.debug(f"Added child membrane: {child.name}")
    
    def remove_child(self, child: 'YggdrasilMembrane'):
        """Remove child membrane"""
        if child in self.children:
            self.children.remove(child)
            child.parent = None
            self.logger.debug(f"Removed child membrane: {child.name}")
    
    def add_rule(self, rule: MembraneRule):
        """Add processing rule"""
        self.rules.append(rule)
        self.rules.sort(key=lambda r: r.priority, reverse=True)
        self.logger.debug(f"Added rule: {rule.name}")
    
    def remove_rule(self, rule_name: str):
        """Remove processing rule"""
        self.rules = [r for r in self.rules if r.name != rule_name]
        self.logger.debug(f"Removed rule: {rule_name}")
    
    def grant_permission(self, permission: str):
        """Grant permission to this membrane"""
        self.permissions.add(permission)
    
    def revoke_permission(self, permission: str):
        """Revoke permission from this membrane"""
        self.permissions.discard(permission)
    
    def allow_source(self, source: str):
        """Allow messages from specific source"""
        self.allowed_sources.add(source)
    
    def allow_target(self, target: str):
        """Allow sending messages to specific target"""
        self.allowed_targets.add(target)
    
    def _validate_outgoing_message(self, message: MembraneMessage) -> bool:
        """Validate outgoing message"""
        # Check if target is allowed
        if self.allowed_targets and message.target_membrane not in self.allowed_targets:
            self.logger.warning(
                f"Target not allowed: {message.target_membrane}"
            )
            return False
        
        # Check security level compatibility
        if message.security_level == "encrypted" and self.security_level != "encrypted":
            self.logger.warning("Cannot send encrypted message from non-encrypted membrane")
            return False
        
        # Check TTL
        if message.ttl <= 0:
            self.logger.warning("Message TTL expired")
            return False
        
        return True
    
    def _validate_incoming_message(self, message: MembraneMessage) -> bool:
        """Validate incoming message"""
        # Check if source is allowed
        if self.allowed_sources and message.source_membrane not in self.allowed_sources:
            self.logger.warning(
                f"Source not allowed: {message.source_membrane}"
            )
            return False
        
        # Check security level compatibility
        if message.security_level == "encrypted" and self.security_level != "encrypted":
            self.logger.warning("Cannot receive encrypted message in non-encrypted membrane")
            return False
        
        return True
    
    def send_message(self, 
                    target: str,
                    message_type: str,
                    data: Any,
                    priority: MessagePriority = MessagePriority.MEDIUM,
                    security_level: Optional[str] = None) -> bool:
        """
        Send message to another membrane
        
        Args:
            target: Target membrane name
            message_type: Type of message
            data: Message payload
            priority: Message priority
            security_level: Optional security level override
            
        Returns:
            True if message was sent successfully
        """
        message = MembraneMessage(
            source_membrane=self.name,
            target_membrane=target,
            message_type=message_type,
            data=data,
            priority=priority,
            security_level=security_level or self.security_level
        )
        
        if not self._validate_outgoing_message(message):
            self.stats['messages_rejected'] += 1
            return False
        
        # Start routing from self
        success = self._route_message(message)
        if success:
            self.sent_messages.append(message)
            self.stats["messages_sent"] += 1
            self.logger.debug(
                f"Sent message to {target}: {message_type}"
            )
        return success
    
    def _route_message(self, message: MembraneMessage) -> bool:
        """Route message to target membrane"""
        # Decrease TTL
        message.ttl -= 1
        if message.ttl <= 0:
            self.logger.warning("Message TTL expired during routing")
            return False
        
        # Check if this is the target
        if message.target_membrane == self.name:
            return self.receive_message(message)
        
        # Check children
        for child in self.children:
            if child.name == message.target_membrane:
                return child.receive_message(message)
            if child._route_message(message):
                return True
        
        # If not found, and this is not the root, pass to parent
        if self.parent:
            return self.parent._route_message(message)

        # If this is the root and not found, the message cannot be routed
        if not self.parent:
            root_membrane = self
            # Check all membranes in the hierarchy starting from the root
            target_membrane = root_membrane._find_descendant(message.target_membrane)
            if target_membrane:
                return target_membrane.receive_message(message)

        self.logger.warning(
            f"Could not route message to {message.target_membrane}"
        )
        return False
    
    def _find_descendant(self, name: str) -> Optional['YggdrasilMembrane']:
        """Find a descendant membrane by name"""
        for child in self.children:
            if child.name == name:
                return child
            found = child._find_descendant(name)
            if found:
                return found
        return None

    def receive_message(self, message: MembraneMessage) -> bool:
        """
        Receive message from another membrane
        
        Args:
            message: Incoming message
            
        Returns:
            True if message was accepted
        """
        if not self._validate_incoming_message(message):
            self.stats['messages_rejected'] += 1
            return False
        
        self.message_queue.append(message)
        self.received_messages.append(message)
        self.stats['messages_received'] += 1
        
        self.logger.debug(
            f"Received message from {message.source_membrane}: {message.message_type}"
        )
        return True
    
    def process_messages(self, max_messages: int = 10) -> int:
        """
        Process messages from queue
        
        Args:
            max_messages: Maximum number of messages to process
            
        Returns:
            Number of messages processed
        """
        processed = 0
        
        # Sort by priority
        messages = sorted(
            list(self.message_queue)[:max_messages],
            key=lambda m: m.priority.value,
            reverse=True
        )
        
        for message in messages:
            self._process_message(message)
            self.message_queue.remove(message)
            processed += 1
            self.stats['messages_processed'] += 1
        
        return processed
    
    def _process_message(self, message: MembraneMessage):
        """Process a single message"""
        self.logger.debug(
            f"Processing message: {message.message_type} from {message.source_membrane}"
        )
        
        # Handle different message types
        if message.message_type == "atom_transfer":
            self._handle_atom_transfer(message)
        elif message.message_type == "query":
            self._handle_query(message)
        elif message.message_type == "command":
            self._handle_command(message)
        elif message.message_type == "notification":
            self._handle_notification(message)
        else:
            self.logger.warning(f"Unknown message type: {message.message_type}")
    
    def _handle_atom_transfer(self, message: MembraneMessage):
        """Handle atom transfer message"""
        atom_data = message.data
        # Create atom in local atomspace
        # Implementation depends on atom data format
        pass
    
    def _handle_query(self, message: MembraneMessage):
        """Handle query message"""
        query = message.data
        # Process query and send response
        # Implementation depends on query format
        pass
    
    def _handle_command(self, message: MembraneMessage):
        """Handle command message"""
        command = message.data
        # Execute command
        # Implementation depends on command format
        pass
    
    def _handle_notification(self, message: MembraneMessage):
        """Handle notification message"""
        # Log notification
        self.logger.info(f"Notification: {message.data}")
    
    def process_atoms(self, max_atoms: int = 100) -> int:
        """
        Process atoms according to membrane rules
        
        Args:
            max_atoms: Maximum number of atoms to process
            
        Returns:
            Number of atoms processed
        """
        processed = 0
        
        # Get atoms sorted by attention value
        atoms = sorted(
            self.atomspace.atoms.values(),
            key=lambda a: a.attention_value.sti,
            reverse=True
        )[:max_atoms]
        
        for atom in atoms:
            # Apply rules
            for rule in self.rules:
                if not rule.enabled:
                    continue
                
                try:
                    if rule.condition(atom):
                        rule.action(atom, self)
                        self.stats['rules_executed'] += 1
                except Exception as e:
                    self.logger.error(
                        f"Error executing rule {rule.name}: {e}"
                    )
            
            processed += 1
            self.stats['atoms_processed'] += 1
        
        return processed
    
    def step(self, process_messages: bool = True, process_atoms: bool = True):
        """
        Execute one processing step
        
        Args:
            process_messages: Whether to process messages
            process_atoms: Whether to process atoms
        """
        if process_messages:
            self.process_messages()
        
        if process_atoms:
            self.process_atoms()
        
        # Process children
        for child in self.children:
            child.step(process_messages, process_atoms)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get membrane statistics"""
        return {
            'name': self.name,
            'type': self.membrane_type.value,
            'state': self.state,
            'resources': self.resources.copy(),
            'stats': self.stats.copy(),
            'atomspace': self.atomspace.get_statistics(),
            'children': [child.name for child in self.children],
            'message_queue_size': len(self.message_queue),
            'rules_count': len(self.rules)
        }
    
    def shutdown(self):
        """Shutdown membrane and children"""
        self.logger.info(f"Shutting down membrane: {self.name}")
        
        # Shutdown children first
        for child in self.children:
            child.shutdown()
        
        # Clear resources
        self.atomspace.clear()
        self.message_queue.clear()
        self.state = "shutdown"


class MembraneReservoir:
    """
    Collection of interconnected membranes forming a reservoir
    
    This class manages multiple membranes and their interactions,
    implementing a reservoir computing architecture.
    """
    
    def __init__(self, name: str):
        """
        Initialize membrane reservoir
        
        Args:
            name: Reservoir name
        """
        self.name = name
        self.logger = logging.getLogger(f"{__name__}.{name}")
        
        # Membrane registry
        self.membranes: Dict[str, YggdrasilMembrane] = {}
        self.root_membranes: List[YggdrasilMembrane] = []
        
        # Global message routing
        self.message_history: List[MembraneMessage] = []
        
        self.logger.info(f"Initialized membrane reservoir: {name}")
    
    def add_membrane(self, membrane: YggdrasilMembrane, 
                    parent_name: Optional[str] = None):
        """
        Add membrane to reservoir
        
        Args:
            membrane: Membrane to add
            parent_name: Optional parent membrane name
        """
        if membrane.name in self.membranes:
            raise ValueError(f"Membrane already exists: {membrane.name}")
        
        self.membranes[membrane.name] = membrane
        
        if parent_name:
            parent = self.membranes.get(parent_name)
            if parent:
                parent.add_child(membrane)
            else:
                raise ValueError(f"Parent membrane not found: {parent_name}")
        else:
            self.root_membranes.append(membrane)
        
        self.logger.info(f"Added membrane: {membrane.name}")
    
    def remove_membrane(self, membrane_name: str):
        """Remove membrane from reservoir"""
        if membrane_name not in self.membranes:
            return
        
        membrane = self.membranes[membrane_name]
        
        # Remove from parent
        if membrane.parent:
            membrane.parent.remove_child(membrane)
        else:
            self.root_membranes.remove(membrane)
        
        # Shutdown and remove
        membrane.shutdown()
        del self.membranes[membrane_name]
        
        self.logger.info(f"Removed membrane: {membrane_name}")
    
    def get_membrane(self, name: str) -> Optional[YggdrasilMembrane]:
        """Get membrane by name"""
        return self.membranes.get(name)
    
    def step(self, steps: int = 1):
        """
        Execute processing steps for all membranes
        
        Args:
            steps: Number of steps to execute
        """
        for _ in range(steps):
            for membrane in self.root_membranes:
                membrane.step()
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get reservoir statistics"""
        return {
            'name': self.name,
            'total_membranes': len(self.membranes),
            'root_membranes': len(self.root_membranes),
            'membranes': {
                name: membrane.get_statistics()
                for name, membrane in self.membranes.items()
            }
        }
    
    def shutdown(self):
        """Shutdown all membranes"""
        self.logger.info(f"Shutting down reservoir: {self.name}")
        for membrane in self.root_membranes:
            membrane.shutdown()
        self.membranes.clear()
        self.root_membranes.clear()
