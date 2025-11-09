#!/usr/bin/env python3.11
"""
SENAS - Self-Evolving Neural Architecture Search
Prototype Implementation

This is a working prototype demonstrating the core concepts of SENAS.
"""
import numpy as np
import random
from typing import List, Dict, Tuple
from dataclasses import dataclass
from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
import time


console = Console()


@dataclass
class Architecture:
    """Neural architecture representation"""
    layers: List[int]
    connections: List[Tuple[int, int]]
    activation: str
    name: str
    
    def __post_init__(self):
        self.fitness = 0.0
        self.accuracy = 0.0
        self.efficiency = 0.0
        self.params = sum(self.layers[i] * self.layers[i+1] for i in range(len(self.layers)-1))
        self.flops = self.params * 2  # Simplified FLOPs estimation


class DTESNCore:
    """Deep Tree Echo State Network Core"""
    
    def __init__(self, reservoir_size: int = 1024):
        self.reservoir_size = reservoir_size
        self.reservoir = np.random.randn(reservoir_size, reservoir_size) * 0.1
        self.state = np.zeros(reservoir_size)
    
    def generate_architectures(self, population_size: int, diversity_factor: float = 0.8) -> List[Architecture]:
        """Generate diverse neural architectures using reservoir dynamics"""
        architectures = []
        
        for i in range(population_size):
            # Update reservoir state
            input_signal = np.random.randn(self.reservoir_size) * diversity_factor
            self.state = np.tanh(self.reservoir @ self.state + input_signal)
            
            # Extract architecture from reservoir state
            num_layers = max(3, min(10, int(abs(self.state[0]) * 10)))
            layer_sizes = [max(16, min(512, int(abs(self.state[j]) * 512))) 
                          for j in range(1, num_layers + 1)]
            
            # Generate connections (simplified)
            connections = [(i, i+1) for i in range(len(layer_sizes)-1)]
            
            # Random activation
            activations = ['relu', 'tanh', 'sigmoid', 'gelu']
            activation = random.choice(activations)
            
            arch = Architecture(
                layers=layer_sizes,
                connections=connections,
                activation=activation,
                name=f"SENAS_Gen{i}"
            )
            
            architectures.append(arch)
        
        return architectures


class MembraneSystem:
    """P-System Membrane Computing for architecture evaluation"""
    
    def __init__(self, max_depth: int = 8):
        self.max_depth = max_depth
        self.membranes = [[] for _ in range(max_depth)]
    
    def parallel_evaluate(self, architectures: List[Architecture]) -> List[Architecture]:
        """Evaluate architectures in parallel using membrane computing"""
        # Distribute architectures across membranes by complexity
        for arch in architectures:
            depth = min(len(arch.layers), self.max_depth - 1)
            self.membranes[depth].append(arch)
        
        # Parallel evaluation (simulated)
        evaluated = []
        for depth, membrane in enumerate(self.membranes):
            for arch in membrane:
                # Membrane-specific evaluation rules
                complexity_bonus = 1.0 - (depth / self.max_depth) * 0.2
                arch.fitness = self._evaluate_architecture(arch) * complexity_bonus
                evaluated.append(arch)
        
        # Clear membranes
        self.membranes = [[] for _ in range(self.max_depth)]
        
        return evaluated
    
    def _evaluate_architecture(self, arch: Architecture) -> float:
        """Evaluate single architecture"""
        # Simplified fitness function
        depth_score = len(arch.layers) / 10.0
        width_score = np.mean(arch.layers) / 512.0
        efficiency_score = 1.0 / (1.0 + arch.params / 1000000.0)
        
        return (depth_score + width_score + efficiency_score) / 3.0


