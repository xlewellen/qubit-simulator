import parent_qubit as pq
import nqubit as nq
import math
import numpy as np 
import random

class SingleQubit(pq.ParentQubit):
    def __init__(self):
        self.numqubits = 1
        self.state = [1.0, 0.0]

    def set_value(self, v, i):
        self.state[i] = v
    
    def set_values(self, v):
        self.state = v
    
    def get_value(self, i):
        x = self.state[i]
        if (abs(x) < 0.0000000001):
            return 0
        return x
    
    def get_values(self):
        val = []
        for i in range(len(self.state)):
            val.append(self.get_value(i))
        return val

    def set_phase(self, p, i):
        if p >= 0:
            self.state[i] = abs(self.state[i])
        else:
            self.state[i] = abs(self.state[i]) * (-1)
    
    def set_phases(self, p):
        for i in range(len(self.state)):
            self.set_phase(p[i], i)

    def get_phase(self, i):
        if self.state[i] >= 0:
            return 1
        else:
            return -1

    def get_num_qubits(self):
        return self.numqubits
    
    def merge_qubits(self, pq):
        merge = nq.NQubit(self.numqubits + pq.numqubits)
        merge.state = np.kron(self.state, pq.state)
        return merge

    def to_bra_ket(self):
        out = str(self.state[0]) + "|0> + " + str(self.state[1]) + "|1>"
        return out

    def apply_not_gate(self, i=None):
        x = [[0,1],[1,0]]
        self.state = np.matmul(x, self.state)

    def apply_hadamard_gate(self, i=None):
        half = 1/math.sqrt(2)
        h = [[half,half],[half,half * -1]]
        self.state = np.matmul(h, self.state)
    
    def apply_z_gate(self, i=None):
        z = [[1,0],[0,-1]]
        self.state = np.matmul(z, self.state)

    def apply_cnot_gate(i,j):
        return
    
    def apply_swap_gate(i,j):
        return
    
    def measure(self):
        per = math.pow(abs(self.state[0]), 2)
        cmp = random.random()
        if (cmp <= per):
            self.set_values([1.0, 0.0])
            return 0
        else:
            self.set_values([0.0, 1.0])
            return 1
