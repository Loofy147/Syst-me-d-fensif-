"""
RESULTS VISUALIZATION MODULE
============================

Generates insightful charts and visualizations from simulation results.
"""

import os
import matplotlib.pyplot as plt
from typing import List, Dict, Any

def plot_fitness_over_time(history: List[Dict[str, Any]], output_dir: str):
    """Plots defender fitness and attacker success rate over generations."""

    generations = [h['generation'] for h in history]
    defender_fitness = [h['fitness'] for h in history]
    attacker_success = [h['attacker_success_rate'] * 100 for h in history]

    fig, ax1 = plt.subplots(figsize=(12, 7))

    # Plot Defender Fitness on the left y-axis
    ax1.plot(generations, defender_fitness, 'g-', label='Defender Fitness', linewidth=2)
    ax1.set_xlabel('Generation')
    ax1.set_ylabel('Defender Fitness (%)', color='g')
    ax1.tick_params('y', colors='g')
    ax1.grid(True, linestyle='--', alpha=0.6)

    # Create a second y-axis for Attacker Success Rate
    ax2 = ax1.twinx()
    ax2.plot(generations, attacker_success, 'r-', label='Attacker Success Rate', linewidth=2)
    ax2.set_ylabel('Attacker Success Rate (%)', color='r')
    ax2.tick_params('y', colors='r')

    plt.title('Co-evolution: Defender Fitness vs. Attacker Success Rate', fontsize=16)
    fig.tight_layout()

    # Add legends
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=2)

    plt.savefig(os.path.join(output_dir, 'fitness_vs_success.png'), bbox_inches='tight')
    plt.close()

def plot_defense_strength_evolution(history: List[Dict[str, Any]], output_dir: str):
    """Plots the evolution of each defense mechanism's strength."""

    if not history:
        return

    generations = [h['generation'] for h in history]

    # Extract defense names from the first history entry
    defense_names = history[0]['defense_strengths'].keys()

    defense_strengths = {name: [] for name in defense_names}

    for h in history:
        for name in defense_names:
            defense_strengths[name].append(h['defense_strengths'][name]['strength'])

    plt.figure(figsize=(12, 7))

    for name, strengths in defense_strengths.items():
        plt.plot(generations, strengths, label=name.replace('_', ' ').title(), linewidth=2)

    plt.title('Evolution of Defense Mechanism Strengths', fontsize=16)
    plt.xlabel('Generation')
    plt.ylabel('Strength (1-10)')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout(rect=[0, 0, 0.85, 1]) # Adjust layout to make room for legend

    plt.savefig(os.path.join(output_dir, 'defense_strength_evolution.png'))
    plt.close()

def generate_visualization_report(history: List[Dict[str, Any]]):
    """Generates and saves all visualization charts."""

    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"\n📊 Generating visualization report in '{output_dir}/'...")

    try:
        plot_fitness_over_time(history, output_dir)
        plot_defense_strength_evolution(history, output_dir)
        print("   ✓ Fitness vs. Attacker Success chart saved.")
        print("   ✓ Defense Strength Evolution chart saved.")
    except Exception as e:
        print(f"   ✗ Error generating visualizations: {e}")
        return

    print("✅ Visualization report complete.")
