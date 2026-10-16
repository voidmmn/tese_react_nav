# Parecer conjunto do manuscrito e da carta de resposta — Access-2026-46291

**Data:** 16 de outubro de 2026  
**Manuscrito examinado:** PDF terminado em `(8).pdf`, 21 páginas, compilado em 16/10/2026.  
**Carta examinada:** `response_to_reviewers_46291(3).md`.  
**Fontes examinadas:** `access.tex` e os sete arquivos de seções, da introdução ao apêndice.  
**Referência de avaliação:** comentários dos revisores da decisão de outubro, carta anterior `(2).md` e, nos pontos históricos indicados, PDF `(7).pdf`.

## 1. Parecer executivo

**Eu ainda não enviaria este PDF. A estratégia científica da revisão é adequada, mas a integração das correções no manuscrito não está concluída.**

O artigo agora contém os experimentos e as análises que respondem às objeções centrais: HEU/HEU-sel, KOF, cenário marginal, sensibilidade dos limiares e reavaliação do critério de confirmação. O rebaixamento da atualização de valor também foi efetivamente realizado. Não vejo motivo, a partir desta leitura, para abandonar essa estratégia ou exigir uma nova bateria geral de simulações.

O problema é que a versão atual conserva descrições, tabelas e conclusões da versão anterior ao lado das análises novas. Em alguns pontos, a **carta promete uma precisão que o PDF ainda não entrega**. Há também divergências numéricas e uma incompatibilidade entre o procedimento estatístico declarado e pelo menos um valor publicado.

Os principais impedimentos são:

1. **A família confirmatória declarada não corresponde à Tabela 4**, e um valor de *p* não é compatível com o teste exato descrito.
2. **Os resultados do APF divergem entre as Tabelas 5 e 9**, alterando inclusive o sentido da comparação de distância percorrida.
3. **O Algoritmo 1 usa a confirmação como condição de saída do controlador**, enquanto a análise retrospectiva e a carta afirmam que ela é apenas pontuação.
4. **Conclusões sobre persistência, fronteira de detecção e equivalência continuam mais fortes no artigo do que na carta.**
5. **O resumo e a conclusão confundem KOa com o método completo** ao combinar o contraste estatístico e o custo de 31 s.
6. A matriz/proveniência não foi integralmente atualizada para a bateria nova; há erros adicionais na discussão das exclusões, na interpretação geométrica e na comparação com DWA.

Minha recomendação é **uma revisão técnica dirigida antes da ressubmissão**, com reconciliação dos resultados a partir de uma fonte única e sincronização final entre PDF e carta. Isso é diferente de concluir que os experimentos novos são inválidos: não disponho dos dados brutos e do código nesta entrega para fazer essa afirmação.

## 2. O que está efetivamente resolvido

| Pedido | Verificação nesta versão | Avaliação |
|---|---|---|
| R2.1/R3.1: reduzir a centralidade de Bellman/RL | Título e keywords reposicionados; contribuição centrada na arquitetura; formulação no Apêndice C | Atendido no essencial |
| R2.2: propriedade formal ou nota de projeto | Opção pela nota de projeto; sem novo lema nem pretensão de operador de aprendizagem original | Opção adequada |
| R2.3: comparação no mesmo controlador | HEU e HEU-sel descritos e resultados apresentados na Seção V-B/Tabela 6 | Experimento apresentado; interpretação ainda precisa de ajustes |
| R3.2: patrulha com keep-out e sem camada reativa | KOF incluído na Seção V-C | Comparação apresentada; resumo/conclusão precisam identificar corretamente KOa |
| R2.5: sensibilidade à confirmação | Re-scoring em 2,8/3,3/4,0 m e distância física ao alvo apresentados | Análise pertinente; conflita com o Algoritmo 1 |
| R2.6: custo da precedência | CM e varredura do limiar de modalidade apresentados | Pedido substancialmente atendido |
| R2.7: separar média de taxa | Resumo usa 10/10, 4/9 e 9/10 com denominadores | Atendido; há uma frase contraditória no corpo |
| R2.9: natureza da faixa da figura do resíduo | Legenda da Figura 7 declara explicitamente dispersão entre runs, não IC da média | Atendido |
| R3 minor 1: limitar escopo | Eventos idealizados e localização fixa estão no resumo e na conclusão | Atendido |
| R3: literatura de filtros/keep-out | Nova Seção II-D e quatro referências novas presentes | Melhora real; Tabela 1 contém erro sobre DWA |
| R3 minor 3: carta anexada/placeholder | Não encontrei carta de resposta anexada ao PDF nem DOI fictício/history de exemplo | Resolvido no PDF recebido |

