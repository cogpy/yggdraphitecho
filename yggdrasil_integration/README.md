# Yggdrasil Decision Forests Integration for Aphrodite Engine

## Overview

This integration introduces a novel cognitive computing architecture that leverages **Yggdrasil Decision Forests** as a distributed atomspace arena within the `yggdraphitecho` repository. The system creates a powerful neural-symbolic framework where decision forests serve as the computational substrate for atomspace operations, with the Aphrodite engine providing a relational bridge to the Arc-Halo Cognitive Fusion Reactor Core.

**NEW**: The integration now includes full **Arc-Halo database integration** for production-ready deployment with PostgreSQL persistence, multi-model orchestration, and comprehensive state management.

## Quick Links

-   **Core Documentation**: `core/README.md`
-   **Membranes Documentation**: `membranes/README.md`
-   **Bridge Documentation**: `bridge/README.md`
-   **Fusion Documentation**: `fusion/README.md`
-   **Architecture Overview**: `yggdrasil_atomspace_architecture.md`

## Architecture

The integration is designed with a layered architecture comprising three primary computational domains:

1.  **Yggdrasil Membrane Reservoir Layer**: Provides distributed storage and pattern recognition using decision forest structures.
2.  **Aphrodite Relational Bridge Layer**: Enables semantic reasoning and neural-symbolic integration through LLM-based processing.
3.  **Arc-Halo Cognitive Fusion Reactor Core**: Implements self-awareness, identity persistence, and meta-learning capabilities using Deep Tree Echo state networks.

**NEW**: **Arc-Halo Database Integration Layer**: Provides PostgreSQL persistence for reactor state, fusion operations, cognitive states, and model interaction graphs.

For a comprehensive description of the architecture, please refer to the [Yggdrasil Decision Forests Distributed AtomSpace Arena Architecture](yggdrasil_atomspace_architecture.md) document.

## Key Features

### Core Features

-   **Distributed AtomSpace**: A scalable and efficient atomspace implementation backed by Yggdrasil Decision Forests.
-   **Membrane Computing**: P-System membrane computing using decision forests as computational substrates.
-   **Neural-Symbolic Integration**: The Aphrodite engine acts as a bridge between the symbolic atomspace and neural processing.
-   **Self-Awareness**: The Arc-Halo Cognitive Fusion Reactor Core provides a persistent self-model and identity.
-   **Meta-Learning**: The system can learn and improve its own cognitive strategies over time.

### Arc-Halo Database Integration (NEW)

-   **PostgreSQL Persistence**: Complete reactor state persistence using Neon serverless PostgreSQL or standard PostgreSQL.
-   **Multi-Model Orchestration**: Support for ensemble, cascade, parallel, and hierarchical reactor types.
-   **Fusion Strategies**: Configurable fusion strategies including weighted averaging, voting, stacking, and dynamic selection.
-   **Model Interaction Graphs**: Complex model relationships with feeds_into, validates, augments, and corrects interactions.
-   **Cognitive State Management**: Persistent storage of attention focus, active goals, memory, and context.
-   **Graceful Degradation**: Automatic fallback to in-memory operation when database is unavailable.

## Getting Started

### Prerequisites

-   Python 3.9+
-   Yggdrasil Decision Forests (`pip install ydf`)
-   pytest (`pip install pytest pytest-asyncio`)
-   **Optional**: psycopg2-binary for database integration (`pip install psycopg2-binary`)
-   **Optional**: PostgreSQL 13+ or Neon database account for persistence

### Running Tests

To verify the installation and functionality of the integration, run the following command from the root of the `yggdraphitecho` repository:

```bash
python3 -m pytest yggdrasil_integration/tests/
```

All 29 tests should pass, including 8 tests for the Arc-Halo database integration.

## Usage Examples

### Basic Usage (In-Memory)

```python
import asyncio
from yggdrasil_integration.membranes.yggdrasil_membrane import MembraneReservoir
from yggdrasil_integration.bridge.aphrodite_bridge import AphroditeBridge
from yggdrasil_integration.fusion.arc_halo_fusion_core import ArcHaloFusionCore

async def main():
    # Initialize the components
    reservoir = MembraneReservoir(name="main_reservoir")
    bridge = AphroditeBridge(reservoir=reservoir)
    fusion_core = ArcHaloFusionCore(name="main_core", reservoir=reservoir, bridge=bridge)

    # Activate the fusion core
    fusion_core.activate()

    # Process a query
    query_text = "What is the nature of consciousness?"
    response = await fusion_core.process_query(query_text)
    print(response)

    # Run a fusion cycle
    await fusion_core.fusion_cycle()

    # Deactivate the core
    fusion_core.deactivate()

if __name__ == "__main__":
    asyncio.run(main())
```

### Enhanced Usage with Database Persistence (NEW)

```python
import asyncio
import os
from yggdrasil_integration.membranes.yggdrasil_membrane import MembraneReservoir
from yggdrasil_integration.bridge.aphrodite_bridge import AphroditeBridge
from yggdrasil_integration.fusion.arc_halo_db_integration import (
    EnhancedArcHaloFusionCore, ArcHaloDatabase, ReactorConfig,
    ReactorType, FusionStrategy
)

async def main():
    # Initialize components
    reservoir = MembraneReservoir(name="main_reservoir")
    bridge = AphroditeBridge(reservoir=reservoir)
    
    # Create database connection (requires NEON_DATABASE_URL environment variable)
    database = None
    reactor_config = None
    
    if os.getenv("NEON_DATABASE_URL"):
        database = ArcHaloDatabase()
        reactor_config = ReactorConfig(
            reactor_name="production_reactor",
            reactor_type=ReactorType.HIERARCHICAL,
            fusion_strategy=FusionStrategy.DYNAMIC
        )
    
    # Create enhanced fusion core with optional database
    fusion_core = EnhancedArcHaloFusionCore(
        name="main_core",
        reservoir=reservoir,
        bridge=bridge,
        database=database,
        reactor_config=reactor_config
    )
    
    # Activate and run
    fusion_core.activate()
    
    for _ in range(10):
        await fusion_core.fusion_cycle()
    
    # Get reactor status from database (if available)
    if fusion_core.reactor_id:
        status = fusion_core.get_reactor_status_from_db()
        print(f"Reactor operations: {status['operation_count']}")
    
    fusion_core.deactivate()

if __name__ == "__main__":
    asyncio.run(main())
```

