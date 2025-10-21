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

from typing import Any, List, Dict, Tuple
import random
import base64

from src.core.models import DefenseType, Exploit, SeverityLevel
from src.attacks.models import AttackPattern
from src.attacks.intelligence import (
    AttackerIntelligence, AttackVector, PayloadCharacteristics
)


# ============================================================================
# ADVANCED ATTACK TECHNIQUES
# ============================================================================

class AdaptiveAttackGenerator:
    """Generates adaptive attacks based on intelligence"""

    def __init__(self, intelligence: AttackerIntelligence):
        self.intelligence = intelligence
        self.mutation_history: List[str] = []

    def generate_injection_attack(self, optimized: bool = True) -> Tuple[Any, PayloadCharacteristics]:
        """Generate SQL injection with adaptive parameters"""

        if optimized:
            params = self.intelligence.get_optimal_parameters(AttackVector.INJECTION)
        else:
            params = {"size": 50, "encoding_layers": 0, "complexity": 1, "obfuscation_level": 3}

        # Base injection
        base_payloads = [
            "'; DROP TABLE users--",
            "admin' OR '1'='1",
            "1' UNION SELECT * FROM",
            "'; DELETE FROM admin--",
        ]

        payload = random.choice(base_payloads)

        # Apply obfuscation
        payload = self._apply_obfuscation(payload, params["obfuscation_level"])

        # Apply encoding layers
        payload = self._apply_encoding(payload, params["encoding_layers"])

        # Adjust size
        if len(payload) < params["size"]:
            padding = "/*" + "A" * (params["size"] - len(payload) - 4) + "*/"
            payload = payload + padding

        chars = PayloadCharacteristics(
            vector=AttackVector.INJECTION,
            size=len(str(payload)),
            encoding_layers=params["encoding_layers"],
            complexity=1,
            obfuscation_level=params["obfuscation_level"],
            uses_quotes="'" in str(payload) or '"' in str(payload),
            uses_special_chars=True,
            is_polymorphic=False
        )

        return payload, chars

    def generate_overflow_attack(self, optimized: bool = True) -> Tuple[Any, PayloadCharacteristics]:
        """Generate buffer overflow with adaptive size"""

        if optimized:
            params = self.intelligence.get_optimal_parameters(AttackVector.OVERFLOW)
        else:
            params = {"size": 1000, "encoding_layers": 0, "complexity": 1, "obfuscation_level": 3}

        # Generate overflow payload
        patterns = ["A", "B", "X", "\x00", "\xff"]
        pattern = random.choice(patterns)
        payload = pattern * params["size"]

        # Add malicious trailer
        payload += "'; DROP--"

        chars = PayloadCharacteristics(
            vector=AttackVector.OVERFLOW,
            size=len(payload),
            encoding_layers=0,
            complexity=1,
            obfuscation_level=0,
            uses_quotes=True,
            uses_special_chars=True,
            is_polymorphic=False
        )

        return payload, chars

    def generate_type_confusion_attack(self, optimized: bool = True) -> Tuple[Any, PayloadCharacteristics]:
        """Generate type confusion with adaptive complexity"""

        if optimized:
            params = self.intelligence.get_optimal_parameters(AttackVector.TYPE_CONFUSION)
        else:
            params = {"size": 100, "encoding_layers": 0, "complexity": 2, "obfuscation_level": 3}

        # Build nested structure based on complexity
        payload = {"malicious": "payload"}

        for i in range(params["complexity"]):
            payload = {"nested_" + str(i): payload}

        # Add injection in deep layer
        self._inject_deep(payload, "'; DROP TABLE--", params["complexity"])

        chars = PayloadCharacteristics(
            vector=AttackVector.TYPE_CONFUSION,
            size=len(str(payload)),
            encoding_layers=0,
            complexity=params["complexity"],
            obfuscation_level=params["obfuscation_level"],
            uses_quotes=True,
            uses_special_chars=False,
            is_polymorphic=False
        )

        return payload, chars

    def generate_encoding_attack(self, optimized: bool = True) -> Tuple[Any, PayloadCharacteristics]:
        """Generate multi-layer encoded attack"""

        if optimized:
            params = self.intelligence.get_optimal_parameters(AttackVector.ENCODING)
        else:
            params = {"size": 100, "encoding_layers": 2, "complexity": 1, "obfuscation_level": 5}

        payload = "'; DROP TABLE users--"

        # Apply encoding layers
        payload = self._apply_encoding(payload, params["encoding_layers"])

        chars = PayloadCharacteristics(
            vector=AttackVector.ENCODING,
            size=len(payload),
            encoding_layers=params["encoding_layers"],
            complexity=1,
            obfuscation_level=params["obfuscation_level"],
            uses_quotes=False,  # Encoded
            uses_special_chars=False,  # Encoded
            is_polymorphic=False
        )

        return payload, chars

    def generate_state_corruption_attack(self, optimized: bool = True) -> Tuple[Any, PayloadCharacteristics]:
        """Generate state corruption attack"""

        if optimized:
            params = self.intelligence.get_optimal_parameters(AttackVector.STATE_CORRUPTION)
        else:
            params = {"size": 200, "encoding_layers": 0, "complexity": 3, "obfuscation_level": 4}

        payload = {
            "_protected": "corrupted",
            "__proto__": {"isAdmin": True},
            "state": {"internal": "compromised"}
        }

        # Add complexity
        for i in range(params["complexity"]):
            payload[f"nested_{i}"] = {"level": i, "data": payload.copy()}

        chars = PayloadCharacteristics(
            vector=AttackVector.STATE_CORRUPTION,
            size=len(str(payload)),
            encoding_layers=0,
            complexity=params["complexity"],
            obfuscation_level=params["obfuscation_level"],
            uses_quotes=False,
            uses_special_chars=True,
            is_polymorphic=False
        )

        return payload, chars

    def generate_polymorphic_attack(self, base_payload: str) -> Tuple[Any, PayloadCharacteristics]:
        """Generate polymorphic variant"""

        # Mutation strategies
        mutations = [
            lambda p: p.replace("'", '"'),  # Quote swap
            lambda p: p.replace(" ", "/**/"),  # Comment injection
            lambda p: p.upper() if random.random() > 0.5 else p.lower(),  # Case change
            lambda p: p.replace("OR", "||"),  # Operator substitution
            lambda p: p.replace("=", " LIKE "),  # Operator variation
            lambda p: self._unicode_transform(p),  # Unicode tricks
        ]

        # Apply random mutations
        payload = base_payload
        for _ in range(random.randint(1, 3)):
            mutation = random.choice(mutations)
            payload = mutation(payload)

        self.mutation_history.append(payload)

        chars = PayloadCharacteristics(
            vector=AttackVector.INJECTION,
            size=len(payload),
            encoding_layers=0,
            complexity=1,
            obfuscation_level=7,
            uses_quotes="'" in payload or '"' in payload,
            uses_special_chars=True,
            is_polymorphic=True
        )

        return payload, chars

    def generate_adaptive_campaign(self, count: int = 10) -> List[Tuple[str, Any, PayloadCharacteristics]]:
        """Generate adaptive attack campaign"""

        campaign = []

        # Analyze defender's weakness
        weakest = self.intelligence.identify_weakest_defense()

        # Generate attacks targeting weakness
        generators = [
            ("injection", self.generate_injection_attack),
            ("overflow", self.generate_overflow_attack),
            ("type_confusion", self.generate_type_confusion_attack),
            ("encoding", self.generate_encoding_attack),
            ("state_corruption", self.generate_state_corruption_attack),
        ]

        for i in range(count):
            # Bias towards weak defense
            if weakest and "sanit" in weakest.lower() and random.random() > 0.3:
                attack_type, generator = ("injection", self.generate_injection_attack)
            elif weakest and "type" in weakest.lower() and random.random() > 0.3:
                attack_type, generator = ("type_confusion", self.generate_type_confusion_attack)
            elif weakest and "bounds" in weakest.lower() and random.random() > 0.3:
                attack_type, generator = ("overflow", self.generate_overflow_attack)
            else:
                attack_type, generator = random.choice(generators)

            payload, chars = generator(optimized=True)
            campaign.append((attack_type, payload, chars))

        return campaign

    def _apply_obfuscation(self, payload: str, level: int) -> str:
        """Apply obfuscation based on level"""

        if level >= 3:
            # Comment injection
            payload = payload.replace(" ", "/**/")

        if level >= 5:
            # Case randomization
            payload = ''.join(c.upper() if random.random() > 0.5 else c.lower() for c in payload)

        if level >= 7:
            # Unicode substitution
            payload = self._unicode_transform(payload)

        if level >= 9:
            # Character building
            payload = self._char_build(payload)

        return payload

    def _apply_encoding(self, payload: str, layers: int) -> str:
        """Apply encoding layers"""

        encoded = payload

        for layer in range(layers):
            if layer % 3 == 0:
                # Base64
                encoded = base64.b64encode(encoded.encode()).decode()
            elif layer % 3 == 1:
                # URL encoding
                encoded = self._url_encode(encoded)
            else:
                # Hex encoding
                encoded = self._hex_encode(encoded)

        return encoded

    def _inject_deep(self, obj: Dict, value: str, depth: int):
        """Inject value at specific depth"""
        if depth <= 0:
            obj["injected"] = value
            return

        for key, val in obj.items():
            if isinstance(val, dict):
                self._inject_deep(val, value, depth - 1)
                break

    def _unicode_transform(self, text: str) -> str:
        """Transform using unicode tricks"""
        transforms = {
            "O": "Ο",  # Greek Omicron
            "A": "Α",  # Greek Alpha
            "E": "Ε",  # Greek Epsilon
            "o": "ο",  # Greek lowercase omicron
            "a": "α",  # Greek lowercase alpha
        }

        for old, new in transforms.items():
            if random.random() > 0.5:
                text = text.replace(old, new)

        return text

    def _char_build(self, text: str) -> str:
        """Build string using character codes"""
        # Simulated - in real SQL: CHAR(65)+CHAR(66)...
        return f"CHAR({','.join(str(ord(c)) for c in text[:10])})"

    def _url_encode(self, text: str) -> str:
        """URL encode"""
        return ''.join(f'%{ord(c):02X}' if c in "';\"-" else c for c in text)

    def _hex_encode(self, text: str) -> str:
        """Hex encode"""
        return ''.join(f'\\x{ord(c):02x}' for c in text)


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
            AttackPattern(
                DefenseType.SANITIZATION,
                lambda: self.attack_generator.generate_injection_attack(optimized=True),
                "Adaptive SQL Injection",
                difficulty=8
            ),
            AttackPattern(
                DefenseType.BOUNDS_ENFORCEMENT,
                lambda: self.attack_generator.generate_overflow_attack(optimized=True),
                "Adaptive Buffer Overflow",
                difficulty=8
            ),
            AttackPattern(
                DefenseType.TYPE_CHECKING,
                lambda: self.attack_generator.generate_type_confusion_attack(optimized=True),
                "Adaptive Type Confusion",
                difficulty=9
            ),
            AttackPattern(
                DefenseType.SANITIZATION,
                lambda: self.attack_generator.generate_encoding_attack(optimized=True),
                "Adaptive Encoding Attack",
                difficulty=7
            ),
            AttackPattern(
                DefenseType.STATE_PROTECTION,
                lambda: self.attack_generator.generate_state_corruption_attack(optimized=True),
                "Adaptive State Corruption",
                difficulty=9
            ),
            AttackPattern(
                DefenseType.SANITIZATION,
                lambda: self.attack_generator.generate_polymorphic_attack("admin' OR '1'='1"),
                "Polymorphic Mutation Attack",
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
                # New generator returns payload and characteristics
                payload, chars = pattern.payload_generator()
            except Exception as e:
                print(f"  ⚠️  Payload generation error: {pattern.description}")
                continue

            blocked, reason = self.target.test_defense(pattern.defense_type, payload)

            # Record detailed outcome with the new intelligence module
            self.attacker_intelligence.record_attack(
                payload, chars, blocked, pattern.defense_type.name, reason
            )

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
