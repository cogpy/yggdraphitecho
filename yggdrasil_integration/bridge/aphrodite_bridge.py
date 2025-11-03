"""
Aphrodite Relational Bridge Layer

This module implements the neural-symbolic bridge between Yggdrasil membrane
reservoirs and the Arc-Halo Cognitive Fusion Reactor Core. It uses the Aphrodite
LLM engine for semantic reasoning and query translation.
"""

import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import numpy as np
import json
import asyncio

from ..core.yggdrasil_atomspace import (
    YggdrasilAtomSpace, Atom, LinkAtom, AtomType, TruthValue, AttentionValue
)
from ..membranes.yggdrasil_membrane import (
    YggdrasilMembrane, MembraneReservoir, MembraneMessage, MessagePriority
)


class ReasoningMode(Enum):
    """Reasoning modes for the bridge"""
    SYMBOLIC = "symbolic"  # Pure atomspace reasoning
    NEURAL = "neural"  # Pure LLM reasoning
    HYBRID = "hybrid"  # Combined approach
    ADAPTIVE = "adaptive"  # Learn best mode per query type


class QueryType(Enum):
    """Types of queries the bridge can handle"""
    PATTERN_MATCH = "pattern_match"
    SIMILARITY = "similarity"
    INFERENCE = "inference"
    ANALOGY = "analogy"
    CAUSAL = "causal"
    ABDUCTIVE = "abductive"
    PLANNING = "planning"
    EXPLANATION = "explanation"


@dataclass
class BridgeQuery:
    """Query to the Aphrodite bridge"""
    query_id: str
    query_type: QueryType
    natural_language: str
    context: Dict[str, Any] = field(default_factory=dict)
    reasoning_mode: ReasoningMode = ReasoningMode.ADAPTIVE
    max_results: int = 10
    confidence_threshold: float = 0.5


@dataclass
class BridgeResponse:
    """Response from the Aphrodite bridge"""
    query_id: str
    results: List[Dict[str, Any]]
    reasoning_mode_used: ReasoningMode
    confidence: float
    explanation: str
    processing_time: float
    metadata: Dict[str, Any] = field(default_factory=dict)


