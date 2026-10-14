# Parecer técnico — quinta rodada de avaliação

**Artigo:** *A Two-Layer Deliberative–Reactive Architecture with an Affective Attraction–Repulsion Layer for Autonomous Substation Inspection*  
**Autores:** Milton Miranda Neto e Alexandre Cardoso  
**Versão:** PDF com sufixo `(4)`, 16 páginas  
**Data:** 11 de setembro de 2026  
**Referência:** parecer da quarta rodada, versão `(3)` e comentários originais dos quatro revisores  
**Natureza:** avaliação técnica independente segundo critérios pertinentes à revisão científica da IEEE Access; não representa decisão editorial da revista.

**Recomendação: parecer favorável ao encaminhamento após correções pontuais obrigatórias. A revisão resolveu a maior parte das pendências da quarta rodada. Restam principalmente a Figura 5, que continua antiga no PDF anexado, e uma afirmação ainda não sustentada sobre a coincidência entre métricas da missão inteira e após a ativação.**

A classificação técnica desta rodada é de **revisão menor, concentrada em consistência e relato**, sem necessidade demonstrada de nova bateria experimental para manter o escopo atual. Isso não significa aprovar o arquivo exatamente como está: a figura contraditória precisa ser substituída, e a interpretação temporal deve ser corrigida. As limitações anteriores de originalidade e generalização permanecem, mas não foram agravadas pelos reparos desta versão.

## 1. Como conduzi esta rodada

Mantive os mesmos critérios: contribuição científica, correspondência entre formalização e implementação, inspeção e segurança, desenho experimental, comparadores, estatística, robustez, reprodutibilidade, literatura e apresentação. A avaliação começa pelos critérios de encerramento da quarta rodada; uma pendência corrigida não volta a ser exigida sob outro nome.

Li o novo PDF e comparei seus trechos relevantes com a versão anterior. Inspecionei visualmente as páginas com equações, figuras e tabelas, incluindo a nova localização da Figura 5 na **p. 10** e da Tabela 10 na **p. 16**.

O repositório consultado resolve a tag `v1.0-resubmission` para o commit **`e7c04223c31695aee7a6074d6e67cfe32edd2e02`**, cujo pai é o commit examinado na quarta rodada, `12081a70ed645a78a348440e8d1623ac6678e781`. Apenas quatro arquivos de conteúdo mudaram: o gerador da auditoria, a própria auditoria, o manifesto de proveniência e o arquivo de checksums. **Os 160 CSVs de métricas, o código de navegação e o analisador estatístico mantêm identidade com a quarta rodada.** [Versão examinada][repo].

Por essa razão, não repeti testes operacionais sobre funções inalteradas nem uma nova simulação. Conferi os resultados do novo manuscrito contra o recálculo já verificado na quarta rodada, após confirmar a identidade dos dados. Verifiquei também os checksums SHA-256 dos 30 CSVs de E5/DHa/DHb disponíveis integralmente no trabalho local, preservando os finais de linha originais; eles conferem com o manifesto. A confirmação de identidade dos 160 arquivos usa os hashes de objetos do Git, não uma afirmação de que recalculei 160 SHA-256 nesta rodada.

A auditoria nova contém **1.537 eventos**. Cruzei seus registros por configuração e repetição com `run_seed`, examinei os episódios e comparei os tempos de ativação com as séries completas dos 18 ensaios dinâmicos válidos. Essa comparação temporal é uma verificação nova, possibilitada pela correção da auditoria.

As páginas citadas neste parecer são as do PDF `(4)`, de 16 páginas.

## 2. Balanço das pendências da quarta rodada

