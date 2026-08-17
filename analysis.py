from experiment_runner import ExperimentRunner
import numpy as np
from experiment import ExperimentResult
import matplotlib.pyplot as plt

class ResultAnalysis:
    def __init__(self,result:ExperimentResult):
        self.result = result
    
    def summarize_results(self)->str:
        lines = []
        lines.append("===== Experiment Summary =====")
        lines.append(f"Experiment Name = {self.result.name}")
        lines.append(f"Backend = {self.result.backend}")
        lines.append(f"Gate Count = {self.result.gate_count}")
        lines.append(f"Shots = {self.result.shots}")
        
        lines.append("Ideal Counts:")
        for state, count in self.result.ideal_counts.items():
            lines.append(f"{state}: {count}")
    
        lines.append("Noisy Counts:")
        for state, count in self.result.noise_counts.items():
            lines.append(f"{state}: {count}")
    
        return "\n".join(lines)
    
    def tvd(self)->float:
        all_states = self.result.ideal_counts.keys() | self.result.noise_counts.keys()
        tvd = 0.0
        for state in all_states:
            ideal_prob = self.result.ideal_counts.get(state, 0) / self.result.shots
            noise_prob = self.result.noise_counts.get(state, 0) / self.result.shots
            tvd += abs(ideal_prob - noise_prob)
        
        tvd = tvd / 2
        return tvd

    def get_countshift(self) -> dict:
        countshift = {}
        all_states = self.result.ideal_counts.keys() | self.result.noise_counts.keys()
    
        for state in all_states:
            countdiff = (
                self.result.noise_counts.get(state, 0)
                - self.result.ideal_counts.get(state, 0)
            ) / self.result.shots
    
            countdiff *= 100
            countshift[state] = countdiff
    
        return countshift

    
    def plot_noisy_distribution(self):
        states = list(self.result.noise_counts.keys())
        counts = list(self.result.noise_counts.values())
        plt.bar(states, counts)
        plt.xlabel("States")
        plt.ylabel("Counts")
        plt.title("Counts plotted per state")
        plt.show()

    def plot_shifts(self):
        states = list(self.get_countshift().keys())
        shifts = list(self.get_countshift().values())
        plt.bar(states, shifts)
        plt.xlabel("States")
        plt.ylabel("Shifts(in %)")
        plt.title("Shifts plotted per state")
        plt.show()

    def plot_ideal_vs_noisy(self):
        states = sorted(self.result.ideal_counts.keys() | self.result.noise_counts.keys())
        x = np.arange(len(states))
        width = 0.4
        ideal = [self.result.ideal_counts.get(state, 0) for state in states]
        noisy = [self.result.noise_counts.get(state, 0) for state in states]
        plt.bar(x - width/2, ideal, width, label="Ideal")
        plt.bar(x + width/2, noisy, width, label="Noisy")
        plt.xticks(x, states)
        plt.xlabel("Measurement State")
        plt.ylabel("Counts")
        plt.title("Ideal vs Noisy Distribution")
        plt.legend()
        plt.show()


    