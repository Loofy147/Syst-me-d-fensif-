"""
ORCHESTRATED MULTI-MODEL ATTACK SCENARIOS
==========================================

Sophisticated attack campaigns that combine multiple techniques:
- Chained multi-stage attacks
- Adaptive attack sequences
- Coordinated distributed patterns
- Time-based progressive exploitation
- Context-aware mutations
"""

from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import random
from src.core.models import DefenseType
from src.logger import logger
from src.attacks.advanced import AdvancedRedTeamExecutor
from src.attacks.intelligence import PayloadCharacteristics


class AttackPhase(Enum):
    """Enumeration of the different phases of an orchestrated attack."""

    RECONNAISSANCE = "recon"
    INITIAL_PROBE = "probe"
    EXPLOITATION = "exploit"
    PRIVILEGE_ESCALATION = "escalate"
    PERSISTENCE = "persist"


@dataclass
class AttackScenario:
    """Represents a complete attack scenario with multiple stages."""

    name: str
    description: str
    phases: List[Tuple[AttackPhase, List[Any]]]  # Phase + payloads
    difficulty: int
    requires_state: bool = False


# ============================================================================
# SCENARIO 1: THE POLYMORPHIC TRANSFORMER
# ============================================================================

class PolymorphicTransformerScenario:
    """
    Attack that transforms itself based on defense responses.
    Learns what gets blocked and mutates to avoid detection.
    """
    
    def __init__(self):
        self.mutation_count = 0
        self.blocked_patterns = set()
    
    def generate_wave(self, generation: int) -> List[Tuple[str, Any]]:
        """Generate attack wave that evolves based on what was blocked"""
        
        wave = []
        
        # Base injection
        base = "admin' OR '1'='1"
        
        # Apply mutations based on what was blocked before
        if "OR" in self.blocked_patterns:
            base = base.replace("OR", "||")
        
        if "'" in self.blocked_patterns:
            # Switch to double quotes
            base = base.replace("'", '"')
        
        if "1=1" in self.blocked_patterns:
            # Use different always-true condition
            base = base.replace("1=1", "2>1")
        
        # Add progressive obfuscation
        mutations = [
            ("sql_injection", base),
            ("sql_injection", base.replace(" ", "/**/")),  # Comment obfuscation
            ("sql_injection", self._unicode_transform(base)),  # Unicode tricks
            ("sql_injection", self._case_variation(base)),  # Case mixing
        ]
        
        self.mutation_count += len(mutations)
        return mutations
    
    def record_block(self, payload: str):
        """Learn what patterns get blocked"""
        for pattern in ["OR", "AND", "'", '"', "=", "1=1", "DROP"]:
            if pattern in payload:
                self.blocked_patterns.add(pattern)
    
    def _unicode_transform(self, text: str) -> str:
        """Transform using unicode lookalikes"""
        transforms = {"O": "Ο", "A": "Α", "E": "Ε"}  # Greek letters
        for old, new in transforms.items():
            text = text.replace(old, new)
        return text
    
    def _case_variation(self, text: str) -> str:
        """Random case variation"""
        return ''.join(c.upper() if random.random() > 0.5 else c.lower() for c in text)


# ============================================================================
# SCENARIO 2: THE LAYERED SIEGE
# ============================================================================

class LayeredSiegeScenario:
    """
    Multi-phase attack that progressively escalates:
    1. Probe defenses with safe payloads
    2. Test each defense type
    3. Find weakest point
    4. Concentrate attack on weakness
    5. Chain exploits through weak point
    """
    
    def generate_campaign(self, generation: int) -> AttackScenario:
        """Generate complete attack campaign"""
        
        phases = []
        
        # Phase 1: Reconnaissance
        recon_payloads = [
            "test",  # Baseline
            "a" * 10,  # Small payload
            "normal_input",  # Legitimate-looking
        ]
        phases.append((AttackPhase.RECONNAISSANCE, [("input_validation", p) for p in recon_payloads]))
        
        # Phase 2: Defense probing
        probe_payloads = [
            "'",  # Test sanitization
            ["test"],  # Test type checking
            "A" * 100,  # Test bounds
            {"key": "value"},  # Test state protection
        ]
        phases.append((AttackPhase.INITIAL_PROBE, [
            ("sanitization", probe_payloads[0]),
            ("type_checking", probe_payloads[1]),
            ("bounds_enforcement", probe_payloads[2]),
            ("state_protection", probe_payloads[3]),
        ]))
        
        # Phase 3: Exploitation (multi-vector)
        exploit_payloads = [
            "'; DROP TABLE users--",  # SQL injection
            "A" * 5000,  # Buffer overflow
            {"_protected": "corrupted"},  # State corruption
            self._generate_encoded_payload(),  # Encoded attack
        ]
        phases.append((AttackPhase.EXPLOITATION, [
            ("sanitization", exploit_payloads[0]),
            ("bounds_enforcement", exploit_payloads[1]),
            ("state_protection", exploit_payloads[2]),
            ("sanitization", exploit_payloads[3]),
        ]))
        
        # Phase 4: Chained exploit
        chained_payload = {
            "sql": "'; DROP--",
            "overflow": "X" * 10000,
            "_internal": "compromised"
        }
        phases.append((AttackPhase.PRIVILEGE_ESCALATION, [
            ("combined", chained_payload)
        ]))
        
        return AttackScenario(
            name="Layered Siege",
            description="Progressive multi-phase attack campaign",
            phases=phases,
            difficulty=9,
            requires_state=True
        )
    
    def _generate_encoded_payload(self) -> str:
        """Generate multi-layer encoded payload"""
        import base64
        payload = "'; DROP--"
        encoded = base64.b64encode(payload.encode()).decode()
        return encoded


