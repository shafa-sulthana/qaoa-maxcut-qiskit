import numpy as np
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from scipy.optimize import minimize


# ---------------------------------
# 1. Define the Max-Cut problem
# ---------------------------------

edges = [(0, 1), (1, 2), (0, 2)]


def cut_value(bitstring, edges):
    value = 0

    for i, j in edges:
        if bitstring[i] != bitstring[j]:
            value += 1

    return value


# ---------------------------------
# 2. Calculate average cut
# ---------------------------------

def calculate_average_cut(counts, edges):
    total_shots = sum(counts.values())
    total_cut = 0

    for bitstring, count in counts.items():
        cut = cut_value(bitstring, edges)
        total_cut += cut * count

    return total_cut / total_shots


# ---------------------------------
# 3. Create QAOA circuit
# ---------------------------------

def create_qaoa_circuit(gamma, beta):

    qc = QuantumCircuit(3)

    # Initial superposition
    for qubit in range(3):
        qc.h(qubit)

    # Cost layer
    for i, j in edges:
        qc.cx(i, j)
        qc.rz(2 * gamma, j)
        qc.cx(i, j)

    # Mixer layer
    for qubit in range(3):
        qc.rx(2 * beta, qubit)

    qc.measure_all()

    return qc


# ---------------------------------
# 4. QAOA objective function
# ---------------------------------

simulator = AerSimulator()


def qaoa_objective(params):

    gamma, beta = params

    circuit = create_qaoa_circuit(gamma, beta)

    result = simulator.run(
        circuit,
        shots=1024
    ).result()

    counts = result.get_counts()

    average_cut = calculate_average_cut(
        counts,
        edges
    )

    # scipy minimizes, so return negative
    return -average_cut


# ---------------------------------
# 5. Optimize parameters
# ---------------------------------

initial_params = [0.5, 0.3]

result = minimize(
    qaoa_objective,
    initial_params,
    method="COBYLA",
    options={"maxiter": 30}
)

optimal_gamma, optimal_beta = result.x


# ---------------------------------
# 6. Run optimized circuit
# ---------------------------------

optimized_circuit = create_qaoa_circuit(
    optimal_gamma,
    optimal_beta
)

optimized_result = simulator.run(
    optimized_circuit,
    shots=1024
).result()

optimized_counts = optimized_result.get_counts()


# ---------------------------------
# 7. Calculate final performance
# ---------------------------------

optimized_average_cut = calculate_average_cut(
    optimized_counts,
    edges
)


# ---------------------------------
# 8. Display results
# ---------------------------------

print("QAOA Max-Cut Results")
print("----------------------------")

print("Optimal gamma:", optimal_gamma)
print("Optimal beta:", optimal_beta)

print(
    "Average cut:",
    optimized_average_cut
)

print(
    "Maximum possible cut:",
    2
)

print("\nMeasurement results:")

for bitstring, count in sorted(
    optimized_counts.items(),
    key=lambda x: x[1],
    reverse=True
):

    print(
        bitstring,
        "->",
        count,
        "shots",
        "| Cut value:",
        cut_value(bitstring, edges)
    )


# ---------------------------------
# 9. Probability distribution
# ---------------------------------

total_shots = sum(
    optimized_counts.values()
)

probabilities = {}

for bitstring, count in optimized_counts.items():

    probabilities[bitstring] = (
        count / total_shots
    )


# ---------------------------------
# 10. Plot results
# ---------------------------------

bitstrings = list(probabilities.keys())
prob_values = list(probabilities.values())

plt.figure(figsize=(8, 5))

plt.bar(
    bitstrings,
    prob_values
)

plt.xlabel("Bitstring")
plt.ylabel("Probability")

plt.title(
    "QAOA Solution Probability Distribution"
)

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    "qaoa_probability_distribution.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()