| Pendência anterior | O que mudou | Situação atual |
|---|---|---|
| Figura 5 representava os dados antigos de E5 | Mudou de página, mas conserva o mesmo conteúdo gráfico antigo | **Pendente** |
| Totais 156 válidas, quatro imóveis e 97,5% | P. 9 informa 154, seis, 96,25% e n = 8–10; p. 14 informa seis exclusões | **Corrigido numericamente** |
| “Mission never started” ignorava o relógio de missão acumulado | Texto reconhece que a maioria das execuções imóveis acumula tempo | **Corrigida a contradição direta**; causa de infraestrutura ainda é afirmada sem logs publicados correspondentes |
| Mínimos da missão inteira eram chamados de pós-ativação “por construção” | O coletor sem filtro é explicitado e o texto declara métricas da missão inteira | **Avanço importante**, mas a frase “the two coincide in practice” preserva uma equivalência não demonstrada para TTC |
| Auditoria não distinguia posição do alvo e do robô | Colunas `target_true_x/y` e `robot_x/y` separadas | **Corrigido** |
| Parser descartava o tempo ROS explícito | Colunas `time_ros_s` e `time_log_s`, com campos vazios documentados | **Corrigido** |
| Faltavam fins de Avoid e resultados de metas | Auditoria inclui entradas, saídas e sete resultados de aborto | **Corrigido para os episódios centrais examinados** |
| E5 repetição 6 era descrita como retry não concluído | Pp. 12–13 descrevem falha sem nova tentativa registrada e não alegam política geral de retry | **Corrigido** |
| Faltava proveniência por lote | Publicados `PROVENANCE.md` e `CHECKSUMS.sha256` | **Substancialmente atendido**, com ressalvas de precisão documental |
| Formalização omitia vazio, ε, período e saturação interna | P. 5 e Tabela 3 explicitam esses pontos | **Corrigida a divergência principal** |
| Promessa de varredura do raio sem resultado | P. 5 agora promete apenas a análise de ruído apresentada | **Corrigido** |
| Resumo/conclusão exageravam segurança e limite temporal | Pp. 1 e 14 usam contatos observados, aumento medido e completude 4/9 e 9/10 | **Corrigido nesses trechos**; linguagem antiga persiste no corpo |
| Metadados de exemplo pareciam dados reais | DOI e volume passaram a campos claramente zerados | **Melhora editorial suficiente para distinguir rascunho de publicação** |

Os dois defeitos operacionais da terceira rodada — antecipação do perigo no keepout e persistência de aborto entre episódios — **continuam encerrados**. Os arquivos que os corrigiram não foram alterados nesta rodada. Não encontrei evidência de regressão de navegação introduzida agora.

## 3. Primeira correção obrigatória: a Figura 5 ainda é a antiga

**Localização:** p. 10, Figura 5.  
**Origem:** pendência já existente e demonstrada na quarta rodada.  
**Natureza:** sincronização do PDF, sem necessidade de nova coleta.

A figura inserida no arquivo efetivamente anexado ainda mostra, na coluna E5, um ponto com **três inspeções**, outro com quatro e uma execução com duração de aproximadamente **440 s**. Esses pontos pertencem à distribuição antiga.

Os CSVs atuais contêm nove execuções E5 com cinco inspeções e uma com quatro. Nenhuma tem três inspeções; a duração máxima é **401,94 s**.

| Elemento | Figura 5 do PDF `(4)` | Dados atuais |
|---|---:|---:|
| Mínimo de inspeções em E5 | **3** | **4** |
| Média de inspeções em E5 | Aproximadamente **4,7** | **4,9** |
| Duração máxima de E5 | Aproximadamente **440 s** | **401,94 s** |
| Média de duração de E5 | Distribuição antiga, próxima de 402 s | **397,03 s** |

A verificação não depende apenas de leitura visual: o fluxo de desenho do objeto PDF correspondente ao painel tem **o mesmo SHA-256 nas versões `(3)` e `(4)`**. Portanto, o painel foi reposicionado na paginação, mas sua representação gráfica não foi substituída. A Tabela 5 e o texto estão atualizados; a figura não.

Isso pode resultar de um arquivo gráfico antigo ainda referenciado no projeto, de uma cópia não substituída ou de exportação anterior à recompilação. Não determinei qual dessas causas ocorreu e não atribuo o problema ao algoritmo.

**Ação suficiente:** gerar o painel com `gerar_boxplots.py` sobre os resultados atuais, verificar qual arquivo a instrução de inclusão gráfica utiliza, substituí-lo e recompilar. No PDF final, conferir que E5 não apresenta o ponto de três inspeções nem o ponto de 440 s. O gerador já está publicado e não mudou desde a quarta rodada. [Gerador do painel][boxplots].

**Critério de encerramento:** Figura 5 coerente com a Tabela 5 e com a distribuição 5, 5, 5, 5, 5, 4, 5, 5, 5, 5 de inspeções E5 por repetição.

## 4. Segunda correção obrigatória: retirar a equivalência temporal não demonstrada

### 4.1. A definição da métrica melhorou

Na p. 11, o artigo agora reconhece que o coletor mede distância e TTC durante toda a missão, sem filtrar a ativação. Essa é uma das alternativas expressamente aceitas no parecer anterior: manter as métricas globais e limitar a alegação temporal.

Entretanto, entre essa definição e a frase que nega uma janela separadamente recalculada, permanece a afirmação **“the two coincide in practice”**, justificada pela geometria e pela aproximação ao alvo. A explicação de distância não demonstra a mesma propriedade para TTC, que também depende da velocidade radial.

### 4.2. Um caso concreto já contém o TTC mínimo antes da ativação

O tempo ROS agora preservado na auditoria permite verificar **DHa, repetição 4**:

