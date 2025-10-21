"""
AUTONOMOUS DEFENSE INTELLIGENCE ENGINE
========================================

A self-learning system that builds its own understanding through experience.
No pre-programmed solutions - it learns attack patterns, builds a knowledge base,
and evolves its own defensive strategies.

Core Intelligence Components:
------------------------------
1. KNOWLEDGE BASE: Attack pattern library learned from experience
2. REASONING ENGINE: Analyzes attacks to extract principles
3. PATTERN RECOGNITION: Identifies attack families and variations
4. STRATEGY SYNTHESIS: Creates new defenses from learned principles
5. META-LEARNING: Learns how to learn faster over time
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Set, Any, Optional, Tuple
from enum import Enum
from collections import defaultdict
import hashlib
import json
from src.core.models import EvolvableSeed, DefenseType
from src.config import config
from src.logger import logger


# ============================================================================
# ATTACK PATTERN KNOWLEDGE BASE
# ============================================================================

class AttackFamily(Enum):
    """Enumeration of the different families of attacks."""

    INJECTION = "injection"
    OVERFLOW = "overflow"
    TYPE_MANIPULATION = "type_manipulation"
    STATE_CORRUPTION = "state_corruption"
    ENCODING_OBFUSCATION = "encoding_obfuscation"
    LOGIC_EXPLOITATION = "logic_exploitation"
    RESOURCE_EXHAUSTION = "resource_exhaustion"
    UNKNOWN = "unknown"


@dataclass
class AttackSignature:
    """Represents the signature of a learned attack pattern."""

    signature_id: str
    family: AttackFamily
    characteristics: Dict[str, Any] = field(default_factory=dict)
    success_count: int = 0
    block_count: int = 0
    first_seen: int = 0
    last_seen: int = 0
    variations: List[str] = field(default_factory=list)
    
    @property
    def success_rate(self) -> float:
        """Returns the success rate of the attack."""
        total = self.success_count + self.block_count
        return self.success_count / total if total > 0 else 0.0


@dataclass
class DefensivePrinciple:
    """Represents a learned defensive principle."""

    principle_id: str
    description: str
    applicable_families: Set[AttackFamily]
    effectiveness: float = 0.5
    times_applied: int = 0
    times_successful: int = 0
    prerequisites: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        self.ema_alpha = config.get("intelligence", "ema_alpha")

    def update_effectiveness(self, successful: bool):
        """Updates the effectiveness of the principle using an Exponential Moving Average."""
        self.times_applied += 1
        if successful:
            self.times_successful += 1

        # Use EMA to weigh recent results more heavily
        current_outcome = 1.0 if successful else 0.0
        if self.times_applied == 1:
            self.effectiveness = 0.5  # Start at a neutral value
        self.effectiveness = (self.ema_alpha * current_outcome) + (1 - self.ema_alpha) * self.effectiveness


@dataclass
class KnowledgeEntry:
    """Represents an entry in the knowledge base."""

    entry_id: str
    category: str
    content: Dict[str, Any]
    confidence: float
    source: str  # "learned" or "evolved"
    generation_learned: int


class AttackKnowledgeBase:
    """A self-building knowledge base of attack patterns."""

    def __init__(self):
        self.signatures: Dict[str, AttackSignature] = {}
        self.principles: Dict[str, DefensivePrinciple] = {}
        self.knowledge: Dict[str, KnowledgeEntry] = {}
        self.generation = 0
        self.total_attacks_analyzed = 0
    
    def analyze_attack(self, payload: Any, attack_type: str, blocked: bool) -> AttackSignature:
        """Analyze attack and extract signature"""
        
        self.total_attacks_analyzed += 1
        
        # Extract characteristics
        characteristics = self._extract_characteristics(payload, attack_type)
        
        # Generate signature
        sig_hash = self._generate_signature_hash(characteristics)
        
        # Update or create signature
        if sig_hash in self.signatures:
            sig = self.signatures[sig_hash]
            sig.last_seen = self.generation
            if blocked:
                sig.block_count += 1
            else:
                sig.success_count += 1
        else:
            # Learn new signature
            family = self._classify_attack_family(characteristics)
            sig = AttackSignature(
                signature_id=sig_hash,
                family=family,
                characteristics=characteristics,
                first_seen=self.generation,
                last_seen=self.generation
            )
            if blocked:
                sig.block_count = 1
            else:
                sig.success_count = 1
            
            self.signatures[sig_hash] = sig
        
        return sig
    
    def _extract_characteristics(self, payload: Any, attack_type: str) -> Dict[str, Any]:
        """Extract observable characteristics from attack"""
        
        chars = {
            "attack_type": attack_type,
            "payload_type": type(payload).__name__,
            "has_quotes": "'" in str(payload) or '"' in str(payload),
            "has_semicolon": ";" in str(payload),
            "has_dashes": "--" in str(payload),
            "has_sql_keywords": any(kw in str(payload).upper() for kw in ["DROP", "SELECT", "DELETE", "UNION"]),
            "has_special_chars": any(c in str(payload) for c in ["<", ">", "{", "}", "%", "$"]),
            "is_encoded": self._detect_encoding(payload),
            "size_bytes": len(str(payload)),
            "is_complex_type": isinstance(payload, (dict, list, tuple)),
            "has_nested_structure": self._has_nested_structure(payload),
            "has_magic_methods": hasattr(payload, "__str__") or hasattr(payload, "__repr__"),
            "is_callable": callable(payload),
        }
        
        return chars
    
    def _detect_encoding(self, payload: Any) -> str:
        """Detect if payload is encoded"""
        payload_str = str(payload)
        
        if payload_str.startswith("data:") or "base64" in payload_str.lower():
            return "base64"
        if "%" in payload_str and any(c in payload_str for c in "0123456789ABCDEF"):
            return "url"
        if "\\x" in payload_str:
            return "hex"
        if "\\u" in payload_str:
            return "unicode"
        
        return "none"
    
    def _has_nested_structure(self, payload: Any) -> bool:
        """Check for nested data structures"""
        if isinstance(payload, dict):
            return any(isinstance(v, (dict, list)) for v in payload.values())
        if isinstance(payload, list):
            return any(isinstance(item, (dict, list)) for item in payload)
        return False
    
    def _classify_attack_family(self, characteristics: Dict) -> AttackFamily:
        """Classify attack into family based on a scoring system."""
        scores = {family: 0 for family in AttackFamily}

        # Define scoring rules
        rules = {
            AttackFamily.INJECTION: [
                ("has_sql_keywords", 3),
                ("has_quotes", 1),
                ("has_semicolon", 1),
            ],
            AttackFamily.ENCODING_OBFUSCATION: [
                ("is_encoded", lambda v: 3 if v != "none" else 0),
            ],
            AttackFamily.OVERFLOW: [
                ("size_bytes", lambda v: 3 if v > 1000 else 0),
            ],
            AttackFamily.TYPE_MANIPULATION: [
                ("is_complex_type", 2),
                ("has_magic_methods", 2),
            ],
            AttackFamily.STATE_CORRUPTION: [
                ("has_nested_structure", 3),
            ],
        }

        # Calculate scores
        for family, family_rules in rules.items():
            for characteristic, score in family_rules:
                value = characteristics.get(characteristic)
                if value:
                    if callable(score):
                        scores[family] += score(value)
                    else:
                        scores[family] += score

        # Determine the family with the highest score
        if any(s > 0 for s in scores.values()):
            highest_score_family = max(scores, key=scores.get)
            if scores[highest_score_family] > 0:
                return highest_score_family

        return AttackFamily.UNKNOWN
    
    def _generate_signature_hash(self, characteristics: Dict) -> str:
        """Generate unique signature hash"""
        # Use key characteristics for signature
        key_chars = {
            k: v for k, v in characteristics.items()
            if k in ["attack_type", "has_sql_keywords", "is_encoded", 
                    "is_complex_type", "has_nested_structure"]
        }
        sig_str = json.dumps(key_chars, sort_keys=True)
        return hashlib.md5(sig_str.encode()).hexdigest()[:12]
    
    def learn_principle(self, principle: DefensivePrinciple):
        """Add learned principle to knowledge base"""
        self.principles[principle.principle_id] = principle
    
    def get_relevant_principles(self, family: AttackFamily) -> List[DefensivePrinciple]:
        """Get principles applicable to attack family"""
        return [
            p for p in self.principles.values()
            if family in p.applicable_families
        ]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get knowledge base statistics"""
        family_counts = defaultdict(int)
        for sig in self.signatures.values():
            family_counts[sig.family.value] += 1
        
        return {
            "total_signatures": len(self.signatures),
            "total_principles": len(self.principles),
            "attacks_analyzed": self.total_attacks_analyzed,
            "family_distribution": dict(family_counts),
            "avg_principle_effectiveness": sum(p.effectiveness for p in self.principles.values()) / len(self.principles) if self.principles else 0
        }


