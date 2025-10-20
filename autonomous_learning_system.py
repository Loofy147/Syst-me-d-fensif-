"""
AUTONOMOUS LEARNING SYSTEM - Complete Integration
==================================================

Brings together all components into a self-learning defense system that:
- Learns attack patterns from experience
- Reasons about attack families and relationships
- Synthesizes new defenses autonomously
- Faces orchestrated multi-scenario attacks
- Evolves faster with each generation (meta-learning)
"""

import time
from typing import Dict, List, Any
from core import EvolvableSeed, DefenseType
from autonomous_intelligence import AutonomousIntelligence
from orchestrated_attacks import ScenarioOrchestrator


# ============================================================================
# AUTONOMOUS LEARNING ORCHESTRATOR
# ============================================================================

class AutonomousLearningSystem:
    """Complete self-learning defense system"""
    
    def __init__(self, seed_name: str = "AutonomousDefenseSystem"):
        self.seed = EvolvableSeed(seed_name)
        self.intelligence = AutonomousIntelligence(self.seed)
        self.attack_orchestrator = ScenarioOrchestrator()
        self.generation = 0
        self.learning_history = []
    
    def run_learning_cycle(self, max_generations: int = 10):
        """Run complete autonomous learning cycle"""
        
        print("\n" + "="*90)
        print("🧠 AUTONOMOUS LEARNING SYSTEM - SELF-ADAPTIVE EVOLUTION")
        print("="*90)
        print(f"System: {self.seed.name}")
        print(f"Max Generations: {max_generations}")
        print(f"\nThe system will learn attack patterns, reason about defenses,")
        print(f"and synthesize new protections WITHOUT pre-programmed responses.\n")
        
        for gen in range(max_generations):
            self.generation = gen
            self.intelligence.next_generation()
            
            print(f"\n{'='*90}")
            print(f"🔄 GENERATION {gen} - AUTONOMOUS LEARNING CYCLE")
            print(f"{'='*90}")
            
            # Generate orchestrated attack campaign
            campaign = self.attack_orchestrator.generate_orchestrated_campaign(gen)
            
            # Process each attack and learn
            print(f"\n🎯 PROCESSING ATTACKS & LEARNING...")
            print(f"{'-'*90}")
            
            results = []
            blocked_count = 0
            
            for scenario_name, attack_type, payload in campaign:
                # Map attack_type to DefenseType
                defense_type = self._map_to_defense_type(attack_type)
                
                # Test defense
                blocked, reason = self.seed.test_defense(defense_type, payload)
                
                # Learn from result
                learning_result = self.intelligence.process_attack_result(
                    payload, attack_type, blocked
                )
                
                # Feed back to attack scenarios
                self.attack_orchestrator.learn_from_results(scenario_name, payload, blocked)
                
                results.append({
                    "scenario": scenario_name,
                    "blocked": blocked,
                    "learned": learning_result
                })
                
                if blocked:
                    blocked_count += 1
            
            fitness = (blocked_count / len(campaign) * 100) if campaign else 0
            
            # Generation summary
            print(f"\n📊 GENERATION {gen} RESULTS:")
            print(f"  Attacks Processed: {len(campaign)}")
            print(f"  Attacks Blocked: {blocked_count}/{len(campaign)}")
            print(f"  Defense Fitness: {fitness:.1f}%")
            
            # Show what was learned
            new_signatures = sum(1 for r in results if r["learned"].get("learned_new"))
            print(f"  New Patterns Learned: {new_signatures}")
            
            strategies_applied = sum(len(r["learned"].get("strategies_applied", [])) for r in results)
            print(f"  Strategies Synthesized: {strategies_applied}")
            
            # Display intelligence state
            self.intelligence.print_intelligence_state()
            
            # Display defense state
            self._print_defense_state()
            
            # Learning history
            self.learning_history.append({
                "generation": gen,
                "fitness": fitness,
                "blocked": blocked_count,
                "total": len(campaign),
                "new_signatures": new_signatures,
                "strategies": strategies_applied
            })
            
            # Check for mastery
            if fitness >= 95 and gen >= 3:
                print(f"\n🏆 MASTERY ACHIEVED: {fitness:.1f}% defense at generation {gen}")
                break
        
        # Final analysis
        self._print_final_analysis()
    
    def _map_to_defense_type(self, attack_type: str) -> DefenseType:
        """Map attack type string to DefenseType enum"""
        mapping = {
            "sql_injection": DefenseType.SANITIZATION,
            "input_validation": DefenseType.INPUT_VALIDATION,
            "type_checking": DefenseType.TYPE_CHECKING,
            "bounds_enforcement": DefenseType.BOUNDS_ENFORCEMENT,
            "state_protection": DefenseType.STATE_PROTECTION,
            "sanitization": DefenseType.SANITIZATION,
            "timing_probe": DefenseType.RATE_LIMITING,
            "timing_exploit": DefenseType.SANITIZATION,
            "context_attack": DefenseType.SANITIZATION,
            "swarm_attack": DefenseType.RATE_LIMITING,
            "swarm_combined": DefenseType.SANITIZATION,
            "evolutionary": DefenseType.SANITIZATION,
            "metamorphic": DefenseType.SANITIZATION,
            "combined": DefenseType.STATE_PROTECTION,
        }
        return mapping.get(attack_type, DefenseType.INPUT_VALIDATION)
    
    def _print_defense_state(self):
        """Print current defense state"""
        print(f"\n🛡️  CURRENT DEFENSE STATE:")
        snapshot = self.seed.get_defense_snapshot()
        for name, state in snapshot.items():
            status = "✓" if state['active'] else "✗"
            bar = "█" * state['strength'] + "░" * (10 - state['strength'])
            eff = state.get('effectiveness', 0) * 100
            print(f"  {status} {name:25} {bar} ({state['strength']:2d}/10) Eff: {eff:5.1f}%")
    
    def _print_final_analysis(self):
        """Print comprehensive final analysis"""
        
        print(f"\n{'='*90}")
        print("🎓 AUTONOMOUS LEARNING COMPLETE - FINAL ANALYSIS")
        print(f"{'='*90}")
        
        if not self.learning_history:
            return
        
        first = self.learning_history[0]
        last = self.learning_history[-1]
        
        print(f"\n📈 LEARNING PROGRESSION:")
        print(f"  Generation 0 Fitness: {first['fitness']:.1f}%")
        print(f"  Final Fitness: {last['fitness']:.1f}%")
        print(f"  Improvement: +{last['fitness'] - first['fitness']:.1f}%")
        
        total_signatures = self.intelligence.knowledge_base.get_statistics()['total_signatures']
        total_principles = len(self.intelligence.knowledge_base.principles)
        
        print(f"\n🧠 KNOWLEDGE ACQUIRED:")
        print(f"  Attack Signatures Learned: {total_signatures}")
        print(f"  Defensive Principles: {total_principles}")
        print(f"  Total Attacks Analyzed: {self.intelligence.knowledge_base.total_attacks_analyzed}")
        
        print(f"\n📊 GENERATION-BY-GENERATION:")
        print(f"  {'Gen':>3} | {'Fitness':>7} | {'Blocked':>7} | {'New Sigs':>8} | {'Strategies':>10}")
        print(f"  {'-'*3}-+-{'-'*7}-+-{'-'*7}-+-{'-'*8}-+-{'-'*10}")
        
        for entry in self.learning_history:
            print(f"  {entry['generation']:3d} | {entry['fitness']:6.1f}% | "
                  f"{entry['blocked']:2d}/{entry['total']:2d} | "
                  f"{entry['new_signatures']:8d} | {entry['strategies']:10d}")
        
        # Meta-learning analysis
        meta = self.intelligence.reasoning_engine.meta_learn()
        if meta.get("status") == "learned":
            print(f"\n🎯 META-LEARNING INSIGHTS:")
            print(f"  Learning Velocity: {meta.get('learning_velocity', 0):.2f} signatures/generation")
            print(f"  Highly Effective Principles: {len(meta.get('highly_effective_principles', []))}")
        
        # Scenario performance
        scenario_perf = self.attack_orchestrator.get_scenario_analysis()
        print(f"\n🎭 ATTACK SCENARIO EFFECTIVENESS (from attacker perspective):")
        for scenario, performance in sorted(scenario_perf.items(), key=lambda x: x[1], reverse=True):
            bar = "█" * int(performance * 10) + "░" * (10 - int(performance * 10))
            print(f"  {scenario:20} {bar} {performance*100:5.1f}%")
        
        # Intelligence report
        intel_report = self.intelligence.get_intelligence_report()
        print(f"\n🔬 INTELLIGENCE SYSTEM STATE:")
        print(f"  Knowledge Entries: {len(self.intelligence.knowledge_base.knowledge)}")
        print(f"  Reasoning Steps: {len(self.intelligence.reasoning_engine.reasoning_history)}")
        
        if intel_report["principle_effectiveness"]:
            print(f"\n  Top 3 Most Effective Principles:")
            sorted_principles = sorted(
                intel_report["principle_effectiveness"].items(),
                key=lambda x: x[1],
                reverse=True
            )[:3]
            for i, (principle, effectiveness) in enumerate(sorted_principles, 1):
                print(f"    {i}. {principle:30} {effectiveness*100:5.1f}%")
        
        print(f"\n{'='*90}")
        print("CONCLUSION")
        print(f"{'='*90}")
        print(f"\n✅ The system demonstrated AUTONOMOUS LEARNING:")
        print(f"   • Built knowledge base from experience ({total_signatures} attack patterns)")
        print(f"   • Reasoned about attack families and relationships")
        print(f"   • Synthesized {total_principles} defensive principles WITHOUT pre-programming")
        print(f"   • Adapted to {len(scenario_perf)} different attack scenarios")
        print(f"   • Improved fitness from {first['fitness']:.1f}% → {last['fitness']:.1f}%")
        print(f"\n🎯 The intelligence LEARNED, not just executed pre-programmed rules.\n")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Run autonomous learning system"""
    
    # Create autonomous system
    system = AutonomousLearningSystem("AutonomousDefender_v1")
    
    # Run learning cycle
    system.run_learning_cycle(max_generations=8)


if __name__ == "__main__":
    main()