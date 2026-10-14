# Parecer técnico — quarta rodada de avaliação

**Artigo:** *A Two-Layer Deliberative–Reactive Architecture with an Affective Attraction–Repulsion Layer for Autonomous Substation Inspection*  
**Autores:** Milton Miranda Neto e Alexandre Cardoso  
**Versão avaliada:** PDF com sufixo `(3)`, 15 páginas  
**Data:** 11 de setembro de 2026  
**Comparação:** versão `(2)`, parecer da terceira rodada e comentários originais dos quatro revisores  
**Natureza:** parecer independente segundo critérios de avaliação científica pertinentes à IEEE Access; não representa decisão editorial da revista.

**Recomendação: concluir uma revisão direcionada antes de submeter. Os dois bloqueios operacionais da terceira rodada foram corrigidos e os ensaios afetados foram repetidos. O artigo avançou substancialmente, mas o PDF ainda mistura resultados antigos e novos, e algumas afirmações sobre auditoria e segurança excedem o que os registros publicados demonstram.**

Minha avaliação é mais favorável que na terceira rodada. Não encontrei, nas verificações realizadas, uma nova falha de controle equivalente à ativação antecipada do perigo ou à contaminação entre episódios por um aborto anterior. As pendências atuais são delimitadas: atualizar a Figura 5 e os totais da bateria; esclarecer a janela das métricas do perigo dinâmico; corrigir e completar a auditoria; e ajustar a explicação da única execução incompleta de E5. Não recomendo repetir indiscriminadamente as 160 tentativas nem transformar o trabalho em um novo projeto de aprendizado por reforço.

## 1. Escopo e evidências desta avaliação

Mantive os critérios das rodadas anteriores: contribuição e originalidade, correspondência entre matemática e implementação, validade das métricas de inspeção e segurança, comparadores e ablações, estatística, robustez, reprodutibilidade, literatura, apresentação e atendimento aos revisores originais.

Examinei o novo PDF, as alterações em relação à terceira versão, o código publicado e os dados associados. A referência `v1.0-resubmission` resolve nesta consulta para o commit **`12081a70ed645a78a348440e8d1623ac6678e781`**. Todas as referências ao código neste parecer fixam esse commit. [Versão examinada][repo].

O pacote atual contém **160 CSVs de métricas**. Em relação à terceira rodada, **130 arquivos conservam os mesmos hashes e 30 foram substituídos**, correspondentes às novas execuções de E5, DHa e DHb. Li os 30 novos CSVs, reaproveitei os valores extraídos dos 130 arquivos cuja identidade foi confirmada e executei o script estatístico atual sobre os valores finais das 160 tentativas. Para esse recálculo, reconstruí arquivos intermediários contendo os valores finais por métrica; não os confundo com séries temporais completas.

Também examinei os **793 eventos** de `audit_trail.csv` e seu gerador. Cruzei configuração e repetição com `run_seed`, conferindo os totais de investigações iniciadas, inspeções creditadas e investigações adiadas. **Não houve divergências nesses três cruzamentos.**

Executei verificações isoladas das funções que apresentavam os dois defeitos críticos e da classificação de falha de investigação. Regenerei a Figura 5 com o script publicado, adaptando apenas o diretório de entrada para os dados locais, e a comparei visualmente com o painel inserido no PDF. Não executei novas missões no Gazebo, nem verifiquei um robô físico. Os testes isolados confirmam os casos examinados, não a ausência de qualquer defeito possível na pilha ROS/Nav2.

As páginas indicadas abaixo são as do novo PDF de 15 páginas.

## 2. O que foi efetivamente resolvido

| Pendência da terceira rodada | Evidência nesta versão | Situação |
|---|---|---|
| Keepout podia conhecer o perigo dinâmico antes de sua ativação | Ativação ambiental ocorre antes dos dois canais; ambos consultam `_hazard_live` | **Corrigida no código e confirmada no caso isolado** |
| Aborto do episódio anterior podia encerrar a investigação seguinte | `_enter` reinicializa `_nav_outcome`; a proteção por época permanece | **Corrigida e confirmada no caso isolado** |
| `reason=failed` não entrava no conjunto de falhas do avaliador | Novo ramo registra o alvo em `failed` | **Corrigida para a classificação solicitada** |
| Falha de navegação era agregada como timeout de investigação | Nova métrica `investigation_failed`; separação no coletor e no analisador | **Corrigida nos novos registros** |
| Ensaios afetados precisavam ser repetidos | Novos dez E5, dez DHa e dez DHb; reaproveitamento dos outros treze grupos declarado | **Atendido quanto à coleta necessária** |
| Campo formal não representava memória independente de perigo e atração | Eqs. 4–7 passam a usar dois acumuladores com retenção e decaimento | **Divergência principal corrigida**; restam detalhes formais menores |
| Disparo de Avoid era descrito sem todas as condições | P. 5 inclui limiar, pose, refratário e habilitação do recuo | **Atendido** |
| Rejeições N2 eram atribuídas ao ruído sem evidência por episódio | Auditoria lista as seis rejeições e respectivas distâncias | **Atendido para a causa operacional registrada** |
| Geradores das Figs. 5 e 7 não estavam publicados | `gerar_boxplots.py` e `gerar_qconv.py` estão disponíveis | **Disponibilização atendida**; a Fig. 5 no PDF continua antiga |
| Descrição de Mann–Whitney não contemplava todos os ramos do script | P. 9 e Apêndice B distinguem cálculo exato, permutação de braços constantes e aproximação com empates | **Atendido no ponto solicitado** |
| Limite binomial exato era chamado de Wilson | P. 13 corrige a denominação e distingue os dois intervalos | **Atendido** |
| p de TTC dinâmico era incompatível com o resultado | P. 11 e Tabela 10 refletem o novo p, aproximadamente 0,001 | **Atendido** |
| Faltavam custos e discussão dos abortos em DHa | P. 11 informa tempo, distância, adiamento e três abortos entre oito válidas | **Avanço substancial**; falta rastrear o término de cada episódio |
| Tabela 7 omitia os tamanhos válidos dos braços | Legenda informa RHM 9, KOa 10 e KOb 9 | **Atendido** |
| Equação invadia a outra coluna | Composição da p. 5 foi reorganizada | **Corrigido visualmente na página examinada** |

