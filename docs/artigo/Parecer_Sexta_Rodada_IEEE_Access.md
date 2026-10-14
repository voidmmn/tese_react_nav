# Parecer técnico — sexta rodada de avaliação

**Artigo:** *A Two-Layer Deliberative–Reactive Architecture with an Affective Attraction–Repulsion Layer for Autonomous Substation Inspection*  
**Autores:** Milton Miranda Neto e Alexandre Cardoso  
**Versão avaliada:** PDF com sufixo `(5)`, 16 páginas  
**Data:** 11 de setembro de 2026  
**Referência:** parecer da quinta rodada, PDF `(4)` e comentários originais dos quatro revisores  
**Natureza:** avaliação técnica independente com critérios pertinentes à revisão científica da IEEE Access; não representa decisão editorial da revista.

**Recomendação: favorável à submissão, após uma correção factual localizada de redação e a revisão editorial final. Os dois ajustes obrigatórios da quinta rodada foram atendidos. Não identifico pendência que exija modificar o método, o código, os dados ou a bateria experimental para sustentar o escopo atual.**

A Figura 5 foi efetivamente atualizada. A interpretação de TTC distingue agora a missão inteira da janela posterior à ativação, e a evidência temporal de distância foi incorporada sem estendê-la indevidamente ao TTC. A auditoria e a proveniência estão melhor delimitadas.

Resta uma frase na p. 13 que chama as métricas de contato e afastamento de “unchanged”. Os contatos observados continuam zerados, mas a distância mínima aumentou sob ruído. A correção é simples, com texto substituto fornecido neste parecer. Não a equiparo aos bloqueios metodológicos ou operacionais das rodadas anteriores.

## 1. Escopo e verificação desta rodada

Mantive os critérios anteriores: contribuição e originalidade, formalização, correspondência com a implementação, métricas de inspeção e segurança, comparadores, estatística, robustez, reprodutibilidade, literatura e apresentação. A sexta rodada também verifica se os critérios de encerramento da quinta foram cumpridos, sem reabrir exigências já resolvidas pela delimitação do escopo.

O pacote atual corresponde ao commit **`8ed48680d1c15fe5ac5e1326499e8b4f0e269bf4`**, cujo pai é `e7c04223c31695aee7a6074d6e67cfe32edd2e02`, examinado na quinta rodada. A comparação das árvores confirma que **somente `results/PROVENANCE.md` mudou no repositório**. Os 160 CSVs, o analisador estatístico, o código de navegação, os geradores de figuras e a auditoria mantêm os mesmos hashes. [Pacote examinado][repo].

Li os trechos revisados do PDF e conferi as equações, figuras e tabelas relevantes. A Figura 5, na p. 10, foi comparada visualmente com a distribuição dos dados já verificados; confirmei também que seu conteúdo gráfico interno difere do objeto antigo que persistia nas duas versões anteriores.

Reaproveitei as verificações quantitativas e operacionais anteriores somente onde a identidade dos arquivos foi confirmada. Não executei novas missões no Gazebo, nem repeti testes sobre funções inalteradas. Também não apresento a identidade dos arquivos como prova de ausência de qualquer defeito possível na pilha de navegação.

As páginas indicadas abaixo são as do PDF `(5)`, de 16 páginas.

## 2. Encerramento das pendências anteriores

| Pendência da quinta rodada | Evidência nesta versão | Situação |
|---|---|---|
| Figura 5 ainda continha três inspeções e duração próxima de 440 s em E5 | Novo painel apresenta mínimo de quatro inspeções e distribuição temporal compatível com máximo de 401,94 s | **Encerrada** |
| Afirmação de equivalência entre TTC global e pós-ativação | P. 11 explicita a métrica global, a ausência de reinicialização e o caso com mínimo anterior à ativação | **Encerrada** |
| Distância e TTC recebiam a mesma justificativa temporal | P. 11 limita a localização pós-ativação à distância nas 18 execuções válidas | **Encerrada** |
| “Temporary keepout” na introdução | P. 2 descreve keepout persistente projetado por detecção | **Encerrada nesse trecho central** |
| Dez execuções confundiam tentativas com amostra analisada | Resumo, introdução e matriz usam “attempted runs”; resultados preservam n = 8–10 | **Encerrada no relato principal** |
| Causa de infraestrutura afirmada como comprovada | P. 9 distingue imobilidade observável de diagnóstico compatível com falha de inicialização | **Encerrada quanto à transparência da evidência** |
| Extração de Avoid não cobria APF | P. 9 declara expressamente essa limitação e restringe os cruzamentos | **Encerrada por delimitação de escopo** |
| Manifesto confundia snapshot de referência com código original de coleta | Manifesto agora diferencia as duas coisas | **Encerrada no manifesto**; harmonizar uma expressão residual do PDF |
| Arquivos substituídos apontavam apenas para pasta local | Manifesto indica o commit público anterior e os caminhos de E5/DHa/DHb | **Encerrada quanto à localização pública** |
| Conjunto vazio na formalização podia ser interpretado como global | P. 5 explicita o conjunto próprio de cada canal | **Encerrada** |
| “No-value ablation” sugeria desligamento de toda a tabela Q | Passou a ablação η = 0, com modulação afetiva identificada | **Encerrada na terminologia revisada** |
| Segurança geral e “graceful degradation” | Trechos principais usam contatos observados e taxas 4/9 e 9/10 | **Amplamente atendida**; uma nova frase sobre afastamento exige correção |

