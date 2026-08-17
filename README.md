# Quantum Noise Lab V2

Quantum Noise Lab (QNL) is a modular framework for benchmarking quantum algorithms under simulated hardware-derived noise.

QNL V2 extends the original Pauli-noise framework by using calibration data from Qiskit's fake backends to construct algorithm-specific noise experiments and statistically analyze how different quantum algorithms respond to realistic hardware error rates.

---

## V2 Goals

QNL V2 focuses on:

* Hardware-derived gate error rates
* Readout error modeling
* Backend-specific noise
* Repeated statistical analysis
* Total Variation Distance (TVD)
* Algorithm comparisons
* Qubit-count sweeps
* Backend consistency experiments
* Visualization of noise sensitivity

The primary algorithms benchmarked are:

* Deutsch-Jozsa
* Bernstein-Vazirani
* Grover's Algorithm

---

# Experiment Pipeline

Each experiment follows the same general pipeline:

```text
Quantum Algorithm
       ↓
Generated Circuit
       ↓
Backend Selection
       ↓
Transpilation / ISA Circuit
       ↓
Backend Calibration Data
       ↓
Gate + Readout Noise
       ↓
Ideal Execution
       +
Noisy Execution
       ↓
Measurement Counts
       ↓
Repeated Analysis
       ↓
TVD / Statistical Metrics
       ↓
Sweep Results
       ↓
Visualization
```

This separates algorithm generation from noise modeling and analysis.

---

# Experiment

The `Experiment` class defines the parameters of a benchmark.

```python
Experiment(
    name="DJ Noise Sweep",
    circuit=qc,
    noise_model=noise,
    shots=100
)
```

An experiment contains:

* Experiment name
* Quantum circuit
* Noise model
* Number of shots
* Selected backend

The experiment can automatically select a compatible backend when one is not explicitly provided.

---

# Hardware Noise Model

QNL V2 uses the `HardwareNoiseModel` class.

The model receives a Qiskit backend:

```python
HardwareNoiseModel(backend)
```

The backend provides calibration information used to construct the simulated noise.

QNL V2 currently extracts:

* Gate error probabilities
* Readout error probabilities
* Gate names
* Gate qubit locations
* Backend qubit count

---

# Gate Noise

Gate-specific error rates are extracted from backend properties.

The noise model associates errors with:

```text
Gate
+
Physical Qubit(s)
```

For example:

```text
CX on qubits (0, 1)
```

can have a different error rate from:

```text
CX on qubits (1, 2)
```

This allows QNL V2 to preserve backend-specific variation instead of applying one global error probability to every gate.

The current Pauli approximation distributes the gate error rate across:

```text
X
Y
Z
```

to provide a simple controllable approximation of hardware error.

---

# Readout Noise

QNL V2 also extracts readout error probabilities from the selected backend.

Readout noise is applied during measurement to model the possibility of an incorrect classical result.

This is important because an algorithm can have a correct quantum state but still produce an incorrect measured bitstring because of measurement error.

---

# Backend Selection

QNL V2 supports multiple Qiskit fake backends.

Example backends used in the benchmarking experiments include:

```python
FakeManilaV2()
FakeLimaV2()
FakeJakartaV2()
FakeGuadalupeV2()
FakeNairobiV2()
```

These backends differ in:

* Number of qubits
* Connectivity
* Native instructions
* Gate error rates
* Readout error rates
* Hardware calibration characteristics

Consequently, the same algorithm can experience different noise depending on the selected backend.

---

# Experiment Runner

`ExperimentRunner` executes both ideal and noisy versions of an experiment.

The ideal circuit is executed normally:

```text
Circuit
  ↓
Ideal Aer simulation
  ↓
Ideal counts
```

For the noisy execution, QNL generates noisy circuit instances and executes them through Aer.

```text
Circuit
  ↓
HardwareNoiseModel
  ↓
Noisy circuit instances
  ↓
Aer simulation
  ↓
Noise counts
```

The resulting `ExperimentResult` stores:

```text
ideal_counts
noise_counts
backend
name
gate_count
shots
```

---

# Repeated Analysis

Quantum measurements are probabilistic, so a single noisy experiment is not sufficient to characterize an algorithm.

QNL V2 therefore includes `RepeatedAnalysis`.

```python
analysis = RepeatedAnalysis(experiment)

mean_tvd = analysis.run(30)
```

The analysis repeatedly executes the experiment and calculates the TVD for each run.

The resulting values are stored and averaged:

```text
Experiment
    ↓
Run
    ↓
TVD
    ↓
Run again
    ↓
TVD
    ↓
...
    ↓
Mean TVD
```

This reduces the effect of random sampling variation and provides a more stable estimate of noise sensitivity.

---

# Total Variation Distance

