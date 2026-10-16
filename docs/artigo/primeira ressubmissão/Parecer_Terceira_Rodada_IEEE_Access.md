# Parecer técnico — terceira rodada de avaliação

**Artigo:** *A Two-Layer Deliberative–Reactive Architecture with an Affective Attraction–Repulsion Layer for Autonomous Substation Inspection*  
**Autores:** Milton Miranda Neto e Alexandre Cardoso  
**Versão avaliada:** arquivo com sufixo `(2)`, 15 páginas  
**Data:** 10 de setembro de 2026  
**Referência de comparação:** pareceres da primeira e da segunda rodada e comentários originais dos quatro revisores  
**Natureza:** avaliação independente com critérios de revisão da IEEE Access; não representa decisão editorial da revista.

**Recomendação: ainda não submeter esta versão. A revisão resolveu várias objeções centrais, mas duas falhas de implementação comprometem o novo ensaio e a recuperação após falhas de navegação.**

O avanço é concreto: o resumo e a conclusão já reconhecem a perda de completude; a inspeção foi delimitada como proxy; o TOST indevido para duas amostras constantes foi retirado; a descrição do keepout ficou mais fiel; e foram acrescentadas vinte execuções para investigar o benefício do recuo diante de um perigo emergente. Os dados disponíveis agora permitem reproduzir as estatísticas de dezesseis configurações.

Entretanto, o novo perigo pode entrar no keepout **antes da ativação descrita no artigo**, e o tratamento imediato de aborto mantém um resultado de falha entre episódios, podendo encerrar uma investigação nova por causa da anterior. São problemas verificáveis, não pedidos genéricos para aumentar o número de experimentos. Além deles, permanecem inconsistências específicas entre formalização, registros publicados e interpretação de algumas métricas.

## 1. Como esta rodada foi conduzida

Mantive os mesmos critérios: contribuição científica, correção matemática e operacional, validade da inspeção e da segurança, desenho experimental, estatística, reprodutibilidade, robustez, literatura, apresentação e atendimento aos revisores.

