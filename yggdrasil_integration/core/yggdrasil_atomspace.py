"""
Yggdrasil Decision Forests AtomSpace Implementation

This module provides a distributed atomspace implementation backed by Yggdrasil
decision forests. It maps atomspace operations to decision forest structures,
enabling scalable cognitive computing with pattern recognition capabilities.
"""

import logging
from typing import Dict, List, Optional, Any, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
import numpy as np
from collections import defaultdict
import hashlib
import json

try:
    import ydf
except ImportError:
    ydf = None
    logging.warning("Yggdrasil Decision Forests (ydf) not installed. Install with: pip install ydf")

logger = logging.getLogger(__name__)


class AtomType(Enum):
    """Atom types for the atomspace"""
    NODE = "Node"
    LINK = "Link"
    CONCEPT_NODE = "ConceptNode"
    PREDICATE_NODE = "PredicateNode"
    VARIABLE_NODE = "VariableNode"
    EVALUATION_LINK = "EvaluationLink"
    INHERITANCE_LINK = "InheritanceLink"
    SIMILARITY_LINK = "SimilarityLink"
    MEMBER_LINK = "MemberLink"
    EXECUTION_LINK = "ExecutionLink"


@dataclass
class TruthValue:
    """Truth value for atoms (strength and confidence)"""
    strength: float = 0.5  # [0, 1]
    confidence: float = 0.0  # [0, 1]
    
    def to_vector(self) -> np.ndarray:
        """Convert to numpy array for forest encoding"""
        return np.array([self.strength, self.confidence])
    
    @classmethod
    def from_vector(cls, vec: np.ndarray) -> 'TruthValue':
        """Create from numpy array"""
        return cls(strength=float(vec[0]), confidence=float(vec[1]))


@dataclass
class AttentionValue:
    """Attention value for ECAN (Economic Attention Network)"""
    sti: float = 0.0  # Short-term importance
    lti: float = 0.0  # Long-term importance
    vlti: float = 0.0  # Very long-term importance
    
    def to_vector(self) -> np.ndarray:
        """Convert to numpy array for forest encoding"""
        return np.array([self.sti, self.lti, self.vlti])
    
    @classmethod
    def from_vector(cls, vec: np.ndarray) -> 'AttentionValue':
        """Create from numpy array"""
        return cls(sti=float(vec[0]), lti=float(vec[1]), vlti=float(vec[2]))


@dataclass
class Atom:
    """Base atom class for atomspace"""
    atom_id: str
    atom_type: AtomType
    name: str = ""
    truth_value: TruthValue = field(default_factory=TruthValue)
    attention_value: AttentionValue = field(default_factory=AttentionValue)
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=lambda: __import__('time').time())
    
    def to_feature_vector(self) -> np.ndarray:
        """Convert atom to feature vector for decision forest"""
        # Encode atom type as one-hot
        atom_types = list(AtomType)
        type_encoding = np.zeros(len(atom_types))
        type_encoding[atom_types.index(self.atom_type)] = 1.0
        
        # Encode name as hash features
        name_hash = hashlib.md5(self.name.encode()).digest()
        name_features = np.frombuffer(name_hash[:8], dtype=np.float32) / 255.0
        
        # Combine all features
        features = np.concatenate([
            type_encoding,
            self.truth_value.to_vector(),
            self.attention_value.to_vector(),
            name_features,
            [self.timestamp]
        ])
        
        return features
    
    def get_semantic_hash(self) -> str:
        """Get semantic hash for similarity matching"""
        content = f"{self.atom_type.value}:{self.name}"
        return hashlib.sha256(content.encode()).hexdigest()


@dataclass
class LinkAtom(Atom):
    """Link atom connecting other atoms"""
    outgoing: List[str] = field(default_factory=list)  # List of atom IDs
    
    def to_feature_vector(self) -> np.ndarray:
        """Convert link atom to feature vector"""
        base_features = super().to_feature_vector()
        
        # Encode outgoing set size and hash
        outgoing_size = np.array([len(self.outgoing)])
        outgoing_hash = hashlib.md5(
            ''.join(sorted(self.outgoing)).encode()
        ).digest()
        outgoing_features = np.frombuffer(outgoing_hash[:8], dtype=np.float32) / 255.0
        
        return np.concatenate([base_features, outgoing_size, outgoing_features])


