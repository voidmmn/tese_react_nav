"""
Campo atrator Phi(s).
=====================

Phi(s) modula a camada reativa em função de eventos sensoriais:

    Phi > 0  -> atração   (anomalia de interesse: ponto quente, descarga)
    Phi < 0  -> repulsão  (perigo / obstáculo dinâmico)
    Phi = 0  -> neutro    (comportamento Nav2 padrão)

PRECEDÊNCIA DE SEGURANÇA (Eq. 4): a repulsão tem prioridade CATEGÓRICA sobre a
atração. Perigo e atração são rastreados SEPARADAMENTE (magnitude do perigo em
`_haz`; atração de maior módulo, com sinal, em `_att`), cada um com decaimento
temporal próprio. O valor do campo é:

    Phi = -_haz            se houver perigo acima do limiar (_haz > eps)
    Phi = _att             caso contrário

Assim, um perigo mais fraco co-localizado com uma atração mais saliente ainda
domina o campo — a prioridade NÃO é uma disputa de magnitude. O decaimento faz
uma detecção "esfriar" quando deixa de ser observada, evitando aprisionamento.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Dict

_EPS = 1e-3


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

    _att: float = 0.0            # atração corrente (maior módulo, sinal preservado)
    _haz: float = 0.0            # perigo corrente (magnitude >= 0)
    _last_decay: float = field(default_factory=time.monotonic)

    # ------------------------------------------------------------------ #
    def observe(self, modality: str, intensity: float) -> float:
        """
        Registra uma leitura sensorial. Perigo e atração são acumulados em
        canais separados; a precedência é resolvida em `value`. Leituras abaixo
        do limiar da modalidade são ignoradas. Retorna o Phi atualizado.
        """
        thr = self.thresholds.get(modality)
        w = self.weights.get(modality)
        if thr is None or w is None:
            return self.value
        if intensity < thr:
            return self.value

        contribution = w * intensity
        if modality == 'hazard':
            # canal de segurança: acumula a MAGNITUDE do perigo mais forte
            self._haz = max(self._haz, abs(contribution))
        else:
            # canal de atração: mantém o evento de maior módulo (sinal preservado)
            if abs(contribution) > abs(self._att):
                self._att = contribution
        self._clip()
        return self.value

    # ------------------------------------------------------------------ #
    def step_decay(self) -> float:
        """Aplica decaimento temporal a ambos os canais. Chamar periodicamente."""
        now = time.monotonic()
        if now - self._last_decay >= self.decay_period:
            self._att *= self.decay
            self._haz *= self.decay
            if abs(self._att) < _EPS:
                self._att = 0.0
            if self._haz < _EPS:
                self._haz = 0.0
            self._last_decay = now
        return self.value

    @property
    def value(self) -> float:
        # PRECEDÊNCIA CATEGÓRICA: qualquer perigo acima do limiar domina qualquer
        # atração, independentemente da magnitude relativa (Eq. 4).
        if self._haz > _EPS:
            return -self._haz
        return self._att

    # canais individuais (diagnóstico/auditoria)
    @property
    def hazard(self) -> float:
        return self._haz

    @property
    def attraction(self) -> float:
        return self._att

    def reset(self) -> None:
        self._att = 0.0
        self._haz = 0.0

    def _clip(self) -> None:
        self._att = max(-self.clip, min(self.clip, self._att))
        self._haz = min(self.clip, self._haz)   # magnitude, >= 0
