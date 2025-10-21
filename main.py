from src.orchestration import AutonomousLearningSystem
from src.logger import logger


def main():
    """Run autonomous learning system"""
    logger.info("🚀 Starting Autonomous Learning System...")
    system = AutonomousLearningSystem("AutonomousDefender_v2")
    system.run_learning_cycle()
    logger.info("✅ System run complete.")


if __name__ == "__main__":
    main()
