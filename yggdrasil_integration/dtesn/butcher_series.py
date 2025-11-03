"""
Butcher B-Series Rooted Trees for Temporal Integration

This module implements Butcher B-Series rooted trees for high-order temporal
integration in the Deep Tree Echo State Network. The Butcher series provides
a systematic framework for analyzing and constructing Runge-Kutta methods
through rooted tree structures.

References:
- Butcher, J. C. (1963). "Coefficients for the study of Runge-Kutta integration processes"
- Hairer, E., Nørsett, S. P., & Wanner, G. (2008). "Solving Ordinary Differential Equations I"
"""

import numpy as np
import math
from typing import List, Dict, Tuple, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import logging


class TreeOrder(Enum):
    """Order of Butcher tree (number of vertices)"""
    ORDER_1 = 1  # Single vertex
    ORDER_2 = 2  # Two vertices
    ORDER_3 = 3  # Three vertices
    ORDER_4 = 4  # Four vertices
    ORDER_5 = 5  # Five vertices


@dataclass
class RootedTree:
    """
    Rooted tree structure for Butcher B-Series
    
    A rooted tree is represented by its structure and associated coefficients.
    Each tree corresponds to a term in the B-series expansion.
    """
    order: int  # Number of vertices
    structure: str  # String representation (e.g., "τ", "[τ]", "[[τ]]")
    alpha: float  # Elementary weight (coefficient)
    gamma: int  # Symmetry coefficient
    density: int  # Density (number of monotonic labelings)
    
    def __post_init__(self):
        """Calculate derived properties"""
        self.factorial_order = math.factorial(self.order)
        self.weight = self.alpha / (self.gamma * self.factorial_order)


class ButcherTableau:
    """
    Butcher tableau for Runge-Kutta methods
    
    The tableau encodes the coefficients of a Runge-Kutta method:
    c | A
    -----
      | b^T
    
    where:
    - c: stage nodes
    - A: Runge-Kutta matrix
    - b: weights
    """
    
    def __init__(self, c: np.ndarray, A: np.ndarray, b: np.ndarray):
        """
        Initialize Butcher tableau
        
        Args:
            c: Stage nodes (s-dimensional vector)
            A: Runge-Kutta matrix (s×s matrix)
            b: Weights (s-dimensional vector)
        """
        self.c = np.array(c)
        self.A = np.array(A)
        self.b = np.array(b)
        self.stages = len(c)
        
        self.logger = logging.getLogger(f"{__name__}.ButcherTableau")
        
        # Validate dimensions
        assert self.A.shape == (self.stages, self.stages), "A must be s×s"
        assert len(self.b) == self.stages, "b must be s-dimensional"
        
        # Check consistency: c_i = sum_j a_ij
        for i in range(self.stages):
            assert np.isclose(self.c[i], np.sum(self.A[i, :])), \
                f"Row sum condition violated at stage {i}"
    
    @classmethod
    def explicit_euler(cls):
        """Forward Euler method (order 1)"""
        return cls(
            c=np.array([0.0]),
            A=np.array([[0.0]]),
            b=np.array([1.0])
        )
    
    @classmethod
    def rk4(cls):
        """Classic 4th-order Runge-Kutta method"""
        return cls(
            c=np.array([0.0, 0.5, 0.5, 1.0]),
            A=np.array([
                [0.0, 0.0, 0.0, 0.0],
                [0.5, 0.0, 0.0, 0.0],
                [0.0, 0.5, 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0]
            ]),
            b=np.array([1/6, 1/3, 1/3, 1/6])
        )
    
    @classmethod
    def heun(cls):
        """Heun's method (order 2)"""
        return cls(
            c=np.array([0.0, 1.0]),
            A=np.array([
                [0.0, 0.0],
                [1.0, 0.0]
            ]),
            b=np.array([0.5, 0.5])
        )
    
    @classmethod
    def midpoint(cls):
        """Midpoint method (order 2)"""
        return cls(
            c=np.array([0.0, 0.5]),
            A=np.array([
                [0.0, 0.0],
                [0.5, 0.0]
            ]),
            b=np.array([0.0, 1.0])
        )
    
    @classmethod
    def rk38(cls):
        """3/8-rule Runge-Kutta method (order 4)"""
        return cls(
            c=np.array([0.0, 1/3, 2/3, 1.0]),
            A=np.array([
                [0.0, 0.0, 0.0, 0.0],
                [1/3, 0.0, 0.0, 0.0],
                [-1/3, 1.0, 0.0, 0.0],
                [1.0, -1.0, 1.0, 0.0]
            ]),
            b=np.array([1/8, 3/8, 3/8, 1/8])
        )


