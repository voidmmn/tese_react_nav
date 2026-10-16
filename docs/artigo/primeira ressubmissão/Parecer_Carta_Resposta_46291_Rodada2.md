# Segunda avaliação da carta de resposta — Access-2026-46291

**Documento avaliado:** response_to_reviewers_46291(1).md  
**Comparação:** versão anterior da carta e parecer correspondente.  
**Data:** 14 de outubro de 2026.

## Parecer

**A carta melhorou, especialmente na resposta R2.3, mas ainda não recomendo submetê-la como está.** O problema principal agora é que algumas correções foram feitas em respostas específicas, sem serem propagadas para a síntese inicial e o encerramento.

Não estou solicitando outra ampliação experimental. As prioridades desta rodada são coerência interna, delimitação das inferências e resposta explícita a pedidos ainda parcialmente atendidos.

A confirmação das alterações no manuscrito, das métricas e dos registros permanece pendente do envio do artigo atualizado e, quando necessário, dos dados. Não certifico aqui a auditoria do código relatada pelos autores.

## 1. O que melhorou e não precisa ser reaberto

- **R2.3:** distingue contagens observadas idênticas de ausência de diferença detectada nas medidas contínuas.
- **Equivalência:** declara expressamente que não foi demonstrada.
- **Cenário adverse:** retirou a afirmação de que todos os métodos sempre inspecionam todas as cinco anomalias.
- **Mecanismo de HEU:** reconhece, a partir dos logs relatados, que há precedência e preempção, e que a diferença envolve o disparo e a persistência temporal.
- **R2.8:** removeu a contagem de cruzamentos de saída inferida de lacunas do registro e explicitou uma limitação do instrumento.
- **Tom:** o encerramento e a resposta sobre ajuste do APF ficaram menos autodepreciativos.

Esses avanços são relevantes. A próxima edição deve preservá-los e corrigir os trechos que ainda contam a história anterior.

## 2. Correção prioritária: o resumo inicial contradiz R2.3

A seção “What changed, in one paragraph” praticamente não foi atualizada e contém três afirmações incompatíveis com a nova resposta.

| Síntese inicial | Informação agora apresentada em R2.3 | Correção |
|---|---|---|
| “the saliency selection rule is inert” | Não foi detectada diferença; não há demonstração de equivalência. | Usar “no statistically detectable effect of changing the selection criterion in the evaluated scenarios”. |
| “reproduces the method in every scenario and metric” | As métricas contínuas variam, e as contagens no cenário adverse não são constantes. | Restringir identidade às contagens e cenários em que ela foi efetivamente observada. |
| “a generic … supervisor that discards [categorical safety precedence]” | HEU preserva precedência e preempta a investigação três vezes por execução. | Descrever a alteração do disparo e a perda da persistência do campo, sem afirmar remoção da precedência. |

**Essa é uma contradição científica, não apenas uma preferência de estilo.** O editor pode ler a síntese antes das respostas detalhadas.

Sugestão para substituir integralmente o parágrafo:

> The revised manuscript focuses on the evaluated deliberative–reactive architecture. Across the tested scenarios, replacing saliency-based target selection with nearest-target selection produced no statistically detectable difference in the reported outcomes; we therefore no longer claim a demonstrated benefit from that selection criterion. The raw-detection supervisor behaved differently in the conflict scenario. Inspection of the logs indicates that it retains hazard precedence, while its triggering logic does not use the field's temporal persistence. Because the trigger-mode switch changes both the decision signal and its persistence, the comparison does not isolate persistence alone. We report this limitation alongside the prolonged suppression observed in the marginal-hazard scenario. Separately, the static on-route hazard experiments support attributing the clearance improvement to detection-triggered keepout handling.

Usar a afirmação sobre os logs apenas conforme a auditoria efetivamente concluída.

## 3. Atribuição: manter no encerramento a cautela adotada em R2.3

R2.3 reconhece corretamente que separar a fonte do disparo da persistência exigiria outra variante. Contudo, o encerramento volta a afirmar:

> “the temporal persistence of its hazard channel has a measured benefit under conflict”

A comparação mede o efeito da configuração que combina essas características. A persistência é uma interpretação mecanística compatível com os logs, não um fator isolado por esse contraste.

