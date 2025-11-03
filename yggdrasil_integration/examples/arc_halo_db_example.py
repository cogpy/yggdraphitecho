"""
Example: Enhanced Arc-Halo Cognitive Fusion Reactor with Database Integration

This example demonstrates how to use the enhanced Arc-Halo fusion core with
PostgreSQL database persistence for reactor state and fusion operations.
"""

import asyncio
import os
from yggdrasil_integration.membranes.yggdrasil_membrane import (
    MembraneReservoir, YggdrasilMembrane, MembraneType
)
from yggdrasil_integration.bridge.aphrodite_bridge import AphroditeBridge
from yggdrasil_integration.fusion.arc_halo_db_integration import (
    EnhancedArcHaloFusionCore, ArcHaloDatabase, ReactorConfig,
    ReactorType, FusionStrategy, InteractionType
)
from yggdrasil_integration.fusion.arc_halo_fusion_core import IdentityAspect
from yggdrasil_integration.core.yggdrasil_atomspace import AtomType


async def main():
    """
    Main example demonstrating the enhanced Arc-Halo fusion core
    """
    print("=" * 80)
    print("Enhanced Arc-Halo Cognitive Fusion Reactor Example")
    print("=" * 80)
    print()
    
    # Step 1: Initialize the membrane reservoir
    print("Step 1: Initializing membrane reservoir...")
    reservoir = MembraneReservoir(name="arc_halo_reservoir")
    
    # Add specialized membranes for different cognitive functions
    cognitive_membrane = YggdrasilMembrane(
        name="cognitive_core",
        membrane_type=MembraneType.COGNITIVE
    )
    reservoir.add_membrane(cognitive_membrane)
    
    sensory_membrane = YggdrasilMembrane(
        name="sensory_input",
        membrane_type=MembraneType.SENSORY
    )
    reservoir.add_membrane(sensory_membrane, parent_name="cognitive_core")
    
    motor_membrane = YggdrasilMembrane(
        name="motor_output",
        membrane_type=MembraneType.MOTOR
    )
    reservoir.add_membrane(motor_membrane, parent_name="cognitive_core")
    
    print(f"  Created {len(reservoir.membranes)} membranes")
    print()
    
    # Step 2: Initialize the Aphrodite bridge
    print("Step 2: Initializing Aphrodite bridge...")
    bridge = AphroditeBridge(reservoir=reservoir)
    print("  Bridge initialized")
    print()
    
    # Step 3: Initialize database (if connection string is available)
    print("Step 3: Checking database connection...")
    database = None
    reactor_config = None
    
    if os.getenv("NEON_DATABASE_URL"):
        try:
            database = ArcHaloDatabase()
            print("  Database connection established")
            
            # Create reactor configuration
            reactor_config = ReactorConfig(
                reactor_name="yggdrasil_fusion_reactor_example",
                reactor_type=ReactorType.HIERARCHICAL,
                fusion_strategy=FusionStrategy.DYNAMIC,
                config={
                    "membrane_count": len(reservoir.membranes),
                    "bridge_type": "aphrodite",
                    "yggdrasil_enabled": True
                },
                metadata={
                    "description": "Example hierarchical fusion reactor with Yggdrasil integration",
                    "version": "1.0.0"
                }
            )
        except Exception as e:
            print(f"  Database connection failed: {e}")
            print("  Continuing without database persistence...")
    else:
        print("  NEON_DATABASE_URL not set, skipping database integration")
        print("  Set NEON_DATABASE_URL to enable database persistence")
    print()
    
    # Step 4: Initialize the enhanced fusion core
    print("Step 4: Initializing enhanced Arc-Halo fusion core...")
    fusion_core = EnhancedArcHaloFusionCore(
        name="arc_halo_core",
        reservoir=reservoir,
        bridge=bridge,
        database=database,
        reactor_config=reactor_config
    )
    
    if fusion_core.reactor_id:
        print(f"  Fusion core created with reactor ID: {fusion_core.reactor_id}")
    else:
        print("  Fusion core created (no database persistence)")
    print()
    
    # Step 5: Configure identity and goals
    print("Step 5: Configuring identity and goals...")
    
    # Add core beliefs
    fusion_core.self_model.add_identity_atom(
        IdentityAspect.CORE_BELIEFS,
        "I am a cognitive system designed to understand and process information",
        stability=0.95,
        salience=0.9
    )
    
    fusion_core.self_model.add_identity_atom(
        IdentityAspect.CORE_BELIEFS,
        "Knowledge should be organized hierarchically for efficient retrieval",
        stability=0.9,
        salience=0.8
    )
    
    # Add capabilities
    fusion_core.self_model.add_identity_atom(
        IdentityAspect.CAPABILITIES,
        "Pattern recognition using decision forests",
        stability=0.85,
        salience=0.85
    )
    
    fusion_core.self_model.add_identity_atom(
        IdentityAspect.CAPABILITIES,
        "Neural-symbolic reasoning through Aphrodite bridge",
        stability=0.85,
        salience=0.85
    )
    
    # Add goals
    fusion_core.self_model.add_identity_atom(
        IdentityAspect.GOALS,
        "Achieve coherent understanding of complex cognitive architectures",
        stability=0.8,
        salience=0.9
    )
    
    fusion_core.self_model.add_identity_atom(
        IdentityAspect.GOALS,
        "Continuously improve meta-learning strategies",
        stability=0.75,
        salience=0.85
    )
    
    print(f"  Added {len(fusion_core.self_model.identity_atoms)} identity atoms")
    print()
    
    # Step 6: Add some knowledge to the cognitive membrane
    print("Step 6: Populating knowledge base...")
    
    # Add concepts
    concept_ids = []
    concepts = [
        "consciousness", "cognition", "perception", "memory",
        "reasoning", "learning", "attention", "emotion"
    ]
    
    for concept in concepts:
        atom_id = cognitive_membrane.atomspace.add_node(
            AtomType.CONCEPT_NODE,
            concept
        )
        concept_ids.append(atom_id)
    
    # Add relationships
    cognitive_membrane.atomspace.add_link(
        AtomType.SIMILARITY_LINK,
        [concept_ids[0], concept_ids[1]]  # consciousness - cognition
    )
    
    cognitive_membrane.atomspace.add_link(
        AtomType.SIMILARITY_LINK,
        [concept_ids[1], concept_ids[4]]  # cognition - reasoning
    )
    
    cognitive_membrane.atomspace.add_link(
        AtomType.SIMILARITY_LINK,
        [concept_ids[2], concept_ids[6]]  # perception - attention
    )
    
    print(f"  Added {len(concepts)} concepts and 3 relationships")
    print()
    
    # Step 7: Activate the fusion core
    print("Step 7: Activating fusion core...")
    fusion_core.activate()
    print("  Fusion core activated")
    print()
    
    # Step 8: Process queries
    print("Step 8: Processing queries...")
    print()
    
    queries = [
        "What is the relationship between consciousness and cognition?",
        "How does perception relate to attention?",
        "What are the key capabilities of this system?"
    ]
    
    for i, query_text in enumerate(queries, 1):
        print(f"  Query {i}: {query_text}")
        response = await fusion_core.process_query(query_text)
        
        print(f"    Confidence: {response['response'].confidence:.2f}")
        print(f"    Results: {len(response['response'].results)}")
        print(f"    Reasoning mode: {response['response'].reasoning_mode_used.value}")
        
        if response['response'].results:
            print(f"    Top result: {response['response'].results[0]}")
        
        print()
    
    # Step 9: Execute fusion cycles
    print("Step 9: Executing fusion cycles...")
    
    for i in range(5):
        await fusion_core.fusion_cycle()
        if (i + 1) % 2 == 0:
            print(f"  Completed {i + 1} fusion cycles")
    
    print()
    
    # Step 10: Display statistics
    print("Step 10: Displaying statistics...")
    stats = fusion_core.get_statistics()
    
    print(f"  Fusion cycles: {stats.get('fusion_cycles', 0)}")
    print(f"  Queries processed: {stats.get('queries_processed', 0)}")
    print(f"  Total experiences: {stats.get('total_experiences', 0)}")
    print(f"  Meta-learning events: {stats.get('meta_learning_events', 0)}")
    print()
    
    # Step 11: Display identity summary
    print("Step 11: Identity summary...")
    identity = fusion_core.self_model.get_identity_summary()
    
    print(f"  Core Beliefs: {len(identity.get('core_beliefs', []))}")
    for belief in identity.get('core_beliefs', [])[:2]:
        print(f"    - {belief['content']} (stability: {belief['stability']:.2f})")
    
    print(f"  Capabilities: {len(identity.get('capabilities', []))}")
    for capability in identity.get('capabilities', []):
        print(f"    - {capability['content']}")
    
    print(f"  Goals: {len(identity.get('goals', []))}")
    for goal in identity.get('goals', []):
        print(f"    - {goal['content']} (salience: {goal['salience']:.2f})")
    
    print()
    
    # Step 12: Database status (if available)
    if fusion_core.reactor_id:
        print("Step 12: Database reactor status...")
        reactor_status = fusion_core.get_reactor_status_from_db()
        
        if reactor_status:
            print(f"  Reactor name: {reactor_status['reactor_name']}")
            print(f"  Reactor type: {reactor_status['reactor_type']}")
            print(f"  Fusion strategy: {reactor_status['fusion_strategy']}")
            print(f"  Status: {reactor_status['status']}")
            print(f"  Model count: {reactor_status['model_count']}")
            print(f"  Operation count: {reactor_status['operation_count']}")
            print(f"  Recent operations: {len(reactor_status['recent_operations'])}")
        
        print()
    
    # Step 13: Deactivate the fusion core
    print("Step 13: Deactivating fusion core...")
    fusion_core.deactivate()
    print("  Fusion core deactivated")
    print()
    
    # Cleanup
    if database:
        database.close()
    
    print("=" * 80)
    print("Example completed successfully!")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())
