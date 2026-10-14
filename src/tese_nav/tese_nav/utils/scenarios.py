"""
Definições dos CENÁRIOS experimentais (anomalias e perigos).
============================================================

Extraído de `anomaly_simulator.py` na resubmissão (Access-2026-46291) para que
os scripts de ANÁLISE possam importar as definições sem depender de `rclpy`.
O `anomaly_simulator` re-exporta tudo, então os imports existentes
(`from tese_nav.anomaly_simulator import scenario_events`) seguem válidos.

Fonte única da verdade sobre intensidades e posições verdadeiras dos eventos.
"""

# anomalias de ATRAÇÃO (id, x, y, tipo, intensidade) — coerentes com subestacao.sdf
DEFAULT_ANOMALIES = [
    {'id': 0, 'x': 10.0, 'y': 10.0, 'type': 'thermal', 'intensity': 0.85},
    {'id': 1, 'x': 0.0, 'y': 15.0, 'type': 'thermal', 'intensity': 0.91},
    {'id': 2, 'x': -5.0, 'y': 5.0, 'type': 'acoustic', 'intensity': 0.72},
]

# zonas de PERIGO (repulsão), persistentes. Posicionado ao LADO da 1ª perna
# (spawn -10,-10 -> transit_sul 13,-8), com o destino ALÉM dele (a leste): o
# robô passa a ~3 m, o recuo radial o empurra para o norte e ele segue a leste
# sem reentrar na zona -> UM recuo limpo (vs oscilação quando o perigo fica ao
# lado de uma perna cujo objetivo está "atrás" da zona).
DEFAULT_HAZARDS = [
    {'id': 100, 'x': 2.0, 'y': -13.0, 'intensity': 0.9},
]

# Cenário ADVERSO (E5): mesma rota, mas anomalias mais DENSAS. Clusters (2 perto
# do transformador, 2 perto do disjuntor) fazem múltiplas entrarem no raio ao
# mesmo tempo -> testa a arbitragem (qual investigar primeiro) e o
# visitado-uma-vez sob carga (5 anomalias vs 3 do default). Mantém o MESMO
# perigo do default (recuo único limpo): um 2º perigo na rota travaria o robô
# (objetivo "atrás" da zona -> AVOID infinito), então o eixo "adverso" aqui é a
# densidade de anomalias, não de perigos.
ADVERSE_ANOMALIES = [
    {'id': 0, 'x': 10.0, 'y': 10.0, 'type': 'thermal', 'intensity': 0.85},
    {'id': 1, 'x': 7.0, 'y': 8.0, 'type': 'acoustic', 'intensity': 0.78},   # cluster transformador
    {'id': 2, 'x': 0.0, 'y': 15.0, 'type': 'thermal', 'intensity': 0.91},
    {'id': 3, 'x': -5.0, 'y': 5.0, 'type': 'acoustic', 'intensity': 0.72},
    {'id': 4, 'x': -8.0, 'y': 8.0, 'type': 'thermal', 'intensity': 0.80},   # cluster disjuntor
]
ADVERSE_HAZARDS = [
    {'id': 100, 'x': 2.0, 'y': -13.0, 'intensity': 0.9},
]

# Cenário PERIGO-SOBRE-A-ROTA (safety): perigo em cima da 1ª perna da patrulha
# (spawn -10,-10 -> transit_sul 13,-8), em ~(1.5,-9). O baseline (sem camada
# afetiva) passa por cima; o método recua (reflexo reativo) E projeta um keepout
# no costmap global (repulsão afetiva -> planejador deliberativo replaneja e
# contorna). Anomalias iguais ao default para a missão também inspecionar.
ROUTE_HAZARD_ANOMALIES = list(DEFAULT_ANOMALIES)
ROUTE_HAZARD_HAZARDS = [
    {'id': 100, 'x': 1.5, 'y': -9.0, 'intensity': 0.9},   # SOBRE a 1ª perna
]

