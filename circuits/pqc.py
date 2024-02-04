from qiskit import QuantumCircuit
from qiskit.circuit.library import RXXGate
from qiskit.quantum_info import Operator
from qiskit.circuit import Parameter
from qiskit import Aer, transpile
from typing import Dict
from copy import deepcopy


class PQC:
    """

    Example:

        pqc = PQC(nodes=[0, 1, 2], edges=[(0, 1), (1, 2)])
        pqc.circuit.draw('mpl')
        pqc.set_parameters([
            0.2, 0.2, 0.2, 3.14, 3.14, 3.14, 3.14, 3.14, 3.14, 0.1, 0.1
        ])
        pqc.statevector

    """

    def __init__(self, nodes, edges, shots=1000):
        self.nodes = nodes
        self.edges = edges
        self.pcircuit, self.parameters = generate_pqc(self.nodes, self.edges)
        self.circuit = deepcopy(self.pcircuit)
        self.shots = 1000

    def get_statevector(self, parameters: Dict):
        """ """
        qc = deepcopy(self.pcircuit)
        qc.assign_parameters(parameters, inplace=True)
        print(qc.parameters)
        sim_statevector = Aer.get_backend("aer_simulator_statevector")
        job_statevector = sim_statevector.run(qc, shots=self.shots)
        qc.save_statevector(label=f"pqc_state")

        result = sim_statevector.run(qc).result()
        data = result.data(0)
        self.circuit = qc
        return data

    def set_parameters(self, params_list):
        """ """
        p = 0
        params = {}
        for node in self.nodes:
            params[self.parameters[f"a_{node}"]] = params_list[p]
            p += 1

        for node in self.nodes:
            params[self.parameters[f"b_{node}"]] = params_list[p]
            p += 1

        for node in self.nodes:
            params[self.parameters[f"c_{node}"]] = params_list[p]
            p += 1

        for edge in self.edges:
            params[self.parameters[f"x_{edge[0]}.{edge[1]}"]] = params_list[p]
            p += 1

        self.statevector = self.get_statevector(params)


def generate_pqc(nodes, edges):
    """
    nodes : [indices]
    edges : [(index_1, index_2)]
    """
    num_qubits = len(nodes)
    pqc = QuantumCircuit(num_qubits)
    params = {}
    for node in nodes:
        params[f"a_{node}"] = Parameter(f"a_{node}")
        params[f"b_{node}"] = Parameter(f"b_{node}")
        params[f"c_{node}"] = Parameter(f"c_{node}")
        pqc.rz(params[f"a_{node}"], qubit=node)
        pqc.rx(params[f"b_{node}"], qubit=node)
        pqc.rz(params[f"c_{node}"], qubit=node)

    for edge in edges:
        params[f"x_{edge[0]}.{edge[1]}"] = Parameter(f"x_{edge[0]}.{edge[1]}")
        pqc.append(RXXGate(theta=params[f"x_{edge[0]}.{edge[1]}"]), edge)
    return pqc, params