Também é necessário trocar “saliency weighting … showed no detectable effect” por **“changing the target-selection criterion showed no detectable effect”**. A ablação da seleção não remove necessariamente todos os usos da ponderação no campo.

Sugestão de encerramento:

> We thank the reviewers for helping us clarify the contribution and strengthen its experimental assessment. The revised manuscript focuses on the evaluated architecture, reports the absence of a detectable benefit from changing the target-selection criterion in the tested scenarios, and documents differences associated with the field-based and raw-detection triggering modes. It also reports the inspection cost observed under a marginal hazard and attributes the clearance improvement in the static on-route scenario to detection-triggered keepout handling. The scope and limitations of each comparison are stated explicitly.

Não é necessário repetir a narrativa de que uma hipótese substituiu outra e depois também perdeu suporte.

## 4. Segurança: o limite de escopo continua faltando em R3.2

A carta ainda usa:

> “the safety benefit is attributable to the detection-triggered keep-out”

e:

> “What the reactive layer adds over KOF is the inspection behaviour and only that”

Acrescentar **“in the static on-route hazard scenario”** às conclusões pertinentes e retirar “and only that”. Isso evita generalizar para os cenários conflict e CM, que discutem outros aspectos do comportamento.

Nomear o comparador de 1,71 m: **KOa ou RHM, conforme os dados usados**. “Keep-out-only ablation” é ambíguo porque KOa conserva a camada de inspeção reativa; KOF é a patrulha sem essa camada.

A diferença de 2 cm, acompanhada de p_Holm = 0,42, deve ser descrita como uma diferença pequena observada, sem diferença estatisticamente detectada, e não como equivalência estabelecida.

## 5. R2.8 melhorou, mas ainda conclui mais do que seus registros demonstram

Foi correto reconhecer que silêncio do registro não é um cruzamento geométrico. Entretanto, permanecem:

- “the step does not by itself drive the machine”;
- “shows no boundary chattering”;
- “neither arising from the boundary”.

O intervalo entre transições e a associação com início de eventos não identificam, sozinhos, a causa geométrica de cada transição. Uma transição exigir outras condições do FSM também não torna o salto irrelevante.

**O ponto matemático e o ponto experimental devem ser separados:**

- A equação tem uma descontinuidade em d = R.
- Os registros mostram saltos de campo e intervalos entre transições.
- Sem sincronização com a posição relativa ao evento, não se pode atribuir cada salto ou transição à travessia dessa fronteira.

Uma resposta suficiente pode reconhecer essa limitação, sem prometer uma nova bateria. Sugestão:

> The discontinuity at d = R follows directly from Eq. (3). In a retrospective analysis, we measured steps in the logged field at recorded onsets and the intervals between FSM transitions. These observations characterize the logged response but do not isolate the causal effect of crossing the sensing boundary, because geometric crossings were not recorded synchronously. The shortest transition intervals identified in the dense scenario were associated in the inspected logs with consecutive servicing or goal-abort events. We therefore limit our statement to those observations and do not claim that the analysis rules out boundary-induced chattering in general.

Se mantiver “approximately 38 s”, esclarecer que é uma duração calculada para uma condição inicial específica, não um atraso universal do logger. A intensidade inicial e renovações do campo alteram essa duração.

Há ainda uma questão de descrição a verificar: “recorded only while it exceeds ε” e “last recorded magnitude is exactly ε” precisam ser conciliadas com arredondamento, comparação inclusiva ou ordem de registro. Só detalhar o que a implementação realmente faz.

## 6. Denominadores: a pendência anterior permanece

A abertura informa:

- 130 tentativas novas;
- 127 execuções válidas;
- três execuções imóveis.

R3 minor 2 continua mencionando “the two new heuristic blocks in default and conflict at n = 9”, sem enumerar os grupos afetados.

Já R2.3 informa dez execuções para o método e HEU-sel em default e conflict. Isso pode estar correto se as exclusões forem de outros grupos, mas a redação atual não permite verificar.

**Substituir a expressão ambígua pela lista nominal configuração–cenário e respectivo n**, ou remeter a uma tabela que enumere tentativas, válidas e exclusões. As três exclusões precisam ser contabilizadas sem inferência do leitor.

Trocar também “raises every completeness figure” por “raises the completeness estimates for the affected groups”.

