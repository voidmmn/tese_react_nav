# Tese de doutorado — Milton Miranda Neto (UFU)

Área de trabalho para a **escrita do documento da tese**. Este README é o **log de
progresso** — mantido atualizado a cada avanço para que uma nova sessão do Claude
Code (ou o próprio autor) recupere rapidamente o que já foi feito.

## Contexto

- **Autor:** Prof. Milton Miranda Neto (doutorando, UFU).
- **Orientador:** Prof. Alexandre Cardoso (UFU).
- **Qualificação:** aprovada. Banca: Prof. Renato Aquino Lopes (UFU) e
  Prof. Ígor Andrade Moraes (UEMG).
- **Publicação A2 exigida pelo programa:** artigo IEEE Access (Qualis A2) — "A
  Two-Layer Deliberative–Reactive Architecture with an Affective Attraction–Repulsion
  Layer for Autonomous Substation Inspection", **submetido em 2026-09-12** e
  confirmado em revisão (2026-09-14). **Manuscript ID: Access-2026-46291**
  (resubmissão; ID original: Access-2026-33687). Materiais em `docs/artigo/`.
- **Hipótese/tema:** navegação deliberativa–reativa com campo afetivo de
  atração/repulsão (camada "Stay Alert") sobre Nav2/MPPI, para inspeção autônoma de
  subestações. Código: `~/tese_ws` (github.com/voidmmn/tese_react_nav).

## Estrutura (mesmo padrão do artigo)

```
docs/tese/
├── README.md        ← este log
├── sections/        ← capítulos/seções em .tex (via \input no main)
└── figs/            ← figuras (PNG→PDF para o Overleaf)
```

## Convenções

- LaTeX **modular**: um arquivo por capítulo em `sections/`, incluídos por `\input`
  a partir do arquivo principal (a definir com base no template da qualificação).
- Figuras: converter PNG→PDF com a skill **`png-to-pdf`**
  (`python3 .claude/skills/png-to-pdf/scripts/png2pdf.py figs/x.png`).
- Registrar cada passo importante aqui **e** na memória do Claude Code
  (`project-tese-documento`).

## Log de progresso

### 2026-09-12 — Setup da área de trabalho
- Criados `docs/tese/`, `docs/tese/figs/`, `docs/tese/sections/`.
- Criada a skill `png-to-pdf` (`.claude/skills/png-to-pdf/`), testada e funcionando.
- Registrada a memória `project-tese-documento` + índice `MEMORY.md`.
- **Pendente:** receber o **.zip do LaTeX da qualificação** (já aprovado) para
  reusar a estrutura como base da tese. Só então montar o `main.tex` e os capítulos
  (não criar antes, para não conflitar com o template da qualificação).

### 2026-09-14 — Submissão do artigo confirmada
- IEEE Access confirmou a submissão da resubmissão. **Novo Manuscript ID:
  `Access-2026-46291`** (o original era `Access-2026-33687`) — usar o novo em toda
  correspondência. Status: em revisão ("full consideration"). APC US$ 2.160 só se
  aceito. Sem pendência de lista de autores.

### 2026-09-14 — Qualificação extraída e estrutura mapeada
- `Qualificação_2_Milton.zip` extraído em `docs/tese/` (base da tese). Removidos os
  `figs/`/`sections/` vazios (o template usa `figuras/` e `cap_*/`).
- **Template:** ABNTeX2, classe `ppgee` (PPGEE-UFU), main `main_ppgee_ufu.tex`,
  hoje `[qualidr]` → trocar p/ **`[tesedr]`** na tese. Coorientador:
  **Edgard A. Lamounier Junior**. `\data{2025}` → ano da defesa.
- **Capítulos:** introdução · fundamentação (sessões 2.1–2.5) · revisão sistemática ·
  proposta · resultados/cronograma · conclusão · bib ABNTeX2.