Continuam encerrados os reparos anteriores de ativação do perigo, reinicialização do resultado de navegação entre episódios, classificação de `failed`, separação entre falha e timeout, proteção de metas antigas e correspondência principal da memória do campo.

## 3. Figura 5: correção confirmada

O painel da p. 10 agora corresponde à coleta atual. Na coluna E5, a distribuição de inspeções contém nove resultados iguais a cinco e um igual a quatro. O ponto de três inspeções desapareceu. A distribuição de duração também deixou de conter a execução antiga próxima de 440 s.

| Elemento de E5 | Referência dos CSVs atuais | Figura 5 revisada |
|---|---:|---|
| Média de inspeções | **4,90** | Compatível |
| Mínimo e máximo de inspeções | **4 e 5** | Compatíveis |
| Completude por missão | **9/10** | Distribuição compatível |
| Duração média | **397,03 s** | Compatível |
| Intervalo de duração | **385,82 a 401,94 s** | Compatível |
| Distância mínima ao perigo | **4,854 ± 0,032 m** | Distribuição compatível |

A Tabela 5, na p. 11, mantém 4,9 ± 0,3 inspeções e 397 ± 4 s. Figura, tabela e discussão de E5 estão agora sincronizadas no ponto que motivava a objeção.

**Não há necessidade de gerar outra figura para encerrar esta pendência.** O que faltava era substituir o painel efetivamente incluído no PDF, e isso foi feito. [Gerador publicado][boxplots].

## 4. TTC e distância: interpretação agora adequada

A p. 11 declara quatro pontos essenciais:

1. Distância e TTC são mínimos acumulados ao longo da missão, incluindo o período anterior à ativação.
2. O coletor não reinicializa essas métricas quando o perigo surge.
3. Os registros permitem localizar o mínimo de distância após a ativação nas 18 execuções dinâmicas válidas.
4. A mesma conclusão não é estendida ao TTC, cujo mínimo final já estava registrado antes da ativação em uma execução.

Isso corresponde à verificação da quinta rodada. O caso concreto permanece DHa repetição 4: o TTC mínimo final de aproximadamente **6,104554 s** já consta da amostra de tempo ROS **96,000 s**, enquanto a ativação ocorre em **96,500 s**. Como os arquivos são os mesmos, não foi necessário repetir essa análise para validar a nova descrição. [Auditoria][audit] e [CSV do caso temporal][dha4].

O artigo pode continuar reportando os resultados:

| Contraste DHa − DHb | Resultado | Interpretação admitida |
|---|---:|---|
| Distância mínima | **+0,327 m**, IC ≈ [0,23; 0,42], δ = 1 | Maior mínimo de afastamento; os mínimos finais foram atingidos após ativação nos casos avaliados |
| TTC radial mínimo | **+0,511 s**, IC ≈ [0,20; 0,84], δ = 0,85 | Diferença na métrica global da missão, sem alegar estimação separada de efeito pós-ativação |
| Duração | **+9,42 s** | Custo operacional associado ao braço com recuo |
| Distância percorrida | **+1,65 m** | Deslocamento adicional |
| Inspeção no encontro perigoso | DHa 0/8; DHb 10/10 | Adiamento deliberado em troca de afastamento maior |

A exposição dos custos e do adiamento impede que o ganho de margem seja apresentado como benefício sem contrapartida. A distinção entre preempção, saída `safe` e chegada à meta de recuo também permanece explícita.