class SemanticEncoder:
    """
    Encodes natural language and atoms into shared semantic space
    
    This class provides bidirectional translation between symbolic atomspace
    representations and neural embeddings.
    """
    
    def __init__(self, embedding_dim: int = 768):
        """
        Initialize semantic encoder
        
        Args:
            embedding_dim: Dimension of semantic embeddings
        """
        self.embedding_dim = embedding_dim
        self.logger = logging.getLogger(f"{__name__}.SemanticEncoder")
        
        # Cache for embeddings
        self.atom_embeddings: Dict[str, np.ndarray] = {}
        self.text_embeddings: Dict[str, np.ndarray] = {}
        
        self.logger.info("Initialized SemanticEncoder")
    
    def encode_atom(self, atom: Atom) -> np.ndarray:
        """
        Encode atom into semantic embedding
        
        Args:
            atom: Atom to encode
            
        Returns:
            Semantic embedding vector
        """
        if atom.atom_id in self.atom_embeddings:
            return self.atom_embeddings[atom.atom_id]
        
        # Combine structural and semantic features
        structural_features = atom.to_feature_vector()
        
        # Encode atom name/content semantically
        # In production, use actual LLM embeddings
        semantic_features = self._encode_text_simple(atom.name)
        
        # Combine features
        embedding = np.concatenate([
            structural_features[:min(len(structural_features), self.embedding_dim // 2)],
            semantic_features[:self.embedding_dim // 2]
        ])
        
        # Pad or truncate to embedding_dim
        if len(embedding) < self.embedding_dim:
            embedding = np.pad(embedding, (0, self.embedding_dim - len(embedding)))
        else:
            embedding = embedding[:self.embedding_dim]
        
        self.atom_embeddings[atom.atom_id] = embedding
        return embedding
    
    def encode_text(self, text: str) -> np.ndarray:
        """
        Encode text into semantic embedding
        
        Args:
            text: Text to encode
            
        Returns:
            Semantic embedding vector
        """
        if text in self.text_embeddings:
            return self.text_embeddings[text]
        
        # In production, use actual LLM embeddings via Aphrodite
        embedding = self._encode_text_simple(text)
        
        self.text_embeddings[text] = embedding
        return embedding
    
    def _encode_text_simple(self, text: str) -> np.ndarray:
        """Simple text encoding (placeholder for actual LLM embeddings)"""
        # Use hash-based encoding as placeholder
        import hashlib
        hash_bytes = hashlib.sha512(text.encode()).digest()
        embedding = np.frombuffer(hash_bytes, dtype=np.float32)[:self.embedding_dim]
        # Normalize
        embedding = embedding / (np.linalg.norm(embedding) + 1e-10)
        return embedding
    
    def compute_similarity(self, embedding1: np.ndarray, 
                          embedding2: np.ndarray) -> float:
        """Compute cosine similarity between embeddings"""
        norm1 = np.linalg.norm(embedding1)
        norm2 = np.linalg.norm(embedding2)
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return float(np.dot(embedding1, embedding2) / (norm1 * norm2))


class QueryTranslator:
    """
    Translates natural language queries into atomspace patterns
    
    This class uses LLM-based understanding to convert queries into
    executable atomspace operations.
    """
    
    def __init__(self, encoder: SemanticEncoder):
        """
        Initialize query translator
        
        Args:
            encoder: Semantic encoder instance
        """
        self.encoder = encoder
        self.logger = logging.getLogger(f"{__name__}.QueryTranslator")
        
        # Query templates
        self.templates: Dict[QueryType, List[str]] = self._init_templates()
        
        self.logger.info("Initialized QueryTranslator")
    
    def _init_templates(self) -> Dict[QueryType, List[str]]:
        """Initialize query templates for different query types"""
        return {
            QueryType.PATTERN_MATCH: [
                "Find atoms matching pattern: {pattern}",
                "Search for: {pattern}",
                "Locate atoms with: {pattern}"
            ],
            QueryType.SIMILARITY: [
                "Find atoms similar to: {reference}",
                "What is similar to: {reference}",
                "Show similar concepts to: {reference}"
            ],
            QueryType.INFERENCE: [
                "What can be inferred from: {premise}",
                "Deduce from: {premise}",
                "Conclude from: {premise}"
            ],
            QueryType.ANALOGY: [
                "Find analogies to: {source}",
                "What is analogous to: {source}",
                "Compare with: {source}"
            ],
            QueryType.CAUSAL: [
                "What causes: {effect}",
                "Why does: {effect}",
                "Explain the cause of: {effect}"
            ],
            QueryType.ABDUCTIVE: [
                "What could explain: {observation}",
                "Hypothesize about: {observation}",
                "Generate explanations for: {observation}"
            ]
        }
    
    def translate_query(self, query: BridgeQuery, 
                       atomspace: YggdrasilAtomSpace) -> Dict[str, Any]:
        """
        Translate natural language query to atomspace pattern
        
        Args:
            query: Bridge query
            atomspace: Target atomspace
            
        Returns:
            Translated query pattern
        """
        self.logger.info(f"Translating query: {query.query_type.value}")
        
        # Extract key entities and relationships from query
        entities = self._extract_entities(query.natural_language)
        relationships = self._extract_relationships(query.natural_language)
        
        # Build atomspace pattern
        pattern = {
            'query_type': query.query_type.value,
            'entities': entities,
            'relationships': relationships,
            'constraints': self._extract_constraints(query.natural_language),
            'context': query.context
        }
        
        return pattern
    
    def _extract_entities(self, text: str) -> List[str]:
        """Extract entities from text (placeholder for NER)"""
        # In production, use actual NER via LLM
        # For now, simple word extraction
        import re
        words = re.findall(r'\w+', text.lower())
        # Filter common words
        stopwords = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'to', 'from', 'of'}
        entities = [w for w in words if w not in stopwords and len(w) > 2]
        return entities[:5]  # Limit to top 5
    
    def _extract_relationships(self, text: str) -> List[str]:
        """Extract relationships from text"""
        # In production, use dependency parsing via LLM
        # For now, look for common relationship indicators
        relationships = []
        rel_keywords = {
            'causes': 'causes',
            'leads to': 'causes',
            'results in': 'causes',
            'is a': 'inheritance',
            'similar to': 'similarity',
            'like': 'similarity',
            'part of': 'member',
            'contains': 'member'
        }
        
        text_lower = text.lower()
        for keyword, rel_type in rel_keywords.items():
            if keyword in text_lower:
                relationships.append(rel_type)
        
        return relationships
    
    def _extract_constraints(self, text: str) -> Dict[str, Any]:
        """Extract constraints from text"""
        constraints = {}
        
        # Extract temporal constraints
        if 'recent' in text.lower():
            constraints['temporal'] = 'recent'
        elif 'old' in text.lower() or 'historical' in text.lower():
            constraints['temporal'] = 'historical'
        
        # Extract confidence constraints
        if 'certain' in text.lower() or 'definite' in text.lower():
            constraints['min_confidence'] = 0.8
        elif 'possible' in text.lower() or 'maybe' in text.lower():
            constraints['min_confidence'] = 0.3
        
        return constraints


class AphroditeBridge:
    """
    Main bridge between Yggdrasil membranes and Arc-Halo fusion core
    
    This class orchestrates neural-symbolic integration, providing semantic
    reasoning capabilities over the atomspace substrate.
    """
    
    def __init__(self, 
                 reservoir: MembraneReservoir,
                 embedding_dim: int = 768):
        """
        Initialize Aphrodite Bridge
        
        Args:
            reservoir: Membrane reservoir to bridge
            embedding_dim: Dimension of semantic embeddings
        """
        self.reservoir = reservoir
        self.embedding_dim = embedding_dim
        self.logger = logging.getLogger(f"{__name__}.AphroditeBridge")
        
        # Components
        self.encoder = SemanticEncoder(embedding_dim)
        self.translator = QueryTranslator(self.encoder)
        
        # Query history
        self.query_history: List[Tuple[BridgeQuery, BridgeResponse]] = []
        
        # Performance tracking
        self.mode_performance: Dict[ReasoningMode, List[float]] = {
            mode: [] for mode in ReasoningMode
        }
        
        # Statistics
        self.stats = {
            'total_queries': 0,
            'successful_queries': 0,
            'failed_queries': 0,
            'avg_confidence': 0.0,
            'mode_usage': {mode.value: 0 for mode in ReasoningMode}
        }
        
        self.logger.info("Initialized AphroditeBridge")
    
    async def process_query(self, query: BridgeQuery) -> BridgeResponse:
        """
        Process a query through the bridge
        
        Args:
            query: Bridge query to process
            
        Returns:
            Bridge response with results
        """
        import time
        start_time = time.time()
        
        self.logger.info(f"Processing query: {query.query_id}")
        self.stats['total_queries'] += 1
        
        # Select reasoning mode
        mode = self._select_reasoning_mode(query)
        self.stats['mode_usage'][mode.value] += 1
        
        # Process based on mode
        if mode == ReasoningMode.SYMBOLIC:
            results = await self._process_symbolic(query)
        elif mode == ReasoningMode.NEURAL:
            results = await self._process_neural(query)
        elif mode == ReasoningMode.HYBRID:
            results = await self._process_hybrid(query)
        else:  # ADAPTIVE
            results = await self._process_adaptive(query)
        
        # Compute confidence
        confidence = self._compute_confidence(results)
        
        # Generate explanation
        explanation = self._generate_explanation(query, results, mode)
        
        processing_time = time.time() - start_time
        
        response = BridgeResponse(
            query_id=query.query_id,
            results=results,
            reasoning_mode_used=mode,
            confidence=confidence,
            explanation=explanation,
            processing_time=processing_time
        )
        
        # Update statistics
        if results:
            self.stats['successful_queries'] += 1
        else:
            self.stats['failed_queries'] += 1
        
        # Track performance
        self.mode_performance[mode].append(confidence)
        
        # Store in history
        self.query_history.append((query, response))
        
        return response
    
    def _select_reasoning_mode(self, query: BridgeQuery) -> ReasoningMode:
        """Select best reasoning mode for query"""
        if query.reasoning_mode != ReasoningMode.ADAPTIVE:
            return query.reasoning_mode
        
        # Adaptive mode selection based on query type and history
        if query.query_type in [QueryType.PATTERN_MATCH, QueryType.SIMILARITY]:
            # Structural queries work well with symbolic
            return ReasoningMode.SYMBOLIC
        elif query.query_type in [QueryType.EXPLANATION, QueryType.ABDUCTIVE]:
            # Generative queries need neural
            return ReasoningMode.NEURAL
        else:
            # Complex reasoning benefits from hybrid
            return ReasoningMode.HYBRID
    
    async def _process_symbolic(self, query: BridgeQuery) -> List[Dict[str, Any]]:
        """Process query using pure symbolic reasoning"""
        self.logger.debug("Processing with symbolic reasoning")
        
        results = []
        
        # Get atomspace from a cognitive membrane
        cognitive_membranes = [
            m for m in self.reservoir.membranes.values()
            if m.membrane_type.value == "cognitive"
        ]
        
        if not cognitive_membranes:
            self.logger.warning("No cognitive membranes available")
            return results
        
        atomspace = cognitive_membranes[0].atomspace
        
        # Translate query to pattern
        pattern = self.translator.translate_query(query, atomspace)
        
        # Execute pattern matching
        if query.query_type == QueryType.PATTERN_MATCH:
            results = self._pattern_match(atomspace, pattern, query.max_results)
        elif query.query_type == QueryType.INFERENCE:
            results = self._pattern_match(atomspace, pattern, query.max_results)
        elif query.query_type == QueryType.SIMILARITY:
            results = self._similarity_search(atomspace, pattern, query.max_results)
        
        return results
    
    async def _process_neural(self, query: BridgeQuery) -> List[Dict[str, Any]]:
        """Process query using pure neural reasoning"""
        self.logger.debug("Processing with neural reasoning")
        
        # In production, this would call the Aphrodite LLM engine
        # For now, return placeholder results
        results = [{
            'type': 'neural_response',
            'content': f"Neural reasoning result for: {query.natural_language}",
            'confidence': 0.7
        }]
        
        return results
    
    async def _process_hybrid(self, query: BridgeQuery) -> List[Dict[str, Any]]:
        """Process query using hybrid neural-symbolic reasoning"""
        self.logger.debug("Processing with hybrid reasoning")
        
        # Run both symbolic and neural in parallel
        symbolic_task = self._process_symbolic(query)
        neural_task = self._process_neural(query)
        
        symbolic_results, neural_results = await asyncio.gather(
            symbolic_task, neural_task
        )
        
        # Merge and rank results
        merged_results = self._merge_results(symbolic_results, neural_results)
        
        return merged_results[:query.max_results]
    
    async def _process_adaptive(self, query: BridgeQuery) -> List[Dict[str, Any]]:
        """Process query with adaptive mode selection"""
        # Select best mode based on performance history
        mode = self._select_reasoning_mode(query)
        
        # Update query mode and process
        query.reasoning_mode = mode
        
        if mode == ReasoningMode.SYMBOLIC:
            return await self._process_symbolic(query)
        elif mode == ReasoningMode.NEURAL:
            return await self._process_neural(query)
        else:
            return await self._process_hybrid(query)
    
    def _pattern_match(self, atomspace: YggdrasilAtomSpace, 
                      pattern: Dict[str, Any], max_results: int) -> List[Dict[str, Any]]:
        """Execute pattern matching on atomspace"""
        results = []
        
        entities = pattern.get('entities', [])
        if not entities:
            return results
        
        # Search for atoms matching entities
        for entity in entities:
            matching_atoms = atomspace.get_atoms_by_name(entity)
            for atom in matching_atoms[:max_results]:
                results.append({
                    'atom_id': atom.atom_id,
                    'type': atom.atom_type.value,
                    'name': atom.name,
                    'truth_value': {
                        'strength': atom.truth_value.strength,
                        'confidence': atom.truth_value.confidence
                    },
                    'match_type': 'exact'
                })
        
        return results[:max_results]
    
    def _similarity_search(self, atomspace: YggdrasilAtomSpace,
                          pattern: Dict[str, Any], max_results: int) -> List[Dict[str, Any]]:
        """Execute similarity search on atomspace"""
        results = []
        
        entities = pattern.get('entities', [])
        if not entities:
            return results
        
        # Find atoms with similar names
        reference_entity = entities[0]
        reference_atoms = atomspace.get_atoms_by_name(reference_entity)
        
        if not reference_atoms:
            return results
        
        reference_atom = reference_atoms[0]
        
        # Find similar atoms
        similar = atomspace.find_similar_atoms(reference_atom.atom_id, max_results)
        
        for atom_id, similarity in similar:
            atom = atomspace.get_atom(atom_id)
            if atom:
                results.append({
                    'atom_id': atom.atom_id,
                    'type': atom.atom_type.value,
                    'name': atom.name,
                    'similarity': similarity,
                    'truth_value': {
                        'strength': atom.truth_value.strength,
                        'confidence': atom.truth_value.confidence
                    }
                })
        
        return results
    
    def _merge_results(self, symbolic_results: List[Dict[str, Any]],
                      neural_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Merge symbolic and neural results"""
        # Combine results and rank by confidence/similarity
        all_results = []
        
        for result in symbolic_results:
            result['source'] = 'symbolic'
            all_results.append(result)
        
        for result in neural_results:
            result['source'] = 'neural'
            all_results.append(result)
        
        # Sort by confidence/similarity
        def get_score(r):
            if 'similarity' in r:
                return r['similarity']
            elif 'confidence' in r:
                return r['confidence']
            elif 'truth_value' in r:
                return r['truth_value'].get('confidence', 0.5)
            return 0.5
        
        all_results.sort(key=get_score, reverse=True)
        
        return all_results
    
    def _compute_confidence(self, results: List[Dict[str, Any]]) -> float:
        """Compute overall confidence for results"""
        if not results:
            return 0.0
        
        confidences = []
        for result in results:
            if 'confidence' in result:
                confidences.append(result['confidence'])
            elif 'similarity' in result:
                confidences.append(result['similarity'])
            elif 'truth_value' in result:
                confidences.append(result['truth_value'].get('confidence', 0.5))
        
        if not confidences:
            return 0.5
        
        return float(np.mean(confidences))
    
    def _generate_explanation(self, query: BridgeQuery, 
                            results: List[Dict[str, Any]],
                            mode: ReasoningMode) -> str:
        """Generate explanation for results"""
        if not results:
            return f"No results found for query: {query.natural_language}"
        
        explanation = f"Found {len(results)} results using {mode.value} reasoning. "
        
        if mode == ReasoningMode.SYMBOLIC:
            explanation += "Results based on structural pattern matching in atomspace."
        elif mode == ReasoningMode.NEURAL:
            explanation += "Results based on semantic understanding via LLM."
        elif mode == ReasoningMode.HYBRID:
            explanation += "Results combined from both symbolic and neural reasoning."
        
        return explanation
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get bridge statistics"""
        return {
            'stats': self.stats.copy(),
            'mode_performance': {
                mode.value: {
                    'avg_confidence': float(np.mean(scores)) if scores else 0.0,
                    'count': len(scores)
                }
                for mode, scores in self.mode_performance.items()
            },
            'query_history_size': len(self.query_history)
        }