| Registro | Tempo ROS | Valor |
|---|---:|---:|
| TTC mínimo acumulado | 95,000 s | 6,590789 s |
| TTC mínimo acumulado | **96,000 s** | **6,104554 s** |
| Ativação do perigo | **96,500 s** | `hazard_activated`, ID 100 |
| TTC mínimo acumulado | 97,000 s | 6,104554 s |
| TTC mínimo ao final da execução | Final | **6,104554 s** |

O valor final de TTC já estava registrado **0,5 s antes da ativação**. Portanto, não se pode usar essa série de mínimos acumulados como demonstração de que o valor foi produzido por uma janela exclusivamente posterior ao surgimento do perigo. [CSV de DHa repetição 4][dha4] e [auditoria com o tempo de ativação][audit].

Isso não prova que um TTC numericamente igual jamais possa ter ocorrido depois da ativação. O coletor guarda apenas o menor valor até cada instante, então uma repetição posterior do mesmo valor não pode ser distinguida. A conclusão sustentada é mais restrita: **há contribuição pré-ativação documentada, e a igualdade das duas janelas não foi demonstrada**.

### 4.3. Distância e TTC devem receber conclusões diferentes

Cruzei as 18 execuções dinâmicas válidas com seus instantes de ativação. Para evitar atribuir precisão maior que a amostragem, considerei se o mínimo acumulado ainda diminuiu depois da primeira amostra registrada após a ativação.

| Métrica | Resultado da verificação temporal |
|---|---|
| Distância mínima | **18/18** atingiram valor menor que o da primeira amostra posterior à ativação; o mínimo final foi, portanto, atingido depois dela |
| TTC mínimo | **16/18** atingiram valor menor depois dessa primeira amostra |
| TTC em DHa repetição 4 | O valor final já constava da última amostra anterior à ativação |
| TTC em DHa repetição 6 | A primeira amostra posterior já contém o mínimo final; o intervalo entre amostras atravessa a ativação e não permite localizar o instante com precisão |

Assim, há suporte nos registros para a localização pós-ativação dos mínimos de **distância**. A mesma afirmação irrestrita para **TTC** não é sustentada.

Essa conferência não é um recálculo de TTC instantâneo após ativação. Filtrar as linhas do CSV por `timestamp ≥ t_ativação` não resolve o problema, porque as linhas contêm mínimos acumulados e podem carregar valores anteriores.

### 4.4. Correção proporcional ao escopo escolhido

**Não exijo nova simulação para encerrar esta pendência.** Basta manter a definição global já adotada e eliminar a frase de coincidência das duas janelas, com a conclusão limitada à métrica efetivamente medida.

Sugestão de substituição do trecho metodológico:

> The clearance and radial time-to-collision values reported below are whole-mission minima relative to the hazard’s location, including the pre-activation period. The collector does not reset these metrics upon activation. These results therefore compare overall mission-level margins in the emerging-hazard scenario and do not estimate a separate post-activation TTC effect.

Se desejar acrescentar a evidência específica de distância, ela pode ser apresentada separadamente, acompanhada da comparação temporal dos registros. Não é necessário generalizá-la a TTC.

O ganho de aproximadamente **0,33 m de distância mínima** permanece apoiado pelos dados. O ganho de aproximadamente **0,51 s de TTC global** também continua reproduzível. O ajuste é na atribuição temporal desse segundo resultado, não em apagar a diferença observada.

## 5. Auditoria: a pendência central foi resolvida

### 5.1. Esquema e relógios

O novo gerador separa a posição verdadeira do alvo da posição do robô e preserva o tempo ROS quando ele está presente na mensagem. O timestamp do cabeçalho permanece em outra coluna, com significado documentado. A descrição da p. 9 também deixa claro que nem todos os eventos carregam tempo de simulação.

Essas correções eliminam os dois defeitos de esquema identificados na quarta rodada. Elas permitiram a verificação temporal da seção anterior, que não era possível de maneira inequívoca com a trilha antiga. [Gerador atualizado][auditgen].

### 5.2. Contagens e identidade de episódios

| Grupo | Inícios de investigação | Inspeções creditadas | Rejeições de confirmação | Falhas de investigação | Adiamentos |
|---|---:|---:|---:|---:|---:|
| E5 | **52** | **49** | 0 | **3** | 0 |
| N2 | **27** | **21** | **6** | 0 | 0 |
| DHa | **8** | **0** | 0 | 0 | **8** |
| DHb | **11** | **10** | 0 | **1** | 0 |

Os cruzamentos de investigações iniciadas, créditos e adiamentos continuam sem divergências com os contadores dos 160 CSVs. Também não encontrei, na checagem das chaves de episódio, encerramento de investigação associado a outro ID de alvo nem sobreposição de inícios Investigate/Avoid sob o mesmo identificador.

