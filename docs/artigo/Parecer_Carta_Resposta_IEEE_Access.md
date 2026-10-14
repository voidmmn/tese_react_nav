# Parecer sobre a carta de resposta aos revisores

**Manuscrito:** Access-2026-33687, identificador informado na carta.  
**Data:** 12 de setembro de 2026.  
**Documentos examinados:** `author_response.md`, `comentarios dos revisores(1).txt` e a versão final disponível do artigo, arquivo com sufixo `(6).pdf`.

**Parecer:** a carta tem boa estrutura, responde aos itens numerados dos quatro revisores e apresenta corretamente o reposicionamento central do trabalho. Entretanto, **recomendo corrigir algumas afirmações antes de enviá-la**, porque descrevem mudanças que não estão no artigo ou ampliam o alcance dos resultados. Os problemas mais importantes estão na resposta sobre a Eq. (3), na distinção entre remover ηΦ e desligar Q, e na descrição dos testes estatísticos.

Esta avaliação é da carta. **Os achados abaixo não exigem novos experimentos nem reabrem a avaliação metodológica já encerrada.** São principalmente divergências entre a resposta e o material final. As referências de página usam a numeração impressa do PDF `(6)`; se houver uma versão posterior, as localizações deverão acompanhar essa versão.

## 1. O que está bem resolvido

A carta reconhece expressamente que Q não controla o robô, explica que o mecanismo executado é a supervisão reativa integrada ao Nav2 e não tenta defender a modulação de valor como uma política aprendida já validada. Também reconhece limitações relevantes: simulação, inspeção como proxy, ausência de baseline heurístico com o mesmo controlador e ausência de comparação com uma política aprendida atuante.

Os principais números citados correspondem ao artigo:

| Informação da carta | Conferência no artigo |
|---|---|
| 160 tentativas, 154 válidas, 6 imóveis; 96,25% | Correto como proporção de tentativas que satisfizeram o critério de movimento. Seção V, p. 9. |
| E1: aproximadamente 320 s e 80,4 m; E3: 364 s e 86,6 m | Correto. Tabela 5, p. 11; Seção V-E, p. 12. |
| E5: aproximadamente 397 s, 92,2 m e inspeção completa em 9/10 | Correto. Tabela 5 e Seção V-F, pp. 11 e 13. |
| N2: inspeção completa em 4/9 | Correto. Tabela 8 e Seção V-H, p. 13. |
| RHM: distância mínima de 1,71 m; RHB: 0,71 m | Correto. Seção V-B e Tabela 6, pp. 10–11. |
| DHa versus DHb: aproximadamente +0,33 m de distância mínima | Correto para o ensaio dirigido, com as limitações declaradas. Seção V-C e Tabela 10. |
| 21 referências e tabela comparativa | Correto para a versão examinada. Tabela 1, p. 4; referências, p. 15. |
| Separação entre investigação iniciada e inspeção confirmada | Compatível com a Seção III-C, p. 6, e com a descrição da auditoria, p. 9. |

A decisão de dizer claramente o que foi implementado e o que permaneceu como limitação é adequada. O ajuste necessário é fazer essa distinção funcionar em todos os parágrafos, inclusive na introdução.

## 2. Correções prioritárias

### A. A carta diz que a descontinuidade da Eq. (3) foi removida, mas ela permanece

**Local:** resposta 2.m1; resposta aos pontos menores do Revisor 4, que remete a ela.

**Trecho problemático:** “The intensity profile now tapers continuously toward R, removing the discontinuity”.

**O artigo final diz:** na p. 5, Eq. (3), a intensidade é

\[
i_e(d)=I_e\left(1-\frac{d}{2R}\right),\quad d\leq R.
\]

Portanto, em `d = R`, ela ainda vale `I_e/2`. O texto reconhece expressamente o salto na fronteira e apresenta a histerese, os limiares distintos e o compromisso com o episódio como explicação para evitar disparos repetidos. **Não houve a alteração do perfil que a carta anuncia.**

Esta é a divergência mais direta e deve ser corrigida na carta. Não recomendo mudar o modelo para torná-lo compatível com essa frase.

