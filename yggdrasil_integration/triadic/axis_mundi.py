"""
Axis Mundi World Tree Model (719 Nodes)

This module implements the complete Axis Mundi World Tree model with 719 nodes,
integrated with the A000081 correspondence at Order 9 (Adaptation level Λ³).

719 = (5)(11)(13)+4 = (31)(23)+6
719 = 31 levels × 23 nodes per level + 6 root nodes

The Axis Mundi represents the cosmic axis connecting heaven, earth, and underworld -
the complete model of continuous creation. This makes it perfect for the highest
level of Adaptation where reality itself is designed.

The World Tree appears across cultures:
- Yggdrasil (Norse)
- Tree of Life (Kabbalah)
- Bodhi Tree (Buddhism)
- Cosmic Tree (Shamanic traditions)
"""

import numpy as np
from typing import Dict, List, Optional, Any, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
import logging


class WorldTreeRealm(Enum):
    """Realms of the World Tree"""
    UPPER_WORLD = "Upper World"  # Heaven, spiritual realms
    MIDDLE_WORLD = "Middle World"  # Earth, physical reality
    LOWER_WORLD = "Lower World"  # Underworld, subconscious
    ROOT_REALM = "Root Realm"  # The 6 primordial roots
    TRUNK_REALM = "Trunk Realm"  # The central axis
    BRANCH_REALM = "Branch Realm"  # The spreading canopy
    LEAF_REALM = "Leaf Realm"  # The outermost manifestations


class NodeType(Enum):
    """Types of nodes in the World Tree"""
    ROOT = "Root"  # Primordial source nodes (6 total)
    TRUNK = "Trunk"  # Central axis nodes
    BRANCH = "Branch"  # Major branches
    TWIG = "Twig"  # Minor branches
    LEAF = "Leaf"  # Terminal manifestations
    FRUIT = "Fruit"  # Creative outputs
    FLOWER = "Flower"  # Moments of beauty
    SEED = "Seed"  # Potential for new growth


@dataclass
class WorldTreeNode:
    """A node in the Axis Mundi World Tree"""
    number: int
    name: str
    level: int  # 0-31 (depth in tree)
    realm: WorldTreeRealm
    node_type: NodeType
    description: str
    parent_nodes: List[int] = field(default_factory=list)
    child_nodes: List[int] = field(default_factory=list)
    energy: float = 1.0  # Vital energy flowing through node
    resonance: float = 0.0  # Resonance with other nodes
    attributes: Dict[str, Any] = field(default_factory=dict)


