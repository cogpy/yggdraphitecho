"""
Arc-Halo Database Integration for Cognitive Fusion Reactor

This module integrates the Arc-Halo PostgreSQL database schema with the
Yggdrasil-based cognitive fusion reactor, enabling persistent storage of
model states, fusion operations, and cognitive states.
"""

import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import json
import uuid
from datetime import datetime, timezone
import os

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor, Json
    from psycopg2.pool import SimpleConnectionPool
    PSYCOPG2_AVAILABLE = True
except ImportError:
    psycopg2 = None
    RealDictCursor = None
    Json = None
    SimpleConnectionPool = None
    PSYCOPG2_AVAILABLE = False
    logging.warning("psycopg2 not installed. Install with: pip install psycopg2-binary")

from .arc_halo_fusion_core import (
    ArcHaloFusionCore, IdentityAspect, CognitiveState, MetaLearningRecord
)


class ReactorType(Enum):
    """Types of cognitive fusion reactors"""
    ENSEMBLE = "ensemble"
    CASCADE = "cascade"
    PARALLEL = "parallel"
    HIERARCHICAL = "hierarchical"


class FusionStrategy(Enum):
    """Fusion strategies for multi-model orchestration"""
    WEIGHTED_AVERAGE = "weighted_average"
    VOTING = "voting"
    STACKING = "stacking"
    DYNAMIC = "dynamic"


class InteractionType(Enum):
    """Types of model interactions"""
    FEEDS_INTO = "feeds_into"
    VALIDATES = "validates"
    AUGMENTS = "augments"
    CORRECTS = "corrects"


@dataclass
class ReactorConfig:
    """Configuration for a cognitive fusion reactor"""
    reactor_name: str
    reactor_type: ReactorType
    fusion_strategy: FusionStrategy
    config: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