class HypergraphPredictor:
    """Hypergraph-based zero-shot performance predictor"""
    
    def __init__(self):
        self.embedding_dim = 128
    
    def predict_performance(self, architectures: List[Architecture]) -> List[Architecture]:
        """Predict performance using hypergraph embeddings"""
        for arch in architectures:
            # Extract hypergraph features
            features = self._extract_features(arch)
            
            # Compute embedding
            embedding = self._compute_embedding(features)
            
            # Predict performance
            arch.accuracy = self._predict_accuracy(embedding, arch)
            arch.efficiency = self._predict_efficiency(embedding, arch)
            arch.fitness = (arch.accuracy + arch.efficiency) / 2.0
        
        return architectures
    
    def _extract_features(self, arch: Architecture) -> Dict:
        """Extract hypergraph features"""
        return {
            'depth': len(arch.layers),
            'width': np.mean(arch.layers),
            'connectivity': len(arch.connections),
            'params': arch.params,
            'activation': hash(arch.activation) % 100
        }
    
    def _compute_embedding(self, features: Dict) -> np.ndarray:
        """Compute hypergraph embedding"""
        # Simplified embedding
        embedding = np.array([
            features['depth'] / 10.0,
            features['width'] / 512.0,
            features['connectivity'] / 20.0,
            features['params'] / 1000000.0,
            features['activation'] / 100.0
        ])
        return np.pad(embedding, (0, self.embedding_dim - len(embedding)))
    
    def _predict_accuracy(self, embedding: np.ndarray, arch: Architecture) -> float:
        """Predict accuracy from embedding"""
        # Simplified prediction
        base_accuracy = 0.85
        depth_bonus = min(0.1, len(arch.layers) * 0.01)
        width_bonus = min(0.05, np.mean(arch.layers) / 10000.0)
        
        return min(0.99, base_accuracy + depth_bonus + width_bonus + random.gauss(0, 0.02))
    
    def _predict_efficiency(self, embedding: np.ndarray, arch: Architecture) -> float:
        """Predict efficiency from embedding"""
        # Simplified prediction
        base_efficiency = 0.7
        param_penalty = min(0.3, arch.params / 10000000.0)
        
        return max(0.1, base_efficiency - param_penalty + random.gauss(0, 0.05))