QNL V2 uses Total Variation Distance to compare ideal and noisy measurement distributions.

For two probability distributions:

```text
TVD(P,Q) = 1/2 Σ |P(x) - Q(x)|
```

Interpretation:

```text
TVD = 0
```

means the distributions are identical.

A larger TVD means the noisy distribution has moved farther from the ideal distribution.

Therefore:

```text
Lower TVD → More robust

Higher TVD → More sensitive to noise
```

---

# Algorithm Sweep

QNL V2 performs sweeps across:

* Algorithm
* Number of qubits
* Target bitstring where applicable
* Backend
* Repeated executions

Example structure:

```text
Algorithm
   ↓
Qubit count
   ↓
Generate circuit
   ↓
Select backend
   ↓
Run repeated analysis
   ↓
Store result
```

The results are collected into Pandas DataFrames for further analysis.

Example columns include:

```text
Algorithm
Qubits
Bitstring
Mean TVD
Ideal Counts
Noise Counts
Backend
```

---

# Deutsch-Jozsa Results

Deutsch-Jozsa showed relatively low and steadily increasing noise sensitivity as the number of qubits increased.

Representative results from the sweep:

```text
Qubits    Mean TVD

2         0.028
3         0.041
4         0.052
```

The increase is comparatively gradual.

This is consistent with the relatively shallow structure of the Deutsch-Jozsa circuit.

The algorithm generally requires:

```text
Hadamards
+
Oracle
+
Hadamards
+
Measurement
```

with relatively little repeated amplification.

---

# Bernstein-Vazirani Results

Bernstein-Vazirani also showed a gradual increase in TVD with circuit size.

Representative results:

```text
Qubits    Mean TVD

2         0.041
3         0.069
4         0.103
```

The noise sensitivity is somewhat higher than Deutsch-Jozsa at corresponding sizes.

This is consistent with BV's oracle structure and the increasing number of operations required to encode the hidden bitstring.

However, the increase remains relatively controlled.

---

# Grover Results

Grover's Algorithm behaved very differently.

Representative results:

```text
Qubits    Mean TVD

2         0.083
3         0.376
4         0.835
```

The increase is dramatically steeper than for Deutsch-Jozsa or Bernstein-Vazirani.

At four qubits, the noisy distribution can become extremely different from the ideal distribution.

This is the central finding of the QNL V2 sweep.

---

# Why Grover Is Much More Sensitive

Grover does not simply construct a state and measure it.

It repeatedly performs:

```text
Oracle
   ↓
Diffuser
   ↓
Oracle
   ↓
Diffuser
   ↓
...
```

The purpose of these iterations is to amplify the amplitude of the marked state.

This creates an important property:

> Grover's algorithm repeatedly manipulates amplitudes that must remain precisely controlled for amplification to work.

Noise therefore affects the algorithm at multiple stages.

A gate error can:

1. Modify an amplitude.
2. Change the interference pattern.
3. Affect the next oracle/diffuser operation.
4. Become amplified or redistributed by later iterations.
5. Ultimately change the measured probability distribution.

This is fundamentally different from a shallow algorithm where an error may only perturb the final distribution once.

---

# Ideal Grover Distribution

The ideal Grover distribution is itself not necessarily a single deterministic bitstring for every circuit size and iteration count.

For example, with a small search space and an appropriate iteration count, the marked state should dominate the distribution.

However, the remaining states can still have nonzero probability depending on the number of iterations.

This is why QNL compares the **full ideal probability distribution** against the noisy distribution rather than simply checking whether the most common bitstring is correct.

---

# Grover Iteration Sensitivity

The sweep also showed that Grover's performance depends strongly on the number of amplification iterations.

Increasing iterations does not necessarily improve performance under noise.

In an ideal circuit:

```text
More appropriate iterations
        ↓
Higher marked-state probability
```

Under noise:

```text
More iterations
        ↓
More gates
        ↓
More opportunities for error
        ↓
Greater accumulated noise
```

Therefore, the iteration count becomes an important tradeoff between:

```text
Amplitude amplification
```

and

```text
Noise accumulation
```

This explains why simply increasing the number of Grover iterations is not a valid strategy for noisy hardware.

---

# Backend Sweep

QNL V2 also evaluates the algorithms across multiple fake backends.

This allows the experiment to distinguish:

```text
Algorithm sensitivity
```

from:

```text
Backend-specific hardware sensitivity
```

Different backends provide different calibration data.

Consequently, two executions of the same circuit can produce different noisy distributions.

The backend sweep records these differences for later comparison.

---

# Backend Consistency

The backend consistency experiments investigate whether the same algorithm exhibits similar noise behavior across different hardware models.

The purpose is not to expect identical results.

Instead, the experiment asks:

```text
Does the overall noise trend remain?

Does TVD increase with circuit size?

Does Grover remain substantially more sensitive?

How much variation comes from the backend?
```