Há dois episódios sem encerramento na trilha de KOb: uma investigação na repetição 8 e um Avoid na repetição 9. Dado que esse grupo termina por limite de execução, não classifico automaticamente essas ausências como erro de parser ou sucesso. Devem ser lidas como episódios sem término registrado dentro da janela coletada.

### 5.3. Os três abortos de DHa agora podem ser rastreados

| Repetição DHa | Episódio de Avoid | Resultado de navegação registrado | Término de Avoid |
|---:|---:|---|---|
| 3 | 2 | `aborted` | `safe`, duração 15 s |
| 4 | 2 | `aborted` | `safe`, duração 14 s |
| 6 | 2 | `aborted` | `safe`, duração 14 s |

As oito execuções válidas DHa têm entrada e saída de Avoid, todas com motivo `safe`. Isso corrobora a discussão das pp. 11–12: a saída do supervisor pode ocorrer após o campo decair, mesmo sem conclusão da meta de recuo. **Não mantenho a falta desses desfechos como bloqueio atual.**

É importante preservar a interpretação: `safe` é o nome de uma condição de saída baseada em Φ; `retreated` é outra condição, ligada à chegada. Nem uma nem outra substitui as medições independentes de afastamento e contato. O novo pacote permite fazer essa distinção com evidência, e o artigo já a reconhece.

Há sete resultados `nav_result` na trilha: três abortos DHa, um DHb e três E5. O novo texto deixou de prometer uma lista completa de resultados `succeeded` por meta que o gerador não fornece, o que é uma correção adequada de escopo.

### 5.4. Ressalva menor: a extração de Avoid não cobre APF

Os nove CSVs APF válidos registram um evento de evitação cada, mas a trilha não contém os correspondentes `avoid_start/avoid_end`. O gerador reconhece as mensagens do supervisor Stay Alert; o controlador APF tem outro caminho de registro.

Isso não compromete a auditoria DHa/DHb/E5/N2 realizada acima. A correção proporcional é documentar que a extração dos episódios de Avoid cobre o **Stay Alert**, enquanto os resultados APF correspondentes permanecem nos CSVs agregados. Se a intenção for prometer auditoria completa de todos os controladores, incluir também os padrões APF.

Trata-se de uma limitação localizada de cobertura da nova extração, não de uma falha de navegação introduzida no APF. A afirmação de que todos os agregados cruzam com a auditoria deve indicar quais eventos e controladores foram efetivamente cruzados.

## 6. Dados, amostra e estatística

Os resultados quantitativos centrais não mudaram em relação à quarta rodada. Isso é coerente com a identidade dos 160 CSVs e do analisador estatístico.

| Resultado | Valor verificado | Situação no PDF |
|---|---:|---|
| Tentativas / válidas / imóveis | **160 / 154 / 6** | Corrigido |
| Fração que atende ao critério de movimento | **96,25%** | Corrigido |
| E5: inspeções | **4,90 ± 0,32** | Tabela e texto corretos; figura antiga |
| E5: completude | **9/10**, IC Wilson ≈ **[0,60; 0,98]** | Correto |
| E5: duração | **397,03 ± 4,18 s** | Tabela e texto corretos |
| N2: completude | **4/9**, IC Wilson ≈ **[0,19; 0,73]** | Correto |
| DHa/DHb: n válido | **8 / 10** | Correto |
| DHa/DHb: distância mínima | **2,551 ± 0,146 / 2,224 ± 0,005 m** | Correto |
| DHa/DHb: TTC global | **5,232 ± 0,448 / 4,721 ± 0,207 s** | Correto como métrica global |
| DHa − DHb: custo temporal | **+9,42 s** | Arredondamento coerente |
| DHa − DHb: deslocamento adicional | **+1,65 m** | Arredondamento coerente |

Os tamanhos válidos são dez na maioria dos grupos, nove em APF, RHM, N2 e KOb, e oito em DHa. A Tabela 10 usa os denominadores corretos e identifica os contrastes do perigo emergente como exploratórios, sem incluí-los na família confirmatória de Holm.

Permanecem aceitas as correções anteriores: testes adequados aos braços constantes, efeitos e intervalos, descrição dos ramos de Mann–Whitney, TOST não aplicado aos casos degenerados e distinção entre intervalo Wilson e limite binomial exato. O limite aproximado de **31% para zero falhas em oito execuções** foi acrescentado corretamente na p. 14. [Analisador estatístico, inalterado][statistics].

### 6.1. Precisar a classificação das seis tentativas imóveis

A p. 9 melhorou ao reconhecer o relógio acumulado sem movimento. Entretanto, continua afirmando que todas são falhas de inicialização porque o contêiner não colocou o robô em operação. A p. 14 repete a causa de inicialização.

