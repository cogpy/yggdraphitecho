# Core: Yggdrasil AtomSpace

This module provides a distributed atomspace implementation backed by Yggdrasil decision forests. It maps atomspace operations to decision forest structures, enabling scalable cognitive computing with pattern recognition capabilities.

## Key Components

-   `YggdrasilAtomSpace`: The main class for the atomspace implementation.
-   `Atom`, `LinkAtom`: Dataclasses for representing atoms and links.
-   `AtomType`: Enum for different types of atoms.
-   `TruthValue`, `AttentionValue`: Dataclasses for representing truth and attention values.

## Functionality

-   Adding, removing, and retrieving atoms and links.
-   Indexing atoms by type and name for efficient retrieval.
-   Updating truth and attention values.
-   Generating feature matrices for decision forest training.
-   Training and querying decision forest models for different cognitive domains.
-   Finding similar atoms using decision forest similarity.
