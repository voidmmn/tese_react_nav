# Tese de doutorado — Milton Miranda Neto (PPGEE/UFU)

Fontes LaTeX da tese *Arquitetura deliberativo-reativa de duas camadas com campo de
atração–repulsão disparado por limiar para inspeção de subestações*.

- **Autor:** Milton Miranda Neto · **Orientador:** Alexandre Cardoso (UFU)
- **Publicação decorrente:** IEEE Access, DOI
  [10.1109/ACCESS.2026.3753770](https://doi.org/10.1109/ACCESS.2026.3753770).
  Fontes em `../artigo/`.
- O uso de ferramentas de inteligência artificial na preparação deste trabalho está
  declarado nos pré-textuais da tese e no *Acknowledgment* do artigo.

## Como compilar

```bash
./compilar.sh          # pdflatex x3 + bibtex -> main_ppgee_ufu.pdf
```

Requer `abntex2` e a classe `ppgee.cls` (incluída). Dependências TeX Live/TinyTeX:
`abntex2 memoir xpatch textcase enumitem ae lastpage pdfpages algorithms nomencl
koma-script cmap lipsum acronym bigfoot xstring colortbl multirow booktabs bm
babel-portuges hyphen-portuguese`.

## Organização

| Caminho | Conteúdo |
|---|---|
| `main_ppgee_ufu.tex` | arquivo principal; classe `ppgee` com a opção `tesedr` |
| `cap_introducao/` … `cap_conclusao/` | um diretório por capítulo, incluídos por `\input` |
| `figuras/` | figuras conceituais e quantitativas (`.pdf` para o pdfLaTeX) |
| `bib/` | bibliografia no padrão abntex2 |
| `compilar.sh` | compilação completa |

As figuras quantitativas são **geradas** pelos scripts em `figuras/` a partir de
`../../results`; não são editadas à mão.

## Reprodutibilidade

A versão avaliada é a etiqueta **`tese-defesa-v1`**, cujas notas de lançamento
registram o *commit* exato. O ramo `main` continua recebendo trabalho e **não** é o
estado avaliado.

O pacote de reprodutibilidade (`empacotar_reprodutibilidade.sh`, na raiz do
repositório) reúne o código, as 320 execuções analisadas com um CSV e um log de
lançamento cada, a verificação do decaimento temporal, a trilha de auditoria, os
manifestos, as somas de verificação e o manifesto dos lançamentos descartados. Os
procedimentos, os denominadores e as limitações declaradas estão no Capítulo 5 da tese;
cada tabela de resultado é regenerada por um script ali nomeado.

## Limitação de implementação declarada

A guarda que autoriza o decaimento dos acumuladores compara instantes de relógio de
parede, enquanto os temporizadores dos nós seguem o relógio simulado, de modo que o
período realizado nas 320 execuções analisadas ficou em cerca de 1,6 s onde a
especificação pede 1 s. Isso está declarado na Seção 4.5.2 e verificado na Seção 6.13,
que mede o que muda sob o relógio especificado: os contrastes centrais sobrevivem, e a
janela de supressão relatada na Seção 6.8.1 não. O padrão do parâmetro `decay_clock`
permanece `wall` de propósito, para que as execuções analisadas sigam comparáveis entre
si e com o artigo publicado.
