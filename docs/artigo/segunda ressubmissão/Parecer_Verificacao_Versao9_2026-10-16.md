# Verificação das correções — manuscrito, versão (9)

**Data:** 16 de outubro de 2026  
**Documento:** *A Two-Layer Deliberative–Reactive Architecture with an Affective Attraction–Repulsion Layer for Autonomous Substation Inspection*, PDF com sufixo `(9)`, 23 páginas.  
**Natureza:** parecer técnico independente; não representa decisão editorial da IEEE. As páginas abaixo são as numeradas no PDF.

## Veredito

**O manuscrito melhorou substancialmente, mas eu ainda corrigiria esta versão antes de submetê-la.** Os principais problemas anteriores de valores incompatíveis, atribuição do ganho ao método completo e confusão entre confirmação e controle foram corrigidos. Restam contradições localizadas entre passagens do próprio artigo, especialmente na classificação da análise estatística e na definição de duas métricas.

Não recomendo uma nova bateria de experimentos para resolver os itens deste parecer. As ações necessárias são sincronização do texto e, em alguns pontos, consulta aos registros e ao gerador das tabelas já existentes.

Li o PDF completo e conferi visualmente suas páginas, com inspeção ampliada dos trechos críticos. Esta rodada verifica a consistência do manuscrito: **não equivale a recalcular os resultados a partir dos CSVs, auditar os commits ou validar o código**. Também não certifica uma versão atualizada da carta de resposta que não foi examinada nesta rodada.

## 1. O que considero resolvido

| Questão anterior | Verificação nesta versão | Situação |
|---|---|---|
| APF com valores e sinal de intervalo incompatíveis | Tabelas 6 e 10: distância de aproximadamente 86,4 m para APF e 86,6 m para E3; IC da diferença E3 − APF `[+0,08; +0,30]` m. O texto reconhece a proximidade das distâncias. | Resolvido no manuscrito. |
| Confirmação indevidamente inserida na decisão do controlador | Algoritmo 1 emite o evento de encerramento; §III-C e §V-I separam a avaliação posterior da lógica de controle. | Resolvido. A ressalva sobre o hand-off abaixo é outra linha do algoritmo. |
| Família de 15 testes sem exposição completa | Tabela 5 apresenta os 15 testes, tamanhos amostrais, procedimentos, efeitos, intervalos e p-valores. Os valores discutidos na sua mensagem aparecem corrigidos. | Resolvido quanto à apresentação; o rótulo estatístico ainda precisa de ajuste. |
| Condição de keep-out pouco verificável | Tabelas 2 e 3 incluem Ret. e KO; a legenda da Tabela 3 esclarece que os seis blocos HEU/HEU-sel estão com KO desligado. | Resolvido. |
| Ganho KOa × KOF atribuído ao método completo | Resumo e conclusão distinguem o contraste de ablação da arquitetura completa. | Resolvido. |
| Persistência e seleção confundidas como efeito isolado | A descrição de HEU e HEU-sel delimita melhor o que cada comparação altera. | Substancialmente resolvido. |
| Exclusões e desempenho absoluto | A discussão distingue E3, APF e RHM e apresenta a influência das exclusões. | Correção incorporada. |
| DWA descrito como soma vetorial | A comparação distingue DWA de APF. | Resolvido. |
| Interpretação geométrica de 0,5 m | O texto calcula 0,25 m da borda do robô ao ponto de perigo e ressalva que isso não é distância a uma superfície física. | Resolvido. |
| Resultado adverso apresentado como inspeção completa universal | E5 aparece como 4,9 ± 0,3 anomalias, com 9/10 execuções completas. | Resolvido. |
| Renovação do campo no CM | §III-C e §V-F explicam que, sem KO, não ocorre delegação e novas observações renovam o canal de perigo. | Resolvido na exposição principal. |

Esses itens não precisam ser reabertos apenas porque outras frases ainda ficaram desatualizadas.

## 2. Correções necessárias antes do envio

