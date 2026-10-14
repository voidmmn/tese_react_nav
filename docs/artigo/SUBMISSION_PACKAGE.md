# Pacote de submissão — IEEE Access (RESUBMISSÃO)

**Resubmissão revisada** do manuscrito Access-2026-33687 (rejeitado com uma
resubmissão permitida). Além do manuscrito, esta submissão exige a **carta de
resposta ponto-a-ponto aos revisores** (ver seção 3b) — que a versão original
deste checklist não listava.

Portal: IEEE Author Portal (https://ieee.atyponrex.com/) — login com conta IEEE
(não serve ScholarOne). O sistema COMPILA o LaTeX; fonte e PDF devem bater.

## 1. Fonte LaTeX (ZIP — Overleaf: Menu > Download > Source)
Conteúdo obrigatório do ZIP:
- [ ] access.tex
- [ ] sections/01_introduction.tex
- [ ] sections/02_related_work.tex
- [ ] sections/03_method.tex
- [ ] sections/04_experimental_setup.tex
- [ ] sections/05_results.tex
- [ ] sections/06_conclusion.tex
- [ ] sections/07_appendix.tex
- [ ] references.bib
- [ ] access.bbl            (gerado pelo BibTeX — incluir! REGERAR após as
                             mudanças de referências desta rodada, senão compila
                             com bibliografia velha)
- [ ] ieeeaccess.cls        (do template)
- [ ] IEEEtran.bst          (do template)
- [ ] figs/architecture.pdf
- [ ] figs/box_panel.pdf     (VERSÃO NOVA — regerada com os dados atuais; a antiga
                             mostrava E5 com 3 inspeções e 440 s. Gerar de dentro
                             de figs/: `cd figs && python3 gen_boxpanel.py`)
- [ ] figs/concept_overview.pdf
- [ ] figs/qconv.pdf
- [ ] figs/stay_alert_fsm.pdf (VERSÃO CORRIGIDA da Fig. 3 — FSM com θin único,
                             seta unidirecional Investigate→Avoid, retorno
                             Avoid→Patrol e nota de refratário sem override)
- [ ] figs/traj_overlay.pdf
- [ ] figs/world_map.pdf

## 2. PDF do manuscrito
- [ ] PDF compilado no Overleaf (casa com o fonte). NÃO usar o "(Paperpal Edit).pdf".

## 3. Cover letter (PDF)
- [ ] cover_letter.tex compilado -> PDF, subir como "Cover Letter".
      (Documento STANDALONE — não vai no ZIP do manuscrito nem no Overleaf do
      artigo; compilar sozinho. Subir o PDF, NÃO o .md nem o .tex.)

## 3b. Response to Reviewers (PDF) — OBRIGATÓRIO NA RESUBMISSÃO
- [ ] response_to_reviewers.md compilado/exportado -> PDF, subir como
      "Response to Reviewers" (ou anexo suplementar, conforme o portal pedir).
- [ ] Conferir a resposta contra os comentários ORIGINAIS dos 4 revisores
      (arquivo "comentarios dos revisores.txt") — a numeração R1.1–R4 deve casar.
- [ ] Conferir as letras/números de seção citados na resposta contra o PDF final.

## 4. Graphical Abstract
- [ ] Graphical Abstract dedicado. O portal pede um GA próprio; opções:
      figs/GA.png (banner dedicado, sem números falsos) OU
      figs/concept_overview.pdf (Fig. 1). Escolher UM e conferir as regras de
      tamanho/formato do IEEE Access.

## NÃO subir (dado pessoal / lixo / fontes .md)
- alexandre.pdf, milton.pdf (Lattes — bios já estão no manuscrito)
- cover_letter.md, response_to_reviewers.md (são FONTES; subir os PDFs gerados
  deles, não o .md)
- os Parecer_*.md (avaliações internas — NÃO são os comentários dos revisores)
- IEEE-Access-Submission-Checklist.pdf, ieee.txt, PROMPTS_REGENERAR_FIGURAS.md
- resultado_preflight.png, "(Paperpal Edit).pdf", *.Zone.Identifier

## Metadados no portal
- [ ] Manuscript type: Research Article
- [ ] Título (igual ao access.tex)
- [ ] Abstract (~210 palavras, colar)
- [ ] Keywords (as 10 do access.tex)
- [ ] Autor 1: Milton Miranda Neto — correspondente — voidmmn@ufu.br —
      ORCID 0000-0002-1568-4201 (público e vinculado à conta IEEE)
- [ ] Autor 2: Alexandre Cardoso — alexandre@ufu.br — ORCID (dele)
- [ ] Funding: declarar se houver (CAPES/CNPq/FAPEMIG); senão "None"
- [ ] Conflitos de interesse: None
- [ ] Reviewers sugeridos/opostos: opcional

## Pré-voo (antes de clicar em submeter)
- [ ] ORCID do Milton público e vinculado no portal (item 4 do checklist)
- [ ] PDF e fonte idênticos em conteúdo (subir o `04_experimental_setup.tex` e
      demais .tex atualizados na última rodada; recompilar)
- [ ] Todas as figs/tabelas aparecem e estão citadas (Fig. 5 = box_panel NOVO)
- [ ] Refs [1]-[21] resolvidas, sem "??" no PDF (literatura expandida; access.bbl
      regerado)
- [ ] Cover letter (PDF) e Response to Reviewers (PDF) prontos como anexos do
      portal (não no ZIP do manuscrito)
- [ ] Bios dos 2 autores presentes após as referências
- [ ] Acknowledgment com disclosure de IA presente
- [ ] < 20 páginas, < 40 MB por arquivo