**Substituição sugerida para 2.m1:**

> The range-dependent intensity profile is retained: Eq. (3) gives an intensity of I_e/2 at d = R, and the event is no longer reported beyond R. We now explicitly acknowledge this boundary discontinuity and explain the roles of the distinct enter/exit thresholds and episode commitment in preventing repeated reactive transitions. We also report sensitivity to event-position and intensity noise. We have not performed a dedicated detection-radius sweep and do not claim that the intensity profile itself is continuous at R. See Section III-B, p. 5, and Section V-H, p. 13.

Para os pontos menores do Revisor 4, basta remeter a essa resposta corrigida e dizer que a descontinuidade foi **explicada**, não removida.

### B. η = 0 não significa “sem Q”

**Locais:** respostas 2.1, 2.5 e 4.2; resumo de ablações. A expressão “no-value” na resposta 4.2 é especialmente imprecisa.

O experimento E0 zera o termo externo `ηΦ`, mas mantém o componente TD e a tabela Q. Isso é explícito na Seção III-B, p. 6, e na Tabela 5, p. 11. O código já auditado também mantém a atualização por transição observada.

A ablação responde diretamente ao pedido do Revisor 4 de testar `η=0`. **Não é literalmente um ensaio com o nó Q removido**, como os itens 2.1 e 2.5 podem fazer parecer. A ausência de influência de Q na navegação é estabelecida pelo fluxo de controle; a ablação confirma a ausência de efeito comportamental do termo afetivo nos resultados observados.

Há uma segunda frase a ajustar em 2.1: “the greedy action is computed but never sent to the base”. Na implementação corrigida examinada, a ação que indexa a atualização é inferida da odometria. Não é preciso afirmar que uma ação greedy é calculada. Isso também pode confundir o máximo sobre ações no alvo TD com seleção de ação para execução.

**Substituição sugerida para o núcleo de 2.1:**

> Q does not select executed actions. The action associated with each observed transition is inferred from odometry, while motion is generated by Nav2/MPPI toward patrol, inspection, or retreat goals. No exploration policy acts on the robot, and the discrete Q-table actions are not mapped to velocity commands. The table is updated from consecutive odometry observations. E0 retains Stay Alert and sets η = 0, removing the affective value term while retaining the passive TD update. Thus, E0 is an ablation of ηΦ, not a separate experiment with the Q node disabled. The absence of a Q-to-control connection explains why the value table cannot drive the reported navigation behavior. See Section III-B, p. 6, and Tables 5 and 10.

**Para 4.1:** a frase “Implemented exactly as suggested” é defensável quanto ao pedido específico de `η=0`; pode ser mantida se a continuação descrever precisamente esse experimento.

### C. A descrição estatística precisa preservar o alcance de cada método

**Locais:** respostas 1.2, 2.3 e 2.7; resumo final.

Há quatro ajustes distintos:

1. **“Welch’s t-test is removed” é amplo demais.** Os testes de diferença foram substituídos por Mann–Whitney/permutação, mas a função `tost` do script de análise utiliza dois testes unilaterais com erro-padrão e graus de liberdade de Welch. Não há contradição em usar métodos diferentes para perguntas diferentes; a carta precisa explicá-lo.
2. **“E0 equivalent to E3 by TOST” precisa dizer “mission time”.** A Tabela 10, p. 16, testa equivalência de tempo com margem ±5 s. Para o número de inspeções, os dois grupos têm valores observados idênticos, e a tabela apresenta `n/a` para o TOST. O teste não demonstra equivalência global de trajetórias, segurança ou todos os comportamentos.
3. **O IC bootstrap é da diferença de médias Δ.** As Tabelas 4 e 10 apresentam δ de Cliff separadamente. A carta não deve deixar o leitor entender que os intervalos são de δ.
4. **Holm se aplica à família principal de sete comparações.** Os resultados secundários e o ensaio dirigido não devem parecer integralmente corrigidos por Holm. A Tabela 10 identifica as comparações exploratórias do perigo emergente como não corrigidas.