class ButcherBSeries:
    """
    Butcher B-Series for analyzing Runge-Kutta methods
    
    The B-series provides a formal framework for representing the solution
    of ODEs as an infinite series indexed by rooted trees.
    """
    
    def __init__(self, max_order: int = 4):
        """
        Initialize B-series with rooted trees up to given order
        
        Args:
            max_order: Maximum tree order to generate
        """
        self.max_order = max_order
        self.trees: Dict[int, List[RootedTree]] = {}
        self.logger = logging.getLogger(f"{__name__}.ButcherBSeries")
        
        # Generate rooted trees up to max_order
        self._generate_trees()
    
    def _generate_trees(self):
        """Generate rooted trees up to max_order"""
        # Order 1: Single vertex τ
        self.trees[1] = [
            RootedTree(order=1, structure="τ", alpha=1.0, gamma=1, density=1)
        ]
        
        # Order 2: [τ]
        self.trees[2] = [
            RootedTree(order=2, structure="[τ]", alpha=1.0, gamma=1, density=1)
        ]
        
        # Order 3: [[τ]], [τ,τ]
        self.trees[3] = [
            RootedTree(order=3, structure="[[τ]]", alpha=1.0, gamma=1, density=1),
            RootedTree(order=3, structure="[τ,τ]", alpha=1.0, gamma=2, density=1)
        ]
        
        # Order 4: [[[τ]]], [[τ,τ]], [[τ],[τ]], [τ,τ,τ]
        self.trees[4] = [
            RootedTree(order=4, structure="[[[τ]]]", alpha=1.0, gamma=1, density=1),
            RootedTree(order=4, structure="[[τ,τ]]", alpha=1.0, gamma=2, density=1),
            RootedTree(order=4, structure="[[τ],[τ]]", alpha=1.0, gamma=1, density=2),
            RootedTree(order=4, structure="[τ,τ,τ]", alpha=1.0, gamma=6, density=1)
        ]
        
        # Order 5 (partial - common trees)
        if self.max_order >= 5:
            self.trees[5] = [
                RootedTree(order=5, structure="[[[[τ]]]]", alpha=1.0, gamma=1, density=1),
                RootedTree(order=5, structure="[[[τ,τ]]]", alpha=1.0, gamma=2, density=1),
                RootedTree(order=5, structure="[[[τ],[τ]]]", alpha=1.0, gamma=1, density=2),
                RootedTree(order=5, structure="[[τ,τ,τ]]", alpha=1.0, gamma=6, density=1),
                RootedTree(order=5, structure="[[τ],[τ,τ]]", alpha=1.0, gamma=2, density=2),
                RootedTree(order=5, structure="[[τ],[τ],[τ]]", alpha=1.0, gamma=1, density=6),
                RootedTree(order=5, structure="[τ,τ,τ,τ]", alpha=1.0, gamma=24, density=1)
            ]
        
        self.logger.info(f"Generated {sum(len(trees) for trees in self.trees.values())} rooted trees up to order {self.max_order}")
    
    def get_trees(self, order: int) -> List[RootedTree]:
        """Get all rooted trees of given order"""
        return self.trees.get(order, [])
    
    def compute_elementary_weight(self, tree: RootedTree, tableau: ButcherTableau) -> float:
        """
        Compute elementary weight for a tree given a Butcher tableau
        
        Args:
            tree: Rooted tree
            tableau: Butcher tableau
            
        Returns:
            Elementary weight Φ(tree)
        """
        # This is a simplified implementation
        # Full implementation would recursively compute based on tree structure
        
        if tree.order == 1:
            # Φ(τ) = Σ b_i
            return np.sum(tableau.b)
        
        elif tree.order == 2:
            # Φ([τ]) = Σ b_i c_i
            return np.sum(tableau.b * tableau.c)
        
        elif tree.order == 3:
            if tree.structure == "[[τ]]":
                # Φ([[τ]]) = Σ b_i c_i^2
                return np.sum(tableau.b * tableau.c**2)
            elif tree.structure == "[τ,τ]":
                # Φ([τ,τ]) = Σ b_i Σ a_ij c_j
                result = 0.0
                for i in range(tableau.stages):
                    result += tableau.b[i] * np.sum(tableau.A[i, :] * tableau.c)
                return result
        
        elif tree.order == 4:
            if tree.structure == "[[[τ]]]":
                # Φ([[[τ]]]) = Σ b_i c_i^3
                return np.sum(tableau.b * tableau.c**3)
            elif tree.structure == "[[τ,τ]]":
                # Φ([[τ,τ]]) = Σ b_i c_i Σ a_ij c_j
                result = 0.0
                for i in range(tableau.stages):
                    result += tableau.b[i] * tableau.c[i] * np.sum(tableau.A[i, :] * tableau.c)
                return result
            elif tree.structure == "[[τ],[τ]]":
                # Φ([[τ],[τ]]) = Σ b_i Σ a_ij c_j^2
                result = 0.0
                for i in range(tableau.stages):
                    result += tableau.b[i] * np.sum(tableau.A[i, :] * tableau.c**2)
                return result
            elif tree.structure == "[τ,τ,τ]":
                # Φ([τ,τ,τ]) = Σ b_i Σ a_ij Σ a_jk c_k
                result = 0.0
                for i in range(tableau.stages):
                    for j in range(tableau.stages):
                        result += tableau.b[i] * tableau.A[i, j] * np.sum(tableau.A[j, :] * tableau.c)
                return result
        
        # Default: return approximate value
        return tree.alpha / tree.gamma
    
    def order_conditions(self, tableau: ButcherTableau, target_order: int) -> Dict[str, float]:
        """
        Check order conditions for a Butcher tableau
        
        Args:
            tableau: Butcher tableau to check
            target_order: Desired order of accuracy
            
        Returns:
            Dictionary mapping tree structures to residuals
        """
        conditions = {}
        
        for order in range(1, min(target_order + 1, self.max_order + 1)):
            for tree in self.get_trees(order):
                weight = self.compute_elementary_weight(tree, tableau)
                exact_weight = 1.0 / tree.factorial_order
                residual = abs(weight - exact_weight)
                conditions[f"Order {order}: {tree.structure}"] = residual
        
        return conditions
    
    def verify_method(self, tableau: ButcherTableau, target_order: int, tolerance: float = 1e-10) -> bool:
        """
        Verify that a Runge-Kutta method achieves target order
        
        Args:
            tableau: Butcher tableau
            target_order: Target order of accuracy
            tolerance: Tolerance for order conditions
            
        Returns:
            True if method achieves target order
        """
        conditions = self.order_conditions(tableau, target_order)
        
        for condition, residual in conditions.items():
            if residual > tolerance:
                self.logger.warning(f"Order condition violated: {condition} (residual: {residual:.2e})")
                return False
        
        self.logger.info(f"Method verified to order {target_order}")
        return True