**Não considero necessário reintroduzir Q-learning comportamental, QD/QD0, prova de convergência ou experimento em hardware para concluir esta revisão.** Os revisores ofereceram o reposicionamento como alternativa, e essa alternativa foi adotada.

A pequena menção à atualização de valor no fim do resumo já a identifica como nota de projeto. Removê-la pode ajudar a encurtar o resumo, mas não a considero, isoladamente, descumprimento do pedido de rebaixamento.

## 3. Correções necessárias antes do envio

### P1 — Família estatística e valores de p precisam ser reconciliados

**Prioridade: bloqueador de envio.**

**Localização:** PDF pp. 9–11, Tabela 4; Apêndice B, pp. 18–19; `05_results.tex`, linhas 33–76; `07_appendix.tex`, linhas 54–86; carta R2.4.

O texto declara a nova família:

- proposto × HEU, em default;
- proposto × HEU-sel, em default;
- KOa × KOF, em route-hazard.

A carta explicita **cinco desfechos por contraste, totalizando 15 testes**. Entretanto, o artigo encaminha o leitor à Tabela 4 como consolidação da família confirmatória, e essa tabela continua contendo os **sete testes antigos**: E1 × E3, E3 × APF e RHB × RHM. O Apêndice B repete que a Tabela 4 é a família confirmatória.

Isso não é apenas uma referência cruzada errada: coexistem duas definições de família e duas gerações de resultados corrigidos, sem separação suficiente.

**Há também uma incompatibilidade numérica verificável.** O artigo informa KOa com três inspeções em todos os dez runs e KOF com zero em todos os dez. Para esses dois grupos constantes e completamente separados, o procedimento declarado — permutação exata bilateral — fornece:

```text
p_exato = 2 / C(20,10)
        = 0,000010825088224469...

Em uma família Holm com 15 testes:
p_ajustado ≤ 15 × p_exato
           ≈ 0,00016238.
```

O valor divulgado para esse contraste é **p_Holm = 0,0027** (`05_results.tex`, linha 362; carta R3.2). Portanto, **esse valor não pode resultar simultaneamente dos grupos descritos, do teste exato declarado e de Holm sobre 15 testes**. Pode haver uma aproximação assintótica no script ou outra diferença de procedimento, mas não é possível determinar a causa apenas pelo manuscrito.

Isso provavelmente não muda a conclusão de diferença entre zero e três inspeções. Muda, porém, a confiabilidade do relato do método estatístico.

**Correção:**

1. Conferir o ramo do script usado para grupos constantes/com empates.
2. Gerar uma tabela auditável dos 15 testes: contraste, cenário, desfecho, n de cada grupo, procedimento, p bruto e p de Holm.
3. Fazer do conjunto novo a tabela confirmatória efetiva.
4. Se conservar os resultados antigos, identificá-los como análises anteriores/exploratórias, sem apresentá-los como a família nova.
5. Atualizar números e remissões no texto, apêndice e carta a partir dessa mesma saída.
6. Explicitar como foi tratado o “tempo de investigação” do KOF, que não realiza investigações: zero como tempo total é diferente de média por episódio inexistente.

Não recomendo substituir 0,0027 por um número calculado isoladamente à mão. **Reexecute a análise estatística completa da família**, preservando os dados existentes.

**Origem:** a Tabela 4 é herdada — conferi os mesmos sete testes no PDF anterior. A incompatibilidade surge ao conservá-la como confirmatória depois de introduzir a família nova.

### P2 — A tabela consolidada do APF contradiz a tabela geral

**Prioridade: bloqueador de envio.**

**Localização:** Tabela 5, PDF p. 11, versus Tabela 9, p. 15; Figura 5, p. 10; `05_results.tex`, linhas 101–107 e 606–610.

| Métrica do APF em default, n = 9 | Tabela 5 | Tabela 9 |
|---|---:|---:|
| Distância percorrida | 86,4 ± 0,1 m | 88,9 ± 1,1 m |
| Distância mínima ao perigo | 4,81 ± 0,00 m | 4,79 ± 0,06 m |
| Duração da missão | 404 ± 5 s | 404 ± 5 s |

As duas tabelas dizem apresentar **média ± desvio-padrão dos runs válidos**, para a mesma configuração. Não é uma diferença explicável por média versus mediana.

O efeito na interpretação é concreto:

- Pela Tabela 5, E3 percorre 86,6 m e APF 86,4 m: o método percorre ligeiramente **mais**.
- Pela Tabela 9, E3 percorre 86,6 m e APF 88,9 m: o método percorre **menos**, com IC negativo para a diferença.

A Figura 5 mostra o APF praticamente concentrado em 4,81 m de afastamento, visualmente alinhado à Tabela 5, não à dispersão informada na Tabela 9.

