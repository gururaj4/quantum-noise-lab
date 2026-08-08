class Experiment:
    def __init__(self, name, circuit, noise_model, shots):
        self.name = name
        self.circuit = circuit
        self.noise_model = noise_model
        self.shots = shots

class ExperimentResult:
    def __init__(self):
        self.name = None
        self.ideal_counts= None
        self.noise_counts = None
        self.circuit_depth = None
        self.gate_count = None
        self.success_probability: float = None
        self.countshift = None
        self.shots = 0