Continuam encerradas as correções já aceitas anteriormente: distinção entre supervisor e tabela Q, ablação η = 0, reconhecimento da equivalência com aumento de recompensa, abandono de alegação de convergência, retirada do TOST indevido para braços constantes, delimitação da inspeção como proxy e cancelamento de meta antiga aceita tardiamente.

## 3. Confirmação dos dois reparos operacionais

### 3.1. Ativação do perigo e distribuição da informação

O ciclo `_check_proximity` agora chama `_update_hazard_activation` antes de `_emit_keepout`. O ramo reativo e a projeção no costmap verificam a mesma condição de elegibilidade `_hazard_live`.

Repeti o contraexemplo da terceira rodada: perigo com raio de ativação de 3 m, robô a 4 m e conjunto de perigos ativos vazio. Agora não há retenção no keepout nem publicação. Ao aproximar o robô para 2,9 m e executar a ativação antes da projeção, o perigo passa a ativo e a publicação ocorre.

| Verificação isolada | Resultado atual |
|---|---|
| Perigo inativo, robô a 4 m | Nenhuma marca e nenhuma publicação de keepout |
| Robô a 2,9 m, após ativação ambiental | Perigo ativo e keepout publicado |
| Ordem dos eventos nas 18 execuções dinâmicas válidas | Ativação → primeira projeção no keepout → primeira publicação reativa |

A sequência registrada é consistente com a correção. Ela não demonstra entrega simultânea aos consumidores ROS, mas elimina a antecipação específica que motivou a objeção anterior. **Não mantenho essa falha como bloqueio atual.** [Ativação e canais][simulator].

### 3.2. Resultado de navegação restrito ao episódio atual

No segundo teste, entrei em uma investigação nova após um estado anterior `aborted`, sem fornecer ainda um resultado para a nova meta. `_nav_outcome` passou a `None`, e o ciclo seguinte não encerrou a investigação por causa da falha antiga.

O tratamento de aceitação tardia continuou cancelando a meta obsoleta no caso verificado. A classificação isolada de `investigate_end reason=failed` também passou a incluir o alvo no conjunto `failed`.

Isso encerra o defeito demonstrado na terceira rodada. Permanecer no conjunto `committed` após uma falha é uma questão distinta, relacionada à política de novas tentativas; o reparo da classificação não demonstra, por si, uma política geral de recuperação. [Supervisor][supervisor] e [avaliador de eventos][simulator].

## 4. Resultados atualizados: o que os dados sustentam

### 4.1. E5 melhorou na nova coleta

| Métrica | Resultado recalculado de E5, n = 10 |
|---|---:|
| Inspeções creditadas | **4,90 ± 0,32** de cinco |
| Inspeção completa | **9/10**; IC Wilson de 95% aproximadamente **[0,60; 0,98]** |
| Investigações iniciadas | 5,20 ± 0,42 |
| Duração da missão | **397,03 ± 4,18 s** |
| Intervalo observado de duração | **385,82 a 401,94 s** |
| Distância percorrida | 92,24 ± 0,44 m |
| Distância mínima ao perigo | 4,854 ± 0,032 m |
| Execuções com aborto reativo | 3/10 |
| Falhas de investigação por navegação | Três eventos |
| Entradas na região de contato | Zero |

A Tabela 5, a discussão de V-F e os contrastes atualizados da Tabela 10 refletem os agregados principais. O contraste E5 − E3 produz **+1,90 inspeções** e **+32,59 s**, com os intervalos publicados reproduzidos. O aumento absoluto de inspeções compara cenários com totais de alvos diferentes; a taxa de completude por missão continua sendo a medida adequada para discutir a dificuldade de E5.

O resultado atual é melhor que o da coleta anterior, mas não atribuo toda a diferença causalmente a um reparo específico: as missões foram repetidas e também estão sujeitas à variabilidade da simulação e da navegação.

### 4.2. DHa/DHb preservam a evidência de uma margem transiente maior