### R1 — O rótulo “confirmatório” ainda contradiz a seleção retrospectiva dos desfechos

**Prioridade alta. Localização: contribuição 2, p. 2; pp. 9–12; Tabela 7, p. 14; Apêndice B e Tabela 14.**

A ressalva das pp. 10–11 é um avanço importante: os cinco desfechos foram definidos depois das execuções e a extensão da família é retrospectiva. Contudo, o restante do artigo continua usando formulações incompatíveis com essa ressalva:

- Contribuição 2: “with the confirmatory family stated in advance”.
- Título da Tabela 5: “The complete confirmatory family”.
- §V-B: “Confirmatory (Holm-corrected within the confirmatory family)” e “five confirmatory outcomes”.
- Outras ocorrências em métodos, resultados e legendas continuam chamando a família atual de confirmatória.

**Não basta retirar “pre-registered”.** Registro público e especificação prospectiva são questões distintas; aqui a limitação substantiva é que os desfechos foram escolhidos retrospectivamente. Apresentar todos os 15 testes e aplicar Holm torna a família explícita, mas não elimina a seleção retrospectiva nem torna prospectivo o conjunto de hipóteses.

**Ação:** adotar uma denominação uniforme, como “primary comparison family with retrospectively specified outcomes”. Manter os valores e a correção de multiplicidade; ajustar a classificação e a força das conclusões. Uma formulação possível:

> The three contrasts were specified in the analysis plan, whereas the five outcomes were selected retrospectively. We therefore report these fifteen tests as a primary comparison family with retrospectively specified outcomes. Holm adjustment addresses multiplicity within this reported family; it does not remove the limitations associated with retrospective outcome selection.

Na contribuição 2, substituir a promessa de família declarada antecipadamente por algo como:

> …with all fifteen tests in the primary comparison family reported and Holm-adjusted, and with retrospective outcome selection explicitly acknowledged.

Na Tabela 5, usar “Complete primary comparison family: three contrasts × five retrospectively specified outcomes”. Em §V-B, “Primary comparison, default scenario”. Fazer a mesma sincronização nas demais legendas. Preservar a identificação histórica da família da submissão anterior, quando esse for o assunto: uma substituição automática indiscriminada pode alterar esse sentido.

**Precisão adicional sobre a cronologia, p. 10:** o texto afirma que os contrastes foram especificados antes de as novas execuções produzirem qualquer dado, mas a evidência descrita é um commit anterior à gravação do primeiro arquivo. A segunda afirmação, isoladamente, não demonstra a primeira. Considerando sua informação de que o plano já reconhecia atividades iniciadas na noite 1, delimite a afirmação ao que o histórico efetivamente comprova. Se o que está comprovado é a anterioridade em relação ao primeiro CSV arquivado, diga isso. Não é necessário criar um novo protocolo; é necessário evitar uma alegação temporal mais forte que sua evidência.

**Origem:** pendência anterior corrigida no parágrafo central, mas ainda não propagada pelo documento.

### R2 — “Tempo total por execução” ainda vira “episódio médio” na análise de histerese

**Prioridade alta. Localização: Tabela 5, p. 12, versus §V-F, p. 16.**

A legenda da Tabela 5 define corretamente *investigation time* como tempo total por execução. Isso resolve a interpretação do zero de KOF e da diferença de −35,68 s.

Entretanto, a análise de histerese ainda diz:

> “shortens the mean investigation episode (35.1 → 26.6 s, p = 0.0003)”

Tempo total por execução e duração média por episódio são variáveis diferentes. O total pode mudar por duração, número e composição dos episódios. Não se pode trocar uma interpretação pela outra mantendo os mesmos números.

**Ação:** conferir no gerador a variável e o agregador de 35,1 e 26,6. Se forem os totais por execução, escrever:

> …reduces the per-run total time spent in Investigate (35.1 → 26.6 s, p = 0.0003), while the number of credited inspections remains three out of three.

