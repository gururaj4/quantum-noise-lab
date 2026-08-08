from qiskit import QuantumCircuit
import random

class PauliChannel():
    def __init__(self,x:float,y:float,z:float,i:float):
        if abs((x + y + z + i) - 1.0) > 1e-6:
            raise ValueError("Sum of all probabilities has to add up to 1")
        if x < 0 or z < 0 or y < 0 or i < 0:
            raise ValueError("Probabilities always have to be greater than or equal to 0")
        self.x = x
        self.y = y
        self.z = z
        self.i = i 


    def _random_noise(self,qc:QuantumCircuit,qubit):
        num = random.random()
        if num <= self.x:
            qc.x(qubit)
        elif num <= self.x + self.z:
            qc.z(qubit)
        elif num <= self.x + self.y + self.z:
            qc.y(qubit)
        
    def apply_noise(self,circuit:QuantumCircuit)->QuantumCircuit:
        qc = QuantumCircuit(circuit.num_qubits,circuit.num_clbits)
        for instruction in circuit.data:
            qc.append(instruction)
            if instruction.operation.name != 'measure':
                for qubit in instruction.qubits:
                    self._random_noise(qc,qubit)
        return qc
        
            
            
            
    