| Métrica | DHa: recuo + keepout, n = 8 | DHb: keepout, n = 10 |
|---|---:|---:|
| Inspeções creditadas | 0,00 ± 0,00 | 1,00 ± 0,00 |
| Investigações adiadas por perigo | 1,00 ± 0,00 | 0,00 ± 0,00 |
| Distância mínima ao perigo | **2,551 ± 0,146 m** | **2,224 ± 0,005 m** |
| Proxy radial mínimo de TTC | **5,232 ± 0,448 s** | **4,721 ± 0,207 s** |
| Tempo abaixo de 2 m | 0,00 s | 0,00 s |
| Entradas na região de contato | Zero | Zero |
| Duração registrada | **347,57 ± 1,70 s** | **338,15 ± 0,48 s** |
| Distância percorrida | **84,92 ± 1,73 m** | **83,27 ± 0,08 m** |
| Execuções com aborto reativo | **3/8** | **1/10** |

O contraste DHa − DHb reproduz **+0,327 m** de distância mínima, IC de aproximadamente **[0,23; 0,42]**, Cliff’s δ = 1 e **p = 4,57 × 10⁻⁵**. Para TTC, a diferença é **+0,511 s**, IC **[0,20; 0,84]**, δ = 0,85 e p aproximadamente **1,0 × 10⁻³**.

O custo é de **9,42 s** e **1,65 m** adicionais, além do adiamento da inspeção. Esses custos agora aparecem na p. 11, com arredondamento compatível. É uma melhora importante na interpretação: a vantagem não é uma redução demonstrada de colisões, pois ambos os braços tiveram zero contatos observados e zero tempo abaixo de 2 m; é maior afastamento no encontro estudado, com custo operacional e perda deliberada daquela inspeção.

As três execuções DHa com aborto e o `avoid_success` registrado em todas as oito não são, isoladamente, uma contradição: esse contador pode resultar de saída por decaimento de Φ, sem chegada à meta de recuo. A p. 11 já reconhece essa distinção. O que ainda falta é demonstrar a sequência por episódio e evitar usar o nome `safe` como validação física independente.

O ensaio é corretamente identificado na Tabela 10 como **dirigido e exploratório**, com p sem correção de Holm. Não trato esses p como pertencentes à família confirmatória da Tabela 4. [Análise estatística publicada][statistics].

## 5. Pendência principal: o PDF ainda contém resultados da coleta antiga

### 5.1. Figura 5 não corresponde aos novos CSVs

**Localização:** p. 9, Figura 5.  
**Origem:** problema novo de sincronização do manuscrito após a nova coleta; não é um novo defeito do controlador.

O painel inserido no PDF conserva, para E5, um ponto com **três inspeções**, outro com quatro e uma duração próxima de **440 s**. Na coleta atual, há nove execuções com cinco inspeções, uma com quatro e nenhuma com três; a duração máxima é **401,94 s**.

| Elemento de E5 | Figura 5 no PDF | Dados atuais |
|---|---|---|
| Mínimo de inspeções | 3 | **4** |
| Média visual de inspeções | Aproximadamente 4,7 | **4,9** |
| Maior duração | Aproximadamente 440 s | **401,94 s** |
| Distribuição de distância mínima | Painel antigo | Distribuição da nova coleta é diferente |

Regenerei o painel com `gerar_boxplots.py` sobre os valores finais atuais. O resultado corresponde aos novos números, não à figura embutida no PDF. Portanto, a disponibilização do script foi atendida, mas falta inserir sua saída atual no manuscrito. [Gerador da Figura 5][boxplots].

**Correção suficiente:** substituir o arquivo da figura pela geração da coleta atual e recompilar o PDF, conferindo seus pontos extremos contra a Tabela 5. Isso não requer novos experimentos.

### 5.2. O total correto é 154 válidas e seis imóveis

**Localização:** p. 9, início de resultados, e p. 13, ameaças à validade.  
**Origem:** os totais antigos eram corretos na terceira rodada e ficaram desatualizados após as novas execuções DHa.

| Quantidade | Texto atual | Pacote atual |
|---|---:|---:|
| Tentativas totais | 160 | **160** |
| Execuções válidas para a análise comportamental | 156 | **154** |
| Execuções imóveis excluídas | 4 | **6** |
| Fração classificada como válida | 97,5% | **96,25%**, ou **96,3%** |
| Faixa de n válido por configuração | 9–10 | **8–10** |

As seis exclusões são APF repetição 10, RHM repetição 5, N2 repetição 10, KOb repetição 5 e **DHa repetições 1 e 8**. A Tabela 10 e V-C já reconhecem DHa com n = 8, tornando a contradição interna especialmente fácil de detectar.

Não basta substituir os números: a expressão “mission never started” continua imprecisa. Cinco dessas seis execuções registram duração de missão acumulada, embora não apresentem deslocamento relevante. O dado diretamente observável é que **o robô permaneceu imóvel**, segundo o critério usado pelo analisador; atribuir todas as ocorrências à mesma falha de inicialização do contêiner exige o registro correspondente.

**Redação sugerida:** “Of 160 attempted runs, 154 met the movement criterion for behavioral analysis and six remained immobile. Behavioral results use n = 8–10 valid runs per configuration; the fraction meeting this criterion was 154/160 (96.25%).” A causa de infraestrutura pode ser acrescentada quando documentada.

Para DHa, informar separadamente **8/8 preempções entre as válidas** e **8/10 tentativas com execução válida e preempção**. Não chamar nenhuma dessas razões de inspeção completa ou sucesso integral de missão.

