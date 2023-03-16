import numpy as np
import nqubit as nq

class QCircuit:
    @staticmethod
    def same_entangle(qa, i, j):
        qa.apply_hadamard_gate(i)
        qa.apply_cnot_gate(i,j)
    
    @staticmethod
    def bernvaz(qa, qo):
        qa.apply_hadamard_gate()
        qo.probe_bernvaz(qa)
        qa.apply_hadamard_gate()

    @staticmethod
    def archimedes(qa, qo):
        qa.apply_hadamard_gate()
        qo.probe_archimedes(qa)
        qa.apply_hadamard_gate(0)
        qa.apply_hadamard_gate(1)
        qa.apply_hadamard_gate(2)
        
    

    