O critério demonstrado pelos CSVs é **imobilidade**, operacionalizado pelo analisador. Não foram acrescentados ao repositório os logs brutos necessários para verificar independentemente a mesma causa de infraestrutura em todas as seis tentativas. Isso não invalida a exclusão descrita nem modifica os totais; limita o nome causal do desfecho.

Recomendo chamar 154/160 de **fração de tentativas que atenderam ao critério de movimento**, ou apresentar a classificação de infraestrutura como diagnóstico dos autores acompanhado de sua evidência. É um ajuste de relato, não motivo para recolher os dados novamente.

No resumo, na introdução e na legenda da Tabela 2, “ten runs per configuration” pode ser refinado para **“ten attempted runs per configuration”**, já que o n analisado varia. A seção de resultados já esclarece essa diferença; harmonizar a terminologia evita uma ambiguidade residual.

## 7. E5 e N2: causas agora sustentadas

A descrição de E5 foi corrigida nas pp. 12–13. Ela informa que três execuções tiveram falha reativa, duas apresentaram um início adicional de investigação e concluíram os cinco alvos, e a terceira terminou com quatro créditos sem nova tentativa registrada para o alvo falho.

E5 repetição 6 continua sendo o exemplo decisivo: o alvo 4 termina como falha de navegação e não há início posterior para ele. O texto agora corresponde ao registro. A ressalva de que os dois inícios adicionais não demonstram uma política geral de retry também foi incorporada. **Essa pendência está encerrada.**

Em N2, as seis rejeições por distância continuam rastreáveis nas repetições 2, 5, 7, 8 e 9, incluindo duas na repetição 7. As distâncias rejeitadas ficam entre 3,33 e 3,56 m, acima do limiar de 3,30 m. A análise sustenta a perda de créditos na etapa de confirmação, sem confundir rejeição geométrica com timeout ou aborto.

Essas observações não transformam o proxy em inspeção física validada, mas o artigo já declara essa limitação. Não reabro uma exigência de orientação, qualidade de imagem ou permanência fisicamente verificada para um trabalho que delimitou sua contribuição à navegação e decisão.

## 8. Formalização, contribuição, robustez e apresentação

### 8.1. Formalização do campo

A p. 5 agora inclui ε = 10⁻³, período de decaimento de 1 s, λ = 0,85, saturação interna dos acumuladores e tratamento do conjunto vazio. A Tabela 3 acompanha os parâmetros. A descrição de saturação deixou de agir apenas sobre a leitura e passou a corresponder à memória limitada implementada.

Considero encerrada a divergência principal entre equações e memória dos dois canais. Como pequeno refinamento, a frase sobre conjunto vazio pode dizer explicitamente que **cada canal** permanece retido ou decai quando seu próprio conjunto elegível está vazio, permitindo que o outro seja atualizado normalmente. Isso é precisão de notação, sem evidência de defeito experimental.

A distinção entre campo e tabela Q continua correta: não há política de exploração atuando no robô, as ações discretas são inferidas e a navegação vem das metas Nav2. A equivalência da modulação com aumento de recompensa e a ausência de garantias de invariância/convergência seguem explícitas. Não se exige conectar Q à execução para sustentar a contribuição reposicionada.

### 8.2. Originalidade e comparadores

O artigo oferece uma contribuição de integração e análise experimental de supervisão deliberativa–reativa. Sua originalidade demonstrada permanece **moderada**: não há comparação com uma heurística de igual simplicidade, utilizando o mesmo controlador, que isole a vantagem específica da ponderação afetiva.

A comparação APF é útil como referência de sistema, e a discussão das pp. 11–12 reconhece a diferença de controlador e parâmetros. As ablações mostram que keepout resolve o perigo estático e que recuo isolado oscila. O ensaio dinâmico acrescenta evidência de margem de afastamento em situação de preempção.

Essas limitações são anteriores e assumidas. Não imponho agora PPO, DDQN, uma nova política Q ou outro comparador como condição adicional de encerramento. Um revisor pode continuar julgando a originalidade insuficiente; este parecer não garante aceitação. Mas essa avaliação deve incidir sobre a contribuição de integração declarada, sem atribuir ao artigo uma promessa de novo operador de aprendizagem que ele retirou.

### 8.3. Estabilidade e robustez

O resíduo completo e sua agregação entre execuções continuam adequados para a alegação limitada de estabilidade empírica. O gerador da Figura 7 permanece disponível. Não há uma prova de convergência, e o manuscrito não deve ser avaliado como se a oferecesse.

A análise de ruído, o cenário denso, o conflito e o perigo emergente delimitam um conjunto útil de testes. Não demonstram generalização para mapas arbitrários, deriva de localização ou percepção física. Essas limitações estão descritas. A promessa de varredura de raio foi retirada conforme solicitado; não há motivo para exigir novos resultados somente para preservar uma frase já removida.

