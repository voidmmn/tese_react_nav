"""
Tabela Q tabular para a Bellman atratora.
=========================================

Q-learning tabular com discretização de estado. Mantida simples e
interpretável (decisão de projeto da tese: "convergência garantida").

Estado discreto: (cell_x, cell_y, anomaly_bucket)
  - cell_x, cell_y : célula da grade do mundo (resolução configurável)
  - anomaly_bucket : nível de anomalia local discretizado [0..n_buckets-1]

Ações: forward, left, right, stop.
"""
from __future__ import annotations

import json
from typing import Dict, Iterable, Tuple

ACTIONS = ('forward', 'left', 'right', 'stop')

State = Tuple[int, int, int]


def discretize(x: float, y: float, anomaly: float,
               cell_size: float = 1.0,
               anomaly_buckets: int = 4) -> State:
    """Converte posição contínua + nível de anomalia em estado discreto."""
    cx = int(round(x / cell_size))
    cy = int(round(y / cell_size))
    # anomaly assumido em [0, 1]; clamp e discretiza
    a = min(max(anomaly, 0.0), 1.0)
    bucket = min(int(a * anomaly_buckets), anomaly_buckets - 1)
    return (cx, cy, bucket)


class QTable:
    """Tabela Q esparsa (default 0.0) com utilitários de update e log."""

    def __init__(self, alpha: float = 0.1, gamma: float = 0.95):
        self.alpha = alpha
        self.gamma = gamma
        self._q: Dict[Tuple[State, str], float] = {}
        self.updates = 0
        # soma dos |td_error| por janela (proxy SEM o termo afetivo) e soma do
        # |resíduo completo| = |alpha*td + eta*Phi| (COM o termo afetivo). O
        # segundo é o que de fato mede se a atualização com a perturbação
        # afetiva se estabiliza (R1#4/R2#4): reportar só o proxy não pode
        # atestar estabilidade do termo que ele exclui.
        self._abs_td_window = 0.0
        self._abs_full_window = 0.0
        self._window_count = 0

    # ------------------------------------------------------------------ #
    def get(self, state: State, action: str) -> float:
        return self._q.get((state, action), 0.0)

    def max_q(self, state: State) -> float:
        return max(self.get(state, a) for a in ACTIONS)

    def best_action(self, state: State) -> str:
        return max(ACTIONS, key=lambda a: self.get(state, a))

    # ------------------------------------------------------------------ #
    def update(self, state: State, action: str, reward: float,
               next_state: State, phi: float = 0.0, eta: float = 0.0) -> float:
        """
        Atualização de Bellman *atratora*:

            Q(s,a) <- Q(s,a) + alpha*[r + gamma*max_a' Q(s',a') - Q(s,a)]
                              + eta * Phi(s,a)

        Retorna o td_error (sem o termo atrator) para fins de métrica.
        """
        q_sa = self.get(state, action)
        td_error = reward + self.gamma * self.max_q(next_state) - q_sa
        full_residual = self.alpha * td_error + eta * phi   # incremento aplicado
        self._q[(state, action)] = q_sa + full_residual

        self.updates += 1
        self._abs_td_window += abs(td_error)
        self._abs_full_window += abs(full_residual)
        self._window_count += 1
        return td_error

    # ------------------------------------------------------------------ #
    def mean_abs_td(self, reset: bool = True) -> float:
        """TD-error médio absoluto da janela (proxy SEM o termo afetivo).
        Se reset, zera AMBAS as janelas (td e resíduo completo)."""
        if self._window_count == 0:
            return 0.0
        m = self._abs_td_window / self._window_count
        if reset:
            self._abs_td_window = 0.0
            self._abs_full_window = 0.0
            self._window_count = 0
        return m

    def mean_abs_full(self) -> float:
        """|resíduo completo| médio da janela = média de |alpha*td + eta*Phi|.
        Não reseta (leia ANTES de mean_abs_td, que compartilha o contador)."""
        if self._window_count == 0:
            return 0.0
        return self._abs_full_window / self._window_count

    def size(self) -> int:
        return len(self._q)

    def items(self) -> Iterable[Tuple[Tuple[State, str], float]]:
        return self._q.items()

    def to_json(self) -> str:
        # chaves tuple não são serializáveis: converte para string
        return json.dumps({f'{s}|{a}': v for (s, a), v in self._q.items()})