# ============================================================================
# REASONING ENGINE - Analyzes and Synthesizes Strategies
# ============================================================================

class ReasoningEngine:
    """Analyzes attacks and synthesizes defensive strategies."""

    def __init__(self, knowledge_base: AttackKnowledgeBase):
        self.kb = knowledge_base
        self.reasoning_history: List[Dict] = []
    
    def analyze_failure(self, signature: AttackSignature, payload: Any) -> Dict[str, Any]:
        """Deep analysis of why an attack succeeded"""
        
        analysis = {
            "signature_id": signature.signature_id,
            "family": signature.family,
            "root_causes": [],
            "recommended_principles": [],
            "confidence": 0.0
        }
        
        # Analyze based on family
        if signature.family == AttackFamily.INJECTION:
            analysis["root_causes"].append("Insufficient input sanitization")
            analysis["root_causes"].append("Missing dangerous pattern detection")
            analysis["recommended_principles"].append("multi_layer_sanitization")
            analysis["recommended_principles"].append("pattern_blacklist_expansion")
        
        elif signature.family == AttackFamily.ENCODING_OBFUSCATION:
            encoding_type = signature.characteristics.get("is_encoded")
            analysis["root_causes"].append(f"Undetected {encoding_type} encoding")
            analysis["recommended_principles"].append("decode_before_check")
            analysis["recommended_principles"].append("multi_layer_decoding")
        
        elif signature.family == AttackFamily.TYPE_MANIPULATION:
            if signature.characteristics.get("has_magic_methods"):
                analysis["root_causes"].append("Trusts object-provided values")
                analysis["recommended_principles"].append("introspection_validation")
            if signature.characteristics.get("is_complex_type"):
                analysis["root_causes"].append("Insufficient type depth checking")
                analysis["recommended_principles"].append("recursive_type_validation")
        
        elif signature.family == AttackFamily.OVERFLOW:
            analysis["root_causes"].append("Bounds checking too lenient")
            analysis["recommended_principles"].append("strict_size_limits")
            analysis["recommended_principles"].append("memory_based_validation")
        
        elif signature.family == AttackFamily.STATE_CORRUPTION:
            analysis["root_causes"].append("Inadequate state protection")
            analysis["recommended_principles"].append("deep_state_inspection")
            analysis["recommended_principles"].append("protected_attribute_blocking")
        
        # Calculate confidence based on signature frequency
        analysis["confidence"] = min(signature.success_count / 10.0, 1.0)
        
        self.reasoning_history.append(analysis)
        return analysis
    
    def synthesize_defense_strategy(self, analyses: List[Dict]) -> List[str]:
        """Synthesize new defense strategy from analyses"""
        
        # Aggregate recommended principles
        principle_frequency = defaultdict(int)
        for analysis in analyses:
            for principle in analysis["recommended_principles"]:
                principle_frequency[principle] += 1
        
        # Prioritize by frequency and add to KB if new
        strategies = []
        for principle, freq in sorted(principle_frequency.items(), key=lambda x: x[1], reverse=True):
            if principle not in self.kb.principles:
                # Create new principle
                new_principle = self._create_principle(principle, analyses)
                self.kb.learn_principle(new_principle)
                strategies.append(f"LEARNED: {principle}")
            else:
                strategies.append(f"APPLY: {principle}")
        
        return strategies
    
    def _create_principle(self, principle_name: str, analyses: List[Dict]) -> DefensivePrinciple:
        """Create new defensive principle"""
        
        # Determine applicable families from analyses
        families = set()
        for analysis in analyses:
            if principle_name in analysis["recommended_principles"]:
                families.add(analysis["family"])
        
        descriptions = {
            "multi_layer_sanitization": "Apply sanitization checks at multiple processing stages",
            "pattern_blacklist_expansion": "Expand dangerous pattern list based on observed attacks",
            "decode_before_check": "Decode payloads before applying validation",
            "multi_layer_decoding": "Recursively decode multiple encoding layers",
            "introspection_validation": "Use introspection to validate object internals",
            "recursive_type_validation": "Recursively validate nested type structures",
            "strict_size_limits": "Enforce strict size and memory limits",
            "memory_based_validation": "Validate based on actual memory usage not reported size",
            "deep_state_inspection": "Deeply inspect object graphs for corruption",
            "protected_attribute_blocking": "Block access to protected attributes",
        }
        
        return DefensivePrinciple(
            principle_id=principle_name,
            description=descriptions.get(principle_name, "Unknown principle"),
            applicable_families=families,
            effectiveness=0.5
        )
    
    def meta_learn(self) -> Dict[str, Any]:
        """Analyze learning effectiveness and adapt learning strategy"""
        
        min_history = config.get("intelligence", "meta_learning")["min_history_for_analysis"]
        if len(self.reasoning_history) < min_history:
            return {"status": "insufficient_data"}
        
        # Analyze which principles work best
        principle_effectiveness = defaultdict(list)
        min_applications = config.get("intelligence", "meta_learning")["min_applications_for_pruning"]
        for principle in self.kb.principles.values():
            if principle.times_applied > min_applications:
                principle_effectiveness[principle.principle_id].append(principle.effectiveness)
        
        # Find patterns in successful and unsuccessful principles
        highly_effective_threshold = config.get("intelligence", "meta_learning")["highly_effective_threshold"]
        underperforming_threshold = config.get("intelligence", "meta_learning")["underperforming_threshold"]

        highly_effective = [
            pid for pid, effs in principle_effectiveness.items()
            if sum(effs) / len(effs) > highly_effective_threshold
        ]
        underperforming = [
            pid for pid, effs in principle_effectiveness.items()
            if sum(effs) / len(effs) < underperforming_threshold
        ]
        
        return {
            "status": "learned",
            "highly_effective_principles": highly_effective,
            "underperforming_principles": underperforming,
            "total_principles_learned": len(self.kb.principles),
            "learning_velocity": len(self.kb.signatures) / max(self.kb.generation, 1)
        }