# ============================================================================
# SCENARIO 3: THE TIMING ORACLE
# ============================================================================

class TimingOracleScenario:
    """
    Uses timing information to deduce defense state.
    Sends payloads and measures response patterns.
    """
    
    def __init__(self):
        self.timing_data = []
    
    def generate_timing_probes(self, generation: int) -> List[Tuple[str, Any]]:
        """Generate payloads to probe timing behavior"""
        
        probes = [
            # Fast operations
            ("timing_probe", "a"),
            ("timing_probe", 123),
            
            # Medium operations  
            ("timing_probe", "A" * 100),
            ("timing_probe", ["test"] * 10),
            
            # Slow operations
            ("timing_probe", "X" * 10000),
            ("timing_probe", {"nested": {"deep": {"structure": "yes"}}}),
            
            # Exploit based on timing
            ("timing_exploit", self._craft_payload_from_timing()),
        ]
        
        return probes
    
    def record_timing(self, payload: Any, duration: float, blocked: bool):
        """Learn from timing information"""
        self.timing_data.append({
            "size": len(str(payload)),
            "duration": duration,
            "blocked": blocked
        })
    
    def _craft_payload_from_timing(self) -> Any:
        """Craft exploit based on observed timing patterns"""
        if not self.timing_data:
            return "normal_input"
        
        # Find sweet spot: slow enough to process, fast enough to not timeout
        avg_duration = sum(t["duration"] for t in self.timing_data) / len(self.timing_data)
        
        # Generate payload targeting that timing window
        size = int(avg_duration * 1000)
        return "B" * min(size, 50000) + "'; DROP--"


# ============================================================================
# SCENARIO 4: THE CONTEXT CHAMELEON
# ============================================================================

class ContextChameleonScenario:
    """
    Attack that adapts to the context and mimics legitimate traffic.
    Uses knowledge of what passed before to craft convincing attacks.
    """
    
    def __init__(self):
        self.successful_patterns = []
        self.failed_patterns = []
    
    def generate_context_attacks(self, generation: int) -> List[Tuple[str, Any]]:
        """Generate attacks that blend with legitimate patterns"""
        
        attacks = []
        
        # Learn what "looks legitimate"
        if self.successful_patterns:
            # Mimic successful patterns but inject malicious content
            for pattern in self.successful_patterns[-3:]:
                mimicked = self._inject_into_pattern(pattern)
                attacks.append(("context_attack", mimicked))
        
        # Generate new camouflaged attacks
        legitimate_looking = [
            "user@example.com",  # Looks like email
            "2024-01-15",  # Looks like date
            "Product_Name_123",  # Looks like identifier
        ]
        
        for legit in legitimate_looking:
            # Inject malicious content
            attacks.append(("context_attack", legit + "'; DROP--"))
            attacks.append(("context_attack", legit + "\x00" + "malicious"))
        
        return attacks
    
    def learn_from_result(self, payload: Any, blocked: bool):
        """Learn what patterns work"""
        if blocked:
            self.failed_patterns.append(str(payload))
        else:
            self.successful_patterns.append(str(payload))
    
    def _inject_into_pattern(self, pattern: str) -> str:
        """Inject malicious content into legitimate pattern"""
        # Insert at various positions
        mid = len(pattern) // 2
        injections = [
            pattern + "'; DROP--",
            pattern[:mid] + "/**/OR/**/1=1" + pattern[mid:],
            pattern.replace("_", "_'; DROP TABLE users;--_"),
        ]
        return random.choice(injections)