**Encerro a objeção temporal da quinta rodada. Não recomendo nova coleta DHa/DHb para a alegação global que o texto agora adota.**

## 5. Única correção factual de redação que considero necessária

**Localização:** p. 13, final de V-H, análise de ruído.  
**Trecho:** “while the observed contact and clearance metrics are unchanged”.  
**Origem:** imprecisão introduzida na reformulação textual desta rodada, sem alteração dos dados ou do algoritmo.

A expressão é correta para a contagem de contatos observados, que permanece zerada, mas não para a distância mínima ao perigo:

| Configuração | Distância mínima média ao perigo |
|---|---:|
| E3, sem ruído | **4,86 ± 0,03 m** |
| N1, ruído moderado | **5,01 ± 0,11 m** |
| N2, ruído alto | **5,29 ± 0,20 m** |

A própria Tabela 10 apresenta E3 → N2 com diferença de aproximadamente **+0,43 m**, IC de 95% **[0,31; 0,56]**, Cliff’s δ = 1 e p ≈ **2 × 10⁻⁵**. Portanto, as métricas de afastamento não ficaram inalteradas: o mínimo médio aumentou.

Isso não é uma piora escondida de segurança nem invalida o resultado de ruído. É uma descrição incorreta de um resultado que as tabelas já mostram adequadamente.

**Redação substituta sugerida para as frases finais desse argumento:**

> Under high perception noise, full-inspection completion fell to 4/9 valid runs, while no contact-region entries were observed. Mean minimum hazard clearance increased from 4.86 ± 0.03 m in E3 to 5.29 ± 0.20 m in N2. These results describe the observed trade-off under the tested noise levels and do not establish a general safety guarantee.

Manter em seguida a frase sobre intervalo Wilson e unidade experimental por missão. Se preferir uma alteração ainda menor, substituir apenas a oração problemática por:

> while no contact-region entries were observed and mean minimum hazard clearance increased.

**Essa correção exige somente texto.** Não há motivo para modificar médias, intervalos, testes ou séries experimentais.

## 6. Avaliação científica pelos mesmos critérios

### 6.1. Contribuição e originalidade

O trabalho está adequadamente apresentado como arquitetura de supervisão deliberativa–reativa, com campo de saliência, arbitragem, aproximação de anomalias e resposta a perigos. A formulação de atualização de valor permanece secundária e não recebe o crédito causal pelo movimento executado.

A originalidade demonstrada é **moderada**, associada à integração e à análise experimental. A ausência de um supervisor heurístico de simplicidade equivalente, usando o mesmo controlador, continua limitando a demonstração de vantagem específica da ponderação afetiva. Essa limitação é reconhecida na p. 12 e não foi agravada nesta versão.

Não reabro a exigência de uma política Q atuante, PPO/DDQN, ou novo comparador como condição para concluir estas revisões. O artigo deve ser julgado pela contribuição que efetivamente declara. Um avaliador externo ainda pode discordar sobre a suficiência da originalidade, mas essa é uma questão de mérito científico remanescente, não uma inconsistência interna agora detectada.

### 6.2. Matemática e implementação

A formalização mantém os dois acumuladores, memória por retenção de magnitude, decaimento, limiar residual, saturação interna e precedência do canal de perigo. A explicação do conjunto vazio passou a ser específica de cada canal, encerrando a ambiguidade anterior.

A equivalência com aumento de recompensa, para taxa de aprendizado fixa, está corretamente reconhecida. O artigo não reivindica invariância de política ou convergência de Q-learning para o termo aditivo adotado.

Os reparos operacionais anteriores permanecem nos mesmos arquivos. Não surgiu uma nova modificação de controle para auditar nesta rodada. Portanto, não há fundamento para exigir a repetição de testes ou experimentos somente porque o PDF foi revisado.

### 6.3. Desenho experimental e comparadores

A matriz de dezesseis configurações permite examinar o comportamento básico, a ablação η = 0, ruído, densidade, conflito e a separação entre keepout e recuo. Os resultados negativos de KOb e a vantagem do keepout no perigo estático são discutidos, o que evita atribuir ao recuo toda a contribuição de navegação.

A comparação APF continua qualificada como comparação entre implementações de sistemas com controladores e parâmetros distintos. Isso é aceitável no escopo declarado; não demonstra isoladamente superioridade do campo sobre qualquer alternativa reativa.

O ensaio dinâmico permanece dirigido e exploratório, e seus p não são apresentados como parte da família confirmatória corrigida por Holm. Não há nova exigência experimental decorrente da sexta rodada.