## 6. Pendência anterior: janela temporal das métricas do perigo dinâmico

**Localização:** p. 11, afirmação de que o mínimo da missão inteira é, “by construction”, o mínimo após a ativação.  
**Origem:** problema de definição da métrica já identificado na terceira rodada; o novo texto procura resolvê-lo, mas o coletor permaneceu sem o filtro necessário.

No `metrics_node`, a lista `_hazards` vem diretamente do cenário. A distância mínima, o tempo abaixo de folga e o TTC são calculados sobre essa lista, sem consulta ao estado de ativação do perigo. A correção em `anomaly_simulator` controla o que os canais de navegação percebem; ela não foi propagada para a elegibilidade dos perigos no coletor. [Coletor de métricas][metrics].

Há uma demonstração simples nos arquivos: as duas tentativas DHa imóveis, sem evento de ativação na auditoria, registram distância mínima ao perigo de aproximadamente **12,369 m**. Portanto, o coletor mede a distância à posição do perigo mesmo quando ele não foi ativado.

Isso **não demonstra que os mínimos numéricos publicados para as execuções válidas estejam errados**. É plausível que os mínimos de distância tenham ocorrido depois da ativação, mas essa igualdade deve ser verificada, não deduzida da existência ambiental do perigo. Para TTC, a ressalva é ainda mais relevante: o mínimo depende também da velocidade radial, podendo pertencer a outra fase da aproximação.

**Correção necessária:** distinguir explicitamente a métrica de missão inteira da métrica após ativação. Se os registros originais permitirem alinhar tempo ROS, posição e velocidade, calcular a janela `t ≥ t_ativação`, comparar os resultados e informar se coincidem. Se só houver mínimos acumulados, filtrar linhas posteriores à ativação pode continuar carregando um mínimo anterior; isso não equivale a recomputar a janela.

Se não houver registro suficiente para essa recuperação, há duas alternativas honestas: manter os números como métricas de missão inteira, retirar a equivalência “por construção” e limitar a interpretação temporal; ou instrumentar e repetir apenas DHa/DHb para sustentar especificamente a afirmação pós-ativação. A escolha depende da força da alegação que os autores desejam manter. Não é necessário repetir os outros quatorze grupos por essa razão.

## 7. Auditoria: avanço confirmado e ajustes ainda necessários

### 7.1. As seis rejeições de N2 agora são verificáveis

| Repetição N2 | ID do alvo | Distância registrada | Limite de confirmação |
|---:|---:|---:|---:|
| 2 | 0 | 3,33 m | 3,30 m |
| 5 | 2 | 3,36 m | 3,30 m |
| 7 | 0 | 3,56 m | 3,30 m |
| 7 | 1 | 3,47 m | 3,30 m |
| 8 | 0 | 3,34 m | 3,30 m |
| 9 | 2 | 3,53 m | 3,30 m |

Os 27 inícios, 21 créditos e seis rejeições correspondem aos nove CSVs válidos. A atribuição dessas perdas à etapa de confirmação tem agora suporte direto nos registros. **Não seria correto repetir a objeção genérica de que não há auditoria publicada.**

A interpretação continua circunscrita ao proxy: demonstra rejeição por distância ao alvo verdadeiro, não falha de um sensor físico nem comprovação de orientação ou qualidade de imagem. Esse escopo já foi aceito e não exige reabrir a definição inteira de inspeção. [Trilha publicada][audit].

### 7.2. A auditoria não contém todos os desfechos que o texto anuncia

Na p. 9, o texto atribui à trilha desfechos de navegação como succeeded, aborted e cancelled, além de timeout e deferred. Entretanto, o gerador extrai eventos do avaliador de anomalias: `start`, `inspected`, `rejected`, `failed`, `deferred` e os três eventos relativos à ativação/publicação do perigo.

`failed` traz uma classificação agregada como `navegação`, sem distinguir aborto, cancelamento e rejeição da meta. A trilha também não inclui os eventos de fim de Avoid que permitem distinguir `safe`, `retreated` e `timeout`. Os contadores de navegação dos CSVs não substituem a associação entre meta, episódio e resultado.

Por isso, a p. 11 avançou ao reconhecer os três abortos DHa, mas a sequência “aborto da meta → saída por decaimento → recuperação da patrulha” ainda não pode ser reconstituída integralmente a partir do CSV de auditoria publicado.

**Correção suficiente:** ampliar a extração para incluir início e fim de Avoid, desfecho da meta reativa e identificador de episódio/meta, ou disponibilizar os trechos de log necessários. Se a trilha permanecer como está, reduzir a lista de informações prometidas na p. 9 e não atribuir a ela uma demonstração causal que não contém.

O rótulo `safe` é uma condição do supervisor baseada em Φ. A supressão da republicação reativa após delegação ao keepout pode fazer o campo decair. Isso explica por que um episódio pode terminar sem a meta de recuo ter sido alcançada, mas não constitui uma nova medição de segurança física; clearance e TTC continuam tendo papel próprio.

### 7.3. O novo esquema mistura coordenadas e descarta o tempo ROS explícito

**Origem:** problema novo no artefato de auditoria acrescentado nesta revisão, sem evidência de que tenha alterado a navegação.

