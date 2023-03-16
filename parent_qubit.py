from abc import ABC, abstractmethod
    

class ParentQubit(ABC):
    def __init__(self, numqubits):
        self.numquibits = numqubits

    @abstractmethod
    def set_value(v,i):
        pass

    @abstractmethod
    def set_values(v):
        pass

    @abstractmethod
    def get_value(i):
        pass

    @abstractmethod
    def get_values():
        pass

    @abstractmethod
    def set_phase(p,i):
        pass

    @abstractmethod
    def set_phases(p):
        pass

    @abstractmethod
    def get_phase(i):
        pass

    @abstractmethod
    def get_num_qubits():
        pass

    @abstractmethod
    def merge_qubits(pq):
        pass

    @abstractmethod
    def to_bra_ket():
        pass

    @abstractmethod
    def apply_not_gate(i=None):
        pass

    @abstractmethod
    def apply_hadamard_gate(i=None):
        pass

    @abstractmethod
    def apply_z_gate(i=None):
        pass

    @abstractmethod
    def apply_cnot_gate(i,j):
        pass

    @abstractmethod
    def apply_swap_gate(i,j):
        pass

    @abstractmethod
    def measure():
        pass