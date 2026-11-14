# Pendências de texto abertas pela refação das figuras

Criado em 13/11/2026. Cada item é um ajuste no `.tex` que **só pode ser aplicado quando
a figura nova substituir a antiga**. Marcar `[x]` ao aplicar.

## Regra geral, válida para todas

- [ ] **Fonte da legenda.** Todas as figuras refeitas usam hoje `\legend{Fonte: O próprio
  autor.}`. Para ilustração elaborada (não fotográfica) a forma correta é
  `\legend{Fonte: Elaborada pelo autor.}` — e, quando a figura reproduz esquema de
  terceiro já citado no texto, `\legend{Fonte: Elaborada pelo autor com base em
  Fulano (ANO).}`. Ver os itens por figura.
- [ ] **Extensão do arquivo.** As novas saem em `.png`; as chamadas atuais apontam para
  `.jpg`/`.pdf`. Converter com a skill `png-to-pdf` (achata RGBA sobre branco, 300 dpi)
  e ajustar `\includegraphics`.
- [ ] **Margens mortas.** Os PNGs do Illustrae saem quadrados, com faixa branca sobrando.
  Cortar antes de converter, senão vira espaço morto na página.

---

## Figura 2 — `fig_metodologia` (Cap. 1, §Metodologia)

- [ ] Fonte → `Elaborada pelo autor.`
- [ ] A legenda pode deixar de ser só "Fluxograma da metodologia adotada" e registrar o
  que a figura nova acrescenta: o capítulo e o produto de cada fase.

## Figura 3 — `fig_niveis_fusao` (§2.1.2)

- [ ] Fonte → `Elaborada pelo autor com base em Costa (2018) e Santos (2023).`
  (`Costa2018ImplementacaoFusao`, `Santos2023FusaoSensorial`, citados na abertura da
  subseção). Hoje reivindica autoria própria de taxonomia de terceiros.
- [ ] Legenda mais informativa, p. ex.: "Níveis de fusão sensorial: o mesmo fluxo de três
  sensores, variando o ponto em que a fusão ocorre."
- [ ] Avaliar reduzir de `width=\textwidth` para `0.85\textwidth` — é figura didática, não
  resultado.

## Figura 4 — `fig_filtro_kalman` (§2.1.3)

- [ ] **Item 1 da enumeração está errado para a figura nova.** Diz "Embora não esteja
  explicitamente rotulado, o processo começa com os dados vindos dos sensores" — a
  figura nova tem caixa `Medição do sensor` explícita. Reescrever.
- [ ] **Item 6 repete o erro categórico da figura antiga.** Lista "Ciclo Recursivo do
  Filtro de Kalman" como se fosse mais uma etapa; o ciclo é o conjunto, não uma etapa.
  Reescrever como fecho da enumeração, não como item.
- [ ] **Ordem da enumeração.** Hoje: Medição → Correção → Estado Estimado → Predição →
  Estado Previsto. A figura nova é o ciclo canônico de duas fases (Predição ↔ Correção).
  Reordenar a enumeração para casar com a figura.
- [ ] Fonte → `Elaborada pelo autor.`

## Figura 5 — `fig_agente_ambiente` (§2.2.1)

- [ ] Fonte → `Elaborada pelo autor com base em Sutton e Barto (2018).`
  (`Sutton2018`, citado na frase imediatamente anterior à figura.)
- [ ] A figura nova traz índice temporal (`a(t)`, `s(t+1)`, `r(t+1)`); o texto da
  subseção lista os elementos sem índice. Conciliar — ou explicar o índice na legenda.

---

## Decisão de escopo pendente (não é ajuste mecânico)

- [ ] As §2.1 (fusão sensorial, Figuras 3 e 4) fundamentam técnicas que **a tese não
  entrega**: o fim do Capítulo 3 declara que "nenhum mecanismo de percepção, de fusão
  sensorial ou de mitigação de interferência é alegado como contribuição desta tese", e
  a transformada de localização é mantida fixa por controle de confundimento. A decisão
  de **não** enxugar o Capítulo 2 já foi tomada; registrado aqui só para que seja
  decisão, e não esquecimento.
- [ ] A §2.2 (aprendizado por reforço, Figura 5) **não** tem esse problema: há
  atualização de valor com $\alpha$ e $\gamma$ e um baseline Q-driven treinado.

## Figura 6 — `fig_dqn` (§2.2.3)

- [ ] **`\legend` está ANTES do `\caption`**, invertido em relação a todas as outras
  figuras do documento. Corrigir a ordem.
- [ ] **Mudar de `width=0.8\textwidth` para `width=\textwidth`.** Medido: `\textwidth`
  = 455 pt = 16,0 cm; a 0,8 disso o menor rótulo da figura nova fica com 1,38 mm de
  altura de caixa alta (~6,9 pt equivalente), abaixo do piso de 9 pt. Em largura total
  sobe para 1,72 mm (~8,6 pt).
