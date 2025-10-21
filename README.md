# Autonomous Learning System

This project is an autonomous, self-learning defense system designed to evolve and counter simulated cyber attacks. The system is built with a modular architecture that allows for easy extension and experimentation.

## 🚀 Getting Started

To get started with the Autonomous Learning System, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/autonomous-learning-system.git
    ```
2.  **Navigate to the project directory:**
    ```bash
    cd autonomous-learning-system
    ```
3.  **Run the application:**
    ```bash
    python3 main.py
    ```
4.  **View the logs:**
    The system's output is logged to both the console and the `system_run.log` file.

##  Architecture

The system is organized into the following modules:

*   **`src/core`**: Contains the basic data structures and classes that are used across the entire application.
*   **`src/attacks`**: Contains the logic for generating and orchestrating attack scenarios.
*   **`src/defenses`**: Contains the logic for the defense mechanisms.
*   **`src/intelligence`**: Contains the "brains" of the operation, including the knowledge base and reasoning engine.
*   **`src/orchestration`**: Contains the main learning loop and orchestrates the interactions between the other modules.
*   **`main.py`**: The single entry point for running the application.

For a more detailed explanation of the system's design, please see the `ARCHITECTURE.md` file.

## ⚙️ Configuration

The system's parameters can be configured in the `config.json` file. This file allows you to adjust the simulation's settings, such as the number of generations to run, the thresholds for meta-learning, and the logging level.

## 📝 License

This project is licensed under the MIT License - see the `LICENSE` file for details.
