# Resposta ao parecer de 2026-10-16

Todos os itens foram verificados contra os dados (`results/`) e o código antes de
qualquer edição. Commits `5a0d04f` e `fa326f9`.

## Veredito por item

| Item | Veredito | O que foi feito |
|---|---|---|
| **P1** família/p-valores | **Procede, com diagnóstico diferente** | ver abaixo |
| **P2** APF Tab. 5 × Tab. 9 | **Procede, e é pior** | Tabela regerada dos CSVs |
| **P3** confirmação no Alg. 1 | **Procede; o código está certo** | Algoritmo e §III-C corrigidos |
| **P4** KOa × método completo | Procede | Resumo, §I e conclusão reescritos |
| **P5** persistência/equivalência | Procede | 6 trechos reformulados |
| **P6** fronteira de detecção | Procede | Causalidade → associação |
| **P7** matriz da bateria nova | Procede | Nova Tabela 3 (`tab:matrix-new`) |
| **P8** exclusões 2,7 → 3,0 | Procede | Corrigido no artigo **e** na carta |
| **T1** geometria 0,5 m | Procede | Frase removida |
| **T2** DWA como soma vetorial | Procede | Linhas APF e DWA separadas |
| **T3** notação de Φ | Procede | Φₜ; abuso de notação declarado |
| **T4** "all five anomalies" | Procede | Mediana 5, faixa 4–5 |
| **T5** hand-off | Procede | Mecanismo documentado do código |
| §6 carta (7 pontos) | Procede | Todos aplicados |

## P1 — o diagnóstico estava errado, o achado não

O parecer calcula `2/C(20,10) = 1,08e-5` e conclui que `p_Holm = 0,0027` é
impossível. A aritmética está certa; a atribuição não. O `0,0027` é o contraste de
**duração de missão** (bruto 1,746e-4; Holm 0,0021). O erro real é que **o mesmo
valor foi colado também no contraste de inspeções**, cujo Holm é 1,6e-4.

O `p_Holm = 0,42` está correto: bruto 0,0524, posto 8 de 15 → 0,4194. Isso confirma
que Holm sobre 15 testes foi de fato aplicado.

**O problema de fundo é maior do que o parecer podia ver sem o repositório.** O
`CONFIRMATORY` de `analise_estatistica.py` ainda era a família de **7 testes da
submissão anterior**, e `CONFIGS` nem listava HEU/KOF/CM. **Nenhum script
versionado calculava a família de 15** — os valores eram avulsos e digitados no
`.tex`.

Recuperei o conjunto de desfechos por busca exaustiva sobre 8 candidatos: ele
reproduz `0,0052`, `0,0511` e `0,4194` exatamente. São inspeções, folga mínima,
duração, **recuos** e **tempo de investigação** — exatamente os cinco que a carta
já nomeava no R2.4.

**Quatro p-valores estavam errados**, não um:

```
inspeções KOa×KOF    0,0027  →  1,6e-4
recuos E3×HEU        0,0034  →  3,0e-4
investigação E3×HEU  0,0034  →  0,0030
duração E3×HEU       0,0052  →  0,0050
```

Nenhum muda conclusão. Agora: `write_confirmatory()` emite
`results/familia_confirmatoria.csv` com n, médias, Δ, Cliff, IC, **procedimento** e
p bruto/Holm dos 15; `tabela_confirmatoria_tex.py` gera o corpo da Tabela 4 desse
CSV; os 7 antigos viram `tab:legacystats` no Apêndice B, sem correção.

## P2 — pior do que o parecer viu

| | Tabela 9 | `results/` |
|---|---|---|
| APF distância | 88,9 ± 1,1 | **86,39 ± 0,09** |
| APF folga mín. | 4,79 ± 0,06 | **4,81 ± 0,00** |
| IC da dif. de distância | [−3,1, −1,6] | **[+0,08, +0,30]** |

Além dos valores, **o sinal do IC estava invertido**. A linha de duração estava
certa. Tabela regerada; a legenda agora declara a convenção (proposto − APF,
oposta à da Tabela 4) e o texto diz que as distâncias são praticamente iguais.