This provides a more meaningful interpretation of the algorithm-level results.

---

# Visualizations

QNL V2 includes several visualization notebooks and generated figures.

Current visualizations include:

```text
tvd_vs_qubits.png
```

Shows how TVD changes as the number of qubits increases.

```text
tvd_by_backend_per_algorithm.png
```

Compares algorithm noise sensitivity across different backends.

```text
backend_consistency.png
```

Shows variation across backend experiments.

```text
cov_vs_qubits.png
```

Examines statistical variation as circuit size increases.

The sweep notebooks also generate CSV datasets for reproducibility and further analysis.

---

# Generated Data

The project stores sweep results such as:

```text
backend_sweep.csv
generalsweep.csv
```

These datasets allow the visualizations and analysis to be reproduced without rerunning every experiment.

---

# Key Findings

The QNL V2 experiments demonstrate three distinct noise-sensitivity regimes:

```text
Deutsch-Jozsa
      ↓
Low / gradual TVD increase


Bernstein-Vazirani
      ↓
Moderate / gradual TVD increase


Grover
      ↓
Rapid TVD increase
```

The important observation is not simply that Grover has a larger TVD.

It is that its TVD increases **much more rapidly with circuit size**.

This provides experimental evidence that algorithms requiring repeated amplitude amplification are substantially more vulnerable to accumulated gate and readout noise.

---

# Interpretation

The results suggest that circuit depth and repeated interference operations are important contributors to noise sensitivity.

A simplified conceptual relationship is:

```text
Circuit complexity
       +
Number of noisy operations
       +
Repeated interference
       ↓
Accumulated error
       ↓
Distribution distortion
       ↓
Higher TVD
```

Grover provides a particularly clear demonstration of this effect because its algorithmic advantage depends directly on repeated coherent operations.

---

# Limitations

QNL V2 intentionally uses a simplified noise model.

The current model does not attempt to reproduce every physical noise process occurring on real quantum hardware.

In particular:

* Pauli noise is an approximation.
* Gate errors are mapped into a simplified X/Y/Z error model.
* Readout error is represented using a simplified measurement-error mechanism.
* Fake backend calibration data represents backend characteristics but is not equivalent to running directly on physical hardware.
* The number of repetitions and shots affects statistical uncertainty.
* Small circuits can show substantial run-to-run variation.

Therefore, the results should be interpreted as **hardware-informed simulation experiments**, not direct measurements of physical quantum processors.

---

# Project Structure

```text
quantum-noise-lab/
│
├── experiment.py
├── experiment_runner.py
├── noise_model.py
├── analysis.py
├── repeated_analysis.py
│
├── Sweeps.ipynb
├── Plots.ipynb
│
├── backend_sweep.csv
├── generalsweep.csv
│
├── backend_consistency.png
├── cov_vs_qubits.png
├── tvd_by_backend_per_algorithm.png
├── tvd_vs_qubits.png
│
└── reports/
```

---

# Relationship With Quantum Algorithms Toolkit

QNL is designed as the benchmarking layer for the Quantum Algorithms Toolkit.

```text
Quantum Algorithms Toolkit
            ↓
    Generate Algorithms
            ↓
     Quantum Circuits
            ↓
     Quantum Noise Lab
            ↓
 Hardware-Derived Noise
            ↓
 Ideal vs Noisy Results
            ↓
       Statistical Analysis
```

This separation allows algorithm implementations to remain independent of the benchmarking infrastructure.

---

# V2 Status

**Quantum Noise Lab V2 — Complete**

Implemented:

* Hardware-derived noise model
* Fake-backend calibration extraction
* Gate-specific error rates
* Readout error modeling
* Ideal execution
* Noisy execution
* Repeated analysis
* Total Variation Distance
* Algorithm sweeps
* Qubit-count sweeps
* Backend sweeps
* Backend consistency analysis
* CSV result generation
* Automated plotting
* Comparative algorithm analysis
* Grover noise investigation

The main V2 finding is that **Grover's Algorithm exhibits dramatically greater noise sensitivity than Deutsch-Jozsa and Bernstein-Vazirani as circuit size increases**, primarily because repeated oracle and diffuser operations create substantially more opportunities for hardware-derived errors to accumulate and distort the amplitude-amplification process.

---

# Future Work

Potential future improvements include:

* More realistic noise channels
* Gate-dependent error channels beyond Pauli approximations
* Correlated noise
* T1/T2-based decoherence
* More detailed readout-error matrices
* Larger backend sweeps
* Confidence intervals
* Statistical significance testing
* Error-mitigation experiments
* Circuit-depth normalization
* Additional quantum algorithms
* Direct hardware execution

QNL V2 provides the foundation for investigating these effects in future versions.