A palavra “pre-declared” para a família de comparações deve ser usada somente se os autores tiverem documentação de quando essa definição ocorreu. O manuscrito identifica a família principal, mas isso, por si só, não comprova pré-especificação anterior à observação dos resultados. Não estou afirmando que houve seleção posterior; recomendo apenas não anunciar uma cronologia que a carta não documenta.

**Substituição sugerida para 1.2:**

> The former Welch difference tests were replaced by Mann–Whitney U tests, using the exact U distribution for untied small samples, exact permutation p-values for fully separated constant groups, and the tie-corrected normal approximation for other tied samples. Tables 4 and 10 report the mean difference Δ, Cliff’s δ, and a 95% bootstrap confidence interval for Δ. Holm correction is applied to the seven principal comparisons in Table 4. Secondary comparisons are reported separately in Appendix B; the directed emerging-hazard comparisons are exploratory and are not Holm-corrected. For the η ablation, mission-time equivalence is assessed with a Welch-based TOST within a ±5 s margin. Constant inspection counts are described as identical observed outcomes, not as TOST-established equivalence. Per-mission completion rates are accompanied by Wilson-score intervals.

**Substituição sugerida para 2.3:**

> We adopt option (b): the η sweep is interpreted as a numerical analysis of the passive value table. Q and η have no connection to executed control. E0 and E3 have identical observed inspection counts, and their mean mission times are equivalent within the ±5 s TOST margin reported in Table 10. This does not establish equivalence of every behavioral metric or trajectory. We did not conduct a full FSM × value-update factorial experiment; instead, we document the control architecture and report the targeted η = 0 ablation. See Section III-B, p. 6, Section V-E, p. 12, and Appendix B.

O valor de `pTOST` da comparação E0/E3 aparece arredondado como `4×10⁻⁷` na Tabela 10. Não é necessário dar mais casas decimais na carta.

### D. A Figura 7 agrega E3, não toda a bateria

**Locais:** respostas 1.4, 2.4 e 3.3.

“Across all runs” é ambíguo: pode ser entendido como todas as 154 execuções válidas. A legenda e a Seção V-G, p. 13, especificam **todas as dez execuções válidas de E3**. A faixa é o percentil 2,5–97,5 entre execuções após reamostragem em tempo normalizado, **não um intervalo de confiança da média**.

A resposta 1.4 também deve abordar explicitamente a sugestão de comparação com Q tabular convencional: E0 fornece o braço sem o termo afetivo e a Tabela 5 reporta os resíduos, mas não há ali uma comparação entre duas políticas Q atuantes.

**Substituição sugerida para 1.4:**

> We now report the complete update residual |αδ + ηΦ|, which includes the affective contribution. Figure 7 aggregates all ten valid E3 runs after resampling their time series onto a common normalized mission-time grid. It shows the across-run mean and the 2.5th–97.5th percentile band, representing inter-run spread rather than a confidence interval for the mean. Table 5 also reports the residual for E0, where η = 0 and the passive update has no affective term. This is not a comparison between learned policies controlling the robot. We interpret the results as empirical stability of finite-run increments and make no formal convergence claim. See Section V-G, Figure 7, p. 13, and Table 5, p. 11.

As respostas 2.4 e 3.3 podem remeter a esse texto, repetindo apenas “all ten valid E3 runs” para evitar a ambiguidade.

### E. Proveniência, imobilidade e os timeouts antigos precisam ser descritos separadamente

**Locais:** parágrafo inicial “Evaluation battery”, resposta 2.7 e resposta 2.m5.

“Single uniform battery” pode sugerir que todas as 160 tentativas foram coletadas sob o mesmo código corrigido. A p. 9 registra outra história: E5, DHa e DHb foram recoletados, enquanto as outras treze configurações foram reutilizadas. O manifesto documenta essa correspondência. O protocolo consolidado tem 16 configurações, mas a coleta não foi um único lote integralmente novo.

Além disso, o artigo diz que as seis execuções imóveis são **compatíveis com** falha de inicialização, sem certificar a causa de infraestrutura. A carta começa chamando-as diretamente de “startup failures” e só depois ressalva a causalidade. A redação deve ser consistente desde o início.

