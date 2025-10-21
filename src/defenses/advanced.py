"""
ULTIMATE DEFENSE MECHANISMS - Counter Advanced Attacks
=======================================================

Implements sophisticated defenses for advanced attack patterns:
- Multi-layer decoding
- Deep object inspection
- Magic method validation
- Introspection-based type checking
"""

import base64
import sys
from typing import Any, Tuple
from src.core.models import DefenseMechanism, DefenseConfig, DefenseType
from src.logger import logger


# ============================================================================
# ADVANCED SANITIZATION - Multi-layer Decoding
# ============================================================================

class AdvancedSanitizationDefense(DefenseMechanism):
    """Sanitization with multi-layer decoding"""
    
    def evaluate(self, value: Any) -> Tuple[bool, str]:
        """Check raw and decoded versions"""
        
        dangerous = ["'", '"', ";", "--", "/*", "*/", "DROP", "DELETE", "UNION", 
                    "SELECT", "INSERT", "UPDATE", "OR", "AND", "EXEC", "EVAL"]
        
        if self.config.strength >= 8:
            dangerous.extend(["<", ">", "{", "}", "[", "]", "$", "\\x", "%"])
        
        # Check raw value
        value_str = str(value).upper()
        for pattern in dangerous:
            if pattern in value_str:
                return True, f"Rejected: dangerous pattern '{pattern}' (raw)"
        
        # Decode and check Base64
        if self.config.strength >= 6:
            try:
                decoded = base64.b64decode(str(value)).decode('utf-8', errors='ignore').upper()
                for pattern in dangerous:
                    if pattern in decoded:
                        return True, f"Rejected: dangerous pattern '{pattern}' (base64 decoded)"
            except:
                pass
        
        # Decode and check URL encoding
        if self.config.strength >= 7:
            try:
                import urllib.parse
                decoded = urllib.parse.unquote(str(value)).upper()
                for pattern in dangerous:
                    if pattern in decoded:
                        return True, f"Rejected: dangerous pattern '{pattern}' (URL decoded)"
                
                # Double URL decode
                double_decoded = urllib.parse.unquote(decoded).upper()
                for pattern in dangerous:
                    if pattern in double_decoded:
                        return True, f"Rejected: dangerous pattern '{pattern}' (double URL decoded)"
            except:
                pass
        
        # Check hex encoding
        if self.config.strength >= 8:
            hex_patterns = ["\\x27", "\\x22", "\\x3b", "\\x2d\\x2d"]
            for pattern in hex_patterns:
                if pattern.lower() in str(value).lower():
                    return True, f"Rejected: hex encoded dangerous pattern"
        
        # Check unicode tricks
        if self.config.strength >= 9:
            # Zero-width characters used for obfuscation
            zero_width = ["\u200b", "\u200c", "\u200d", "\ufeff"]
            for zwc in zero_width:
                if zwc in str(value):
                    return True, f"Rejected: zero-width character obfuscation"
        
        return False, "Passed advanced sanitization"


# ============================================================================
# DEEP TYPE INSPECTION - Magic Method Validation
# ============================================================================

