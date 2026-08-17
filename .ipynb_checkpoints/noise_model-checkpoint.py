from qiskit import QuantumCircuit,transpile
import random
from qiskit_ibm_runtime.fake_provider import (
    FakeManilaV2,
    FakeLimaV2,
    FakeJakartaV2,
    FakeGuadalupeV2,
    FakeNairobiV2,
)
backends = [
    FakeManilaV2(),
    FakeLimaV2(),
    FakeJakartaV2(),
    FakeGuadalupeV2(),
    FakeNairobiV2(),
]
class HardwareNoiseModel():
    def __init__(self,backend):
        self.backend = backend
    
    
    def _gate_noise(self,qc:QuantumCircuit,qubits,rate):
        xrate = rate/3
        zrate = 2 * rate / 3
        yrate = rate
        for qubit in qubits:
            num = random.random()
            if num < xrate:
                qc.x(qubit)
            elif num < zrate: 
                qc.z(qubit)
            elif num < yrate:
                qc.y(qubit)
            else:
                pass
        
        
    def apply_noise(self, circuit: QuantumCircuit) -> QuantumCircuit:
        if self.backend is None:
            compatible_backends = [
                end for end in backends
                if end.num_qubits >= circuit.num_qubits
            ]
            if not compatible_backends:
                raise ValueError("Circuit has more qubits than all available noise models")
            self.backend = random.choice(compatible_backends)
        elif self.backend.num_qubits < circuit.num_qubits:
            raise ValueError("Selected backend has fewer qubits than the circuit")

        properties = self.backend.properties()
        error_dict = {}
    
        for gate in properties.gates:
            for parameter in gate.parameters:
                if parameter.name == "gate_error":
                    key = (gate.gate, tuple(gate.qubits))
                    error_dict[key] = parameter.value
        readout_error = {}
        for qubit in range(self.backend.num_qubits):
            readout_error[qubit] = properties.readout_error(qubit)
        qc = circuit.copy_empty_like()
        
        for instruction in circuit.data:
            qubits = tuple(circuit.find_bit(q).index for q in instruction.qubits)
            if instruction.operation.name == "measure":
                for qubit in qubits:
                    if random.random() < readout_error.get(qubit, 0):
                        qc.x(qubit)
                qc.append(instruction)
            else:
                qc.append(instruction)
                key = (instruction.operation.name, qubits)
                error_rate = error_dict.get(key, 0)
                self._gate_noise(qc, qubits, error_rate)
        return qc