### 6.4. Estatística e denominadores

Os **160 arquivos**, **154 execuções válidas** e **seis tentativas imóveis** estão mantidos. A faixa de n válido continua 8–10, com nove em APF, RHM, N2 e KOb, e oito em DHa. O uso de dez *tentativas* na matriz foi esclarecido no resumo e na introdução.

Os resultados conferem com os recálculos anteriores sobre os mesmos dados:

| Resultado | Valor de referência |
|---|---:|
| Fração de tentativas que atende ao critério de movimento | **154/160 = 96,25%** |
| E5: completude | **9/10**, Wilson ≈ [0,60; 0,98] |
| N2: completude | **4/9**, Wilson ≈ [0,19; 0,73] |
| E3: inspeções no cenário padrão | **3,0 ± 0,0** |
| RHM/RHB: distância mínima no perigo sobre a rota | **1,71 / 0,71 m**, aproximadamente |
| E3 − E1: duração | **+44,18 s**, aproximadamente |
| E5 − E3: duração | **+32,59 s**, aproximadamente |

Permanecem resolvidos o TOST degenerado, a distinção de intervalos binomiais, a descrição do cálculo de Mann–Whitney e a multiplicidade da família confirmatória. Não reproduzi novamente uma análise integral inalterada; preservei as verificações já realizadas após comprovar a identidade dos arquivos. [Analisador estatístico][statistics].

### 6.5. Inspeção, segurança e robustez

A inspeção continua definida como proxy de chegada confirmada, com dwell comandado e limitação explícita de orientação e persistência fisicamente verificadas. O crédito é separado de início, falha, rejeição e adiamento. A explicação de E5 e das seis rejeições N2 mantém correspondência com os episódios publicados.

A segurança é tratada principalmente por contatos observados, afastamento e TTC radial, com ressalvas de amostra finita. O artigo diferencia precedência lógica de garantia física e reconhece o refratário e as demais condições de disparo.

A validação permanece em simulação, com percepção abstrata e localização idealizada. Ruído e cenários dirigidos fornecem evidência delimitada; não demonstram generalização a mapas e condições arbitrárias. Essas limitações estão suficientemente expostas para o escopo atual. A correção da frase “unchanged” evita contradizer essa análise quantitativa.

### 6.6. Auditoria e reprodutibilidade

A auditoria de **1.537 eventos** é a mesma verificada na quinta rodada. Permanecem confirmados os três abortos DHa seguidos de saída `safe`, os sete resultados de aborto registrados no conjunto, as seis rejeições N2 e a falha E5 sem nova tentativa registrada na repetição 6.

A p. 9 agora informa que a extração de Avoid cobre Stay Alert, enquanto APF permanece representado pelos seus contadores agregados. Essa é a delimitação solicitada; não mantenho a ausência dos episódios APF na trilha como erro não reconhecido.

O manifesto distingue snapshots de referência e código efetivamente executado na coleta original, além de indicar onde os arquivos substituídos podem ser consultados publicamente. Isso é suficiente para encerrar a exigência documental principal. A tag continua móvel; a identificação fixa do pacote desta avaliação é o commit informado na seção 1. [Manifesto revisado][provenance].

### 6.7. Literatura e apresentação

A literatura permanece ampliada em relação ao artigo original e coerente com o reposicionamento, incluindo navegação híbrida, percepção ativa, campos potenciais e modulação de recompensa. Não fiz nova busca bibliográfica exaustiva nesta rodada; mantive a avaliação anterior das referências e do alcance da contribuição.

A Figura 5 corrigida elimina a principal incoerência visual. Equações e tabelas examinadas estão legíveis, e a discussão quantitativa acompanha os dados. Restam detalhes de remissão e composição, sem impacto demonstrado na conclusão científica.

## 7. Refinamentos editoriais finais, sem reabrir a metodologia

| Localização | Ajuste recomendado | Motivo |
|---|---|---|
| P. 9, proveniência | Trocar “collection commit for each batch” por “reference snapshot for each batch”, conforme o manifesto | O PDF deve adotar a distinção documental que já foi corrigida no repositório |
| Pp. 9–11, remissões | Corrigir referências gerais a V-H quando o assunto é E5 ou Avoid | E5 está em V-F; o ensaio dinâmico está em V-C; V-H trata de ruído |
| P. 11, legenda da Tabela 6 | Preferir “reactive retreat combined with a detection-triggered persistent keepout” | Evita sugerir que a projeção do keepout só ocorre após completar o recuo |
| P. 14, Apêndice A | Trocar “both scenarios” por “all five scenarios” | A Tabela 9 contempla cinco cenários |
| P. 2, contribuição | Preferir “provides patrol coverage” a “guarantees coverage” | Evita linguagem de garantia geral quando existem condições e encerramentos por limite |