Acrescentar “median” ou “mean” somente conforme a estatística realmente calculada. A explicação de que o robô se compromete mais perto do alvo deve ser sustentada pelos registros correspondentes ou apresentada como interpretação possível; o total de investigação sozinho não demonstra esse mecanismo.

**Origem:** correção anterior incorporada à definição principal, mas não a esta interpretação secundária.

### R3 — A faixa das inspeções rejeitadas contém distâncias menores que o limiar de rejeição

**Prioridade alta. Localização: §V-I, pp. 16–17, especialmente início da coluna direita da p. 17.**

O texto afirma que os episódios recusados pelo critério de 3,3 m terminaram a **2,9–3,6 m** do alvo verdadeiro. No mesmo trecho, a rejeição é atribuída à distância no encerramento, sem abortos ou timeouts.

Sob essa definição, um encerramento a 2,9 m está dentro do limiar de 3,3 m. Portanto, essa faixa não pode caracterizar exclusivamente as rejeições por exceder esse limiar. Isso é uma inconsistência textual verificável; não estou concluindo que o avaliador esteja implementado incorretamente.

**Ação:** consultar o subconjunto rejeitado no `audit_trail.csv`, usando o mesmo evento, alvo e instante empregados na confirmação. Corrigir a faixa ou removê-la. Não deduzir o limite inferior correto sem consultar os dados.

Uma substituição suficiente, utilizando a faixa geral já apresentada no artigo, é:

> Under high noise, closing distances across all episodes ranged from 1.83 to 3.56 m. Episodes whose closing distance exceeded the 3.3 m confirmation threshold were not credited.

Essa redação pressupõe que esse seja o critério exato do avaliador; conferir também o tratamento da igualdade. Se um episódio a 2,9 m tiver sido rejeitado por outro motivo, é esse motivo que precisa aparecer, em vez de atribuí-lo à distância.

Os resultados 4/9 e seis rejeições em 27 episódios podem permanecer se confirmados nos registros. Não é necessário repetir as simulações.

**Origem:** inconsistência na explicação da faixa de rejeições; a nova redação não resolveu a separação entre o subconjunto rejeitado e o conjunto de todos os episódios.

### R4 — O Algoritmo 1 ainda delega ao keep-out incondicionalmente

**Prioridade média. Localização: Algoritmo 1, linha 7, p. 7.**

O texto principal agora explica corretamente que o hand-off exige o canal de keep-out habilitado. A linha 7 do algoritmo, porém, ainda manda entregar o perigo ao keep-out e afirma que seu sinal reativo é suprimido, sem essa condição.

Isso contradiz as configurações sem KO e a explicação do CM. Também deixa ambígua a diferença entre parar novas publicações e apagar o valor já armazenado no campo.

**Ação:** explicitar a condição e a memória remanescente. Por exemplo:

> enter Avoid; pause patrol; send retreat goal; if keep-out is enabled, delegate the hazard to the deliberative layer and stop further reactive publications for that hazard; retain the stored hazard-channel value and let it decay.

Se o algoritmo pretende cobrir também as ablações com retirada reativa desabilitada, incluir o respectivo sinalizador na condição de entrada em Avoid. Alternativamente, delimitar expressamente o algoritmo à configuração com retirada habilitada. Não é uma solicitação de mudança no controlador.

**Origem:** linha remanescente do pseudocódigo; a correção de confirmação no mesmo algoritmo está aceita.

### R5 — O último período sobre a fronteira ainda exclui uma associação não mensurada

**Prioridade média. Localização: último parágrafo da p. 17.**

O texto reconhece corretamente que os cruzamentos de saída do raio de detecção não são temporizados. Contudo, conclui que dois eventos não estão associados a um cruzamento porque o campo registrado está acima do valor de fronteira:

> “…the recorded field at the transition is well above the boundary value, so neither is associated with a boundary crossing…”

Com memória e decaimento, a magnitude do campo não determina sozinha a posição atual em relação à fronteira. Se o cruzamento não foi registrado, essa observação não o exclui. Trocar causalidade por “associação” não basta para sustentar a exclusão.

