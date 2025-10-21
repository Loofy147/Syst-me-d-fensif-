from src.orchestration import AutonomousLearningSystem
from src.logger import logger
from src.visualization import generate_visualization_report


def main():
    """Run autonomous learning system"""
    logger.info("🚀 Starting Autonomous Learning System...")
    system = AutonomousLearningSystem("AutonomousDefender_v2")
    system.run_learning_cycle()

    # Generate visualization report from the learning history
    if system.learning_history:
        generate_visualization_report(system.learning_history)

    logger.info("✅ System run complete.")


if __name__ == "__main__":
    main()
