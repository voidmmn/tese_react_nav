# Parecer final — sétima rodada de avaliação

**Artigo:** *A Two-Layer Deliberative–Reactive Architecture with an Affective Attraction–Repulsion Layer for Autonomous Substation Inspection*  
**Autores:** Milton Miranda Neto e Alexandre Cardoso  
**Versão avaliada:** PDF com sufixo `(6)`, 16 páginas  
**Data:** 11 de setembro de 2026  
**Referência:** parecer da sexta rodada, versão `(5)` e comentários originais dos quatro revisores  
**Natureza:** avaliação técnica independente com critérios pertinentes à revisão científica da IEEE Access; não representa decisão editorial da revista.

**Recomendação final: favorável à submissão. Considero encerradas as correções técnicas exigidas nestas rodadas, dentro do escopo e dos arquivos examinados. Não solicito novas alterações metodológicas, novos experimentos ou outra rodada ampla de avaliação.**

A última incorreção factual apontada na sexta rodada foi corrigida: a análise de ruído agora informa que a distância mínima média ao perigo aumentou de 4,86 m para 5,29 m, em vez de afirmar que permaneceu inalterada. A Figura 5 correta, a distinção temporal de TTC e distância, os denominadores da amostra e a delimitação da auditoria foram preservados. Os ajustes de proveniência e das principais remissões também foram incorporados.

## 1. Escopo da conferência final

Mantive os critérios utilizados anteriormente: contribuição e originalidade, formalização, correspondência com a implementação, inspeção e segurança, desenho experimental, comparadores, estatística, robustez, reprodutibilidade, literatura e apresentação.

Comparei o texto desta versão com o PDF da sexta rodada, examinei as mudanças e conferi visualmente as páginas relevantes, especialmente a Figura 5 e a análise de ruído. As alterações identificadas são localizadas e não modificam a formulação central nem os resultados quantitativos.

O repositório continua no commit **`8ed48680d1c15fe5ac5e1326499e8b4f0e269bf4`**, exatamente o pacote auditado na sexta rodada. Portanto, os 160 CSVs, o código operacional, o analisador estatístico e a auditoria permanecem na mesma versão. [Pacote de referência][repo].

Reaproveitei as verificações das rodadas anteriores sobre esses arquivos inalterados. Não executei novas missões no Gazebo, nem repeti testes isolados de funções que não mudaram. Esta conclusão combina a verificação das correções atuais com a evidência acumulada das rodadas anteriores; não equivale a uma nova execução independente de toda a bateria.

As páginas citadas referem-se ao PDF `(6)`, de 16 páginas.

## 2. Encerramento das pendências da sexta rodada

| Item anterior | Conferência nesta versão | Resultado |
|---|---|---|
| Distância mínima chamada de “unchanged” sob ruído | P. 13 informa aumento de 4,86 ± 0,03 m para 5,29 ± 0,20 m | **Corrigido** |
| Contatos e afastamento recebiam a mesma interpretação | Texto distingue ausência de contatos observados do aumento de afastamento e nega garantia geral | **Corrigido** |
| PDF chamava o manifesto de registro de “collection commit” | P. 9 usa “reference snapshot for each batch” | **Corrigido** |
| Figura 5 e Tabela 5 remetiam E5 a V-H | Legendas agora remetem a V-F | **Corrigido** |
| Discussão misturava remissões de ruído e densidade | P. 10 distingue V-H para ruído e V-F para densidade | **Corrigido** |
| Legenda da Tabela 6 sugeria keepout posterior ao recuo | P. 11 descreve recuo combinado com keepout persistente acionado por detecção | **Corrigido** |
| Apêndice A mencionava apenas dois cenários | P. 14 informa “all five scenarios” | **Corrigido** |
| Introdução usava “guarantees coverage” | P. 2 passou a “provides coverage” | **Corrigido** |

Não há uma nova contradição equivalente à identificada na sexta rodada. A redação revisada descreve os resultados, em vez de ampliar sua interpretação para uma garantia geral de segurança.

## 3. Correção da análise de ruído

