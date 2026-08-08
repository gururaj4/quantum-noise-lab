# SPECTRE V1 — Quantum Benchmarking & Noise Observatory

SPECTRE is a modular framework for benchmarking quantum circuits under simulated noise.

The goal of V1 is to establish a clean experiment pipeline that can execute a quantum circuit ideally, apply a configurable noise model, run the noisy circuit, and compare the resulting measurement distributions.

---

## V1 Capabilities

SPECTRE V1 currently supports:

* Quantum circuit experiments through a standardized `Experiment` object.
* Ideal circuit execution using Qiskit Aer.
* Configurable Pauli noise.
* Noisy circuit execution.
* Automated collection of ideal and noisy measurement counts.
* Basic success-probability analysis.
* Per-state count-shift analysis.
* Circuit depth and gate-count tracking.
* Basic result summaries.
* Visualization of noisy distributions, count shifts, and ideal-vs-noisy results.

---

## Experiment Pipeline

Each experiment follows the same pipeline:

```text
Experiment
    │
    ▼
Circuit
    │
    ▼
Transpilation
    │
    ├───────────────┐
    ▼               ▼
Ideal Execution    Noise Model
    │               │
    │               ▼
    │          Noisy Circuit
    │               │
    │               ▼
    │          Noisy Execution
    │               │
    └───────┬───────┘
            ▼
      Result Analysis
            │
            ▼
      ExperimentResult
            │
            ▼
       Visualization
```

This separates the experiment definition, execution, noise injection, analysis, and visualization layers so that more sophisticated models can be added later without redesigning the entire framework.

---

# Experiment

An `Experiment` defines the parameters of a benchmark:

```python
Experiment(
    name="Deutsch-Jozsa - Identity - Pauli Noise",
    circuit=qc,
    noise_model=noise,
    shots=1000
)
```

The experiment contains:

* A name
* A quantum circuit
* A noise model
* A number of measurement shots

---

# Pauli Noise Model

V1 uses a configurable Pauli noise model.

The model samples from:

```text
I — Identity
X — Bit flip
Y — Bit + phase flip
Z — Phase flip
```

The probabilities determine how frequently each Pauli operation is introduced into the circuit.

The purpose of this model in V1 is to provide a simple, controllable noise source for validating the benchmarking pipeline.

---

# Experiment Runner

`ExperimentRunner` executes the experiment and produces an `ExperimentResult`.

The runner:

1. Transpiles the circuit for the simulator.
2. Executes the ideal circuit.
3. Applies the noise model.
4. Executes the noisy circuit.
5. Collects measurement counts.
6. Calculates basic performance metrics.
7. Stores the results for visualization.

The result contains:

```text
ExperimentResult
├── ideal_counts
├── noise_counts
├── circuit_depth
├── gate_count
├── success_probability
├── countshift
└── shots
```

---

# Analysis

V1 uses two basic metrics.

### Success Probability

Measures the fraction of noisy measurements that produce an outcome present in the ideal distribution.

```text
success probability =
successful noisy shots / total shots
```

### Count Shift

Measures the change in frequency of each measurement state between the ideal and noisy experiments.

```text
count shift =
(noisy count − ideal count) / total shots × 100
```

For example:

```text
Ideal:
{'0': 1000}

Noisy:
{'0': 964, '1': 36}
```

produces:

```text
Success Probability = 96.4%

Count Shift:
0: -3.6%
1: +3.6%
```

These metrics provide a basic indication of how noise changes the observed output of a quantum circuit.

---

# Visualization

V1 includes three basic visualizations:

### Noisy Distribution

Shows the measured distribution after noise is applied.

### Count Shift

Shows how the frequency of each state changes relative to the ideal result.

### Ideal vs Noisy

Compares the ideal and noisy measurement distributions directly.

---

# Example

A Deutsch-Jozsa circuit can be benchmarked by defining an experiment and passing it to the runner using the file Deutsch_Josza_execution.ipynb:

```python
experiment = Experiment(
    name="Deutsch-Jozsa - Identity - Pauli Noise",
    circuit=qc,
    noise_model=noise,
    shots=1000
)

runner = ExperimentRunner()
result = runner.run(experiment)
```

The resulting `ExperimentResult` can then be summarized and visualized.

---

# V1 Status

SPECTRE V1 establishes the **core benchmarking pipeline**:

```text
Quantum Circuit
      ↓
Experiment
      ↓
Ideal + Noisy Execution
      ↓
Measurement Counts
      ↓
Basic Analysis
      ↓
Visualization
```

V1 intentionally uses a simple Pauli noise model and basic analysis.

The purpose of V1 is to establish a reliable foundation for the next stage of development.

---

# V2 Direction

V2 will focus on making SPECTRE's noise modeling and analysis substantially more realistic and useful.

Planned improvements include:

* More sophisticated noise models.
* Improved fidelity/error analysis.
* More meaningful statistical metrics.
* Systematic noise experiments and parameter sweeps.
* Richer visualizations and comparative analysis.

V2 will build directly on the experiment and benchmarking infrastructure established in V1.

