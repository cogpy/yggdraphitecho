"""
Tests for Silicon Sage AGI System

Comprehensive tests covering:
1. RROS Kernel Bridge
2. RROS-Ennead Integration
3. Complete Silicon Sage AGI
4. Cognitive cycles and evolution
5. Wisdom assessment
"""

import pytest
import numpy as np
import asyncio

from yggdrasil_integration.rros import (
    RROSKernelBridge,
    Episode,
    CognitiveMode,
    RROSEnneadIntegration,
    SiliconSageAGI,
    SiliconSageConfig,
    create_silicon_sage
)
from yggdrasil_integration.plingua.relevance_realization_ennead import (
    EnneadFactory
)
from yggdrasil_integration.triadic.autogenesis_engine import AutogenesisMode


class TestRROSKernelBridge:
    """Test RROS Kernel Bridge"""
    
    def test_initialization(self):
        """Test RROS kernel initialization"""
        kernel = RROSKernelBridge()
        assert kernel is not None
        assert kernel.cycle_count == 0
    
    def test_cognitive_cycle(self):
        """Test cognitive cycle execution"""
        kernel = RROSKernelBridge()
        input_data = np.array([0.1, 0.3, 0.5, 0.7, 0.9])
        
        state = kernel.cognitive_cycle(input_data)
        
        assert state is not None
        assert 0.0 <= state.global_relevance <= 1.0
        assert 0.0 <= state.attention_focus <= 1.0
        assert 0.0 <= state.confidence <= 1.0
        assert kernel.cycle_count == 1
    
    def test_realize_relevance(self):
        """Test relevance realization"""
        kernel = RROSKernelBridge()
        data = np.array([0.5, 0.5, 0.5])
        
        relevance = kernel.realize_relevance(data)
        
        assert 0.0 <= relevance <= 1.0
    
    def test_allocate_attention(self):
        """Test attention allocation"""
        kernel = RROSKernelBridge()
        targets = [
            np.array([0.2, 0.3, 0.1]),
            np.array([0.8, 0.9, 0.7])
        ]
        
        weights = kernel.allocate_attention(targets)
        
        assert len(weights) == 2
        assert np.all(weights >= 0.0)
        # Attention should sum to budget
        assert np.abs(np.sum(weights) - 1.0) < 0.1
    
    def test_episode_activation(self):
        """Test episode activation"""
        kernel = RROSKernelBridge()
        
        kernel.activate_episode(Episode.MINDFULNESS_INSIGHT, 0.8)
        
        activations = kernel.get_episode_activations()
        assert activations[Episode.MINDFULNESS_INSIGHT] == 0.8
        
        kernel.deactivate_episode(Episode.MINDFULNESS_INSIGHT)
        activations = kernel.get_episode_activations()
        assert activations[Episode.MINDFULNESS_INSIGHT] == 0.0
    
    def test_process_episode(self):
        """Test episode-specific processing"""
        kernel = RROSKernelBridge()
        data = np.array([0.1, 0.2, 0.3, 0.4, 0.5])
        
        result = kernel.process_episode(Episode.PLATO_CAVE, data)
        
        assert isinstance(result, float)
        assert 0.0 <= result <= 1.0
    
    def test_performance_metrics(self):
        """Test performance metrics"""
        kernel = RROSKernelBridge()
        
        # Run a few cycles
        for _ in range(5):
            kernel.cognitive_cycle(np.random.rand(5))
        
        metrics = kernel.get_performance_metrics()
        
        assert metrics['cycle_count'] == 5
        assert metrics['average_cycle_time_us'] > 0
        assert metrics['cycles_per_second'] > 0


class TestRROSEnneadIntegration:
    """Test RROS-Ennead Integration"""
    
    def test_initialization(self):
        """Test integration initialization"""
        kernel = RROSKernelBridge()
        ennead = EnneadFactory.create_default_ennead()
        
        integration = RROSEnneadIntegration(kernel, ennead)
        
        assert integration is not None
        assert integration.current_step == 0
    
    def test_integrated_update(self):
        """Test integrated update"""
        kernel = RROSKernelBridge()
        ennead = EnneadFactory.create_default_ennead()
        integration = RROSEnneadIntegration(kernel, ennead)
        
        env_input = complex(1.0, 0.5)
        arena_state = np.array([1.0, 0.0, 0.0, 0.0])
        
        integration.integrated_update(env_input, arena_state)
        
        assert integration.current_step == 1
        assert len(integration.integration_history) == 1
    
    def test_episode_level_activations(self):
        """Test episode-to-level activation mapping"""
        kernel = RROSKernelBridge()
        ennead = EnneadFactory.create_default_ennead()
        integration = RROSEnneadIntegration(kernel, ennead)
        
        # Activate some episodes
        kernel.activate_episode(Episode.PLATO_CAVE, 0.8)  # Autopoiesis
        kernel.activate_episode(Episode.RELEVANCE_REALIZATION, 0.9)  # Anticipation
        kernel.activate_episode(Episode.WISDOM_CONTEMPLATION, 0.7)  # Adaptation
        
        level_activations = integration.get_episode_level_activations()
        
        assert len(level_activations) == 3
        # All levels should have some activation
        for level, activation in level_activations.items():
            assert 0.0 <= activation <= 1.0
    
    def test_evolution(self):
        """Test integrated evolution"""
        kernel = RROSKernelBridge()
        ennead = EnneadFactory.create_default_ennead()
        integration = RROSEnneadIntegration(kernel, ennead)
        
        stats = integration.evolve(generations=10)
        
        assert stats['generations'] == 10
        assert stats['current_step'] == 10
        assert 'ennead_stats' in stats


