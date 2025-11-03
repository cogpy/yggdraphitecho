"""
Tests for Design Systems Integration

Comprehensive tests covering:
1. Design Systems Correspondence
2. Schell's 115 Game Design Lenses
3. Alexander's 286 Architectural Patterns
4. Axis Mundi 719 World Tree
5. A000081 Order 7-9 correspondence
"""

import pytest
import numpy as np

from yggdrasil_integration.triadic.design_systems_correspondence import (
    DesignSystemsCorrespondence, DesignSystem
)
from yggdrasil_integration.triadic.schell_lenses import (
    SchellLensSystem, LensCategory
)
from yggdrasil_integration.triadic.alexander_patterns import (
    AlexanderPatternLanguage, PatternScale
)
from yggdrasil_integration.triadic.axis_mundi import (
    AxisMundiWorldTree, WorldTreeRealm, NodeType
)
from yggdrasil_integration.triadic.a000081_correspondence import (
    A000081TriadicSystem
)


class TestDesignSystemsCorrespondence:
    """Test Design Systems Correspondence"""
    
    def test_initialization(self):
        """Test correspondence initialization"""
        triadic = A000081TriadicSystem(max_order=9)
        correspondence = DesignSystemsCorrespondence(triadic)
        
        assert correspondence is not None
        assert correspondence.triadic is not None
    
    def test_a000081_verification(self):
        """Test A000081 correspondence verification"""
        from yggdrasil_integration.triadic.a000081_correspondence import A000081
        
        # Verify orders 7-9
        order_7 = A000081[8]  # Order 7 at index 8
        order_8 = A000081[9]  # Order 8 at index 9
        order_9 = A000081[10]  # Order 9 at index 10
        
        assert order_7 == 115, f"Order 7 should be 115, got {order_7}"
        assert order_8 == 286, f"Order 8 should be 286, got {order_8}"
        assert order_9 == 719, f"Order 9 should be 719, got {order_9}"
    
    def test_factorizations(self):
        """Test factorizations of 115, 286, 719"""
        # 115 = (5)(23)
        assert 115 == 5 * 23
        assert 115 == 2 * 5 * 11 + 5
        
        # 286 = (11)(26) = 253+33
        assert 286 == 11 * 26
        assert 286 == 2 * 11 * 13
        assert 286 == 253 + 33
        
        # 719 = (31)(23)+6
        assert 719 == 31 * 23 + 6
        assert 719 == 5 * 11 * 13 + 4
    
    def test_adaptation_level_mapping(self):
        """Test adaptation level mapping"""
        triadic = A000081TriadicSystem(max_order=9)
        correspondence = DesignSystemsCorrespondence(triadic)
        
        mapping = correspondence.get_adaptation_level_mapping()
        
        assert mapping[7] == DesignSystem.SCHELL_LENSES
        assert mapping[8] == DesignSystem.ALEXANDER_PATTERNS
        assert mapping[9] == DesignSystem.AXIS_MUNDI
    
    def test_complete_correspondence(self):
        """Test complete correspondence structure"""
        triadic = A000081TriadicSystem(max_order=9)
        correspondence = DesignSystemsCorrespondence(triadic)
        
        complete = correspondence.get_complete_correspondence()
        
        assert 'autopoiesis' in complete
        assert 'anticipation' in complete
        assert 'adaptation' in complete
        
        # Check Adaptation level
        adaptation = complete['adaptation']
        assert adaptation['orders'] == [7, 8, 9]
        assert adaptation['a000081'] == [115, 286, 719]
        assert 'design_systems' in adaptation


