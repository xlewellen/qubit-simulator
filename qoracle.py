import nqubit as nq
import numpy as np 

class QOracle():
    def __init__(self):
        self.state = np.eye(16)
    
    def set_bernvaz(self, code):
        p0 = [[1,0],[0,0]]
        p1 = [[0,0],[0,1]]
        s = nq.binStr(code, 3)
        for i in range(3):
            if s[i] == '1':
                cx = nq.create_double_gate(i, 3, p0, p1, 4)
                self.state = np.matmul(self.state, cx)
    
    def probe_bernvaz(self, nq):
        nq.state = np.matmul(self.state, nq.state)