Em `gerar_auditoria.py`, os eventos `start` gravam a posição verdadeira do alvo em `true_x` e `true_y`. Nos eventos de ativação e primeira publicação, esses mesmos campos recebem a **posição do robô**, capturada de `robot=(x,y)`. O nome das colunas passa a ter significados diferentes conforme o evento.

O parser também extrai o tempo `t=...` explícito nas mensagens de ativação/publicação, mas o descarta. A coluna `t` recebe o timestamp do cabeçalho da linha de log, em escala de época, enquanto os CSVs de métricas usam valores de tempo ROS da simulação. Assim, a trilha preserva a ordem dos registros, mas não oferece diretamente a base comum de tempo necessária para cruzar a ativação com as métricas.

**Correção:** usar colunas distintas, por exemplo `target_true_x`, `target_true_y`, `robot_x`, `robot_y`, `time_ros_s` e `time_log_s`, documentando campos ausentes. Preservar o tempo ROS já presente nas mensagens e registrar um identificador de execução consistente com o CSV de métricas. Essa mudança é pequena e melhora diretamente a possibilidade de encerrar a pendência da seção 6. [Gerador da auditoria][auditgen].

Não interpreto esses problemas de esquema como evidência de fabricação dos dados. Os agregados conferem; o problema é a semântica e a suficiência das informações publicadas.

## 8. E5: a causa melhorou, mas a frase sobre a última tentativa permanece incorreta

**Localização:** p. 12, V-F.  
**Origem:** pendência anterior de atribuição causal, parcialmente resolvida pela nova auditoria.

Os registros atuais sustentam que todos os cinco alvos tiveram investigação iniciada em cada execução de E5. Três execuções apresentam falha de navegação; em duas delas há início adicional de investigação e posterior completude. Isso é muito mais informativo que a explicação genérica anterior sobre incapacidade de revisitar os alvos.

Porém, a única execução incompleta, **E5 repetição 6**, tem exatamente cinco eventos `start`: alvos 0, 1, 2 e 3 recebem crédito, o alvo 4 é iniciado e termina como `failed`, e **não há novo `start` para o alvo 4**. O CSV registra cinco investigações iniciadas, quatro créditos e uma falha de investigação.

Logo, a frase de que nessa execução “the re-attempt does not finish within the mission” não corresponde ao registro disponível. Não há uma nova tentativa iniciada e deixada incompleta; há falha sem nova tentativa registrada.

**Redação sugerida:** “Three runs recorded a reactive navigation failure. Two subsequently initiated an additional investigation and completed all five targets; the remaining run ended with four credited inspections and no further recorded attempt on the failed target.”

Também convém evitar apresentar as duas reinvestigações observadas como demonstração de uma política geral de retry. O ramo `reason=failed` classifica o alvo como falho, mas não o remove de `committed`; a presença de um início adicional merece ser descrita como observação dos episódios, a menos que a regra de recuperação correspondente seja explicitada e demonstrada. Não é necessário inventar uma nova política para corrigir a redação atual.

## 9. Avaliação científica pelos mesmos critérios

### 9.1. Contribuição e comparadores

O reposicionamento permanece correto: a contribuição demonstrada é a arquitetura de supervisão deliberativa–reativa, seu campo de arbitragem e sua integração com Nav2/MPPI. A tabela Q é uma formulação auxiliar; a ablação confirma que η não governa as ações executadas. Não reabro a exigência de uma política aprendida atuante quando o artigo já declara esse escopo.

A comparação com APF e as ablações de keepout/recuo são úteis. O texto agora assume adequadamente que a diferença temporal frente a APF envolve controladores e parâmetros de aproximação diferentes. Ainda não há isolamento da vantagem específica do campo frente a um supervisor heurístico igualmente simples usando o mesmo controlador. Essa é uma **limitação anterior de originalidade demonstrada**, não um defeito novo desta versão.

Para sustentar o artigo atual, a contribuição deve continuar formulada como integração e análise de comportamento, sem proclamar superioridade geral sobre supervisores convencionais ou métodos de aprendizado. Um comparador heurístico com o mesmo controlador fortaleceria a contribuição, mas não o transformo agora em obrigação experimental nova para encerrar as inconsistências identificadas.

### 9.2. Formalização matemática

O avanço das Eqs. 4–7 é substancial: os dois acumuladores finalmente representam retenção de máximos e memória independente de perigo e atração. A equivalência da modulação com aumento de recompensa na Eq. 8 permanece correta para a taxa de aprendizado fixa declarada. A ausência de garantia de invariância e de convergência está explicitada.

Restam ajustes de precisão: definir o que ocorre com conjuntos elegíveis vazios; informar ε e o período de decaimento; e alinhar a saturação dos **acumuladores**, feita após observações no código, à descrição que apresenta saturação da saída. Saturar um acumulador antes do decaimento não é, em geral, igual a conservar um valor interno arbitrariamente grande e saturar apenas sua leitura. Não demonstrei impacto dessa diferença nas execuções publicadas; é uma correspondência formal a completar.

As ressalvas anteriores sobre usar Φ(s) para um campo com memória e sobre chamar de progresso uma recompensa constante por amostra continuam secundárias. Uma notação temporal e uma frase sobre a aproximação do estado resolvem melhor isso que uma alegação de representação Markoviana completa. [Campo implementado][field].

