# Parecer técnico — segunda rodada de avaliação

**Artigo:** *A Two-Layer Deliberative–Reactive Architecture with an Affective Attraction–Repulsion Layer for Autonomous Substation Inspection*  
**Autores:** Milton Miranda Neto e Alexandre Cardoso  
**Versão examinada:** PDF com sufixo `(1)`, 13 páginas  
**Data:** 10 de setembro de 2026  
**Natureza:** avaliação independente, simulando o rigor de uma revisão da IEEE Access; não constitui decisão editorial da revista.

**Recomendação: o artigo melhorou substancialmente, mas ainda não recomendo sua submissão nesta forma. As pendências ultrapassam uma revisão menor.**

Esta rodada contém correções efetivas de implementação, novos experimentos e dados que agora permitem reproduzir a estatística principal. Não seria correto repetir o parecer anterior como se nada tivesse sido resolvido. Entretanto, persistem problemas na definição operacional de inspeção, na atribuição do benefício do recuo, na equivalência estatística das contagens e na coerência entre resultados, resumo e conclusão.

A IEEE Access adota decisões de aceitação ou rejeição; portanto, “revisão substancial” é aqui uma descrição do trabalho necessário, não uma categoria editorial intermediária. Minha recomendação simulada seria rejeitar a versão atual por necessitar correções, reconhecendo potencial de publicação após resolvê-las. A elegibilidade para uma nova submissão depende da decisão efetivamente recebida da revista. [Processo editorial da IEEE Access](https://ieeeaccess.ieee.org/authors/stages-of-peer-review/).

## 1. Escopo, critérios e evidências

Mantive os critérios da primeira rodada: contribuição e originalidade; correção matemática; correspondência entre algoritmo e código; validade das métricas; desenho experimental e comparadores; estatística; robustez e segurança; reprodutibilidade; literatura; coerência editorial e atendimento aos quatro revisores.

Foram considerados o novo PDF, os comentários originais dos quatro revisores e o parecer anterior de 8 de setembro. A comparação histórica utiliza esse parecer e a extração preservada da versão anteriormente analisada. As páginas indicadas neste documento referem-se ao novo PDF.

Também examinei o pacote público indicado pelo artigo. Na consulta desta rodada, a referência `v1.0-resubmission` aponta para o commit **`8ec78f870e9369f3ac49f48062f7e52c9021fefc`**. Foram lidos os **140 arquivos `results/metrics_*.csv`**, extraídos os valores finais por execução e recalculadas as estatísticas com o novo script disponibilizado. Para E3, também examinei as séries temporais do resíduo e dos contadores de eventos. [Versão do repositório auditada](https://github.com/voidmmn/tese_react_nav/tree/8ec78f870e9369f3ac49f48062f7e52c9021fefc).

Realizei verificações isoladas das funções de conclusão de navegação, prioridade do campo, confirmação de inspeção e inferência de ação. Elas verificam o comportamento dessas funções, sem executar uma missão completa no Gazebo. A leitura dos CSVs e a reprodução da análise não certificam que cada execução histórica tenha sido produzida exatamente pelo código atual; essa correspondência exige identificação da versão por execução. Também não realizei auditoria bibliográfica integral de todas as referências.

**Legenda de atendimento:** atendido = a objeção está resolvida no escopo atual; parcial = houve avanço, mas resta uma pendência material; pendente = a correção necessária não está demonstrada. Uma ressalva nova abaixo decorre da verificação da correção apresentada, mantendo o critério da primeira rodada.

## 2. Correções confirmadas que devem ser preservadas

| Problema da primeira rodada | Evidência desta versão | Resultado da verificação |
|---|---|---|
| Callback tratava cancelamento e aborto como chegada | `StayAlertNode._on_goal_done` verifica o status e o episódio | **Corrigido nesse callback.** Sucesso registra chegada; cancelamento e aborto não registram; resultado de episódio antigo é ignorado |
| Uma atração mais intensa impedia a prioridade de perigo | `AttractionField` mantém canais separados de perigo e atração | **Corrigido.** Acústica +1,14 seguida de perigo −1,05 resulta em −1,05; a ordem inversa também preserva a prioridade |
| CONF suprimia a anomalia antes de o campo arbitrar | O simulador publica perigo e anomalias no mesmo ciclo, sem o antigo retorno antecipado | **Corrigido no fluxo de percepção.** O ensaio passa a exercitar melhor a regra pretendida |
| Investigate não podia ser interrompido por perigo | Preempção antes do tratamento dos estados, com resultado `deferred_hazard` | **Implementado**, sujeito à disponibilidade da pose e ao período refratário; isso limita a generalidade da garantia |
| Keepout recebia posição verdadeira antecipadamente a 8 m | Projeção usa posição percebida e, por padrão, o alcance sensorial de 5 m | **Corrigido nesse canal.** Também foi removida a ativação dependente do nome do cenário |
| Alvo/crédito eram associados à anomalia mais próxima | Seleção por saliência e ID ecoado no início da investigação | **Avanço material.** Restam sincronização pose–ID e rastreabilidade do término |
| Não havia decomposição entre recuo e keepout | KOa e KOb na Tabela 7, p. 10 | **Experimento solicitado realizado**, inclusive com a falha do recuo isolado explicitada |
| O pacote público não reproduzia a revisão | 140 CSVs e `analise_estatistica.py` disponíveis | **Lacuna principal de dados resolvida.** A reprodução numérica das Tabelas 4 e 10 foi possível |
| Equivalência temporal era inferida da não significância | TOST com margem de ±5 s | **Avanço válido para os contrastes temporais**, condicionado à justificativa da margem e das premissas |
| Texto confundia estabilidade com queda monotônica | Fig. 7 e V-F reconhecem picos e ausência de convergência formal | **Melhora substancial**, embora ainda haja redação incompatível na conclusão |
| Localização idealizada era descrita como AMCL efetivo | IV-A e IV-D explicitam transformação fixa | **Esclarecido no método**, restando limpar menções residuais à variabilidade de localização |

A relação com aumento de recompensa também ficou mais coerente: a introdução e a legenda da Fig. 1 já apresentam a tabela de valores como componente passivo, sem atribuir a ela a atuação imediata do robô.

## 3. O que a reanálise dos dados confirma

Há dez tentativas em cada uma das 14 configurações. Pelo critério do script, 136 têm deslocamento superior a 1 m e quatro são excluídas. As exclusões são uma em APF, uma em RHM, uma em N2 e uma em KOb. Os valores de distância dessas quatro execuções são efetivamente próximos de zero, não deslocamentos curtos próximos do limiar de 1 m.

| Configuração | Tentativas / válidas | Inspeções, média ± DP | Missões com todas as anomalias elegíveis inspecionadas | Tempo registrado, média ± DP |
|---|---:|---:|---:|---:|
| E1 — patrulha | 10 / 10 | 0,00 ± 0,00 | 0/10, para as três anomalias fora da rota | 320,26 ± 0,49 s |
| E0 — η = 0 | 10 / 10 | 3,00 ± 0,00 | 10/10 | 363,74 ± 1,10 s |
| E3 — método padrão | 10 / 10 | 3,00 ± 0,00 | 10/10 | 364,44 ± 1,42 s |
| E5 — cenário denso | 10 / 10 | 4,70 ± 0,67 | **8/10**, para cinco anomalias | 402,52 ± 13,45 s |
| APF | 10 / 9 | 3,00 ± 0,00 | 9/9 válidas | 403,80 ± 4,70 s |
| RHM — recuo + keepout | 10 / 9 | 3,00 ± 0,00 | 9/9 válidas | 371,88 ± 1,26 s |
| KOa — keepout sem recuo | 10 / 10 | 3,00 ± 0,00 | 10/10 | 352,22 ± 0,61 s |
| KOb — recuo sem keepout | 10 / 9 | 0,22 ± 0,44 | **0/9**, para três anomalias | 627,16 ± 5,85 s, encerramento por limite |
| N1 — ruído moderado | 10 / 10 | 3,00 ± 0,00 | 10/10 | 366,56 ± 4,92 s |
| N2 — ruído alto | 10 / 9 | 2,33 ± 0,71 | **4/9** válidas | 374,07 ± 7,88 s |
| CONF — conflito | 10 / 10 | 3,00 ± 0,00 | 10/10 para as três fora do conflito; a quarta é suprimida | 364,04 ± 1,78 s |

Os valores representam o critério de inspeção do código publicado, cuja limitação é discutida na seção 5. O tempo de KOb não é tempo até conclusão bem-sucedida. E2, E4 e RHB também foram conferidos; a tabela acima seleciona os grupos necessários às principais conclusões.

As médias e desvios das Tabelas 5–8 conferem com os dados, respeitados os arredondamentos. As diferenças, Cliff’s delta, intervalos bootstrap e valores de p das Tabelas 4 e 10 são reproduzíveis pelo script. Alguns exemplos:

| Comparação e variável | Recalculado | Correspondência com o PDF |
|---|---|---|
| E3 − E1, tempo | +44,18 s; IC bootstrap 95% [43,26; 45,03]; p = 1,81 × 10⁻⁴ | Confere |
| APF − E3, tempo | +39,36 s; IC [36,43; 42,47]; p = 2,17 × 10⁻⁵ | Confere |
| RHM − RHB, distância mínima | +1,00 m; Cliff = 1; p = 2,17 × 10⁻⁵ | Confere |
| E3 − E0, tempo | +0,70 s; IC [−0,39; 1,73]; p de diferença = 0,151 | Confere |
| E0 versus E3, TOST temporal ±5 s | p = 4,09 × 10⁻⁷ | Confere |
| N2 − E3, inspeções | −0,67; IC [−1,11; −0,22]; p ≈ 0,009 | Confere com o procedimento implementado |
| E5 − E3, tempo | +38,09 s; IC [32,53; 47,11] | Confere |

**Reproduzir um cálculo não basta para validar sua interpretação.** As pendências estatísticas abaixo não decorrem de números arbitrários no PDF, mas de escolhas e rótulos do procedimento que os produz. [Script estatístico auditado](https://github.com/voidmmn/tese_react_nav/blob/8ec78f870e9369f3ac49f48062f7e52c9021fefc/src/tese_nav/scripts/analise_estatistica.py).

## 4. Pendência prioritária: resumo e conclusão contradizem os próprios resultados

Na p. 1, o resumo continua afirmando que a camada inspeciona todas as anomalias. Na p. 2, a introdução mantém a mesma generalização para os cenários padrão e adverso. Na p. 12, a conclusão chega a especificar **3/3 no padrão e 5/5 no adverso**.

Isso contradiz os resultados novos: E5 tem 4,7 ± 0,7 e somente 8/10 missões completas; N2 tem 2,3 ± 0,7 e 4/9 missões completas. Em CONF, três de quatro anomalias são inspecionadas, por decisão deliberada de não abordar a anomalia em conflito.

A discussão de V-E e V-G reconhece corretamente essas limitações. Portanto, o problema é uma revisão incompleta das afirmações centrais do artigo. É uma pendência particularmente evitável, porque R1.7 e R2.9 a haviam solicitado expressamente.

Também é preciso corrigir a afirmação de que o método “mais que duplica” tanto a distância quanto o TTC. Pelas médias não arredondadas, RHM/RHB corresponde a aproximadamente **2,41 vezes a distância** e **2,02 vezes o proxy de TTC**. A segunda razão está muito próxima de 2, com dispersão relevante; os testes apresentados avaliam diferença entre grupos, não sustentam uma afirmação inferencial de razão superior a 2. A expressão “aproximadamente duplica o proxy radial” é mais defensável.

O aumento de tempo de aproximadamente 14% descreve E3 em relação a E1. Não deve resumir como se fosse uniforme o custo de E5, N2 e RHM, nem justificar uma garantia de custo limitado. Um timeout limita a duração da tentativa; não garante conclusão dentro de um limite.

**Critério de encerramento:** resumo, introdução, legendas e conclusão devem usar os mesmos denominadores, cenários, métricas e limites descritos nas tabelas. Eliminar “todas” sem qualificação e “garantia categórica de segurança”.

## 5. Pendência prioritária: o que conta como inspeção concluída

### 5.1. A falha antiga de status foi corrigida

Executei isoladamente `_on_goal_done` com sucesso, cancelamento e aborto. Somente sucesso preencheu `_reached_at`. Um sucesso de episódio anterior também foi ignorado. Essa correção resolve o falso reconhecimento de chegada pelo simples término da ação que havia sido identificado na primeira rodada.

### 5.2. A confirmação independente ainda não implementa o critério anunciado

As pp. 5–7 descrevem chegada ao standoff do alvo verdadeiro e permanência de três segundos. Entretanto, `AnomalySimulator._on_event` recebe o fim com motivo de inspeção e verifica apenas a distância na última pose disponível. O limiar automático é:

**2,0 m de standoff + 0,8 m de margem + 0,5 m adicional = 3,3 m.**

Em uma verificação isolada, um evento de término com o robô a **3,2 m** do alvo foi aceito como inspeção. Isso é permitido pelo código, mas diverge de uma leitura de “within the inspection standoff” como estar a até 2 m. Standoff como alvo nominal pode admitir tolerância; o problema é não definir nem justificar a tolerância efetivamente usada na métrica.

O supervisor espera três segundos após o sucesso da navegação, o que é um avanço. Contudo, o avaliador não verifica independentemente a permanência na região durante esse intervalo, nem orientação/campo de visão. Ele confirma proximidade final após receber a mensagem. A pose também é a última obtida pelo ciclo do simulador; falta um requisito explícito de atualidade da amostra.

Não concluo que todas as inspeções estejam erradas. Concluo que a métrica atual mede **navegação concluída, espera comandada e proximidade final dentro de 3,3 m**, e não toda a condição física descrita no manuscrito.

Há duas soluções defensáveis: implementar um avaliador da condição completa, com região, tolerâncias e permanência claramente definidas; ou limitar o nome e a descrição da métrica ao que foi efetivamente verificado. Para manter a alegação de inspeção com dwell confirmado, recomendo a primeira.

### 5.3. Falhas ainda não têm registro suficiente

Quando a confirmação de proximidade falha, o simulador adiciona o alvo a `failed` e escreve uma mensagem de log, mas não publica um desfecho específico que o coletor contabilize como rejeição da confirmação. Em N2, há inspeções não creditadas, embora os CSVs registrem zero timeouts de investigação, zero abortos e zero adiamentos. Isso é compatível com o mecanismo descrito na discussão, mas o conjunto de métricas não permite quantificar diretamente quantas falhas foram causadas por cada etapa.

Em E5, as duas execuções incompletas iniciaram cinco investigações cada. `metrics_E5_20260909_162649.csv` registra três inspeções, dois timeouts e um aborto de navegação; `metrics_E5_20260909_170733.csv` registra quatro inspeções, um timeout e um aborto. Portanto, a explicação da p. 11 — deixar o layout sem revisitar todos os eventos — não descreve suficientemente o que os contadores mostram: houve tentativas iniciadas que não concluíram. Aborto e timeout podem pertencer ao mesmo episódio e não devem ser somados como falhas independentes. Em N2, as nove execuções válidas também iniciaram três investigações cada, reforçando a necessidade de registrar explicitamente a falha de confirmação.

O pseudocódigo encerra a investigação quando a navegação é abortada/cancelada; o código registra o resultado e pode permanecer no estado até expirar o orçamento, pois `_nav_outcome` não é usado nessa transição. Há ainda um caso assíncrono residual: uma resposta tardia de aceitação de meta é ignorada por `_on_goal_resp` sem cancelar explicitamente a meta aceita daquele episódio. É um risco de gerenciamento de metas a verificar, não uma falha observada nas 140 missões.

**Critério de encerramento:** um registro por episódio deve vincular ID do evento, ID da meta, posição percebida, chegada, início/fim do dwell, confirmação independente e motivo de falha. Publicar separadamente compromisso, inspeção confirmada, aborto, rejeição, timeout, adiamento e falha de confirmação. Verificar uma meta inalcançável e uma resposta tardia de aceitação.

Fontes: [supervisor reativo](https://github.com/voidmmn/tese_react_nav/blob/8ec78f870e9369f3ac49f48062f7e52c9021fefc/src/tese_nav/tese_nav/stay_alert_node.py) e [simulador/avaliador](https://github.com/voidmmn/tese_react_nav/blob/8ec78f870e9369f3ac49f48062f7e52c9021fefc/src/tese_nav/tese_nav/anomaly_simulator.py).

## 6. O que KOa e KOb mudam na contribuição científica

A Tabela 7 é uma das melhores adições da revisão. Ela permite distinguir componentes que antes eram confundidos.

| Resultado recalculado | RHM: recuo + keepout | KOa: keepout sem recuo | KOb: recuo sem keepout |
|---|---:|---:|---:|
| Inspeções | 3,00 | 3,00 | 0,22 |
| Distância mínima | 1,713 m | 1,714 m | 4,291 m |
| Proxy radial mínimo de TTC | 5,583 s | 5,812 s | 8,663 s |
| Recuos | 1,00 | 0,00 | 29,56 |
| Tempo registrado | 371,88 s | 352,22 s | 627,16 s, sem concluir a missão |
| Tempo abaixo de 2 m | 9,204 s | 9,306 s | 0,000 s |

A interpretação principal é que **o keepout permite resolver o perigo sobre a rota, enquanto o recuo isolado preserva distância às custas de oscilação e falta de progresso**. O texto já reconhece boa parte disso e deve preservar esse resultado negativo.

O ponto ainda insuficientemente enfrentado é que KOa conclui as mesmas inspeções, apresenta praticamente a mesma distância mínima e é **19,66 s mais rápido**, cerca de 5,6% em relação ao seu próprio tempo. O método completo não apresenta vantagem demonstrada sobre KOa nos indicadores principais da Tabela 7. Há uma pequena redução descritiva do tempo abaixo de 2 m, aproximadamente 0,10 s, que impede afirmar dominância absoluta em todas as métricas; esse possível benefício precisa ser contextualizado, não presumido relevante.

Como análise exploratória adicional, aplicando o mesmo bootstrap do pacote ao contraste RHM − KOa, obtive IC 95% de **[18,79; 20,49] s** para o acréscimo de tempo e **[−0,0105; 0,0071] m** para a diferença de distância mínima. São cálculos desta revisão, não uma nova família confirmatória pré-especificada. O segundo intervalo não prova igualdade, mas mostra que a diferença observada de distância é muito pequena neste cenário.

A afirmação de que o recuo é uma “resposta inicial rápida” pode ser verdadeira, mas a Tabela 7 não mede latência de reação, transiente de aproximação ou resposta a perigo novo durante a execução. Falta demonstrar qual benefício compensa o custo adicional do recuo.

**Correção necessária:** apresentar KOa como comparador central e discutir o resultado com clareza. Se o recuo permanecer como contribuição essencial, acrescentar um ensaio direcionado de perigo que surge durante movimento ou investigação, medindo latência, distância durante o transiente e recuperação, sob a mesma informação. Alternativamente, delimitar o recuo como componente de projeto cujo benefício incremental ainda não foi demonstrado e concentrar a contribuição comprovada na supervisão e integração do keepout.

Não é necessário inventar uma função de utilidade a posteriori para favorecer RHM. A arquitetura pode ser útil mesmo quando a ablação mostra que um componente é dispensável no cenário estático avaliado.

## 7. Segurança: prioridade lógica melhorou; garantia física continua excessiva

A prioridade do perigo foi corrigida no campo e incorporada à preempção de Investigate. Isso atende a uma parte importante da primeira rodada. Entretanto, a p. 10 ainda fala em “categorical safety guarantee”, inclusive associando-a ao entorno de equipamentos energizados.

O resultado demonstrado é mais limitado: uma regra de seleção privilegia perigo sob condições explícitas, e não foram observadas entradas no raio de contato simulado nas execuções consideradas. Não há demonstração de invariância de um conjunto seguro, tratamento geral de falhas de percepção ou garantia física de afastamento.

RHM permanece em média **9,2 s abaixo do limiar de folga de 2 m** usado pelo próprio avaliador. Isso não é contraditório com melhorar a segurança relativa, mas é incompatível com apresentar a zona como inviolável. A definição de contato por distância inferior a 0,5 m e a qualificação do TTC como proxy na p. 11 são correções adequadas; elas precisam aparecer também onde os resultados são interpretados de forma mais forte.

O período refratário é de 8 s no código e impede nova preempção nesse intervalo. A existência de uma pose de recuo é outra condição. Além disso, o sinal de um perigo delegado ao keepout é suprimido. Essas condições precisam integrar a definição da propriedade alegada, sobretudo se um segundo perigo aparecer durante o refratário. CONF estático não verifica todas essas situações.

A implementação do keepout também continua diferente da sequência descrita no Algoritmo 1:

- A projeção ocorre no ciclo de percepção ao detectar o perigo, independentemente de iniciar o recuo; não é consequência de concluir o recuo.
- A marca fica retida até o fim da missão; não há expiração temporal do keepout “temporário” descrito no texto.
- A delegação ocorre em `avoid_start`, não após recuo confirmado, e seleciona perigo por proximidade à posição verdadeira. Embora a projeção tenha deixado de usar informação privilegiada, essa lógica de seleção ainda consulta a geometria verdadeira.
- A delegação não confirma explicitamente que a mesma observação/ID já produziu uma marca válida no planejador. Sob ruído, os canais podem utilizar amostras distintas.

Isso não exige abandonar o keepout: exige descrevê-lo como marca persistente de perigo percebido e estabelecer um protocolo verificável de transferência para o planejador. Distinguir o fim do sinal reativo do afastamento físico.

O limite superior de risco de aproximadamente 26% para zero ocorrências em dez missões independentes, agora reconhecido na p. 11, é uma melhoria. Para grupos com nove válidas, o limite unilateral análogo é aproximadamente 28,3%. São ilustrações da incerteza amostral, não estimativas de risco elétrico real.

**Critério de encerramento:** usar “prioridade de seleção” para a propriedade lógica; “aumento observado de distância/redução de exposição” para os resultados; e retirar a garantia geral de segurança. Se quiser manter uma alegação de resposta transiente robusta, o teste direcionado proposto na seção 6 pode validar simultaneamente preempção e utilidade do recuo. [Coletor de métricas de segurança](https://github.com/voidmmn/tese_react_nav/blob/8ec78f870e9369f3ac49f48062f7e52c9021fefc/src/tese_nav/tese_nav/metrics_node.py).

## 8. Estatística: números reproduzíveis, com três correções obrigatórias

### 8.1. Wilson não é um intervalo “exato”

Os intervalos publicados para 8/10, aproximadamente [0,49; 0,94], e para 4/9, aproximadamente [0,19; 0,73], correspondem corretamente ao **intervalo de Wilson**. A correção necessária é chamá-los pelo nome adequado. Wilson é um intervalo de escore; o intervalo binomial usualmente chamado exato é o de Clopper–Pearson. Não usar “exact (Wilson)” nem depois chamar o mesmo intervalo de exato. [Documentação dos métodos binomiais em statsmodels](https://www.statsmodels.org/stable/generated/statsmodels.stats.proportion.proportion_confint.html).

Isso não exige substituir Wilson: basta corrigir o rótulo e manter o método consistente. Também convém reportar a incerteza dos grupos 10/10 e 9/9, cujos intervalos de Wilson são aproximadamente [0,72; 1] e [0,70; 1].

### 8.2. O TOST para contagens constantes não valida equivalência

Na função `tost`, quando o erro padrão é zero, o programa retorna p = 0 se a diferença observada estiver dentro da margem. E3 e N1 têm dez contagens iguais a três; essa exceção é acionada e produz o resultado exibido na Tabela 10 como p inferior a 10⁻⁶.

Isso é uma decisão programada para um caso degenerado, não evidência inferencial de equivalência entre as populações. A ausência de dispersão em duas pequenas amostras no teto da escala não demonstra ausência de variabilidade populacional. O problema é especialmente importante porque o Apêndice B usa esse resultado para concluir equivalência sob ruído moderado.

**Correção obrigatória:** retirar esse p e limitar a conclusão a desempenho observado idêntico, com incerteza por missão; ou empregar um procedimento de equivalência apropriado ao desfecho binário/limitado, com margem substantiva e amostra capaz de sustentá-lo. Não é necessário refazer toda a bateria para corrigir a afirmação.

Os TOST temporais E0 versus E2/E3/E4 não têm esse mesmo defeito: apresentam variância positiva e os valores são reproduzíveis. Permanecem a necessidade de justificar a margem de ±5 s, informar a premissa de amostras independentes ou eventual pareamento e distinguir uma margem declarada no manuscrito de uma pré-especificação documentada antes da análise.

### 8.3. O método de p deve corresponder à implementação

A legenda da Tabela 4 e o Apêndice B descrevem permutação exata quando um braço é degenerado. O script trata exatamente o caso especial em que **ambos** são constantes e distintos; em outras comparações com empates, usa aproximação assintótica de Mann–Whitney. Isso explica, por exemplo, o p de aproximadamente 1,8 × 10⁻⁴ para tempo E1/E3, embora a separação entre os grupos seja completa.

O uso assintótico não torna automaticamente toda a análise inválida. Mas a descrição precisa dizer o que foi realizado. Para amostras pequenas com empates, é preferível verificar os contrastes relevantes por permutação apropriada, em vez de chamar o resultado de exato. O método exato comum de Mann–Whitney sem tratamento de empates não resolve esse problema sozinho. [Documentação de Mann–Whitney no SciPy](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.mannwhitneyu.html).

A correção de Holm da família de sete comparações está implementada de forma coerente e foi reproduzida. As comparações secundárias devem ser chamadas exploratórias se não houver controle correspondente de multiplicidade. O IC bootstrap da diferença de médias e o teste de postos respondem a perguntas relacionadas, mas não idênticas; evitar tratá-los como o mesmo teste sobre a média.

Há ainda um defeito no cálculo automatizado de “inspeção completa”: o script toma o **máximo observado no grupo** como número-alvo. Esse denominador deve vir da definição do cenário. Em KOb, por exemplo, o máximo observado é um, embora existam três anomalias; se o grupo fosse incluído no laço atual, o critério poderia chamar uma inspeção de completa. Para CONF, definir previamente três anomalias elegíveis e uma suprimida, sem derivar esse total dos resultados.

## 9. Reprodutibilidade, exclusões e duração de missão

A publicação dos 140 arquivos e do novo script é uma resposta concreta ao maior problema de reprodutibilidade da primeira rodada. As sementes por repetição também estão presentes: o executável passa o número da repetição e os CSVs registram `run_seed`. A frase da p. 8 sobre uma semente fixa deve ser atualizada para refletir esse protocolo.

Restam cinco pontos verificáveis:

1. **KOa e KOb estão ausentes de `CONFIGS` no script estatístico.** O programa lê os 140 arquivos e conta 136 válidos, mas produz resumo e tabelas por configuração para apenas 12 grupos. A Tabela 7 pode ser reconstruída dos dados, como fiz nesta rodada, porém não é gerada pelo fluxo anunciado. Incluir as duas ablações e os denominadores válidos.
2. **O script de bateria em blocos é uma retomada parcial.** E3 e CONF aparecem como já concluídos e não são novamente executados por suas chamadas. Isso pode ser adequado para a coleta realizada, mas o pacote precisa de um comando explícito que gere toda a matriz a partir do zero, com ordem e parâmetros identificáveis.
3. **O limite de 600 s não está implementado como medição direta de tempo decorrido.** O shell incrementa um contador em dez segundos após cada espera, mas a consulta de conclusão também consome tempo. As métricas usam relógio ROS; o decaimento do campo usa relógio monotônico de parede. Assim, o orçamento nominal do shell, o tempo simulado e a duração registrada não são intercambiáveis. Isso ajuda a explicar a necessidade de esclarecer os 627 s de KOb, sem provar por si só a origem de toda a diferença.
4. **Imobilidade não identifica sozinha a causa da falha.** As quatro excluídas têm deslocamento praticamente nulo, o que sustenta separar essas tentativas da análise de navegação em movimento. Entretanto, três possuem duração de missão acumulada superior a 600 s; logo, o estado de início da missão chegou ao coletor. A frase “mission never started” não é literalmente válida para todas. Distinguir missão sinalizada, movimento iniciado, falha de bringup e falha de atuação, apoiando o diagnóstico em logs.
5. **A referência de versão mudou.** O parecer anterior registrou `v1.0-resubmission` apontando para `32bbe7a729ca51f99711e759903505ab592c3da6`; nesta rodada ela resolve para `8ec78f870e9369f3ac49f48062f7e52c9021fefc`. Citar o commit exato e criar uma versão nova identificável, preservando as anteriores, evita que o mesmo nome signifique conjuntos experimentais diferentes.

A confiabilidade de inicialização/movimento observada é 136/140 = **97,1%**. Ela não é taxa de missão concluída: KOb tem nove execuções em movimento que não concluem a tarefa. Para N2, por exemplo, inspeção completa é 4/9 condicional às válidas e **4/10 por tentativa**; para APF e RHM, é 9/9 válidas e 9/10 por tentativa. Mostrar ambas as perspectivas responde melhor à solicitação sobre exclusões.

O novo conjunto substitui resultados anteriores e distingue as quatro tentativas imóveis dos antigos timeouts. A resposta aos revisores deve registrar essa substituição, as correções de código que a motivaram e a rastreabilidade do conjunto antigo. Não apresentar a nova exclusão como se fosse, por si só, a análise de sensibilidade dos dois timeouts da primeira submissão.

Para os desfechos temporais, publicar um indicador explícito de missão concluída e motivo de término. Em KOb, reportar tempo até interrupção/censura e taxa de conclusão zero; não misturar esse valor com tempos até sucesso na interpretação de eficiência.

## 10. Campo afetivo, identidade e atualização de valores

A Eq. 6 reconhece corretamente que, para taxa de aprendizagem fixa e não nula, o termo externo pode ser representado por aumento de recompensa. A dupla contagem foi retirada. Esse ponto pode ser considerado atendido conceitualmente.

A Eq. 4, p. 5, ainda mistura a escolha de um índice por `argmax` com a atribuição de um valor escalar a Φ. Também indexa modalidades, embora múltiplos eventos da mesma modalidade possam coexistir. Definir conjuntos de eventos elegíveis, selecionar explicitamente o evento, estabelecer desempate e então atribuir sua contribuição ao campo. Definir o caso sem eventos e como a memória temporal participa da seleção.

O código mantém memórias separadas de atração e perigo e faz o perigo dominar até a magnitude residual cair abaixo de 10⁻³. Isso não é inteiramente descrito pela equação instantânea seguida de um único decaimento escalar. A regra matemática deve representar a implementação publicada, incluindo persistência de estímulos anteriores.

A seleção por saliência e o ID no início da investigação são correções importantes. Porém, ID e pose trafegam em tópicos separados, sem uma mensagem atômica com timestamp/episódio. O término também não transporta explicitamente o ID do evento. Sob atualização de alvo, não fica garantido que a pose consumida e o ID ecoado se refiram à mesma observação. Essa é uma pendência de consistência a resolver ou a testar sob troca rápida de alvos.

A tabela Q continua fora do caminho de atuação. Não é necessário exigir que o autor construa uma política aprendida se o artigo assumir esse escopo. Mas o diagnóstico de valores ainda precisa ser matematicamente interpretável:

- A nova função infere a ação da odometria, o que melhora a associação ação–transição. Entretanto, verifica deslocamento linear pequeno antes da rotação. Uma rotação pura foi classificada como `stop` na verificação isolada; isso prejudica o significado de `left/right/stop`.
- A recompensa denominada progresso permanece uma constante por atualização de odometria. Explicar esse fato ou usar uma medida real de progresso, deixando clara a dependência da frequência de amostragem.
- O estado com célula e módulo de Φ não representa univocamente sinal, identidade e memória. A notação Φ(s) exige essa ressalva; Φ no instante t é mais precisa quando o estado não incorpora a memória necessária.
- A p. 5 ainda afirma que uma ação greedy é computada para logging, enquanto o trecho revisado de atualização usa a ação inferida do movimento. Atualizar a descrição para corresponder ao código.

Se Q permanecer apenas como formulação prospectiva, recomendo reduzir seu peso no resumo, palavras-chave e contribuição central, ou deslocar detalhes para apêndice. Isso evita que o leitor espere um benefício de aprendizagem que os experimentos não pretendem demonstrar. [Atualização de valores auditada](https://github.com/voidmmn/tese_react_nav/blob/8ec78f870e9369f3ac49f48062f7e52c9021fefc/src/tese_nav/tese_nav/bellman_node.py).

## 11. Figura 7 e afirmações de estabilidade

A revisão agora usa o resíduo completo, agrega dez execuções de E3 e descreve uma trajetória não monotônica. Os CSVs sustentam a existência de picos durante os episódios de inspeção e valores finais pequenos. A média dos últimos valores registrados em E3 é aproximadamente **0,0198**, com desvio de aproximadamente **0,0103**, coerente com a Tabela 5.

Isso resolve boa parte das objeções R1.4 e R2.4. Permanecem três cuidados:

- Definir “95% band”: intervalo de confiança da média, percentis entre execuções ou outra construção? Indicar normalização do tempo, interpolação, suavização e tratamento das amostras após `COMPLETE`. O último registro do CSV não é necessariamente o instante exato de conclusão da missão.
- Não chamar a faixa de estreita “throughout” sem qualificação: visualmente ela se alarga nos picos. O pico intermediário da média também é menor do que o intervalo de 0,25–0,30 citado para cada uma das três investigações.
- Resíduos pequenos e limitados em missões finitas apoiam estabilidade empírica dos incrementos observados, não convergência da tabela. Na p. 12 ainda aparece a formulação de convergência avaliada empiricamente; substituir por estabilidade dos incrementos durante as simulações.

Se o diagnóstico Q continuar tendo destaque, acrescentar a curva E0 nas mesmas condições permite responder diretamente à comparação solicitada com a atualização sem o termo afetivo. Se for tratado como material secundário, a redação deve refletir esse papel e não sugerir uma conclusão teórica que a figura não fornece.

## 12. Comparadores, robustez e relevância da contribuição

E0 demonstra que η não altera o mecanismo de controle; não demonstra que a formulação afetiva supera uma heurística equivalente. APF oferece um comparador reativo útil, mas também muda o controlador: o método envia metas ao Nav2/MPPI, enquanto APF atua por forças/velocidades. Ganhos, limites, standoff e orçamento de investigação devem estar documentados e alinhados ou justificados.

O código APF mantém parâmetros próprios, incluindo standoff de 1,8 m e orçamento de 30 s, frente aos 2 m e 40 s descritos para Stay Alert. Assim, a redução temporal observada sustenta vantagem sobre **essa implementação APF**, sem isolar como causa a ponderação afetiva. E3 gasta aproximadamente 9,7% menos tempo que APF e percorre distância praticamente igual; a vantagem principal é temporal.

O comparador ainda mais informativo é um supervisor de detecção, escolha de alvo e retorno usando os mesmos Nav2/MPPI, metas, informação e critérios de inspeção, com prioridade simples e sem a memória/ponderação afetiva. A primeira rodada já o recomendava. KOa agora responde à decomposição de segurança, mas não substitui essa comparação para a originalidade do mecanismo de atração.

Não considero obrigatório acrescentar PPO ou DDQN apenas para aumentar a lista de baselines. A solicitação original fazia sentido para uma contribuição de aprendizado por reforço. Com o novo escopo, a carta de resposta pode justificar a escolha de supervisores comparáveis. Se o artigo continuar reivindicando avanço em aprendizagem, essas comparações e uma política Q atuante voltam a ser necessárias.

A robustez melhorou: o ruído agora tem sementes por repetição, a degradação de N2 é reportada e E5 já não apresenta resultado artificialmente perfeito nas tabelas. Porém, N1/N2 variam posição e intensidade conjuntamente; não identificam isoladamente a causa da perda. Dois níveis em uma geometria não sustentam robustez geral. “Graceful degradation” é uma interpretação forte para queda de 10/10 para 4/9 missões completas; é melhor reportar a perda quantificada e os indicadores de segurança observados.

Persistem limitações assumidas de localização, persistência de eventos, latência, falsos negativos e geometria. Não é necessário executar uma campanha ilimitada: eliminar promessas de varreduras não realizadas e priorizar o teste de perigo durante investigação, que resolve diretamente uma alegação central. Na p. 4, a menção à sensibilidade ao raio/perfil de detecção ainda precisa corresponder a um resultado apresentado ou ser transferida para trabalho futuro.

## 13. Literatura, terminologia e apresentação do PDF

O título atual representa melhor a contribuição real. A Tabela 1 e a bibliografia de 21 referências são avanços preservados, mas a distinção em relação a supervisores híbridos, arbitragem por prioridade e replanejamento por mapa de risco ainda precisa ser mais direta. A novidade não pode depender essencialmente da combinação com um Bellman que não atua na navegação.

A definição de *active sensing* na comparação exige coerência. O próprio trabalho aparece como “Yes (patrol)”, embora a patrulha seja fixa e o texto associe o conceito a movimentos para obter observações além de uma rota fixa. Distinguir patrulha com exposição dos sensores, reposicionamento acionado por eventos e planejamento informativo de observações. O trabalho pode realizar o segundo sem demonstrar otimização do terceiro.

A referência [2] continua citada como 2025. O registro oficial consultado novamente apresenta publicação em **4 de fevereiro de 2026** e citação com ano **2026**, embora o volume corresponda a 2025. Ajustar pelos metadados do editor. [Registro oficial do artigo de Zhang e colaboradores](https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2025.1759501/full).

Na inspeção visual do novo PDF:

- **A Eq. 6, p. 5, ultrapassa a largura da coluna e invade o texto à direita.** Quebrar a equação em linhas ou usar uma forma abreviada corretamente definida. É um defeito visível de composição, não um artefato da extração textual.
- A Fig. 3 já inclui preempção e nota de refratário, mas os rótulos são pequenos. O Algoritmo 1 precisa refletir a projeção persistente do keepout, a saída por falha e o timeout de Avoid implementado no código.
- As Tabelas 4, 6–8 e 10 deveriam informar n válido por configuração ou por par, especialmente para APF, RHM, N2 e KOb.
- A Tabela 3 deve incluir tolerância real de confirmação, refratário, raio do keepout e parâmetros relevantes do baseline; separar parâmetros de percepção, controle e avaliação.
- Permanecem datas de exemplo, DOI de exemplo e rodapé “VOLUME 11, 2023”. Preparar a versão de submissão sem metadados que pareçam atribuídos pela revista.
- A ordem das figuras na declaração de assistência de IA permanece corrigida. Não há necessidade de reabrir essa observação como pendência.

## 14. Atendimento aos comentários originais — mesma matriz da primeira rodada

### Revisor 1

| Item | Estado nesta rodada | Evidência e pendência |
|---|---|---|
| R1.1 — teoria e convergência | **Parcial, muito avançado** | Recompensa aumentada e ausência de garantia reconhecidas em III-B; corrigir a frase de convergência empírica da p. 12 |
| R1.2 — estatística | **Parcial** | Tabelas reproduzidas, efeito/IC/Holm disponíveis; corrigir Wilson, TOST degenerado, método exato/assintótico e n por grupo |
| R1.3 — robustez | **Parcial** | Ruído com sementes e perda de completude quantificada; alcance ainda limitado a poucos cenários |
| R1.4 — todas as execuções e comparação Q | **Parcial, avançado** | Resíduo completo e dez séries disponíveis; definir faixa/processamento e incluir E0 se Q mantiver destaque |
| R1.5 — literatura comparativa | **Parcial** | Tabela e referências preservadas; melhorar comparação com supervisão híbrida próxima e active sensing |
| R1.6 — custo e utilidade | **Parcial, avançado** | Distância/tempo por inspeção e novas ablações; discutir KOa e tempos censurados, limitar “bounded” |
| R1.7 — resumo alinhado | **Pendente na alegação de completude** | Resumo continua generalizando todas as anomalias, apesar de E5/N2 |

### Revisor 2 — comentários maiores

| Item | Estado nesta rodada | Evidência e pendência |
|---|---|---|
| R2.1 — papel de Q e ablação | **Parcial, muito avançado** | Não atuação de Q e E0 demonstrados; corrigir ação inferida e descrição de logging |
| R2.2 — shaping e dupla contagem | **Atendido conceitualmente** | Eq. 6 e introdução reconhecem aumento de recompensa; falta apenas corrigir composição da equação |
| R2.3 — interpretação de η | **Atendido no escopo comportamental** | Invariância decorre da arquitetura e não é vendida como sensibilidade de uma política aprendida; TOST temporal é reproduzível |
| R2.4 — estabilidade completa | **Parcial, avançado** | Resíduo completo agregado; faltam definição da faixa e consistência final da linguagem |
| R2.5 — comparadores justos | **Parcial** | E0/APF/KOa/KOb são úteis; documentar APF e comparar com supervisor equivalente ou limitar contribuição |
| R2.6 — segurança e recuperação | **Parcial, avançado** | Perigo na rota e decomposição realizados; permanecem exposição abaixo de 2 m e garantia excessiva |
| R2.7 — estatística, dados e timeouts | **Parcial, com avanço decisivo** | 140 CSVs e análise principal reproduzíveis; corrigir inferência e distinguir tentativas, censura e substituição da bateria antiga |
| R2.8 — inspeção, identidade e falha | **Parcial; ainda prioritário** | Status correto, ID e estados separados; avaliador aceita 3,3 m sem dwell independente e não contabiliza todas as rejeições |
| R2.9 — alegações excessivas | **Pendente em pontos centrais** | Resumo/conclusão contradizem E5/N2; segurança categórica permanece |
| R2.10 — literatura | **Parcial** | Escopo bibliográfico cresceu, mas diferenciação frente a supervisores próximos ainda é fraca |

### Revisor 2 — comentários menores

| Item | Estado nesta rodada | Evidência e pendência |
|---|---|---|
| R2.m1 — fronteira do raio | **Parcial** | Histerese/compromisso descritos; retirar promessa de varredura não apresentada ou acrescentar resultado |
| R2.m2 — argmax | **Pendente** | Eq. 4 ainda não define corretamente evento, valor, empate e conjunto vazio |
| R2.m3 — Φ e ação | **Parcial** | Dependência de ação foi retirada, mas estado não representa sinal/memória completamente |
| R2.m4 — resíduo zero no baseline | **Atendido** | Legenda explica atualização inativa; “não aplicável” continua uma alternativa editorial |
| R2.m5 — reprodução | **Parcial, muito avançado** | Sementes, dados e script disponíveis; atualizar texto, versão, relógios e incluir KOs no gerador |
| R2.m6 — metadados | **Pendente** | Datas/DOI/rodapé de exemplo permanecem |

### Revisores 3 e 4

| Item | Estado nesta rodada | Evidência e pendência |
|---|---|---|
| R3.1 — ganho de Bellman | **Atendido quanto à distinção causal** | Q não comanda ações; o ganho próprio do diagnóstico não deve ser superestimado |
| R3.2 — perigo na rota | **Atendido quanto ao ensaio; parcial na conclusão** | RHM/RHB e KOa/KOb respondem à geometria; garantia física não demonstrada |
| R3.3 — estabilidade/convergência | **Parcial, avançado** | Fig. 7 e V-F melhoraram; remover formulação residual na conclusão |
| R4.1 — η = 0 e reformulação | **Atendido no reposicionamento principal** | Título, introdução, Fig. 1 e ablação refletem supervisão reativa |
| R4.2 — baseline simples | **Parcial** | APF e KOa ajudam; comparabilidade de atuação e benefício da parametrização afetiva permanecem |
| R4.3 — segurança e conflito | **Parcial, muito avançado** | Arbitragem de perigo corrigida e percepção publica ambas as modalidades; falta limitar a garantia e validar condições temporais |
| R4 menor — chattering/fronteira | **Parcial** | Refratário documentado e KOb revela oscilação; integrar isso à propriedade operacional |
| R4 menor — Welch degenerado | **Parcial** | Substituição principal realizada; surgiu uso inválido de TOST para contagem constante |
| R4 menor — ordem das figuras | **Atendido** | Agradecimento mantém sequência correta |

## 15. Plano de encerramento das pendências

Não recomendo repetir experimentos apenas para aumentar a amostra. A próxima rodada deve produzir evidência dirigida às lacunas restantes.

| Prioridade | Ação | Evidência suficiente para encerrar |
|---|---|---|
| **P0** | Corrigir resumo, introdução e conclusão | Completude E5 = 8/10 e N2 = 4/9; CONF com denominador explícito; nenhuma garantia geral de segurança |
| **P0** | Fixar a definição de inspeção | Critério espacial e temporal documentado; log de confirmação/rejeição por evento; contagens recalculadas ou claramente limitadas ao proxy atual |
| **P0** | Corrigir TOST degenerado e Wilson | Remoção do p artificial; método de equivalência apropriado ou descrição sem equivalência; rótulos corretos de IC |
| **P1** | Resolver a interpretação de KOa | Comparação explícita de custo e segurança; benefício do recuo demonstrado em teste dirigido ou delimitado como não demonstrado |
| **P1** | Alinhar keepout e transições | Pseudocódigo reproduz projeção, persistência, delegação e falhas; tratamento verificável de callbacks tardios |
| **P1** | Fechar a reprodução da bateria | Gerador com 14 grupos, n por grupo, motivo de término e versão por execução; novo identificador de versão |
| **P1** | Corrigir Eq. 4 e a identidade dos eventos | Seleção por evento com desempate/memória; pose e ID associados ao mesmo episódio |
| **P1** | Tornar a comparação reativa justa | Mesma informação e controlador no comparador relevante, ou restrição explícita da alegação à implementação APF testada |
| **P2** | Finalizar diagnóstico Q e Fig. 7 | Ação/recompensa descritas corretamente; faixa e processamento definidos; linguagem restrita à estabilidade empírica |
| **P2** | Revisar apresentação e bibliografia | Eq. 6 sem sobreposição, parâmetros/n completos, referência [2] corrigida e metadados de exemplo removidos |

P0 pode alterar interpretação ou validade do resultado principal; P1 afeta contribuição, operação ou reprodução; P2 afeta precisão secundária e apresentação. Se o avaliador de inspeção for alterado, a necessidade de nova coleta depende de os logs existentes permitirem reconstruir o critério corrigido. Não presumir que apenas editar o texto valida retrospectivamente uma condição física não registrada.

A carta aos revisores deve apresentar cada comentário, mudança concreta, localização e evidência. Para pontos resolvidos por restrição de escopo, declarar explicitamente essa escolha. Evitar afirmar genericamente que “todos os comentários foram atendidos” enquanto as pendências acima permanecerem.

## 16. Julgamento final nos critérios da primeira rodada

| Critério | Avaliação atual |
|---|---|
| Relevância para inspeção robótica | **Boa.** Problema pertinente e aplicação claramente motivada |
| Contribuição ao conhecimento | **Potencial, ainda insuficientemente isolada.** KOa altera a justificativa do recuo; originalidade deve se apoiar no supervisor efetivamente avaliado |
| Solidez técnica | **Melhorou muito, mas ainda incompleta.** Status e prioridade foram corrigidos; confirmação de inspeção e protocolo de metas exigem fechamento |
| Validação experimental | **Moderada.** Há ablações úteis e resultados negativos; faltam igualdade de condições em comparadores e evidência transiente para a função atribuída ao recuo |
| Estatística | **Reproduzível, com correções obrigatórias.** Tabelas principais conferem; equivalência de contagens e rótulos de métodos não estão corretos |
| Segurança | **Evidência específica em simulação.** Não sustenta garantia categórica de segurança física |
| Reprodutibilidade | **Avanço decisivo.** Dados presentes e reanálise possível; faltam fechar pipeline, versão e desfechos por tentativa |
| Abrangência e referências | **Adequadas como base, ainda com lacunas de posicionamento.** Não é uma questão de atingir um número arbitrário de referências |
| Clareza e apresentação | **Boa estrutura, revisão final incompleta.** Contradições no resumo/conclusão e sobreposição da Eq. 6 são visíveis |
| Prontidão para submissão | **Ainda não.** Recomendo resolver P0 e as pendências P1 relacionadas à contribuição central antes de enviar |

O mérito desta revisão é ter transformado várias intenções em correções verificáveis e resultados reproduzíveis. O trabalho necessário agora é mais localizado: assegurar que “inspeção” signifique o que o método mede, retirar inferências estatísticas indevidas e explicar por que a arquitetura completa é preferível ao keepout isolado nas condições em que essa preferência é alegada. Com esses pontos resolvidos, a avaliação poderá se concentrar no mérito científico do supervisor, sem ficar comprometida por inconsistências evitáveis entre texto, código e dados.