Por fim, **154/160 é a proporção que satisfez o critério de movimento**, não a taxa de missões integralmente bem-sucedidas. Usar “mission reliability” sem essa definição pode confundir movimento, conclusão da patrulha e inspeção completa.

**Substituição sugerida para “Evaluation battery”:**

> The revised evaluation comprises 16 configurations with ten attempted runs each (160 attempts). Of these, 154 met the published movement criterion for behavioral analysis and six remained immobile, giving a movement-qualified fraction of 96.25% and valid sample sizes of 8–10 per configuration. E5, DHa, and DHb were rerun after corrections to hazard activation and failure handling; the other thirteen configurations were retained, with their provenance and checksums documented in the release manifest. Immobility is consistent with an initialization failure, but its infrastructure cause is not independently certified by the published logs. The archived package is identified by tag v1.0-resubmission and commit 8ed48680d1c15fe5ac5e1326499e8b4f0e269bf4.

O pedido 2.7(f) se refere a **dois timeouts da submissão original**. Os seis imóveis da bateria revisada não devem ser apresentados como se fossem exatamente aqueles dois casos. A resposta atual não fornece literalmente a análise com/sem os dois timeouts antigos. Ela apresenta outra estratégia para a bateria revisada — isso é explicável, mas precisa ser declarado.

**Substituição sugerida para o trecho 2.7(f):**

> Regarding (f), we do not present a with/without sensitivity reanalysis of the two timeout runs from the original submission. The revised results use the corrected evaluation battery described in Section IV-D. For this battery, we report performance conditional on the movement criterion separately from the six immobile attempts. These six cases are not identified as the two original mid-mission timeouts. Their observable exclusion criterion and per-run records are provided, and the 154/160 movement-qualified fraction is reported separately from inspection completion and navigation performance. See Section V, p. 9, and Section V-I, p. 14.

Isso substitui a formulação excessivamente conclusiva “All six are addressed” por uma resposta explícita sobre o que mudou e o que não foi executado literalmente.

Em 2.m5, especifique que as sementes registradas se referem ao gerador de ruído de percepção por repetição. O artigo também reconhece variação de física e temporização; a carta não deve sugerir que todas as fontes de aleatoriedade são controladas por uma única semente.

### F. A numeração das equações ainda é a da versão antiga

**Locais:** respostas 2.8 e 2.m2, resposta 4.3 e resumo “Definitions”.

Os comentários dos revisores naturalmente mencionam a antiga Eq. (4). Entretanto, ao descrever o manuscrito revisado, a carta precisa usar:

| Conteúdo atual | Localização no PDF `(6)` |
|---|---|
| Acumulador do canal de perigo | Eq. (4), p. 5 |
| Seleção/acumulador de atração e desempate | Eq. (5) e texto adjacente, p. 5 |
| Decaimento | Eq. (6), p. 5 |
| Leitura do campo com precedência do perigo | **Eq. (7), p. 5** |
| Equivalência algébrica com aumento da recompensa | Eq. (8), p. 5 |

**Formulação sugerida para 2.8:**

> The original signed-selection rule has been replaced by the two-channel formulation in Eqs. (4)–(7). Equation (7) gives the hazard channel precedence whenever h > ε; this residual condition is distinct from the FSM threshold Φ ≤ −θ_in and its additional conditions for entering Avoid. The selection and tie-breaking rule for attraction events is specified with Eq. (5), and Eq. (6) describes decay. See Section III-B, p. 5, and Section III-C, p. 6.

Preserve a antiga numeração **dentro do comentário original**; nas respostas, escreva “formerly Eq. (4), now Eqs. (4)–(7)” quando isso ajudar o revisor.

### G. A justificativa para não incluir políticas aprendidas está defensiva e especulativa

**Local:** resposta 2.5.

**Trecho:** “a genuinely learned reactive navigator would be under-trained here and uninformative”.

A carta não apresenta um treinamento que sustente essa previsão. Além disso, a frase pode soar como desqualificação do experimento solicitado. A razão suficiente já está no próprio trabalho: ele não implementa uma política Q atuante e foi reposicionado como integração de supervisão reativa.