### 9.3. Estatística

A análise melhorou e os contrastes principais foram reproduzidos. Estão corretamente resolvidos o caso degenerado de TOST, a separação entre Wilson e limite binomial exato, a descrição dos ramos de Mann–Whitney e a identificação exploratória dos contrastes DHa/DHb. A correção de Holm da família confirmatória de sete comparações permanece reproduzível.

Os principais ajustes estatísticos atuais são de relato: totais válidos, gráfico antigo e interpretação da janela de segurança. Para DHa, o tamanho válido caiu para oito; os intervalos e a discussão devem usar esse denominador. Se o exemplo de risco da p. 13 for estendido a esse grupo, o limite binomial exato unilateral de 95% para zero falhas em oito execuções é aproximadamente **31,2%**. Isso não obriga a mudar o método de Wilson usado para as taxas descritivas.

O p = 0,75 no TOST E3/N2 continua sendo ausência de evidência de equivalência pelo procedimento adotado. Não deve ser tratado, isoladamente, como prova formal de não equivalência. E as durações de KOb até interrupção não representam tempos de conclusão bem-sucedida.

### 9.4. Inspeção, segurança e robustez

O proxy de inspeção está adequadamente delimitado como resposta de navegação e confirmação por distância. Os resultados não validam diagnóstico elétrico, orientação da câmera ou qualidade do sensoriamento físico. Essa limitação é aceitável no escopo assumido e já foi reconhecida.

A segurança dispõe agora de evidência muito melhor que no artigo original: perigo sobre a rota, ablações, conflito, ruído e perigo emergente com ativação corrigida. Entretanto, ausência de contato na amostra, preempção lógica e êxito da meta de recuo são desfechos distintos. O nome de uma transição não substitui a medição independente.

A robustez continua limitada a poucos níveis de ruído e a cenários escolhidos. A frase da p. 5 que promete resultados de sensibilidade ao **raio** de detecção ainda não encontra uma varredura correspondente nos resultados apresentados. A correção proporcional é retirar “radius” dessa promessa ou apontar o resultado já existente, se houver; não é necessário iniciar uma nova campanha somente para preservar essa frase.

No resumo e na conclusão, substituir “safety holds throughout” por descrição dos contatos observados e “bounded time increase” por aumento medido evita sugerir garantia universal. “Degrades gracefully” também merece linguagem quantitativa: sob N2, a completude é 4/9, um limite relevante que o próprio artigo já informa.

### 9.5. Reprodutibilidade, literatura e apresentação

A publicação dos geradores e da auditoria melhora sensivelmente o pacote. O reaproveitamento de treze configurações é agora declarado e a justificativa por ausência de abortos, cancelamentos e rejeições confere nos contadores. Isso sustenta a decisão de repetir seletivamente os grupos afetados; não equivale a provar que cada arquivo antigo foi gerado pelo código atual.

A mesma tag aponta agora para outro commit. Citar apenas `v1.0-resubmission` não fixa a proveniência. Recomendo registrar no PDF ou em um manifesto o commit de coleta por lote, parâmetros, seeds, arquivos e hashes, mantendo identificáveis os dados substituídos. O commit desta revisão difere do `c142b3fd5a3a8106d8a51fa9ccabbd08bb9948d8` examinado na terceira rodada.

A literatura e a tabela comparativa permanecem mais amplas e melhor alinhadas que no artigo original; a referência [2] passou a indicar 2026, conforme a correção solicitada anteriormente. O ponto científico remanescente é distinguir a contribuição de integração frente à arbitragem híbrida convencional, e não simplesmente aumentar a contagem de referências. Não fiz nesta rodada uma nova busca bibliográfica exaustiva nem uso a ausência de referências novas como bloqueio.

A composição das equações melhorou. Permanecem metadados de template na p. 1 e no rodapé, incluindo datas fictícias, DOI aparente de exemplo e “VOLUME 11, 2023”. Ajustar conforme a preparação do manuscrito, sem inventar datas ou DOI editorial. A Figura 5 desatualizada é uma inconsistência de conteúdo e tem prioridade maior que esses detalhes gráficos.

## 10. Atendimento aos revisores originais

“Atendido no escopo” significa que a objeção foi resolvida pela delimitação explícita da contribuição, sem alegar que uma funcionalidade ausente passou a existir. “Parcial” identifica a limitação remanescente; não implica automaticamente exigir novos experimentos.

### Revisor 1

| Item | Situação na quarta rodada | Avaliação |
|---|---|---|
| R1.1 — teoria e convergência | **Atendido no escopo** | Formulação auxiliar, equivalência com recompensa e limites teóricos explícitos |
| R1.2 — estatística e multiplicidade | **Atendido no método; relato a corrigir** | Procedimentos e contrastes conferem; corrigir n global e Figura 5 |
| R1.3 — robustez | **Parcial, com avanço** | Ruído e ativação dinâmica corrigida; generalização ampla não demonstrada |
| R1.4 — resíduo e múltiplas execuções | **Atendido para estabilidade empírica** | Resíduo completo agregado e gerador publicado; não sustenta convergência |
| R1.5 — literatura comparativa | **Parcial, avançado** | Tabela e referências adequadas ao reposicionamento; diferenciação frente a heurística equivalente permanece limitada |
| R1.6 — custo de inspeção | **Atendido no núcleo** | Tempo, deslocamento e custo do adiamento agora discutidos |
| R1.7 — resumo | **Parcial, próximo de encerrar** | Papel de Q claro; qualificar linguagem de segurança e de limite temporal |