- [ ] Fonte → `Elaborada pelo autor com base em Mnih et al. (2015).` (`Mnih2015`, citado
  na frase que antecede a figura.)

## Classe de defeito que atinge QUATRO figuras — `\cite` em `\legend`

- [ ] `\legend{Fonte: Adaptado de \cite{...}}` imprime o autor **entre parênteses**
  ("Adaptado de (MUZY, 2012).") quando ele é o sujeito da frase. Trocar por
  `\citeonline`. Mesma classe do revisao interna. Ocorrências:
  - `cap_fundamentacao/sessao_2.3.tex:10` — `\cite{Muzy2012}`
  - `cap_fundamentacao/sessao_2.4.tex:41` — `\cite{Kortenkamp2016, Brugali2009ComponentI}`
  - `cap_fundamentacao/sessao_2.5.tex:12` — `\cite{Siegwart2011, Murphy2000}`
  - `cap_fundamentacao/sessao_2.5.tex:162` — `\cite{Durrant2006, Thrun2005}`
  (nos casos de duas referências, `\citeonline` precisa de duas chamadas ligadas por
  "e", porque não aceita lista.)

## Figura 7 — `fig_subestacao_tipica` (§2.3.1)

- [ ] **TC e TP não estão na lista de abreviaturas.** A figura nova já expande as duas
  siglas no próprio rótulo; verificar se o texto corrido também as usa sem expandir.

## Figura 8 — `fig_arquiteturas_roboticas` (§2.4.1)

- [ ] **A figura nova cobre três paradigmas, não quatro.** A arquitetura baseada em
  componentes foi deixada de fora por não ser um fluxo de controle, e sim um eixo
  ortogonal de organização de software. Ajustar a frase que chama a figura
  (`\autoref{fig:arquiteturas_roboticas}` em §2.4.1) para dizer que a figura compara os
  **três paradigmas de fluxo de controle**, e acrescentar uma frase explicando que a
  arquitetura baseada em componentes se situa em outro eixo. Sem isso, a figura
  contradiz a lista de quatro itens logo acima dela.
- [ ] Oportunidade: a arquitetura desta tese **é** a híbrida de duas camadas. Vale uma
  frase ligando a coluna "Híbrida" desta figura ao Capítulo 4.

## Figura 9 — `fig_ros_vs_ros2` (§2.4.2)

- [ ] **A frase que chama a figura está errada.** §2.4.2 diz que a figura "mostra a
  arquitetura de comunicação **proposta na documentação oficial** do ROS/ROS2" — mas a
  figura é desenho do autor, não reprodução da documentação. Reescrever.
- [ ] **A fonte não cita nada:** `\legend{Fonte: Adaptado da documentação oficial.}`.
  Qual documentação? A tese já cita `ROS2Design2024` e `Macenski2022` no parágrafo.
  Trocar por `Elaborada pelo autor com base em Macenski et al. (2022) e na documentação
  de projeto do ROS 2 (2024).`
- [ ] **Revisar a afirmação do texto** de que "a comunicação entre nós é gerenciada pelo
  ROS Master". O Master faz registro e descoberta; depois disso os nós comunicam-se
  ponto a ponto. A figura nova deixa essa distinção explícita, e o texto precisa
  acompanhá-la para não contradizê-la.

## Figura 12 — `architecture` (§4.1) — REFEITA, pendências de texto

- [ ] A legenda atual existe quase só para **traduzir cada rótulo interno** entre
  parênteses (`\emph{Deliberative --- Active sensing}`, `\emph{Waypoint patrol}`, etc.).
  Com a figura em português, toda essa tradução sai e a legenda encolhe para descrever
  o que a figura mostra.
- [ ] A figura nova desenha $\Phi$ como **série temporal escalar com limiar**, em vez da
  superfície espacial anterior. Isso agora concorda com o parágrafo de §4.2 que
  distingue $\Phi$ de um campo potencial espacial. Vale uma frase na legenda apontando
  que o decaimento aparece em degraus, por ser aplicado uma vez por período.

## Figura 13 — `stay_alert_fsm` (§4.5) — pendências de texto

- [ ] **A legenda contradiz o §4.2.** Hoje diz: "o campo puxa em direção à atração
  (\emph{attraction}) e empurra para longe da repulsão (\emph{repulsion})". Essa é
  exatamente a leitura de campo potencial espacial que o §4.2 nega — "não se toma seu
  gradiente e dele não se extrai direção de movimento alguma". Reescrever: $\Phi$
  arbitra qual canal governa e arma o disparo; a direção vem da geometria da meta
  emitida.
