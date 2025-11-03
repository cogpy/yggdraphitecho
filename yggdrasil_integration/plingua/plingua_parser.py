"""
P-Lingua Parser for Relevance Realization Membranes

This module implements a Python parser for P-Lingua^{RR} - the extended
P-Lingua syntax for Relevance Realization membrane computing.

The parser converts P-Lingua^{RR} source code into executable membrane
structures that integrate with the Yggdrasil atomspace and triadic
correspondence system.

Grammar: 𝔊^{RR-Π} = (N, Σ, P, S)
"""

import re
from typing import List, Dict, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import logging


class TrialecticLevel(Enum):
    """Trialectic levels in RR hierarchy"""
    AUTOPOIESIS = 1  # Λ¹: Self-manufacture
    ANTICIPATION = 2  # Λ²: Projective dynamics
    ADAPTATION = 3  # Λ³: Agent-arena dynamics


class TargetDirection(Enum):
    """Target directions for trialectic rules"""
    AUTO = "↓"  # Autopoietic
    ANTIC = "↑"  # Anticipatory
    ADAPT = "↔"  # Adaptive


@dataclass
class Triad:
    """
    Triadic structure (x, y, z) with mutual constitution
    
    Represents: {(x,y,z) | x ⊗^η y ⊗^η z, ∀^ω(x ⇔^α y ⇔^α z ⇔^α x)}
    """
    x: str
    y: str
    z: str
    coherence: float = 0.0
    
    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"


@dataclass
class Affordance:
    """
    Affordance φ(agent, arena) in transjective space
    
    Represents: φ ∈ ℍ^{transjective}
    """
    agent: str
    arena: str
    polarity: str  # '+', '-', or '0'
    strength: float = 0.0


@dataclass
class TrialecticRule:
    """
    Trialectic transformation rule
    
    Represents: r^Θ: (x,y,z)ᵢ →^{co-const} (x',y',z')ⱼ ⟨Target⟩ ⟨Constraint⟩
    """
    rule_id: str
    source_triad: Triad
    target_triad: Triad
    target_direction: TargetDirection
    constraints: List[str] = field(default_factory=list)
    membrane: Optional[str] = None


@dataclass
class LambdaMembrane:
    """
    Membrane at trialectic level Λⁱ
    
    Represents: [λᵢ ⟨Trialectic-Content⟩]^{Λⁱ}
    """
    level: TrialecticLevel
    name: str
    triads: List[Triad] = field(default_factory=list)
    rules: List[TrialecticRule] = field(default_factory=list)
    children: List['LambdaMembrane'] = field(default_factory=list)
    coherence: float = 0.0


@dataclass
class AgentArena:
    """
    Agent-arena boundary
    
    Represents: ⟦⟨Agent-Arena⟩⟧^{Ω} where Ω ∈ ℂ^{evolutionary}
    """
    name: str
    membranes: List[LambdaMembrane] = field(default_factory=list)
    affordances: List[Affordance] = field(default_factory=list)
    coupling_strength: float = 0.0


@dataclass
class ThetaSystem:
    """
    Complete Θ-system
    
    Represents the entire relevance realization system
    """
    model_name: str
    agent_arenas: List[AgentArena] = field(default_factory=list)
    constraints: Dict[str, str] = field(default_factory=dict)
    relevance_gradient: float = 0.0


