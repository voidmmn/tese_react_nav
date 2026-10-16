# Verificação final — manuscrito (10) e carta de resposta (4)

**Data:** 16 de outubro de 2026.  
**Arquivos examinados:** manuscrito com sufixo `(10)`, 24 páginas; `response_to_reviewers_46291(4).md`.  
**Escopo:** fechamento das pendências do parecer sobre a versão (9), consistência entre manuscrito e carta e avaliação do tom da resposta. Não houve reexecução de testes nem auditoria dos CSVs ou do histórico do repositório.

## Veredito

**A revisão funcionou. O corpo do manuscrito resolveu os seis pontos principais da rodada anterior.** A carta tem tom respeitoso, tecnicamente responsável e compatível com uma ressubmissão: reconhece limitações, explica as decisões e não promete um benefício que os experimentos não demonstraram.

Ainda faria uma edição curta de sincronização antes de enviar o conjunto. A carta conservou duas formulações antigas importantes, e uma legenda do manuscrito ainda mantém a alegação temporal mais forte que o texto principal acabou de limitar. Isso não exige novos experimentos nem reformulação da contribuição.

Minha recomendação é **favorável ao encaminhamento após os ajustes localizados abaixo**, dentro do escopo desta conferência. Isso não é uma previsão de aceitação editorial.

## 1. Fechamento do parecer anterior

| Item | O que encontrei agora | Avaliação |
|---|---|---|
| R1 — classificação da família estatística | Contribuição 2, métodos, §V, título da Tabela 5 e apêndice passaram a apresentar uma família primária com desfechos retrospectivos. A p. 11 distingue claramente multiplicidade, escolha retrospectiva e registro público. | Resolvido no enquadramento. Resta sincronizar a cronologia na legenda e na carta, conforme item 2.1. |
| R2 — investigação por execução versus por episódio | §V-F, p. 16: tempo **total por execução**, mediana 35,1 → 26,6 s; o mecanismo é apresentado como interpretação, e os agregados não são tratados como medida da duração de episódios. | Resolvido no artigo. Uma frase antiga permanece em R3.3 da carta. |
| R3 — distâncias das inspeções rejeitadas | §V-I, p. 17: seis rejeitadas em 3,33–3,56 m; 21 creditadas em 1,83–3,30 m; confirmação quando a distância é no máximo 3,3 m. R2.5 da carta acompanha esses valores. | Resolvido quanto à consistência interna e entre os documentos. |
| R4 — hand-off incondicional | Algoritmo 1, p. 7: retirada condicionada à habilitação; delegação condicionada ao keep-out; interrupção de novas publicações sem apagar a memória do canal. | Resolvido. |
| R5 — fronteira não instrumentada | §V-I, p. 18: o texto reconhece que os registros não estabelecem se houve cruzamento coincidente com os eventos. R2.8 da carta mantém essa limitação. | Resolvido. |
| R6 — horizonte de 400 s e falso máximo de 372 s | §V-F, p. 15: o horizonte é definido como censura da métrica, distinguido do orçamento da execução; o texto reconhece missões superiores a 400 s. | Resolvido quanto à justificativa operacional. Há uma ressalva de redação temporal no item 2.1. |

Os ajustes menores também aparecem: “two of the five”, a legenda qualificada da Figura 5, a descrição limitada da variação de histerese e a remoção da duplicação de `n` na Tabela 6. A Tabela 3 distingue as alterações de HEU e HEU-sel. Não recomendo reabrir esses pontos.

## 2. Ajustes que eu faria antes do envio

### 2.1. Usar a mesma cronologia no artigo e na carta

**Este é o principal ajuste restante.**

A p. 11 do manuscrito agora diz exatamente o que o registro apresentado demonstra: o commit com os contrastes precede o primeiro arquivo de resultados arquivado em aproximadamente uma hora, sem extrapolar essa ordenação para afirmar ausência de dados ou de execuções anteriores.

Entretanto, ainda aparecem:

- **Legenda da Tabela 5, p. 12:** “The contrasts were fixed before the runs”.
- **Carta, R2.4:** “The three contrasts were specified before the battery produced any data”.

Essas frases são mais fortes que a formulação corrigida da p. 11. Não estou questionando novamente os contrastes nem pedindo outra análise: basta propagar a mesma descrição documental.

**Substituição sugerida para a legenda da Tabela 5:**

> The analysis-plan commit containing the three contrasts precedes the first archived result file, as detailed in Section V; the five outcomes were selected retrospectively. Holm adjustment addresses multiplicity within this reported family and does not make outcome selection prospective.

**Substituição sugerida para o início de R2.4 da carta:**

> Section V distinguishes the documented timing of the contrasts from the retrospective selection of outcomes. The released analysis-plan commit containing the three contrasts precedes the first archived result file by about an hour. We limit the chronology claim to that documented ordering. The five outcomes were selected after the runs; the fifteen tests are therefore reported as a primary comparison family with retrospectively specified outcomes, rather than as a confirmatory family. Holm adjustment addresses multiplicity within this reported family; it does not remove the limitations of retrospective outcome selection.

No mesmo ajuste, conferir as expressões “declared before execution” em G2, “declared the scenarios before running” em R2.3 e “declared in the analysis plan before the battery” na p. 15, sobre o horizonte de 400 s. **Elas podem permanecer se houver evidência independente da anterioridade que afirmam.** Se estiverem apoiadas somente no mesmo commit anterior ao primeiro CSV, usar “specified in the analysis plan”, sem acrescentar uma anterioridade à execução que esse registro sozinho não comprova. Isso é uma única padronização temporal, não quatro novas pendências científicas.