class DeepTypeInspectionDefense(DefenseMechanism):
    """Type checking with deep object introspection"""
    
    def evaluate(self, value: Any) -> Tuple[bool, str]:
        """Deep inspection of object structure"""
        
        # Basic type rejection
        if isinstance(value, (list, dict, tuple, set)):
            return True, f"Rejected: {type(value).__name__} type"
        
        # Check for custom classes
        if self.config.strength >= 7:
            if hasattr(value, '__dict__') and not isinstance(value, (str, int, float, bool)):
                return True, f"Rejected: custom class instance"
        
        # Check for dangerous magic methods
        if self.config.strength >= 8:
            dangerous_methods = ['__str__', '__repr__', '__call__', '__del__', 
                                '__getattr__', '__setattr__', '__dict__']
            
            for method in dangerous_methods:
                if hasattr(value, method):
                    try:
                        method_obj = getattr(type(value), method, None)
                        # Check if it's custom-defined (not inherited from object)
                        if method_obj is not None and method_obj != getattr(object, method, None):
                            return True, f"Rejected: custom {method} implementation"
                    except:
                        pass
        
        # Check for metaclass manipulation
        if self.config.strength >= 9:
            value_type = type(value)
            if type(value_type) != type:
                return True, f"Rejected: custom metaclass detected"
        
        # Check for properties
        if self.config.strength >= 9:
            if hasattr(type(value), '__dict__'):
                for attr_name in dir(type(value)):
                    try:
                        attr = getattr(type(value), attr_name)
                        if isinstance(attr, property):
                            return True, f"Rejected: property-based object"
                    except:
                        pass
        
        # Check for generators/iterators
        if self.config.strength >= 6:
            if hasattr(value, '__iter__') and not isinstance(value, (str, bytes)):
                return True, f"Rejected: iterator/generator type"
        
        # Check for callables
        if self.config.strength >= 7:
            if callable(value) and not isinstance(value, type):
                return True, f"Rejected: callable object"
        
        return False, "Passed deep type inspection"


# ============================================================================
# INTROSPECTION BOUNDS ENFORCEMENT - Actual Size Validation
# ============================================================================

class IntrospectionBoundsDefense(DefenseMechanism):
    """Bounds checking with actual memory inspection"""
    
    def evaluate(self, value: Any) -> Tuple[bool, str]:
        """Check actual size, not reported size"""
        
        max_len = 50 - (10 - self.config.strength) * 3
        
        # For strings - check actual length, not __len__
        if isinstance(value, str):
            # Use sys.getsizeof for actual memory size
            actual_size = sys.getsizeof(value)
            if actual_size > max_len * 10:  # Rough heuristic
                return True, f"Rejected: actual size {actual_size} bytes"
            
            # Also iterate and count (bypass __len__ override)
            try:
                count = sum(1 for _ in value)
                if count > max_len:
                    return True, f"Rejected: actual length {count} chars"
            except:
                pass
        
        # For objects with __len__ - don't trust it
        if self.config.strength >= 8:
            if hasattr(value, '__len__'):
                # Check if __len__ is overridden
                if hasattr(type(value), '__len__'):
                    len_method = getattr(type(value), '__len__')
                    if len_method != getattr(list, '__len__', None):
                        return True, f"Rejected: custom __len__ implementation"
        
        # Check actual memory size
        if self.config.strength >= 9:
            try:
                actual_bytes = sys.getsizeof(value)
                if actual_bytes > 10000:  # 10KB limit
                    return True, f"Rejected: memory size {actual_bytes} bytes"
            except:
                pass
        
        # For collections - check recursively
        if isinstance(value, (list, dict)):
            try:
                if isinstance(value, list):
                    if len(value) > max_len / 2:
                        return True, f"Rejected: collection too large"
                elif isinstance(value, dict):
                    if len(value) > max_len / 2:
                        return True, f"Rejected: dictionary too large"
            except:
                pass
        
        return False, "Passed introspection bounds check"


# ============================================================================
# STATE PROTECTION WITH DEEP INSPECTION
# ============================================================================

