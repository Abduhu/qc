from qiskit import QuantumCircuit
from qiskit.circuit.library import GraphState
from qiskit_aer import AerSimulator, StatevectorSimulator, Aer, QasmSimulator
from networkx import gnm_random_graph
from itertools import combinations


def graph_operation(circuit, edges):
    """
    """
    for qubit in circuit.qubits:
        # create |+> states
        circuit.h(qubit=qubit)
    
    for edge in edges:
        circuit.cz(edge[0], edge[1])


def create_graph_state(num_qubits, edges):
    """
    """
    qc = QuantumCircuit(num_qubits)
    graph_operation(qc, edges)
    
    return qc


def create_qiskit_graph_state(adjency_matrix):
    qc = QuantumCircuit(2)
    qc.compose(GraphState(adjency_matrix), inplace=True)
    
    return qc


def create_random_graph_state(n_qubits, n_edges, seed=None):
    """
    # Params
    n_qubits = 3
    n_edges = 3
    seed = None

    graph_state = gen_graph_circ(n_qubits, n_edges, seed)
    test_state = gen_graph_circ(3, 1, None)

    meas_circ = build_meas_circ(state=graph_state, test=test_state)
    """
    # Graph generation
    graph = gnm_random_graph(n_qubits, n_edges, seed)

    # Graph state construction
    graph_state = QuantumCircuit(n_qubits)

    for q in range(n_qubits):
        graph_state.h(q)
    for i, j in graph.edges():
        graph_state.cz(i, j)
        
    return graph_state


def build_meas_circ(state, test):
    if test.num_qubits < state.num_qubits:
        meas_circ = state
        meas_circ.barrier()
        meas_circ = meas_circ.compose(test.inverse())
    else:
        meas_circ = test
        meas_circ.barrier()
        meas_circ = meas_circ.compose(state.inverse()).inverse()
    
    meas_circ.measure_all()
    
    return meas_circ