class PLinguaParser:
    """
    Parser for P-Lingua^{RR} membrane computing language
    
    Parses P-Lingua source code into executable Θ-system structures
    """
    
    def __init__(self):
        """Initialize P-Lingua parser"""
        self.logger = logging.getLogger(f"{__name__}.PLinguaParser")
        
        # Token patterns
        self.patterns = {
            'model': r'@model<([^>]+)>',
            'theta_system': r'@Θ-system\s+(\w+)',
            'agent_arena': r'@agent_arena\s+(\w+)',
            'lambda': r'@lambda\[(\d+)\]\s+\'(\w+)',
            'triad': r'\(([^,]+),\s*([^,]+),\s*([^)]+)\)',
            'rule': r'\[([^\]]+)\]\s*\'(\w+)',
            'affordances': r'@affordances\s*=\s*\{([^}]+)\}',
            'constraints': r'@constraints\s*\{([^}]+)\}',
            'emergence': r'@emergence\s+(\w+)',
        }
        
        self.logger.info("Initialized P-Lingua^{RR} parser")
    
    def parse(self, source: str) -> ThetaSystem:
        """
        Parse P-Lingua source into Θ-system
        
        Args:
            source: P-Lingua source code
            
        Returns:
            Parsed Θ-system
        """
        self.logger.info("Parsing P-Lingua source")
        
        # Extract model name
        model_match = re.search(self.patterns['model'], source)
        model_name = model_match.group(1) if model_match else "unnamed_model"
        
        # Create Θ-system
        theta_system = ThetaSystem(model_name=model_name)
        
        # Parse Θ-system block
        theta_match = re.search(self.patterns['theta_system'], source)
        if theta_match:
            theta_name = theta_match.group(1)
            self.logger.debug(f"Found Θ-system: {theta_name}")
        
        # Parse agent-arena blocks
        agent_arenas = self._parse_agent_arenas(source)
        theta_system.agent_arenas = agent_arenas
        
        # Parse constraints
        constraints = self._parse_constraints(source)
        theta_system.constraints = constraints
        
        self.logger.info(
            f"Parsed Θ-system '{model_name}' with "
            f"{len(agent_arenas)} agent-arenas"
        )
        
        return theta_system
    
    def _parse_agent_arenas(self, source: str) -> List[AgentArena]:
        """Parse agent-arena blocks"""
        agent_arenas = []
        
        # Find all agent-arena blocks
        for match in re.finditer(self.patterns['agent_arena'], source):
            name = match.group(1)
            
            # Extract block content (simplified - would need proper block parsing)
            agent_arena = AgentArena(name=name)
            
            # Parse membranes within this agent-arena
            membranes = self._parse_membranes(source)
            agent_arena.membranes = membranes
            
            # Parse affordances
            affordances = self._parse_affordances(source)
            agent_arena.affordances = affordances
            
            agent_arenas.append(agent_arena)
            
            self.logger.debug(
                f"Parsed agent-arena '{name}' with {len(membranes)} membranes"
            )
        
        return agent_arenas
    
    def _parse_membranes(self, source: str) -> List[LambdaMembrane]:
        """Parse lambda membranes"""
        membranes = []
        
        for match in re.finditer(self.patterns['lambda'], source):
            level_num = int(match.group(1))
            name = match.group(2)
            
            # Map level number to trialectic level
            level_map = {
                1: TrialecticLevel.AUTOPOIESIS,
                2: TrialecticLevel.ANTICIPATION,
                3: TrialecticLevel.ADAPTATION
            }
            
            level = level_map.get(level_num, TrialecticLevel.AUTOPOIESIS)
            
            membrane = LambdaMembrane(level=level, name=name)
            
            # Parse triads within membrane (simplified)
            triads = self._parse_triads(source)
            membrane.triads = triads
            
            # Parse rules
            rules = self._parse_rules(source, name)
            membrane.rules = rules
            
            membranes.append(membrane)
            
            self.logger.debug(
                f"Parsed membrane '{name}' at level {level.value} "
                f"with {len(triads)} triads"
            )
        
        return membranes
    
    def _parse_triads(self, source: str) -> List[Triad]:
        """Parse triadic structures"""
        triads = []
        
        for match in re.finditer(self.patterns['triad'], source):
            x = match.group(1).strip()
            y = match.group(2).strip()
            z = match.group(3).strip()
            
            triad = Triad(x=x, y=y, z=z)
            triads.append(triad)
        
        return triads
    
    def _parse_rules(self, source: str, membrane_name: str) -> List[TrialecticRule]:
        """Parse trialectic transformation rules"""
        rules = []
        
        for match in re.finditer(self.patterns['rule'], source):
            rule_content = match.group(1)
            rule_membrane = match.group(2)
            
            if rule_membrane != membrane_name:
                continue
            
            # Parse rule content (simplified)
            # Format: [source --> target]'membrane
            if '-->' in rule_content:
                parts = rule_content.split('-->')
                source_part = parts[0].strip()
                target_part = parts[1].strip() if len(parts) > 1 else source_part
                
                # Extract triads from source and target
                source_triad = self._extract_triad_from_rule(source_part)
                target_triad = self._extract_triad_from_rule(target_part)
                
                if source_triad and target_triad:
                    rule = TrialecticRule(
                        rule_id=f"r_{len(rules)}",
                        source_triad=source_triad,
                        target_triad=target_triad,
                        target_direction=TargetDirection.AUTO,
                        membrane=membrane_name
                    )
                    rules.append(rule)
        
        return rules
    
    def _extract_triad_from_rule(self, rule_part: str) -> Optional[Triad]:
        """Extract triad from rule part"""
        # Look for comma-separated elements
        elements = [e.strip() for e in rule_part.split(',')]
        
        if len(elements) >= 3:
            return Triad(x=elements[0], y=elements[1], z=elements[2])
        
        return None
    
    def _parse_affordances(self, source: str) -> List[Affordance]:
        """Parse affordance specifications"""
        affordances = []
        
        match = re.search(self.patterns['affordances'], source)
        if match:
            content = match.group(1)
            
            # Parse affordance triads
            for triad_match in re.finditer(self.patterns['triad'], content):
                agent = triad_match.group(1).strip()
                arena = triad_match.group(2).strip()
                
                affordance = Affordance(
                    agent=agent,
                    arena=arena,
                    polarity='+'
                )
                affordances.append(affordance)
        
        return affordances
    
    def _parse_constraints(self, source: str) -> Dict[str, str]:
        """Parse constraint specifications"""
        constraints = {}
        
        match = re.search(self.patterns['constraints'], source)
        if match:
            content = match.group(1)
            
            # Parse constraint lines
            for line in content.split(';'):
                line = line.strip()
                if ':' in line:
                    parts = line.split(':', 1)
                    name = parts[0].strip()
                    expr = parts[1].strip()
                    constraints[name] = expr
        
        return constraints
    
    def generate_code(self, theta_system: ThetaSystem) -> str:
        """
        Generate P-Lingua code from Θ-system
        
        Args:
            theta_system: Θ-system to generate code for
            
        Returns:
            P-Lingua source code
        """
        lines = []
        
        # Model declaration
        lines.append(f"@model<{theta_system.model_name}>")
        lines.append("")
        
        # Θ-system declaration
        lines.append(f"@Θ-system {theta_system.model_name} {{")
        lines.append("")
        
        # Agent-arenas
        for aa in theta_system.agent_arenas:
            lines.append(f"    @agent_arena {aa.name} {{")
            lines.append("")
            
            # Membranes
            for membrane in aa.membranes:
                lines.append(f"        @lambda[{membrane.level.value}] '{membrane.name} {{")
                
                # Triads
                for triad in membrane.triads:
                    lines.append(f"            {triad};")
                
                # Rules
                for rule in membrane.rules:
                    lines.append(
                        f"            [{rule.source_triad} --> {rule.target_triad}]'"
                        f"{rule.membrane}"
                    )
                
                lines.append("        }")
                lines.append("")
            
            lines.append("    }")
            lines.append("")
        
        # Constraints
        if theta_system.constraints:
            lines.append("    @constraints {")
            for name, expr in theta_system.constraints.items():
                lines.append(f"        {name} : {expr};")
            lines.append("    }")
        
        lines.append("}")
        
        return "\n".join(lines)


