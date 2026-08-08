from experiment import ExperimentResult
import matplotlib.pyplot as plt
import numpy as np
def plot_noisy_distribution(result:ExperimentResult):
    states = list(result.noise_counts.keys())
    counts = list(result.noise_counts.values())
    plt.bar(states, counts)
    plt.xlabel("States")
    plt.ylabel("Counts")
    plt.title("Counts plotted per state")
    plt.show()

def plot_shifts(result:ExperimentResult):
    states = list(result.countshift.keys())
    shifts = list(result.countshift.values())
    plt.bar(states, shifts)
    plt.xlabel("States")
    plt.ylabel("Shifts(in %)")
    plt.title("Shifts plotted per state")
    plt.show()

import numpy as np
import matplotlib.pyplot as plt

def plot_ideal_vs_noisy(result: ExperimentResult):
    states = sorted(result.ideal_counts.keys() | result.noise_counts.keys())
    x = np.arange(len(states))
    width = 0.4
    ideal = [result.ideal_counts.get(state, 0) for state in states]
    noisy = [result.noise_counts.get(state, 0) for state in states]
    plt.bar(x - width/2, ideal, width, label="Ideal")
    plt.bar(x + width/2, noisy, width, label="Noisy")
    plt.xticks(x, states)
    plt.xlabel("Measurement State")
    plt.ylabel("Counts")
    plt.title("Ideal vs Noisy Distribution")
    plt.legend()
    plt.show()