A p. 13 agora é compatível com a Tabela 8 e com os contrastes da Tabela 10:

| Configuração | Inspeções completas por missão válida | Distância mínima média ao perigo |
|---|---:|---:|
| E3, sem ruído | **10/10** | **4,86 ± 0,03 m** |
| N1, ruído moderado | **10/10** | **5,01 ± 0,11 m** |
| N2, ruído alto | **4/9** | **5,29 ± 0,20 m** |

A conclusão adequada é a que o texto agora apresenta: no ruído alto, a completude de inspeção diminui, não são observadas entradas na região de contato, e o afastamento mínimo médio aumenta. Isso descreve a troca observada no ensaio, sem confundir ausência de contato com invariância de todas as métricas de segurança.

O contraste de afastamento E3 → N2 continua sendo aproximadamente **+0,43 m**, com IC de 95% **[0,31; 0,56]**, Cliff’s δ = 1 e p ≈ **2 × 10⁻⁵**. A nova redação não exige modificar qualquer número.

**Encerro a última correção factual obrigatória da sexta rodada.**

## 4. Preservação das correções mais importantes

### 4.1. Figura 5 e resultados de E5

A Figura 5 da p. 10 mantém o painel corrigido. Seu conteúdo gráfico interno é idêntico ao da versão `(5)`, validado na sexta rodada, e continua representando a coleta atual:

- Nove execuções E5 com cinco inspeções e uma com quatro.
- Média de 4,90 inspeções, sem o ponto antigo de três inspeções.
- Duração média de aproximadamente 397,03 s, com intervalo de 385,82 a 401,94 s, sem o ponto antigo de 440 s.

A Figura 5, a Tabela 5 e a discussão de V-F permanecem coerentes. A explicação da falha de E5 repetição 6 também foi preservada: quatro créditos e nenhuma nova tentativa registrada após a falha do alvo restante. As duas reinvestigações observadas em outras execuções não são apresentadas como demonstração de uma política geral de retry.

### 4.2. Distância e TTC no perigo emergente

A p. 11 mantém a separação necessária:

- As métricas publicadas são mínimos acumulados da missão inteira, incluindo o período anterior à ativação.
- Os registros permitem localizar os mínimos finais de distância após a ativação nas 18 execuções dinâmicas válidas.
- A mesma conclusão não é generalizada ao TTC; o texto reconhece que uma execução já registra o mínimo final antes da ativação.

O resultado de aproximadamente **+0,33 m de distância mínima** e **+0,51 s de TTC global** permanece acompanhado dos custos de tempo, deslocamento e adiamento da inspeção. Não foi restabelecida a alegação indevida de um efeito de TTC separadamente calculado após a ativação.

### 4.3. Amostra e auditoria

Os denominadores continuam corretos: **160 tentativas, 154 válidas e seis imóveis**, com n válido entre oito e dez. A fração de tentativas que atende ao critério de movimento é **96,25%**.

A auditoria permanece na versão de **1.537 eventos**, já examinada. Mantêm-se a separação entre posição do alvo e do robô, a distinção dos relógios e os desfechos de investigação e Avoid. A limitação da extração de Avoid ao Stay Alert, sem detalhamento equivalente para APF, continua explícita.

Os três abortos DHa seguidos de saída `safe` não são confundidos com chegada à meta de recuo. As seis rejeições N2 permanecem atribuídas à confirmação por distância, com registros por episódio. [Auditoria de referência][audit].

### 4.4. Código e formulação

Como o pacote não mudou, permanecem os reparos anteriores da ativação ambiental dos perigos, da reinicialização do resultado de navegação entre episódios e da classificação das falhas. A memória dos dois canais, a saturação interna, o decaimento e o conjunto elegível próprio de cada canal continuam descritos.

Não identifiquei regressão introduzida por esta revisão do PDF.

## 5. Avaliação científica consolidada

