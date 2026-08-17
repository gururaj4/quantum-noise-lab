from experiment import Experiment
from experiment import ExperimentResult
from qiskit_aer import AerSimulator


class ExperimentRunner:
    def run(self, experiment: Experiment) -> ExperimentResult:
        result = ExperimentResult()
        simulator = AerSimulator()

        result.name = experiment.name
        result.backend = experiment.backend.name

        # Ideal counts
        idealrun = simulator.run(
            experiment.circuit,
            shots=experiment.shots
        )
        idealresult = idealrun.result()
        idealcounts = idealresult.get_counts()
        result.ideal_counts = idealcounts

        # Noisy counts
        result.noise_counts = {}
        noisy_circuits = []
        for i in range(experiment.shots):
            noisycircuit = experiment.noise_model.apply_noise(experiment.circuit)
            noisy_circuits.append(noisycircuit)
        noisy_job = simulator.run(noisy_circuits,shots=1)
        noisy_result = noisy_job.result()
        for i in range(experiment.shots):
            noisycounts = noisy_result.get_counts(i)
            for state,count in noisycounts.items():
                result.noise_counts[state] = result.noise_counts.get(state,0) + count

        result.gate_count = experiment.circuit.size()
        result.shots = experiment.shots

        return result