# ============================================================================
# SCENARIO 5: THE DISTRIBUTED SWARM
# ============================================================================

class DistributedSwarmScenario:
    """
    Coordinated attack from multiple "sources" that individually look harmless
    but collectively overwhelm or exploit rate limiting.
    """
    
    def __init__(self, swarm_size: int = 5):
        self.swarm_size = swarm_size
        self.attack_vectors = []
    
    def generate_swarm_attack(self, generation: int) -> List[Tuple[str, Any]]:
        """Generate distributed coordinated attack"""
        
        swarm = []
        
        # Each agent sends seemingly harmless payload
        for agent_id in range(self.swarm_size):
            # Fragment attack across agents
            fragment = self._generate_fragment(agent_id, generation)
            swarm.append(("swarm_attack", fragment))
        
        # Collective payload when combined
        combined = self._combine_fragments(swarm)
        swarm.append(("swarm_combined", combined))
        
        return swarm
    
    def _generate_fragment(self, agent_id: int, generation: int) -> str:
        """Generate attack fragment for single agent"""
        fragments = [
            "'",
            " OR ",
            "'1'='1",
            "'; DROP",
            " TABLE--",
        ]
        return fragments[agent_id % len(fragments)]
    
    def _combine_fragments(self, swarm: List) -> str:
        """Combine fragments into complete attack"""
        return "".join(str(item[1]) for item in swarm[:5])


# ============================================================================
# SCENARIO 6: THE EVOLUTIONARY ARMS RACE
# ============================================================================

class EvolutionaryArmsRaceScenario:
    """
    Attack that evolves in response to defenses using genetic algorithm.
    Maintains population of attack variants, selects best performers.
    """
    
    def __init__(self):
        self.population = []
        self.generation = 0
        self.fitness_history = []
        self._initialize_population()
    
    def _initialize_population(self):
        """Create initial attack population"""
        base_attacks = [
            "'; DROP--",
            "admin' OR '1'='1",
            "1' UNION SELECT",
            "'; DELETE FROM",
            "admin'--",
        ]
        self.population = [{"genome": attack, "fitness": 0.0} for attack in base_attacks]
    
    def evolve_generation(self) -> List[Tuple[str, Any]]:
        """Evolve attack population for one generation"""
        
        # Selection: Keep top performers
        self.population.sort(key=lambda x: x["fitness"], reverse=True)
        survivors = self.population[:3]
        
        # Crossover: Combine successful attacks
        offspring = []
        for i in range(2):
            parent1 = random.choice(survivors)
            parent2 = random.choice(survivors)
            child_genome = self._crossover(parent1["genome"], parent2["genome"])
            offspring.append({"genome": child_genome, "fitness": 0.0})
        
        # Mutation: Randomly modify
        for individual in offspring:
            if random.random() > 0.5:
                individual["genome"] = self._mutate(individual["genome"])
        
        # New population
        self.population = survivors + offspring
        
        # Add novel attacks
        self.population.append({"genome": self._generate_novel(), "fitness": 0.0})
        
        attacks = [("evolutionary", ind["genome"]) for ind in self.population]
        self.generation += 1
        
        return attacks
    
    def update_fitness(self, genome: str, blocked: bool):
        """Update fitness based on result (success = high fitness)"""
        for individual in self.population:
            if individual["genome"] == genome:
                individual["fitness"] = 0.0 if blocked else 1.0
                break
    
    def _crossover(self, genome1: str, genome2: str) -> str:
        """Combine two attack genomes"""
        split = len(genome1) // 2
        return genome1[:split] + genome2[split:]
    
    def _mutate(self, genome: str) -> str:
        """Randomly mutate attack"""
        mutations = [
            lambda g: g.replace("'", '"'),  # Quote type
            lambda g: g.replace(" ", "/**/"),  # Comment injection
            lambda g: g.upper() if random.random() > 0.5 else g.lower(),  # Case
            lambda g: g + " AND 1=1",  # Always-true
            lambda g: "CAST(" + g + " AS VARCHAR)",  # Type cast obfuscation
        ]
        mutation = random.choice(mutations)
        return mutation(genome)
    
    def _generate_novel(self) -> str:
        """Generate completely novel attack"""
        templates = [
            "admin'--",
            "1' OR '1'='1",
            "'; EXEC xp_",
            "1' WAITFOR DELAY",
            "' HAVING 1=1--",
        ]
        novel = random.choice(templates)
        # Apply random obfuscation
        if random.random() > 0.5:
            novel = self._mutate(novel)
        return novel