| Critério | Julgamento final | Limite da conclusão |
|---|---|---|
| Relevância | **Boa** | Problema pertinente à navegação para inspeção de subestações |
| Clareza da contribuição | **Boa** | Contribuição demonstrada é supervisão e integração deliberativa–reativa |
| Originalidade | **Moderada** | A vantagem específica do campo sobre uma heurística com o mesmo controlador não foi isolada |
| Formalização | **Suficiente no escopo** | Não oferece novo operador de aprendizagem nem garantia formal de convergência |
| Correspondência com o código | **Adequada nos pontos auditados** | Não equivale a certificação exaustiva da pilha ROS/Nav2 |
| Desenho experimental | **Adequado ao escopo delimitado** | Cenários escolhidos e amostras pequenas não demonstram generalização ampla |
| Estatística | **Consistente com os dados examinados** | Contrastes exploratórios continuam separados da família confirmatória |
| Inspeção | **Definição clara e auditável** | É proxy de navegação/chegada confirmada, não validação de diagnóstico físico |
| Segurança | **Evidência empírica delimitada** | Contato, afastamento, TTC e saída do supervisor são desfechos distintos |
| Reprodutibilidade | **Boa para dados e episódios examinados** | Proveniência distingue referência pública de execução original de cada lote |
| Apresentação | **Adequada para encaminhamento** | Há detalhes editoriais residuais sem impacto científico |

A ablação η = 0 permanece corretamente interpretada. Como Q não controla as ações executadas, a contribuição não pode ser apresentada como superioridade de uma política aprendida afetivamente modulada. O texto atual reconhece isso no resumo, no método, nos resultados e na conclusão.

A comparação APF, as ablações de keepout/recuo, o conflito e os ensaios de ruído e perigo emergente sustentam uma análise de sistema mais informativa que a comparação original apenas com patrulha fixa. Os limites de comparação continuam assumidos, especialmente a diferença de controlador frente a APF e a ausência de uma heurística equivalente com o mesmo controlador.

Essas limitações são parte do mérito científico que a revista avaliará. Não as converto, nesta conferência final, em novas exigências que ampliariam o escopo depois de concluídas as correções acordadas.

## 6. Atendimento final aos revisores originais

“Atendido no escopo” significa que a objeção foi respondida pela evidência disponível e pela delimitação explícita das alegações. Não significa que tenham sido acrescentadas capacidades que permanecem fora do trabalho.

### Revisor 1

| Comentário | Situação final |
|---|---|
| R1.1 — propriedades teóricas e convergência | **Atendido no escopo:** sem herança indevida de garantias de Q-learning |
| R1.2 — estatística, efeitos e multiplicidade | **Atendido:** métodos, intervalos, denominadores e figuras coerentes |
| R1.3 — robustez | **Parcial, com limites explícitos:** ruído e cenários dirigidos; generalidade ampla não demonstrada |
| R1.4 — resíduo completo e múltiplas execuções | **Atendido para estabilidade empírica:** métrica completa, agregação e processamento disponíveis |
| R1.5 — literatura e comparação | **Atendido na ampliação:** permanece a limitação de originalidade demonstrada |
| R1.6 — custo de inspeção | **Atendido:** tempo, distância e adiamento discutidos |
| R1.7 — alinhamento do resumo | **Atendido:** mecanismo atuante e alcance das evidências claros |

### Revisor 2 — comentários maiores

| Comentário | Situação final |
|---|---|
| R2.1 — papel de Q e ablação | **Atendido no reposicionamento:** ações comandadas pelo supervisor; ablação explícita |
| R2.2 — reward shaping e dupla contagem | **Atendido:** equivalência e limite da novidade reconhecidos |
| R2.3 — significado da varredura de η | **Atendido no escopo:** análise numérica, sem política aprendida atuante |
| R2.4 — estabilidade | **Atendido na alegação limitada:** sem confusão com convergência |
| R2.5 — comparadores | **Parcial, limitação assumida:** APF e ablações presentes; heurística com mesmo controlador ausente |
| R2.6 — segurança e recuperação | **Atendido no escopo empírico adotado:** perigos, desfechos e janelas interpretados de modo consistente |
| R2.7 — estatística e dados | **Atendido no núcleo:** contagens, métricas, figuras, scripts e pacote identificável |
| R2.8 — inspeção, identidade e falhas | **Atendido no núcleo avaliado:** proxy e estados separados, com limites assíncronos declarados |
| R2.9 — alegações excessivas | **Atendido no núcleo:** completude e segurança delimitadas; última contradição textual corrigida |
| R2.10 — literatura | **Atendido na ampliação:** suficiência da originalidade permanece matéria de julgamento científico |

