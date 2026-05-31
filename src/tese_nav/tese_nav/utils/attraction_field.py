"""
Campo atrator Phi(s,a).
=======================

Phi(s,a) modula a equação de Bellman em função de eventos sensoriais:

    Phi > 0  -> atração   (anomalia de interesse: ponto quente, descarga)
    Phi < 0  -> repulsão  (perigo / obstáculo dinâmico)
    Phi = 0  -> neutro    (comportamento Nav2 padrão)

A intensidade combina múltiplas modalidades sensoriais com pesos
configuráveis e aplica um decaimento temporal — uma anomalia detectada
"esfria" se deixa de ser observada, evitando que o robô fique preso.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Dict


@dataclass
class AttractionField:
    # pesos por modalidade (acústica > térmica: descargas parciais são
    # eventos mais críticos em subestações)
    weights: Dict[str, float] = field(default_factory=lambda: {
        'thermal': 1.0,
        'acoustic': 1.2,
        'hazard': -1.5,   # repulsão
    })
    # limiares de disparo por modalidade (permissivos: registram a leitura
    # dentro de quase todo o alcance do sensor)
    thresholds: Dict[str, float] = field(default_factory=lambda: {
        'thermal': 0.4,
        'acoustic': 0.3,
        'hazard': 0.3,
    })
    decay: float = 0.85          # fator multiplicativo por passo de decaimento
    decay_period: float = 1.0    # segundos
    clip: float = 2.0            # limita |Phi|

    _phi: float = 0.0
    _last_decay: float = field(default_factory=time.monotonic)

    # ------------------------------------------------------------------ #
    def observe(self, modality: str, intensity: float) -> float:
        """
        Registra uma leitura sensorial e atualiza Phi.

        Retorna o Phi atualizado. Leituras abaixo do limiar são ignoradas.
        """
        thr = self.thresholds.get(modality)
        w = self.weights.get(modality)
        if thr is None or w is None:
            return self._phi
        if intensity < thr:
            return self._phi

        contribution = w * intensity
        # mantém o evento mais forte da janela (em magnitude, preservando sinal)
        if abs(contribution) > abs(self._phi):
            self._phi = contribution
        self._clip()
        return self._phi

    # ------------------------------------------------------------------ #
    def step_decay(self) -> float:
        """Aplica decaimento temporal. Chamar periodicamente (timer)."""
        now = time.monotonic()
        if now - self._last_decay >= self.decay_period:
            self._phi *= self.decay
            if abs(self._phi) < 1e-3:
                self._phi = 0.0
            self._last_decay = now
        return self._phi

    @property
    def value(self) -> float:
        return self._phi

    def reset(self) -> None:
        self._phi = 0.0

    def _clip(self) -> None:
        self._phi = max(-self.clip, min(self.clip, self._phi))