class PLinguaInterpreter:
    """
    Interpreter for executing P-Lingua^{RR} programs
    
    Executes parsed Θ-systems with trialectic dynamics
    """
    
    def __init__(self, theta_system: ThetaSystem):
        """
        Initialize interpreter
        
        Args:
            theta_system: Parsed Θ-system to execute
        """
        self.theta_system = theta_system
        self.logger = logging.getLogger(f"{__name__}.PLinguaInterpreter")
        
        # Execution state
        self.current_step = 0
        self.max_steps = 1000
        
        self.logger.info(f"Initialized interpreter for {theta_system.model_name}")
    
    def step(self) -> bool:
        """
        Execute one step of trialectic evolution
        
        Returns:
            True if step was executed, False if halted
        """
        if self.current_step >= self.max_steps:
            return False
        
        # Apply all applicable rules in parallel
        rules_applied = 0
        
        for agent_arena in self.theta_system.agent_arenas:
            for membrane in agent_arena.membranes:
                rules_applied += self._apply_membrane_rules(membrane)
        
        # Update coherence
        self._update_coherence()
        
        # Update relevance gradient
        self._update_relevance_gradient()
        
        self.current_step += 1
        
        self.logger.debug(
            f"Step {self.current_step}: applied {rules_applied} rules"
        )
        
        return rules_applied > 0
    
    def _apply_membrane_rules(self, membrane: LambdaMembrane) -> int:
        """Apply all applicable rules in membrane"""
        rules_applied = 0
        
        for rule in membrane.rules:
            # Check if rule is applicable
            if self._is_rule_applicable(rule, membrane):
                self._apply_rule(rule, membrane)
                rules_applied += 1
        
        return rules_applied
    
    def _is_rule_applicable(self, rule: TrialecticRule, membrane: LambdaMembrane) -> bool:
        """Check if rule can be applied"""
        # Check if source triad exists in membrane
        for triad in membrane.triads:
            if (triad.x == rule.source_triad.x and
                triad.y == rule.source_triad.y and
                triad.z == rule.source_triad.z):
                return True
        
        return False
    
    def _apply_rule(self, rule: TrialecticRule, membrane: LambdaMembrane):
        """Apply trialectic transformation rule"""
        # Find and transform source triad
        for i, triad in enumerate(membrane.triads):
            if (triad.x == rule.source_triad.x and
                triad.y == rule.source_triad.y and
                triad.z == rule.source_triad.z):
                
                # Replace with target triad
                membrane.triads[i] = Triad(
                    x=rule.target_triad.x,
                    y=rule.target_triad.y,
                    z=rule.target_triad.z,
                    coherence=triad.coherence
                )
                break
    
    def _update_coherence(self):
        """Update trialectic coherence"""
        for agent_arena in self.theta_system.agent_arenas:
            for membrane in agent_arena.membranes:
                # Compute membrane coherence
                if len(membrane.triads) > 0:
                    membrane.coherence = sum(t.coherence for t in membrane.triads) / len(membrane.triads)
    
    def _update_relevance_gradient(self):
        """Update relevance gradient ∇ℜ"""
        # Simplified relevance computation
        total_coherence = 0.0
        total_membranes = 0
        
        for agent_arena in self.theta_system.agent_arenas:
            for membrane in agent_arena.membranes:
                total_coherence += membrane.coherence
                total_membranes += 1
        
        if total_membranes > 0:
            self.theta_system.relevance_gradient = total_coherence / total_membranes
    
    def run(self, max_steps: Optional[int] = None) -> Dict[str, Any]:
        """
        Run interpreter until halting or max steps
        
        Args:
            max_steps: Maximum steps to execute
            
        Returns:
            Execution statistics
        """
        if max_steps:
            self.max_steps = max_steps
        
        self.logger.info(f"Running interpreter for max {self.max_steps} steps")
        
        steps_executed = 0
        while self.step():
            steps_executed += 1
        
        stats = {
            'steps_executed': steps_executed,
            'final_relevance': self.theta_system.relevance_gradient,
            'membranes': len([
                m for aa in self.theta_system.agent_arenas
                for m in aa.membranes
            ])
        }
        
        self.logger.info(
            f"Execution complete: {steps_executed} steps, "
            f"relevance = {self.theta_system.relevance_gradient:.3f}"
        )
        
        return stats