# ============================================================================
# SCENARIO 7: THE METAMORPHIC PAYLOAD
# ============================================================================

class MetamorphicPayloadScenario:
    """
    Payload that changes its structure but maintains malicious function.
    Each iteration looks completely different but achieves same goal.
    """
    
    def __init__(self):
        self.transformation_count = 0
    
    def generate_metamorphs(self, generation: int) -> List[Tuple[str, Any]]:
        """Generate metamorphic variations"""
        
        # Core malicious intent: Drop table
        intent = "DROP_TABLE"
        
        metamorphs = []
        
        # Transformation 1: Direct SQL
        metamorphs.append(("metamorphic", "'; DROP TABLE users--"))
        
        # Transformation 2: Unicode encoding
        metamorphs.append(("metamorphic", self._unicode_encode("'; DROP TABLE--")))
        
        # Transformation 3: Hex encoding
        metamorphs.append(("metamorphic", self._hex_encode("'; DROP TABLE--")))
        
        # Transformation 4: Base64
        import base64
        metamorphs.append(("metamorphic", base64.b64encode(b"'; DROP TABLE--").decode()))
        
        # Transformation 5: Character building
        metamorphs.append(("metamorphic", "'; DR'+'OP TA'+'BLE--"))
        
        # Transformation 6: Function calls (simulated)
        metamorphs.append(("metamorphic", "CHAR(39)+CHAR(59)+CHR(68)+CHR(82)"))
        
        # Transformation 7: Nested structure
        metamorphs.append(("metamorphic", {
            "query": {"nested": {"deep": "'; DROP--"}}
        }))
        
        self.transformation_count += len(metamorphs)
        return metamorphs
    
    def _unicode_encode(self, text: str) -> str:
        """Encode using unicode escapes"""
        return ''.join(f'\\u{ord(c):04x}' for c in text)
    
    def _hex_encode(self, text: str) -> str:
        """Encode using hex"""
        return ''.join(f'\\x{ord(c):02x}' for c in text)


# ============================================================================
# SCENARIO 8: THE SIDE-CHANNEL ANALYZER
# ============================================================================

class SideChannelAnalysisScenario:
    """
    Tries to leak information by observing error messages and response times.
    """
    def generate_probes(self, generation: int) -> List[Tuple[str, Any]]:
        """Generates probes to trigger side-channel leakage."""
        probes = [
            ("side_channel_probe", "A" * 10),
            ("side_channel_probe", "A" * 100),
            ("side_channel_probe", "A" * 1000),
            ("side_channel_probe", {"$ne": "A"}),
            ("side_channel_probe", {"$gt": ""}),
        ]
        return probes

# ============================================================================
# SCENARIO 9: THE ADAPTIVE ARSENAL
# ============================================================================

class AdaptiveArsenalScenario:
    """
    Injects a wave of advanced, adaptive attacks from the main Red Team executor.
    This scenario acts as a bridge, bringing the most sophisticated attacks
    into the orchestrated campaign.
    """
    def __init__(self, red_team_executor: AdvancedRedTeamExecutor):
        self.red_team_executor = red_team_executor

    def generate_adaptive_wave(self, generation: int, num_attacks: int = 5) -> List[Tuple[str, Any, PayloadCharacteristics]]:
        """
        Selects a diverse set of high-difficulty adaptive attacks.
        Returns the payload and its characteristics.
        """
        self.red_team_executor.generation = generation

        all_patterns = self.red_team_executor.advanced_patterns
        high_difficulty_patterns = [p for p in all_patterns if p.difficulty >= 8]

        selected_patterns = []
        seen_types = set()
        for p in sorted(high_difficulty_patterns, key=lambda x: x.difficulty, reverse=True):
            if p.defense_type not in seen_types:
                selected_patterns.append(p)
                seen_types.add(p.defense_type)

        if len(selected_patterns) < num_attacks:
            remaining_patterns = [p for p in all_patterns if p not in selected_patterns]
            selected_patterns.extend(
                random.sample(
                    remaining_patterns,
                    min(len(remaining_patterns), num_attacks - len(selected_patterns))
                )
            )

        attack_wave = []
        for pattern in selected_patterns[:num_attacks]:
            try:
                payload, chars = pattern.payload_generator()
                attack_type = pattern.defense_type.name.lower()
                attack_wave.append((attack_type, payload, chars))
            except Exception:
                continue

        return attack_wave

