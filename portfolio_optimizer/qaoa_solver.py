import numpy as np
import cirq
import itertools
from typing import Sequence, List


def make_qaoa_circuit(
    mu: np.ndarray,
    cov: np.ndarray,
    gammas: Sequence[float],
    betas: Sequence[float]
) -> cirq.Circuit:
    """
    Constructs a QAOA circuit for portfolio optimization.
    """
    n = len(mu)
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit(cirq.H.on_each(*qubits))
    for p in range(len(gammas)):
        gamma, beta = gammas[p], betas[p]
        for i, q in enumerate(qubits):
            h = mu[i] / 2
            circuit.append(cirq.Z(q)**(2 * gamma * h / np.pi))
        for i, j in itertools.combinations(range(n), 2):
            J = cov[i, j] / 4
            circuit.append(cirq.ZZ(qubits[i], qubits[j])**(2 * gamma * J / np.pi))
        circuit.append(cirq.rx(2 * beta).on_each(*qubits))
    circuit.append(cirq.measure(*qubits, key='z'))
    return circuit


def select_portfolio(
    mu: np.ndarray,
    cov: np.ndarray,
    tickers: List[str],
    budget: int,
    depth: int,
    grid_points: int,
    shots: int
) -> List[str]:
    """
    Runs QAOA circuit grid search and selects the best portfolio.
    Falls back to Sharpe ratio if no solution found.
    """
    sim = cirq.Simulator()
    best_score, best_bits = -np.inf, None
    gamma_vals = np.linspace(0, np.pi, grid_points)
    beta_vals = np.linspace(0, np.pi/2, grid_points)
    for gammas in itertools.product(gamma_vals, repeat=depth):
        for betas in itertools.product(beta_vals, repeat=depth):
            circ = make_qaoa_circuit(mu, cov, gammas, betas)
            res = sim.run(circ, repetitions=shots)
            counts = res.histogram(key='z', fold_func=lambda b: ''.join(str(int(x)) for x in b[::-1]))
            for bstr, ct in counts.items():
                bits = np.array([int(c) for c in bstr])
                k = bits.sum()
                if 0 < k <= budget:
                    cost = -mu.dot(bits) + bits @ cov @ bits
                    score = (ct/shots) * (-cost)
                    if score > best_score:
                        best_score, best_bits = score, bits
    if best_bits is None:
        sharpe = mu / np.sqrt(np.diag(cov))
        idxs = np.argsort(-sharpe)[:budget]
        best_bits = np.zeros_like(mu, int)
        best_bits[idxs] = 1
    return [tickers[i] for i, v in enumerate(best_bits) if v]
