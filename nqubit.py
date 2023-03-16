import parent_qubit as pq
import math
import numpy as np 
import random

def binInt(s):
    return int(s, 2)

def binStr(i, numqubit):
    formatstr = '0' + str(numqubit) + 'b'
    return format(i, formatstr)

def create_double_gate(i, j, p0, p1, size):
    eye = [[1,0],[0,1]]
    x = [[0,1],[1,0]]
    dif = abs(j - i)
    if j > i:
        for _ in range(1,dif):
            p0 = np.kron(p0, eye)
            p1 = np.kron(p1, eye)
        p0 = np.kron(p0, eye)
        p1 = np.kron(p1, x)
    else:
        for _ in range(1,dif):
            p0 = np.kron(eye, p0)
            p1 = np.kron(eye, p1)
        p0 = np.kron(eye, p0)
        p1 = np.kron(x, p1)
    cx = p0 + p1
    for _ in range(min(i,j)):
        cx = np.kron(eye, cx)
    for _ in range(max(i,j), size - 1):
        cx = np.kron(cx, eye)
    return cx

class NQubit(pq.ParentQubit):
    def __init__(self, numqubits):
        self.numqubits = numqubits
        self.state = [0]*(2**numqubits)
        self.state[0] = 1

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
        merge = NQubit(self.numqubits + pq.numqubits)
        merge.state = np.kron(self.state, pq.state)
        return merge

    def to_bra_ket(self):
        num = self.numqubits
        out = str(abs(self.state[0])) + "|" + binStr(0, num) + ">"
        for i in range(1, len(self.state)):
            if self.get_phase(i) == 1:
                out += " + "
            else:
                out += " - "
            out += str(abs(self.state[i])) + "|" + binStr(i, num) + ">"
        return out

    def __apply_single_gate(self, gate, i=None):
        eye = [[1,0],[0,1]]
        mat = gate
        if i == None:
            for j in range(1, self.numqubits):
                mat = np.kron(mat, gate)
        else:
            if i != 0:
                mat = eye
            for j in range(1, self.numqubits):
                if i == j:
                    mat = np.kron(mat, gate)
                else:
                    mat = np.kron(mat, eye)
        self.state = np.matmul(mat, self.state)

    def apply_not_gate(self, i=None):
        x = [[0,1],[1,0]]
        self.__apply_single_gate(x, i)


    def apply_hadamard_gate(self, i=None):
        half = 1/math.sqrt(2)
        h = [[half,half],[half,half * -1]]
        self.__apply_single_gate(h, i)
    
    def apply_z_gate(self, i=None):
        z = [[1,0],[0,-1]]
        self.__apply_single_gate(z, i)


    def apply_cnot_gate(self, i,j):
        p0 = [[1,0],[0,0]]
        p1 = [[0,0],[0,1]]
        cx = create_double_gate(i, j, p0, p1, self.numqubits)
        self.state = np.matmul(cx, self.state)

    def __swap(self, s, i, j):
        new = ""
        for k in range(len(s)):
            if k == j:
                new += s[i]
            elif k == i:
                new += s[j]
            else:
                new += s[k]
        return new


    def apply_swap_gate(self, i,j):
        sol = []
        size = len(self.state)
        num = self.numqubits
        for k in range(size):
            row = [0]*size
            binstr = binStr(k, num)
            if binstr[i] == binstr[j]:
                row[k] = 1
            else:
                newstr = self.__swap(binstr, i, j)
                row[binInt(newstr)] = 1
            sol.append(row)
        self.state = np.matmul(sol, self.state)
    
    def measure(self):
        sol = [0]*len(self.state)
        cmp = random.random()
        sum = 0
        for i in range(len(self.state)):
            self.state[i] = math.pow(abs(self.state[i]), 2)
            if (cmp <= sum + self.state[i]):
                sol[i] = 1
                self.state = sol
                return i
            sum += self.state[i]
        return 0