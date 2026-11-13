# Prompts para o Illustrae — refação das figuras da tese

## Estilo da casa (repetir em toda figura)

> Fundo branco puro. Sem sombras, sem gradientes, sem efeito tridimensional, sem ícones
> decorativos. Preenchimento das caixas em azul claro `#CFE2F3`, contorno `#1F3864` com
> 1,5 pt, texto `#000000`. Um único tom de destaque, laranja escuro `#B45F06`, reservado
> para o que é resultado ou artefato produzido. Tipografia sans-serif humanista (Source
> Sans Pro, Lato ou equivalente); caixa alta apenas nos títulos de etapa, o resto em
> caixa mista. A figura será impressa com 12,5 cm de largura em página A4 — nenhum texto
> pode ficar abaixo do equivalente a 9 pt nessa largura. Setas retas, pretas, com ponta
> sólida preenchida. Todo o texto em português do Brasil, exatamente como transcrito.

---

## Figura 2 — Fluxograma da metodologia adotada

**Arquivo de destino:** `figuras_novo/fig_metodologia.*`
**Onde entra:** Capítulo 1, Seção "Metodologia" (`cap_introducao/introducao.tex`).

### Prompt

```
Crie um fluxograma vertical de cinco etapas em três colunas, para um documento
acadêmico impresso em preto e branco ou em cores, proporção aproximada 4:3 em retrato
(sugestão 1400 x 1150 px).

ESTILO
Fundo branco puro. Sem sombras, sem gradientes, sem efeito tridimensional, sem ícones
decorativos. Caixas das etapas com preenchimento azul claro #CFE2F3, contorno #1F3864
de 1,5 pt e cantos levemente arredondados. Texto preto #000000. Tipografia sans-serif
humanista (Source Sans Pro, Lato ou equivalente). Setas retas verticais, pretas, com
ponta sólida. A figura será reduzida para 12,5 cm de largura: nenhum texto pode ficar
menor que o equivalente a 9 pt nessa largura. Todo o texto em português do Brasil,
exatamente como transcrito abaixo, sem traduzir e sem reescrever.

ESTRUTURA
Três colunas alinhadas em cinco linhas.
- Coluna da esquerda, estreita: uma etiqueta discreta, em cinza escuro #595959, sem
  caixa, indicando o capítulo correspondente.
- Coluna central, larga: a caixa azul da etapa, com o título em CAIXA ALTA e negrito.
  As cinco caixas centrais têm a MESMA largura e estão centralizadas no mesmo eixo
  vertical, ligadas por uma seta vertical preta de cada caixa para a seguinte.
- Coluna da direita: o produto daquela etapa, em texto corrido de caixa mista, cor
  laranja escuro #B45F06, sem caixa, precedido de um pequeno marcador quadrado da
  mesma cor. Ligado à caixa central por um traço horizontal fino cinza.

CONTEÚDO, linha a linha

Linha 1
  esquerda: Caps. 2 e 3
  centro:   REVISÃO CRÍTICA DA LITERATURA
  direita:  Lacunas declaradas e matriz de trabalhos próximos

Linha 2
  esquerda: Cap. 4
  centro:   PROJETO DA ARQUITETURA DE DUAS CAMADAS
  direita:  Campo com dois canais de memória, regra de precedência e máquina de estados

Linha 3
  esquerda: Caps. 4 e 5
  centro:   IMPLEMENTAÇÃO EM ROS 2, NAV2/MPPI E GAZEBO FORTRESS
  direita:  Pacotes ROS 2 e seis cenários de simulação

Linha 4
  esquerda: Cap. 5
  centro:   AVALIAÇÃO EXPERIMENTAL
  direita:  32 pares configuração–cenário; 320 execuções tentadas, 311 válidas

Linha 5
  esquerda: Cap. 6
  centro:   ANÁLISE ESTATÍSTICA
  direita:  Testes livres de distribuição, tamanhos de efeito e intervalos bootstrap;
            pacote reprodutível verificável por somas de verificação

OBSERVAÇÕES
Não acrescente etapas, não acrescente setas de retorno ou de iteração entre as etapas:
o fluxo é estritamente linear, de cima para baixo. Não acrescente título dentro da
figura — a legenda fica fora, no documento. Mantenha o cifrão, o travessão e os
acentos exatamente como escritos.
```

### Ajustes a fazer no documento quando a figura chegar

- Trocar `\legend{Fonte: O próprio autor.}` por `\legend{Fonte: Elaborada pelo autor.}`,
  que é a forma usada nas demais figuras elaboradas, não fotográficas.
- A legenda pode deixar de ser só "Fluxograma da metodologia adotada" e passar a
  registrar o que a figura acrescenta: o capítulo e o produto de cada fase.
