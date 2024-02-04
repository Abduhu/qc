from qiskit import Aer, transpile
import numpy as np


def get_statevector(qc):
    backend = Aer.get_backend('statevector_simulator')
    transpiled = transpile(qc, backend)
    sv = backend.run(transpiled).result().get_statevector()
    return sv


def get_probs(qc):
    sv = np.array(get_statevector(qc))
    return np.round(np.abs(sv)**2, decimals=3)