- [ ] **A ressalva sobre a terceira saída de `AVOID` pode sair.** A legenda hoje diz que
  "a lista completa e normativa das transições, incluindo a terceira saída de
  \textsc{Avoid}, está na Tabela~\ref{tab:prop-transicoes}" porque a figura antiga só
  mostrava duas. A figura nova inclui as três (seguro / recuado / esgotado), então a
  remissão passa a ser complementar, não corretiva.
- [ ] Como na Figura 12, a legenda deixa de precisar traduzir rótulos internos
  (`follow waypoints`, `inspected`, `timeout`, `safe`, `retreated`) e encolhe bastante.

---

# APLICADO em 14/11/2026

Todas as pendências acima foram executadas, exceto as marcadas abaixo como remanescentes.

**Figuras convertidas e substituídas (12):** achatadas sobre branco, margens mortas
cortadas, 300 dpi, via a skill `png-to-pdf`. Todas as chamadas `\includegraphics` do
Capítulo 2 passaram de `.jpg`/`.png` para `.pdf`; `architecture` e `stay_alert_fsm` são
chamadas sem extensão e já recebem o PDF novo.

**Fontes das legendas corrigidas (10):** "O próprio autor" → "Elaborada pelo autor",
com atribuição a terceiros onde a figura adapta esquema citado (Costa e Santos; Sutton
e Barto; Mnih et al.; Muzy; Kortenkamp e Brugali; Macenski e documentação do ROS 2;
Siegwart e Murphy; Durrant-Whyte e Thrun). Os quatro `\cite` dentro de `\legend`
viraram `\citeonline`.

**Correções de texto acopladas às figuras:**
- §2.1.3 — enumeração do filtro de Kalman inteiramente reescrita: a ordem passou a ser
  o ciclo de duas fases; o item que dizia que a medição "não está explicitamente
  rotulada" saiu; e o item que listava "Ciclo Recursivo do Filtro de Kalman" como se
  fosse uma etapa foi substituído por um fecho que declara que o filtro **é** o ciclo.
- §2.4.1 — a frase que chama a figura passa a dizer que ela compara os **três**
  paradigmas de fluxo de controle, e explica que a arquitetura baseada em componentes
  está em outro eixo; acrescentou-se a ligação com o Capítulo 4.
- §2.4.2 — a frase que dizia que a figura mostra "a arquitetura proposta na documentação
  oficial" foi corrigida, e o parágrafo que afirmava que "a comunicação entre nós é
  gerenciada pelo ROS Master" passou a distinguir descoberta de tráfego de dados.
- §4.1 e §4.5 — as duas legendas deixaram de ser glossários de tradução. A de §4.5
  perdeu a frase "o campo puxa em direção à atração e empurra para longe da repulsão",
  que contradizia §4.2, e a ressalva sobre a terceira saída de `AVOID` deixou de ser
  corretiva, por a figura agora trazer as três.
- §6.1 e `.bib` — artigo atualizado de "aceito" para "publicado em acesso antecipado".

**Verificação:** 178 páginas, erros=0, zero citações indefinidas, zero referências
indefinidas, nenhum estouro de linha novo (os cinco maiores são os pré-existentes).

## REMANESCENTE

- [ ] **DOI do artigo** — marcado como `PENDENTE` em `MirandaNeto2026TwoLayer`. O IEEE
  Xplore não entrega conteúdo a cliente automatizado; colar da página do artigo.
- [x] **Figura 1 (`fig_contextualizacao`)** — RESOLVIDA em 14/11/2026. O autor
  confirmou que a fotografia é sua, feita em subestação da Eletronorte, com uso
  autorizado. A ilustração conceitual genérica foi substituída pela foto. A legenda
  foi reescrita: deixa de negar que seja registro fotográfico e passa a declarar o que
  é, mantendo a ressalva essencial de que a plataforma retratada **não** é a avaliada.
  Fonte passou a "Fotografia do autor, registrada em subestação da Eletronorte".
  Largura reduzida de 0,8 para 0,45 do texto, porque a foto é em retrato (720x1280) e
  a 0,8 ocuparia 22,8 cm de altura. A placa de um veículo de terceiro ao fundo foi
  borrada por privacidade, e a alteração está declarada na própria legenda e no
  comentário do fonte.
  - [ ] Se existir o original em resolução maior que 720x1280, vale substituir: a
    7,2 cm de largura a imagem atual rende 254 ppi, abaixo dos 300 usados no resto.
- [ ] **Figuras 14, 15 e 16** (`world_map`, `traj_overlay`, `box_panel`) — intocadas por
  serem saída de script, não ilustração conceitual. Regeneráveis pelos scripts
  listados em §5.9.2.