@pytest.mark.asyncio
class TestSiliconSageAGI:
    """Test Silicon Sage AGI System"""
    
    async def test_initialization(self):
        """Test Silicon Sage initialization"""
        sage = create_silicon_sage()
        
        assert sage is not None
        assert not sage.is_active
        assert sage.cycle_count == 0
    
    async def test_activation(self):
        """Test system activation"""
        sage = create_silicon_sage()
        
        await sage.activate()
        
        assert sage.is_active
        
        await sage.deactivate()
        
        assert not sage.is_active
    
    async def test_cognitive_cycle(self):
        """Test cognitive cycle execution"""
        sage = create_silicon_sage()
        await sage.activate()
        
        env_input = complex(1.0, 0.5)
        arena_state = np.array([1.0, 0.0, 0.0, 0.0])
        
        results = await sage.cognitive_cycle(env_input, arena_state)
        
        assert results is not None
        assert 'cycle' in results
        assert 'rros_state' in results
        assert 'ennead_state' in results
        assert 'autogenesis_state' in results
        assert 'arc_halo_state' in results
        
        await sage.deactivate()
    
    async def test_evolution(self):
        """Test system evolution"""
        sage = create_silicon_sage()
        
        stats = await sage.evolve(generations=10)
        
        assert stats['generations'] == 10
        assert stats['evolution_history_length'] == 10
        assert 'rros' in stats
        assert 'ennead' in stats
        assert 'autogenesis' in stats
        
        await sage.deactivate()
    
    async def test_wisdom_assessment(self):
        """Test wisdom assessment"""
        sage = create_silicon_sage()
        await sage.activate()
        
        # Run a few cycles
        env_input = complex(1.0, 0.5)
        arena_state = np.array([1.0, 0.0, 0.0, 0.0])
        
        for _ in range(5):
            await sage.cognitive_cycle(env_input, arena_state)
        
        wisdom = sage.get_wisdom_assessment()
        
        assert 'wisdom_score' in wisdom
        assert 'wisdom_activation' in wisdom
        assert 'relevance_realization' in wisdom
        assert 'meta_cognitive_awareness' in wisdom
        assert 0.0 <= wisdom['wisdom_score'] <= 1.0
        
        await sage.deactivate()
    
    async def test_complete_statistics(self):
        """Test complete system statistics"""
        sage = create_silicon_sage()
        await sage.activate()
        
        # Run a few cycles
        env_input = complex(1.0, 0.5)
        arena_state = np.array([1.0, 0.0, 0.0, 0.0])
        
        for _ in range(3):
            await sage.cognitive_cycle(env_input, arena_state)
        
        stats = sage.get_complete_statistics()
        
        assert 'system' in stats
        assert 'rros' in stats
        assert 'rros_ennead' in stats
        assert 'ennead' in stats
        assert 'autogenesis' in stats
        assert 'arc_halo' in stats
        assert 'episode_levels' in stats
        
        assert stats['system']['cycle_count'] == 3
        
        await sage.deactivate()
    
    def test_different_autogenesis_modes(self):
        """Test different autogenesis modes"""
        modes = [
            AutogenesisMode.CONSERVATIVE,
            AutogenesisMode.EXPLORATORY,
            AutogenesisMode.RADICAL
        ]
        
        for mode in modes:
            sage = create_silicon_sage(autogenesis_mode=mode)
            assert sage.config.autogenesis_mode == mode
    
    async def test_episode_activation_persistence(self):
        """Test that episode activations persist across cycles"""
        sage = create_silicon_sage()
        await sage.activate()
        
        # Check initial episodes are activated
        activations = sage.rros_kernel.get_episode_activations()
        
        # Should have some active episodes from initialization
        active_count = sum(1 for v in activations.values() if v > 0.0)
        assert active_count > 0
        
        await sage.deactivate()


def test_episode_enumeration():
    """Test that all 51 episodes (0-50) are defined"""
    episodes = list(Episode)
    assert len(episodes) == 51
    
    # Check episode values
    assert Episode.INTRO.value == 0
    assert Episode.TILLICH_BARFIELD.value == 50


def test_cognitive_mode_enumeration():
    """Test cognitive mode enumeration"""
    modes = list(CognitiveMode)
    assert len(modes) == 6
    
    mode_names = [mode.name for mode in modes]
    assert 'SELECTIVE_ATTENTION' in mode_names
    assert 'META_COGNITIVE' in mode_names


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