# Cenário CONFLITO atração×repulsão (R2#8/R4#3): um perigo FRACO co-localizado
# com uma anomalia FORTE, ambos dentro do raio de detecção ao mesmo tempo quando
# o robô passa pela 1ª perna (~(2,-8.96)). Testa se a prioridade de segurança
# domina a seleção por magnitude: mesmo a anomalia (0.95) sendo mais saliente que
# o perigo (0.40), o robô deve EVITAR o perigo e NÃO inspecionar a anomalia
# co-localizada. As 3 anomalias default continuam (inspecionadas normalmente).
# Anomalia acústica FORTE co-localizada com o perigo em (2,-13) (mesma geometria
# estável do default -> 1 avoid limpo). Em |w*i|: anomalia = w_acoustic*0.95 =
# 1.2*0.95 = 1.14; perigo = |w_hazard|*0.70 = 1.5*0.70 = 1.05. Ou seja, a
# anomalia é MAIS saliente que o perigo -- se a arbitragem fosse por magnitude, a
# atração venceria. O perigo (0.70) ainda cruza o limiar de Avoid na passagem
# (~4 m). Demonstra a precedência de segurança: o robô EVITA e não inspeciona a
# anomalia co-localizada, apesar de ela ser mais forte.
CONFLICT_ANOMALIES = DEFAULT_ANOMALIES + [
    {'id': 5, 'x': 2.0, 'y': -13.0, 'type': 'acoustic', 'intensity': 0.95},
]
CONFLICT_HAZARDS = [
    {'id': 100, 'x': 2.0, 'y': -13.0, 'intensity': 0.70},   # co-localizado, mais fraco em |w*i|
]

# ENSAIO DIRIGIDO -- perigo que SURGE DURANTE a investigação (R4.2/§6 do parecer):
# uma anomalia térmica na aproximação da 1ª perna e um perigo CO-LOCALIZADO que só
# ATIVA (passa a ser publicado) quando o robô chega a <= activate_radius (3 m), i.e.,
# já comprometido com a investigação e aproximando-se. Isola o VALOR DO RECUO reativo:
# com recuo (avoid on, DHa) o robô foge de imediato via preempção; sem recuo (keepout
# só, DHb) depende do replanejamento do Nav2, mais lento -> aproxima-se mais do perigo.
DYNHAZ_ANOMALIES = [
    {'id': 0, 'x': 2.0, 'y': -13.0, 'type': 'thermal', 'intensity': 0.90},
]
DYNHAZ_HAZARDS = [
    {'id': 100, 'x': 2.0, 'y': -13.0, 'intensity': 0.90, 'activate_radius': 3.0},
]

SCENARIOS = {
    'default': (DEFAULT_ANOMALIES, DEFAULT_HAZARDS),
    'adverse': (ADVERSE_ANOMALIES, ADVERSE_HAZARDS),
    'route_hazard': (ROUTE_HAZARD_ANOMALIES, ROUTE_HAZARD_HAZARDS),
    'conflict': (CONFLICT_ANOMALIES, CONFLICT_HAZARDS),
    'dyn_hazard': (DYNHAZ_ANOMALIES, DYNHAZ_HAZARDS),
}

# §8: o keepout deliberativo NÃO é mais gated por nome de cenário. É um canal
# deliberativo geral, controlado pelo parâmetro `publish_keepout`, que projeta um
# perigo DETECTADO (dentro do raio sensorial, na posição PERCEBIDA) no costmap
# global para o Nav2 contornar. Assim a resposta em dois tempos (recuo reflexo +
# keepout) usa só informação detectada — sem verdade de terreno nem projeção
# antecipada — e a ativação vira uma regra operacional, não conhecimento do
# cenário. Os experimentos escolhem publish_keepout/enable_reactive_avoid via
# launch para a ablação causal (recuo-só / keepout-só / ambos).

def scenario_events(name):
    """Retorna (anomalias, perigos) do cenário. Fallback p/ 'default'."""
    return SCENARIOS.get(name, SCENARIOS['default'])
