"""
AUTONOMOUS LIVE DEFENSE SYSTEM
==============================

Orchestrates a live learning environment where an AI-driven WAF defends a
real, containerized web application from a live, intelligent Red Team.
"""

import time
import threading
import docker
from typing import Dict, List, Any

from src.core.models import EvolvableSeed
from src.intelligence import AutonomousIntelligence
from src.attacks.advanced import AdvancedRedTeamExecutor
from src.attacks.intelligence import AttackerIntelligence
from src.proxy import run_proxy
from src.config import config
from src.logger import logger
from src.core.models import DefenseType


class AutonomousLearningSystem:
    """The main orchestrator for the live autonomous learning system."""

    def __init__(self, seed_name: str = "AutonomousDefender_Live"):
        self.seed = EvolvableSeed(seed_name)
        self.intelligence = AutonomousIntelligence(self.seed)

        # Attacker setup
        self.attacker_intelligence = AttackerIntelligence()
        self.red_team_executor = AdvancedRedTeamExecutor(None, self.attacker_intelligence) # No direct target

        self.generation = 0
        self.learning_history = []

        # Live environment components
        self.docker_client = docker.from_env()
        self.target_container = None
        self.proxy_server = None
        self.proxy_thread = None

    def run_learning_cycle(self):
        """Run the complete live learning and defense cycle."""

        max_generations = config.get("simulation", "max_generations")
        proxy_port = config.get("proxy", "port")
        app_port = config.get("target_app", "port")
        waf_url = f"http://localhost:{proxy_port}/login"

        try:
            # --- Setup Live Environment ---
            logger.info("🚀 Setting up live defense environment...")
            self._start_target_app(app_port)
            self._start_proxy(app_port, proxy_port)
            time.sleep(2) # Give servers a moment to start

            # --- Main Learning Loop ---
            for gen in range(max_generations):
                self.generation = gen
                self.intelligence.next_generation()
                self.attacker_intelligence.next_generation()
                self.red_team_executor.generation = gen

                logger.info(f"\n{'='*90}")
                logger.info(f"🔄 GENERATION {gen} - LIVE DEFENSE CYCLE")
                logger.info(f"{'='*90}")

                # Execute live attacks against the WAF
                results, blocked_count, total_attacks, fitness = self.red_team_executor.execute_advanced_suite(waf_url)

                # The defensive learning now happens implicitly as the WAF uses the seed.
                # We still need to process results to update our history and metrics.
                for exploit in results:
                    self.intelligence.process_attack_result(
                        exploit.payload, exploit.vector.name, exploit.blocked
                    )

                self._update_learning_history(gen, fitness, blocked_count, total_attacks, results)
                self.intelligence.print_intelligence_state()
                self._print_defense_state()
                self.attacker_intelligence.print_intelligence_state()

                # Meta-learning and pruning
                self.intelligence.reasoning_engine.meta_learn()

        finally:
            # --- Teardown Live Environment ---
            logger.info("🔥 Tearing down live defense environment...")
            self._stop_proxy()
            self._stop_target_app()
            logger.info("✅ System run complete.")

    def _start_target_app(self, app_port: int):
        """Build and run the vulnerable Flask app in a Docker container."""
        logger.info("   - Building and starting target application container...")
        try:
            image, _ = self.docker_client.images.build(path="./target_app", tag="vulnerable-app")
            self.target_container = self.docker_client.containers.run(
                image,
                detach=True,
                ports={f'5000/tcp': app_port},
                name="vulnerable-app-instance"
            )
            logger.info(f"   ✓ Target app running in container: {self.target_container.short_id}")
        except Exception as e:
            logger.error(f"   ✗ Failed to start target app container: {e}")
            raise

    def _stop_target_app(self):
        """Stop and remove the Docker container."""
        if self.target_container:
            logger.info("   - Stopping target application container...")
            try:
                self.target_container.stop()
                self.target_container.remove()
                logger.info("   ✓ Target app container stopped and removed.")
            except docker.errors.NotFound:
                pass # Container might already be gone
            except Exception as e:
                logger.error(f"   ✗ Error stopping target app container: {e}")

    def _start_proxy(self, app_port: int, proxy_port: int):
        """Run the WAF proxy in a background thread."""
        logger.info("   - Starting AI Firewall (WAF Proxy)...")
        self.proxy_server = run_proxy(
            self.seed,
            'localhost',
            app_port,
            proxy_port
        )
        self.proxy_thread = threading.Thread(target=self.proxy_server.serve_forever)
        self.proxy_thread.daemon = True
        self.proxy_thread.start()
        logger.info(f"   ✓ AI Firewall is live on port {proxy_port}.")

    def _stop_proxy(self):
        """Stop the WAF proxy server."""
        if self.proxy_server:
            logger.info("   - Shutting down AI Firewall...")
            self.proxy_server.shutdown()
            self.proxy_server.server_close()
            logger.info("   ✓ AI Firewall shut down.")

    def _update_learning_history(self, gen, fitness, blocked_count, total_attacks, results):
        """Update the learning history with results from the generation."""
        new_signatures = sum(1 for r in results if not r.blocked)
        strategies_applied = len(self.intelligence.reasoning_engine.reasoning_history)

        self.learning_history.append({
            "generation": gen,
            "fitness": fitness,
            "attacker_success_rate": self.attacker_intelligence.get_success_rate(),
            "defense_strengths": self.seed.get_defense_snapshot(),
            "blocked": blocked_count,
            "total": total_attacks,
            "new_signatures": new_signatures,
            "strategies": strategies_applied
        })

    def _print_defense_state(self):
        """Print current defense state"""
        logger.info(f"\n🛡️  CURRENT DEFENSE STATE:")
        snapshot = self.seed.get_defense_snapshot()
        for name, state in snapshot.items():
            status = "✓" if state['active'] else "✗"
            bar = "█" * state['strength'] + "░" * (10 - state['strength'])
            logger.info(f"  {status} {name:25} {bar} ({state['strength']:2d}/10)")