**Substituição sugerida para a parte relativa aos baselines ausentes:**

> We have not included an actuating reward-augmented Q-learning baseline or a recent learned reactive navigator. Implementing and training such policies is outside the revised experimental scope, which evaluates reactive supervision rather than learned action selection. We therefore make no claim of superiority over these missing baselines. The APF comparison evaluates the released APF implementation, which differs in controller and approach parameters. A heuristic supervisor using the same Nav2/MPPI controller to isolate the contribution of affective weighting also remains an explicit limitation. See Section V-E, p. 12.

Também vale substituir em 2.2 “We removed the reward component” por **“We removed the affective component from the reward, retaining the progress reward”**. A redação atual pode sugerir, desnecessariamente, que toda a recompensa foi removida.

## 3. Ajustes de precisão e apresentação

### 3.1. Os comentários estão resumidos, não integralmente transcritos

A introdução afirma “each reviewer comment is quoted”. Vários blocos, porém, condensam ou reformulam o original, além de usar reticências. Por exemplo, 2.7 transforma os pedidos em expressões abreviadas; 1.4 combina uma paráfrase com o pedido sobre Q tabular.

Use uma destas duas soluções: reproduzir fielmente os comentários ou identificar todos os blocos abreviados como **“Comment summary”**, sem aspas de citação literal. A segunda exige menos trabalho e preserva a estrutura atual.

**Introdução sugerida:**

> Below, we provide a condensed summary of each numbered comment, followed by our response. We distinguish experimental changes, revisions to the interpretation of the results, and limitations that remain outside the revised scope. Where a requested experiment was not performed, we state this explicitly.

Na primeira apresentação do trabalho, substitua “added the ablations, baselines, safety scenarios, statistics, and literature requested” por **“added targeted ablations, an APF baseline, safety scenarios, revised statistical analyses, and an expanded literature discussion”**. Isso evita prometer atendimento integral antes de explicar as exceções.

### 3.2. Acrescente localizações no manuscrito

Hoje a carta remete com frequência a outras respostas, mas raramente ao artigo. Isso dificulta conferir se a mudança existe. Uma linha “Changes in manuscript” após cada resposta é suficiente; não é necessário fornecer números de linha inexistentes.

| Respostas | Localizações úteis no PDF `(6)` |
|---|---|
| 1.1; 2.1–2.3; 3.1; 4.1 | Resumo, p. 1; contribuições, p. 2; Seção III-B, pp. 4–6; Seção V-E, p. 12. |
| 1.2; 2.7 | Seção V, pp. 9–10; Tabela 4, p. 11; Apêndice B, pp. 14–16; Tabela 10, p. 16. |
| 1.3; 2.9 | Seções V-F e V-H, p. 13; Tabela 8, p. 13; ameaças à validade, p. 14. |
| 1.4; 2.4; 3.3 | Seção V-G e Figura 7, p. 13; Tabela 5, p. 11. |
| 1.5; 2.10 | Seção II, p. 3; Tabela 1, p. 4; referências, p. 15. |
| 1.6 | Seção V-E, p. 12; Tabelas 4, 5 e 10. |
| 2.5; 4.2 | Tabelas 3 e 5, pp. 9 e 11; Seção V-E, p. 12. |
| 2.6; 3.2; 4.3 | Seções V-B–V-D, pp. 10–12; Tabelas 6, 7 e 10. |
| 2.8; 2.m1–2.m3 | Seções III-B e III-C, pp. 5–6; auditoria na Seção IV-D, p. 9. |
| 2.m4 | Seção IV-C, p. 8, e legenda da Tabela 5, p. 11. |
| 2.m5 | Seção IV-D, pp. 8–9; Tabela 3, p. 9. |
| 2.m6; pontos menores do Revisor 4 | Cabeçalho/rodapé do artigo; agradecimentos, p. 15. |

### 3.3. Fortaleça a resposta 1.6 com o resultado que já existe