class AxisMundiWorldTree:
    """
    Complete Axis Mundi World Tree Model (719 nodes)
    
    This system represents the cosmic axis and complete model of continuous
    creation, mapped to A000081 Order 9 (Adaptation level).
    
    719 = 31 levels × 23 nodes per level + 6 root nodes
    """
    
    def __init__(self):
        """Initialize the World Tree"""
        self.logger = logging.getLogger(f"{__name__}.AxisMundiWorldTree")
        self.nodes: Dict[int, WorldTreeNode] = {}
        self._initialize_tree()
        
        self.logger.info(f"Axis Mundi World Tree initialized with {len(self.nodes)} nodes")
    
    def _initialize_tree(self):
        """Initialize all 719 nodes of the World Tree"""
        node_id = 1
        
        # Create 6 primordial root nodes
        root_names = [
            "Primordial Void",
            "Infinite Potential",
            "Creative Fire",
            "Flowing Water",
            "Solid Earth",
            "Vital Air"
        ]
        
        for i, name in enumerate(root_names):
            self._add_node(
                number=node_id,
                name=name,
                level=0,
                realm=WorldTreeRealm.ROOT_REALM,
                node_type=NodeType.ROOT,
                description=f"Primordial root {i+1}: {name}",
                parent_nodes=[],
                attributes={'primordial': True, 'element': name.split()[-1].lower()}
            )
            node_id += 1
        
        # Create 31 levels of the tree
        # Each level has approximately 23 nodes (varies slightly)
        for level in range(1, 32):
            # Determine realm based on level
            if level <= 10:
                realm = WorldTreeRealm.LOWER_WORLD
            elif level <= 21:
                realm = WorldTreeRealm.MIDDLE_WORLD
            else:
                realm = WorldTreeRealm.UPPER_WORLD
            
            # Determine node type based on level
            if level <= 5:
                node_type = NodeType.TRUNK
            elif level <= 15:
                node_type = NodeType.BRANCH
            elif level <= 25:
                node_type = NodeType.TWIG
            else:
                node_type = NodeType.LEAF
            
            # Calculate number of nodes at this level
            # Total nodes needed: 719 - 6 roots = 713 across 31 levels
            # Average: 713 / 31 ≈ 23 nodes per level
            num_nodes = 23  # Default 23 nodes per level
            
            # Ensure we don't exceed 719 total
            if node_id + num_nodes > 719:
                num_nodes = 719 - node_id + 1
            
            for i in range(num_nodes):
                if node_id > 719:
                    break
                
                # Connect to parent nodes in previous level
                parent_nodes = self._get_parent_nodes(node_id, level)
                
                # Create node
                self._add_node(
                    number=node_id,
                    name=f"{node_type.value} {node_id}",
                    level=level,
                    realm=realm,
                    node_type=node_type,
                    description=f"Level {level} {node_type.value} in {realm.value}",
                    parent_nodes=parent_nodes,
                    attributes={
                        'depth': level,
                        'branch_factor': len(parent_nodes)
                    }
                )
                
                # Update parent nodes with this child
                for parent_id in parent_nodes:
                    if parent_id in self.nodes:
                        self.nodes[parent_id].child_nodes.append(node_id)
                
                node_id += 1
            
            if node_id > 719:
                break
        
        self.logger.info(f"✓ Created {len(self.nodes)} nodes across 31 levels")
        self._verify_structure()
    
    def _add_node(self, number: int, name: str, level: int, realm: WorldTreeRealm,
                  node_type: NodeType, description: str, parent_nodes: List[int],
                  attributes: Dict[str, Any] = None):
        """Add a node to the tree"""
        node = WorldTreeNode(
            number=number,
            name=name,
            level=level,
            realm=realm,
            node_type=node_type,
            description=description,
            parent_nodes=parent_nodes,
            child_nodes=[],
            energy=1.0,
            resonance=0.0,
            attributes=attributes or {}
        )
        self.nodes[number] = node
    
    def _get_parent_nodes(self, node_id: int, level: int) -> List[int]:
        """Get parent nodes for a new node"""
        if level == 0:
            return []  # Root nodes have no parents
        
        if level == 1:
            # Level 1 connects to all 6 roots
            return list(range(1, 7))
        
        # Find nodes in previous level
        prev_level_nodes = [n.number for n in self.nodes.values() if n.level == level - 1]
        
        if not prev_level_nodes:
            return []
        
        # Connect to 2-3 parent nodes (branching factor)
        num_parents = min(3, len(prev_level_nodes))
        
        # Use deterministic selection based on node_id
        np.random.seed(node_id)
        parents = np.random.choice(prev_level_nodes, size=num_parents, replace=False)
        
        return sorted(parents.tolist())
    
    def _verify_structure(self):
        """Verify the tree structure"""
        # Verify total count
        assert len(self.nodes) == 719, f"Expected 719 nodes, got {len(self.nodes)}"
        
        # Verify root nodes
        roots = [n for n in self.nodes.values() if n.node_type == NodeType.ROOT]
        assert len(roots) == 6, f"Expected 6 roots, got {len(roots)}"
        
        # Verify levels
        max_level = max(n.level for n in self.nodes.values())
        assert max_level == 31, f"Expected max level 31, got {max_level}"
        
        # Verify factorization: 719 = (31)(23)+6
        assert 719 == 31 * 23 + 6, "Factorization check failed"
        
        # Verify alternate factorization: 719 = (5)(11)(13)+4
        assert 719 == 5 * 11 * 13 + 4, "Alternate factorization check failed"
        
        self.logger.info("✓ Tree structure verified")
    
    def get_node(self, number: int) -> Optional[WorldTreeNode]:
        """Get a specific node by number"""
        return self.nodes.get(number)
    
    def get_nodes_by_level(self, level: int) -> List[WorldTreeNode]:
        """Get all nodes at a specific level"""
        return [n for n in self.nodes.values() if n.level == level]
    
    def get_nodes_by_realm(self, realm: WorldTreeRealm) -> List[WorldTreeNode]:
        """Get all nodes in a realm"""
        return [n for n in self.nodes.values() if n.realm == realm]
    
    def get_root_nodes(self) -> List[WorldTreeNode]:
        """Get the 6 primordial root nodes"""
        return [n for n in self.nodes.values() if n.node_type == NodeType.ROOT]
    
    def traverse_from_root(self, root_number: int, max_depth: int = 10) -> List[WorldTreeNode]:
        """
        Traverse the tree from a root node
        
        Args:
            root_number: Root node number (1-6)
            max_depth: Maximum depth to traverse
            
        Returns:
            List of nodes in traversal order
        """
        if root_number < 1 or root_number > 6:
            raise ValueError(f"Root number must be 1-6, got {root_number}")
        
        visited = set()
        traversal = []
        queue = [(root_number, 0)]
        
        while queue:
            node_num, depth = queue.pop(0)
            
            if node_num in visited or depth > max_depth:
                continue
            
            visited.add(node_num)
            node = self.get_node(node_num)
            if node:
                traversal.append(node)
                
                # Add child nodes
                for child_num in node.child_nodes:
                    if child_num not in visited:
                        queue.append((child_num, depth + 1))
        
        return traversal
    
    def find_path(self, start: int, end: int) -> Optional[List[WorldTreeNode]]:
        """
        Find path between two nodes
        
        Args:
            start: Starting node number
            end: Ending node number
            
        Returns:
            Path as list of nodes, or None if no path exists
        """
        if start not in self.nodes or end not in self.nodes:
            return None
        
        # BFS to find shortest path
        visited = set()
        queue = [(start, [start])]
        
        while queue:
            node_num, path = queue.pop(0)
            
            if node_num == end:
                return [self.get_node(n) for n in path]
            
            if node_num in visited:
                continue
            
            visited.add(node_num)
            node = self.get_node(node_num)
            
            if node:
                # Check both parents and children
                neighbors = node.parent_nodes + node.child_nodes
                for neighbor in neighbors:
                    if neighbor not in visited:
                        queue.append((neighbor, path + [neighbor]))
        
        return None
    
    def flow_energy(self, source_node: int, amount: float):
        """
        Flow energy from a source node through the tree
        
        Args:
            source_node: Source node number
            amount: Amount of energy to flow
        """
        node = self.get_node(source_node)
        if not node:
            return
        
        # Energy flows to children
        node.energy += amount
        
        if node.child_nodes:
            # Distribute energy among children
            energy_per_child = amount / len(node.child_nodes)
            for child_num in node.child_nodes:
                self.flow_energy(child_num, energy_per_child * 0.9)  # 10% loss
    
    def calculate_resonance(self, node1: int, node2: int) -> float:
        """
        Calculate resonance between two nodes
        
        Args:
            node1: First node number
            node2: Second node number
            
        Returns:
            Resonance value (0-1)
        """
        n1 = self.get_node(node1)
        n2 = self.get_node(node2)
        
        if not n1 or not n2:
            return 0.0
        
        # Resonance based on:
        # 1. Level proximity
        level_diff = abs(n1.level - n2.level)
        level_resonance = 1.0 / (1.0 + level_diff)
        
        # 2. Realm compatibility
        realm_resonance = 1.0 if n1.realm == n2.realm else 0.5
        
        # 3. Path distance
        path = self.find_path(node1, node2)
        path_resonance = 1.0 / (1.0 + len(path)) if path else 0.0
        
        # Combined resonance
        resonance = (level_resonance + realm_resonance + path_resonance) / 3.0
        
        return resonance
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about the World Tree"""
        realm_counts = {}
        for node in self.nodes.values():
            realm = node.realm.value
            realm_counts[realm] = realm_counts.get(realm, 0) + 1
        
        type_counts = {}
        for node in self.nodes.values():
            node_type = node.node_type.value
            type_counts[node_type] = type_counts.get(node_type, 0) + 1
        
        return {
            'total_nodes': len(self.nodes),
            'root_nodes': 6,
            'levels': 31,
            'avg_nodes_per_level': (719 - 6) / 31,
            'realms': len(set(n.realm for n in self.nodes.values())),
            'realm_distribution': realm_counts,
            'node_types': len(set(n.node_type for n in self.nodes.values())),
            'type_distribution': type_counts,
            'factorization': '(31)(23)+6 = 31 levels × 23 nodes + 6 roots',
            'alternate_factorization': '(5)(11)(13)+4',
            'a000081_order': 9,
            'ennead_level': 'Λ³ Adaptation',
            'symbolism': 'Axis Mundi - Complete model of continuous creation'
        }
    
    def visualize_level(self, level: int) -> str:
        """
        Create a text visualization of a level
        
        Args:
            level: Level to visualize (0-31)
            
        Returns:
            Text visualization
        """
        nodes = self.get_nodes_by_level(level)
        
        viz = f"\n=== Level {level} ({len(nodes)} nodes) ===\n"
        
        for node in nodes[:10]:  # Show first 10
            parent_str = f"← {len(node.parent_nodes)} parents" if node.parent_nodes else "ROOT"
            child_str = f"→ {len(node.child_nodes)} children" if node.child_nodes else "LEAF"
            viz += f"  [{node.number}] {node.name} {parent_str} {child_str}\n"
        
        if len(nodes) > 10:
            viz += f"  ... and {len(nodes) - 10} more nodes\n"
        
        return viz