class YggdrasilAtomSpace:
    """
    Distributed AtomSpace implementation using Yggdrasil Decision Forests
    
    This class provides a scalable atomspace backed by decision forests,
    enabling efficient pattern recognition and distributed storage.
    """
    
    def __init__(self, name: str = "default", enable_persistence: bool = True):
        """
        Initialize Yggdrasil AtomSpace
        
        Args:
            name: Name of the atomspace instance
            enable_persistence: Enable persistent storage
        """
        self.name = name
        self.enable_persistence = enable_persistence
        self.logger = logging.getLogger(f"{__name__}.{name}")
        
        # Atom storage
        self.atoms: Dict[str, Atom] = {}
        self.type_index: Dict[AtomType, Set[str]] = defaultdict(set)
        self.name_index: Dict[str, Set[str]] = defaultdict(set)
        self.incoming_index: Dict[str, Set[str]] = defaultdict(set)
        
        # Decision forest models for different cognitive domains
        self.forest_models: Dict[str, Any] = {}
        self.feature_cache: Dict[str, np.ndarray] = {}
        
        # Statistics
        self.stats = {
            'total_atoms': 0,
            'total_queries': 0,
            'cache_hits': 0,
            'cache_misses': 0
        }
        
        self.logger.info(f"Initialized YggdrasilAtomSpace: {name}")
    
    def _generate_atom_id(self, atom_type: AtomType, name: str, 
                          outgoing: Optional[List[str]] = None) -> str:
        """Generate unique atom ID"""
        content = f"{atom_type.value}:{name}"
        if outgoing:
            content += f":{','.join(sorted(outgoing))}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    
    def add_node(self, atom_type: AtomType, name: str, 
                 truth_value: Optional[TruthValue] = None,
                 attention_value: Optional[AttentionValue] = None) -> str:
        """
        Add a node atom to the atomspace
        
        Args:
            atom_type: Type of the atom
            name: Name/content of the atom
            truth_value: Optional truth value
            attention_value: Optional attention value
            
        Returns:
            Atom ID
        """
        atom_id = self._generate_atom_id(atom_type, name)
        
        if atom_id in self.atoms:
            self.logger.debug(f"Atom already exists: {atom_id}")
            return atom_id
        
        atom = Atom(
            atom_id=atom_id,
            atom_type=atom_type,
            name=name,
            truth_value=truth_value or TruthValue(),
            attention_value=attention_value or AttentionValue()
        )
        
        self._index_atom(atom)
        self.stats['total_atoms'] += 1
        
        self.logger.debug(f"Added node: {atom_type.value} - {name}")
        return atom_id
    
    def add_link(self, atom_type: AtomType, outgoing: List[str],
                 name: str = "",
                 truth_value: Optional[TruthValue] = None,
                 attention_value: Optional[AttentionValue] = None) -> str:
        """
        Add a link atom to the atomspace
        
        Args:
            atom_type: Type of the link
            outgoing: List of atom IDs this link connects
            name: Optional name for the link
            truth_value: Optional truth value
            attention_value: Optional attention value
            
        Returns:
            Atom ID
        """
        atom_id = self._generate_atom_id(atom_type, name, outgoing)
        
        if atom_id in self.atoms:
            self.logger.debug(f"Link already exists: {atom_id}")
            return atom_id
        
        # Verify all outgoing atoms exist
        for out_id in outgoing:
            if out_id not in self.atoms:
                raise ValueError(f"Outgoing atom not found: {out_id}")
        
        link = LinkAtom(
            atom_id=atom_id,
            atom_type=atom_type,
            name=name,
            outgoing=outgoing,
            truth_value=truth_value or TruthValue(),
            attention_value=attention_value or AttentionValue()
        )
        
        self._index_atom(link)
        
        # Update incoming index
        for out_id in outgoing:
            self.incoming_index[out_id].add(atom_id)
        
        self.stats['total_atoms'] += 1
        
        self.logger.debug(f"Added link: {atom_type.value} connecting {len(outgoing)} atoms")
        return atom_id
    
    def _index_atom(self, atom: Atom):
        """Index atom for efficient retrieval"""
        self.atoms[atom.atom_id] = atom
        self.type_index[atom.atom_type].add(atom.atom_id)
        if atom.name:
            self.name_index[atom.name].add(atom.atom_id)
        
        # Cache feature vector
        self.feature_cache[atom.atom_id] = atom.to_feature_vector()
    
    def get_atom(self, atom_id: str) -> Optional[Atom]:
        """Get atom by ID"""
        return self.atoms.get(atom_id)
    
    def get_atoms_by_type(self, atom_type: AtomType) -> List[Atom]:
        """Get all atoms of a specific type"""
        atom_ids = self.type_index.get(atom_type, set())
        return [self.atoms[aid] for aid in atom_ids]
    
    def get_atoms_by_name(self, name: str) -> List[Atom]:
        """Get all atoms with a specific name"""
        atom_ids = self.name_index.get(name, set())
        return [self.atoms[aid] for aid in atom_ids]
    
    def get_incoming_set(self, atom_id: str) -> List[Atom]:
        """Get all atoms that link to this atom"""
        incoming_ids = self.incoming_index.get(atom_id, set())
        return [self.atoms[aid] for aid in incoming_ids]
    
    def get_outgoing_set(self, atom_id: str) -> List[str]:
        """Get outgoing atoms for a link"""
        atom = self.atoms.get(atom_id)
        if isinstance(atom, LinkAtom):
            return atom.outgoing
        return []
    
    def update_truth_value(self, atom_id: str, truth_value: TruthValue):
        """Update truth value of an atom"""
        if atom_id in self.atoms:
            self.atoms[atom_id].truth_value = truth_value
            # Invalidate feature cache
            self.feature_cache[atom_id] = self.atoms[atom_id].to_feature_vector()
    
    def update_attention_value(self, atom_id: str, attention_value: AttentionValue):
        """Update attention value of an atom"""
        if atom_id in self.atoms:
            self.atoms[atom_id].attention_value = attention_value
            # Invalidate feature cache
            self.feature_cache[atom_id] = self.atoms[atom_id].to_feature_vector()
    
    def remove_atom(self, atom_id: str) -> bool:
        """Remove atom from atomspace"""
        if atom_id not in self.atoms:
            return False
        
        atom = self.atoms[atom_id]
        
        # Remove from indices
        self.type_index[atom.atom_type].discard(atom_id)
        if atom.name:
            self.name_index[atom.name].discard(atom_id)
        
        # Remove incoming links
        for incoming_id in list(self.incoming_index.get(atom_id, [])):
            self.remove_atom(incoming_id)
        
        # Remove from outgoing indices
        if isinstance(atom, LinkAtom):
            for out_id in atom.outgoing:
                self.incoming_index[out_id].discard(atom_id)
        
        # Remove from storage
        del self.atoms[atom_id]
        if atom_id in self.feature_cache:
            del self.feature_cache[atom_id]
        
        self.stats['total_atoms'] -= 1
        return True
    
    def get_feature_matrix(self, atom_ids: Optional[List[str]] = None) -> np.ndarray:
        """
        Get feature matrix for atoms
        
        Args:
            atom_ids: Optional list of atom IDs. If None, use all atoms.
            
        Returns:
            Feature matrix (n_atoms x n_features)
        """
        if atom_ids is None:
            atom_ids = list(self.atoms.keys())
        
        if not atom_ids:
            return np.array([])
        
        features = [self.feature_cache[aid] for aid in atom_ids if aid in self.feature_cache]
        return np.vstack(features) if features else np.array([])
    
    def train_forest_model(self, domain: str, atom_ids: List[str], 
                          labels: Optional[np.ndarray] = None,
                          model_type: str = "RANDOM_FOREST"):
        """
        Train a decision forest model for a cognitive domain
        
        Args:
            domain: Name of the cognitive domain
            atom_ids: List of atom IDs to train on
            labels: Optional labels for supervised learning
            model_type: Type of forest model (RANDOM_FOREST, GRADIENT_BOOSTED_TREES)
        """
        if ydf is None:
            raise ImportError("Yggdrasil Decision Forests not installed")
        
        features = self.get_feature_matrix(atom_ids)
        
        if features.size == 0:
            self.logger.warning(f"No features available for domain: {domain}")
            return
        
        # For unsupervised learning, use Isolation Forest
        if labels is None:
            # Use isolation forest for anomaly detection / clustering
            self.logger.info(f"Training isolation forest for domain: {domain}")
            # Note: YDF doesn't have isolation forest, so we'll use clustering approach
            # In production, integrate with sklearn's IsolationForest or similar
            return
        
        # Supervised learning
        import pandas as pd
        
        # Create DataFrame for YDF
        feature_names = [f"f{i}" for i in range(features.shape[1])]
        df = pd.DataFrame(features, columns=feature_names)
        df['label'] = labels
        
        # Train model
        if model_type == "RANDOM_FOREST":
            learner = ydf.RandomForestLearner(label="label")
        elif model_type == "GRADIENT_BOOSTED_TREES":
            learner = ydf.GradientBoostedTreesLearner(label="label")
        else:
            raise ValueError(f"Unknown model type: {model_type}")
        
        model = learner.train(df)
        self.forest_models[domain] = model
        
        self.logger.info(f"Trained {model_type} model for domain: {domain}")
    
    def query_forest(self, domain: str, query_features: np.ndarray) -> np.ndarray:
        """
        Query a trained forest model
        
        Args:
            domain: Name of the cognitive domain
            query_features: Feature vector to query
            
        Returns:
            Prediction/similarity scores
        """
        if domain not in self.forest_models:
            raise ValueError(f"No model trained for domain: {domain}")
        
        import pandas as pd
        
        model = self.forest_models[domain]
        feature_names = [f"f{i}" for i in range(query_features.shape[1])]
        df = pd.DataFrame(query_features, columns=feature_names)
        
        predictions = model.predict(df)
        return predictions
    
    def find_similar_atoms(self, atom_id: str, top_k: int = 10) -> List[Tuple[str, float]]:
        """
        Find similar atoms using decision forest similarity
        
        Args:
            atom_id: Reference atom ID
            top_k: Number of similar atoms to return
            
        Returns:
            List of (atom_id, similarity_score) tuples
        """
        if atom_id not in self.atoms:
            return []
        
        ref_features = self.feature_cache[atom_id]
        all_features = self.get_feature_matrix()
        
        if all_features.size == 0:
            return []
        
        # Compute cosine similarity
        ref_norm = np.linalg.norm(ref_features)
        all_norms = np.linalg.norm(all_features, axis=1)
        
        similarities = np.dot(all_features, ref_features) / (all_norms * ref_norm + 1e-10)
        
        # Get top-k (excluding self)
        top_indices = np.argsort(similarities)[::-1][1:top_k+1]
        atom_ids = list(self.atoms.keys())
        
        results = [(atom_ids[idx], float(similarities[idx])) for idx in top_indices]
        return results
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get atomspace statistics"""
        type_counts = {
            atom_type.value: len(atom_ids) 
            for atom_type, atom_ids in self.type_index.items()
        }
        
        return {
            'name': self.name,
            'total_atoms': self.stats['total_atoms'],
            'type_distribution': type_counts,
            'total_queries': self.stats['total_queries'],
            'cache_hit_rate': (
                self.stats['cache_hits'] / 
                max(1, self.stats['cache_hits'] + self.stats['cache_misses'])
            ),
            'forest_models': list(self.forest_models.keys())
        }
    
    def clear(self):
        """Clear all atoms from atomspace"""
        self.atoms.clear()
        self.type_index.clear()
        self.name_index.clear()
        self.incoming_index.clear()
        self.feature_cache.clear()
        self.forest_models.clear()
        self.stats['total_atoms'] = 0
        self.logger.info("Cleared atomspace")