O revisor pediu uma leitura operacional do custo. A Seção V-E já fornece aproximadamente **2 m adicionais e 15 s adicionais por anomalia inspecionada**. Acrescente isso à carta, deixando claro que é a razão entre o custo adicional E3–E1 e as três inspeções adicionais; não é uma medição isolada do tempo de permanência em cada alvo.

> Relative to E1, E3 adds approximately 6.2 m and 44 s for three additional inspections, corresponding to about 2 m and 15 s per additional inspected anomaly. These are aggregate marginal mission costs, not measurements of per-target dwell duration. See Section V-E, p. 12.

### 3.4. Use o mesmo denominador ao apresentar ruído

Em 1.3, “3/3” conta alvos, enquanto “4/9” conta missões. Ambos os números são verdadeiros, mas compará-los diretamente pode sugerir queda de 100% para um denominador de nove alvos.

Prefira:

> All three anomalies were inspected in 10/10 valid moderate-noise runs; under high noise, all three were inspected in only 4/9 valid runs.

### 3.5. Preserve os qualificadores das métricas de segurança

Nos trechos 2.6 e no resumo final, prefira **“no entries into the simulated contact region were observed in the valid runs”** a “zero collisions everywhere”. O artigo define colisão como distância centro a centro inferior a 0,5 m, não contato físico medido por sensor.

Na descrição do ensaio DHa/DHb, pode acrescentar que ele é dirigido e exploratório, que os grupos têm 8 e 10 execuções válidas e que o ganho de +0,33 m foi acompanhado de maior tempo/distância e adiamento da inspeção. Se mencionar TTC nesse ensaio, mantenha a interpretação de mínimo ao longo da missão; não o apresente como uma estatística exclusivamente pós-ativação.

Essas qualificações já estão no artigo e protegem a correspondência entre os dois documentos.

### 3.6. Ajuste o tom sem mudar a posição científica

“Exceptionally careful” pode ser reduzido a “careful”. “Limitation assumed” fica mais natural como **“acknowledged limitation”**. “To be candid” e repetições de “honestly” podem ser omitidas: a precisão das respostas já comunica transparência.

Na resposta 2.10, não dê a entender que toda formulação equivalente a “to our knowledge” foi eliminada: a p. 3 ainda contém “Within this scope, we are not aware of a prior method…”. Melhor afirmar que a formulação de novidade foi **delimitada ao escopo e contextualizada pela revisão ampliada**.

Os placeholders estão efetivamente zerados no PDF. Isso pode ser informado como preparação de rascunho; não demonstra, por si só, cumprimento de todas as exigências de produção editorial da revista. Esta conferência não auditou as regras atuais do portal de submissão.

## 4. Cobertura dos revisores e decisão

| Revisor | Avaliação da resposta |
|---|---|
| **1** | Os sete pontos têm resposta. Refinar estatística, população da Figura 7, comparação com E0 e denominadores; acrescentar o custo marginal já publicado. |
| **2** | Os dez pontos maiores e seis menores estão representados. Corrigir as divergências objetivas em 2.m1, 2.1, 2.3, 2.7 e 2.8; tornar explícitas as limitações em 2.5 e o tratamento diferente do pedido sobre timeouts antigos. |
| **3** | Os três pontos estão respondidos. Precisar o conjunto E3 na estabilidade e usar as mesmas qualificações de segurança do artigo. |
| **4** | Os três pontos maiores e o bloco de pontos menores estão cobertos. Preservar a distinção ηΦ/Q, atualizar a numeração das equações e corrigir a remissão sobre a descontinuidade. |

**A carta está próxima da versão de envio, mas eu não a enviaria exatamente como está.** Corrigir as afirmações acima é importante porque um revisor pode consultar a Eq. (3), a legenda da Figura 7 ou a Tabela 10 e encontrar imediatamente algo diferente do que a resposta anuncia.

Essas divergências foram identificadas na carta fornecida agora; não constituem evidência de regressão no artigo final. A recomendação anterior sobre o manuscrito permanece: os ajustes desta tarefa são de fidelidade documental, clareza e rastreabilidade da resposta.

O arquivo `author_response.md` recebido foi preservado. As redações em inglês neste parecer são propostas prontas para substituir os trechos correspondentes.
