"""
ADVANCED ATTACK ARSENAL - SOPHISTICATED EXPLOITATION PATTERNS
==============================================================

Advanced attacks designed to bypass evolved defenses:
- Polymorphic payloads
- Encoding obfuscation
- Time-based attacks
- Logic bombs
- Chained exploits
- Zero-day simulations
"""

from typing import Any, List, Dict
import random
import base64

from src.core.models import DefenseType, Exploit, SeverityLevel
from src.attacks.models import AttackPattern


# ============================================================================
# ADVANCED ATTACK TECHNIQUES
# ============================================================================

class AdaptiveAttackGenerator:
    """Generates adaptive and parameterized attack payloads."""
    def __init__(self, intelligence):
        self.intelligence = intelligence

    def polymorphic_sql_injection(self, gen: int = 0, encoding_layers: int = 1) -> str:
        """Generates a polymorphic and multi-layered SQL injection payload."""
        variants = [
            "1' OR '1'='1",
            "1'/**/OR/**/1=1--",
            "1'||'1'='1",
            "1' UNION SELECT NULL--",
            "admin'--",
        ]
        payload = variants[gen % len(variants)]

        for _ in range(encoding_layers):
            payload = base64.b64encode(payload.encode()).decode()

        return payload

    def polymorphic_buffer_overflow(self, gen: int = 0, size: int = 1000):
        """Generates a polymorphic buffer overflow payload with a tunable size."""
        patterns = ["A", "B", "X", "\x00", "\xff", "🔴"]
        pattern = patterns[gen % len(patterns)]
        return pattern * size

    # === Type Confusion Attacks ===

    def nested_type_confusion(self, depth: int = 3) -> Any:
        """Creates a nested object with confusing types to test deep type checking."""
        payload: Any = "initial_string"
        for i in range(depth):
            container_type = random.choice([list, set, dict])
            if container_type == list:
                payload = [payload, i]
            elif container_type == set:
                try:
                    payload = {payload, i}
                except TypeError:
                    # Fallback to list if payload is not hashable
                    payload = [payload, i]
            elif container_type == dict:
                payload = {f"key_{i}": payload}
        return payload

    def generator_type_confusion(self) -> Any:
        """Uses a generator to bypass simple type checks that don't handle iterators."""
        def malicious_generator():
            yield "part1"
            yield 2
            yield {"command": "delete", "target": "*"}
        return malicious_generator()

    def class_injection(self) -> Any:
        """Defines a class with malicious behavior in its methods."""
        class MaliciousPayload:
            def __str__(self):
                return "1' OR '1'='1"
            def __len__(self):
                return 99999
        return MaliciousPayload()

    # === Logic Bombs ===

    def time_based_bomb(self, generation: int) -> Dict:
        """A logic bomb that triggers based on an arbitrary 'time' value (generation)."""
        trigger_condition = (generation > 0 and generation % 10 == 0)
        return {"execute": trigger_condition, "payload": "DELETE *"}

    def length_based_bomb(self) -> Dict:
        """A logic bomb where declared length mismatches actual length."""
        return {"declared_length": 1000, "payload": "A" * 20}

    # === Chained Exploits ===

    def chained_type_and_injection(self) -> Any:
        """First passes a type check, then delivers an injection."""
        return [1, 2, "admin'--"]

    def chained_overflow_and_state(self) -> Dict:
        """Combines a buffer overflow with a state-corrupting instruction."""
        return {"buffer": "A" * 5000, "state_key": "__admin__", "state_value": True}

    # === Zero-Day Simulations ===

    def memory_exhaustion_attack(self, scale: int = 1000000) -> List:
        """Attempts to exhaust memory by creating a massive list."""
        try:
            return ["A"] * scale
        except MemoryError:
            return ["MemoryError"]

    def prototype_pollution(self) -> Dict:
        """Simulates prototype pollution by attempting to modify shared objects."""
        return {"__class__": {"__init__": {"__globals__": {"is_admin": True}}}}

    def format_string_exploit(self) -> str:
        """Uses format string specifiers to read/write memory."""
        return "User: %s%s%s%n"

    # === Advanced State Manipulation ===

    def property_hijacking(self) -> Any:
        """Hijacks a property to execute code upon access."""
        class HijackedProp:
            @property
            def name(self):
                return "1' OR '1'='1"
        return HijackedProp()

    def metaclass_injection(self) -> Any:
        """Injects a malicious metaclass to alter class creation."""
        class MaliciousMeta(type):
            def __new__(cls, name, bases, dct):
                dct['injected_attribute'] = '1; rm -rf /'
                return super().__new__(cls, name, bases, dct)
        class BenignClass(metaclass=MaliciousMeta):
            pass
        return BenignClass

    # === Advanced Injection Vectors ===

    def xpath_injection(self) -> str:
        """Injects a payload to exploit XPath queries."""
        return "' or 1=1 or ''='"

    def nosql_injection(self) -> Dict:
        """Injects a payload for NoSQL databases using query operators."""
        return {"$ne": ""}

    def command_injection(self) -> str:
        """Injects a shell command."""
        return "; ls /"

    def template_injection(self) -> str:
        """Injects code into a template engine (SSTI)."""
        return "{{ ''.__class__.__mro__[1].__subclasses__()[133]('whoami', shell=True, stdout=-1).communicate() }}"


# ============================================================================
# ADVANCED RED TEAM EXECUTOR
# ============================================================================