### 8.4. Harmonização de linguagem ainda necessária

O resumo e a conclusão melhoraram claramente, com resultados explícitos de 4/9 e 9/10 e ausência de entradas observadas na região de contato. Entretanto, persistem trechos antigos:

| Localização | Expressão ou ideia | Ajuste recomendado |
|---|---|---|
| P. 2, contribuições | “temporary deliberative keepout” e sequência posterior ao recuo | Descrever keepout persistente acionado por detecção, coerente com a p. 6 |
| P. 2, introdução/contribuições | “safety is maintained throughout” | Usar a descrição observacional adotada no resumo |
| P. 13, V-F/V-H/V-I | “safety is maintained”, “safety is unaffected” e perda de completude “but not safety” | Referir-se aos contatos e às margens medidas, sem ampliar para segurança geral |
| Pp. 13 e 15 | “degrades gracefully” | Preferir os números de completude já publicados |
| Pp. 2, 8 e 14 | “no-value ablation” | Usar “η = 0 ablation” ou “without affective value modulation”; E0 não desliga toda a tabela Q |

Não são novos problemas causados pelos reparos. São expressões antigas que ficaram em outras partes do manuscrito após a correção do resumo e da conclusão.

### 8.5. Literatura e apresentação

A revisão de literatura e a tabela comparativa permanecem ampliadas em relação ao artigo original, com 21 referências e reconhecimento da tradição de navegação híbrida. Mantive a avaliação anterior: a principal questão remanescente é a diferenciação científica da integração, não uma contagem mínima de referências. Não fiz uma nova busca bibliográfica exaustiva nesta rodada.

As equações da p. 5 estão legíveis, sem a invasão de coluna que ocorreu em versões anteriores. A Tabela 10 foi deslocada para uma p. 16 isolada, com grande espaço em branco. Esse é um ajuste opcional de composição; não compromete os valores nem constitui bloqueio científico. Conferir também remissões a V-H quando o texto trata de E5 ou de Avoid, discutidos em outras subseções.

Os campos editoriais zerados identificam melhor o caráter de manuscrito. Não é necessário inventar DOI, volume ou datas reais para corrigir placeholders; a adequação ao template de envio deve ser tratada na preparação final.

## 9. Proveniência: avanço real, com duas ressalvas documentais

`PROVENANCE.md` distingue os lotes reaproveitados de E5/DHa/DHb recoletados, informa seeds e aponta checksums. `CHECKSUMS.sha256` lista os 160 arquivos atuais. Esses artefatos melhoram a possibilidade de identificar exatamente os dados usados. [Manifesto][provenance] e [checksums][checksums].

Há duas precisões a observar:

1. **Versão de referência e versão efetivamente usada na coleta devem ser distinguíveis.** O manifesto chama de código de coleta o commit da terceira rodada para arquivos de datas anteriores. Os pareceres anteriores já constataram reaproveitamento entre rodadas. Identificar o snapshot que contém e reproduz um lote é útil, mas não demonstra sozinho que todo o código desse snapshot foi usado em sua execução original. Quando houver reaproveitamento, registrar essa distinção e a justificativa de compatibilidade.
2. **O diretório dos arquivos substituídos é declarado como fora da árvore versionada.** `results/_pre_rerun_P0/` não está disponível no snapshot público consultado. Os arquivos anteriores podem ser identificados em commits anteriores; citar esses caminhos e commits públicos é mais útil ao leitor que depender de um diretório local inacessível.

A linha da quinta rodada ainda remete à tag móvel. O commit fixo que deve identificar o pacote examinado aqui é `e7c04223c31695aee7a6074d6e67cfe32edd2e02`. No texto, prefira remeter às versões de referência do manifesto em vez de dizer primeiro que uma tag única é a versão exata que produziu todos os resultados.

Esses refinamentos não anulam os checksums verificados nem justificam repetir as missões. Considero a providência pedida na quarta rodada **substancialmente atendida**, sem equiparar a publicação do manifesto a uma certificação independente de toda a história de coleta.

## 10. Atendimento aos revisores originais

“Atendido no escopo” significa que a contribuição foi delimitada de forma compatível com a evidência. “Parcial” não equivale automaticamente a pedir novos experimentos.

### Revisor 1

| Item | Situação na quinta rodada | Fundamentação |
|---|---|---|
| R1.1 — teoria/convergência | **Atendido no escopo** | Alegação empírica, sem herdar garantias de Q-learning |
| R1.2 — estatística/multiplicidade | **Atendido no método** | Contagens corrigidas; resta substituir figura antiga |
| R1.3 — robustez | **Parcial, limite explícito** | Ruído e cenários dirigidos; generalização ampla não demonstrada |
| R1.4 — resíduo e várias execuções | **Atendido para estabilidade empírica** | Resíduo completo, agregação e gerador publicados |
| R1.5 — literatura comparativa | **Parcial, avançado** | Síntese ampliada; originalidade de integração continua moderada |
| R1.6 — custos e utilidade | **Atendido no núcleo** | Tempo, distância e adiamento apresentados |
| R1.7 — resumo | **Atendido no núcleo** | Papel de Q, completude e contatos observados bem delimitados |