### Revisor 2 — comentários menores

| Comentário | Situação final |
|---|---|
| R2.m1 — fronteira do raio/chattering | **Delimitado:** mecanismos descritos e promessa sem evidência retirada; sem garantia geral de ausência de oscilação |
| R2.m2 — argmax e campo | **Atendido no núcleo:** seleção, canais, memória, vazio e saturação explicitados |
| R2.m3 — dependência de Φ | **Atendido quanto à ação:** sem dependência de a; aproximação de estado não usada para alegar garantia formal |
| R2.m4 — resíduo zero no baseline | **Atendido:** atualização inativa explicada |
| R2.m5 — reprodução | **Atendido no núcleo documental:** seeds, snapshots, dados, hashes e auditoria |
| R2.m6 — metadados | **Preparação editorial:** não constitui bloqueio científico remanescente |

### Revisores 3 e 4

| Comentário | Situação final |
|---|---|
| R3.1 — benefício de Bellman | **Atendido quanto à distinção causal** |
| R3.2 — perigo sobre a rota | **Atendido:** ensaio e ablações disponíveis |
| R3.3 — estabilidade versus convergência | **Atendido no escopo empírico** |
| R4.1 — η = 0 e reformulação | **Atendido no núcleo** |
| R4.2 — baseline reativo | **Parcial, com limitação assumida** |
| R4.3 — segurança e conflito | **Atendido no escopo avaliado** |
| R4 menor — fronteira/oscilação | **Delimitado pelos mecanismos e resultados apresentados** |
| R4 menor — estatística degenerada | **Atendido** |
| R4 menor — ordem das figuras | **Atendido** |

Não recomendo apresentar na resposta aos revisores que todas as solicitações experimentais foram executadas literalmente. A resposta deve explicar o que foi implementado, o que foi resolvido por reposicionamento e quais limitações foram assumidas. Essa distinção é compatível com um parecer favorável e evita prometer mais do que o artigo demonstra.

## 7. Observação editorial residual, sem condicionar a submissão

Na p. 9, o parágrafo da auditoria ainda agrupa rejeições, falhas de inspeção e desfechos de Avoid sob uma remissão genérica a **V-H**. Uma referência mais precisa seria **V-C, V-F e V-H**, ou simplesmente **Section V**.

É uma remissão interna, não uma contradição de dados ou de método. As remissões principais da Figura 5, Tabela 5 e discussão de E5 já foram corrigidas. **Não condiciono o parecer favorável a outra versão do PDF nem solicito uma oitava rodada por esse detalhe.**

## 8. Encerramento

**Minha recomendação é encaminhar o artigo para submissão.** A última correção factual foi realizada, as correções anteriores foram preservadas e não surgiram novos bloqueios técnicos na conferência final.

Não recomendo nova campanha experimental, mudança de arquitetura ou ampliação dos comparadores como requisito adicional destas revisões. O próximo trabalho é a preparação do encaminhamento editorial, preservando esta versão do manuscrito e a identificação fixa do pacote experimental.

O parecer favorável significa que considero o trabalho tecnicamente apresentável dentro de seu escopo de supervisão deliberativa–reativa e validação em simulação. A decisão de publicação continua pertencendo à revista, particularmente quanto à suficiência da originalidade e à contribuição para a área. **Do ponto de vista desta revisão, podemos encerrar as rodadas de correção.**

[repo]: https://github.com/voidmmn/tese_react_nav/tree/8ed48680d1c15fe5ac5e1326499e8b4f0e269bf4
[audit]: https://github.com/voidmmn/tese_react_nav/blob/8ed48680d1c15fe5ac5e1326499e8b4f0e269bf4/results/audit_trail.csv