class TestSchellLensSystem:
    """Test Schell's 115 Game Design Lenses"""
    
    def test_initialization(self):
        """Test lens system initialization"""
        system = SchellLensSystem()
        
        assert len(system.lenses) == 115
    
    def test_lens_categories(self):
        """Test lens categories"""
        system = SchellLensSystem()
        
        categories = set(lens.category for lens in system.lenses.values())
        assert len(categories) > 0
        assert LensCategory.ESSENTIAL_EXPERIENCE in categories
        assert LensCategory.HIDDEN in categories
    
    def test_hidden_lenses(self):
        """Test hidden lenses"""
        system = SchellLensSystem()
        
        hidden = system.get_hidden_lenses()
        assert len(hidden) == 2
        assert all(lens.is_hidden for lens in hidden)
        assert all(lens.number >= 114 for lens in hidden)
    
    def test_get_lens(self):
        """Test getting specific lens"""
        system = SchellLensSystem()
        
        lens1 = system.get_lens(1)
        assert lens1 is not None
        assert lens1.number == 1
        assert lens1.name == "Essential Experience"
        
        lens115 = system.get_lens(115)
        assert lens115 is not None
        assert lens115.is_hidden
    
    def test_apply_lens(self):
        """Test applying a lens"""
        system = SchellLensSystem()
        
        context = {'experience': 'game design', 'goal': 'fun'}
        analysis = system.apply_lens(1, context)
        
        assert 'lens' in analysis
        assert 'context' in analysis
        assert 'questions' in analysis
        assert 'insights' in analysis
    
    def test_apply_multiple_lenses(self):
        """Test applying multiple lenses"""
        system = SchellLensSystem()
        
        context = {'experience': 'game design'}
        analysis = system.apply_multiple_lenses([1, 2, 3], context)
        
        assert analysis['lenses_applied'] == 3
        assert len(analysis['analyses']) == 3
        assert 'synthesized_insights' in analysis
    
    def test_statistics(self):
        """Test lens system statistics"""
        system = SchellLensSystem()
        
        stats = system.get_statistics()
        
        assert stats['total_lenses'] == 115
        assert stats['published_lenses'] == 113
        assert stats['hidden_lenses'] == 2
        assert stats['a000081_order'] == 7
        assert stats['ennead_level'] == 'Λ³ Adaptation'


class TestAlexanderPatternLanguage:
    """Test Alexander's 286 Architectural Patterns"""
    
    def test_initialization(self):
        """Test pattern language initialization"""
        language = AlexanderPatternLanguage()
        
        assert len(language.patterns) == 286
    
    def test_pattern_scales(self):
        """Test pattern scales"""
        language = AlexanderPatternLanguage()
        
        scales = set(pattern.scale for pattern in language.patterns.values())
        assert len(scales) > 0
        assert PatternScale.REGIONS in scales
        assert PatternScale.CIVIC_ANGEL in scales
    
    def test_civic_angel_patterns(self):
        """Test civic angel patterns"""
        language = AlexanderPatternLanguage()
        
        civic = language.get_civic_angel_patterns()
        assert len(civic) == 33
        assert all(pattern.is_civic_angel for pattern in civic)
        assert all(pattern.number > 253 for pattern in civic)
    
    def test_get_pattern(self):
        """Test getting specific pattern"""
        language = AlexanderPatternLanguage()
        
        pattern1 = language.get_pattern(1)
        assert pattern1 is not None
        assert pattern1.number == 1
        assert pattern1.name == "Independent Regions"
        
        pattern254 = language.get_pattern(254)
        assert pattern254 is not None
        assert pattern254.is_civic_angel
    
    def test_apply_pattern(self):
        """Test applying a pattern"""
        language = AlexanderPatternLanguage()
        
        context = {'scale': 'buildings', 'goal': 'community'}
        application = language.apply_pattern(12, context)
        
        assert 'pattern' in application
        assert 'context' in application
        assert 'problem' in application
        assert 'solution' in application
        assert 'recommendations' in application
    
    def test_pattern_sequence(self):
        """Test creating pattern sequence"""
        language = AlexanderPatternLanguage()
        
        sequence = language.create_pattern_sequence(1, "create community")
        
        assert len(sequence) > 0
        assert sequence[0].number == 1
    
    def test_statistics(self):
        """Test pattern language statistics"""
        language = AlexanderPatternLanguage()
        
        stats = language.get_statistics()
        
        assert stats['total_patterns'] == 286
        assert stats['main_patterns'] == 253
        assert stats['civic_angel_patterns'] == 33
        assert stats['a000081_order'] == 8
        assert stats['ennead_level'] == 'Λ³ Adaptation'


