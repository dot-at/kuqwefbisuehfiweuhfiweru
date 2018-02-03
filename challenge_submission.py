# -*- coding: utf-8 -*-

#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================

"""
---------------> please fill out this section <---------------

Your Name :

Your E-Mail :

Description of the algorithm :

- How does the algorithm work?
- Did you use any previously published schemes? Cite relevant papers.
- What packages did you use in your code and for what part of the algorithm?
- How general is your approach? Does it work for arbitrary coupling layouts (qubit number)?
- Are there known situations when the algorithm fails?


---------------> please fill out this section <---------------
"""

# Include any Python modules needed for your implementation here

# The following class is the input and output circuit representation for a
# QISKit compiler
from qiskit.dagcircuit import DAGCircuit


def compiler_function(dag_circuit, coupling_map=None, gate_costs='default'):
    """
    Modify a DAGCircuit based on a gate cost function.

    Instructions:
        Your submission involves filling in the implementation
        of this function. The function takes as input a DAGCircuit
        object, which can be generated from a QASM file by using the
        function 'qasm_to_dag_circuit' from the included 
        'submission_evaluation.py' module. For more information
        on the DAGCircuit object see the or QISKit documentation
        (eg. 'help(DAGCircuit)').

    Args:
        dag_circuit (DAGCircuit): DAGCircuit object to be compiled.
        coupling_circuit (list): Coupling map for device topology.
                                 A coupling map of None corresponds an
                                 all-to-all connected topology.
        gate_costs (dict) : dictionary of gate names and costs.

    Returns:
        A modified DAGCircuit object that satisfies an input coupling_map
        and has as low a gate_cost as possible.
    """

    if gate_costs == 'default':
        # Default gate costs used for evaluation of submission
        gate_costs = {'id': 0, 'u1': 0,
                      'u2': 1, 'u3': 1, 'U': 1,
                      'cx': 10, 'CX': 10}
    #####################
    # Put your code here
    #####################
    # Example using mapper passes in Qiskit
    import copy
    from qiskit.mapper import swap_mapper, direction_mapper, cx_cancellation, optimize_1q_gates, Coupling
    coupling = Coupling(coupling_map)
    compiled_dag, final_layout = swap_mapper(copy.deepcopy(dag_circuit), coupling, initial_layout = None, trials=20)
    # Expand swaps
    compiled_dag = _unroller_code(compiled_dag.qasm())
    # Change cx directions
    compiled_dag = direction_mapper(compiled_dag, coupling)
    # Simplify cx gates
    cx_cancellation(compiled_dag)
    # Simplify single qubit gates
    compiled_dag = optimize_1q_gates(compiled_dag)
    #####################
    # Put your code here
    #####################
    # Return the compiled dag circuit
    return compiled_dag


def _unroller_code(qasm_circuit, basis_gates=None):
    """ Unroll the code.

    Circuit is the circuit to unroll using the DAG representation.
    This is an internal function.

    Args:
        qasm_circuit: a circuit representation as qasm text.
        basis_gates (str): a comma seperated string and are the base gates,
                           which by default are: u1,u2,u3,cx,id
    Return:
        dag_ciruit (dag object): a dag representation of the circuit
                                 unrolled to basis gates
    """
    from qiskit import qasm, unroll
    if not basis_gates:
        basis_gates = "u1,u2,u3,cx,id"  # QE target basis
    program_node_circuit = qasm.Qasm(data=qasm_circuit).parse()
    unroller_circuit = unroll.Unroller(program_node_circuit,
                                       unroll.DAGBackend(
                                           basis_gates.split(",")))
    dag_circuit_unrolled = unroller_circuit.execute()
    return dag_circuit_unrolled
