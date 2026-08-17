# SPECTRE — Algorithm Noise Sweep Findings

## 1. Objective

This experiment evaluated how three quantum algorithms respond to hardware-calibrated noise as circuit size increases:

- Deutsch-Jozsa (DJ)
- Bernstein-Vazirani (BV)
- Grover

Each algorithm was evaluated at 2, 3, and 4 qubits across five IBM Qiskit fake-provider backends. Each configuration was repeated 30 times, with Total Variation Distance (TVD) used as the primary measure of deviation between the ideal and noisy output distributions.

The five backends were FakeManilaV2, FakeLimaV2, FakeJakartaV2, FakeGuadalupeV2, and FakeNairobiV2.

## 2. Method

The SPECTRE experiment pipeline transpiles the circuit once for the selected backend and then evaluates ideal and noisy execution using the same transpiled circuit. Noise is resampled during noisy execution. This ensures that the measured difference between ideal and noisy distributions is attributable to the injected noise model rather than a different circuit structure.

The noise model uses backend calibration data for gate-specific error rates and per-qubit readout error rates. Gate errors are represented using a Pauli approximation, while readout error is represented as a symmetric bit-flip check immediately before measurement.

For each configuration, repeated analysis reports the mean TVD, standard deviation, and coefficient of variation. TVD is defined as:

```text
TVD = 1/2 * sum_x |P_ideal(x) - P_noisy(x)|
```

A TVD of 0 means the two distributions are identical, while 1 represents maximal difference.

## 3. Main Results

The sweep produced a clear separation between the three algorithms.

| Algorithm | TVD at 2 qubits | TVD at 4 qubits | Approx. growth |
|---|---:|---:|---:|
| Deutsch-Jozsa | 0.02 | 0.08 | ~4x |
| Bernstein-Vazirani | 0.04 | 0.11 | ~2.8x |
| Grover | 0.06 | 0.85 | ~14x |

The exact sweep values vary slightly between repeated runs, but the ordering and overall trend are stable: DJ is the least noise-sensitive, BV is intermediate, and Grover is substantially more sensitive.

## 4. Deutsch-Jozsa

Deutsch-Jozsa showed the strongest robustness in the sweep. TVD remained low across the tested qubit counts, increasing gradually from approximately 0.02 at 2 qubits to approximately 0.08 at 4 qubits.

This indicates that the output distribution remains relatively close to the ideal distribution even as the circuit grows within the tested range.

## 5. Bernstein-Vazirani

Bernstein-Vazirani showed moderate noise sensitivity. TVD increased from approximately 0.04 at 2 qubits to approximately 0.11 at 4 qubits.

The increase is larger than for Deutsch-Jozsa, but still substantially smaller than the degradation observed for Grover.

## 6. Grover

Grover was the clear outlier.

TVD increased from approximately 0.06 at 2 qubits to approximately 0.85 at 4 qubits. A TVD near 0.85 means that the noisy output distribution is dramatically different from the ideal distribution.

The coefficient-of-variation analysis also supports the significance of this result. For Grover, the coefficient of variation decreased from approximately 39% at 2 qubits to approximately 4% at 4 qubits. The larger observed effect is therefore not simply caused by an increasingly unstable estimator; the measured degradation becomes more reproducible as the effect grows.

## 7. Backend-to-Backend Variation

The backend sweep showed that Grover's degradation is not isolated to a single fake backend.

Across the five tested backends, backend-to-backend standard deviations were approximately 0.01–0.04, which is small compared with the change in TVD caused by increasing the algorithm's qubit count.

This suggests that, within this experiment, algorithm and circuit structure are stronger drivers of the observed noise sensitivity than the choice among the five simulated backend calibration profiles.

This should be interpreted as an experimental observation rather than a universal statement about IBM hardware.

## 8. Why Grover Is More Sensitive

The observed behavior is consistent with the structure of Grover's algorithm.

Grover repeatedly applies an oracle and a diffuser to amplify the amplitude of the marked state. The algorithm therefore depends heavily on maintaining precise relative amplitudes and phases throughout repeated interference operations.

As the number of qubits increases, the search space grows exponentially and the circuit requires additional amplification structure. Errors introduced during these operations can alter amplitudes or phases and therefore change the final interference pattern.

By contrast, the DJ and BV circuits used in this sweep remain comparatively shallow and do not rely on the same repeated amplitude-amplification process.

The sweep therefore supports the interpretation that Grover's greater sensitivity is related to its circuit structure and interference requirements.

## 9. Important Interpretation

The results do **not** demonstrate that Grover is universally 14 times more sensitive to noise than Deutsch-Jozsa or Bernstein-Vazirani on physical IBM hardware.

The experiment uses:

- Qiskit's fake-provider backend calibration data
- A first-order Pauli approximation for gate errors
- Symmetric readout-error modeling
- No T1/T2 idle decoherence
- No crosstalk
- No real hardware execution

Therefore, the findings should be understood as a controlled simulation study of algorithmic sensitivity under the implemented hardware-calibrated noise model.

## 10. Conclusion

The sweep demonstrates a strong algorithm-dependent difference in noise sensitivity.

Deutsch-Jozsa remained comparatively robust, Bernstein-Vazirani showed moderate degradation, and Grover experienced a dramatic increase in TVD as the number of qubits increased.

The most significant observation is the separation between the algorithm/qubit-count effect and backend-to-backend variation. The five backend profiles produced relatively small variation compared with the large increase in Grover's TVD.

This makes Grover the most useful case study for the next stage of SPECTRE: rather than simply measuring that noise exists, the framework can now be used to investigate which circuit properties are responsible for the observed degradation.

## 11. Next Steps

The natural extensions of this experiment are:

1. Add Simon's algorithm and QFT to the sweep.
2. Compare TVD against circuit depth and gate count.
3. Separate the contributions of gate errors and readout errors.
4. Investigate Grover iteration count as an experimental variable.
5. Extend the noise model with T1/T2 relaxation and other realistic effects.
6. Validate the simulated results against real IBM hardware using a comparable calibration snapshot.

The current sweep establishes the baseline result: **algorithm structure matters substantially when quantum circuits operate under realistic, hardware-derived noise.**