### Revisor 2 — comentários maiores

| Item | Situação | Fundamentação |
|---|---|---|
| R2.1 — papel de Q e ablação | **Atendido no reposicionamento** | Comando efetivo e η = 0 claros |
| R2.2 — shaping/dupla contagem | **Atendido** | Equivalência e moderação da novidade mantidas |
| R2.3 — significado de η | **Atendido no escopo** | Não apresentado como política aprendida atuante |
| R2.4 — estabilidade | **Atendido na alegação limitada** | Não confunde resíduo observado com convergência |
| R2.5 — comparadores | **Parcial, limitação assumida** | APF e ablações úteis; ausência de heurística com mesmo controlador |
| R2.6 — segurança/recuperação | **Muito avançado** | Ativação corrigida e desfechos auditáveis; ajustar a atribuição temporal de TTC |
| R2.7 — estatística/dados | **Próximo de encerrar no escopo** | n correto, dados e manifesto presentes; Figura 5 ainda contraditória |
| R2.8 — inspeção/identidade/falhas | **Atendido no núcleo avaliado** | Proxy explícito, créditos separados, falhas e adiamentos auditáveis; limites assíncronos reconhecidos |
| R2.9 — alegações | **Parcial, próximo de encerrar** | Resumo, conclusão e E5 corrigidos; harmonizar frases residuais |
| R2.10 — literatura | **Parcial, avançado** | Ampliada; diferenciação arquitetural permanece o ponto de julgamento |

### Revisor 2 — comentários menores

| Item | Situação | Fundamentação |
|---|---|---|
| R2.m1 — raio/chattering | **Atendido quanto à correção de relato** | Mecanismos descritos e promessa de varredura retirada; sem garantia geral de ausência de oscilação |
| R2.m2 — argmax/formalização | **Atendido no núcleo** | Dois canais, memória, parâmetros e saturação explicitados |
| R2.m3 — dependência de Φ | **Atendido quanto à ação** | Memória temporal continua uma ressalva de representação, sem política Q atuante |
| R2.m4 — zero no baseline | **Atendido** | Atualização inativa explicada |
| R2.m5 — reprodução | **Substancialmente atendido** | Seeds, commits de referência, checksums e auditoria; completar precisão da proveniência |
| R2.m6 — metadados | **Ajuste de preparação final** | Campos zerados distinguem template de publicação |

### Revisores 3 e 4

| Item | Situação | Fundamentação |
|---|---|---|
| R3.1 — benefício de Bellman | **Atendido quanto à distinção causal** | Navegação atribuída ao supervisor |
| R3.2 — perigo na rota | **Atendido no ensaio solicitado** | RHM/RHB e ablações disponíveis |
| R3.3 — estabilidade/convergência | **Atendido no escopo** | Interpretação empírica e agregação |
| R4.1 — η = 0 e reformulação | **Atendido no núcleo** | Título e contribuição alinhados ao mecanismo |
| R4.2 — baseline reativo | **Parcial, limitação assumida** | APF presente; não isola a ponderação com mesmo controlador |
| R4.3 — segurança/conflito | **Muito avançado** | Conflito, ativação e auditabilidade presentes; qualificar TTC e linguagem residual |
| R4 menor — fronteira/oscilação | **Parcial, adequadamente delimitado** | Histerese, compromisso e limite KOb discutidos |
| R4 menor — estatística degenerada | **Atendido** | Métodos inadequados centrais corrigidos |
| R4 menor — ordem das figuras | **Atendido** | Sequência correta no agradecimento |

## 11. Problemas antigos, novos e encerrados

| Item | Origem | Consequência nesta rodada |
|---|---|---|
| Figura 5 antiga | **Já existia na quarta rodada** | Continua pendente no PDF anexado |
| TTC global apresentado como equivalente ao pós-ativação | **Pendência anterior parcialmente reformulada** | A nova auditoria permitiu demonstrar uma contribuição anterior à ativação; não foi causada por uma mudança de controle |
| Coordenadas/relógios da auditoria | Problemas acrescentados na quarta rodada | **Resolvidos agora** |
| Ausência de fins de Avoid | Pendência anterior | **Resolvida para Stay Alert e para os casos DHa centrais** |
| Contagem global da bateria | Erro de atualização da quarta rodada | **Resolvido agora** |
| Narrativa de retry em E5 | Pendência anterior | **Resolvida agora** |
| Saturação/parâmetros do campo | Pendência anterior | **Resolvida no núcleo** |
| Cobertura de Avoid no APF | Limitação identificada na nova extensão do parser | Ajuste menor de escopo da auditoria; sem efeito demonstrado na navegação |
| Proveniência e expressões antigas no corpo | Pendências anteriores, reduzidas | Precisão documental e harmonização de linguagem |
| Regressão do controlador | **Não identificada** | Código operacional inalterado desde a quarta rodada |