### Revisor 2 — comentários maiores

| Item | Situação na quarta rodada | Avaliação |
|---|---|---|
| R2.1 — Q nas ações e ablação | **Atendido no reposicionamento** | Não atuação de Q explicitada; η = 0 reproduz comportamento |
| R2.2 — reward shaping e dupla contagem | **Atendido** | Derivação e restrição da novidade estão claras |
| R2.3 — efeito de η | **Atendido no escopo** | Varredura numérica, sem atribuição de robustez de política aprendida |
| R2.4 — estabilidade | **Atendido para a alegação limitada** | Resíduo completo, agregação e processamento disponíveis |
| R2.5 — comparadores | **Parcial, limitação assumida** | APF e ablações úteis; não isolam ganho frente a heurística com mesmo controlador |
| R2.6 — segurança e recuperação | **Parcial, muito mais forte** | Bloqueio de ativação corrigido; falta fechar janela temporal e desfechos de Avoid |
| R2.7 — estatística e dados | **Parcial, próximo de encerrar** | Recálculo possível; corrigir amostra global, figura e proveniência |
| R2.8 — inspeção, identidade e falhas | **Parcial, com bloqueio operacional resolvido** | Estado residual e classificação corrigidos; N2 auditável; completar desfechos/identidade de episódio |
| R2.9 — alegações | **Parcial** | Completude delimitada; corrigir causalidade de E5 e frases gerais de segurança |
| R2.10 — literatura | **Parcial, avançado** | Ampliação adequada; originalidade é de integração, não novo operador de aprendizagem |

### Revisor 2 — comentários menores

| Item | Situação | Avaliação |
|---|---|---|
| R2.m1 — fronteira do raio | **Parcial** | Histerese/compromisso descritos; promessa de varredura do raio não demonstrada |
| R2.m2 — argmax | **Quase atendido** | Dois acumuladores corrigem a divergência central; completar vazio e saturação |
| R2.m3 — dependência de Φ | **Atendido quanto à ação; ressalva de memória** | Não há dependência de a; notação temporal seria mais precisa |
| R2.m4 — zero no baseline | **Atendido** | Atualização inativa no baseline explicada |
| R2.m5 — reprodução | **Parcial, avançado** | Seeds, dados e geradores presentes; fixar commits por lote e bases de tempo |
| R2.m6 — metadados | **Pendente editorial** | Persistem informações de template |

### Revisores 3 e 4

| Item | Situação | Avaliação |
|---|---|---|
| R3.1 — benefício de Bellman | **Atendido quanto à distinção causal** | Comportamento atribuído ao supervisor |
| R3.2 — perigo na rota | **Atendido no ensaio solicitado** | RHM/RHB e ablações fornecem evidência; ressalva temporal pertence ao ensaio adicional |
| R3.3 — estabilidade/convergência | **Atendido no escopo** | Interpretação empírica e agregação disponíveis |
| R4.1 — η = 0 e reformulação | **Atendido no núcleo** | Título e contribuição reposicionados |
| R4.2 — baseline reativo | **Parcial, limitação assumida** | APF implementado; comparação com heurística de mesmo controlador segue ausente |
| R4.3 — segurança e conflito | **Parcial, avançado** | Conflito e prioridade exercitados; ativação corrigida; concluir auditoria temporal |
| R4 menor — fronteira/chattering | **Parcial** | Mecanismos e limites descritos; evitar garantia geral |
| R4 menor — estatística degenerada | **Atendido** | Procedimentos inadequados centrais corrigidos |
| R4 menor — ordem das figuras | **Atendido** | Agradecimento mantém sequência correta |

## 11. São problemas antigos ou novos?

| Problema | Origem | Interpretação |
|---|---|---|
| Keepout antes da ativação | Introduzido no ensaio anterior | **Resolvido nesta revisão** |
| Aborto anterior contaminando novo episódio | Introduzido no tratamento anterior de falhas | **Resolvido nesta revisão** |
| Ausência de classificação de `failed` | Pendência anterior | **Resolvida para os novos registros** |
| Figura 5 com dados antigos | **Novo após a repetição de E5** | Arquivo gráfico não atualizado; não é regressão de navegação |
| 156/160 e quatro exclusões | **Novo após a repetição de DHa** | Totais antigos ficaram no texto; os próprios quadros já usam n = 8 |
| Coordenadas e relógios da auditoria | **Novo no gerador acrescentado** | Problema de esquema/extração, sem evidência de impacto no controle |
| Métricas sem filtro de ativação | **Já existia** | A ativação dos canais foi corrigida, mas a definição no coletor não mudou |
| Falta de desfecho detalhado de Avoid | **Já existia, parcialmente resolvido** | Agora há auditoria, porém ela não inclui esses eventos |
| Causa da incompletude de E5 | **Já existia, muito reduzido** | Dados esclarecem as falhas; resta uma frase incompatível com a repetição 6 |
| Heurística com mesmo controlador, generalização e metadados | **Limitações anteriores** | Não foram causadas pelos reparos atuais |

