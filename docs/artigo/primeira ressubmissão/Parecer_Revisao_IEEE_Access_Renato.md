# Parecer técnico sobre a versão revisada

**Navegação deliberativa e reativa para inspeção de subestações**  
Prof. Milton Miranda Neto | Avaliação independente | 8 de setembro de 2026

**Conclusão: revisão substancial necessária; não recomendo submeter esta versão ainda.**

A reformulação responde à objeção conceitual mais importante dos quatro revisores: a navegação efetivamente executada é controlada por um supervisor reativo e pelo Nav2, enquanto a tabela Q não comanda o robô. O novo título, a ablação E0 e a derivação da equivalência com aumento de recompensa são avanços reais. A inclusão de APF, perigo na rota, conflito e ruído também melhora o desenho de avaliação proposto.

Entretanto, o atendimento não está completo. Há divergências entre o PDF e o código da própria tag citada, uma falha que permite reconhecer uma ação abortada como chegada, um ensaio de conflito que filtra a anomalia antes da arbitragem, uma zona proibida construída com informação antecipada e métricas estatísticas que ainda não sustentam certas conclusões. Esses problemas atingem validade interna e reprodutibilidade, não apenas apresentação.

Este é um parecer simulado segundo critérios de revisão da **IEEE Access**, não uma manifestação oficial da revista. A recomendação científica equivale a uma revisão substancial. No sistema binário da revista, eu não recomendaria **Accept** para os materiais atuais. A possibilidade administrativa de nova submissão depende da carta editorial, que não foi fornecida; foram fornecidos os comentários dos revisores. A revista informa que admite somente uma ressubmissão quando autorizada. [Política editorial](https://ieeeaccess.ieee.org/authors/stages-of-peer-review/).

## 1. Materiais, método e alcance da avaliação

Foram lidos integralmente: **O**, artigo original, “Affective Attraction–Repulsion Value Modulation for Reactive Inspection Navigation in Electrical Substations”, 8 páginas; **N**, artigo revisado, “A Two-Layer Deliberative–Reactive Architecture with an Affective Attraction–Repulsion Layer for Autonomous Substation Inspection”, 12 páginas; **R**, arquivo “comentarios dos revisores.txt”, com os quatro pareceres. As páginas citadas neste relatório são as páginas impressas dos PDFs. Não foi recebida uma carta de resposta ponto a ponto.

Também foram inspecionadas visualmente as páginas de N, com ampliação de figuras e equações relevantes, e consultado o repositório público que o próprio artigo oferece como evidência. A tag **v1.0-resubmission existe** e resolve para o commit **32bbe7a729ca51f99711e759903505ab592c3da6**. A leitura do código neste relatório refere-se a esse commit fixo. A branch principal continuava em **8312da792e92279ecb4f2b6ecb42ef8faee16314** na consulta. A ausência de uma página GitHub Release separada não significa ausência da tag.

Foram auditadas as rotinas de supervisão, geração e contagem de eventos, campo afetivo, atualização de Q, APF, métricas e configurações relevantes. Não foram executadas as missões ROS 2/Gazebo. Duas verificações isoladas de funções confirmaram caminhos de falha; elas são identificadas expressamente, sem serem tratadas como experimentos de navegação. Os 120 registros novos não estavam disponíveis no pacote consultado, de modo que não foi possível recalcular as tabelas revisadas ou confirmar que as falhas de código ocorreram nas missões reportadas.

Distingo três níveis de evidência: **confirmado documentalmente**, para contradições no PDF ou no código; **confirmado por verificação isolada**, para comportamento reproduzido de funções; e **não verificável com os materiais disponíveis**, para resultados que exigem os novos logs. Código defeituoso demonstra possibilidade de erro; não demonstra, por si só, que todos os números publicados estejam errados.

## 2. O que mudou e o que já merece ser preservado

| Aspecto | Versão original | Versão revisada | Avaliação |
|---|---|---|---|
| Contribuição central | Modulação de valores no título e no resumo | Arquitetura de duas camadas no título | Mudança correta, mas há trechos e figura herdados |
| Papel de Q | Relação causal com movimento ambígua | Ações greedy apenas registradas; não atuadas | Esclarecimento decisivo, N pp. 2 e 5 |
| Ablação | Sem eta = 0 | E0 preserva a FSM e zera eta | Atende à ideia principal dos revisores |
| Recompensa | Progresso + atração, além do termo externo | Progresso apenas; derivação de aumento de recompensa | Correção matemática pertinente |
| Comparador reativo | Apenas patrulha fixa | APF adicional | Necessário e útil, mas comparabilidade incompleta |
| Segurança | Perigo lateral à rota | RHB/RHM, mais cenário CONF | Mais informativo, com problemas de atribuição e implementação |
| Estatística | Welch com contagens degeneradas | Mann–Whitney/permutação, Cliff, bootstrap e Holm | Melhora do plano, ainda incompleta e sem script correspondente |
| Estabilidade | Uma trajetória de erro TD parcial | Resíduo completo, agregado de E3 | Métrica melhor; interpretação e dados ainda exigem revisão |
| Literatura | 14 referências | 21 referências e tabela comparativa | Ampliação útil; síntese ainda precisa correção |

O trabalho não precisa demonstrar um novo teorema de RL para ter valor como contribuição aplicada. A IEEE Access admite contribuições de desenvolvimento e integração, desde que sejam distintas, tecnicamente sólidas e adequadamente validadas. A estratégia mais defensável é fortalecer a arquitetura e retirar da contribuição principal o módulo Q que não influencia a execução. [Critérios para revisores](https://ieeeaccess.ieee.org/reviewers/reviewer-guidelines/).

## 3. Auditoria dos comentários do Revisor 1

**Legenda:** atendido = solução adequada ao escopo atual; parcial = melhora relevante com pendência; não atendido = a correção necessária não foi demonstrada. Atendimento textual não equivale a validação dos dados.

| Item | Solicitação e evidência em N | Julgamento e ação necessária |
|---|---|---|
| R1.1 | Não herdar garantias de Q-learning; N p. 5 admite ausência de convergência formal e equivalência com recompensa | **Parcial.** Boa correção em III-B; remover a distinção incompatível na introdução, a causalidade da Fig. 1 e a frase sobre convergência empírica na p. 11 |
| R1.2 | Efeitos, ICs, testes adequados e multiplicidade; Tabelas 4 e 9 | **Parcial.** Cliff e Holm aparecem; faltam p numéricos, n por braço, método de bootstrap, tratamento de empates e script atualizado; IC degenerado não exprime generalização |
| R1.3 | Robustez mais ampla, especialmente percepção incerta; N1/N2, RHM e CONF | **Parcial.** Há dois níveis combinados de ruído e novos cenários; sem varredura de geometria, persistência ou localização; o raio prometido não é variado na matriz |
| R1.4 | Erro TD em múltiplas execuções e comparação com Q convencional; Fig. 7 e E0 | **Parcial.** Resíduo completo é adequado como diagnóstico; falta curva E0 sob condições iguais, dados da agregação e consistência entre gráfico e interpretação |
| R1.5 | Literatura recente e tabela de posicionamento; II e Tabela 1 | **Parcial.** Tabela existe e a bibliografia cresceu; definição de active sensing é inconsistente e faltam comparações explícitas com supervisores híbridos próximos |
| R1.6 | Troca entre inspeção, distância, tempo e segurança; V-D | **Parcial, com avanço claro.** Reporta cerca de 2 m e 15 s adicionais por anomalia; recuperar tempo de investigação, comparar custo por sucesso e não chamar custo observado de limite garantido |
| R1.7 | Resumo alinhado à FSM e estabilidade empírica; p. 1 | **Parcial.** Distinção Q/FSM explícita; “todas as anomalias” ignora CONF, a segurança é superestimada e o custo bounded não foi provado |

## 4. Auditoria dos comentários do Revisor 2

| Item maior | Solicitação e evidência em N | Julgamento e ação necessária |
|---|---|---|
| R2.1 | Explicar política, exploração, atuação, frequência e ablação; III-B p. 5 e E0 | **Parcial forte.** Responde que Q não atua e atualiza por odometria; falta resolver o significado da ação associada à transição observada. A ablação tem sentido arquitetural, mas seus dados novos não estão no pacote |
| R2.2 | Relação com shaping e dupla contagem; Eq. 6 e r = rprog | **Atendido na derivação; parcial no artigo.** O aumento de recompensa é reconhecido e a dupla contagem removida; a introdução ainda diz o contrário |
| R2.3 | Eta sem efeito comportamental; análise apenas numérica ou política aprendida | **Parcial forte.** O novo escopo é correto. Retirar “equivalência estatística” não testada e não atribuir pequenas diferenças exclusivamente ao acaso sem análise |
| R2.4 | Resíduo completo, múltiplas execuções e cautela sobre convergência | **Parcial.** Melhor métrica e redação na p. 10; falta validar agregação, curva comparativa e significado do resíduo final; não há política aprendida sendo avaliada |
| R2.5 | FSM sem Q, APF, Q com recompensa aumentada e método recente | **Parcial.** E0 e APF incluídos. Não há resultados de Q atuante nem DRL recente. Com escopo de supervisor, justificar formalmente esses itens como fora de escopo e priorizar heurística equivalente + keepout |
| R2.6 | Perigo na rota, métricas de segurança e recuperação | **Parcial crítico.** Cenário existe; ambos têm zero colisões; RHM ainda fica 8,7 s abaixo de 2 m. Código revela keepout antecipado, preempção incompleta e TTC aproximado |
| R2.7 | Comparações, p exatos, IC, multiplicidade, contagens e timeouts | **Parcial crítico.** Pares e efeitos explicitados; persistem p < 0,001, ausência de n por grupo e ICs degenerados. Os dois timeouts antigos não são reapresentados em análise com/sem exclusão |
| R2.8 | Distinguir detectar, iniciar, concluir e timeout; seleção e retenção de evento | **Não resolvido operacionalmente.** Texto melhora, mas conclusão depende de callback que não verifica sucesso; identidade é inferida pela anomalia mais próxima; resultados separados prometidos não aparecem nas tabelas |
| R2.9 | Corrigir “todas”, não significância e generalização | **Parcial.** Custo de tempo agora é admitido; CONF contém quatro anomalias e só três são inspecionadas; equivalência retorna na p. 10; generalização de ruído ainda é estreita |
| R2.10 | Síntese bibliográfica mais ampla | **Parcial.** 21 referências; integrar arbitragem, supervisão híbrida e inspeção orientada por eventos à comparação central; verificar os atributos de cada estudo na Tabela 1 |

| Item menor | Julgamento e evidência |
|---|---|
| R2.m1 - Descontinuidade no raio | **Parcial.** N p. 4 discute histerese e compromisso, mas não apresenta varredura de perfil/R; não elimina por si só reentrada de perigos persistentes |
| R2.m2 - argmax formal | **Não atendido.** Eq. 4 continua usando argmax como se retornasse valor; faltam conjunto vazio, empates e identidade por evento |
| R2.m3 - Dependência da ação | **Parcial.** Phi(s) substitui Phi(s,a); o estado (célula, bucket de módulo) não identifica univocamente sinal, alvo e memória do campo |
| R2.m4 - TD zero no baseline | **Atendido conceitualmente.** Legenda da Tabela 5 explica atualização inativa. Preferível “não aplicável” a zero, para evitar aparência de estabilidade perfeita |
| R2.m5 - Sementes, hardware, RTF e versão | **Parcial.** Hardware/RTF/tag informados; tag confirmada. Faltam sementes por execução, n válidos por grupo e dados/scripts da nova análise; conferir núcleos versus threads do hardware |
| R2.m6 - Metadados de produção | **Não atendido.** DOI de exemplo, datas 00 e VOLUME 11, 2023 permanecem; utilizar o template vigente sem simular metadados editoriais |

Não considero obrigatório acrescentar PPO ou DDQN apenas para aumentar o número de baselines. A exigência era coerente com a contribuição originalmente anunciada em RL. Ao mudar o escopo, a carta deve explicar essa mudança e demonstrar vantagem sobre supervisores comparáveis, com mesmas informações e mesmos controladores. Manter RL como contribuição principal restabelece a necessidade desses testes.

## 5. Auditoria dos Revisores 3 e 4

| Item | Julgamento e evidência |
|---|---|
| R3.1 - Benefício adicional de Bellman | **Parcial forte.** N admite que não há efeito sobre ações; E0 responde à pergunta. Restam Fig. 1, introdução e contribuição secundária excessiva |
| R3.2 - Perigo diretamente na rota | **Parcial.** Ensaio novo responde à geometria; não separa recuo de keepout e não demonstra inviolabilidade da zona de segurança |
| R3.3 - Estabilidade, não convergência | **Parcial.** Redação e resíduo melhores; Fig. 7 não representa simplesmente queda contínua e a p. 11 preserva formulação inadequada |
| R4.1 - Eta = 0; reformular título/resumo/contribuição | **Parcial forte.** Mudanças principais feitas; o módulo Q deve ser claramente diagnóstico/prospectivo em todo o texto e figuras |
| R4.2 - Baseline reativo de simplicidade semelhante | **Parcial.** APF existe, mas troca também o controlador local; falta documentar parâmetros e comparar com heurística de desvio via mesmo Nav2/MPPI |
| R4.3 - Segurança, perigo na rota e conflito real | **Parcial crítico.** RHM e CONF incluídos; CONF suprime atração no simulador, não exercitando a arbitragem alegada; keepout usa raio e verdade de terreno privilegiados |
| R4 menor - Salto em R / chattering | **Parcial.** Explicação adicionada, mas recorrência de recuos em N2/CONF e período refratário do código precisam ser descritos e medidos |
| R4 menor - Welch degenerado | **Parcial.** Métodos planejados mudaram; faltam script, testes identificados por linha, p numéricos e IC adequado para frequência de sucesso |
| R4 menor - Ordem das figuras no agradecimento | **Atendido.** N p. 11 traz Figs. 4, 5, 6 e 7 em ordem |

## 6. Falha crítica: conclusão da navegação não significa sucesso

**Evidência:** N p. 5 define inspeção como chegada + permanência; Algoritmo 1, p. 6, repete o critério. Na tag revisada, `StayAlertNode._on_goal_done` recebe o future mas não lê seu resultado, não verifica o status e não associa o callback à identidade da meta vigente. Se o modo for Investigate ou Avoid, simplesmente preenche `_reached_at`.

Uma ação ROS 2 pode terminar em SUCCEEDED, ABORTED ou CANCELED. O retorno de resultado não implica chegada bem-sucedida. [Estados terminais de ações ROS 2](https://design.ros2.org/articles/actions.html).

**Verificação isolada realizada:** executei o corpo do callback sobre objetos simulados com status 4, 5 e 6, correspondentes a sucesso, cancelamento e aborto. Nos três casos, `_reached_at` foi preenchido. Não foi preciso simular o Nav2 para confirmar que o status é ignorado.

Como consequência possível, após três segundos o supervisor pode emitir `investigate_end reason=inspected` mesmo depois de uma navegação abortada. `AnomalySimulator._on_event` aceita essa mensagem para creditar a anomalia, sem conferir independentemente a pose real e a permanência. Assim, a correção conceitual pedida em R2.8 ainda não está garantida pelo código. Isso também afeta `retreated` e a métrica de sucesso do recuo.

**Correção exigida:** validar `future.result().status == STATUS_SUCCEEDED`; conferir o identificador da meta/episódio; tratar aborto, cancelamento e rejeição como desfechos próprios; iniciar dwell somente após sucesso verificado; confirmar posição/orientação/tempo por um avaliador independente. Callbacks de metas canceladas de episódios anteriores não podem concluir o episódio atual. Testar especificamente rejeição, aborto, cancelamento tardio e meta inalcançável.

Esta é a prioridade mais alta: antes de interpretar 3/3 ou 5/5 como sucesso real, é preciso demonstrar que o instrumento de medição distingue sucesso de término. Não afirmo que todas as inspeções reportadas foram falsas; afirmo que a implementação publicada permite falsos positivos e os logs novos não possibilitaram excluir essa hipótese.

Fonte do código: [stay_alert_node.py no commit auditado](https://github.com/voidmmn/tese_react_nav/blob/32bbe7a729ca51f99711e759903505ab592c3da6/src/tese_nav/tese_nav/stay_alert_node.py) e [anomaly_simulator.py](https://github.com/voidmmn/tese_react_nav/blob/32bbe7a729ca51f99711e759903505ab592c3da6/src/tese_nav/tese_nav/anomaly_simulator.py).

## 7. Falha crítica: prioridade de perigo e ensaio de conflito

Há três problemas distintos.

**7.1. Preempção incompleta na máquina de estados.** No Algoritmo 1, o perigo só é consultado dentro de `mode = Patrol`. Em Investigate, as únicas saídas são chegada + dwell ou timeout. A rotina publicada reproduz essa lógica: não há transição Investigate → Avoid provocada por perigo. Logo, um perigo que apareça durante aproximação ou inspeção não está coberto pela alegação de prioridade categórica. O período refratário pós-recuo do código acrescenta outra exceção ausente no pseudocódigo.

**7.2. A Eq. 4 não foi implementada no campo publicado.** A equação escolhe perigo antes de atração. Entretanto, `AttractionField.observe` continua conservando a contribuição de maior módulo entre o novo estímulo e o campo anterior, independentemente da modalidade. Verificação isolada: uma observação acústica de intensidade 0,95 produz Phi = +1,14; a observação seguinte de perigo com intensidade 0,70 produz contribuição -1,05, mas Phi permanece +1,14. É um contraexemplo à prioridade imediata no módulo do campo. A persistência de um estímulo positivo anterior pode atrasar ou impedir a troca de sinal até ocorrer decaimento suficiente.

**7.3. CONF filtra o conflito antes de chegar ao campo.** Em `AnomalySimulator._check_proximity`, ao encontrar perigo dentro do raio, o simulador publica o perigo e executa `return`, deixando de publicar as anomalias daquele tick. No cenário co-localizado e inicialmente neutro, o campo não recebe simultaneamente as duas contribuições concorrentes. Portanto, 10/10 recuos em CONF não valida a arbitragem da Eq. 4; pode apenas validar a supressão prévia da atração. Essa filtragem independe ainda do teste de intensidade exigido na equação: basta encontrar o perigo no raio para omitir a atração.

**Correção exigida:** percepção deve disponibilizar todos os eventos detectados, com IDs e timestamps; a decisão deve priorizar perigos em um único ponto explícito, com preempção de todos os estados em que a locomoção/inspeção possa prosseguir. Testar tanto atração e perigo simultâneos quanto perigo novo após atração forte. Registrar os dois estímulos de entrada, o evento escolhido e a transição realizada. Tratar a permanência em segurança como uma propriedade diferente da prioridade de seleção.

Fonte: [AttractionField](https://github.com/voidmmn/tese_react_nav/blob/32bbe7a729ca51f99711e759903505ab592c3da6/src/tese_nav/tese_nav/utils/attraction_field.py), além das duas rotinas citadas na seção anterior. Os contraexemplos identificam falhas das funções publicadas; não quantificam sua incidência em missões completas.

## 8. Falha crítica: atribuição do ganho de segurança e keepout

N pp. 2, 7–9 descreve um recuo rápido seguido de keepout temporário, interpretado como expressão deliberativa da repulsão. No código, porém, `_emit_keepout` usa as coordenadas verdadeiras do perigo, dispara ao atingir **8 m**, usa um disco de **1,2 m** e mantém a marca latched até o fim da missão. O raio sensorial anunciado é **5 m**. A projeção não exige que Phi ultrapasse um limiar nem que o recuo tenha terminado ou sequer começado. É ativada especificamente quando o nome do cenário pertence a `KEEPOUT_SCENARIOS = {'route_hazard'}`.

Assim, o planejador pode receber o perigo três metros antes da detecção que aciona o mecanismo reativo. Isso não é necessariamente uma arquitetura inválida: pode ser um canal antecipado de mapa ou percepção. Mas precisa ser explicitado e disponibilizado igualmente aos comparadores pertinentes. Não sustenta a narrativa de que o recuo primeiro detectou o perigo e depois produziu a zona proibida. O fato de a configuração depender do nome do cenário também deve ser substituído por uma regra operacional aplicável a perigos detectados em geral, ou descrito como variante específica da arquitetura.

Além disso, `avoid_start` já delega o perigo ao keepout e futuras publicações daquele perigo podem ser suprimidas. Portanto, cessação do campo repulsivo não significa, nesse cenário, que o robô saiu fisicamente de perigo; pode indicar apenas transferência de responsabilidade. O campo, a FSM e o mapa de risco precisam ter estados distintos e auditáveis.

**Experimento mínimo para atribuição causal:** comparar no mesmo cenário e com a mesma informação (a) Nav2 + keepout sem recuo, (b) Nav2 + recuo sem keepout e (c) Nav2 + recuo + keepout. A patrulha fixa continua útil como referência operacional, mas não isola os mecanismos. Medir distância mínima, tempo dentro da zona, recuperação, conclusão e custo. Se o recuo isolado falhar ou oscilar, esse também é um resultado válido e deve ser apresentado.

Fonte: [projeção e delegação no simulador](https://github.com/voidmmn/tese_react_nav/blob/32bbe7a729ca51f99711e759903505ab592c3da6/src/tese_nav/tese_nav/anomaly_simulator.py) e [ativação no launch](https://github.com/voidmmn/tese_react_nav/blob/32bbe7a729ca51f99711e759903505ab592c3da6/src/tese_nav/launch/stay_alert.launch.py).

## 9. O que as métricas de segurança realmente mostram

| Métrica, Tabela 6 de N | RHB | RHM | Interpretação permitida |
|---|---|---|---|
| Distância mínima ao perigo | 0,71 m | 1,73 m | +1,02 m; cerca de 2,44 vezes, no cenário específico |
| TTC reportado | 2,8 s | 6,0 s | Cerca de 2,14 vezes; depende de definição correta do indicador |
| Tempo abaixo da folga | 14,4 s | 8,7 s | Redução de cerca de 39,6%; exposição não foi eliminada |
| Colisões | 0 | 0 | Não demonstra redução observada de colisões |
| Inspeções | 0 | 3 | Deve ser revalidado após corrigir reconhecimento de sucesso |

Os cálculos acima usam médias arredondadas do PDF; não são uma reanálise dos dados brutos. O código define `clearance_threshold = 2.0 m`. Portanto, os 8,7 s de RHM significam tempo dentro da zona de folga usada pelo próprio avaliador. **A redação defensável é redução de exposição e aumento de distância no cenário testado, não garantia categórica de segurança.**

`collisions` é contado quando a distância ao ponto do perigo cai abaixo de 0,5 m. Não é leitura de um sensor de contato nem contador geral de colisões com equipamentos. Nomear como entrada na região de contato simulada, ou acrescentar avaliação física de contato. Distinguir distância centro a centro, distância à fronteira de uma região perigosa e distância entre o footprint do robô e essa fronteira. Sem essa geometria, clearance pode ser interpretado incorretamente.

O TTC implementado é `d / closing`, com closing obtido pela diferença finita da distância ao perigo mais próximo. Ele é um indicador de aproximação radial ao centro, não necessariamente tempo até colisão com uma região finita. Em passagem tangencial, a distância radial pode diminuir sem ocorrer colisão futura. Para TTC geométrico, explicitar a região e procurar o primeiro instante de interseção da trajetória prevista com sua fronteira; sem interseção, TTC é infinito. Se mantiver d/closing, renomear como proxy e informar limiar, amostragem, filtragem e tratamento de mudança do perigo mais próximo.

Zero ocorrências em dez ensaios não prova risco nulo. Sob um modelo de dez missões independentes e idênticas, 0/10 falhas admite limite superior unilateral exato de 95% de aproximadamente **25,9%** para a probabilidade de falha. É uma ilustração da limitação amostral, não uma estimativa do risco real de operação elétrica. A segurança elétrica também não foi modelada por tensão, zona de arco ou distâncias normativas; o artigo deve permanecer no domínio da navegação simulada.

Fonte operacional: [metrics_node.py](https://github.com/voidmmn/tese_react_nav/blob/32bbe7a729ca51f99711e759903505ab592c3da6/src/tese_nav/tese_nav/metrics_node.py).

## 10. Identidade de eventos, inspeção e estado interno

O PDF promete seleção da anomalia mais saliente e retenção do alvo. No código, as intensidades das anomalias no raio são publicadas, mas a pose de inspeção é a da **anomalia mais próxima**. Ao receber `investigate_start`, o crédito é associado novamente à anomalia não concluída mais próxima, agora em um raio de até **2R** e usando posições verdadeiras. Esses procedimentos podem escolher eventos distintos. Uma anomalia intensa e distante pode elevar Phi, enquanto a pose e o crédito pertencem a uma anomalia próxima e fraca.

Essa divergência é especialmente relevante para E5, que é apresentado como teste de arbitragem entre eventos agrupados, e N1/N2, nos quais posições percebidas são perturbadas enquanto a atribuição de crédito usa a geometria verdadeira. Sem IDs nas mensagens de início/fim, não se demonstra correspondência entre evento detectado, selecionado, alvo navegado e alvo contabilizado.

Recomendo um registro por evento com `event_id`, modalidade, posição percebida, posição de referência apenas no avaliador, intensidade, instante de detecção, início, chegada confirmada, fim de dwell, timeout/aborto e justificativa de supressão. Cada meta e cada callback deve carregar `episode_id` e `goal_id`.

O estado `visited` no começo da investigação deve ser renomeado para `committed` ou `in_progress`. Separar `completed`, `failed`, `deferred_by_hazard` e eventual política de retentativa. Não tornar uma inspeção abortada permanentemente indistinguível de uma inspeção concluída. O algoritmo deve expressar o que o texto promete.

A Eq. 4 deve indexar **eventos e**, não somente modalidades m, pois vários eventos térmicos ou acústicos podem coexistir. Definir conjuntos elegíveis de perigos e anomalias por tick; escolher explicitamente o evento e*, com regra determinística de desempate; depois definir Phi = w[m(e*)] i[e*]. Na ausência de eventos elegíveis, definir decaimento ou neutralidade. O `argmax` retorna argumento/índice; não deve ser atribuído diretamente a um escalar sem essa definição.

O campo depende de memória e tempo, enquanto s guarda apenas célula e bucket de |Phi|. Estados com o mesmo bucket podem ter sinais e eventos diferentes. Escrever Phi_t, ou incluir no estado as variáveis necessárias, é mais rigoroso do que afirmar simplesmente Phi(s). O mesmo problema compromete a interpretação Markoviana da tabela Q. Essa correção não exige construir uma política aprendida; exige apenas não atribuir à representação propriedades que ela não possui.

## 11. Bellman, recompensa e estabilidade numérica

A fatoração da Eq. 6 está correta para alpha não nulo: adicionar eta Phi fora do erro TD equivale, com alpha fixo, a usar recompensa aumentada `r' = r + (eta/alpha) Phi`. Isso resolve o principal equívoco de originalidade. A retirada de max(Phi,0) da recompensa também resolve a dupla contagem, inclusive no `bellman_node.py` revisado.

Ainda assim, na p. 2 de N permanece a afirmação de que o método difere de reward shaping por modificar a função de valor em vez da recompensa. Ela conflita com III-B e deve ser removida. A Fig. 1 e sua legenda ainda atribuem aproximação/recuo ao termo de Bellman. O componente Q deve aparecer como diagnóstico fora do caminho de controle, ou ir para material suplementar.

Há um problema adicional: `bellman_node.py` escolhe uma ação greedy para registro, guarda-a como `prev_action` e usa a transição realmente produzida por Nav2 para atualizar esse par. A ação registrada não foi a ação responsável por produzir a transição. Q-learning ser off-policy não dispensa registrar a ação **efetivamente executada pela política de comportamento**. Sem uma correspondência definida entre comandos/decisões reais e a ação discreta, a tabela não pode ser interpretada como aprendizagem validada do valor de forward/left/right/stop.

Também convém esclarecer `rprog = 1.0`: o código adiciona essa constante por atualização de odometria, não uma diferença explícita de progresso até meta. Não basta denominá-la progresso. Definir o evento que gera recompensa, terminalidade, inicialização, frequência de odometria e reinicialização por missão. Alterações de frequência mudam a acumulação de um bônus por amostra.

**Sobre a Fig. 7:** o uso de |alpha delta + eta Phi| é um avanço, pois inclui todo o incremento aplicado. Mas a figura mostra picos ao longo da missão, inclusive na região intermediária, e uma queda perto do fim; não uma diminuição monotônica nem, visualmente, “starts higher” no primeiro instante. Picos podem ser perfeitamente compatíveis com eventos; a narrativa deve explicá-los. A Tabela 5 parece usar residual final próximo de 0,019, enquanto o gráfico permanece bem acima desse nível durante grande parte da missão. Explicitar se a tabela contém última janela, média temporal ou média de finais por execução.

O código agrega resíduos em janela e publica periodicamente. A figura precisa especificar a janela, interpolação do tempo normalizado e se a banda de 95% é IC da média ou faixa entre execuções. Normalização pode esconder diferenças em duração e alinhamento dos eventos. Mostrar E0 e E3 sob entradas equivalentes ajudaria a separar o termo afetivo da dinâmica da atualização comum. Acrescentar máximo de |Q| e de incremento seria mais informativo que apenas residual de encerramento.

Um incremento pequeno por amostra não prova convergência nem, isoladamente, limitação da tabela em horizonte indefinido. Como o módulo não atua, seu diagnóstico numérico não sustenta segurança ou eficiência de navegação. Retirar de N p. 11 a frase de que a convergência foi avaliada empiricamente e dizer somente que foram observados incrementos de valor durante missões finitas.

Fonte: [bellman_node.py](https://github.com/voidmmn/tese_react_nav/blob/32bbe7a729ca51f99711e759903505ab592c3da6/src/tese_nav/tese_nav/bellman_node.py) e [q_table.py](https://github.com/voidmmn/tese_react_nav/blob/32bbe7a729ca51f99711e759903505ab592c3da6/src/tese_nav/tese_nav/utils/q_table.py).

## 12. Estatística: avanços e pendências específicas

**12.1. Métodos prometidos e métodos disponíveis.** A proposta de Cliff, bootstrap, testes por postos/permutação e Holm é melhor que Welch aplicado a duas contagens constantes. Entretanto, as Tabelas 4 e 9 continuam usando p < 0,001, apesar da frase “exact p-values are given”. Teste exato e apresentação do valor numérico de p são coisas diferentes. Publicar os valores calculados, inclusive em notação científica, e identificar método, alternativa, n e ajuste em cada comparação.

O método exato padrão de Mann–Whitney na SciPy não corrige empates. Em amostras pequenas com empates, a implementação recomenda considerar permutação; não basta configurar `method='exact'`. Informar qual estatística foi permutada, esquema de independência/pareamento, enumeração ou número de permutações, semente e tratamento de dados ausentes. [Documentação de Mann–Whitney](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.mannwhitneyu.html).

**12.2. Ausência de diferença não é equivalência.** N p. 10 afirma que a equivalência é estatística e usa p = 0,32 e IC [-1,2; 2,7] s. Mann–Whitney não é um teste de equivalência. O IC sugere diferenças pequenas no tempo, mas a margem aceitável precisa ser definida antes da interpretação. Usar TOST ou outro procedimento apropriado com limites justificados, ou simplesmente afirmar que o desenho não conecta eta aos comandos e as observações são compatíveis com essa ausência de efeito. [TOST para amostras independentes](https://www.statsmodels.org/stable/generated/statsmodels.stats.weightstats.ttost_ind.html).

Delta de Cliff = -0,27 e diferença média +0,34 s não são necessariamente contraditórios: postos e média descrevem aspectos diferentes da distribuição. Não “corrigir” sinais sem os dados. Por outro lado, não descrever -0,40 como inequivocamente “próximo de zero”. E IC em segundos é IC da diferença média, não IC de Cliff; explicitar isso no texto.

**12.3. Contagens degeneradas e incerteza.** O bootstrap de amostras em que toda execução vale 3 pode retornar [3;3]. Isso caracteriza a distribuição empírica observada, mas não implica que o sucesso populacional seja conhecido sem incerteza. Para desfecho binário por missão, 10/10 sucessos têm IC exato bilateral de 95% aproximadamente [69,2%;100%], sob independência e mesma probabilidade de sucesso. Não tratar as três anomalias de uma missão como três repetições independentes. Apresentar sucesso por missão e completude por evento com a estrutura de agrupamento.

**12.4. Multiplicidade.** Separar Tabela 4 confirmatória e Tabela 9 exploratória pode ser defensável, mas é necessário declarar como a família foi escolhida e quantas hipóteses contém. Os sete testes da Tabela 4 devem exibir p bruto e p ajustado. A Tabela 9 não deve sustentar afirmações confirmatórias de robustez sem discussão de multiplicidade. Hedges g é anunciado, mas não consta nas tabelas; removê-lo da promessa ou fornecê-lo quando definido e pertinente. Duas variâncias nulas tornam o efeito padronizado por desvio inadequado.

**12.5. Comparar 3 com 5 não prova robustez.** O contraste E3/E5 no número de anomalias muda também o denominador disponível. A diferença +2 é em boa parte estrutural. Comparar 3/3 com 5/5, tempo/custo por evento, falhas e recuperação. Um p pequeno para o número absoluto não mostra que a solução escala para geometrias ou densidades novas.

**12.6. Tamanho amostral e dependência.** Dez execuções quase determinísticas no mesmo mapa não equivalem a dez cenários independentes. Justificar a amostra por precisão das métricas relevantes e distribuir replicações em layouts/posições/sementes quando houver afirmação de generalização. Não existe necessidade automática de “30 runs”; mais repetições do mesmo caso podem agregar pouca informação. Evitar pseudorreplicação dos ticks e fornecer n efetivo por grupo.

## 13. Exclusões e reprodutibilidade

N declara 120 tentativas, 113 válidas e sete falhas de inicialização, com n entre 7 e 10. É razoável separar falha de infraestrutura da análise condicional de navegação, se o critério for pré-definido e documentado. Mas a frase de que incluir ou excluir robôs imóveis deixa todas as estatísticas comportamentais inalteradas é incorreta: zeros de distância/inspeção alteram médias e taxas se incluídos; se resultados são indefinidos, precisam ser tratados como ausentes, não como equivalentes aos sucessos.

Relatar duas perspectivas: desempenho **condicional à inicialização bem-sucedida** e confiabilidade **por tentativa**. A taxa global de inicialização é 113/120 = 94,2%, mas faltam distribuições por configuração e motivo. Não inferir taxa de missão concluída apenas dessa taxa. Mostrar início, movimento, término, timeout e falha por execução.

O original retinha dois timeouts, um E1 e um E2. A revisão afirma que as sete exclusões novas são falhas diferentes. Isso pode ser verdadeiro, mas não fornece a análise com/sem os dois timeouts solicitada por R2.7. Se os experimentos foram refeitos, explicar claramente qual conjunto foi substituído, quais mudanças de código/ambiente ocorreram e por que. A redução da distância adicional de aproximadamente 14 m para 6,1 m também requer essa rastreabilidade.

**Conferência do pacote público:** a árvore completa da tag revisada contém 50 arquivos `results/metrics_*.csv`, apenas E1–E5. Os hashes desses 50 arquivos coincidem com os do conjunto antigo presente na branch principal. O script `src/tese_nav/scripts/analise_resultados.py` também permanece idêntico: usa `ttest_ind(..., equal_var=False)` e lista E1–E5. Assim, o pacote consultado não contém os 120 CSVs e o script que reproduzem a estatística revisada, embora contenha mudanças no controlador e novos componentes.

Isso é uma lacuna verificável de disponibilização; não é prova de que os novos experimentos não tenham sido feitos. O pacote pode estar desatualizado ou os arquivos podem existir localmente. Contudo, a frase de que código, dados e scripts da avaliação revisada estão liberados não é sustentada pelo conteúdo da tag indicada.

**Correção exigida:** publicar conjunto de dados correspondente à revisão, tabela final por run, motivos de exclusão, sementes e versões; atualizar o script para gerar as Tabelas 4–9 e as figuras; arquivar um novo commit/tag identificável, preservando o histórico; apontar o artigo diretamente para essa versão. O README principal deve orientar o leitor para a revisão correta e não manter apenas a alegação antiga de Bellman como causa do movimento.

Fontes: [árvore da versão auditada](https://github.com/voidmmn/tese_react_nav/tree/32bbe7a729ca51f99711e759903505ab592c3da6), [dados disponíveis](https://github.com/voidmmn/tese_react_nav/tree/32bbe7a729ca51f99711e759903505ab592c3da6/results) e [script estatístico](https://github.com/voidmmn/tese_react_nav/blob/32bbe7a729ca51f99711e759903505ab592c3da6/src/tese_nav/scripts/analise_resultados.py).

## 14. Baselines, custo operacional e robustez

**APF é uma adição importante, mas não isola a contribuição.** Stay Alert envia metas ao Nav2/MPPI; APF passa a controlar velocidades diretamente. O experimento modifica tanto a supervisão quanto o controlador de movimento. Diferença de tempo pode decorrer de ganhos, limites de velocidade, condição de aproximação, planejamento e obstáculos, não necessariamente do campo afetivo.

No código da tag, APF usa standoff 1,8 m e orçamento de investigação 30 s, enquanto o artigo descreve 2 m e 40 s para o método. Há ganhos, limites e período refratário próprios não apresentados no PDF. APF usa diretamente as posições do cenário; uma comparação sob ruído precisaria padronizar a interface de percepção. Estas diferenças não tornam o baseline inútil; tornam necessária sua documentação e restringem a conclusão a duas implementações específicas. [Implementação APF](https://github.com/voidmmn/tese_react_nav/blob/32bbe7a729ca51f99711e759903505ab592c3da6/src/tese_nav/tese_nav/apf_node.py).

O comparador mais informativo é uma heurística “detectar → selecionar alvo → desviar → retornar”, com a mesma FSM, Nav2/MPPI, metas, informação, standoff, dwell e segurança, mas sem ponderação/decadência afetiva. O objetivo é medir o que essas decisões acrescentam à supervisão comum. E0 só mostra que Q é dispensável; não mostra vantagem da parametrização afetiva sobre uma heurística equivalente.

**Custos calculados a partir da Tabela 5:** E3 acrescenta 44 s sobre 320 s, ou 13,75%; acrescenta aproximadamente 6,1 m sobre 80,4 m, ou 7,6%. Isso corresponde a cerca de 14,7 s e 2,0 m adicionais por uma das três inspeções. Frente a APF, 364 s versus 407 s representa redução de aproximadamente 10,6% do tempo, com distâncias praticamente iguais, 86,5 e 86,4 m. A vantagem apresentada é temporal, não de comprimento de trajetória.

Esses números são promissores para uma análise de custo-benefício, mas “modesto” depende dos requisitos da missão e “bounded” não decorre de uma média finita ou de um timeout global. Reportar custo observado e respectivos ICs; definir utilidade somente se pesos de inspeção, risco e tempo forem justificáveis. Não criar uma função de utilidade escolhida a posteriori para favorecer o método.

**Ruído:** N1/N2 perturbam posição e intensidade conjuntamente, em dois níveis; não permitem isolar qual variável explica a diferença. O código usa semente padrão 0 e o PDF informa semente fixa, sem listar sementes por execução. Se a mesma sequência é reiniciada em todas as missões, a variabilidade reportada não representa dez realizações independentes de ruído. Registrar o protocolo real e empregar múltiplas sementes, eventualmente pareadas entre métodos.

As verificações restantes prioritárias são perigo durante Investigate, falso negativo/intermitência, atraso sensorial, erro sistemático de posição, perfis de detecção contínuos versus truncados e mais de uma geometria. N p. 4 promete sensibilidade ao raio, e V-E promete varreduras de densidade/geometria na análise “abaixo”; V-G apresenta apenas os dois níveis de ruído. Executar as varreduras prometidas ou remover as remissões.

AMCL é descrito como localização ativa na p. 6, enquanto p. 7 diz odometria exata e map→odom fixo. Explicitar qual nó fornece a transformação efetiva em cada experimento e não descrever a variabilidade como proveniente de localização se esta foi desabilitada/fixada. Não é necessário resolver sim-to-real para publicar um estudo de simulação; é necessário delimitar seu alcance.

## 15. Literatura, novidade e coerência editorial

O novo título corresponde melhor ao mecanismo demonstrado, embora seja longo e repita “layer”. Uma opção mais objetiva é **“Event-Driven Deliberative–Reactive Navigation for Simulated Substation Inspection”**. Manter “affective” é possível se o artigo operacionalizar o conceito e mostrar o benefício de seus componentes; não basta renomear limiares de prioridade como emoção.

A Tabela 1 define active sensing como movimentação para obter observações além de uma rota fixa, mas marca o próprio trabalho como “Yes (patrol)”, apesar de a patrulha ser fixa. A inspeção reativa adiciona reposicionamento, porém não há objetivo explícito de ganho de informação, incerteza ou seleção informativa de vistas. Uma denominação mais precisa é patrulha para exposição sensorial + reposicionamento acionado por eventos. Aplicar a mesma definição a todos os trabalhos e separar inspeção focada de informative path planning.

Falta demonstrar o que distingue esta arquitetura de supervisores híbridos, arbitragem por prioridade e replanejamento com mapa de risco. A bibliografia tem trabalhos pertinentes, mas a tabela compara classes muito amplas e agrupa APF/DWA em uma linha. Incluir métodos híbridos próximos e atributos operacionais verificáveis. A frase de novidade baseada na combinação com Bellman é frágil porque Bellman não atua no método avaliado.

**Verificação bibliográfica pontual:** a referência [2] existe e seus autores/título correspondem ao registro da Frontiers. A página oficial registra publicação em **4 de fevereiro de 2026** e recomenda citação com ano **2026**, embora o volume seja **12 - 2025** e o DOI contenha 2025. Ajustar o ano conforme os metadados de citação do editor; não deduzir ano pelo DOI. [Registro oficial de Zhang et al.](https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2025.1759501/full).

Não concluí uma auditoria bibliográfica integral das 21 referências. Alguns registros MDPI não puderam ser consultados integralmente; sua falta de acesso não é evidência de inexistência. Conferir autores, ano, volume, DOI, situação editorial e, principalmente, se o conteúdo sustenta cada atributo da Tabela 1. Não exigir aumento arbitrário para 30 ou 40 citações: relevância e síntese são mais importantes que contagem.

**Resumo e conclusão:** a expressão “inspects all” precisa limitar-se às anomalias elegíveis nos cenários em que isso ocorreu. CONF possui quatro anomalias e três concluídas por projeto; relatar a quarta como suprimida por perigo. Informar n válido e escopo simulado. Prioridade lógica, aumento de folga, ausência observada de contato e segurança operacional são quatro afirmações diferentes. Não combiná-las numa garantia única.

**Figura 1:** reformular o fluxo causal: eventos → supervisor → metas Nav2; Q como diagnóstico paralelo. Sua legenda atual, p. 2, ainda afirma comportamento “through an affective term in the Bellman update”. **Figura 2:** representar keepout e sua fonte de informação se ele integra o método avaliado. **Figura 3/Algoritmo 1:** inserir interrupção por perigo, estados de falha, identidade do alvo e período refratário. **Figura 7:** revisar legenda/interpretação e mostrar a agregação real.

**Apresentação:** a composição geral em duas colunas é legível, mas as figuras conceituais têm textos pequenos e as Tabelas 1/5 concentram informação. Preservar diagramas técnicos verificáveis e melhorar tamanho de rótulos. O resumo tem aproximadamente 270 palavras por extração; enxugá-lo pela quantidade de alegações, sem tratar essa contagem como violação de regra não confirmada. Permanecem DOI de exemplo, datas “00 Month, 0000” e rodapé de 2023. O agradecimento corrigiu a ordem das figuras; a descrição do uso de IA deve identificar adequadamente o conteúdo assistido, conforme a política aplicável. [Preparação do artigo](https://ieeeaccess.ieee.org/authors/preparing-your-article/).

## 16. Plano de correções com critério de encerramento

| Prioridade | Ação | Evidência necessária para considerar resolvido |
|---|---|---|
| P0 | Corrigir callback de navegação e contagem independente | Falhas/cancelamentos não contam como chegada; pose, orientação, dwell e IDs confirmados |
| P0 | Unificar prioridade de segurança e preempção | Perigo interrompe investigação; atração e perigo chegam juntos ao decisor; contraexemplos cobertos |
| P0 | Alinhar keepout ao modelo de informação | Raio, fonte, duração e ativação documentados; sem vantagem informacional não declarada |
| P0 | Publicar dados e análise exatos da revisão | Novo pacote reproduz todas as tabelas/figuras e identifica as 120 tentativas, exclusões e versões |
| P1 | Reexecutar resultados afetados pelas correções | Logs independentes de sucesso e segurança; novos números sem reutilizar tabelas invalidadas |
| P1 | Comparar keepout/recuo e heurística equivalente | Benefício de cada componente separável, com mesma percepção e mesmo controlador |
| P1 | Concluir análise estatística | n por grupo, p numéricos, ICs apropriados, multiplicidade e análise de falhas |
| P1 | Delimitar generalização | Cenários adicionais focados nas falhas concretas; afirmações compatíveis com os testes |
| P2 | Limpar escopo, equações e figuras | Nenhuma causalidade atribuída a Q não atuante; Phi/eventos/estados coerentes |
| P2 | Revisar bibliografia e pacote editorial | Referências verificadas, metadados limpos, resposta ponto a ponto com localizações |

O conjunto mínimo de testes de regressão deve cobrir: sucesso versus aborto/cancelamento; meta antiga concluindo após troca de episódio; alvo mais próximo diferente do mais saliente; perigo surgindo durante dwell; perigo fraco após atração forte; ausência de estímulos; conflito com ambas as mensagens efetivamente entregues; e retomada segura após delegação ao planejador. Estes testes são propostos por riscos observados no código, não como exigência genérica de ampliar testes indefinidamente.

Depois de estabilizar o método, congelar o protocolo e executar a matriz relevante. Corrigir o software pode alterar a contagem de inspeções, os tempos e o recuo; portanto, ajustes apenas no PDF não bastam. Se os logs existentes permitirem reavaliar geometricamente cada evento, parte da reanálise pode ser feita sem repetir todas as missões; caso não permitam, repetir os ensaios afetados.

## 17. Como preparar a resposta aos revisores

A carta deve reconhecer explicitamente a mudança de escopo: os resultados sustentam supervisão reativa, não uma política de navegação aprendida por Q. Para cada item R1–R4, apresentar preocupação, modificação efetivamente implementada, seção/página/figura, experimento ou evidência e limitação remanescente. Não afirmar “fully addressed” apenas porque uma frase foi adicionada.

R2.1 e R4.1 devem apontar E0 e a retirada do caminho Q → ação. R2.2 deve apontar a fatoração e a recompensa sem dupla contagem. R2.6/R4.3 devem apontar a nova especificação de segurança, a correção de prioridade e as ablações do keepout. R2.8 deve demonstrar verificação de status e conclusão física. R2.7 deve apontar o pacote de dados e tabelas auditáveis, incluindo falhas. Para baselines de RL dispensados por escopo, explicar a justificativa e oferecer os comparadores de supervisão que respondem à pergunta científica atual.

Este parecer não substitui a carta: ainda faltam correções e validações para que uma resposta afirmativa seja verdadeira. A IEEE Access solicita uma lista de atualizações com a preocupação, resposta dos autores e mudanças realizadas. [Orientação de submissão](https://ieeeaccess.ieee.org/authors/submission-guidelines/).

## 18. Julgamento final nos critérios da revista

| Critério | Resposta simulada |
|---|---|
| Contribui ao conhecimento? | **Potencialmente sim.** Integração aplicada e supervisão interpretável têm valor; o diferencial precisa ser isolado de heurísticas e keepout |
| É tecnicamente sólido? | **Ainda não.** Reconhecimento de sucesso, prioridade, informação do keepout e correspondência método/código exigem correção |
| Apresentação é abrangente? | **Melhorou, mas permanece incompleta.** Faltam definições, dados novos, análise de falhas e comparadores equivalentes |
| Referências são aplicáveis e suficientes? | **Aplicáveis em geral; suficiência parcial.** A síntese de trabalhos híbridos próximos e a exatidão dos atributos da tabela precisam melhorar |
| Há referências a remover? | **Não identifico remoção obrigatória com a evidência disponível.** Corrigir metadados e verificar pertinência antes de ampliar a lista |
| Recomendação científica | **Não aceitar na forma atual; realizar revisão substancial antes da nova submissão** |

A mudança de título e escopo foi a decisão correta. O ponto que agora mais ameaça o artigo é a discrepância entre o mecanismo descrito, o código arquivado e a evidência experimental acessível. Ao corrigir essa cadeia e demonstrar os resultados com métricas independentes, a arquitetura pode ser defendida com muito mais segurança científica, mesmo sem apresentar uma nova contribuição em aprendizagem por reforço.