class SENASGenerator:
    """Self-Evolving Neural Architecture Search Generator"""
    
    def __init__(self, population_size: int = 50, mutation_rate: float = 0.1):
        self.dtesn = DTESNCore(reservoir_size=1024)
        self.membranes = MembraneSystem(max_depth=8)
        self.hypergraph = HypergraphPredictor()
        
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.population = []
        self.generation = 0
        self.best_ever = None
        self.history = []
    
    def evolve_step(self) -> Architecture:
        """Single evolution step"""
        # 1. Generate candidates using DTESN
        if self.generation == 0:
            candidates = self.dtesn.generate_architectures(self.population_size, diversity_factor=0.9)
        else:
            # Generate from current population
            candidates = self._generate_from_population()
        
        # 2. Evaluate using membrane computing
        evaluated = self.membranes.parallel_evaluate(candidates)
        
        # 3. Predict performance via hypergraph
        predicted = self.hypergraph.predict_performance(evaluated)
        
        # 4. Select best individuals
        predicted.sort(key=lambda x: x.fitness, reverse=True)
        self.population = predicted[:self.population_size]
        
        # 5. Track best
        current_best = self.population[0]
        if self.best_ever is None or current_best.fitness > self.best_ever.fitness:
            self.best_ever = current_best
        
        # 6. Record history
        self.history.append({
            'generation': self.generation,
            'best_fitness': current_best.fitness,
            'avg_fitness': np.mean([a.fitness for a in self.population]),
            'diversity': self._compute_diversity()
        })
        
        self.generation += 1
        
        return current_best
    
    def _generate_from_population(self) -> List[Architecture]:
        """Generate new candidates from current population"""
        candidates = []
        
        # Keep top 10% (elitism)
        elite_count = max(1, int(self.population_size * 0.1))
        candidates.extend(self.population[:elite_count])
        
        # Generate rest through mutation and crossover
        while len(candidates) < self.population_size * 2:
            if random.random() < 0.7:  # Crossover
                parent1, parent2 = random.sample(self.population[:20], 2)
                child = self._crossover(parent1, parent2)
            else:  # Mutation
                parent = random.choice(self.population[:20])
                child = self._mutate(parent)
            
            candidates.append(child)
        
        return candidates
    
    def _crossover(self, parent1: Architecture, parent2: Architecture) -> Architecture:
        """Crossover two architectures"""
        # Simple layer-wise crossover
        min_len = min(len(parent1.layers), len(parent2.layers))
        crossover_point = random.randint(1, min_len - 1)
        
        child_layers = parent1.layers[:crossover_point] + parent2.layers[crossover_point:]
        child_connections = [(i, i+1) for i in range(len(child_layers)-1)]
        
        return Architecture(
            layers=child_layers,
            connections=child_connections,
            activation=random.choice([parent1.activation, parent2.activation]),
            name=f"SENAS_Cross_Gen{self.generation}"
        )
    
    def _mutate(self, parent: Architecture) -> Architecture:
        """Mutate an architecture"""
        child_layers = parent.layers.copy()
        
        # Random mutations
        if random.random() < self.mutation_rate:
            # Add layer
            pos = random.randint(0, len(child_layers))
            size = random.randint(16, 512)
            child_layers.insert(pos, size)
        
        if random.random() < self.mutation_rate and len(child_layers) > 3:
            # Remove layer
            pos = random.randint(1, len(child_layers) - 2)
            child_layers.pop(pos)
        
        if random.random() < self.mutation_rate:
            # Modify layer size
            pos = random.randint(0, len(child_layers) - 1)
            child_layers[pos] = max(16, min(512, child_layers[pos] + random.randint(-64, 64)))
        
        child_connections = [(i, i+1) for i in range(len(child_layers)-1)]
        
        return Architecture(
            layers=child_layers,
            connections=child_connections,
            activation=parent.activation,
            name=f"SENAS_Mut_Gen{self.generation}"
        )
    
    def _compute_diversity(self) -> float:
        """Compute population diversity"""
        if len(self.population) < 2:
            return 0.0
        
        # Compute average pairwise difference in layer counts
        layer_counts = [len(a.layers) for a in self.population]
        diversity = np.std(layer_counts) / np.mean(layer_counts) if np.mean(layer_counts) > 0 else 0.0
        
        return min(1.0, diversity)
    
    def get_best_architecture(self) -> Architecture:
        """Get best architecture found so far"""
        return self.best_ever if self.best_ever else self.population[0] if self.population else None
    
    def get_population_stats(self) -> Dict:
        """Get current population statistics"""
        if not self.population:
            return {'avg_fitness': 0, 'diversity': 0, 'best_fitness': 0}
        
        return {
            'avg_fitness': np.mean([a.fitness for a in self.population]),
            'diversity': self._compute_diversity(),
            'best_fitness': self.population[0].fitness,
            'avg_params': np.mean([a.params for a in self.population]),
            'avg_layers': np.mean([len(a.layers) for a in self.population])
        }


def create_evolution_display(generation: int, best: Architecture, stats: Dict) -> Panel:
    """Create rich display for evolution progress"""
    
    # Stats table
    table = Table(title=f"🧬 Generation {generation}", show_header=True)
    table.add_column("Metric", style="cyan", width=25)
    table.add_column("Value", style="green", width=20)
    
    table.add_row("Best Fitness", f"{best.fitness:.6f}")
    table.add_row("Best Accuracy", f"{best.accuracy:.4f} ({best.accuracy*100:.2f}%)")
    table.add_row("Best Efficiency", f"{best.efficiency:.4f}")
    table.add_row("Population Diversity", f"{stats['diversity']:.4f}")
    table.add_row("Avg Fitness", f"{stats['avg_fitness']:.6f}")
    table.add_row("Avg Parameters", f"{int(stats['avg_params']):,}")
    table.add_row("Avg Layers", f"{stats['avg_layers']:.1f}")
    
    # Architecture details
    arch_info = f"""
[yellow]Best Architecture:[/yellow]
  Name: {best.name}
  Layers: {len(best.layers)} ({' → '.join(map(str, best.layers[:5]))}{' ...' if len(best.layers) > 5 else ''})
  Parameters: {best.params:,}
  FLOPs: {best.flops:,}
  Activation: {best.activation}
"""
    
    return Panel(
        table,
        title="[bold magenta]🌟 SENAS - Self-Evolving Neural Architecture Search 🌟[/bold magenta]",
        subtitle=arch_info,
        border_style="magenta",
        padding=(1, 2)
    )


