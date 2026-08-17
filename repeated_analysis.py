from experiment_runner import ExperimentRunner
from analysis import ResultAnalysis
from experiment import Experiment
import statistics

class RepeatedAnalysis:
    def __init__(self, experiment: Experiment):
        self.experiment = experiment
        self.tvds = []

    def run(self, runs: int) -> dict:
        if runs < 2:
            raise ValueError("analysis needs atleast 2 instances for valid results")

        self.tvds = []  # reset in case run() is called more than once on this instance
        runner = ExperimentRunner()
        for i in range(runs):
            result = runner.run(self.experiment)
            analyser = ResultAnalysis(result)
            self.tvds.append(analyser.tvd())

        tvdmean = statistics.mean(self.tvds)
        tvdstd = statistics.stdev(self.tvds)

        return {
            "tvd_mean": tvdmean,
            "tvd_std": tvdstd,
            "runs": runs,
        }