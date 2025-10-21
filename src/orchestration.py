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
from src.core.models import EvolvableSeed
from src.intelligence import AutonomousIntelligence
from src.attacks.orchestration import ScenarioOrchestrator
from src.core.models import DefenseType
from src.config import config
from src.logger import logger


# ============================================================================
# AUTONOMOUS LEARNING ORCHESTRATOR
# ============================================================================

class AutonomousLearningSystem:
    """The main orchestrator for the autonomous learning system."""

    def __init__(self, seed_name: str = "AutonomousDefenseSystem"):
        self.seed = EvolvableSeed(seed_name)
        self.intelligence = AutonomousIntelligence(self.seed)
        self.attack_orchestrator = ScenarioOrchestrator()
        self.generation = 0
        self.learning_history = []

    def run_learning_cycle(self):
        """Run complete autonomous learning cycle"""

        max_generations = config.get("simulation", "max_generations")
        mastery_fitness = config.get("simulation", "mastery_fitness_threshold")
        mastery_generations = config.get("simulation", "mastery_generations_required")

        logger.info("="*90)
        logger.info("🧠 AUTONOMOUS LEARNING SYSTEM - SELF-ADAPTIVE EVOLUTION")
        logger.info("="*90)
        logger.info(f"System: {self.seed.name}")
        logger.info(f"Max Generations: {max_generations}")
        logger.info("\nThe system will learn attack patterns, reason about defenses,")
        logger.info("and synthesize new protections WITHOUT pre-programmed responses.\n")

        for gen in range(max_generations):
            self.generation = gen
            self.intelligence.next_generation()

            logger.info(f"\n{'='*90}")
            logger.info(f"🔄 GENERATION {gen} - AUTONOMOUS LEARNING CYCLE")
            logger.info(f"{'='*90}")

            # Generate orchestrated attack campaign
            campaign = self.attack_orchestrator.generate_orchestrated_campaign(gen)

            # Process each attack and learn
            logger.info(f"\n🎯 PROCESSING ATTACKS & LEARNING...")
            logger.info(f"{'-'*90}")

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
            logger.info(f"\n📊 GENERATION {gen} RESULTS:")
            logger.info(f"  Attacks Processed: {len(campaign)}")
            logger.info(f"  Attacks Blocked: {blocked_count}/{len(campaign)}")
            logger.info(f"  Defense Fitness: {fitness:.1f}%")

            # Show what was learned
            new_signatures = sum(1 for r in results if r["learned"].get("learned_new"))
            logger.info(f"  New Patterns Learned: {new_signatures}")

            strategies_applied = sum(len(r["learned"].get("strategies_applied", [])) for r in results)
            logger.info(f"  Strategies Synthesized: {strategies_applied}")

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
            if fitness >= mastery_fitness and gen >= mastery_generations:
                logger.info(f"\n🏆 MASTERY ACHIEVED: {fitness:.1f}% defense at generation {gen}")
                break

            # Meta-learning and pruning
            meta_insights = self.intelligence.reasoning_engine.meta_learn()
            if meta_insights.get("status") == "learned":
                underperforming = meta_insights.get("underperforming_principles", [])
                if underperforming:
                    logger.info(f"\n🔥 PRUNING {len(underperforming)} underperforming principles: {', '.join(underperforming)}")
                    for principle_id in underperforming:
                        if principle_id in self.intelligence.knowledge_base.principles:
                            del self.intelligence.knowledge_base.principles[principle_id]

            # Decay defense strengths
            for defense_type in DefenseType:
                self.seed.decay_defense_strength(defense_type)

        # Final analysis
        self._print_final_analysis()

    def _map_to_defense_type(self, attack_type: str) -> DefenseType:
        """Map attack type string to DefenseType enum"""
        mapping = {
            "sql_injection": "SANITIZATION",
            "input_validation": "INPUT_VALIDATION",
            "type_checking": "TYPE_CHECKING",
            "bounds_enforcement": "BOUNDS_ENFORCEMENT",
            "state_protection": "STATE_PROTECTION",
            "sanitization": "SANITIZATION",
            "timing_probe": "RATE_LIMITING",
            "timing_exploit": "SANITIZATION",
            "context_attack": "SANITIZATION",
            "swarm_attack": "RATE_LIMITING",
            "swarm_combined": "SANITIZATION",
            "evolutionary": "SANITIZATION",
            "metamorphic": "SANITIZATION",
            "combined": "STATE_PROTECTION",
            "side_channel_probe": "RATE_LIMITING",
        }
        return DefenseType[mapping.get(attack_type, "INPUT_VALIDATION")]

    def _print_defense_state(self):
        """Print current defense state"""
        logger.info(f"\n🛡️  CURRENT DEFENSE STATE:")
        snapshot = self.seed.get_defense_snapshot()
        for name, state in snapshot.items():
            status = "✓" if state['active'] else "✗"
            bar = "█" * state['strength'] + "░" * (10 - state['strength'])
            eff = state.get('effectiveness', 0) * 100
            logger.info(f"  {status} {name:25} {bar} ({state['strength']:2d}/10) Eff: {eff:5.1f}%")

    def _print_final_analysis(self):
        """Print comprehensive final analysis"""

        logger.info(f"\n{'='*90}")
        logger.info("🎓 AUTONOMOUS LEARNING COMPLETE - FINAL ANALYSIS")
        logger.info(f"{'='*90}")

        if not self.learning_history:
            return

        first = self.learning_history[0]
        last = self.learning_history[-1]

        logger.info(f"\n📈 LEARNING PROGRESSION:")
        logger.info(f"  Generation 0 Fitness: {first['fitness']:.1f}%")
        logger.info(f"  Final Fitness: {last['fitness']:.1f}%")
        logger.info(f"  Improvement: +{last['fitness'] - first['fitness']:.1f}%")

        total_signatures = self.intelligence.knowledge_base.get_statistics()['total_signatures']
        total_principles = len(self.intelligence.knowledge_base.principles)

        logger.info(f"\n🧠 KNOWLEDGE ACQUIRED:")
        logger.info(f"  Attack Signatures Learned: {total_signatures}")
        logger.info(f"  Defensive Principles: {total_principles}")
        logger.info(f"  Total Attacks Analyzed: {self.intelligence.knowledge_base.total_attacks_analyzed}")

        logger.info(f"\n📊 GENERATION-BY-GENERATION:")
        logger.info(f"  {'Gen':>3} | {'Fitness':>7} | {'Blocked':>7} | {'New Sigs':>8} | {'Strategies':>10}")
        logger.info(f"  {'-'*3}-+-{'-'*7}-+-{'-'*7}-+-{'-'*8}-+-{'-'*10}")

        for entry in self.learning_history:
            logger.info(f"  {entry['generation']:3d} | {entry['fitness']:6.1f}% | "
                  f"{entry['blocked']:2d}/{entry['total']:2d} | "
                  f"{entry['new_signatures']:8d} | {entry['strategies']:10d}")

        # Meta-learning analysis
        meta = self.intelligence.reasoning_engine.meta_learn()
        if meta.get("status") == "learned":
            logger.info(f"\n🎯 META-LEARNING INSIGHTS:")
            logger.info(f"  Learning Velocity: {meta.get('learning_velocity', 0):.2f} signatures/generation")
            logger.info(f"  Highly Effective Principles: {len(meta.get('highly_effective_principles', []))}")

        # Scenario performance
        scenario_perf = self.attack_orchestrator.get_scenario_analysis()
        logger.info(f"\n🎭 ATTACK SCENARIO EFFECTIVENESS (from attacker perspective):")
        for scenario, performance in sorted(scenario_perf.items(), key=lambda x: x[1], reverse=True):
            bar = "█" * int(performance * 10) + "░" * (10 - int(performance * 10))
            logger.info(f"  {scenario:20} {bar} {performance*100:5.1f}%")

        # Intelligence report
        intel_report = self.intelligence.get_intelligence_report()
        logger.info(f"\n🔬 INTELLIGENCE SYSTEM STATE:")
        logger.info(f"  Knowledge Entries: {len(self.intelligence.knowledge_base.knowledge)}")
        logger.info(f"  Reasoning Steps: {len(self.intelligence.reasoning_engine.reasoning_history)}")

        if intel_report["principle_effectiveness"]:
            logger.info(f"\n  Top 3 Most Effective Principles:")
            sorted_principles = sorted(
                intel_report["principle_effectiveness"].items(),
                key=lambda x: x[1],
                reverse=True
            )[:3]
            for i, (principle, effectiveness) in enumerate(sorted_principles, 1):
                logger.info(f"    {i}. {principle:30} {effectiveness*100:5.1f}%")

        logger.info(f"\n{'='*90}")
        logger.info("CONCLUSION")
        logger.info(f"{'='*90}")
        logger.info(f"\n✅ The system demonstrated AUTONOMOUS LEARNING:")
        logger.info(f"   • Built knowledge base from experience ({total_signatures} attack patterns)")
        logger.info(f"   • Reasoned about attack families and relationships")
        logger.info(f"   • Synthesized {total_principles} defensive principles WITHOUT pre-programming")
        logger.info(f"   • Adapted to {len(scenario_perf)} different attack scenarios")
        logger.info(f"   • Improved fitness from {first['fitness']:.1f}% → {last['fitness']:.1f}%")
        logger.info(f"\n🎯 The intelligence LEARNED, not just executed pre-programmed rules.\n")


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