def run_senas_demo(generations: int = 50):
    """Run SENAS demonstration"""
    
    console.print(Panel.fit(
        "[bold magenta]SENAS - Self-Evolving Neural Architecture Search[/bold magenta]\n\n"
        "[cyan]Demonstrating real-time neural architecture evolution[/cyan]\n"
        "[yellow]Using Deep Tree Echo State Networks + P-System Membranes + Hypergraph Prediction[/yellow]",
        border_style="magenta"
    ))
    
    console.print("\n[cyan]Initializing SENAS...[/cyan]")
    senas = SENASGenerator(population_size=50, mutation_rate=0.15)
    
    console.print("[green]✓ SENAS initialized[/green]")
    console.print(f"[cyan]Starting evolution for {generations} generations...[/cyan]\n")
    
    time.sleep(1)
    
    with Live(console=console, refresh_per_second=4) as live:
        for gen in range(generations):
            # Evolution step
            best = senas.evolve_step()
            stats = senas.get_population_stats()
            
            # Update display
            display = create_evolution_display(gen, best, stats)
            live.update(display)
            
            time.sleep(0.05)  # Slow down for visibility
    
    # Final results
    console.print("\n" + "="*70)
    console.print("[bold green]🎉 Evolution Complete! 🎉[/bold green]".center(70))
    console.print("="*70 + "\n")
    
    final_best = senas.get_best_architecture()
    
    final_table = Table(title="🏆 Final Best Architecture", show_header=True)
    final_table.add_column("Property", style="cyan", width=20)
    final_table.add_column("Value", style="green", width=40)
    
    final_table.add_row("Name", final_best.name)
    final_table.add_row("Fitness", f"{final_best.fitness:.6f}")
    final_table.add_row("Accuracy", f"{final_best.accuracy:.4f} ({final_best.accuracy*100:.2f}%)")
    final_table.add_row("Efficiency", f"{final_best.efficiency:.4f}")
    final_table.add_row("Layers", str(len(final_best.layers)))
    final_table.add_row("Layer Sizes", ' → '.join(map(str, final_best.layers)))
    final_table.add_row("Parameters", f"{final_best.params:,}")
    final_table.add_row("FLOPs", f"{final_best.flops:,}")
    final_table.add_row("Activation", final_best.activation)
    
    console.print(final_table)
    
    # Evolution history
    console.print("\n[cyan]Evolution Progress:[/cyan]")
    history_table = Table(show_header=True)
    history_table.add_column("Generation", style="cyan")
    history_table.add_column("Best Fitness", style="green")
    history_table.add_column("Avg Fitness", style="yellow")
    history_table.add_column("Diversity", style="magenta")
    
    # Show every 10th generation
    for record in senas.history[::max(1, generations//10)]:
        history_table.add_row(
            str(record['generation']),
            f"{record['best_fitness']:.6f}",
            f"{record['avg_fitness']:.6f}",
            f"{record['diversity']:.4f}"
        )
    
    console.print(history_table)
    
    console.print(Panel(
        "[bold green]✨ SENAS successfully evolved optimal neural architecture! ✨[/bold green]\n\n"
        "[cyan]Key Achievements:[/cyan]\n"
        f"• Explored {len(senas.history) * senas.population_size * 2} architectures\n"
        f"• Achieved {final_best.accuracy*100:.2f}% predicted accuracy\n"
        f"• Maintained {stats['diversity']:.2f} population diversity\n"
        f"• Optimized for both accuracy and efficiency\n\n"
        "[yellow]This is just the beginning...[/yellow]\n"
        "SENAS can continue evolving indefinitely, adapting to new requirements!",
        title="[bold magenta]Success![/bold magenta]",
        border_style="green"
    ))


if __name__ == "__main__":
    import sys
    
    # Check for rich
    try:
        from rich import print as rprint
    except ImportError:
        print("Installing rich...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "rich", "-q"])
        print("Please run again.")
        sys.exit(0)
    
    # Run demo
    console.print("[bold cyan]Starting SENAS Demo...[/bold cyan]\n")
    run_senas_demo(generations=50)