**Ação:** manter os mecanismos observados nos logs e retirar a conclusão sobre ausência de cruzamento. Sugestão:

> The logs associate these short intervals with successive service of clustered targets or an immediate navigation abort. Because geometric boundary crossings were not timestamped and the field retains memory, these records do not establish whether a boundary crossing coincided with either event.

Isso preserva a análise útil já feita e sua limitação, sem exigir instrumentação nova para esta submissão.

**Origem:** inferência residual da discussão anterior, ainda presente após a qualificação do restante do parágrafo.

### R6 — A justificativa do horizonte de 400 s cita um máximo incompatível com E5

**Prioridade média. Localização: §V-F, p. 15, versus Tabela 6 e §V-H.**

A justificativa diz que 400 s foi escolhido acima da maior missão registrada pelo método proposto, aproximadamente 372 s em `route-hazard`. Mas E5 apresenta duração média de **397 ± 4 s**. Logo, 372 s não pode ser o máximo global das missões do método.

**Ação:** se 372 s se refere a um subconjunto usado para escolher o horizonte, nomear esse subconjunto e não o apresentar como máximo global. Caso essa proveniência não esteja documentada, remover a comparação com o suposto máximo e manter apenas a definição operacional do horizonte fixo de censura.

Não concluo que o horizonte de 400 s seja inválido, nem que algum E5 necessariamente excedeu 400 s: isso exige os valores individuais. O problema comprovado é a justificativa com máximo de 372 s.

**Origem:** inconsistência introduzida na explicação adicional do horizonte.

## 3. Ajustes curtos de sincronização

Estes podem ser feitos na mesma edição, sem nova análise experimental.

| Localização | Problema | Correção |
|---|---|---|
| §V-B, p. 12 | “three of the five are constant and identical” para E3 × HEU-sel. Na Tabela 5, apenas inspeções e retiradas são constantes e idênticas; os outros três desfechos variam. | Trocar “three” por “two”, considerando os cinco desfechos efetivamente tabelados. |
| Figura 5, p. 11 | “HEU-sel is indistinguishable … throughout” é mais forte que a ausência de diferença detectável discutida no texto. | “No statistically detectable difference was found between HEU-sel and the proposed layer in the default-scenario comparisons.” |
| Histerese, p. 16 | “Halving the width changes nothing” volta a afirmar ausência de efeito, apesar do título e da conclusão devidamente limitados. | “No statistically detectable difference was found between the two tested widths on the reported outcomes.” |
| Legenda da Tabela 3, p. 9 | Diz que cada configuração altera um único fator. HEU altera gatilho e seleção, conforme a própria tabela e §V-B. | Trocar “the single factor it changes” por “the settings that differ from the proposed layer”; reservar “one-factor” ao contraste que efetivamente o é. |
| Legenda da Tabela 6, p. 12 | O tamanho amostral é informado duas vezes, com conjuntos escritos de forma diferente. | Manter uma declaração: `n = 10 for E0–E5 and n = 9 for APF`. |

## 4. Critério para encerrar esta rodada

Eu encerraria a revisão documental quando:

1. A família atual não for mais apresentada como integralmente confirmatória ou definida antecipadamente.
2. A unidade e o agregador do tempo de investigação forem consistentes entre legenda, tabela e análise de histerese.
3. A faixa das rejeições for compatível com o limiar, ou for substituída pela faixa geral corretamente identificada.
4. A condição de hand-off estiver explícita no algoritmo.
5. A discussão de fronteira não excluir eventos geométricos que não foram medidos.
6. A justificativa do horizonte não usar 372 s como máximo global, e os pequenos ajustes da seção 3 forem aplicados.

**Minha avaliação é de uma revisão final localizada, não de reformulação do estudo.** Os resultados centrais não foram refutados por estes achados. O que falta é impedir que frases secundárias voltem a prometer uma evidência mais forte ou uma métrica diferente daquelas que as tabelas e as ressalvas agora descrevem corretamente.