O saldo é positivo. **A nova versão corrigiu mais problemas do que deixou abertos.** A descoberta de um TTC registrado antes da ativação não significa que a auditoria nova criou esse comportamento: ela tornou verificável uma limitação que já estava nos dados e no coletor.

## 12. Critérios de encerramento desta rodada

| Prioridade | Correção | Evidência suficiente para encerrar | Nova coleta? |
|---|---|---|---|
| **Obrigatória** | Substituir a Figura 5 no PDF | E5 sem três inspeções e sem 440 s; distribuição coerente com os CSVs | **Não** |
| **Obrigatória** | Remover a equivalência temporal não demonstrada de TTC | Métrica e conclusão explicitamente de missão inteira; nenhuma alegação de janela pós-ativação não recalculada | **Não** |
| Recomendada antes do envio | Harmonizar segurança, keepout e “no-value” no corpo | Mesmas definições do resumo, método e conclusão | **Não** |
| Recomendada antes do envio | Precisar imobilidade, escopo APF e proveniência | Texto compatível com o que o pacote efetivamente comprova | **Não** |
| Editorial | Ajustar paginação da Tabela 10 e remissões | PDF final legível e referências internas corretas | **Não** |

Não acrescento como exigência uma nova política de aprendizagem, prova de convergência, validação física, nova varredura de mapas ou repetição completa da bateria. Se os autores quiserem defender um efeito de TTC estritamente pós-ativação, será outra alegação e exigirá a métrica correspondente. Para o escopo global agora adotado, a correção textual indicada é suficiente.

## 13. Julgamento final

| Critério | Avaliação |
|---|---|
| Relevância | **Boa** |
| Clareza da contribuição | **Boa**, com Q devidamente secundário |
| Originalidade demonstrada | **Moderada**, centrada em integração e avaliação |
| Correção operacional | **Preservada nos reparos já verificados**, sem regressão identificada |
| Formalização | **Melhor alinhada ao código** |
| Estatística | **Consistente no escopo**, com resultados inalterados e denominadores corrigidos |
| Segurança | **Evidência útil e auditável**, limitada aos proxies e à janela medida |
| Reprodutibilidade | **Melhora substancial**, principalmente nos episódios |
| Apresentação | **Boa, com Figura 5 obrigatoriamente a corrigir** |
| Recomendação | **Favorável à submissão após ajustes pontuais** |

Este parecer não repete o bloqueio estrutural da terceira rodada nem exige outra rodada de experimentos. A revisão atual deixou um conjunto pequeno e verificável de correções. Após substituir a figura efetivamente incluída no PDF, retirar a equivalência temporal não sustentada de TTC e harmonizar a redação, considero o manuscrito tecnicamente em condição de encaminhamento dentro do escopo de supervisão deliberativa–reativa declarado.

[repo]: https://github.com/voidmmn/tese_react_nav/tree/e7c04223c31695aee7a6074d6e67cfe32edd2e02
[audit]: https://github.com/voidmmn/tese_react_nav/blob/e7c04223c31695aee7a6074d6e67cfe32edd2e02/results/audit_trail.csv
[auditgen]: https://github.com/voidmmn/tese_react_nav/blob/e7c04223c31695aee7a6074d6e67cfe32edd2e02/src/tese_nav/scripts/gerar_auditoria.py
[boxplots]: https://github.com/voidmmn/tese_react_nav/blob/e7c04223c31695aee7a6074d6e67cfe32edd2e02/src/tese_nav/scripts/gerar_boxplots.py
[statistics]: https://github.com/voidmmn/tese_react_nav/blob/e7c04223c31695aee7a6074d6e67cfe32edd2e02/src/tese_nav/scripts/analise_estatistica.py
[dha4]: https://github.com/voidmmn/tese_react_nav/blob/e7c04223c31695aee7a6074d6e67cfe32edd2e02/results/metrics_DHa_20260910_202848.csv
[provenance]: https://github.com/voidmmn/tese_react_nav/blob/e7c04223c31695aee7a6074d6e67cfe32edd2e02/results/PROVENANCE.md
[checksums]: https://github.com/voidmmn/tese_react_nav/blob/e7c04223c31695aee7a6074d6e67cfe32edd2e02/results/CHECKSUMS.sha256