class TestAxisMundiWorldTree:
    """Test Axis Mundi 719 World Tree"""
    
    def test_initialization(self):
        """Test World Tree initialization"""
        tree = AxisMundiWorldTree()
        
        assert len(tree.nodes) == 719
    
    def test_root_nodes(self):
        """Test root nodes"""
        tree = AxisMundiWorldTree()
        
        roots = tree.get_root_nodes()
        assert len(roots) == 6
        assert all(node.node_type == NodeType.ROOT for node in roots)
        assert all(node.level == 0 for node in roots)
    
    def test_tree_levels(self):
        """Test tree levels"""
        tree = AxisMundiWorldTree()
        
        # Check all levels 0-31 exist
        for level in range(32):
            nodes = tree.get_nodes_by_level(level)
            assert len(nodes) > 0, f"Level {level} should have nodes"
    
    def test_tree_realms(self):
        """Test tree realms"""
        tree = AxisMundiWorldTree()
        
        realms = set(node.realm for node in tree.nodes.values())
        assert WorldTreeRealm.ROOT_REALM in realms
        assert WorldTreeRealm.LOWER_WORLD in realms
        assert WorldTreeRealm.MIDDLE_WORLD in realms
        assert WorldTreeRealm.UPPER_WORLD in realms
    
    def test_get_node(self):
        """Test getting specific node"""
        tree = AxisMundiWorldTree()
        
        node1 = tree.get_node(1)
        assert node1 is not None
        assert node1.number == 1
        assert node1.node_type == NodeType.ROOT
        
        node719 = tree.get_node(719)
        assert node719 is not None
    
    def test_traverse_from_root(self):
        """Test traversing from root"""
        tree = AxisMundiWorldTree()
        
        traversal = tree.traverse_from_root(1, max_depth=5)
        
        assert len(traversal) > 0
        assert traversal[0].number == 1
    
    def test_find_path(self):
        """Test finding path between nodes"""
        tree = AxisMundiWorldTree()
        
        path = tree.find_path(1, 10)
        
        assert path is not None
        assert len(path) > 0
        assert path[0].number == 1
    
    def test_energy_flow(self):
        """Test energy flow"""
        tree = AxisMundiWorldTree()
        
        initial_energy = tree.get_node(1).energy
        tree.flow_energy(1, 10.0)
        final_energy = tree.get_node(1).energy
        
        assert final_energy > initial_energy
    
    def test_resonance(self):
        """Test resonance calculation"""
        tree = AxisMundiWorldTree()
        
        resonance = tree.calculate_resonance(1, 10)
        
        assert 0.0 <= resonance <= 1.0
    
    def test_statistics(self):
        """Test World Tree statistics"""
        tree = AxisMundiWorldTree()
        
        stats = tree.get_statistics()
        
        assert stats['total_nodes'] == 719
        assert stats['root_nodes'] == 6
        assert stats['levels'] == 31
        assert stats['a000081_order'] == 9
        assert stats['ennead_level'] == 'Λ³ Adaptation'
    
    def test_visualize_level(self):
        """Test level visualization"""
        tree = AxisMundiWorldTree()
        
        viz = tree.visualize_level(0)
        
        assert isinstance(viz, str)
        assert "Level 0" in viz


class TestIntegratedDesignSystems:
    """Test integrated design systems"""
    
    def test_all_systems_initialized(self):
        """Test all systems can be initialized together"""
        triadic = A000081TriadicSystem(max_order=9)
        correspondence = DesignSystemsCorrespondence(triadic)
        schell = SchellLensSystem()
        alexander = AlexanderPatternLanguage()
        axis_mundi = AxisMundiWorldTree()
        
        assert len(schell.lenses) == 115
        assert len(alexander.patterns) == 286
        assert len(axis_mundi.nodes) == 719
    
    def test_correspondence_counts_match(self):
        """Test that correspondence counts match system counts"""
        from yggdrasil_integration.triadic.a000081_correspondence import A000081
        
        order_7 = A000081[8]  # Order 7 at index 8
        order_8 = A000081[9]  # Order 8 at index 9
        order_9 = A000081[10]  # Order 9 at index 10
        
        schell = SchellLensSystem()
        alexander = AlexanderPatternLanguage()
        axis_mundi = AxisMundiWorldTree()
        
        assert order_7 == len(schell.lenses)
        assert order_8 == len(alexander.patterns)
        assert order_9 == len(axis_mundi.nodes)
    
    def test_adaptation_level_integration(self):
        """Test Adaptation level integration"""
        triadic = A000081TriadicSystem(max_order=9)
        correspondence = DesignSystemsCorrespondence(triadic)
        
        # Initialize all design systems
        correspondence.initialize_schell_lenses()
        correspondence.initialize_alexander_patterns()
        correspondence.initialize_axis_mundi()
        
        assert len(correspondence.schell_lenses) == 115
        assert len(correspondence.alexander_patterns) == 286
        assert len(correspondence.axis_mundi_nodes) == 719


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