### Running the Example

A complete example demonstrating the Arc-Halo database integration is available:

```bash
# Set database connection (optional)
export NEON_DATABASE_URL="postgresql://user:password@host/database"

# Run the example
cd /home/ubuntu/yggdraphitecho
PYTHONPATH=/home/ubuntu/yggdraphitecho python3 yggdrasil_integration/examples/arc_halo_db_example.py
```

The example will run successfully with or without database connection, demonstrating graceful degradation.

## Database Setup (Optional)

### Using Neon Serverless PostgreSQL

1.  Sign up for a free account at [neon.tech](https://neon.tech)
2.  Create a new project and database
3.  Copy the connection string from the Neon dashboard
4.  Set the environment variable: `export NEON_DATABASE_URL="your-connection-string"`

### Using Standard PostgreSQL

1.  Install PostgreSQL 13 or higher
2.  Create a database: `createdb arc_halo`
3.  Deploy the Arc-Halo schema (see Arc-Halo repository for SQL files)
4.  Set the environment variable: `export NEON_DATABASE_URL="postgresql://user:password@localhost/arc_halo"`

### Schema Deployment

The Arc-Halo database schema is available in the Arc-Halo repository. Deploy the schema files in order:

1.  `00_master_schema.sql`
2.  `01_core_tables.sql`
3.  `02_tensor_storage.sql`
4.  `03_training_state.sql`
5.  `04_inference_cache.sql`
6.  `05_cognitive_fusion.sql`

Alternatively, use the automated setup script: `./db/scripts/setup_database.sh`

## Testing

The integration includes comprehensive test coverage:

-   **Core Tests** (8 tests): Atomspace operations, feature matrices, decision forest training
-   **Membrane Tests** (5 tests): Membrane creation, message passing, rule processing
-   **Bridge Tests** (4 tests): Query processing, reasoning modes, query translation
-   **Fusion Core Tests** (4 tests): Identity management, fusion cycles, query processing
-   **Database Integration Tests** (8 tests): Reactor creation, state persistence, graceful degradation

Run all tests:

```bash
cd /home/ubuntu/yggdraphitecho
python3 -m pytest yggdrasil_integration/tests/ -v
```

Expected output: `29 passed`

## Project Structure

```
yggdrasil_integration/
├── core/
│   ├── yggdrasil_atomspace.py      # Distributed atomspace implementation
│   └── README.md
├── membranes/
│   ├── yggdrasil_membrane.py       # P-System membrane computing
│   └── README.md
├── bridge/
│   ├── aphrodite_bridge.py         # Neural-symbolic bridge
│   └── README.md
├── fusion/
│   ├── arc_halo_fusion_core.py     # Base fusion reactor
│   ├── arc_halo_db_integration.py  # Database integration (NEW)
│   └── README.md
├── tests/
│   ├── test_yggdrasil_atomspace.py
│   ├── test_yggdrasil_membrane.py
│   ├── test_aphrodite_bridge.py
│   ├── test_arc_halo_fusion_core.py
│   └── test_arc_halo_db_integration.py  # (NEW)
├── examples/
│   └── arc_halo_db_example.py      # Complete example (NEW)
└── README.md
```

## Performance Considerations

### In-Memory Operation

-   Lazy evaluation of decision forest traversals
-   Feature vector caching
-   Attention-based prioritization

### Database Operation (NEW)

-   Connection pooling (1-10 concurrent connections)
-   Asynchronous database writes
-   Batch state updates
-   Lazy loading of cognitive states

### Scalability

-   Horizontal scaling via Neon auto-scaling
-   Vertical scaling via chunked tensor storage
-   Read replicas for analytics queries

## Future Enhancements

-   **Production LLM Integration**: Replace placeholder semantic encoding with actual Aphrodite engine embeddings
-   **Advanced Pattern Recognition**: Gradient boosted trees, isolation forests, ensemble methods
-   **Distributed Deployment**: Multi-node reactor clusters with shared database state
-   **Enhanced Meta-Learning**: Neural architecture search, hyperparameter optimization, transfer learning
-   **Visualization Tools**: Interactive visualization of atomspace graphs, decision forests, and cognitive state
-   **Real-time Monitoring**: Prometheus metrics and Grafana dashboards

## Contributing

Contributions are welcome! Areas of focus:

-   Schema enhancements for additional cognitive capabilities
-   Performance optimizations for large-scale deployments
-   Additional fusion strategies and reactor types
-   Integration with external AI frameworks
-   Documentation improvements and tutorials

## License

This project is part of the yggdraphitecho ecosystem.

## Acknowledgments

-   **Yggdrasil Decision Forests**: Google's production-grade decision forests library
-   **Arc-Halo**: Cognitive Fusion Reactor database infrastructure
-   **Neon**: Serverless PostgreSQL platform
-   **OpenCog**: Inspiration for atomspace architecture

---

**Yggdrasil Decision Forests Integration** - Building the future of cognitive computing 🧠⚡