Esses pontos são ajustes de consistência editorial. Não recomendaria outra rodada ampla de simulações, implementação ou revisão metodológica para resolvê-los. Os placeholders editoriais de DOI, volume e datas devem continuar sendo tratados como campos do manuscrito, sem preenchimento com dados de publicação inventados.

## 8. Atendimento aos revisores originais

O estado “atendido no escopo” reconhece uma resposta por delimitação honesta da contribuição. Ele não significa que o artigo passou a demonstrar aprendizagem atuante, inspeção física ou garantia formal de segurança.

### Revisor 1

| Item | Situação | Avaliação |
|---|---|---|
| R1.1 — teoria/convergência | **Atendido no escopo** | Sem alegação de herdar garantias do Q-learning |
| R1.2 — estatística/multiplicidade | **Atendido** | Métodos, efeitos, intervalos, n e figura compatíveis |
| R1.3 — robustez | **Parcial, com limite explícito** | Ruído e cenários dirigidos; generalização ampla permanece fora da evidência |
| R1.4 — resíduo e múltiplas execuções | **Atendido para estabilidade empírica** | Métrica completa, agregação e gerador publicados |
| R1.5 — literatura/comparação | **Atendido na ampliação; limite de originalidade permanece** | Diferenciação frente a supervisor equivalente não isolada |
| R1.6 — custos | **Atendido no núcleo** | Tempo, deslocamento e adiamento discutidos |
| R1.7 — resumo | **Atendido** | Contribuição, completude e contatos observados alinhados |

### Revisor 2 — comentários maiores

| Item | Situação | Avaliação |
|---|---|---|
| R2.1 — papel de Q/ablação | **Atendido no reposicionamento** | Mecanismo de comando e η = 0 explícitos |
| R2.2 — shaping/dupla contagem | **Atendido** | Equivalência e alcance da novidade reconhecidos |
| R2.3 — efeito de η | **Atendido no escopo** | Sem atribuição de robustez a uma política aprendida atuante |
| R2.4 — estabilidade | **Atendido na alegação limitada** | Sem confusão com convergência |
| R2.5 — comparadores | **Parcial, limitação assumida** | APF e ablações presentes; comparador heurístico de mesmo controlador ausente |
| R2.6 — segurança/recuperação | **Atendido no escopo empírico adotado** | Ativação, desfechos e limites temporais agora coerentes |
| R2.7 — estatística/dados | **Atendido no núcleo** | Totais, figura, dados e identificação do pacote disponíveis |
| R2.8 — inspeção/identidade/falhas | **Atendido no núcleo avaliado** | Proxy e desfechos separados; limites assíncronos reconhecidos |
| R2.9 — alegações | **Atendido no núcleo; uma correção textual necessária** | Corrigir “clearance metrics are unchanged” em V-H |
| R2.10 — literatura | **Atendido na ampliação; mérito de originalidade aberto ao julgamento editorial** | Contribuição descrita como integração |

### Revisor 2 — comentários menores

| Item | Situação | Avaliação |
|---|---|---|
| R2.m1 — raio/chattering | **Atendido quanto ao relato delimitado** | Mecanismos descritos; promessa de varredura retirada; limites de oscilação conhecidos |
| R2.m2 — argmax/formalização | **Atendido no núcleo** | Canais, vazio próprio, memória e saturação explicitados |
| R2.m3 — dependência de Φ | **Atendido quanto à ação** | Não depende de a; memória não é usada para prometer propriedade Markoviana completa |
| R2.m4 — zero no baseline | **Atendido** | Atualização inativa explicada |
| R2.m5 — reprodução | **Atendido no núcleo documental** | Seeds, dados, hashes, snapshots e auditoria; completar harmonização de frase no PDF |
| R2.m6 — metadados | **Preparação editorial final** | Não constitui objeção científica remanescente |

### Revisores 3 e 4