# ============================================================================
# ADAPTIVE DEFENSE SYNTHESIZER
# ============================================================================

class AdaptiveDefenseSynthesizer:
    """Synthesizes new defense mechanisms from learned principles."""

    def __init__(self, knowledge_base: AttackKnowledgeBase, reasoning_engine: ReasoningEngine):
        self.kb = knowledge_base
        self.reasoning = reasoning_engine
        self.synthesized_defenses: Dict[str, Any] = {}
    
    def synthesize_from_principle(self, principle: DefensivePrinciple, seed: EvolvableSeed) -> str:
        """Create concrete defense from abstract principle"""
        
        defense_map = {
            "multi_layer_decoding": (DefenseType.SANITIZATION, 4),
            "introspection_validation": (DefenseType.TYPE_CHECKING, 4),
            "recursive_type_validation": (DefenseType.TYPE_CHECKING, 3),
            "memory_based_validation": (DefenseType.BOUNDS_ENFORCEMENT, 4),
            "deep_state_inspection": (DefenseType.STATE_PROTECTION, 4),
            "pattern_blacklist_expansion": (DefenseType.SANITIZATION, 2),
        }

        if principle.principle_id in defense_map:
            defense_type, strength = defense_map[principle.principle_id]
            return self._synth_defense(seed, defense_type, strength)

        return f"Applied principle: {principle.principle_id}"
    
    def _synth_defense(self, seed: EvolvableSeed, defense_type: DefenseType, strength: int) -> str:
        """Synthesize a defense by strengthening it"""
        seed.strengthen_defense(defense_type, strength)
        return f"🧠 SYNTHESIZED: Strengthened {defense_type.name} by {strength}"


