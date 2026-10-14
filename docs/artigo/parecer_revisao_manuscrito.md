# Parecer Técnico — Manuscrito Access-2026-33687 (versão revisada)

> **Nota de atualização:** este documento cobre duas rodadas de análise. A Parte 1 (abaixo) avaliou a primeira versão revisada recebida. A **Parte 2**, ao final do documento, reavalia a versão mais recente — enviada após as correções adicionais — e atualiza os vereditos que mudaram. Leia a Parte 2 para o estado mais atual; a Parte 1 é mantida como registro histórico do que foi pedido e por quê.

**Papel assumido:** Associate Editor / Revisor sênior, IEEE Access
**Manuscrito original:** *Affective Attraction–Repulsion Value Modulation for Reactive Inspection Navigation in Electrical Substations* (Neto, Cardoso, Carrijo)
**Manuscrito revisado:** *A Two-Layer Deliberative–Reactive Architecture with an Affective Attraction–Repulsion Layer for Autonomous Substation Inspection* (Neto, Cardoso)

---

## 1. Resumo executivo

A revisão é **substancial e, na maior parte, bem direcionada**. Os autores não fizeram uma revisão cosmética: mudaram o título, reformularam a narrativa da contribuição, rodaram uma bateria de experimentos inteiramente nova (E0, APF, RHM/RHB, N1/N2), refizeram a análise estatística e reescreveram passagens do abstract/conclusão que os revisores tinham marcado como incorretas ou exageradas. Isso é o que se espera de uma resposta séria a uma rejeição binária do IEEE Access.

Dito isso, como revisor "chato", meu trabalho é justamente não aceitar a narrativa dos autores de que "está tudo resolvido". Encontrei **três categorias de problema**:

1. **Itens genuinamente resolvidos** — a maioria dos pontos "matadores" (R2 #1, R4 #1, R4 #2, R2/R3 sobre segurança, R1/R2/R3 sobre convergência) foi endereçada de forma honesta, inclusive contra o interesse narrativo dos próprios autores (admitir que η não afeta o comportamento executado é uma concessão rara e correta).
2. **Itens parcialmente resolvidos** — robustez (falta raio de detecção, erro de localização, persistência de evento), custo de missão (sem métrica de utilidade), tabela estatística completa por par de configuração.
3. **Um problema conceitual novo/latente que nenhum revisor pegou explicitamente, mas que decorre diretamente da correção que os autores fizeram** — ver Seção 4. Ele é sério o suficiente para eu, como revisor, reabrir a discussão sobre arbitragem atração×repulsão.

**Recomendação (se eu fosse o Associate Editor):** *Minor Revision* — não mais rejeição, mas ainda não aceitação direta. Os pontos da Seção 4 e 5 abaixo devem ser respondidos na carta de resposta antes da aceitação final, já que o IEEE Access só permite uma rodada de resubmissão.

---

## 2. Quadro-síntese (comentário → status na v2)

| # | Origem | Comentário-chave | Status | Onde foi tratado na v2 |
|---|--------|-------------------|--------|--------------------------|
| 1 | R1-1, R2-4, R3-3 | Não reivindicar garantias de convergência do Q-learning padrão | ✅ Resolvido | Subseção "Convergence" (Seç. III-B): "we therefore make no formal convergence claim" |
| 2 | R1-2, R2-7 | Testes não paramétricos, effect sizes, CIs, correção de múltiplas comparações | ⚠️ Parcial | Mann–Whitney, Cliff's δ, Hedges' g, bootstrap CI, Holm — mas só reportados **seletivamente no texto corrido**, não em tabela sistemática por par |
| 3 | R1-3, R2-6, R3-2 | Robustez ambiental (ruído, perigo na rota, incerteza) | ⚠️ Parcial | N1/N2 (ruído de percepção), RHM/RHB (perigo na rota); **faltam** raio de detecção, persistência, erro de localização |
| 4 | R1-4, R2-4, R3-3 | TD-error de uma única run não prova estabilidade | ✅ Resolvido | Fig. 7 agrega resíduo completo `\|αδ+ηΦ\|` em todas as runs válidas de E3, com banda de 95% |
| 5 | R1-5, R2-10, R4-4 | Revisão bibliográfica rasa (13-14 refs) | ✅ Parcial→Bom | 20 referências, Tabela 1 de posicionamento contra APF/DWA, RL-tuned APF, DRL+ACO, informative path planning |
| 6 | R1-6 | Custo de missão sem métrica de utilidade real | ⚠️ Não resolvido | Discussão qualitativa apenas; nenhuma métrica tipo "inspeção por metro adicional" foi introduzida |
| 7 | R1-7, R2-9, R4-1/3 | Abstract mais forte do que os dados sustentam | ✅ Resolvido | Abstract agora distingue FSM vs. atualização de Bellman e qualifica "empirically stable" |
| 8 | **R2-1, R4-1** | Contribuição de Bellman não é demonstrada — Q não influencia ação executada | ✅ **Resolvido com honestidade exemplar** | Ablação E0 (η=0) reproduz E2-E4 idênticos; nova subseção "What the value table does, and does not, control" responde (a)-(e) do R2 ponto a ponto |
| 9 | R2-2 | Distinção com reward shaping mal fundamentada; dupla contagem de Φ na recompensa | ✅ Resolvido | Recompensa agora é `r = r_prog` apenas; Eq. (6) formaliza a equivalência sob taxa de aprendizado fixa; derivação explícita vs. Ng et al. |
| 10 | R2-3 | η sweep é tautológico dado que FSM usa Φ bruto | ✅ Resolvido (via enquadramento) | Texto agora chama o sweep de "numerical analysis of the value table rather than a behavioral one" |
| 11 | R2-5, R4-2 | Baseline E1 "ganha por construção"; faltam baselines justos | ⚠️ Parcial | APF adicionado (E2-5c-like); E0 cobre "FSM sem Q"; **faltam** reward-shaping convencional e método de RL aprendido recente |
| 12 | R2-6, R3-2, R4-3 | Alegação de segurança fraca (hazard ao lado da rota, não sobre ela) | ✅ Resolvido | Cenário RHM/RHB com hazard *sobre* a perna de patrulha; Tabela 5 com colisões, TTC, tempo abaixo do clearance |
| 13 | R2-8 | Definição de "inspecionado" ambígua (commit vs. dwell vs. timeout) | ✅ Resolvido | Seç. III-C define commit/inspected/timeout como outcomes distintos e reportados separadamente |
| 14 | R2-9 | Frases factualmente incorretas (E2 = 2.7±0.9 mas abstract diz "todas") | ✅ Resolvido (pela própria arquitetura) | Como execução não depende mais de η, E0-E4 agora dão 3.0±0.0 de forma consistente |
| 15 | R2-min-1 | Justificar degrau de Φ em d=R / chattering | ✅ Resolvido | Parágrafo dedicado sobre histerese e não-rechattering |
| 16 | R2-min-3 | Notação Φ(s,a) inconsistente com o cálculo (não depende de a) | ✅ Resolvido | Notação corrigida para Φ(s) em todo o texto |
| 17 | R2-min-4 | Por que TD-error do baseline é zero? | ✅ Resolvido | Legenda da Tabela 4 explicita que é zero quando a atualização de valor está inativa |
| 18 | R2-min-5 | Sementes, hardware, commit hash, versão do simulador | ❌ Não visto | Não localizei essa informação no corpo do PDF revisado |
| 19 | R2-min-6 | Ordem errada de figuras no Acknowledgment | ✅ Resolvido | Agora consta "Figs. 4, 5, 6, and 7" em ordem |
| 20 | R4-3 (parte 2) | Cenário adverso não testa conflito atração×repulsão real (hazard longe dos clusters) | ❌ **Não resolvido** | Hazard permanece em (2,−13) em E5, sem sobreposição com os clusters — ver Seção 4 |

---

## 3. Análise detalhada por revisor

### Revisor 1

- **#1 (teoria de convergência):** resolvido — o texto agora é defensivo e correto ("we make no formal convergence claim... left as future theoretical work").
- **#2 (estatística):** o *aparato* está lá (Mann-Whitney, Cliff's δ, Hedges' g, bootstrap 95% CI, Holm), mas **não vi uma tabela consolidada** com todos os pares comparados, seus p-valores exatos e ICs — o texto reporta números isolados ("Cliff's δ=1, p<0.001") apenas para as comparações que sustentam a narrativa dos autores (inspeção, clearance no RHM). Um revisor estatístico vai pedir a tabela completa (todas as métricas × todos os pares relevantes: E1 vs E0, E1 vs E3, E3 vs APF, E3 vs E5, RHB vs RHM), não uma amostra.
- **#3 (robustez):** parcialmente atendido. Faltam explicitamente: variação do raio de detecção `R`, persistência do evento, erro de localização (os autores dizem explicitamente que a odometria é mantida exata — "held fixed" — o que é o oposto de testar erro de localização) e variação de geometria do mapa. Isso deveria ser reconhecido nas limitações com mais precisão do que está.
- **#4 (TD-error de uma run só):** resolvido — Fig. 7 agora agrega todas as runs de E3.
- **#5 (revisão bibliográfica):** melhor, mas ainda enxuta para um periódico (20 refs). Aceitável, mas não impressionante.
- **#6 (custo/eficiência):** **não resolvido**. Nenhuma métrica de "utilidade por metro" ou "inspeção por segundo adicional" foi introduzida; é só narrativa qualitativa comparando durações.
- **#7 (abstract):** resolvido, e bem.

### Revisor 2 (o mais rigoroso dos quatro — 10 comentários principais)

Este foi o revisor que mais "doeu", e é onde a revisão mais evoluiu.

- **#1 (Q não influencia a ação):** **Este é o ponto mais importante de todo o processo, e os autores o resolveram com integridade** — em vez de tentar mascarar o problema, adicionaram a ablação E0 e reescreveram a contribuição para admitir abertamente que, na instância tabular avaliada, `η` não altera nenhuma ação executada. Isso é exatamente o que R2 pediu ("At minimum, an ablation... is required"). Nota-se coragem editorial aqui: a alternativa mais fácil seria "esconder" isso, e não o fizeram.
- **#2 (reward shaping / dupla contagem):** resolvido de forma elegante — reward agora é só progresso, Φ entra uma única vez, e há uma derivação formal (Eq. 6) relacionando com Ng et al. [8], com honestidade sobre onde a formulação *não* tem as garantias do potential-based shaping.
- **#3 (η sweep tautológico):** resolvido via opção (b) sugerida pelo próprio revisor — o sweep é agora apresentado como análise numérica da tabela de valores, não como robustez comportamental.
- **#4 (estabilidade):** resolvido — resíduo completo agregado, linguagem "empirically stable" em vez de "convergent".
- **#5 (baselines mais fortes):** parcial. Adicionaram (b) APF. Não adicionaram (c) Q-learning com recompensa aumentada convencional nem (d) um método de aprendizado recente. Isso é o "buraco" mais defensável de deixar para trabalho futuro, mas um revisor rigoroso vai cobrar pelo menos (c), já que é a comparação mais direta para a alegação central (Φ como termo de valor vs. Φ como recompensa).
- **#6 (segurança):** resolvido de forma exemplar com RHM/RHB.
- **#7 (rigor estatístico):** parcial, como já discutido no item R1-2 acima. Falta também explicitamente o item (f) — sensibilidade com/sem as runs que não completam. A v2 trocou o fenômeno (agora são "falhas de inicialização", 7/110, não mais "timeout aos 600s" como na v1) sem deixar claro se o fenômeno de timeout da v1 ainda ocorre ou desapareceu, e sem relatar explicitamente o resultado com e sem essas 7 runs excluídas (apenas afirma que as estatísticas usam runs válidas).
- **#8 (definições de evento/inspeção):** resolvido para commit/inspected/timeout. **Não resolvido** para a segunda parte do pedido: "explain tie handling... and how hazard priority in the FSM interacts with magnitude-based event selection" — ver Seção 4, é o ponto mais técnico deste parecer.
- **#9 (afirmações a corrigir):** todas as três frases problemáticas apontadas por R2 foram corrigidas (E2 agora = 3.0±0.0; "no significant increase" virou "modest and bounded increase (≈14%)"; "detection scales" foi explicitamente moderado).
- **#10 (bibliografia):** melhorou de 13 para 20 referências.
- **Menores:** 5 de 6 resolvidos; falta a #5 (sementes/hardware/commit hash/versão do simulador) — ver Seção 5.

### Revisor 3

Comentário mais curto, mas os 3 pontos foram endereçados: (1) benefício da modulação de Bellman esclarecido — inclusive, a resposta é "nenhum, na versão tabular" — resposta correta, ainda que desconfortável para os autores; (2) hazard sobre a rota agora testado (RHM); (3) linguagem "empirical stability" em vez de "convergence" adotada.

### Revisor 4

- **#1 (idêntico ao R2-1):** resolvido, ver acima. O revisor pediu explicitamente para "title, abstract and second contribution bullet" serem ajustados **se a ablação reproduzisse E3** — e foi exatamente isso que aconteceu (E0 = E2 = E3 = E4 em todas as métricas comportamentais) e o título mudou de fato.
- **#2 (baseline E1 ganha por construção):** parcialmente resolvido pela adição do APF, que é "a reactive scheme of similar simplicity" tal como sugerido. O E1 continua existindo como comparação (correto — ele ainda serve para mostrar o valor da camada reativa como um todo), mas agora não é mais a *única* comparação, o que atenua a crítica.
- **#3 (alegação de segurança forte demais):** resolvido via RHM/RHB. **Porém**, a segunda metade deste comentário — sobre o cenário adverso nunca exercitar conflito atração×repulsão porque o hazard permanece longe dos clusters — **não foi resolvida**. Ver Seção 4.
- **Pontos menores:** degrau em d=R justificado; testes com variância zero agora relatados com Cliff's δ e permutação exata em vez de apenas p de Welch (ainda que não sistematicamente tabulados — ver acima); ordem das figuras no Acknowledgment corrigida.

---

## 4. Problema conceitual que persiste (e que eu, como revisor "chato", reabriria)

Este ponto conecta R2-8 (arbitragem/prioridade) e R4-3 (segunda metade) e **não foi fechado pela revisão**, apesar de a v2 ter corrigido quase tudo ao redor dele.

A Eq. (4) seleciona Φ por **magnitude do sinal**, preservando o sinal do evento vencedor:

> Φ ← arg max_{|·|} { Φ, {w_m·i_m : i_m ≥ θ_m} }

Ou seja: se, num dado instante, um evento de atração (ex.: hotspot térmico) tiver `|w_thermal·i_thermal|` maior do que `|w_hazard·i_hazard|` de um perigo simultaneamente dentro do raio de detecção, **Φ assume o valor positivo do evento de atração**, e o hazard simplesmente não aparece no campo agregado.

O Algoritmo 1, por sua vez, é descrito em prosa como implementando "safety before inspection" — repulsão tem prioridade sobre atração. Mas a prioridade codificada no algoritmo (`if Φ ≤ −θ_in ... else if Φ ≥ θ_in ...`) só pode dar prioridade à repulsão **se Φ já for negativo**, e Φ só é negativo quando o hazard *venceu* a disputa de magnitude na Eq. (4). Em outras palavras: **a "prioridade de segurança" está condicionada a o hazard já ter vencido a arbitragem por magnitude** — não existe, na formulação atual, um mecanismo que garanta que um hazard de menor intensidade percebida, mas presente, sempre dispare o modo Avoid mesmo na presença simultânea de um evento de atração mais saliente.

Isso é exatamente o que R2 pediu para ser esclarecido ("how hazard priority in the FSM interacts with magnitude-based event selection") e a v2 não trouxe uma resposta textual a essa pergunta específica — nem uma prova de que essa situação (hazard fraco + atração forte, simultâneos) foi de fato testada.

E o cenário que poderia ter testado exatamente isso — o cenário adverso E5 — **mantém o hazard fixo em (2, −13)**, geograficamente isolado dos clusters de anomalias (perto do transformador e do disjuntor). O cenário RHM também não cria sobreposição temporal entre hazard e anomalia (o hazard está na primeira perna da patrulha; as anomalias, nas pernas seguintes). **Logo, em nenhum dos 11 experimentos da matriz revisada existe um instante em que um evento de atração e um evento de repulsão estejam simultaneamente dentro do raio de detecção.** A palavra "arbitrating" usada no texto para E5 ("arbitrating between clustered events") descreve arbitragem *entre múltiplos eventos de atração*, não arbitragem atração-vs-repulsão — o que é uma distinção que o texto atual não deixa clara e que pode induzir o leitor a pensar que o caso de conflito de sinais foi testado, quando não foi.

**O que eu pediria na resposta aos revisores:**
1. Uma frase explícita esclarecendo que, na formulação atual, a prioridade de segurança é *implícita à magnitude* do sinal, não uma regra independente — ou, alternativamente, uma correção da Eq. (4)/Algoritmo 1 para que a checagem de repulsão preceda a seleção por magnitude quando ambos os tipos de evento estão simultaneamente acima do limiar.
2. Um cenário (mesmo que pequeno, n=10) com um hazard de baixa intensidade e uma anomalia de alta intensidade dentro do mesmo raio simultaneamente, mostrando que o robô ainda evita o perigo — ou reconhecer isso explicitamente como limitação não testada (o que seria honesto, mas enfraquece a alegação de "safety before inspection" tal como está escrita na Seção III-C).

---

## 5. Pendências administrativas — atenção antes de resubmeter

Estas não são comentários de revisor de conteúdo, mas são condições formais da carta do editor e, se ignoradas, podem gerar rejeição por não conformidade independentemente do mérito científico:

1. ~~Mudança de autoria.~~ **[CORREÇÃO — item retirado.]** O PDF fornecido como "versão original" trazia Renato Santos Carrijo na lista de autores, mas o autor confirmou que ele **nunca esteve registrado como autor no IEEE Author Portal** para o manuscrito Access-2026-33687. Logo, não há "mudança de lista de autores" entre a submissão original e a v2, e o formulário "Request for Byline Change" **não se aplica**. O PDF local usado como referência tinha um metadado de autoria incorreto (provável reaproveitamento de template/cabeçalho de outro artigo em coautoria com o Prof. Carrijo); vale conferir se esse arquivo específico não está sendo reutilizado por engano em algum outro fluxo de trabalho, mas isso não gera pendência junto ao editor.
2. **Mudança de título.** Aceitável e bem justificada pelo conteúdo, mas deve ser mencionada explicitamente na carta de resposta aos revisores (idealmente até citando que foi R4 quem sugeriu esse reenquadramento), para o editor não estranhar a divergência com o título original registrado no sistema.
3. **Metadados de produção.** "Date of publication 00 Month, 0000", o DOI placeholder `10.1109/ACCESS.2024.0429000` e "VOLUME 11, 2023" continuam idênticos entre v1 e v2 — isso é normal (só é preenchido na produção final), mas confirme que não é exigido remover esse cabeçalho do template para a resubmissão.
4. **Declaração de financiamento.** [**Correção**: confirmado por diff caractere-a-caractere entre o PDF real de v1 e a v2 — nenhuma das duas versões efetivamente submetidas contém uma declaração de financiamento. O placeholder `TODO: informações de financiamento/apoio, se houver.` só existia no arquivo com metadado de autoria incorreto, não na v1 real. Portanto isto não é algo "removido entre versões", é uma lacuna que já existia desde o início.] Ainda assim, vale adicionar uma frase explícita na v2 (mesmo que seja para declarar ausência de financiamento), já que revistas IEEE costumam exigir essa declaração antes da publicação final.
5. **Divulgação de uso de IA.** Muito bem feito na v2 (parágrafo específico no Acknowledgment distinguindo o que foi gerado por IA — diagramas conceituais via Illustrae.co, texto/scripts assistidos por Claude — do que foi produzido pelo software próprio dos autores). Mantenha isso, é exatamente a prática que a IEEE espera.
6. **Checklist de resubmissão / PDF com marcações.** Lembre-se dos três arquivos exigidos pela carta: (i) documento de resposta aos revisores (comentário → resposta → ação, um a um, para os 4 revisores — ainda não escrito, e agora você tem a matéria-prima para isso a partir deste parecer); (ii) PDF com as alterações destacadas (highlight amarelo); (iii) cópia limpa final em Word/LaTeX + PDF.
7. **Item pendente do R2 (menor #5):** sementes aleatórias, regra de inicialização, real-time factor do simulador, hardware usado e identificador de commit/versão do código — não localizei essa informação no corpo do texto revisado. Como o repositório é público (`github.com/voidmmn/tese_react_nav`), considere ao menos referenciar a tag/commit exata usada para gerar os resultados relatados.

---

## 6. Veredito

Se este fosse meu parecer formal como revisor da IEEE Access na segunda rodada:

> **Recommendation: Minor Revision.**
> Os autores endereçaram a maioria das preocupações centrais das quatro revisões anteriores, notavelmente a questão mais grave (se a atualização de Bellman de fato influencia o comportamento do robô), com uma ablação decisiva e uma reformulação honesta da contribuição. A análise estatística e de robustez melhorou substancialmente. Permanecem, no entanto: (i) ausência de uma tabela estatística consolidada por par de configuração; (ii) nenhum cenário testa efetivamente o conflito simultâneo atração-repulsão, o que enfraquece a alegação de "safety before inspection" tal como formulada na Eq. (4)/Algoritmo 1; (iii) detalhes de reprodutibilidade (sementes, hardware, commit) ausentes; (iv) nenhuma métrica de utilidade de missão foi introduzida apesar do pedido explícito. Recomendo aceitação após esses pontos serem esclarecidos ou reconhecidos como limitação explícita.

Lembre-se: como o IEEE Access permite **apenas uma resubmissão**, vale a pena resolver o ponto da Seção 4 antes de reenviar — é o tipo de observação que, se um revisor original notar na segunda rodada, pode custar a rejeição definitiva sem mais chances.

Posso, se quiser, agora montar o documento formal de **"Response to Reviewers"** (no template exigido: comentário do revisor → resposta → ação), usando este parecer como base, um bloco por revisor.

---
---

# PARTE 2 — Reavaliação (Rodada 2)

**O que mudou nesta submissão:** vocês não fizeram ajustes cosméticos — foram direto no ponto mais grave que eu tinha levantado (Seção 4 da Parte 1) e resolveram com uma correção formal no modelo, não apenas com texto explicativo. Abaixo, o que isso significa item a item.

## 2.1 O problema da Seção 4 — **RESOLVIDO**, e bem resolvido

O que eu tinha apontado: a Eq. (4) antiga selecionava Φ por **magnitude pura** (`arg max_{|·|}`), então um evento de atração mais saliente venceria um hazard mais fraco simultâneo, contradizendo a alegação textual de "safety before inspection". E nenhum experimento testava esse conflito, porque o hazard sempre esteve espacialmente isolado dos clusters de atração.

**O que a v3 fez:**

1. **Reformulou a Eq. (4)** como uma regra de **precedência categórica**, não mais um concurso de magnitude:
 - Se qualquer evento repulsivo (hazard) estiver acima do limiar dentro do raio → Φ assume o valor (negativo) desse hazard, **independentemente** de qualquer atração concorrente, mesmo mais forte.
 - Só na ausência de qualquer hazard acima do limiar é que Φ seleciona, entre os eventos de atração concorrentes, o mais saliente em magnitude.
 - Isso é formalizado com dois conjuntos disjuntos de modalidade, H (hazard) e A (atração), o que também resolve de forma limpa a questão de notação que antes misturava sinal e magnitude num único critério.

2. **Adicionou um cenário experimental dedicado exatamente para testar isso** — o cenário **CONF** (Tabela 2, nova linha): coloca uma âncora de atração *forte* (`|w I_e| = 1.14`) no mesmo local de um hazard *mais fraco* (`|w I_e| = 1.05`). Um critério de seleção por magnitude pura escolheria a atração; a regra de precedência deve escolher Avoid mesmo assim.

3. **Reportou o resultado do teste de forma limpa e honesta**: em 9 das 10 runs válidas, Avoid foi disparado em 100% dos casos (9/9), a âncora de atração co-localizada nunca foi inspecionada, e a duração de missão (364±1 s) ficou indistinguível do cenário padrão — ou seja, a regra de segurança não custou nada em desempenho quando não havia conflito genuíno. Vocês corretamente rotulam isso como "propriedade categórica de segurança, não um efeito médio" e reportam como frequência de ocorrência (9/9), não como média — o tratamento estatístico certo para esse tipo de garantia binária.

**Meu veredito sobre este ponto: totalmente resolvido, e a forma como foi resolvido (mudança no modelo + experimento que tenta ativamente quebrar a alegação) é exatamente o padrão que eu, como revisor rigoroso, exigiria — não é uma correção "para inglês ver", é uma correção que se sujeita a ser refutada e não foi refutada.**

Um ponto residual — não um defeito, mas algo que eu, ainda no papel de chato, anotaria como observação para a discussão: a prioridade agora é **absoluta e categórica** — qualquer hazard acima do limiar, por menor que seja a margem, suprime qualquer atração, por mais saliente que seja. Isso é uma escolha de projeto defensável (e é o que se espera de um sistema de segurança), mas vale uma frase explícita no texto reconhecendo o trade-off: um hazard "no limite" do limiar (falso positivo em potencial) vai sempre vencer uma anomalia genuína e fortemente saliente. Isso não é um problema a corrigir — é só uma frase de uma linha que fortaleceria a discussão ("we adopt a hard safety priority by design; this trades a small risk of over-conservatism near the threshold for a categorical safety guarantee").

## 2.2 Outros pontos que também avançaram nesta rodada

| Item (da Parte 1) | Status anterior | Status agora | Evidência na v3 |
|---|---|---|---|
| Tabela estatística consolidada (R1-2/R2-7) | ⚠️ Parcial | ✅ **Resolvido em boa medida** | Nova Tabela 4 "Consolidated statistics" com Δ, Cliff's δ, IC 95%, p e p_H (Holm) para as comparações principais (E1 vs E3, E3 vs APF, RHB vs RHM) |
| Reprodutibilidade — sementes/hardware/versão (R2-min-5) | ❌ Não visto | ✅ **Resolvido** | Seção IV-D agora especifica hardware (Intel Xeon W-1350, 12 núcleos, 16 GB RAM, Ubuntu 22.04/WSL2, headless, RTF≈1), seed fixa do gerador de ruído de percepção, e "exact code version is archived under a tagged release in the repository" |
| Métrica de utilidade/custo de missão (R1-6) | ❌ Não resolvido | ✅ **Resolvido, de forma simples e honesta** | "each additional anomaly inspected costs about 2 m of extra travel (+6.1 m for three) and 15 s of mission time (+44 s for three)—a favorable exchange given that the fixed baseline inspects none" |
| Sensibilidade com/sem runs que falham (R2-7f) | ⚠️ Ambíguo | ✅ **Esclarecido** | Texto agora diferencia explicitamente falhas de inicialização (8/120, "the navigation container did not bring the robot up") dos timeouts de meio de missão da submissão anterior, e afirma que excluir ou incluir essas runs não muda nenhuma estatística comportamental — a única coisa que essas runs afetam é a taxa de confiabilidade de partida |
| Robustez a erro de localização, persistência de evento, geometria do mapa (R1-3) | ⚠️ Parcial, não reconhecido como lacuna | ⚠️ **Ainda não testado, mas agora reconhecido explicitamente** | "we do not model localization drift here; robustness to localization error, event persistence, and map geometry is left as future work" — antes isso era omissão silenciosa, agora é limitação declarada. Ainda vale cobrar o teste, mas a transparência já é uma melhoria editorial |

## 2.3 O que ainda fica em aberto (residual, não bloqueante)

1. **Baselines (b)/(c) do R2-5 continuam parciais.** A v3 mantém APF e a ablação E0, mas não adicionou nem (c) um Q-learning com recompensa aumentada convencional (o comparativo mais direto contra a própria formulação teórica do artigo) nem (d) um método de RL aprendido recente. Isso é aceitável como trabalho futuro, mas eu manteria a cobrança na carta de resposta, já que R2 pediu explicitamente "at minimum" essas comparações.
2. **A Tabela 4 de estatísticas consolidadas cobre as comparações "principais", não a família completa.** Faltam, por exemplo, comparações estatísticas formais para E0 vs E2–E4 (a prova de que a ablação é estatisticamente indistinguível, não só numericamente idêntica), E3 vs E5 (custo do cenário adverso), e N1/N2 vs E3 (robustez a ruído). Dado que o abstract promete "distribution-free tests" e "Holm correction across the family" de forma ampla, um revisor rigoroso vai notar que "a família" reportada na Tabela 4 é um subconjunto curado, não a família inteira de comparações feitas ao longo do artigo. Sugiro mover a tabela completa para um apêndice, mesmo que resumida.
3. **A garantia categórica de segurança (Seção 2.1 acima)** merece uma frase de reconhecimento do trade-off, como descrito.

## 2.4 Veredito atualizado

Com a correção da Eq. (4) e o cenário CONF, o problema que eu classificaria como potencialmente fatal para uma segunda rejeição (a alegação central de segurança "safety before inspection" não estar de fato garantida pelo mecanismo, nem testada) está **fechado com evidência direta**, não com retórica. Combinado com os outros três itens que também avançaram nesta rodada (estatística consolidada, reprodutibilidade, métrica de utilidade), o manuscrito está, na minha avaliação como revisor, em condição de:

> **Recommendation: Accept (com pendências editoriais menores).**
> Os três pontos da Seção 2.3 são do tipo que um Associate Editor tipicamente aceita resolver via "minor, non-blocking suggestions for the camera-ready version" — nenhum deles, isoladamente, justifica uma segunda rejeição dado que o IEEE Access só permite uma resubmissão. Recomendo, ainda assim, incluir ao menos uma frase sobre o trade-off da prioridade categórica de segurança e mencionar explicitamente na carta de resposta aos revisores que R2-5(c)/(d) ficam para trabalho futuro, para que o editor veja que o ponto foi considerado e não apenas ignorado.

---
---

# PARTE 3 — Reavaliação (Rodada 3, versão "última chance")

**Contexto:** o autor sinalizou que esta é a última oportunidade de aceite no IEEE Access (regra de resubmissão única). Apliquei o mesmo rigor da Parte 2, mas com atenção redobrada a qualquer coisa que pudesse motivar uma segunda rejeição.

## 3.1 Os três pontos residuais da Parte 2 — o que aconteceu

| Ponto residual (Parte 2, Seção 2.3) | Status agora |
|---|---|
| 1. Frase reconhecendo o trade-off da prioridade categórica de segurança | ✅ **Resolvido, quase literalmente como sugerido.** Nova passagem na Seção V-C: *"This is a deliberate design choice: the priority is hard and categorical, so a hazard barely above threshold—a potential false positive—always suppresses even a strongly salient genuine anomaly. We accept this trade-off, exchanging a small risk of over-conservatism near the threshold for a categorical safety guarantee, which is the appropriate bias for an inspection robot operating around energized equipment."* Isso é exatamente o reconhecimento que eu tinha pedido, e ainda vem com uma justificativa de domínio (equipamento energizado) que fortalece o argumento em vez de apenas admitir a limitação. |
| 2. Tabela estatística cobrindo só as comparações "principais", não a família inteira | ✅ **Resolvido com uma solução estatisticamente mais correta do que eu tinha pedido.** Nova **Tabela 9 (Apêndice B)** separa formalmente dois tipos de teste: (a) comparações **confirmatórias** (Tabela 4, com correção de Holm) e (b) comparações de **equivalência** (ablação η, robustez a ruído, custo do cenário adverso) reportadas com Cliff's δ + IC 95%, não com p-valor de significância. Isso é tecnicamente mais rigoroso do que simplesmente "adicionar mais linhas com p-valor" — testar equivalência (ausência de efeito) por p-valor de significância seria um erro metodológico clássico (ausência de evidência ≠ evidência de ausência); ao usar effect size + IC estreito ao redor de zero para as comparações de equivalência, os autores escolheram a ferramenta estatística certa para a pergunta certa. Isso resolve tanto o meu pedido quanto uma armadilha estatística que eu nem tinha explicitado. |
| 3. Baselines (c) Q-learning com recompensa convencional e (d) método de RL aprendido recente | ⚠️ **Ainda não adicionado.** Ver reclassificação abaixo (3.3). |

## 3.2 Verificação numérica cruzada (rodada de conferência final)

Como esta é a última chance, recomputei manualmente todos os números da nova Tabela 9 e da mudança na contagem de runs válidas para garantir que não há inconsistência que um revisor estatístico pudesse pegar:

- Todos os `Δ` da Tabela 9 batem exatamente com as diferenças de médias implícitas nas Tabelas 5 e 7 (ex.: E3 vs N1 em "Min. hazard dist." = 5.19 − 4.87 = 0.32 ✓; E3 vs E5 em "Mission time" = 390 − 364 ≈ 26.2, consistente com o arredondamento exibido ✓).
- A contagem global de runs mudou ligeiramente desta submissão para a anterior (**113/120 válidas, 7 falhas** agora vs. **112/120, 8 falhas** na rodada anterior), e o cenário CONF passou de 9/10 para 10/10 runs válidas. **Atualização do autor:** a causa real não foi estocasticidade de reexecução (como eu tinha especulado abaixo, incorretamente) — foi um **bug de leitura no pipeline de análise**: o glob que varre os arquivos de resultado pulava a repetição 4 (arquivo `115729`), fazendo o CONF aparecer como 9/10 quando na verdade era 10/10 válidas, 0 falhas reais. O autor corrigiu o glob, recontabilizou (120 runs, 113 válidas, 7 falhas) e removeu duas runs de validação que não deveriam estar na pasta `results/`, deixando o dataset do CONF com exatamente 10 repetições. ~~Isso é consistente com a explicação do texto de que essas falhas são de inicialização do container de navegação, não do comportamento do robô — ou seja, é ruído esperado de reexecução, não um dado alterado manualmente.~~ Como a causa era um bug de contabilidade e não de execução, o ponto de atenção correto não é "isso é normal entre reexecuções", e sim: **confirmar que todas as estatísticas do CONF (não só a contagem válida/falha) foram recalculadas com as 10 repetições completas**, e não deixadas coladas ao cache antigo de 9. Comparando o que foi reportado: a distância mínima ao hazard (4.82±0.05) e os retreats (1.1±0.3) aparecem idênticos entre as duas rodadas, enquanto o tempo mínimo até colisão mudou (16.7±2.4 → 16.6±2.3) — a mudança no TTC é evidência de que o recálculo aconteceu de fato; vale confirmar que a coincidência nos outros dois não é um resquício do cálculo antigo por trás de um arredondamento que por acaso bateu igual.

Não encontrei nenhuma outra inconsistência numérica, contradição textual ou tabela desalinhada com o texto nesta versão.

## 3.3 Reclassificação do ponto (c)/(d) — não é mais bloqueante

Na Parte 2 eu tratei a ausência de um baseline de Q-learning com recompensa convencional como uma pendência a cobrar com prioridade. Reavaliando com a versão atual do artigo, rebaixo a prioridade desse ponto, por um motivo estrutural: o artigo **já não reivindica** o termo de Bellman como um operador de aprendizado novo — a Seção III-B é explícita que é "reward augmentation, not a distinct learning operator", e a ablação com η=0 mostra que ele não influencia a ação executada nesta instância tabular. Ora, se o artigo não afirma que o termo de valor é competitivo como *mecanismo de aprendizado*, cobrar uma comparação contra outros métodos de aprendizado (RL com reward shaping, RL profundo) deixa de ser uma comparação estritamente necessária para sustentar a alegação central — vira uma comparação desejável para trabalho futuro, que é exatamente onde os autores já a colocaram ("Future work"). Continuo achando que uma frase reconhecendo explicitamente essa lacuna na carta de resposta ao R2 é prudente, mas não a trataria mais como risco de rejeição.

## 3.4 Um ajuste de acabamento (não bloqueante, mas eu pediria)

O resultado mais forte que vocês têm agora para sustentar "safety before inspection" é o cenário **CONF** (10/10 runs, prioridade de segurança mantida mesmo com uma atração 8% mais saliente do que o hazard). Esse resultado está descrito corretamente na Seção V-C, mas **não aparece nem no abstract nem nos bullets de contribuição da Introdução** — ele fica "enterrado" na seção de resultados. Dado que esse é exatamente o tipo de evidência que fecha a principal objeção de R2/R4 na rodada 1, eu o promoveria: uma cláusula no abstract (ex.: "...we verify this precedence holds even when a hazard is co-located with a more salient anomaly...") e uma menção no primeiro bullet de contribuição tornariam o ponto mais forte do artigo visível a quem lê só o abstract — o que inclui, na prática, o Associate Editor decidindo se manda para revisores de novo ou aceita direto.

## 3.5 Veredito final desta rodada

Não encontrei nenhum problema novo, nenhuma contradição introduzida pelas correções, e os três pontos que eu tinha deixado em aberto foram resolvidos (dois integralmente, um por reclassificação de prioridade, não por omissão). Na minha avaliação como revisor:

> **Recommendation: Accept.** As únicas sugestões restantes (Seção 3.4 acima, e a frase preventiva da Seção 3.2) são de polimento editorial, do tipo que caberia resolver na fase de galley proof / camera-ready, não uma condição para aceite. Não vejo, nesta versão, nenhum ponto que um revisor original da rodada 1 pudesse razoavelmente usar para justificar uma segunda rejeição.

Se eu fosse aconselhar sobre a carta de resposta aos revisores neste momento, o tom deveria ser: reconhecer explicitamente que R2-5(c)/(d) ficam para trabalho futuro (uma frase, não uma desculpa), e destacar o cenário CONF como a resposta direta e testada à preocupação de arbitragem levantada por R2 e R4 na rodada 1 — esse é o argumento mais forte que vocês têm para fechar o processo nesta submissão.