| Item | Situação | Avaliação |
|---|---|---|
| R3.1 — Bellman e comportamento | **Atendido** | Distinção causal explícita |
| R3.2 — perigo na rota | **Atendido** | RHM/RHB e ablações disponíveis |
| R3.3 — estabilidade/convergência | **Atendido no escopo** | Estabilidade empírica entre execuções |
| R4.1 — η = 0 e reformulação | **Atendido no núcleo** | Título e contribuição alinhados |
| R4.2 — baseline reativo | **Parcial, limitação assumida** | APF presente; vantagem específica do campo não totalmente isolada |
| R4.3 — segurança/conflito | **Atendido no escopo avaliado** | Conflito e ensaio dinâmico com interpretações delimitadas |
| R4 menor — fronteira/oscilação | **Delimitado** | Sem demonstração de ausência geral de oscilação |
| R4 menor — estatística degenerada | **Atendido** | Procedimentos centrais corrigidos |
| R4 menor — ordem das figuras | **Atendido** | Sequência do agradecimento preservada |

## 9. O que é antigo, novo e efetivamente encerrado

| Item | Classificação nesta rodada |
|---|---|
| Figura 5 antiga | **Problema anterior encerrado** |
| Equivalência temporal indevida de TTC | **Problema anterior encerrado** |
| Esquema e escopo da auditoria | **Correções preservadas e limitações explicitadas** |
| Contagem global e tentativas imóveis | **Correções preservadas; relato causal melhor delimitado** |
| Proveniência dos dados substituídos | **Correção documental implementada** |
| “Clearance metrics are unchanged” | **Nova imprecisão de redação**, corrigível por substituição de uma frase |
| Remissões e termos residuais | **Refinamentos editoriais**, em grande parte anteriores |
| Novo defeito de controle ou necessidade de recoleta | **Não identificado** |

Você não voltou a introduzir os problemas operacionais das primeiras revisões. A nova imprecisão surgiu ao tornar uma afirmação de segurança mais específica; os dados continuam corretos e mostram a direção da mudança. A solução é descrever essa mudança, sem alterar o experimento.

## 10. Parecer final de prontidão

| Critério | Julgamento |
|---|---|
| Relevância | **Boa** |
| Clareza do mecanismo e da contribuição | **Boa** |
| Originalidade demonstrada | **Moderada**, com limites de comparação assumidos |
| Correção matemática e operacional no escopo auditado | **Suficiente para encaminhamento** |
| Estatística e coerência quantitativa | **Consistentes**, com a figura corrigida |
| Segurança e robustez | **Evidência empírica delimitada**, sem garantia geral |
| Reprodutibilidade | **Boa para os dados e episódios examinados**, com proveniência mais precisa |
| Apresentação | **Adequada**, com pequenos ajustes finais |
| Recomendação | **Submeter após corrigir a frase de V-H e concluir a revisão editorial** |

Considero encerrada a etapa de correções metodológicas e operacionais conduzida nestas rodadas, dentro dos arquivos e do escopo examinados. O artigo está tecnicamente em condição de encaminhamento após o ajuste textual indicado. Não recomendaria iniciar outra campanha experimental nem ampliar novamente o escopo como requisito desta avaliação.

Isso não é previsão de aceitação: a suficiência da originalidade e a pertinência da contribuição de integração ainda serão julgadas pela revista. Mas os bloqueios objetivos que motivaram as revisões anteriores foram resolvidos, e a decisão de submeter pode agora se apoiar em um manuscrito substancialmente mais coerente e verificável.

[repo]: https://github.com/voidmmn/tese_react_nav/tree/8ed48680d1c15fe5ac5e1326499e8b4f0e269bf4
[boxplots]: https://github.com/voidmmn/tese_react_nav/blob/8ed48680d1c15fe5ac5e1326499e8b4f0e269bf4/src/tese_nav/scripts/gerar_boxplots.py
[audit]: https://github.com/voidmmn/tese_react_nav/blob/8ed48680d1c15fe5ac5e1326499e8b4f0e269bf4/results/audit_trail.csv
[dha4]: https://github.com/voidmmn/tese_react_nav/blob/8ed48680d1c15fe5ac5e1326499e8b4f0e269bf4/results/metrics_DHa_20260910_202848.csv
[statistics]: https://github.com/voidmmn/tese_react_nav/blob/8ed48680d1c15fe5ac5e1326499e8b4f0e269bf4/src/tese_nav/scripts/analise_estatistica.py
[provenance]: https://github.com/voidmmn/tese_react_nav/blob/8ed48680d1c15fe5ac5e1326499e8b4f0e269bf4/results/PROVENANCE.md
