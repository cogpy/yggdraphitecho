import pytest
import os
from unittest.mock import Mock, MagicMock, patch
from yggdrasil_integration.fusion.arc_halo_db_integration import (
    EnhancedArcHaloFusionCore, ArcHaloDatabase, ReactorConfig,
    ReactorType, FusionStrategy, InteractionType
)
from yggdrasil_integration.membranes.yggdrasil_membrane import (
    MembraneReservoir, YggdrasilMembrane, MembraneType
)
from yggdrasil_integration.bridge.aphrodite_bridge import AphroditeBridge
from yggdrasil_integration.fusion.arc_halo_fusion_core import IdentityAspect


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


def test_reactor_config():
    """Test ReactorConfig creation"""
    config = ReactorConfig(
        reactor_name="test_reactor",
        reactor_type=ReactorType.HIERARCHICAL,
        fusion_strategy=FusionStrategy.DYNAMIC,
        config={"test": "value"},
        metadata={"version": "1.0"}
    )
    
    assert config.reactor_name == "test_reactor"
    assert config.reactor_type == ReactorType.HIERARCHICAL
    assert config.fusion_strategy == FusionStrategy.DYNAMIC
    assert config.config["test"] == "value"
    assert config.metadata["version"] == "1.0"


def test_enhanced_fusion_core_without_database(reservoir, bridge):
    """Test EnhancedArcHaloFusionCore without database"""
    fusion_core = EnhancedArcHaloFusionCore(
        name="test_core",
        reservoir=reservoir,
        bridge=bridge,
        database=None,
        reactor_config=None
    )
    
    assert fusion_core is not None
    assert fusion_core.reactor_id is None
    assert fusion_core.database is None


@pytest.mark.asyncio
async def test_fusion_cycle_without_database(reservoir, bridge):
    """Test fusion cycle without database persistence"""
    fusion_core = EnhancedArcHaloFusionCore(
        name="test_core",
        reservoir=reservoir,
        bridge=bridge,
        database=None,
        reactor_config=None
    )
    
    fusion_core.activate()
    await fusion_core.fusion_cycle()
    
    assert fusion_core.fusion_cycles == 1


@patch('yggdrasil_integration.fusion.arc_halo_db_integration.PSYCOPG2_AVAILABLE', True)
@patch('yggdrasil_integration.fusion.arc_halo_db_integration.Json', lambda x: x)
@patch('yggdrasil_integration.fusion.arc_halo_db_integration.SimpleConnectionPool')
def test_database_connection_mock(mock_pool_class, reservoir, bridge):
    """Test database connection with mocked psycopg2"""
    # Mock the connection pool
    mock_pool = MagicMock()
    mock_pool_class.return_value = mock_pool
    
    # Mock connection
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_pool.getconn.return_value = mock_conn
    
    # Mock cursor execute and fetchone
    mock_cursor.fetchone.return_value = ["test-reactor-id"]
    
    # Create database with connection string
    database = ArcHaloDatabase(connection_string="postgresql://test")
    
    # Create reactor config
    reactor_config = ReactorConfig(
        reactor_name="test_reactor",
        reactor_type=ReactorType.HIERARCHICAL,
        fusion_strategy=FusionStrategy.DYNAMIC
    )
    
    # Create reactor
    reactor_id = database.create_reactor(reactor_config)
    
    assert reactor_id == "test-reactor-id"
    assert mock_cursor.execute.called


@patch('yggdrasil_integration.fusion.arc_halo_db_integration.PSYCOPG2_AVAILABLE', True)
@patch('yggdrasil_integration.fusion.arc_halo_db_integration.Json', lambda x: x)
@patch('yggdrasil_integration.fusion.arc_halo_db_integration.SimpleConnectionPool')
def test_enhanced_fusion_core_with_mocked_database(mock_pool_class, reservoir, bridge):
    """Test EnhancedArcHaloFusionCore with mocked database"""
    # Mock the connection pool
    mock_pool = MagicMock()
    mock_pool_class.return_value = mock_pool
    
    # Mock connection
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_pool.getconn.return_value = mock_conn
    
    # Mock cursor execute and fetchone
    mock_cursor.fetchone.return_value = ["test-reactor-id"]
    
    # Create database
    database = ArcHaloDatabase(connection_string="postgresql://test")
    
    # Create reactor config
    reactor_config = ReactorConfig(
        reactor_name="test_reactor",
        reactor_type=ReactorType.HIERARCHICAL,
        fusion_strategy=FusionStrategy.DYNAMIC
    )
    
    # Create enhanced fusion core
    fusion_core = EnhancedArcHaloFusionCore(
        name="test_core",
        reservoir=reservoir,
        bridge=bridge,
        database=database,
        reactor_config=reactor_config
    )
    
    assert fusion_core.reactor_id == "test-reactor-id"
    assert fusion_core.database is not None


def test_interaction_types():
    """Test InteractionType enum"""
    assert InteractionType.FEEDS_INTO.value == "feeds_into"
    assert InteractionType.VALIDATES.value == "validates"
    assert InteractionType.AUGMENTS.value == "augments"
    assert InteractionType.CORRECTS.value == "corrects"


def test_reactor_types():
    """Test ReactorType enum"""
    assert ReactorType.ENSEMBLE.value == "ensemble"
    assert ReactorType.CASCADE.value == "cascade"
    assert ReactorType.PARALLEL.value == "parallel"
    assert ReactorType.HIERARCHICAL.value == "hierarchical"


def test_fusion_strategies():
    """Test FusionStrategy enum"""
    assert FusionStrategy.WEIGHTED_AVERAGE.value == "weighted_average"
    assert FusionStrategy.VOTING.value == "voting"
    assert FusionStrategy.STACKING.value == "stacking"
    assert FusionStrategy.DYNAMIC.value == "dynamic"