Li o novo PDF e comparei suas mudanças com as pendências do segundo parecer. Inspecionei visualmente páginas com equações, figuras e tabelas. Consultei o repositório indicado pelo manuscrito, cuja referência `v1.0-resubmission` resolve nesta rodada para o commit **`c142b3fd5a3a8106d8a51fa9ccabbd08bb9948d8`**. [Versão auditada](https://github.com/voidmmn/tese_react_nav/tree/c142b3fd5a3a8106d8a51fa9ccabbd08bb9948d8).

O pacote contém **160 CSVs**: os 140 arquivos da rodada anterior têm hashes idênticos aos já examinados, e há vinte novos arquivos, dez DHa e dez DHb. Reutilizei os valores anteriormente extraídos dos arquivos inalterados, li integralmente os vinte novos e executei a análise atual sobre os valores finais das 160 tentativas. Portanto, não estou presumindo que os 140 experimentos tenham sido refeitos.

Também executei verificações isoladas das funções relacionadas a keepout, entrada/saída de investigação, metas aceitas tardiamente e classificação de rotação. Não executei uma nova bateria no Gazebo. Os contraexemplos abaixo demonstram o comportamento das funções publicadas; a frequência desses problemas em missões completas exige registros ou experimentos adicionais.

As páginas citadas referem-se ao **novo PDF de 15 páginas**. Uso três estados: **atendido**, quando a objeção foi resolvida no escopo declarado; **parcial**, quando resta uma limitação material; e **pendente**, quando falta a correção necessária. Também distingo correção do texto, correção do código e validação experimental: elas não são intercambiáveis.

## 2. Correções que considero confirmadas

| Pendência da segunda rodada | O que mudou | Avaliação nesta rodada |
|---|---|---|
| Resumo/conclusão afirmavam inspeção completa indiscriminadamente | Pp. 1–2 e 13 delimitam o cenário padrão e reconhecem E5/N2 | **Atendido quanto à contradição principal.** Permanecem expressões excessivas sobre segurança e degradação |
| Medida real aceitava 3,3 m, mas o texto anunciava standoff de 2 m | III-C e IV-C explicitam 3,3 m, dwell comandado e ausência de verificação independente de orientação/permanência | **Atendido como restrição de escopo da métrica.** Não equivale a validar inspeção física completa |
| TOST retornava p = 0 para duas amostras constantes | O script retorna ausência de resultado; Tabela 10 traz n/a para E3/N1 | **Atendido.** Não mantenho essa objeção como falha atual |
| Denominador de inspeção completa vinha do máximo observado | `TARGET_ANOM` usa o total definido por configuração | **Atendido para o problema estatístico.** Em DHa, distinguir tarefa deliberadamente adiada de falha indesejada |
| KOa/KOb faltavam no gerador estatístico | `CONFIGS` inclui as duas ablações e DHa/DHb | **Atendido** |
| Bateria em blocos não gerava todos os grupos | O script contém chamadas para as dezesseis configurações | **Atendido quanto à matriz completa** |
| Não havia ensaio do benefício transiente do recuo | DHa/DHb incluídos, com vinte novos CSVs | **Experimento acrescentado**, mas sua implementação não corresponde integralmente ao perigo emergente descrito |
| Keepout era chamado temporário e posterior ao recuo | Pp. 6–8 descrevem projeção na detecção e persistência até o fim da missão | **Atendido na descrição principal do cenário estático** |
| Meta de episódio antigo podia ser aceita sem cancelamento | `_on_goal_resp` cancela a meta aceita tardiamente | **Corrigido e confirmado em verificação isolada** |
| Rotação pura era classificada como parada | Inferência de ação passa a considerar rotação antes de concluir parada | **Corrigido no caso testado:** rotação positiva foi classificada como `left` |
| Argmax confundia índice e valor | Eqs. 4–5 separam evento selecionado e campo; incluem desempate e ausência de evento | **Corrigido formalmente nesse aspecto.** Ainda divergem da memória implementada |
| Fig. 7 não definia a faixa e descrevia picos inadequadamente | V-G define percentis entre execuções, interpolação e alargamento nos picos | **Atendido na descrição**, restando disponibilizar o processamento que gera a figura |
| Conclusão confundia estabilidade com convergência | P. 13 limita a afirmação a incrementos observados em simulações finitas | **Atendido** |
| Tabela classificava o método como active sensing sem qualificação | Tabela 1 passa a usar classificação parcial e explicita ausência de planejamento informativo de vistas | **Melhora adequada**, embora a célula esteja excessivamente estreita |
| Eq. 6 invadia a coluna vizinha | Equação foi quebrada | **Corrigido.** A nova Eq. 5 apresenta agora um problema de composição semelhante |

Esses avanços reduzem o número de objeções abertas. Não é necessário voltar a exigir uma política de aprendizado por reforço atuante se o artigo mantiver a contribuição como supervisão deliberativa–reativa e tratar a tabela Q como formulação secundária.

## 3. Novo ensaio DHa/DHb: os valores conferem

O ensaio da p. 11 pretende mostrar o que o recuo acrescenta quando um perigo aparece durante uma investigação. DHa habilita recuo e keepout; DHb mantém o keepout e desabilita o recuo.

| Métrica recalculada | DHa: recuo + keepout, n = 10 | DHb: keepout, n = 10 |
|---|---:|---:|
| Investigações iniciadas | 1,00 ± 0,00 | 1,00 ± 0,00 |
| Investigações adiadas por perigo | 1,00 ± 0,00 | 0,00 ± 0,00 |
| Inspeções creditadas | 0,00 ± 0,00 | 1,00 ± 0,00 |
| Eventos de recuo | 1,00 ± 0,00 | 0,00 ± 0,00 |
| Distância mínima ao perigo | **2,535 ± 0,132 m** | **2,224 ± 0,005 m** |
| Proxy radial mínimo de TTC | **5,067 ± 0,254 s** | **4,643 ± 0,095 s** |
| Tempo abaixo de 2 m | 0,00 ± 0,00 s | 0,00 ± 0,00 s |
| Entradas na região de contato | 0 em dez execuções | 0 em dez execuções |
| Duração registrada da missão | **347,746 ± 1,524 s** | **338,422 ± 0,743 s** |
| Distância percorrida | **85,200 ± 1,711 m** | **83,292 ± 0,116 m** |
| Eventos de navegação abortada | 0,30 ± 0,48; três execuções com um aborto | 0,00 ± 0,00 |

Pelo script publicado, o contraste **DHa − DHb** produz:

| Desfecho | Diferença | IC bootstrap de 95% | Cliff’s delta | p reproduzido |
|---|---:|---:|---:|---:|
| Distância mínima | +0,311 m | aproximadamente [0,24; 0,39] | 1,00 | **1,08 × 10⁻⁵** |
| Proxy radial de TTC | +0,424 s | aproximadamente [0,27; 0,58] | 0,92 | **1,30 × 10⁻⁴** |
| Tempo abaixo de 2 m | 0,000 s | [0; 0] | 0,00 | 1,00 |

As médias, diferenças e intervalos principais apresentados na p. 11 conferem. Porém, o texto afirma **p < 10⁻⁴ também para TTC**, o que não corresponde ao p reproduzido de 1,30 × 10⁻⁴. Corrigir para o valor numérico. Isso não elimina a evidência de diferença no nível usual de 5%, mas precisa ser corrigido.

O custo do recuo no novo ensaio também deve ser apresentado: aproximadamente **9,32 s adicionais**, ou 2,8% sobre DHb, e **1,91 m adicionais**, além de adiar a inspeção. A escolha operacional é obter maior afastamento ao custo de tempo, distância e não concluir a inspeção naquele encontro. Esse resultado é mais informativo que apresentar apenas o ganho de folga.

Não interpreto 0/10 inspeções em DHa automaticamente como mau desempenho: o alvo se tornou perigoso e a política opta por adiar. É necessário distinguir **conclusão de inspeção**, **resposta correta ao perigo** e **conclusão da patrulha**. A métrica de completude deve continuar transparente, sem trocar o denominador depois de observar o resultado.

[Análise estatística na versão examinada](https://github.com/voidmmn/tese_react_nav/blob/c142b3fd5a3a8106d8a51fa9ccabbd08bb9948d8/src/tese_nav/scripts/analise_estatistica.py).

## 4. Pendência crítica: o keepout conhece o perigo antes de ele “surgir”

**Localização:** pp. 8 e 11; `AnomalySimulator._check_proximity` e `_emit_keepout`.

O PDF descreve um perigo inativo até o robô alcançar 3 m. No código, a condição `activate_radius = 3.0` controla a publicação do **sinal reativo de perigo**, mas não controla a projeção no keepout.

O ciclo de percepção chama `_emit_keepout` antes de processar a ativação dinâmica. Essa função percorre os perigos e projeta suas posições quando entram no raio de 5 m, sem consultar se o perigo dinâmico está ativo. A marca permanece no costmap.

**Verificação isolada realizada:** configurei um perigo com ativação a 3 m, coloquei o robô a 4 m, deixei o conjunto de perigos ativos vazio e executei `_emit_keepout`. O resultado foi uma marca no keepout e uma publicação de nuvem de pontos, embora o perigo continuasse inativo para o canal reativo.

| Condição do teste isolado | Resultado observado |
|---|---|
| Distância robô–perigo | 4 m |
| Raio de ativação dinâmica | 3 m |
| Perigo ativo no canal reativo | Não |
| Perigo retido no keepout | Sim |
| Nuvem de keepout publicada | Sim |

Assim, o ensaio publicado se aproxima de **ativação tardia da repulsão reativa em torno de um perigo que já podia estar representado no mapa**. Não corresponde integralmente ao aparecimento de um perigo anteriormente desconhecido para ambas as camadas.

Isso não torna fictício o ganho de 0,31 m, nem demonstra favorecimento exclusivo de um braço: ambos podem receber a mesma informação antecipada. Mas muda a pergunta experimental e enfraquece a interpretação como validação do benefício diante de um perigo realmente emergente. Também não é possível presumir que eliminar essa antecipação mantenha o mesmo tamanho de efeito.

**Correção recomendada:** a ativação ambiental deve ocorrer antes da distribuição da observação aos canais; apenas perigos ativos devem produzir sinal reativo e keepout. Registrar o instante de ativação, a primeira publicação para cada canal, o início da preempção e o estado do robô. Reexecutar DHa/DHb após a correção, preservando o conjunto anterior.

Uma alternativa é manter o experimento e renomeá-lo explicitamente como ativação tardia de resposta reativa para perigo previamente mapeado. Essa alternativa, porém, deixa aberta a hipótese de perigo emergente que motivou a adição do ensaio.

**Métrica temporal associada:** o coletor calcula distância e TTC sobre a lista de perigos do cenário desde o início, sem filtrar sua ativação. Para a hipótese transiente, apresentar também métricas na janela **após a ativação**. O mínimo de missão inteira pode incorporar aproximação anterior ao surgimento do perigo. O log atual de contadores não oferece o instante exato de ativação para separar essas janelas de forma inequívoca.

[Implementação de ativação e keepout](https://github.com/voidmmn/tese_react_nav/blob/c142b3fd5a3a8106d8a51fa9ccabbd08bb9948d8/src/tese_nav/tese_nav/anomaly_simulator.py) e [coletor de segurança](https://github.com/voidmmn/tese_react_nav/blob/c142b3fd5a3a8106d8a51fa9ccabbd08bb9948d8/src/tese_nav/tese_nav/metrics_node.py).

## 5. Pendência crítica: uma falha anterior pode encerrar a investigação seguinte

**Localização:** III-C, Algoritmo 1 e `StayAlertNode._enter/_update`.

A nova versão encerra imediatamente Investigate quando `_nav_outcome` indica aborto, cancelamento ou rejeição. Essa é a correção solicitada na segunda rodada. Entretanto, `_enter` não reinicializa `_nav_outcome` ao começar um novo episódio.

Um encadeamento possível é:

1. Uma navegação termina abortada e deixa `_nav_outcome` com esse resultado.
2. O episódio é encerrado.
3. O robô inicia outra investigação e envia uma nova meta.
4. Antes de receber o resultado da nova meta, `_update` lê a falha antiga e encerra a investigação nova como falha.

**Verificação isolada realizada:** iniciei um episódio novo após um resultado anterior de aborto e mantive a nova resposta de navegação pendente. O estado de aborto permaneceu após `_enter`; no ciclo seguinte, com apenas 0,2 s de episódio, a função pediu a saída por falha. Não foi necessário simular uma nova falha do Nav2.

**Correção:** reinicializar o resultado de navegação na entrada de cada episódio e associar resultado/estado ao mesmo identificador de meta ou episódio. Testar a sequência completa “primeira meta falha → segunda meta é aceita e alcançada”. Manter a proteção por época e o cancelamento de aceitação tardia, que foram corrigidos corretamente.

Há uma segunda inconsistência ligada à mesma alteração. O supervisor agora emite término com motivo `failed`, mas o avaliador de anomalias só adiciona explicitamente ao conjunto `failed` os términos por timeout ou as rejeições de confirmação. Ao receber o novo motivo, limpa o alvo ativo sem classificá-lo nesse conjunto.

**Verificação isolada:** um alvo comprometido recebeu término com motivo de falha; permaneceu em `committed`, não entrou em `failed` e deixou de ser o alvo ativo. Isso contraria a separação de estados prometida no texto.

Além disso, o coletor passou a contar tanto timeout quanto o motivo genérico de falha dentro de `investigation_timeouts`. O nome deixa de representar uma causa específica. Separar falhas por causa ou renomear o total para investigações malsucedidas, mantendo contadores próprios de timeout, aborto, rejeição e falha de confirmação.

**Por que importa para esta revisão:** os 140 CSVs anteriores foram preservados, e E5 contém abortos reais registrados naquela bateria. A lógica de encerramento mudou; logo, é necessário esclarecer quais resultados correspondem a qual versão e revalidar os casos afetados. Não basta informar a tag atual como se todas as execuções tivessem usado o mesmo comportamento de falha.

[Supervisor na versão auditada](https://github.com/voidmmn/tese_react_nav/blob/c142b3fd5a3a8106d8a51fa9ccabbd08bb9948d8/src/tese_nav/tese_nav/stay_alert_node.py).

## 6. Inspeção, identidade e causas de falha: o escopo melhorou, a auditoria ainda falta

### 6.1. A opção por um proxy é aceitável, se aplicada em todo o artigo

O autor escolheu uma das alternativas oferecidas no segundo parecer: limitar a métrica ao que efetivamente é verificado. Agora são declarados sucesso de navegação, espera comandada e posição final a até 3,3 m do alvo verdadeiro, sem certificação independente de orientação e permanência durante o dwell.

**Não considero obrigatório implementar sensores reais ou uma verificação física completa para publicar um estudo de navegação simulado.** Considero necessário que o nome e a interpretação permaneçam compatíveis com esse proxy. Uma denominação como “visitas de inspeção confirmadas pelo proxy” na primeira definição e uma remissão nas tabelas reduziriam o risco de o leitor interpretar “inspected” como diagnóstico instrumental completo do equipamento.

Ainda falta justificar a tolerância de 1,3 m além do standoff nominal. Se ela vem de requisitos de navegação ou de observação, documentá-los; se foi escolhida para a avaliação, explicitar essa escolha e reconhecer sua influência sobre N2. Não é obrigatório aumentar a campanha experimental para isso, mas o limiar não deve parecer uma propriedade física demonstrada.

### 6.2. Os logs por episódio anunciados não estão no pacote consultado

Nas pp. 8–9, o artigo afirma disponibilizar, ao lado de cada CSV, um log com identidade, posição verdadeira, alvo comprometido, confirmação/rejeição e resultado da navegação. Na árvore pública examinada, **não há arquivos de log por execução nem registros adicionais de eventos em `results`**; estão os CSVs e o resumo. O código contém mensagens que poderiam compor esses logs, mas sua existência no código não equivale à disponibilização dos arquivos que documentam a coleta.

Em N2, os números sustentam **27 investigações iniciadas e 21 inspeções creditadas**, sem timeout ou aborto registrado nas nove válidas. Isso torna plausível a explicação de seis rejeições na etapa de confirmação. Não permite, sozinho, certificar a causa de cada uma. A afirmação da p. 12 de atribuição “precisa” deve ser apoiada pelos seis episódios efetivamente publicados ou descrita como inferência a partir dos contadores e do código.

A correção pode ser pequena: disponibilizar os logs já existentes ou uma tabela de auditoria com execução, ID do alvo, distância final, limite aplicado, estado de navegação, instante e motivo do não crédito. Não é necessário criar novas métricas sem relação com a objeção.

### 6.3. A explicação de E5 permanece incompatível com o detalhe dos contadores

V-F, p. 12, continua atribuindo a perda de completude à saída do layout antes de revisitar cada evento. Nas duas execuções incompletas já identificadas no segundo parecer:

| Execução E5 | Iniciadas | Creditadas | Timeouts registrados | Abortos de navegação |
|---|---:|---:|---:|---:|
| `metrics_E5_20260909_162649.csv` | 5 | 3 | 2 | 1 |
| `metrics_E5_20260909_170733.csv` | 5 | 4 | 1 | 1 |

Todos os cinco alvos tiveram investigação iniciada. A explicação precisa discutir tentativas que não concluíram, e não apenas ausência de revisita. Aborto e timeout podem se referir ao mesmo episódio e não devem ser somados como falhas independentes. Densidade pode contribuir para a dificuldade, mas o nexo causal precisa ser explicado pelos episódios.

### 6.4. Identidade assíncrona foi reconhecida, mas não demonstrada

A p. 13 reconhece que ID e pose são publicados separadamente e deixa a sincronização robusta para refinamento futuro. Isso é mais transparente. Porém, a afirmação de que os casos avaliados têm dinâmica de um único alvo saliente não resolve por si só E5, cuja motivação é justamente haver vários eventos no alcance.

Não afirmo que os alvos tenham sido trocados nas missões publicadas. Falta demonstrar que o ID creditado e a pose navegada correspondem à mesma observação. Os logs por episódio podem encerrar essa dúvida para a bateria já realizada; uma mensagem conjunta com identidade e timestamp resolve melhor o requisito operacional futuro.

## 7. Segurança e contribuição do recuo: como interpretar sem exagero

O texto de V-D, p. 11, melhorou bastante: distingue prioridade de seleção de garantia física e explicita pose disponível, refratário e situações não testadas. Essa correção deve ser preservada.

No resumo, introdução e V-H ainda aparecem expressões como segurança mantida em todos os casos e segurança não afetada pelo ruído. Mesmo quando acompanhadas por “zero collisions”, elas condensam uma propriedade mais ampla em um único proxy. A redação mais precisa é **não foram observadas entradas na região de contato, sob as condições simuladas**, seguida dos valores de distância e exposição relevantes.

RHM continua passando cerca de 9,2 s abaixo do limiar de 2 m. DHa e DHb ficam ambos acima desse limiar e não entram na região de contato. Portanto, o ganho de DHa representa maior margem medida; não corresponde a uma redução observada de violações ou contatos no ensaio. Definir um limiar operacional relevante ajuda a explicar por que 0,31 m adicionais importam, sem inventar uma utilidade posterior para favorecer um braço.

O artigo agora reconhece que o recuo não traz benefício mensurável no cenário estático frente a KOa. Isso responde à crítica anterior. A hipótese de que o benefício aparece no transiente é pertinente e testável, mas precisa da correção da ativação descrita na seção 4.

Um resultado novo merece constar da avaliação: **três das dez execuções DHa registram um aborto de navegação**, ao mesmo tempo que `avoid_success` é um e `avoid_timeout` é zero. São as execuções com sufixos `112023`, `114221` e `114943`. Esses contadores não provam colisão nem ausência de afastamento; mostram que “sucesso do recuo” não é necessariamente sinônimo de meta de recuo atingida sem falha. O supervisor também pode encerrar Avoid pelo decaimento do sinal, especialmente após delegação ao keepout.

Publicar a associação entre aborto, meta e motivo de término permitirá separar: preempção acionada, movimento de afastamento observado, meta atingida, término por sinal reduzido e recuperação da missão. Não usar dez eventos de preempção como substituto de dez recuos fisicamente concluídos.

## 8. Estatística: correções atendidas e ajustes remanescentes

### 8.1. O TOST degenerado foi corrigido

A função agora retorna n/a quando o erro padrão é zero. E3/N1 deixa de ser apresentado como equivalência estatística e passa a ser desempenho observado idêntico. A Tabela 10 e o Apêndice B refletem a correção. **Esta pendência está encerrada.**

Os TOST temporais E0 versus E2/E3/E4 continuam reproduzíveis, com p aproximadamente 8,63 × 10⁻⁷, 4,09 × 10⁻⁷ e 1,62 × 10⁻⁸, respectivamente. Justificar a margem de ±5 s e informar a unidade experimental/independência permanece adequado. O p de 0,75 em E3/N2 indica ausência de evidência de equivalência pelo procedimento usado, não prova autônoma de não equivalência.

### 8.2. Os intervalos de sucesso são Wilson; o limite de risco foi rotulado incorretamente

Os intervalos de completude de E5 e N2 estão corretamente identificados como Wilson. Porém, na p. 13, o manuscrito chama os limites de aproximadamente **26% para n = 10 e 28% para n = 9** de limites unilaterais de Wilson de 95%.

Esses números correspondem ao limite binomial **exato unilateral**, calculado como `1 − 0,05^(1/n)` para zero falhas. Não são os limites unilaterais de Wilson.

| Zero falhas observadas | Exato unilateral de 95% | Wilson unilateral de 95% | Limite superior de Wilson bilateral de 95% |
|---|---:|---:|---:|
| n = 10 | 25,89% | 21,29% | 27,75% |
| n = 9 | 28,31% | 23,11% | 29,91% |

**Correção simples:** manter aproximadamente 26% e 28%, mudando o nome para limite binomial exato unilateral. Não é necessário usar o mesmo método para o intervalo descritivo de completude e para esse exemplo de limite de risco, desde que cada um seja identificado. A documentação distingue Wilson de Clopper–Pearson e os tipos de intervalo. [Métodos binomiais em statsmodels](https://www.statsmodels.org/stable/generated/statsmodels.stats.proportion.proportion_confint.html).

### 8.3. A nova descrição de Mann–Whitney ainda não coincide com o código

Na p. 8 permanece a formulação anterior de permutação exata para braços degenerados. Nas pp. 9–10 e no Apêndice B, passou-se a dizer que o procedimento é assintótico, exceto quando os dois braços constantes estão completamente separados.

O script, entretanto, também usa o método exato de Mann–Whitney em amostras sem empates com tamanho total de até vinte. Por isso, pares contínuos como distância mínima E1/E3 podem ter p exato mesmo sem ambos os grupos constantes. O procedimento não mudou nessa parte; os números continuam os mesmos, mas a descrição ficou incompleta de outra forma.

Sugestão de redação metodológica: identificar separadamente o caso especial de braços constantes, o cálculo exato sem empates e a aproximação assintótica com empates; declarar o método por contraste no suplemento. A diferença entre método exato, aproximação e permutação com empates é documentada no SciPy. [Mann–Whitney no SciPy](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.mannwhitneyu.html).

A correção de Holm da família original de sete comparações continua reproduzível. Os contrastes DHa/DHb foram acrescentados à família secundária no script. Apresentá-los como ensaio dirigido adicional/exploratório e explicitar a multiplicidade, sem sugerir que seus p já estejam incluídos na correção da Tabela 4.

### 8.4. N e resultados por tentativa

A taxa 156/160 = **97,5%** de tentativas classificadas como válidas está correta. É diferente de sucesso de inspeção ou conclusão da missão. APF, RHM e N2 têm nove válidas; KOb também. A Tabela 7 ainda deve informar explicitamente seus n: RHM 9, KOa 10, KOb 9.

A legenda da Tabela 5 informa dez válidas em E1–E5, mas convém incluir E0 explicitamente. Para N2, manter as duas perspectivas: 4/9 entre válidas e 4/10 por tentativa. A análise de missão deve separar o encerramento por limite de KOb do tempo até conclusão das demais configurações.

## 9. Formalização do campo e diagnóstico Q

A separação entre evento escolhido e valor do campo é uma correção adequada das Eqs. 4–5. O desempate pelo menor ID e o caso vazio também foram descritos. Entretanto, a formulação usa conjuntos de eventos elegíveis **no passo atual**, enquanto `AttractionField` conserva máximos anteriores em dois canais, com decaimento independente.

Um exemplo conceitual mostra a diferença: após um perigo observado anteriormente, sua memória pode continuar negativa mesmo quando, no passo atual, só há uma anomalia elegível. Pela Eq. 5, o campo passa à contribuição da anomalia atual; pelo código, a memória de perigo ainda domina até cair abaixo do limiar residual. Além disso, a chegada de um evento atual mais fraco não substitui necessariamente um máximo anterior.

Essa memória pode ser uma decisão de projeto legítima. A correção necessária é descrevê-la na matemática, incluindo os dois acumuladores, a ordem observação/decaimento, a saturação e o limiar residual. Como a proposta central depende do campo, essa correspondência é mais importante que refinar um diagnóstico Q que não atua.

O texto da p. 5 também deduz que Avoid dispara sempre que há perigo no alcance. As condições de intensidade, limiar do supervisor, pose disponível, refratário e habilitação do recuo precisam acompanhar essa afirmação. A versão mais cuidadosa já presente em V-D deve orientar a redação do método.

Quanto à tabela Q, a equivalência com aumento de recompensa permanece corretamente reconhecida. O problema de rotação pura foi corrigido e a descrição de ação inferida da odometria substituiu a antiga alegação de logging greedy. Restam pontos secundários:

- A recompensa chamada progresso continua constante por amostra de odometria. Nomear e explicar essa escolha, incluindo sua dependência da frequência.
- O estado com célula e módulo de Φ não representa todo o sinal, identidade e memória do campo. Evitar pressupor uma representação Markoviana completa; usar uma notação temporal ou explicitar a aproximação.
- E0 usa η = 0; isso remove o termo afetivo da atualização, mas não desliga toda a tabela Q. Chamá-lo ablação sem modulação afetiva é mais preciso que “sem valor” ou “sem Q”.

Não faço desses pontos secundários uma exigência de desenvolver um novo algoritmo de aprendizado. O escopo declarado permite uma avaliação de integração e supervisão, com Q claramente subordinado a ela.

[Campo implementado](https://github.com/voidmmn/tese_react_nav/blob/c142b3fd5a3a8106d8a51fa9ccabbd08bb9948d8/src/tese_nav/tese_nav/utils/attraction_field.py) e [atualização/inferência de ação](https://github.com/voidmmn/tese_react_nav/blob/c142b3fd5a3a8106d8a51fa9ccabbd08bb9948d8/src/tese_nav/tese_nav/bellman_node.py).

## 10. Reprodutibilidade e o que realmente precisa ser reexecutado

A publicação dos vinte novos arquivos e a inclusão das dezesseis configurações no gerador são avanços confirmados. A reprodução estatística da bateria principal e do ensaio adicional é possível. Isso deve ser reconhecido como um ponto favorável.

A pendência agora é **proveniência e correspondência de versão**, além dos logs ausentes. A mesma tag já apontou para conteúdos diferentes nas rodadas anteriores. O commit atual preserva os 140 CSVs e modifica o tratamento de falhas do controlador. Registrar um commit exato por lote, parâmetros e data é necessário para que a expressão “versão exata que produziu os resultados” seja verificável.

Não recomendo repetir as 160 tentativas indiscriminadamente. O mínimo justificável é:

1. Corrigir a ativação dos canais e repetir DHa/DHb, se a hipótese continuar sendo perigo emergente desconhecido.
2. Corrigir o resultado residual entre episódios e verificar recuperação após aborto/rejeição em uma sequência com mais de um alvo; reavaliar E5 e os casos afetados por essa mudança.
3. Para dados reaproveitados, declarar o código usado na coleta e justificar por que as alterações posteriores não modificam as métricas que estão sendo reutilizadas.
4. Publicar os registros por episódio usados para atribuir as seis rejeições N2 e as falhas E5/DHa.

Outras pendências do segundo parecer continuam localizadas:

- O limite nominal de 600 s no shell não mede diretamente todo o tempo decorrido, pois a consulta de conclusão também consome tempo. O campo decai por relógio monotônico e a métrica de duração usa relógio ROS. Documentar a relação entre relógios e tratar 627 s de KOb como tempo até interrupção, não tempo de missão bem-sucedida.
- As quatro tentativas imóveis continuam com deslocamento próximo de zero; a classificação observável é válida. Porém, três têm duração de missão acumulada no coletor. A frase “mission never started” deve distinguir missão sinalizada de início de movimento. O motivo de infraestrutura exige logs, não apenas distância.
- O artigo afirma que o script de análise produz boxplots. O script estatístico auditado produz resumos e comparações, mas não contém o gerador das figuras. Disponibilizar o comando/script correspondente à Fig. 5 e à Fig. 7, incluindo normalização e tratamento do fim de missão.

[Script de bateria completo](https://github.com/voidmmn/tese_react_nav/blob/c142b3fd5a3a8106d8a51fa9ccabbd08bb9948d8/rodar_bateria_blocos.sh).

## 11. Contribuição, comparadores, robustez e literatura

A discussão de APF, p. 11, agora reconhece expressamente que o comparador muda o controlador e usa parâmetros diferentes. O manuscrito limita a vantagem à implementação APF avaliada e deixa o supervisor heurístico com o mesmo Nav2/MPPI como trabalho futuro. Isso responde à crítica de causalidade excessiva dessa comparação.

Essa restrição tem uma consequência científica: o trabalho demonstra comportamento e desempenho de uma integração concreta, mas **ainda não demonstra superioridade da ponderação/memória afetiva sobre uma arbitragem simples equivalente**. Não é necessário tornar esse experimento uma exigência automática se o artigo assumir uma contribuição de integração; é necessário que o avanço reivindicado seja compatível com esse alcance. Se a novidade central continuar sendo a vantagem específica do campo afetivo, a comparação segue necessária.

KOa/KOb e DHa/DHb são comparadores mais informativos para decompor segurança. Depois da correção do novo ensaio, podem sustentar uma narrativa clara: keepout para contorno persistente; recuo para interromper aproximação sob ativação de perigo; inspeção reativa para alvos elegíveis. Essa narrativa deve substituir qualquer atribuição de benefício comportamental ao termo Bellman passivo.

O reposicionamento de active sensing na Tabela 1 melhorou. Ainda convém harmonizar resumo e introdução: a patrulha fixa transporta os sensores, mas não otimiza ganho de informação ou seleção de vistas. O reposicionamento por evento é real e pode ser descrito sem sugerir uma política de percepção ativa mais ampla.

A robustez permanece delimitada. E5 e N1/N2 revelam limites úteis; não sustentam generalização sobre várias geometrias, localização, latência ou persistência. “Graceful degradation” não deve substituir a informação de que a completude cai para 4/9 sob ruído alto. Também continua na p. 5 uma promessa de sensibilidade ao raio de detecção, embora não haja varredura de R apresentada. Remover a promessa ou apresentar a análise correspondente.

A literatura de 21 referências permanece pertinente como base. O argumento de originalidade deve se aproximar mais de supervisão híbrida, arbitragem e replanejamento por mapa de risco, em vez de depender de uma combinação nominal com Bellman. A referência [2] ainda usa ano 2025; o registro editorial anteriormente conferido informa publicação e citação em 2026. Corrigir o registro bibliográfico pelo editor. [Artigo de Zhang e colaboradores](https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2025.1759501/full).

Não realizei nova auditoria integral de todas as referências e não identifico necessidade de aumentar sua quantidade arbitrariamente.

## 12. Apresentação: ajustes concretos no PDF

A composição geral continua legível. As correções devem se concentrar nos seguintes pontos:

| Local | Verificação | Correção |
|---|---|---|
| Eq. 6, p. 5 | A sobreposição anterior foi resolvida | Preservar a quebra atual |
| **Eq. 5, p. 5** | A restrição de intervalo de Φ invade a coluna direita e sobrepõe o título sobre a tabela de valores | Quebrar a linha; mover saturação para texto ou equação separada |
| Tabela 1, p. 4 | A explicação de active sensing ocupa uma coluna estreita com muitas quebras | Usar rótulo curto e nota explicativa abaixo da tabela |
| Tabela 3, p. 8 | Inclui 3,3 m, refratário, keepout e parâmetros APF | Correção positiva; explicitar também o limiar de folga de 2 m e a semântica dos relógios |
| Tabela 7, p. 11 | Não informa n válido por braço | Acrescentar RHM 9, KOa 10, KOb 9 |
| DHa/DHb, p. 11 | Resultados importantes estão apenas no texto | Criar tabela compacta com efeito, custo, adiamento e abortos; integrar ao suplemento estatístico |
| Apêndice A, p. 14 | Tabela de eventos não inclui `dyn_hazard` | Acrescentar posição, intensidade e regra de ativação do novo cenário |
| Fig. 7, p. 12 | A legenda explica percentis; o gráfico usa rótulo genérico de faixa de 95% | Harmonizar rótulos e disponibilizar o gerador |
| Algoritmo 1, p. 7 | Ainda omite saída de Avoid por timeout | Alinhar ao código e às definições de sucesso/falha |
| Primeira página e rodapés | Datas e DOI de exemplo; “VOLUME 11, 2023” | Preparar a versão de submissão sem metadados editoriais fictícios |

O crescimento de 13 para 15 páginas decorre em parte das explicações adicionadas, mas há espaço para concisão. Evitar repetir justificativas de que a avaliação é rigorosa ou honesta; apresentar o procedimento e os limites diretamente. Conferir remissões: E5 é discutido em V-F, enquanto algumas legendas remetem genericamente à seção de ruído V-H.

## 13. Atendimento aos revisores originais — terceira rodada

### Revisor 1

| Item | Estado | Justificativa |
|---|---|---|
| R1.1 — propriedades teóricas/convergência | **Atendido no escopo adotado** | Ausência de garantia e estabilidade apenas empírica estão claras; não se exige uma prova de convergência para o supervisor |
| R1.2 — estatística, efeitos e multiplicidade | **Parcial, próximo de encerrar** | TOST degenerado corrigido; faltam rótulo do limite de risco, método por contraste e p de TTC DHa/DHb |
| R1.3 — robustez | **Parcial** | Novo teste é pertinente, mas ativação precisa ser corrigida; generalidade permanece limitada |
| R1.4 — resíduo completo e múltiplas execuções | **Parcial, muito avançado** | Agregação e faixa definidas; falta gerador público e comparação E0 se o diagnóstico Q continuar central |
| R1.5 — literatura e tabela comparativa | **Parcial, avançado** | Tabela mais honesta sobre active sensing; diferenciação frente a supervisores próximos ainda merece precisão |
| R1.6 — custo e utilidade | **Parcial, avançado** | KOa é reconhecido; acrescentar custo temporal/espacial e adiamento no ensaio novo |
| R1.7 — resumo alinhado | **Parcial, muito avançado** | Contradição sobre completude resolvida; qualificar segurança e “bounded” |

### Revisor 2 — comentários maiores

| Item | Estado | Justificativa |
|---|---|---|
| R2.1 — papel de Q e ablação | **Atendido no reposicionamento principal** | Não atuação de Q e ação inferida descritas; rotação pura corrigida |
| R2.2 — shaping e dupla contagem | **Atendido** | Equivalência com aumento de recompensa e ausência de dupla contagem reconhecidas |
| R2.3 — interpretação de η | **Atendido no escopo atual** | A varredura não é apresentada como sensibilidade de uma política aprendida atuante |
| R2.4 — estabilidade | **Parcial, muito avançado** | Métrica completa e interpretação adequadas; completar reprodução da figura |
| R2.5 — comparadores justos | **Parcial, explicitamente limitado** | APF é qualificado; vantagem específica do campo sobre heurística equivalente não demonstrada |
| R2.6 — segurança e recuperação | **Parcial crítico** | Ensaio dinâmico acrescentado, mas keepout recebe informação antes da ativação; três abortos DHa precisam de interpretação |
| R2.7 — estatística, dados e timeouts | **Parcial, avançado** | 160 arquivos e análise disponíveis; faltam proveniência por lote, logs e tratamento claro dos términos |
| R2.8 — inspeção, identidade e falhas | **Parcial crítico** | Proxy delimitado; nova falha de estado entre episódios e classificação incompleta do motivo `failed` |
| R2.9 — alegações e generalização | **Parcial, muito avançado** | E5/N2 reconhecidos em resumo/conclusão; limpar generalizações residuais de segurança e causas de E5 |
| R2.10 — revisão de literatura | **Parcial** | Base pertinente; contribuição de integração precisa ser diferenciada de arbitragem híbrida convencional |

### Revisor 2 — comentários menores

| Item | Estado | Justificativa |
|---|---|---|
| R2.m1 — fronteira do raio/chattering | **Parcial** | Histerese e compromisso descritos; promessa de sensibilidade ao raio permanece sem resultado |
| R2.m2 — argmax e seleção | **Atendido na notação; parcial na implementação** | Evento e valor separados, empate/vazio definidos; falta representar memória dos dois canais |
| R2.m3 — dependência de Φ | **Parcial** | Dependência da ação afastada; estado não representa toda a memória |
| R2.m4 — resíduo zero no baseline | **Atendido** | Atualização inativa é explicada |
| R2.m5 — reprodução | **Parcial, avançado** | Sementes e matriz completas; tag mutável, relógios e logs continuam pendentes |
| R2.m6 — metadados | **Pendente** | Datas, DOI e rodapé de exemplo permanecem |

### Revisores 3 e 4

| Item | Estado | Justificativa |
|---|---|---|
| R3.1 — benefício de Bellman | **Atendido quanto à distinção causal** | Não se atribui a Q o comando da navegação |
| R3.2 — perigo na rota | **Atendido quanto ao ensaio estático; parcial no transiente** | RHM/RHB e ablações preservados; DHa/DHb requerem correção |
| R3.3 — estabilidade/convergência | **Atendido conceitualmente** | Conclusão limita a estabilidade a simulações finitas |
| R4.1 — ablação η = 0 e reformulação | **Atendido no núcleo** | Título e contribuição refletem arquitetura reativa, com Q secundário |
| R4.2 — baseline reativo simples | **Parcial, com limitação assumida** | APF qualificado; heurística equivalente deixada para futuro limita a originalidade demonstrada |
| R4.3 — segurança e conflito | **Parcial, avançado** | Prioridade lógica qualificada; nova ativação e recuperação operacional ainda não estão corretas |
| R4 menor — fronteira e oscilação | **Parcial** | Refratário e KOb documentam limites; não prometer ausência geral de chattering |
| R4 menor — estatística degenerada | **Atendido no problema central** | TOST artificial foi removido; permanecem ajustes de método e rótulos |
| R4 menor — ordem das figuras | **Atendido** | Agradecimento mantém a sequência correta |

## 14. Correções necessárias antes de nova submissão

| Prioridade | Ação | Critério concreto de encerramento |
|---|---|---|
| **P0 — bloqueia a interpretação do novo ensaio** | Unificar ativação ambiental, sinal reativo e keepout | Antes de ativar: nenhuma informação do perigo nos canais; depois: registro temporal de ambos; DHa/DHb reavaliados ou alegação explicitamente reformulada |
| **P0 — bloqueia recuperação confiável** | Reinicializar resultado de navegação por episódio | Meta nova não falha por resultado antigo; sequência falha → nova meta → sucesso verificada |
| **P0 — ligado ao mesmo defeito** | Classificar o término `failed` em todos os componentes | Alvo entra no estado adequado; timeout e aborto não são confundidos; contadores por causa consistentes |
| **P1** | Publicar os registros anunciados | Episódios N2, E5 e DHa auditáveis com identidade, confirmação e motivo de término |
| **P1** | Alinhar equações à memória do campo | Formalização reproduz os dois canais, decaimento e prioridade residual |
| **P1** | Corrigir estatística localizada | p TTC = valor reproduzido; limite de risco corretamente nomeado; método exato/assintótico documentado por caso |
| **P1** | Fechar proveniência dos resultados | Commit e parâmetros por lote, distinção entre 140 reutilizados e vinte novos, nova versão preservando histórico |
| **P1** | Completar a interpretação experimental | Custos e abortos DHa, causas de E5, janela após ativação e distinção entre adiamento e falha |
| **P2** | Limpar alegações residuais | Segurança como resultado observado; completude como proxy; retirar promessa de varredura de raio não realizada |
| **P2** | Corrigir apresentação | Eq. 5 sem sobreposição, n de Tabela 7, cenário dinâmico no apêndice e metadados limpos |

As prioridades P0 não exigem desenvolver uma teoria nova nem uma campanha irrestrita. Exigem que o experimento e o controlador façam o que a revisão passou a afirmar. Depois dessas correções, repetir apenas os cenários afetados, ou justificar tecnicamente a reutilização dos dados, é mais informativo que aumentar indiscriminadamente o número de execuções.

## 15. Julgamento final

| Critério | Avaliação da terceira versão |
|---|---|
| Relevância | **Boa.** O problema e a aplicação permanecem pertinentes |
| Contribuição científica | **Mais bem delimitada.** Integração e decomposição de mecanismos são promissoras; o novo argumento transiente precisa ser validado corretamente |
| Correção técnica | **Ainda insuficiente para aceitação.** Antecipação do keepout e resultado antigo entre episódios são defeitos concretos |
| Validação experimental | **Melhorou.** Dezesseis configurações e ensaio dirigido; a hipótese nova ainda não está fielmente implementada |
| Estatística | **Próxima de adequada para o escopo**, após correções específicas de método, rótulo e p |
| Reprodutibilidade | **Boa para os agregados; incompleta para os episódios e a proveniência** |
| Segurança | **Resultados simulados específicos**, com prioridade lógica melhor descrita; sem garantia física geral |
| Literatura e originalidade | **Base adequada, distinção ainda limitada** frente a supervisores equivalentes |
| Clareza | **Melhor que na segunda rodada**, com inconsistências residuais e um defeito visível na Eq. 5 |
| Recomendação | **Revisar antes de submeter.** Não considero o conjunto atual de pendências uma revisão meramente editorial |

A terceira versão está mais próxima de um artigo tecnicamente defensável. Minha recomendação permanece desfavorável à submissão imediata por razões mais específicas que nas rodadas anteriores: a validade do novo ensaio de perigo emergente e a continuidade correta dos episódios após falha. Resolver esses pontos, disponibilizar a auditoria anunciada e alinhar a formalização à implementação permitirá uma próxima avaliação centrada no mérito da contribuição, sem reabrir objeções que já foram atendidas.
