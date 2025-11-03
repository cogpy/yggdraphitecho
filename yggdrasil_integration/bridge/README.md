# Bridge: Aphrodite Relational Bridge

This module implements the neural-symbolic bridge between Yggdrasil membrane reservoirs and the Arc-Halo Cognitive Fusion Reactor Core. It uses the Aphrodite LLM engine for semantic reasoning and query translation.

## Key Components

-   `AphroditeBridge`: The main class for the bridge implementation.
-   `BridgeQuery`, `BridgeResponse`: Dataclasses for queries and responses.
-   `SemanticEncoder`: Encodes natural language and atoms into a shared semantic space.
-   `QueryTranslator`: Translates natural language queries into atomspace patterns.
-   `ReasoningMode`, `QueryType`: Enums for reasoning modes and query types.

## Functionality

-   Processing queries using symbolic, neural, or hybrid reasoning.
-   Translating natural language queries into executable atomspace operations.
-   Encoding atoms and text into a shared semantic space for similarity comparisons.
-   Merging and ranking results from different reasoning modes.
-   Generating explanations for query results.