class ArcHaloDatabase:
    """
    Database interface for Arc-Halo Cognitive Fusion Reactor
    
    This class provides methods for interacting with the PostgreSQL database
    to persist reactor state, fusion operations, and cognitive states.
    """
    
    def __init__(self, connection_string: Optional[str] = None):
        """
        Initialize database connection
        
        Args:
            connection_string: PostgreSQL connection string. If None, reads from
                             NEON_DATABASE_URL environment variable.
        """
        if not PSYCOPG2_AVAILABLE:
            raise ImportError("psycopg2 is required for database integration")
        
        self.connection_string = connection_string or os.getenv("NEON_DATABASE_URL")
        if not self.connection_string:
            raise ValueError(
                "Database connection string required. Set NEON_DATABASE_URL "
                "environment variable or pass connection_string parameter."
            )
        
        self.logger = logging.getLogger(f"{__name__}.ArcHaloDatabase")
        
        # Initialize connection pool
        self.pool = SimpleConnectionPool(
            minconn=1,
            maxconn=10,
            dsn=self.connection_string
        )
        
        self.logger.info("Initialized Arc-Halo database connection")
    
    def get_connection(self):
        """Get a connection from the pool"""
        return self.pool.getconn()
    
    def release_connection(self, conn):
        """Release a connection back to the pool"""
        self.pool.putconn(conn)
    
    def create_reactor(self, config: ReactorConfig) -> str:
        """
        Create a new cognitive fusion reactor
        
        Args:
            config: Reactor configuration
            
        Returns:
            Reactor ID (UUID)
        """
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO cognitive_fusion_reactors 
                    (reactor_name, reactor_type, fusion_strategy, config, metadata)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING reactor_id
                """, (
                    config.reactor_name,
                    config.reactor_type.value,
                    config.fusion_strategy.value,
                    Json(config.config),
                    Json(config.metadata)
                ))
                reactor_id = cur.fetchone()[0]
                conn.commit()
                
                self.logger.info(f"Created reactor: {config.reactor_name} ({reactor_id})")
                return str(reactor_id)
        finally:
            self.release_connection(conn)
    
    def add_model_to_reactor(self, reactor_id: str, model_id: str,
                            model_role: str = "primary",
                            weight: float = 1.0,
                            priority: int = 0) -> str:
        """
        Add a model to a reactor
        
        Args:
            reactor_id: Reactor UUID
            model_id: Model UUID
            model_role: Role of the model in the reactor
            weight: Fusion weight
            priority: Priority order
            
        Returns:
            Mapping ID (UUID)
        """
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO reactor_models 
                    (reactor_id, model_id, model_role, weight, priority)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING mapping_id
                """, (reactor_id, model_id, model_role, weight, priority))
                mapping_id = cur.fetchone()[0]
                conn.commit()
                
                self.logger.debug(f"Added model {model_id} to reactor {reactor_id}")
                return str(mapping_id)
        finally:
            self.release_connection(conn)
    
    def record_fusion_operation(self, reactor_id: str,
                               operation_type: str,
                               input_data: Dict[str, Any],
                               fusion_results: Dict[str, Any],
                               participating_models: List[str],
                               execution_time_ms: int) -> str:
        """
        Record a fusion operation
        
        Args:
            reactor_id: Reactor UUID
            operation_type: Type of operation (inference, training, evaluation)
            input_data: Input data for the operation
            fusion_results: Results from the fusion
            participating_models: List of model UUIDs
            execution_time_ms: Execution time in milliseconds
            
        Returns:
            Operation ID (UUID)
        """
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO fusion_operations 
                    (reactor_id, operation_type, input_data, fusion_results, 
                     participating_models, operation_status, completed_at, execution_time_ms)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING operation_id
                """, (
                    reactor_id,
                    operation_type,
                    Json(input_data),
                    Json(fusion_results),
                    participating_models,
                    'completed',
                    datetime.now(timezone.utc),
                    execution_time_ms
                ))
                operation_id = cur.fetchone()[0]
                conn.commit()
                
                self.logger.debug(f"Recorded fusion operation: {operation_id}")
                return str(operation_id)
        finally:
            self.release_connection(conn)
    
    def save_cognitive_state(self, reactor_id: str,
                            state_type: str,
                            state_data: Dict[str, Any],
                            priority: int = 0,
                            expires_at: Optional[datetime] = None) -> str:
        """
        Save cognitive state
        
        Args:
            reactor_id: Reactor UUID
            state_type: Type of state (context, memory, attention_focus, goal)
            state_data: State data
            priority: Priority level
            expires_at: Optional expiration timestamp
            
        Returns:
            State ID (UUID)
        """
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO cognitive_state 
                    (reactor_id, state_type, state_data, priority, expires_at)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING state_id
                """, (
                    reactor_id,
                    state_type,
                    Json(state_data),
                    priority,
                    expires_at
                ))
                state_id = cur.fetchone()[0]
                conn.commit()
                
                self.logger.debug(f"Saved cognitive state: {state_id}")
                return str(state_id)
        finally:
            self.release_connection(conn)
    
    def load_cognitive_state(self, reactor_id: str,
                            state_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Load cognitive states for a reactor
        
        Args:
            reactor_id: Reactor UUID
            state_type: Optional state type filter
            
        Returns:
            List of cognitive states
        """
        conn = self.get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                if state_type:
                    cur.execute("""
                        SELECT * FROM cognitive_state 
                        WHERE reactor_id = %s AND state_type = %s
                        AND (expires_at IS NULL OR expires_at > CURRENT_TIMESTAMP)
                        ORDER BY priority DESC, created_at DESC
                    """, (reactor_id, state_type))
                else:
                    cur.execute("""
                        SELECT * FROM cognitive_state 
                        WHERE reactor_id = %s
                        AND (expires_at IS NULL OR expires_at > CURRENT_TIMESTAMP)
                        ORDER BY priority DESC, created_at DESC
                    """, (reactor_id,))
                
                states = [dict(row) for row in cur.fetchall()]
                return states
        finally:
            self.release_connection(conn)
    
    def create_model_interaction(self, reactor_id: str,
                                 source_model_id: str,
                                 target_model_id: str,
                                 interaction_type: InteractionType,
                                 interaction_weight: float = 1.0,
                                 data_flow_config: Optional[Dict[str, Any]] = None) -> str:
        """
        Create a model interaction in the graph
        
        Args:
            reactor_id: Reactor UUID
            source_model_id: Source model UUID
            target_model_id: Target model UUID
            interaction_type: Type of interaction
            interaction_weight: Interaction weight
            data_flow_config: Optional data flow configuration
            
        Returns:
            Interaction ID (UUID)
        """
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO model_interaction_graph 
                    (reactor_id, source_model_id, target_model_id, interaction_type, 
                     interaction_weight, data_flow_config)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING interaction_id
                """, (
                    reactor_id,
                    source_model_id,
                    target_model_id,
                    interaction_type.value,
                    interaction_weight,
                    Json(data_flow_config or {})
                ))
                interaction_id = cur.fetchone()[0]
                conn.commit()
                
                self.logger.debug(f"Created model interaction: {interaction_id}")
                return str(interaction_id)
        finally:
            self.release_connection(conn)
    
    def get_reactor_status(self, reactor_id: str) -> Dict[str, Any]:
        """
        Get reactor status and statistics
        
        Args:
            reactor_id: Reactor UUID
            
        Returns:
            Reactor status dictionary
        """
        conn = self.get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                # Get reactor info
                cur.execute("""
                    SELECT * FROM cognitive_fusion_reactors 
                    WHERE reactor_id = %s
                """, (reactor_id,))
                reactor = dict(cur.fetchone())
                
                # Get model count
                cur.execute("""
                    SELECT COUNT(*) as model_count 
                    FROM reactor_models 
                    WHERE reactor_id = %s AND is_active = TRUE
                """, (reactor_id,))
                reactor['model_count'] = cur.fetchone()['model_count']
                
                # Get operation count
                cur.execute("""
                    SELECT COUNT(*) as operation_count 
                    FROM fusion_operations 
                    WHERE reactor_id = %s
                """, (reactor_id,))
                reactor['operation_count'] = cur.fetchone()['operation_count']
                
                # Get recent operations
                cur.execute("""
                    SELECT operation_type, operation_status, execution_time_ms
                    FROM fusion_operations 
                    WHERE reactor_id = %s
                    ORDER BY started_at DESC
                    LIMIT 10
                """, (reactor_id,))
                reactor['recent_operations'] = [dict(row) for row in cur.fetchall()]
                
                return reactor
        finally:
            self.release_connection(conn)
    
    def close(self):
        """Close all database connections"""
        if self.pool:
            self.pool.closeall()
            self.logger.info("Closed database connections")


