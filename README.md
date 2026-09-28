%%writefile README.md

# QAOA Max-Cut Optimization

## Project Overview

This project demonstrates the Quantum Approximate Optimization Algorithm (QAOA)
for solving the Max-Cut problem on a 3-node triangle graph.

QAOA combines quantum circuits with classical optimization to search for
high-quality solutions to combinatorial optimization problems.

## Problem

The graph contains three nodes and three edges:

- (0, 1)
- (1, 2)
- (0, 2)

The objective is to divide the nodes into two groups so that the maximum
number of edges connect nodes belonging to different groups.

For this triangle graph, the maximum cut value is 2.

## Methodology

The QAOA circuit consists of:

1. Initial superposition using Hadamard gates
2. Cost Hamiltonian / cost layer
3. Mixer layer
4. Measurement
5. Classical parameter optimization

The two QAOA parameters are:

- Gamma (γ): controls the cost layer
- Beta (β): controls the mixer layer

## Optimization

The classical COBYLA optimizer was used to optimize gamma and beta.

The optimized parameters produced an average cut value very close to the
theoretical maximum of 2.

## Results

The optimized circuit produced the following maximum-cut bitstrings:

- 001
- 010
- 011
- 100
- 101
- 110

Each of these bitstrings has a cut value of 2.

In the final 1024-shot simulation, 1020 measurements produced maximum-cut
solutions.

## Technologies Used

- Python
- Qiskit
- Qiskit Aer
- NumPy
- SciPy
- Matplotlib
- Google Colab

## Project Structure

```text
qaoa-maxcut/
│
├── qaoa_maxcut.py
├── qaoa_probability_distribution.png
└── README.md