class AdvancedRedTeamExecutor:
    """Executes sophisticated attacks"""

    def __init__(self, target_seed, attacker_intelligence):
        self.target = target_seed
        self.attacker_intelligence = attacker_intelligence
        self.attack_generator = AdaptiveAttackGenerator(attacker_intelligence)
        self.generation = 0
        self.advanced_patterns: List[AttackPattern] = []
        self._initialize_advanced_patterns()

    def _initialize_advanced_patterns(self):
        """Initialize advanced attack patterns"""

        self.advanced_patterns = [
            # Polymorphic attacks
            AttackPattern(
                DefenseType.SANITIZATION,
                lambda: self.attack_generator.polymorphic_sql_injection(self.generation),
                "Polymorphic SQL injection",
                difficulty=7
            ),
            AttackPattern(
                DefenseType.BOUNDS_ENFORCEMENT,
                lambda: self.attack_generator.polymorphic_buffer_overflow(self.generation),
                "Polymorphic buffer overflow",
                difficulty=8
            ),

            # Advanced type confusion
            AttackPattern(
                DefenseType.TYPE_CHECKING,
                self.attack_generator.nested_type_confusion,
                "Nested type confusion",
                difficulty=6
            ),
            AttackPattern(
                DefenseType.TYPE_CHECKING,
                self.attack_generator.generator_type_confusion,
                "Generator type confusion",
                difficulty=7
            ),
            AttackPattern(
                DefenseType.TYPE_CHECKING,
                self.attack_generator.class_injection,
                "Custom class injection",
                difficulty=8
            ),

            # Logic bombs
            AttackPattern(
                DefenseType.INPUT_VALIDATION,
                lambda: self.attack_generator.time_based_bomb(self.generation),
                "Time-based logic bomb",
                difficulty=8
            ),
            AttackPattern(
                DefenseType.BOUNDS_ENFORCEMENT,
                self.attack_generator.length_based_bomb,
                "Length-spoofing bomb",
                difficulty=9
            ),

            # Chained exploits
            AttackPattern(
                DefenseType.TYPE_CHECKING,
                self.attack_generator.chained_type_and_injection,
                "Chained type + injection",
                difficulty=9
            ),
            AttackPattern(
                DefenseType.STATE_PROTECTION,
                self.attack_generator.chained_overflow_and_state,
                "Chained overflow + state corruption",
                difficulty=9
            ),

            # Zero-day simulations
            AttackPattern(
                DefenseType.BOUNDS_ENFORCEMENT,
                self.attack_generator.memory_exhaustion_attack,
                "Memory exhaustion attack",
                difficulty=10
            ),
            AttackPattern(
                DefenseType.STATE_PROTECTION,
                self.attack_generator.prototype_pollution,
                "Prototype pollution",
                difficulty=9
            ),
            AttackPattern(
                DefenseType.SANITIZATION,
                self.attack_generator.format_string_exploit,
                "Format string exploit",
                difficulty=8
            ),

            # Advanced state manipulation
            AttackPattern(
                DefenseType.STATE_PROTECTION,
                self.attack_generator.property_hijacking,
                "Property hijacking",
                difficulty=9
            ),
            AttackPattern(
                DefenseType.TYPE_CHECKING,
                self.attack_generator.metaclass_injection,
                "Metaclass injection",
                difficulty=10
            ),

            # Multiple injection types
            AttackPattern(
                DefenseType.SANITIZATION,
                self.attack_generator.xpath_injection,
                "XPath injection",
                difficulty=7
            ),
            AttackPattern(
                DefenseType.SANITIZATION,
                self.attack_generator.nosql_injection,
                "NoSQL injection",
                difficulty=8
            ),
            AttackPattern(
                DefenseType.SANITIZATION,
                self.attack_generator.command_injection,
                "Command injection",
                difficulty=9
            ),
            AttackPattern(
                DefenseType.SANITIZATION,
                self.attack_generator.template_injection,
                "Template injection",
                difficulty=10
            ),
        ]

    def execute_advanced_suite(self) -> tuple:
        """Execute all advanced attacks"""
        exploits = []
        blocked_count = 0

        print(f"\n🔴 LAUNCHING ADVANCED ATTACK SUITE (Generation {self.generation})")
        print(f"{'='*90}")

        for pattern in self.advanced_patterns:
            try:
                payload = pattern.payload_generator()
            except Exception as e:
                print(f"  ⚠️  Payload generation error: {pattern.description}")
                continue

            blocked, reason = self.target.test_defense(pattern.defense_type, payload)
            pattern.record_attempt(not blocked)

            severity = self._calculate_severity(pattern)
            exploit = Exploit(
                vector=pattern.defense_type,
                description=pattern.description,
                payload=str(payload)[:100] + "..." if len(str(payload)) > 100 else payload,
                severity=severity,
                difficulty=pattern.difficulty,
                blocked=blocked,
                defense_reason=reason
            )

            exploits.append(exploit)

            if blocked:
                blocked_count += 1
                status = "✓ BLOCKED"
            else:
                status = "✗ EXPLOITED"

            print(f"  {status:12} | Diff:{pattern.difficulty:2d} | {pattern.description:40} | {reason[:30]}")

        fitness = (blocked_count / len(exploits) * 100) if exploits else 0

        print(f"{'='*90}")
        print(f"  Advanced Attack Results: {blocked_count}/{len(exploits)} blocked ({fitness:.1f}% defense)")

        return exploits, blocked_count, len(exploits), fitness

    def _calculate_severity(self, pattern: AttackPattern) -> SeverityLevel:
        """Calculate exploit severity based on difficulty"""
        if pattern.difficulty >= 9:
            return SeverityLevel.CRITICAL
        elif pattern.difficulty >= 7:
            return SeverityLevel.HIGH
        elif pattern.difficulty >= 5:
            return SeverityLevel.MEDIUM
        else:
            return SeverityLevel.LOW