**Correção:** identificar o conjunto de runs e a coluna de origem usados em cada exportação; regenerar Tabelas 5 e 9 e Figura 5 do mesmo conjunto. Se forem baterias diferentes, declarar explicitamente a diferença e não lhes dar a mesma identificação experimental. Especificar na Tabela 9 a direção da diferença, aparentemente **proposto − APF**, oposta à convenção da Tabela 4.

**Origem:** os valores da Tabela 5 já estavam no PDF anterior. A divergência entre tabelas é um conflito introduzido ao integrar a tabela consolidada nova. Sem CSVs, não posso dizer qual conjunto está correto.

### P3 — A confirmação é pontuação ou condição de controle?

**Prioridade: bloqueador de envio.**

**Localização:** PDF pp. 6–7, Seção III-C e Algoritmo 1, linhas 13–16 do algoritmo; pp. 15–16, análise de re-scoring; `03_method.tex`, linhas 159–179 e 231–236; `05_results.tex`, linhas 702–708; carta R2.5.

O algoritmo só sai de Investigate quando há:

> sucesso da navegação + dwell concluído + pose dentro da distância de confirmação.

Se a distância não for satisfeita, a execução permanece em Investigate até outro critério de saída. Nesse pseudocódigo, mudar a distância de confirmação **pode mudar a duração do episódio e o retorno à patrulha**.

Já a análise e a carta afirmam que a confirmação é **uma função pura de pontuação, sem realimentação comportamental**, o que fundamenta reavaliar as mesmas trajetórias sem novas simulações.

As duas descrições não podem ser simultaneamente corretas.

**Correção, se a implementação é a que vocês auditaram anteriormente:**

```text
Controlador:
  se navegação concluída com sucesso e dwell concluído:
      encerrar episódio e retomar patrulha
      emitir evento de conclusão com identidade do alvo

Avaliador:
  ao receber o evento de conclusão:
      calcular distância verdadeira ao alvo
      creditar inspeção ou registrar rejeição de confirmação
```

O pseudocódigo final deve refletir os nomes e a ordem reais do código, incluindo aborts, timeout e deferral. Diferenciar “episódio concluído pelo controlador” de “inspeção creditada pelo avaliador”.

**Não peço novos runs por causa dessa divergência documental.** Se o código realmente separa controle e avaliação, basta corrigir algoritmo e descrição. Se o código usar a confirmação para controlar a saída, aí o fundamento do re-scoring precisa ser revisto.

**Origem:** o mesmo pseudocódigo já estava no PDF anterior. É um problema herdado, exposto com mais clareza pela análise retrospectiva nova.

### P4 — Resumo e conclusão combinam resultados de KOa e do método completo

**Prioridade: alta.**

**Localização:** resumo, p. 1; conclusão, p. 17; Seção V-C, p. 12; `access.tex`, linhas 95–99; `06_conclusion.tex`, linhas 15–21.

A comparação nova é **KOa × KOF**. A própria carta R3.2 a identifica corretamente. No entanto:

- o resumo diz “full method’s minimum clearance”;
- a conclusão associa “full method” a p_Holm = 0,42;
- os 31 s e as três inspeções adicionais pertencem à comparação **KOa × KOF**.

Pelos números do artigo:

- KOa: aproximadamente 352,1 s;
- KOF: aproximadamente 320,9 s;
- RHM, método completo: aproximadamente 372 s.

Portanto, o custo de 31 s corresponde a KOa, não ao método completo RHM. Igualdade aproximada das folgas de KOa e RHM não autoriza transferir o teste e o custo temporal de uma comparação para outra.

**Correção proposta, depois de conferir os p-valores:**

> “For the static on-route hazard, KOF and KOa had similar observed minimum clearances (median 1.73 and 1.71 m), with no statistically detectable difference. Relative to KOF, KOa added three inspections at approximately 31 s of additional mission time.”

No resumo, pode abreviar a descrição de KOa como a configuração que mantém a inspeção reativa e desativa a retirada. Restringir a atribuição de segurança ao **cenário estático com perigo na rota**.

Substituir também **“hazard-blind patrol carrying the same detection-triggered keep-out”**: KOF recebe informação do perigo pelo canal de keep-out, portanto não é hazard-blind. “Fixed patrol with detection-triggered keep-out and no reactive supervisor” descreve o que foi implementado.

Evitar “reproduces”/“indistinguishable” como substitutos de equivalência demonstrada. A carta já usa corretamente “no statistically detectable difference”.

### P5 — A atribuição causal e as afirmações de ausência de efeito ainda não estão uniformizadas

**Prioridade: alta.**

**Localização:** Seção V-B, pp. 10–12; conclusão, p. 17; `05_results.tex`, linhas 202–246 e 524–554; `06_conclusion.tex`, linhas 27–38; Figura 5.