# ============================================================================
# SCENARIO ORCHESTRATOR
# ============================================================================

class ScenarioOrchestrator:
    """Coordinates multiple attack scenarios"""
    
    def __init__(self, red_team_executor: AdvancedRedTeamExecutor):
        self.red_team_executor = red_team_executor
        self.scenarios = {
            "polymorphic": PolymorphicTransformerScenario(),
            "layered_siege": LayeredSiegeScenario(),
            "timing_oracle": TimingOracleScenario(),
            "context_chameleon": ContextChameleonScenario(),
            "distributed_swarm": DistributedSwarmScenario(),
            "evolutionary": EvolutionaryArmsRaceScenario(),
            "metamorphic": MetamorphicPayloadScenario(),
            "side_channel": SideChannelAnalysisScenario(),
            "adaptive_arsenal": AdaptiveArsenalScenario(red_team_executor),
        }
        self.scenario_performance = {name: 0.0 for name in self.scenarios.keys()}
    
    def generate_orchestrated_campaign(self, generation: int) -> List[Tuple[str, str, Any, Optional[PayloadCharacteristics]]]:
        """
        Generate complete orchestrated attack campaign.
        Returns payload and optional characteristics.
        """
        campaign = []
        
        logger.info(f"\n🎭 ORCHESTRATING MULTI-SCENARIO CAMPAIGN (Generation {generation})")
        logger.info(f"{'='*90}")
        
        # Standard scenarios (no advanced characteristics)
        def extend_campaign(name, attacks):
            for attack_type, payload in attacks:
                campaign.append((name, attack_type, payload, None))

        extend_campaign("polymorphic", self.scenarios["polymorphic"].generate_wave(generation))
        siege = self.scenarios["layered_siege"].generate_campaign(generation)
        for phase, payloads in siege.phases:
            extend_campaign("layered_siege", payloads)
        extend_campaign("timing_oracle", self.scenarios["timing_oracle"].generate_timing_probes(generation))
        extend_campaign("context_chameleon", self.scenarios["context_chameleon"].generate_context_attacks(generation))
        extend_campaign("distributed_swarm", self.scenarios["distributed_swarm"].generate_swarm_attack(generation))
        extend_campaign("evolutionary", self.scenarios["evolutionary"].evolve_generation())
        extend_campaign("metamorphic", self.scenarios["metamorphic"].generate_metamorphs(generation))
        extend_campaign("side_channel", self.scenarios["side_channel"].generate_probes(generation))

        # Adaptive Arsenal (with characteristics)
        logger.info(f"\n📍 Scenario: Adaptive Arsenal (Advanced Attacks)")
        adaptive_attacks = self.scenarios["adaptive_arsenal"].generate_adaptive_wave(generation)
        for attack_type, payload, chars in adaptive_attacks:
            campaign.append(("adaptive_arsenal", attack_type, payload, chars))
        logger.info(f"   Injected {len(adaptive_attacks)} advanced adaptive attacks")

        logger.info(f"\n{'='*90}")
        logger.info(f"📊 Total Campaign Size: {len(campaign)} coordinated attacks\n")
        
        return campaign
    
    def learn_from_results(self, scenario_name: str, payload: Any, blocked: bool,
                           defense_type: str, reason: str,
                           chars: Optional[PayloadCharacteristics] = None):
        """Feed results back to scenarios and intelligence for learning"""
        
        # Feed results to legacy scenarios
        if scenario_name == "polymorphic" and blocked:
            self.scenarios["polymorphic"].record_block(str(payload))
        elif scenario_name == "context_chameleon":
            self.scenarios["context_chameleon"].learn_from_result(payload, blocked)
        elif scenario_name == "evolutionary":
            self.scenarios["evolutionary"].update_fitness(str(payload), blocked)

        # Feed results to the main AttackerIntelligence module
        if scenario_name == "adaptive_arsenal" and chars is not None:
            self.red_team_executor.attacker_intelligence.record_attack(
                payload, chars, blocked, defense_type, reason
            )
        
        # Update scenario performance
        if scenario_name in self.scenario_performance:
            if blocked:
                self.scenario_performance[scenario_name] = max(0, self.scenario_performance[scenario_name] - 0.1)
            else:
                self.scenario_performance[scenario_name] = min(1, self.scenario_performance[scenario_name] + 0.2)
    
    def get_scenario_analysis(self) -> Dict[str, float]:
        """Get performance analysis of each scenario"""
        return self.scenario_performance.copy()