class DeepStateProtectionDefense(DefenseMechanism):
    """State protection with deep object graph inspection"""
    
    def evaluate(self, value: Any) -> Tuple[bool, str]:
        """Deep inspection of state corruption attempts"""
        
        # Check for protected attribute names
        protected_attrs = ["_protected", "_private", "_internal", "__proto__", 
                          "__class__", "__dict__", "__builtins__"]
        
        value_str = str(value)
        for attr in protected_attrs:
            if attr in value_str:
                return True, f"Rejected: protected attribute '{attr}'"
        
        # Check for code execution patterns
        exec_patterns = ["exec", "eval", "compile", "__import__"]
        for pattern in exec_patterns:
            if pattern in value_str:
                return True, f"Rejected: code execution pattern '{pattern}'"
        
        # Deep dictionary inspection
        if isinstance(value, dict):
            for key, val in value.items():
                key_str = str(key)
                
                # Check keys
                for attr in protected_attrs:
                    if attr in key_str:
                        return True, f"Rejected: protected key '{key}'"
                
                # Recursive check for nested dicts
                if isinstance(val, dict):
                    for nested_key in val.keys():
                        if any(attr in str(nested_key) for attr in protected_attrs):
                            return True, f"Rejected: nested protected key"
        
        # Check for circular references (can crash parsers)
        if self.config.strength >= 9:
            try:
                if isinstance(value, dict):
                    # Simple circular reference check
                    for key, val in value.items():
                        if val is value:
                            return True, f"Rejected: circular reference detected"
            except:
                pass
        
        return False, "Passed deep state protection"


# ============================================================================
# ULTIMATE DEFENSE FRAMEWORK
# ============================================================================

def upgrade_to_ultimate_defenses(seed):
    """Upgrade seed to use ultimate defense mechanisms"""
    
    logger.info(f"\n{'='*90}")
    logger.info("🛡️  UPGRADING TO ULTIMATE DEFENSE FRAMEWORK")
    logger.info(f"{'='*90}\n")
    
    # Replace defense mechanisms
    upgrades = []
    
    # Upgrade Sanitization
    old_sanitize = seed.defense_framework.defenses[DefenseType.SANITIZATION]
    new_config = DefenseConfig(DefenseType.SANITIZATION, 
                              active=True, 
                              strength=old_sanitize.config.strength)
    seed.defense_framework.defenses[DefenseType.SANITIZATION] = AdvancedSanitizationDefense(new_config)
    upgrades.append("✓ Upgraded SANITIZATION → Multi-layer decoding defense")
    
    # Upgrade Type Checking
    old_type = seed.defense_framework.defenses[DefenseType.TYPE_CHECKING]
    new_config = DefenseConfig(DefenseType.TYPE_CHECKING,
                              active=True,
                              strength=old_type.config.strength)
    seed.defense_framework.defenses[DefenseType.TYPE_CHECKING] = DeepTypeInspectionDefense(new_config)
    upgrades.append("✓ Upgraded TYPE_CHECKING → Deep introspection defense")
    
    # Upgrade Bounds Enforcement
    old_bounds = seed.defense_framework.defenses[DefenseType.BOUNDS_ENFORCEMENT]
    new_config = DefenseConfig(DefenseType.BOUNDS_ENFORCEMENT,
                              active=True,
                              strength=old_bounds.config.strength)
    seed.defense_framework.defenses[DefenseType.BOUNDS_ENFORCEMENT] = IntrospectionBoundsDefense(new_config)
    upgrades.append("✓ Upgraded BOUNDS_ENFORCEMENT → Introspection-based validation")
    
    # Upgrade State Protection
    old_state = seed.defense_framework.defenses[DefenseType.STATE_PROTECTION]
    new_config = DefenseConfig(DefenseType.STATE_PROTECTION,
                              active=True,
                              strength=old_state.config.strength)
    seed.defense_framework.defenses[DefenseType.STATE_PROTECTION] = DeepStateProtectionDefense(new_config)
    upgrades.append("✓ Upgraded STATE_PROTECTION → Deep graph inspection")
    
    for upgrade in upgrades:
        logger.info(f"  {upgrade}")
    
    # Strengthen all upgraded defenses
    logger.info(f"\n  🔧 Strengthening upgraded defenses...")
    seed.strengthen_defense(DefenseType.SANITIZATION, 3)
    seed.strengthen_defense(DefenseType.TYPE_CHECKING, 3)
    seed.strengthen_defense(DefenseType.BOUNDS_ENFORCEMENT, 3)
    seed.strengthen_defense(DefenseType.STATE_PROTECTION, 3)
    
    logger.info(f"  ✓ All defenses strengthened by +3\n")
    
    return upgrades