- **Ponto estratégico:** o resumo/proposta da qualificação = *framework amplo*
  (fusão sensorial + RL + visão, 5 módulos); o entregue/publicado (artigo A2) = a
  arquitetura FOCADA de duas camadas com campo afetivo (Stay Alert). A tese será
  construída em torno do que foi realmente feito — reconciliação de escopo a definir.

### 2026-11-09 — Tese montada a partir do artigo aceito

- **Artigo ACEITO na IEEE Access** (09/11/2026), com *minor changes* do Revisor 2
  (abstract mais enxuto + nota de trade-off), já aplicadas em `docs/artigo/`.
- **Classe trocada** de `[qualidr]` para `[tesedr]`; `\data{}` para 2026.
- **Ambiente LaTeX resolvido:** o TinyTeX local não tinha `abntex2`. Instalados via
  `tlmgr` (modo usuário, sem sudo): abntex2, memoir, xpatch, textcase, enumitem, ae,
  lastpage, pdfpages, algorithms, nomencl, koma-script, cmap, lipsum, acronym,
  bigfoot, xstring, colortbl, multirow, booktabs, bm, babel-portuges,
  hyphen-portuguese. **Compila do zero:** `./compilar.sh`.
- **Capítulos novos/reescritos:**
  - `cap_proposta/` → **Arquitetura Proposta** (campo Φ com dois canais de memória,
    precedência categórica, FSM Stay Alert, zona de exclusão deliberativa,
    abstração de eventos, nota de projeto sobre a atualização de valor).
  - `cap_avaliacao/` → **Avaliação Experimental** (NOVO capítulo: ambiente, cenários,
    matriz de 20 configurações, métricas, hiperparâmetros, reprodutibilidade).
  - `cap_resultados/` → **Resultados e Discussão** (reescrito integralmente a partir
    da Seção V do artigo; substituiu o antigo "Trabalhos Realizados e Cronograma").
  - `cap_conclusao/` → **Conclusão** (as três atribuições, limites da evidência,
    escopo, limitações, trabalhos futuros; substituiu "Considerações Finais
    Preliminares").
  - `cap_introducao/` → objetivos, metodologia e organização reescritos no passado e
    alinhados ao entregue.
  - Resumo e abstract reescritos; palavras-chave trocadas.
- **Figuras:** `architecture`, `stay_alert_fsm`, `world_map`, `traj_overlay`,
  `box_panel` copiadas do artigo. As três quantitativas foram **regeneradas em
  português** pelos scripts em `figuras/` a partir de `~/tese_ws/results` (os n por
  configuração reproduzem os do artigo: E1 10, APF 9, HEU 9, HEU-sel 10, E3 10).
- **Correções de compilação:** `amsmath`/`bm`/`booktabs`/`multirow` carregados;
  `ros_control` e `ament_cmake` escapados; `\citep`/`\citet` convertidos para
  `\cite`/`\citeonline`; resíduo de markdown/HTML removido do capítulo de proposta.
- **Estado:** 139 páginas, **zero erros de compilação**.

### Rodada de revisão de 13/11/2026

Fechadas nesta rodada: auditoria bibliográfica completa, censo de execuções, relato
estatístico integral, reenquadramento do Capítulo 3 como **Revisão Crítica da
Literatura**, consistência de escopo, pergunta de pesquisa e contribuições declaradas,
matriz de trabalhos próximos, especificação operacional do supervisor, delimitação da
atribuição causal, documentação do baseline Q-driven, definições executáveis das
métricas, alcance das repetições, papel do aprendizado, reorganização da conclusão,
situação editorial do artigo e artefato de reprodutibilidade.

**Estado:** 180 páginas, zero erros de compilação, zero citações indefinidas, zero
referências cruzadas pendentes.

#### Reprodutibilidade — o que identifica esta versão

- A versão correspondente à tese é a etiqueta **`tese-defesa-v1`**, cujas notas de
  lançamento registram o *commit* exato. O ramo `main` segue recebendo trabalho e
  **não** é o estado avaliado.
- `results/CHECKSUMS.sha256` cobre os **323** arquivos de resultado (320 CSVs por
  execução + trilha de auditoria + família primária + manifesto). Conferir com
  `cd results && sha256sum -c CHECKSUMS.sha256`.
- `results/manifesto_execucoes.csv` é a fonte única dos totais: 32 pares, 320
  tentativas, 311 válidas, 9 imóveis, 9 censuradas.
- Cada tabela de resultado é regenerada por um *script* nomeado na §5.9 da tese.

#### Mudanças no instrumento feitas nesta rodada

- `rodar_experimentos.sh` passa a gravar `commit=<sha>` (com sufixo `+sujo` se a
  árvore de trabalho estiver modificada) na linha de lançamento de cada execução.
- `gerar_manifesto.py` passa a ler esse campo e a emitir a coluna `commit`. Nas
  baterias anteriores a 13/11/2026 a coluna fica **vazia** — commit por execução não é
  recuperável retroativamente, e inferi-lo pela data seria conjetura apresentada como
  registro.

#### Defeito de implementação documentado e **não** corrigido

`AttractionField.step_decay()` autoriza a aplicação do fator de decaimento comparando
instantes de **relógio de parede**, enquanto todos os temporizadores dos nós seguem o
relógio simulado (`use_sim_time`). Com fator de tempo real acima da unidade, o período
de decaimento realizado é de cerca de 2 s simulados em vez de 1 s. O comportamento é
idêntico em todos os braços, de modo que não confunde contraste algum, e as janelas de
persistência relatadas são medidas e não derivadas dos parâmetros. Está declarado na
§4.6 da tese. **Corrigir antes de qualquer bateria nova**, porque mudaria o
comportamento de todos os braços.

### Pendências registradas no próprio código

1. **Título** (`main_ppgee_ufu.tex`): ainda é o da qualificação e promete RL e fusão
   sensorial. Bloco de comentário no arquivo com a sugestão alinhada ao entregue.
2. **`Chen2024`** (`cap_revisao_bib/revisao.tex`): citação sem entrada na bib e sem
   fonte localizável. **Não** foi inventada entrada; o PDF imprime `[?]`.
3. **DOIs que não resolvem no Crossref** (7 de 51 citados): AtlantisPress2023Analysis,
   Hussain2020ReviewChallenges, Liu2016EMC, Oliveira2021EstudoAplicacao (prefixo
   duplicado — já corrigido, mas segue 404), Tai2024AutonomousRL, Wang2024Advancements,
   Zhang2023ARVR. 404 no Crossref não prova inexistência (Atlantis/E3S depositam fora),
   mas vale conferir.

## Próximo passo

- Fechar o **título** com o Prof. Alexandre e propagar (capa, ficha catalográfica,
  folha de aprovação, formulários SEI em `docs/documentos-banca/`).
- Resolver `Chen2024` e conferir os 7 DOIs listados acima.
- Revisar os Capítulos 2 e 3 (fundamentação e revisão), herdados da qualificação:
  continuam válidos como contexto, mas não passaram por revisão nesta rodada.
- Figuras conceituais (`architecture`, `stay_alert_fsm`) ainda têm texto interno em
  inglês. Mitigação aplicada em 13/11/2026: ampliadas para a largura total do texto e
  legendas reescritas traduzindo **todos** os rótulos internos, com remissão à tabela
  de transições, que é a fonte normativa. Regerar no Illustrae continua sendo o
  desfecho preferível.
- Criar e publicar a etiqueta `tese-defesa-v1` no commit final, e colocar o *commit*
  exato nas notas de lançamento — a §5.9 da tese já remete a ela.
- Duas figuras conceituais foram **removidas** do Capítulo 1
  (`fig_problema_pesquisa.jpg`, `fig_justificativa.jpg`): a primeira enumerava quatro
  desafios que a tese não trata, a segunda nomeava fusão sensorial e aprendizado por
  reforço como as contribuições científicas do trabalho. Os arquivos continuam em
  `figuras/`.