Não é necessário renomear `familia_confirmatoria.csv`: um nome histórico de arquivo não transforma a análise em confirmatória, e preservar a referência ao artefato pode ser útil à rastreabilidade.

### 2.2. Corrigir “shortened episodes” em R3.3 da carta

O artigo corrigiu a métrica, mas a carta ainda diz:

> “…raised the counted route deviations from 4 to 8 (p = 0.0003) and shortened episodes…”

Isso volta a converter tempo total por execução em duração de episódios. A correção é direta:

> Shifting the entry point increased the median number of route deviations from 4 to 8 (p = 0.0003) and reduced the median per-run total time spent in Investigate from 35.1 to 26.6 s (p = 0.0003), while credited inspections remained three out of three. These aggregate measures do not establish that individual episodes became shorter.

É uma pendência de sincronização da carta. A formulação correspondente no manuscrito está aceita.

### 2.3. Retirar “single factor” da descrição geral da nova bateria na carta

Em **Global changes → New evaluation**, ainda consta:

> “…one row per configuration, with the single factor it changes…”

HEU altera gatilho e seleção. A Tabela 3 já esclarece isso. Substituir por:

> …one row per configuration, listing the settings that differ from the proposed layer, the scenario, and the attempted/valid run counts…

Essa correção preserva a distinção entre o contraste de seleção HEU-sel e o supervisor HEU.

## 3. Pequenos ajustes editoriais recomendados na carta

Não são novos impedimentos metodológicos, mas tornam a resposta mais precisa.

| Localização | Ajuste |
|---|---|
| R3.2, p-valores | Usar `p_Holm = 0.4194` para distância e `p_Holm = 0.0021` para duração, acompanhando a Tabela 5. Os atuais 0,42 e 0,002 são arredondamentos, não resultados contraditórios; a padronização é especialmente útil porque R2.4 afirma que a precisão foi uniformizada. |
| R2.3, bloco `adverse` | Evitar sugerir que as contagens de inspeção variam dentro de todos os três grupos. O manuscrito informa 9/10 execuções com cinco inspeções para o proposto, 10/10 para HEU e 8/10 para HEU-sel. Repetir esses números é mais claro. |
| Introdução, definição de “implemented” | A definição atual limita o rótulo a mudanças de código ou experimento, embora ele também seja usado para alterações documentais. Usar “a manuscript, code, experiment, or analysis change was made”. |
| R2.4, coluna “published” | Verificar se esses valores chegaram efetivamente à versão submetida aos revisores ou se estavam apenas em versões de trabalho desta revisão. No segundo caso, usar “previous draft” e distinguir correção interna de correção de uma afirmação que o revisor recebeu. Não afirmo qual foi o caso sem o histórico correspondente. |

Para o trecho `adverse`, uma redação pronta é:

> All three configurations reached a median of five credited inspections. The proposed layer completed all five in 9/10 runs, HEU in 10/10, and HEU-sel in 8/10. Inspection counts therefore varied within the proposed and HEU-sel groups, whereas HEU inspected all five in every run.

## 4. Tom e atendimento aos revisores

**O tom está adequado.** Não identifiquei hostilidade, recusa evasiva ou promessa experimental incompatível com o reposicionamento adotado. Estão especialmente bem resolvidos:

- A escolha explícita pela alternativa de rebaixar a atualização de valor, sem apresentá-la como responsável pelas ações executadas.
- A separação entre ausência de diferença detectável e equivalência demonstrada.
- O reconhecimento de que o contraste de gatilho não isola a persistência como fator único.
- A atribuição da folga no perigo estático ao keep-out e da inspeção à camada reativa.
- A explicação de que a confirmação é pontuação posterior, permitindo re-scoring.
- A explicitação do custo da precedência e dos limites da análise de fronteira.

Nas respostas examinadas, os comentários estão encaminhados por alteração, análise adicional ou delimitação explícita do escopo. Não encontrei uma nova demanda experimental necessária para fechar as pendências da rodada anterior. A eventual satisfação editorial com esse escopo permanece decisão dos revisores.

A carta é longa, mas organizada por comentário. Não a reescreveria inteira apenas por estilo. Também não acrescentaria novos experimentos para reforçar uma resposta que já aceita corretamente uma limitação.

## 5. Apresentação do PDF

Conferi as 24 páginas renderizadas e ampliei o algoritmo e as tabelas principais. Não identifiquei sobreposição ou corte que inviabilize a leitura desses elementos. O algoritmo atualizado está íntegro.

A p. 24 contém apenas a biografia do segundo autor e grande área em branco. **É um ajuste opcional de paginação**, especialmente porque houve comentário sobre extensão: se for simples acomodar as biografias, vale fazê-lo sem comprimir artificialmente texto ou tabelas. Não considero isso um impedimento científico.

## Encerramento

**Estamos na fase de sincronizar o pacote de submissão.** Eu fecharia os pontos científicos desta rodada e faria apenas os três ajustes da seção 2, acompanhados da revisão editorial curta da seção 3. As pendências restantes são frases antigas e precisão documental; não representam uma nova falha experimental causada pelas correções.