A parte final da Seção V-B reconhece que o contraste HEU × HEU-sel troca **a fonte do disparo e o uso da persistência temporal**. Essa ressalva está correta.

Mas a conclusão volta a dizer:

> “so we attribute the difference to the persistence”

e:

> “it is the temporal persistence ... that distinguishes this layer”.

A carta, no panorama inicial, é mais precisa: o contraste **não isola a persistência sozinha**.

Há outras formulações que precisam acompanhar essa precisão:

- V-B descreve o conflito como direção que “the precedence was designed to prevent”, embora HEU também tenha precedência.
- Figura 5: “HEU-sel is indistinguishable ... throughout”.
- V-B: HEU-sel “matches ... on every metric”.
- Cabeçalho da sensibilidade: “Hysteresis: width is immaterial”.
- Cabeçalho do limiar: “The threshold ... is well placed”.

**Correção:** preservar os achados, limitando a interpretação:

> “The measured difference is associated with the trigger-mode change, which jointly changes the decision signal and its temporal persistence. The episode logs are consistent with a persistence-related explanation, but this factor was not isolated experimentally.”

Para HEU-sel:

> “Discrete outcomes were identical in default and conflict; no statistically detectable difference was found in the reported continuous outcomes.”

Para a histerese:

> “No detectable effect of the tested exit-threshold change in the default scenario.”

Para o limiar:

> “Local sensitivity to the hazard eligibility threshold.”

Isso não exige uma quarta variante experimental. **Exige apenas que a conclusão preserve a limitação já aceita na carta.**

### P6 — A afirmação sobre a fronteira de detecção ainda contradiz a resposta R2.8

**Prioridade: alta.**

**Localização:** Seção III-B, pp. 4–5; Seção V-I, p. 16; `03_method.tex`, linhas 76–83; `05_results.tex`, linhas 734–765; carta R2.8.

A carta declara corretamente que os logs não isolam o efeito causal do cruzamento geométrico e não permitem excluir chattering em geral.

O artigo ainda afirma:

- “does not induce chattering”;
- “cannot repeatedly re-trigger”;
- “so the step does not by itself drive the machine”;
- “Neither arises from the boundary”.

A observação de que menos da metade dos onsets é seguida de transição em dois segundos **não demonstra que o degrau não contribui para as transições restantes**. Da mesma forma, associar os intervalos curtos a serviço consecutivo/abort não é isolar causalmente a fronteira.

**Correção:** transportar para o artigo a redação já amadurecida na carta: histerese/commitment são mecanismos destinados a reduzir retriggers; os logs caracterizam onsets e intervalos, mas não isolam o efeito da fronteira. Nos intervalos de 0,2 s, relatar a associação observada.

A abertura de V ainda menciona **“boundary-crossing count”** (`05_results.tex`, linhas 45–46), apesar de a própria análise reconhecer que não mediu os cruzamentos. Trocar por “logged-onset and FSM-transition analysis”.

Por fim, a carta remete à **Eq. (3)** para o perfil de intensidade, mas no PDF atual ele é a **Eq. (2)**.

### P7 — A bateria nova precisa entrar na matriz e na proveniência

**Prioridade: alta para reprodutibilidade.**

**Localização:** Seção IV-C/D, pp. 7–9; Tabela 2, p. 8; Apêndice A/Tabela 11, p. 18; ameaças à validade, pp. 16–17; carta, “New evaluation”.

A carta apresenta **13 configurações novas, 130 tentativas, 127 válidas**. As exclusões novas aparecem no fim do artigo. Porém:

- Tabela 2 ainda lista apenas as 16 configurações antigas.
- A descrição da matriz continua organizada pela varredura de η.
- A proveniência descreve o manifesto dos **160 CSVs antigos**.
- O Apêndice A diz listar eventos de “all five scenarios”, mas não inclui CM.
- Não há uma correspondência compacta entre cada configuração nova, parâmetro alterado, cenário, referência reutilizada e n válido.

Os resultados novos estão dispersos no corpo, mas isso não substitui uma matriz que permita reconstruir a bateria. Também não está claro, só pela matriz atual, como se chega exatamente às 13 configurações.

**Correção:** acrescentar um painel/tabela para a nova bateria, com:

| Campo mínimo | Finalidade |
|---|---|
| ID e cenário | Reconhecer cada configuração sem inferência |
| Trigger e seleção | Diferenciar HEU, HEU-sel e proposto |
| Retirada e keep-out | Distinguir KOa/KOF/RHM |
| Limiar de modalidade e par de histerese | Reproduzir sensibilidades |
| Tentativas/válidas | Explicar 130/127 e cada exclusão |
| Nova ou reutilizada; versão/manifesto | Fixar proveniência |

