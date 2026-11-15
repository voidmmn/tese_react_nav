# tese_ws — simulação e pacote de reprodução da tese

Workspace ROS 2 da tese **"Arquitetura Deliberativo-Reativa de Duas Camadas para
Inspeção de Subestações Elétricas: Campo de Atração–Repulsão Acionado por Limiar e
Atribuição Experimental de Efeitos a Mecanismos"**.

**Autor:** Milton Miranda Neto · **Orientador:** Prof. Alexandre Cardoso (UFU) ·
PPGEELT/UFU, 2026.

## O que o sistema faz

Duas camadas sobre a mesma pilha de navegação:

- **Camada deliberativa:** ronda por *waypoints* planejada e executada pelo Nav2
  (controlador MPPI, AMCL sobre mapa estático).
- **Camada reativa (*Stay Alert*):** um supervisor que, **ao cruzar um limiar**,
  preempta a ronda para investigar uma anomalia ou se afastar de um risco. A
  decisão consulta um campo escalar Φ de atração e repulsão, construído a partir
  de eventos sensoriais, com **precedência categórica de segurança**: qualquer
  risco acima do limiar domina qualquer atração, independentemente da magnitude
  relativa. Não é disputa de soma entre forças.

> **Nota sobre a formulação.** Versões anteriores deste README descreviam o
> mecanismo como uma "equação de Bellman atratora", em que Φ modularia a função de
> valor em tempo real. **A tese não sustenta essa descrição do método principal.**
> O arbítrio entre inspecionar e se afastar é resolvido por **limiar
> determinístico**; a tabela de valor permanece passiva e não governa o
> comportamento avaliado. Uma política tabular treinada com recompensa aumentada
> por Φ existe no repositório (`qdriven_node.py`), mas **como linha de base
> comparativa**, não como o método proposto.

## Stack

ROS 2 Humble · Gazebo **Fortress** (ign-gazebo 6) · Nav2 (MPPI) · AMCL sobre mapa
estático · robô diferencial `inspector_bot`.

## Estrutura

```
src/tese_nav/tese_nav/     nós: stay_alert, anomaly_simulator, mission, metrics,
                           apf, qdriven, bellman (passivo), fake_scan_publisher
src/tese_nav/scripts/      analisadores e geradores (ver abaixo)
src/tese_nav/config/       nav2_params, waypoints, maps/
src/tese_nav/launch/       robot_sim, nav2_amcl, simulation, stay_alert, experimento
results/                   pacote de reprodução (dados, logs, somas de verificação)
docs/tese/                 fonte LaTeX da tese
docs/artigo/               fonte do artigo (IEEE Access, DOI 10.1109/ACCESS.2026.3753770)
```

## Reproduzir a tese sem rodar simulação

Os números das tabelas saem dos CSVs já publicados. Nada aqui exige Gazebo.

```bash
# 1) integridade dos dados (dois conjuntos, duas coberturas)
cd results
sha256sum -c CHECKSUMS.sha256                         # deve fechar 323/323
sha256sum -c CHECKSUMS_verificacao_decaimento.sha256  # deve fechar  61/61

# 2) censo: 320 tentadas, 311 válidas, 302 concluídas, 9 censuradas
python3 ../src/tese_nav/scripts/gerar_manifesto.py . --conjunto historico
python3 ../src/tese_nav/scripts/gerar_manifesto.py . --conjunto verificacao   # 60

# 3) família primária: 15 testes, Holm dentro da família
python3 ../src/tese_nav/scripts/analise_estatistica.py .
#    grava familia_confirmatoria.csv
#    SHA-256 esperado: 70364075957cf490e3e472d37f83c407350ab08fc0e6b212280c350e09a3592c

# 4) família Q-driven: 24 testes (3 cenários x 8 desfechos)
python3 ../src/tese_nav/scripts/analise_qdriven.py .

# 5) reconciliação dos 685 lançamentos registrados
python3 ../src/tese_nav/scripts/gerar_reconciliacao.py . > reconciliacao_lancamentos.csv
#    grava também reconciliacao_lancamentos_individual.csv, uma linha por lançamento
```

Os três analisadores **falham com erro** se o pacote estiver incompleto, em vez de
produzir tabela vazia ou censo inflado. Um pacote que passa é um pacote completo.

### Dois conjuntos na mesma pasta

`results/` guarda duas baterias, distinguidas pelo rótulo da configuração:

| Conjunto | Rótulos | n |
|---|---|---:|
| Matriz histórica | os 32 restantes | 320 |
| Verificação do relógio do decaimento | `CMw` `CMs` `E3w` `E3s` `HEUw` `HEUs` | 60 |

O sufixo `w` é relógio de parede e `s` é relógio simulado. A verificação **não**
pertence à matriz e tem manifesto e somas de verificação próprios. Os seletores
dos *scripts* impedem que os conjuntos se misturem por omissão.

As dezesseis baterias descartadas (`results/_*`, ~297 MB) **não** são versionadas,
por volume. Cada lançamento delas está nominado em
`reconciliacao_lancamentos_individual.csv`, com origem e critério de exclusão; o
lote `_noturna_20260901` aparece ali como lacuna declarada, porque seus logs não
foram preservados.

## Rodar a simulação

```bash
cd ~/tese_ws && colcon build --packages-select tese_nav && source install/setup.bash
ros2 launch tese_nav experimento.launch.py run_label:=E3 rviz:=true
```

Uma bateria completa leva cerca de dez minutos por execução, com limite de parede
de 600 s por tentativa.

## Qual versão auditar

Use a **etiqueta anotada**, não o ramo principal, que continua recebendo trabalho:

```bash
git rev-parse tese-defesa-v1^{commit}
```

## Limitações declaradas

- O **relógio do decaimento** do campo compara instantes de relógio de parede
  enquanto os temporizadores correm em tempo simulado. O período realizado fica em
  1,57–1,60 s onde a especificação diz 1 s. O padrão do parâmetro `decay_clock`
  permanece `wall` **de propósito**, para que as 320 execuções analisadas sigam
  comparáveis entre si e com o artigo publicado. A Seção 6.13 da tese mede o efeito
  disso e declara qual conclusão depende dele.
- O manifesto **não** registra o identificador de *commit* de cada execução das
  baterias anteriores a 13/11/2026, porque o executor não o gravava. O campo fica
  vazio, em vez de preenchido por inferência de data.
- Entrega simulada: nenhum resultado aqui foi medido em subestação real.