**Você corrigiu os dois problemas operacionais que bloqueavam a terceira rodada. Os principais problemas novos desta rodada são de sincronização e documentação dos resultados corrigidos.** Não há base, nas verificações feitas, para concluir que o artigo ou o controlador tenham piorado globalmente.

## 12. Lista de fechamento antes da submissão

| Prioridade | Ação concreta | Critério de encerramento | Nova simulação? |
|---|---|---|---|
| Alta | Regenerar e inserir a Figura 5 atual | E5 com mínimo de quatro inspeções e máximo de 401,94 s, coerente com a tabela | **Não** |
| Alta | Atualizar totais em todo o PDF | 154 válidas, seis imóveis, 96,25%, n = 8–10; causas descritas conforme evidência | **Não** |
| Alta | Resolver a alegação de métricas pós-ativação | Janela calculada corretamente ou números identificados como missão inteira, sem equivalência não demonstrada | **Só se os registros forem insuficientes e a alegação específica for mantida; apenas DHa/DHb** |
| Alta | Corrigir o esquema e o alcance da auditoria | Tempos e posições inequívocos; incluir fins de Avoid/desfechos de metas ou restringir a promessa do texto | **Não, se os logs originais contiverem os eventos** |
| Média | Ajustar a explicação de E5 repetição 6 | Falha sem nova tentativa registrada, sem alegar retry inacabado | **Não** |
| Média | Fixar a proveniência da coleta | Manifesto com commits/lotes, parâmetros, seeds e hashes | **Não** |
| Baixa | Completar notação e limpar redação/template | Vazio, ε, decaimento e saturação; raio não testado; segurança observada; metadados | **Não** |

Os critérios de encerramento acima são os alvos desta revisão. Não acrescento como condição obrigatória uma nova família de baselines, prova de convergência, implantação física ou ampla varredura de mapas. Esses desenvolvimentos podem fortalecer trabalhos futuros, mas não são necessários para corrigir os problemas demonstrados neste parecer.

## 13. Julgamento final

| Critério | Julgamento |
|---|---|
| Relevância | **Boa** para inspeção autônoma e integração de navegação |
| Clareza da contribuição | **Boa**, desde que mantida como supervisão e integração |
| Originalidade demonstrada | **Moderada**, limitada pela ausência de isolamento frente a heurística equivalente |
| Correção operacional | **Melhorou substancialmente**; os dois contraexemplos anteriores foram resolvidos |
| Desenho experimental | **Adequado ao escopo delimitado**, com limitações explícitas de generalização |
| Estatística | **Majoritariamente consistente e reproduzível**; relato ainda precisa ser sincronizado |
| Segurança | **Evidência empírica útil**, condicionada aos proxies e à janela temporal efetivamente medida |
| Reprodutibilidade | **Boa para agregados; muito melhor para episódios**, ainda incompleta em relógios, desfechos e proveniência |
| Prontidão para envio | **Próxima, mas ainda não concluída** |

O trabalho não está no mesmo patamar de bloqueio da terceira rodada. A arquitetura corrigida e as novas execuções sustentam uma avaliação mais favorável. Ainda assim, um revisor atento encontrará imediatamente a Figura 5 incompatível com a tabela e a contagem global incompatível com DHa; as questões de janela temporal e desfecho de Avoid exigem um fechamento técnico além da revisão de linguagem.

Minha recomendação é concluir os ajustes delimitados acima e então consolidar o pacote de submissão. O passo seguinte é assegurar que **o PDF, os dados, a auditoria e a versão de código descrevam o mesmo experimento**, preservando os avanços já confirmados.

[repo]: https://github.com/voidmmn/tese_react_nav/tree/12081a70ed645a78a348440e8d1623ac6678e781
[simulator]: https://github.com/voidmmn/tese_react_nav/blob/12081a70ed645a78a348440e8d1623ac6678e781/src/tese_nav/tese_nav/anomaly_simulator.py
[supervisor]: https://github.com/voidmmn/tese_react_nav/blob/12081a70ed645a78a348440e8d1623ac6678e781/src/tese_nav/tese_nav/stay_alert_node.py
[metrics]: https://github.com/voidmmn/tese_react_nav/blob/12081a70ed645a78a348440e8d1623ac6678e781/src/tese_nav/tese_nav/metrics_node.py
[field]: https://github.com/voidmmn/tese_react_nav/blob/12081a70ed645a78a348440e8d1623ac6678e781/src/tese_nav/tese_nav/utils/attraction_field.py
[statistics]: https://github.com/voidmmn/tese_react_nav/blob/12081a70ed645a78a348440e8d1623ac6678e781/src/tese_nav/scripts/analise_estatistica.py
[audit]: https://github.com/voidmmn/tese_react_nav/blob/12081a70ed645a78a348440e8d1623ac6678e781/results/audit_trail.csv
[auditgen]: https://github.com/voidmmn/tese_react_nav/blob/12081a70ed645a78a348440e8d1623ac6678e781/src/tese_nav/scripts/gerar_auditoria.py
[boxplots]: https://github.com/voidmmn/tese_react_nav/blob/12081a70ed645a78a348440e8d1623ac6678e781/src/tese_nav/scripts/gerar_boxplots.py
