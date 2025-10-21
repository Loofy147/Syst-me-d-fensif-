# Checklists

This document provides checklists for common tasks that developers and users may need to perform.

## Adding a New Attack Scenario

*   [ ] Create a new class that inherits from `AttackScenario`.
*   [ ] Implement the `generate_wave` method to generate a list of attack payloads.
*   [ ] Add the new scenario to the `SCENARIOS` dictionary in `src/attacks/orchestration.py`.
*   [ ] Add a new `AttackType` enum value for the new scenario.
*   [ ] Add a new mapping from the `AttackType` to a `DefenseType` in `src/orchestration.py`.
*   [ ] Run the tests to ensure that the new scenario is working correctly.

## Adding a New Defense Mechanism

*   [ ] Create a new class that inherits from `DefenseMechanism`.
*   [ ] Implement the `evaluate` method to determine whether a given payload should be blocked.
*   [ ] Add the new defense mechanism to the `DEFENSES` dictionary in `src/core/models.py`.
*   [ ] Run the tests to ensure that the new defense mechanism is working correctly.

## Running an Experiment

*   [ ] Configure the experiment in a new configuration file.
*   [ ] Run the experiment using the `main.py` script.
*   [ ] Analyze the results of the experiment.
*   [ ] Document the results of the experiment.