Acrescentar a geometria/intensidades de CM e a definição do horizonte de 400 s do alvo prioritário, distinguindo-o do timeout de 600 s da missão.

**Sobre a regressão da carta:** dois runs de default são uma verificação limitada. A frase “which are the ones the reused data supply” pode sugerir que todos os dados reutilizados são default, embora também sejam utilizados conflict, adverse e outros. Dizer explicitamente que a regressão empírica cobre default; a reutilização dos demais cenários deve se apoiar no escopo real das alterações e na identificação dos artefatos.

Não estou afirmando que os dados novos não foram publicados. **Estou apontando que a seção de reprodutibilidade enviada ainda descreve essencialmente a bateria anterior.** Não auditei o repositório nesta rodada.

### P8 — A discussão das exclusões usa RHM e APF como se fossem o mesmo contraste

**Prioridade: alta.**

**Localização:** PDF p. 17; `05_results.tex`, linhas 805–815; carta R3 minor 2, linhas 481–484.

A frase diz que retirar runs imóveis eleva “the proposed layer and APF” de **2,7 para 3,0** em ambos, deixando a diferença inalterada.

Mas, de acordo com os próprios n:

- **E3, default:** dez válidos em dez; média 3,0 com ou sem exclusões.
- **APF, default:** nove válidos em dez; média por tentativa 2,7, condicional 3,0.
- **RHM, route-hazard:** nove válidos em dez; média por tentativa 2,7, condicional 3,0.

O grupo proposto que sobe de 2,7 para 3,0 é **RHM**, em outro cenário. Na comparação direta **E3 × APF em default**, a exclusão altera a diferença das médias de contagem por tentativa: passa de 0,3 para zero.

Isso não invalida a análise condicional. Invalida a justificativa de que a exclusão não altera esse contraste.

**Correção:** nomear os grupos e separar as duas perspectivas:

> “In default, E3 averages 3.0 inspections per attempt and APF 2.7; conditional on movement, both average 3.0. RHM, evaluated in route-hazard, also changes from 2.7 per attempt to 3.0 per valid run.”

A mesma correção deve ir para a carta. Não comparar 2,7 de RHM com 2,7 de APF como prova de ausência de efeito da seleção no contraste principal.

## 4. Correções técnicas adicionais

### T1 — A interpretação geométrica de 0,5 m está errada

**Localização:** PDF p. 8; `04_experimental_setup.tex`, linhas 155–164.

O texto afirma que, com raio do robô de 0,25 m, a região de 0,5 m corresponde ao corpo alcançar o centro do perigo.

Para um perigo representado por um ponto, a distância entre a borda do robô e esse ponto é:

```text
0,50 − 0,25 = 0,25 m.
```

Logo, a interpretação não decorre da geometria declarada. Contato entre dois discos a 0,5 m seria compatível com dois raios de 0,25 m, mas esse segundo raio físico precisaria ser definido — não se confunde com o disco de keep-out de 1,2 m.

**Correção:** manter 0,5 m como região operacional definida para pontuação; retirar a frase sobre o corpo alcançar o centro. A interpretação de 2 m como 1,75 m da borda ao **centro** é coerente, mas não significa afastamento da superfície de um equipamento com extensão finita.

Não é necessário mudar os limiares ou repetir os testes para corrigir essa descrição.

### T2 — A Tabela 1 atribui a DWA uma operação de APF

**Localização:** PDF p. 5; `02_related_work.tex`, linhas 155–160.

A linha conjunta **“Classical APF / DWA”** caracteriza ambos como “vector sum”, em que atração forte supera repulsão, e segurança como termo de força.

Essa não é uma descrição correta da DWA clássica. O trabalho original busca comandos no espaço de velocidades dinamicamente alcançáveis, restringindo-os a trajetórias admissíveis nas quais o robô consegue parar, e só depois avalia uma função objetivo.

**Correção:** separar APF de DWA ou retirar DWA dessa linha. Não é necessário criar uma garantia moderna de invariância para DWA; basta não lhe atribuir soma de forças.

Fonte primária conferida: Fox, Burgard e Thrun, *The Dynamic Window Approach to Collision Avoidance*, resumo disponibilizado no laboratório do autor:  
https://rse-lab.cs.washington.edu/abstracts/colli-ieee.abstract.html

Este erro merece atenção porque a nova tabela existe justamente para responder à cobrança de uma comparação crítica e tecnicamente fiel das premissas.

### T3 — Φ ainda é chamado de função apenas da observação/estado atual

**Localização:** PDF p. 4 e Apêndice C, pp. 18–19; `03_method.tex`, linhas 53–57; `07_appendix.tex`, linhas 145–172.

