from experiment import ExperimentResult
import matplotlib.pyplot as plt
def summarize_results(result:ExperimentResult):
    lines=[]
    lines.append("===== Experiment Summary =====")
    lines.append(f"Experiment Name = {result.name}")
    lines.append(f"Circuit Depth = {result.circuit_depth}")
    lines.append(f"Gate Counts = {result.gate_count}")
    lines.append(f"Shots = {result.shots}")
    lines.append(f"Success Probability = {result.success_probability}")
    lines.append(f"Countshift:")
    for state,shift in result.countshift.items():
        lines.append(f"{state}:{shift:.2f}%")
    return "\n".join(lines)

