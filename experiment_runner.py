from experiment import Experiment
from experiment import ExperimentResult
from qiskit_aer import AerSimulator
from qiskit import transpile

class ExperimentRunner:
    def run(self, experiment:Experiment)->ExperimentResult:
        result = ExperimentResult()
        simulator = AerSimulator()
        result.name = experiment.name
        transpiled_circuit = transpile(experiment.circuit,simulator)
        
        idealrun = simulator.run(transpiled_circuit, shots = experiment.shots)
        idealresult = idealrun.result()
        idealcounts = idealresult.get_counts()
        result.ideal_counts = idealcounts

        result.noise_counts = {}
        for i in range(experiment.shots):
            noisycircuit = experiment.noise_model.apply_noise(transpiled_circuit)
            noisyrun = simulator.run(noisycircuit,shots = 1)
            noisyresult = noisyrun.result()
            noisycounts = noisyresult.get_counts()

            for state,count in noisycounts.items():
                result.noise_counts[state] = (result.noise_counts.get(state,0) + count)

        result.circuit_depth = experiment.circuit.depth()
        result.gate_count = experiment.circuit.size()
        
        successful_noiseshots = 0
        countshift = {}
        all_states = result.ideal_counts.keys() | result.noise_counts.keys()
        for state in all_states:
            if state in idealcounts:
                successful_noiseshots += result.noise_counts.get(state,0)
            countdiff = (result.noise_counts.get(state,0) - result.ideal_counts.get(state,0))/experiment.shots
            countdiff = countdiff * 100
            countshift[state] = countdiff
        success_probability = (successful_noiseshots)/experiment.shots
        result.success_probability = success_probability
        result.countshift = countshift
        result.shots = experiment.shots
        return result