O método afirma que Φ depende somente das observações atuais. Entretanto, as equações seguintes introduzem acumuladores com memória, e CM depende justamente de sua persistência.

No apêndice, o texto diz que Φ(s) é função do estado sozinho, mas depois reconhece que o estado discretizado perde o sinal e a memória. Dois contextos com o mesmo estado discretizado podem produzir Φ diferentes. Assim, a notação não é rigorosamente uma função unívoca desse estado.

A carta R2.10 oferece a formulação melhor:

> observações e memórias → Φₜ → estado discretizado → atualização de Q; Q não retorna a Φ.

**Correção:** usar Φₜ na atualização e explicar o estado reduzido como índice da tabela. Se mantiver Φ(s), declarar explicitamente o abuso de notação. Substituir “cannot support an arbitration policy” por “cannot distinguish all situations treated differently by the proposed arbitration rule”.

Não é preciso redesenhar a representação ou implementar uma política aprendida. Basta não reivindicar para o estado uma informação que ele não contém.

### T4 — A frase “all three configurations inspect all five” é falsa para a distribuição descrita

**Localização:** PDF p. 11; `05_results.tex`, linhas 214–216; carta R2.3.

O artigo afirma que os três métodos inspecionam todas as cinco anomalias em adverse. A carta informa valores em **{4,5}**, e o próprio artigo informa E5 com **9/10** runs completos.

**Correção:** “All three configurations had a median of five inspected anomalies, with per-run counts ranging from four to five.”

A mediana cinco da Tabela 6 pode permanecer. Não a converter em conclusão de 100% de completude.

### T5 — A descrição do hand-off precisa explicar a renovação do canal em CM

**Localização:** Seção III-C, p. 6, versus Seção V-F, p. 14.

O método diz que, ao entregar o perigo ao keep-out, seu sinal reativo é suprimido. Já CM descreve um retreat inicial seguido de reobservações que elevam novamente a magnitude do canal.

Isso **pode** ser compatível com a implementação, dependendo do que é suprimido — a publicação, o disparo, a seleção ou a alimentação do acumulador —, mas o texto atual não permite entender a distinção.

**Correção:** dizer exatamente o que o hand-off bloqueia, o que permanece armazenado e se novas observações ainda alimentam h. Se CM muda alguma configuração de hand-off, incluí-la na matriz.

Trato este ponto como **ambiguidade a esclarecer**, não como erro de código demonstrado.

## 5. Figuras, referências e apresentação

### Figuras

- **Figuras 1 e 2:** caixas da atualização de valor foram removidas; a arquitetura aparece como deliberativa–reativa e baseada em limiares. A promessa principal de atualização visual foi cumprida.
- **Figura 3:** contém os estados, a prioridade da repulsão e a nota de refractory. Deve acompanhar a separação entre controle e crédito de inspeção corrigida no Algoritmo 1.
- **Figura 5:** agora compara grupos do mesmo cenário default e inclui HEU/HEU-sel. Isso resolve a mistura de cenários. Falta reconciliar os dados do APF e retirar a linguagem de equivalência da legenda.
- **Figura 6:** a legenda informa que as trajetórias vêm de uma sessão ilustrativa separada. A ressalva de proveniência está clara.
- **Figura 7:** apresenta as quatro curvas de η, com bandas identificadas como dispersão entre runs. A atualização é visível e atende R2.9.

Na Figura 7, “flat throughout at ≈0.08” é excessivo: há transientes e queda final para ≈0,02, reconhecidos na própria legenda. Usar “approximately flat between transients” ou descrever o intervalo efetivo. O parágrafo que diz que a figura agrega “all valid runs of E3” deve esclarecer que está descrevendo **a curva E3 dentro da figura com quatro grupos**.

### Referências

As quatro referências novas aparecem no PDF com os autores e os dados centrais anteriormente conferidos:

- Ames et al., ECC 2019, pp. 3420–3431;
- Wabersich e Zeilinger, *Automatica* 129, 109597, 2021;
- Macenski et al., *Science Robotics* 7(66), eabm6074, 2022;
- Macenski, Moore, Lu, Merzlyakov e Ferguson, *Robotics and Autonomous Systems* 168, 104493, 2023.

Em particular, a autoria do survey de 2023 foi corrigida. Os DOI não aparecem na bibliografia renderizada; isso, por si só, não demonstra ausência no .bib. Não refiz nesta rodada uma auditoria externa integral das 25 referências.

A referência existir não garante que a caracterização feita no texto seja correta: é por isso que a linha APF/DWA precisa ser corrigida.

### Ajustes menores e localizados

