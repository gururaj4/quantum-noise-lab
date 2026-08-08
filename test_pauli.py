from noise.pauli import PauliNoiseModel
import pytest
from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit
def test_initial_conditions():
    pm = PauliNoiseModel(x=0,y=0.5,z=0,i=0.5)
    assert pm.x == 0
    assert pm.y == 0.5
    assert pm.z == 0
    assert pm.i == 0.5

def test_errors():
    with pytest.raises(ValueError):
        pm = PauliNoiseModel(x=1,y=0.1,z=0,i=0)
    with pytest.raises(ValueError):
        pm = PauliNoiseModel(x=-0.1,y=0.1,z=0,i=1.0)

def test_noise_1():
    qc = QuantumCircuit(2,2)
    qc.id(0)
    qc.id(1)
    qc.measure([0,1],[0,1])
    pm1 = PauliNoiseModel(x=0,y=0,z=1.0,i=0)
    qc = pm1.apply_noise(circuit=qc)
    backend= AerSimulator()
    job = backend.run(qc,shots=1000)
    result = job.result()
    counts = result.get_counts()
    for count in counts:
        assert count == '00'


def test_noise_2():
    qc = QuantumCircuit(2,2)
    qc.id(0)
    qc.id(1)
    qc.measure([0,1],[0,1])
    pm1 = PauliNoiseModel(x=1.0,y=0,z=0,i=0)
    qc = pm1.apply_noise(circuit=qc)
    backend= AerSimulator()
    job = backend.run(qc,shots=1000)
    result = job.result()
    counts = result.get_counts()
    for count in counts:
        assert count == '11'
