from qiskit import transpile
from qiskit import QuantumCircuit
import random


class Experiment:
    def __init__(self, name, circuit, noise_model, shots):
        self.name = name
        self.noise_model = noise_model
        self.shots = shots
        backend = noise_model.backend
        self.backend = backend
        self.noise_model.backend = backend
        self.circuit = transpile(circuit, backend)


class ExperimentResult:
    def __init__(self):
        self.name = None
        self.backend = None
        self.ideal_counts = None
        self.noise_counts = None
        self.gate_count = None
        self.shots = 0