| Local | Problema | Correção |
|---|---|---|
| Seção IV-C, p. 8 | “group comparisons use distribution-free” é interrompido por um parágrafo inteiro; “tests ...” reaparece depois | Reunir a frase estatística e colocar a calibração geométrica em parágrafo separado |
| Tabela 3 | Ganhos/limiares/refractory do APF estão no texto, mas não todos na tabela mencionada pela carta | Acrescentar as linhas ou tornar a remissão da carta mais precisa |
| Tabela 6 | Legenda diz que n está no cabeçalho; n está na nota inferior | Corrigir a legenda |
| Tabela 5 | Legenda informa n para E1–E5, omitindo E0 | Incluir E0 |
| Métrica radial de TTC | d/ḋ aparece sem convenção clara do sinal | Definir velocidade de fechamento positiva, ou explicitar −d/ḋ quando ḋ<0 |
| Seção V-I | “stopped 2.9–3.6 m away” é seguido de faixa completa 1,83–3,56 m | Identificar se a primeira faixa é um subconjunto ou usar a faixa completa |
| Resumo | Aproximadamente 370–380 palavras, com muitos resultados e ressalvas | Encurtar após corrigir as atribuições; evitar transformar o resumo em inventário da revisão |
| Texto principal | Expressões como “which we quantify honestly”, “the honest reading”, “new here” | Preferir descrição direta dos resultados; retirar comentários sobre a honestidade da apresentação |
| R2.8 da carta | Remissão à Eq. (3) | Atualizar para Eq. (2) |
| Fechamento da carta | “responses below” | “responses above” |

Não encontrei referências LaTeX internas indefinidas entre os arquivos fornecidos. A inspeção das 21 páginas não revelou tabelas cortadas ou sobreposições grosseiras. As figuras conceituais têm rótulos pequenos, mas os problemas mais relevantes desta rodada são de consistência científica.

## 6. Parecer específico sobre a carta

**O tom continua adequado:** respeitoso, direto, receptivo às críticas e sem confrontação com os revisores. Não recomendo reescrevê-la integralmente.

As alterações desta versão são principalmente localizações mais específicas e a passagem das figuras de “serão atualizadas” para “foram atualizadas”. As remissões a Seção V-B, Tabela 6, Apêndice C e Figura 7 correspondem ao PDF recebido.

Contudo, a aprovação anterior do tom e da estratégia da carta **não equivale a certificar que o manuscrito implementou cada ação anunciada**. Agora, com PDF e fontes juntos, apareceram divergências que não poderiam ser resolvidas apenas lendo a carta.

Antes de enviar, ajustar a carta nos seguintes pontos:

1. **R2.4:** sincronizar a família de 15 testes com a tabela efetiva e os valores recalculados.
2. **R2.5:** fazer a implementação documental do algoritmo corresponder à pontuação sem feedback.
3. **R2.8/R2.10:** levar ao manuscrito as ressalvas corretas que a carta já contém.
4. **R3.2:** manter KOa como referência do contraste com KOF e corrigir o resumo/conclusão.
5. **R3 minor 2:** corrigir a explicação de 2,7 → 3,0, distinguindo RHM de E3.
6. **New evaluation:** descrever sem ambiguidade o alcance da regressão em default e a reutilização dos demais cenários.
7. **R3 minor 3:** adequar a descrição dos placeholders ao PDF realmente entregue.

Neste último ponto, **não identifiquei “Digital Object Identifier” vazio nem “VOLUME 11, 2023” no PDF atual**, embora a carta diga que permanecem. Evitar uma defesa de elementos que não aparecem no arquivo. Uma formulação simples basta:

> “The submitted PDF contains no specimen publication dates or DOI, and the response letter is supplied separately. We will verify the merged review proof before submission.”

Também evitar “not under author control” como afirmação absoluta sobre a classe LaTeX. O que importa ao revisor é o arquivo final, não uma discussão sobre a editabilidade da classe.

O material de equivalência e a figura do resíduo foram deslocados, mas E0/E2/E4 e o resíduo ainda ocupam a matriz e a Tabela 5 do corpo. A carta deve distinguir **discussão/testes deslocados** de **todas as linhas experimentais deslocadas**. Não considero obrigatório retirar do corpo as análises dinâmica e de ruído, cuja permanência foi justificada.

## 7. Matriz final de atendimento aos revisores

