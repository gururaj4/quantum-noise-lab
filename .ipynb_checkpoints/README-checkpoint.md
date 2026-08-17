# SPECTRE — Quantum Benchmarking & Noise Observatory

SPECTRE is a modular framework for benchmarking quantum algorithms under **hardware-calibrated noise**, built on Qiskit. It runs circuits under ideal and noisy conditions, quantifies how much noise degrades the output distribution, and repeats each experiment to report results with statistical uncertainty rather than a single point estimate.

---

## Status

| Component | Status |
|---|---|
| Experiment / ExperimentResult abstraction | ✅ Done |
| Single-transpile pipeline (ideal + noisy share one circuit) | ✅ Done |
| Hardware-calibrated noise model (per-gate + readout error, from real backend calibration data) | ✅ Done |
| Total Variation Distance (TVD) as primary metric | ✅ Done |
| Repeated-trial statistics (mean, std, coefficient of variation) | ✅ Done |
| Backend sweep (5 IBM fake-provider backends) | ✅ Done |
| Algorithm set: Deutsch-Jozsa, Bernstein-Vazirani, Grover | ✅ Done |
| Comparative visualizations | ✅ Done |
| Simon's algorithm, QFT | 📋 Planned |
| Real IBM hardware validation | 📋 Planned |

---

## Noise Model

SPECTRE's noise model is derived from real IBM backend calibration data (via Qiskit's fake-provider backends: `FakeManilaV2`, `FakeLimaV2`, `FakeJakartaV2`, `FakeGuadalupeV2`, `FakeNairobiV2`), not a hand-picked global error rate.

For each gate in a transpiled circuit:
- **Gate error** is looked up per `(gate name, qubit(s))` from the backend's calibration data and applied as a single-decision Pauli channel (X/Y/Z, evenly split) — one random draw per gate application, so error probability matches the backend's reported rate exactly rather than compounding across multi-qubit gates.
- **Readout error** is applied per qubit, immediately before measurement, as an independent bit-flip check sourced from the backend's per-qubit readout error rate.

This is a first-order approximation (symmetric readout error, no T1/T2 idle decoherence, no crosstalk) — stated explicitly as a limitation, not hidden.

---

## Pipeline

```text
Experiment (circuit, noise_model, shots)
        │
        ▼
  Backend resolution + single transpilation
        │
        ├────────────────┐
        ▼                ▼
  Ideal execution   Noisy execution (noise injected per shot)
        │                │
        └────────┬───────┘
                 ▼
          ExperimentResult
        (ideal_counts, noise_counts, gate_count, shots)
                 │
                 ▼
          ResultAnalysis
        (TVD, count shift, summaries, plots)
                 │
                 ▼
          RepeatedAnalysis
    (N repeated runs → mean, std, CoV)
                 │
                 ▼
       Backend / algorithm sweep
                 │
                 ▼
          Comparative plots
```

Transpilation happens exactly once, before noise injection — the ideal and noisy paths always operate on the identical transpiled circuit, so any difference between them is attributable to injected noise, not structural mismatch.

---

## Metrics

**Total Variation Distance (TVD)**

```text
TVD = 1/2 Σ |P_ideal(x) − P_noisy(x)|
```

The primary distance metric between ideal and noisy output distributions. 0 = identical, 1 = maximally different.

**Repeated-trial statistics**

Since noise is resampled independently per shot, a single run's TVD is one draw from a distribution, not a fixed value. `RepeatedAnalysis` runs an experiment N times and reports:

- Mean TVD
- Standard deviation
- Coefficient of variation (std / mean × 100) — indicates how reliable the mean estimate is relative to its own size

---

## Finding

Sweeping DJ, BV, and Grover across 2–4 qubits and 5 backends, with 30 repeated trials per configuration:

| Algorithm | TVD (2q → 4q) | Growth |
|---|---|---|
| Deutsch-Jozsa | 0.02 → 0.08 | ~4x |
| Bernstein-Vazirani | 0.04 → 0.11 | ~2.8x |
| Grover | 0.06 → 0.85 | ~14x |

Grover's output distribution degrades roughly an order of magnitude faster than DJ/BV as qubit count grows — consistent with its circuit depth scaling with the number of amplification iterations, and its reliance on precise interference between amplitudes, which a single stray gate error disrupts more severely than a shallow, non-interference-based algorithm.

This result also becomes *more* reliably measured as it grows: Grover's coefficient of variation drops from ~39% (2 qubits) to ~4% (4 qubits) — the effect is both large and highly reproducible. Backend-to-backend variation (std ~0.01–0.04 across all 5 backends) is small relative to the algorithm/qubit-count effect, indicating circuit structure — not which specific backend is used — is the dominant driver of noise sensitivity in this sweep.

Confirmed stable across three independent sweep runs at two different trial counts (N=10, N=30).

---

## Example

```python
from experiment import Experiment
from experiment_runner import ExperimentRunner
from analysis import ResultAnalysis
from repeated_analysis import RepeatedAnalysis
from noise_model import HardwareNoiseModel

noise = HardwareNoiseModel(backend=None)  # resolves to a compatible fake backend automatically
experiment = Experiment(
    name="Grover - 4 Qubits",
    circuit=qc,
    noise_model=noise,
    shots=100
)

runner = ExperimentRunner()
result = runner.run(experiment)

analysis = ResultAnalysis(result)
print(analysis.tvd())
analysis.plot_ideal_vs_noisy()

repeated = RepeatedAnalysis(experiment)
stats = repeated.run(30)
print(f"TVD = {stats['tvd_mean']:.3f} ± {stats['tvd_std']:.3f}")
```

---

## Known Limitations

- Readout error is modeled as symmetric (single rate per qubit); real hardware readout error is often asymmetric between |0⟩→|1⟩ and |1⟩→|0⟩ misreads.
- No idle/decoherence (T1/T2) noise — only gate-triggered and readout error are modeled.
- No crosstalk between qubits.
- Simulated only; not yet validated against real IBM hardware execution.

---

## Roadmap

- Add Simon's algorithm and QFT to the sweep.
- Validate the noise model against real IBM Quantum hardware execution, using the same calibration snapshot.
- Extend analysis with a depth/gate-count → TVD regression.