class TemporalIntegrator:
    """
    Temporal integrator using Butcher B-Series and Runge-Kutta methods
    
    This class provides high-order temporal integration for reservoir dynamics
    using the Butcher series framework.
    """
    
    def __init__(self, tableau: ButcherTableau, adaptive: bool = False):
        """
        Initialize temporal integrator
        
        Args:
            tableau: Butcher tableau for the RK method
            adaptive: Whether to use adaptive step size
        """
        self.tableau = tableau
        self.adaptive = adaptive
        self.logger = logging.getLogger(f"{__name__}.TemporalIntegrator")
        
        # Initialize B-series for analysis
        self.bseries = ButcherBSeries(max_order=4)
        
        # Verify method order
        self.order = self._determine_order()
        self.logger.info(f"Initialized {self.order}-order temporal integrator")
    
    def _determine_order(self) -> int:
        """Determine the order of the RK method"""
        for order in range(1, 5):
            if not self.bseries.verify_method(self.tableau, order):
                return order - 1
        return 4
    
    def step(self, 
             f: Callable[[float, np.ndarray], np.ndarray],
             t: float,
             y: np.ndarray,
             h: float) -> Tuple[float, np.ndarray]:
        """
        Take a single integration step
        
        Args:
            f: Right-hand side function dy/dt = f(t, y)
            t: Current time
            y: Current state
            h: Step size
            
        Returns:
            Tuple of (new_time, new_state)
        """
        # Compute stage values
        k = np.zeros((self.tableau.stages, len(y)))
        
        for i in range(self.tableau.stages):
            t_i = t + self.tableau.c[i] * h
            y_i = y + h * np.sum(self.tableau.A[i, :, np.newaxis] * k, axis=0)
            k[i] = f(t_i, y_i)
        
        # Compute next state
        y_new = y + h * np.sum(self.tableau.b[:, np.newaxis] * k, axis=0)
        t_new = t + h
        
        return t_new, y_new
    
    def integrate(self,
                  f: Callable[[float, np.ndarray], np.ndarray],
                  t_span: Tuple[float, float],
                  y0: np.ndarray,
                  h: float = 0.01,
                  max_steps: int = 10000) -> Tuple[np.ndarray, np.ndarray]:
        """
        Integrate from t_span[0] to t_span[1]
        
        Args:
            f: Right-hand side function
            t_span: Time span (t0, tf)
            y0: Initial state
            h: Step size
            max_steps: Maximum number of steps
            
        Returns:
            Tuple of (times, states)
        """
        t0, tf = t_span
        t = t0
        y = y0.copy()
        
        times = [t]
        states = [y.copy()]
        
        steps = 0
        while t < tf and steps < max_steps:
            # Adjust final step
            if t + h > tf:
                h = tf - t
            
            t, y = self.step(f, t, y, h)
            
            times.append(t)
            states.append(y.copy())
            steps += 1
        
        return np.array(times), np.array(states)