class EnhancedArcHaloFusionCore(ArcHaloFusionCore):
    """
    Enhanced Arc-Halo Fusion Core with database persistence
    
    This class extends the base ArcHaloFusionCore with database integration
    for persistent storage of reactor state and fusion operations.
    """
    
    def __init__(self, 
                 name: str,
                 reservoir,
                 bridge,
                 database: Optional[ArcHaloDatabase] = None,
                 reactor_config: Optional[ReactorConfig] = None):
        """
        Initialize enhanced fusion core with database
        
        Args:
            name: Name of the fusion core
            reservoir: Membrane reservoir
            bridge: Aphrodite bridge
            database: Optional database connection
            reactor_config: Optional reactor configuration
        """
        super().__init__(name, reservoir, bridge)
        
        self.database = database
        self.reactor_id: Optional[str] = None
        
        # Create reactor in database if database is provided
        if self.database and reactor_config:
            self.reactor_id = self.database.create_reactor(reactor_config)
            self.logger.info(f"Created database reactor: {self.reactor_id}")
    
    async def fusion_cycle(self):
        """Execute fusion cycle with database persistence"""
        import time
        start_time = time.time()
        
        # Execute base fusion cycle
        await super().fusion_cycle()
        
        # Persist cognitive state to database
        if self.database and self.reactor_id:
            self._persist_cognitive_state()
        
        execution_time_ms = int((time.time() - start_time) * 1000)
        
        # Record fusion operation
        if self.database and self.reactor_id:
            self.database.record_fusion_operation(
                reactor_id=self.reactor_id,
                operation_type="fusion_cycle",
                input_data={"cycle": self.fusion_cycles},
                fusion_results=self.get_statistics(),
                participating_models=[],  # Would be populated with actual model IDs
                execution_time_ms=execution_time_ms
            )
    
    def _persist_cognitive_state(self):
        """Persist current cognitive state to database"""
        if not self.database or not self.reactor_id:
            return
        
        # Save attention focus
        if self.self_model.current_state.attention_focus:
            self.database.save_cognitive_state(
                reactor_id=self.reactor_id,
                state_type="attention_focus",
                state_data={
                    "focus_atoms": self.self_model.current_state.attention_focus,
                    "arousal": self.self_model.current_state.arousal_level,
                    "confidence": self.self_model.current_state.confidence_level
                },
                priority=1
            )
        
        # Save active goals
        if self.self_model.current_state.active_goals:
            self.database.save_cognitive_state(
                reactor_id=self.reactor_id,
                state_type="goal",
                state_data={
                    "goals": self.self_model.current_state.active_goals
                },
                priority=2
            )
        
        # Save identity summary
        identity_summary = self.self_model.get_identity_summary()
        self.database.save_cognitive_state(
            reactor_id=self.reactor_id,
            state_type="memory",
            state_data={
                "identity": identity_summary,
                "total_experiences": self.self_model.stats['total_experiences']
            },
            priority=0
        )
    
    def load_cognitive_state_from_db(self):
        """Load cognitive state from database"""
        if not self.database or not self.reactor_id:
            return
        
        # Load all cognitive states
        states = self.database.load_cognitive_state(self.reactor_id)
        
        for state in states:
            state_type = state['state_type']
            state_data = state['state_data']
            
            if state_type == "attention_focus":
                self.self_model.update_cognitive_state(
                    attention_focus=state_data.get('focus_atoms', []),
                    arousal_level=state_data.get('arousal', 0.5),
                    confidence_level=state_data.get('confidence', 0.5)
                )
            elif state_type == "goal":
                self.self_model.update_cognitive_state(
                    active_goals=state_data.get('goals', [])
                )
        
        self.logger.info(f"Loaded {len(states)} cognitive states from database")
    
    def get_reactor_status_from_db(self) -> Optional[Dict[str, Any]]:
        """Get reactor status from database"""
        if not self.database or not self.reactor_id:
            return None
        
        return self.database.get_reactor_status(self.reactor_id)