| Comentário | Situação nesta entrega | Pendência principal |
|---|---|---|
| R1 | Atendido | Nenhuma nova ação específica |
| R2.1 | Substancialmente atendido | Manter rebaixamento e encurtar redundâncias |
| R2.2 | Atendido na estratégia | Ajustar a notação/descrição da nota de projeto |
| R2.3 | Experimentos apresentados; atendimento parcial no relato | Limitar atribuição causal e linguagem de equivalência |
| R2.4 | **Ainda não atendido de forma consistente** | Família, tabela e p-valores |
| R2.5 | **Análise presente, mas com contradição metodológica** | Separar controlador e avaliador no algoritmo |
| R2.6 | Substancialmente atendido | Documentar CM e limitar conclusões da sensibilidade |
| R2.7 | Atendido no resumo | Corrigir “all five” no corpo |
| R2.8 | Parcial | Remover as exclusões causais que os logs não demonstram |
| R2.9 | Atendido | Pequeno ajuste na descrição de η=0 |
| R2.10 | Parcial | Φₜ, memória e estado reduzido coerentes com a carta |
| R2, pergunta adicional 3 | Melhorou substancialmente | Corrigir APF/DWA e completar premissas/proveniência |
| R3.1 | Substancialmente atendido | Evitar reintroduzir centralidade do update pelo excesso de espaço |
| R3.2 | Parcial | KOa versus RHM; geometria; escopo estático |
| R3.3 | **Tabela presente, mas numericamente inconsistente** | Reconciliar APF, intervalos e Figura 5 |
| R3 minor 1 | Atendido | Preservar as qualificações |
| R3 minor 2 | Parcial | Corrigir efeito das exclusões e completar matriz nova |
| R3 minor 3 | PDF sem carta anexada/placeholder identificado; redução parcial | Sincronizar carta e racionalizar texto |
| R3, pergunta adicional 4 | Substancialmente atendido | Não há necessidade automática de acrescentar mais referências |

## 8. Esses problemas são antigos ou foram causados pelas alterações?

A resposta não é única para todos os itens.

| Natureza | Exemplos | Interpretação |
|---|---|---|
| **Problema herdado, confirmado no PDF anterior** | Confirmação no Algoritmo 1; tabela estatística antiga | A revisão nova expôs uma inconsistência que já existia |
| **Conflito de integração** | Nova família declarada × Tabela 4 antiga; Tabela 9 × Tabela 5; re-scoring puro × algoritmo antigo | Trechos antigos e novos não foram reconciliados |
| **Erro em material acrescentado/reformulado** | APF/DWA na tabela crítica; explicação geométrica de 0,5 m; generalização da persistência; equivalência implícita de KOF | Exige corrigir o texto novo, sem abandonar a análise nova |
| **Erro compartilhado pela carta e pelo manuscrito** | 2,7 → 3,0 de “proposto e APF” sem distinguir cenários; p de KOa × KOF | A revisão só da carta não bastava; o confronto com grupos/método revelou o problema |
| **Não verificável apenas com os arquivos atuais** | Origem exata dos números APF; mecanismo preciso do hand-off; validade externa dos CSVs | Exige conferir os artefatos de análise, sem presumir fabricação ou erro experimental |

Portanto, **não considero que as correções tenham estragado o trabalho**. Elas acrescentaram evidência útil. O principal problema é a coexistência de versões diferentes da explicação dentro do mesmo artigo.

## 9. Caminho mínimo para fechar a revisão

1. **Fixar os números:** conferir APF, exportar os 15 testes com o procedimento efetivamente utilizado e atualizar todas as ocorrências.
2. **Fixar a especificação:** separar controle/avaliação, esclarecer hand-off e usar Φₜ com memória.
3. **Fixar as atribuições:** KOa versus RHM; efeito do trigger versus persistência isolada; observação versus equivalência; associação versus causalidade na fronteira.
4. **Fixar a rastreabilidade:** matriz da bateria nova, CM, n válidos, exclusões e versões dos dados.
5. **Compilar e sincronizar a carta:** remissões, figuras, tabelas e afirmações sobre o PDF final.

**Não recomendo novos experimentos automaticamente.** As pendências identificadas pedem sobretudo correção documental e reexecução das análises sobre os dados existentes. Novos runs só seriam necessários se a conferência do código revelar que algum pressuposto experimental central — como a ausência de feedback da confirmação — não corresponde à execução real.

## 10. Limites deste parecer

Li integralmente as fontes fornecidas e a carta, confrontei os pedidos dos revisores e inspecionei o PDF, incluindo as figuras em resolução maior. Comparei os trechos históricos indicados com a versão anterior.

Não compilei o projeto Overleaf completo, pois os assets de figuras e a classe não foram fornecidos como um projeto completo nesta entrega. Não reexecutei simulações, não recalculei todas as estatísticas a partir de CSVs e não auditei o repositório. A conta de permutação apresentada em P1 é uma verificação matemática a partir das contagens constantes declaradas no próprio artigo.

Este é um parecer técnico preparatório, não uma decisão editorial oficial. Minha conclusão é específica: **a estratégia de resposta é defensável e grande parte dos pedidos foi atendida, mas este PDF ainda contém inconsistências verificáveis que devem ser corrigidas antes da ressubmissão.**

