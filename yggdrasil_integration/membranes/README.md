# Membranes: Yggdrasil Membrane Reservoir

This module implements P-System membrane computing using Yggdrasil decision forests as computational substrates. Each membrane is a decision forest that processes atoms and communicates with other membranes.

## Key Components

-   `YggdrasilMembrane`: The main class for the membrane implementation.
-   `MembraneReservoir`: A collection of interconnected membranes.
-   `MembraneMessage`: Dataclass for messages passed between membranes.
-   `MembraneRule`: Dataclass for processing rules.
-   `MembraneType`, `MessagePriority`: Enums for membrane types and message priorities.

## Functionality

-   Creating and managing a hierarchy of membranes.
-   Sending and receiving messages between membranes.
-   Processing messages and atoms according to a set of rules.
-   Routing messages through the membrane hierarchy.
-   Managing membrane state and resources.