# ============================================================================
# AUTONOMOUS INTELLIGENCE COORDINATOR
# ============================================================================

class AutonomousIntelligence:
    """Coordinates all intelligence components."""

    def __init__(self, seed: EvolvableSeed):
        self.seed = seed
        self.knowledge_base = AttackKnowledgeBase()
        self.reasoning_engine = ReasoningEngine(self.knowledge_base)
        self.synthesizer = AdaptiveDefenseSynthesizer(self.knowledge_base, self.reasoning_engine)
        self.generation = 0
    
    def process_attack_result(self, payload: Any, attack_type: str, blocked: bool) -> Dict[str, Any]:
        """Process single attack result and learn"""
        
        # Analyze and learn signature
        signature = self.knowledge_base.analyze_attack(payload, attack_type, blocked)
        
        result = {
            "signature": signature.signature_id,
            "family": signature.family.value,
            "learned_new": signature.first_seen == self.generation,
        }
        
        # If attack succeeded, analyze and synthesize defense
        if not blocked:
            analysis = self.reasoning_engine.analyze_failure(signature, payload)
            result["analysis"] = analysis
            
            # Synthesize defenses from recommended principles
            strategies = []
            for principle_name in analysis["recommended_principles"]:
                if principle_name in self.knowledge_base.principles:
                    principle = self.knowledge_base.principles[principle_name]
                else:
                    # Create principle through reasoning
                    principle = self.reasoning_engine._create_principle(
                        principle_name, 
                        [analysis]
                    )
                    self.knowledge_base.learn_principle(principle)
                
                strategy = self.synthesizer.synthesize_from_principle(principle, self.seed)
                strategies.append(strategy)
                
                # Update principle effectiveness
                principle.update_effectiveness(not blocked)
            
            result["strategies_applied"] = strategies
        
        return result
    
    def next_generation(self):
        """Advance to next generation"""
        self.generation += 1
        self.knowledge_base.generation = self.generation
    
    def get_intelligence_report(self) -> Dict[str, Any]:
        """Generate intelligence report"""
        stats = self.knowledge_base.get_statistics()
        meta = self.reasoning_engine.meta_learn()
        
        return {
            "generation": self.generation,
            "knowledge_base": stats,
            "meta_learning": meta,
            "total_principles": len(self.knowledge_base.principles),
            "principle_effectiveness": {
                p.principle_id: p.effectiveness
                for p in self.knowledge_base.principles.values()
            }
        }
    
    def print_intelligence_state(self):
        """Print current intelligence state"""
        logger.info(f"\n🧠 AUTONOMOUS INTELLIGENCE STATE (Gen {self.generation})")
        logger.info(f"{'='*90}")
        
        stats = self.knowledge_base.get_statistics()
        logger.info(f"\n📚 Knowledge Base:")
        logger.info(f"  Attack Signatures Learned: {stats['total_signatures']}")
        logger.info(f"  Defensive Principles: {stats['total_principles']}")
        logger.info(f"  Attacks Analyzed: {stats['attacks_analyzed']}")
        
        if stats['family_distribution']:
            logger.info(f"\n  Attack Family Distribution:")
            for family, count in stats['family_distribution'].items():
                logger.info(f"    {family:25} {count:3d} signatures")
        
        if self.knowledge_base.principles:
            logger.info(f"\n🎯 Learned Principles (Top 5):")
            sorted_principles = sorted(
                self.knowledge_base.principles.values(),
                key=lambda p: p.effectiveness,
                reverse=True
            )[:5]
            for p in sorted_principles:
                bar = "█" * int(p.effectiveness * 10) + "░" * (10 - int(p.effectiveness * 10))
                logger.info(f"  {p.principle_id:30} {bar} {p.effectiveness*100:5.1f}% ({p.times_applied} applied)")
        
        logger.info(f"{'='*90}\n")