Não apresento números substitutos porque a carta não permite identificá-los com segurança.

## 7. Pendências anteriores ainda presentes nas respostas

| Local | Pendência | Ajuste objetivo |
|---|---|---|
| R2.4 | “three comparisons” não esclarece o total de testes se há vários desfechos. | Identificar os três contrastes, os desfechos e o conjunto ao qual Holm foi aplicado, com remissão à tabela. |
| R2.5 | Boa análise da confirmação, mas não responde explicitamente à generalidade de dois níveis de ruído e um cenário denso. | Acrescentar a restrição das alegações de robustez e a localização das limitações remanescentes. |
| R2.5 | “reproduces 4/9 … validates the procedure” é forte demais. | “provides an internal consistency check at the original threshold”. |
| R2.6 | “changes nothing measurable”, “plateau … cliff” a partir de três valores e p = 0,39. | Relatar ausência de diferença detectada no contraste inferior e a diferença observada no superior, sem caracterizar uma curva geral. |
| R2.6 | Janela de 69,5 s não define início e término. | Dizer se começa na primeira detecção, na última observação ou em outro evento; explicitar eventual renovação do canal. |
| R2.6 | “while the robot is in no danger”. | Substituir pela condição geométrica ou de detecção efetivamente medida. |
| R2.10 | Discute perda de informação, mas não apresenta a sequência que resolve a circularidade. | Explicitar observações/memória → Φ_t → discretização → atualização de Q, sem realimentação de Q para Φ. |
| R2.10 | “cannot support an arbitration policy”. | Limitar a conclusão à incapacidade de distinguir situações agregadas que exigem decisões diferentes segundo a regra proposta. |
| R3.3 | Não apresenta ganhos do APF ou remissão precisa aos valores. | Informar os parâmetros, o procedimento disponível e a tabela/configuração em que estão documentados. |
| R3.3 | “Halving the width changes nothing” e “robust to the width”. | Limitar à ausência de diferença detectada nas duas larguras e no cenário avaliados. |
| R3 minor 3 | Não explica o destino dos resultados de perigo dinâmico e ruído, expressamente mencionados pelo revisor. | Dizer o que foi transferido, o que permaneceu e a razão. |
| Reutilização dos dados | “licensed by … no-ops” apoiado em métricas dentro da faixa anterior. | Descrever o alcance da regressão, evitando apresentá-la como prova completa de ausência de efeito. |

Esses pontos não representam exigências novas desta rodada: constavam da avaliação anterior e permanecem no texto.

## 8. Tom e fechamento editorial

O tom melhorou, e não há motivo para uma reescrita integral. Restam ajustes simples:

- “limitation assumed” → “acknowledged limitation”.
- “both offered the same fork” → “both identified two alternatives”.
- Remover “We do not represent any request as executed when it was not”.
- Retirar “places it in the weakest of them” em R3-Q4. Explicar apenas que o mecanismo não fornece as garantias formais discutidas para os filtros.
- Remover a longa justificativa do lema não adotado em R2.2. A alternativa da nota de projeto já responde ao revisor.
- Retirar “rather than a victory”.
- Acrescentar os números finais de tabelas, figuras e apêndices.

As figuras ainda são uma pendência conhecida. Na versão final, alinhar “were rewritten” com “are being re-rendered” depois de concluí-las e verificá-las. Não afirmar conclusão antes disso.

## 9. Ordem recomendada para a última edição da carta

1. **Substituir a síntese inicial**, incorporando a interpretação atual de R2.3.
2. **Alinhar o encerramento e R3.2** aos limites de atribuição.
3. **Reformular a conclusão de R2.8**, mantendo a análise retrospectiva e sua limitação.
4. **Fechar os denominadores** e a definição da janela de supressão.
5. **Completar as respostas ainda parciais** na tabela da seção 7.
6. Conferir as figuras e inserir as localizações finais após receber a numeração definitiva do manuscrito.

**Conclusão:** não aprovo ainda esta versão para envio, principalmente porque sua síntese contradiz a resposta técnica mais bem revisada. A correção necessária é localizada e não exige reformular novamente o estudo. A carta continuará cobrindo todos os comentários, com uma narrativa única e conclusões proporcionais à evidência.