## P3 — o código está do lado certo

`stay_alert_node.py` não tem nenhuma ocorrência de `confirm`. A confirmação vive no
`anomaly_simulator.py:242`, reagindo ao evento `investigate_end reason=inspected`
que o controlador já emitiu ao sair. **É pontuação pura, sem realimentação** — o
re-scoring do R2.5 está de pé e quem estava errado era o pseudocódigo. Corrigido
sem tocar no código.

## T5 — resolvido do código, não por hipótese

A delegação ao keep-out exige `avoid_start` **e** `publish_keepout`
(`anomaly_simulator.py:276`), e o que ela bloqueia é a **publicação** do perigo
(`:396`): novas observações param de alimentar `h`, o valor armazenado decai, o
keep-out segue travado.

Nos cenários fora de rota o keep-out está **desligado**, logo **não há delegação** e
a reobservação renova `h`. É exatamente por isso que a janela do CM mede 69,5 s
contra os ~39 s do decaimento puro. Verificado: zero linhas `DELEGADO` nos logs de
CM e CONF.

## Discordância parcial

Nenhuma de mérito. Uma de fato: **a ordem das Tabelas 2 e 3 não estava invertida** —
elas ficam lado a lado no topo da p. 8, 2 à esquerda e 3 à direita. Esse erro foi
meu, de uma rodada anterior, por ter lido a extração de texto em vez da página.

## Rodada 2 do parecer (2026-10-16, tarde)

### P1 — anterioridade da família: o parecer está certo, e a resposta é mista

Conferido no histórico, não por memória:

| | declarado antes? | evidência |
|---|---|---|
| os **3 contrastes** | **sim** | `PLANO_ANALISE_RESUB.md` §5, commit `9e0b93a` de 13/10 **21:47**; o primeiro CSV da bateria é `20261013_225416` — **67 min depois** |
| os **5 desfechos** | **não** | não constam de nenhum documento anterior; a busca de hoje foi a primeira vez que ficaram escritos |

Logo a família **não é pré-registrada**. O artigo passa a dizer exatamente isso:
contrastes pré-especificados, extensão retrospectiva, Holm aplicado como correção de
multiplicidade sobre uma família assim delimitada. Era a leitura (b) do parecer, e é
a correta.

### A origem do 0,0027 — eu também estava errado

`0,0027` não era "o valor da duração repetido". É o Holm exato de **proposta × HEU,
tempo de investigação** (0,002679), copiado para duas linhas de KOa × KOF. A lista
correta:

| contraste / desfecho | publicado | correto |
|---|---|---|
| KOa × KOF, inspeções | 0,0027 | 1,6e-4 |
| KOa × KOF, duração | 0,0027 | **0,0021** |
| proposta × HEU, recuos | 0,0034 | 3,0e-4 |
| proposta × HEU, investigação | 0,0034 | **0,0027** |

E duas correções minhas da rodada anterior eram arredondamento ruim: `0,0052` e
`0,0511` já estavam certos — eu havia trocado `0,0052` por `0,0050`. Revertido. O
gerador passou a imprimir 4 casas para que tabela e texto citem o mesmo número.

### T5 — a condição agora é conferível

Tabelas 2 e 3 ganharam colunas **Ret.** e **KO**, dos mesmos campos do runner. Dá
para ver que o keep-out está desligado em toda configuração fora de rota, incluindo
os seis blocos HEU/HEU-sel e o cenário marginal — ou seja, os contrastes
compartilham a condição com o método, não diferem nela.

### Tempo de investigação do KOF

A legenda da Tabela 5 passa a definir a métrica como **total por run**, não média por
episódio: uma configuração que nunca investiga contribui um `0` bem definido, e a
diferença de −35,68 s contra KOa é o total de KOa, não um encurtamento de episódios.

## Estado

Não houve nova bateria: tudo foi reanálise sobre os dados existentes e correção
documental, como o §9 do parecer previa. **A revisão só se encerra com a conferência
final do PDF recompilado** — os itens acima mudam texto, duas tabelas e a carta.
