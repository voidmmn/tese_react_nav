# Avaliação do plano de ressubmissão — IEEE Access

**Manuscrito:** Access-2026-46291  
**Documento avaliado:** PLANO_RESUBMISSAO.md  
**Data:** 13 de outubro de 2026

**O plano está bem estruturado e cobre praticamente todos os comentários, mas eu não o executaria exatamente como está.** A direção editorial está correta; alguns detalhes experimentais e matemáticos precisam ser corrigidos para que a revisão não introduza novas fragilidades.

Minha avaliação é do plano e de sua correspondência com os pareceres. **Não auditei os arquivos de código mencionados**, portanto as afirmações sobre implementação pronta, número de linhas e tempo de execução ainda precisam ser verificadas.

## 1. Manteria a estratégia central, mas reduziria o Eixo 6

Concordo com:

- retirar Bellman/RL das contribuições principais;
- atribuir os resultados de segurança aos componentes efetivamente responsáveis;
- acrescentar uma heurística no mesmo Nav2/MPPI;
- consolidar a comparação com APF;
- investigar confirmação, limiares e histerese;
- melhorar a discussão das premissas dos trabalhos relacionados.

Entretanto, **eu retiraria QD/QD0 desta ressubmissão e os reservaria para a tese ou outro artigo**.

Implementar uma política que realmente controla o robô reabre as questões de treinamento, convergência, transferência do simulador cinemático para Gazebo, ajuste de parâmetros, sementes de treinamento e intervenção do filtro de segurança. Dez execuções de uma única política treinada não avaliam a variabilidade do aprendizado.

Colocar isso no apêndice não reduz a obrigação de validá-lo. Além disso, os revisores ofereceram explicitamente a alternativa de reposicionar Bellman: **não é necessário cumprir simultaneamente as duas alternativas**.

O filtro por `/scan` também não deveria ser chamado de “muleta”. É um componente cuja intervenção precisa ser declarada e medida, caso essa investigação seja realizada.

## 2. O lema proposto contém um problema matemático importante

O plano propõe um limite:

$$
\frac{\eta\Phi_{\max}}{1-\gamma}.
$$

Mas, na atualização apresentada no manuscrito, o termo $\eta\Phi$ está **fora** da multiplicação por $\alpha$:

$$
Q\leftarrow Q+\alpha[r+\gamma\max Q'-Q]+\eta\Phi.
$$

A própria equivalência já demonstrada no artigo é com uma recompensa adicional $\eta\Phi/\alpha$. Portanto, o limite proposto omite esse fator.

Um exemplo de um estado, uma ação, recompensa zero e campo constante evidencia o problema. No equilíbrio:

$$
0=-\alpha(1-\gamma)Q+\eta\Phi,
\qquad
Q=\frac{\eta\Phi}{\alpha(1-\gamma)}.
$$

Isso **não estabelece um teorema para toda a implementação**, mas já mostra por que a expressão do plano não pode ser usada como está.

Também não podemos afirmar que o efeito “se anula com o tempo” apenas porque existe decaimento: novos eventos podem renovar o campo, e valores de pares estado–ação que deixam de ser atualizados podem conservar perturbações anteriores. Garantias de convergência exigem hipóteses próprias; o resultado clássico de Q-learning, por exemplo, exige amostragem repetida das ações nos estados. Ver [Watkins e Dayan (1992), *Q-learning*](https://www.gatsby.ucl.ac.uk/~dayan/papers/wd92.html).

**Minha recomendação: retirar a promessa desse lema do plano obrigatório.** Se permanecer, precisa de uma demonstração independente, com hipóteses explícitas. Uma perturbação limitada ou decrescente também pode existir em outras formas de aumento de recompensa; essa propriedade, sozinha, não demonstra originalidade.

## 3. HEU é o experimento certo, mas o contraste precisa ficar mais preciso

A proposta altera simultaneamente:

- seleção por saliência versus proximidade;
- disparo pelo campo versus alcance;
- aparentemente, a regra de tratamento do perigo.

Isso permite comparar **dois supervisores completos**, mas não atribuir uma diferença exclusivamente à ponderação por saliência.

Eu distinguiria duas perguntas:

| Pergunta | Comparação adequada |
|---|---|
| A arquitetura proposta oferece benefício sobre uma heurística simples? | Método completo versus HEU no mesmo Nav2/MPPI. |
| A seleção por saliência produz benefício específico? | Duas variantes que diferem apenas no critério de seleção, preservando os demais mecanismos. |

Na primeira comparação, mantenha explicitamente iguais percepção, *keepout*, metas de aproximação, confirmação, retorno à patrulha e orçamento de ajuste, salvo o que constituir deliberadamente a diferença entre os supervisores.

**Também mudaria a decisão de executar `conflict` e `adverse` apenas se houver empate no cenário padrão.** Escolha antecipadamente os cenários que respondem à hipótese e execute ambos os métodos neles. Isso evita que a bateria pareça uma busca posterior por um cenário favorável.

E atenção à expressão “decide certo o caso ambíguo”: escolher a anomalia mais saliente só constitui vantagem se houver um critério operacional independente que valorize essa escolha — por exemplo, tempo até inspecionar eventos prioritários. Reproduzir a regra de saliência não demonstra, por si só, melhor decisão.

## 4. A sensibilidade ao perigo precisa distinguir três limiares

Pela formulação do manuscrito, há pelo menos:

- o limiar de elegibilidade do evento;
- o limiar residual $\varepsilon$, que determina a precedência do canal de perigo;
- o limiar de entrada do FSM, que dispara a retirada.

**Variar apenas `enter_threshold` não testa necessariamente a precedência questionada pelo revisor.** Pode alterar o disparo da retirada enquanto a anomalia continua suprimida pelo canal de perigo.

No cenário marginal, registre separadamente:

- quando o perigo passa a dominar o campo;
- quando a inspeção é suprimida;
- quando ocorre retirada;
- qual é o custo em inspeções, atraso e distância ao perigo.

Além disso, variar o limiar de entrada com o de saída fixo não permite distinguir claramente efeito do limiar e efeito da largura de histerese. O Eixo 4c precisa explicitar quais pares entrada/saída serão testados.

## 5. A interpretação da distância de confirmação está forte demais

O plano afirma:

> “Se a completude recuperar com confirmação mais folgada, a degradação é do critério.”

Essa conclusão não decorre automaticamente do resultado. **Ampliar a distância pode simplesmente tornar mais fácil declarar uma inspeção concluída**, sem melhorar a aproximação física.

Eu preservaria uma medida independente, como distância real ao alvo ou atendimento de um requisito fixo de inspeção, e verificaria se o parâmetro:

- apenas classifica o resultado, permitindo reavaliar trajetórias existentes; ou
- altera o encerramento da inspeção e o comportamento, exigindo novas execuções.

A conclusão defensável seria que a completude é sensível ao critério de confirmação, acompanhada da análise da qualidade física da aproximação.

## 6. KOF é uma boa inclusão, com dois cuidados

Primeiro, confirme que a publicação do *keepout* funciona com a camada reativa desligada. A combinação de argumentos no comando não prova que os componentes estejam desacoplados.

Segundo, substitua **“resultado esperado: KOF empata com RHM”** por uma hipótese a testar. Não encontrar diferença estatística não demonstra equivalência.

KOF pode preservar a segurança sem inspecionar as mesmas anomalias. Por isso, compare as funções separadamente: segurança, completude de inspeção e custo de missão.

Na tabela consolidada, também não misture resultados de cenários diferentes como se fossem uma comparação direta. Se E3/APF/HEU estiverem no cenário padrão e RHM/KOF no cenário com perigo na rota, use painéis separados ou rode os comparadores nas mesmas condições.

## 7. Há correções pontuais importantes no restante do plano

| Trecho | Ajuste recomendado |
|---|---|
| **“9/10 [...] reporta contagem média”** | Isso parece uma leitura incorreta. No parecer, 9/10 aparece como execuções com inspeção completa sob agrupamento denso. Verifique a tabela original; não transforme essa proporção em média. |
| **Falhas de partida “independentes do tratamento”** | Trate como hipótese a sustentar pelos logs. Falhas de inicialização podem depender da configuração. Mostre tentativas, exclusões e motivos por grupo. |
| **Limite de aproximadamente 26%** | Corresponde a zero ocorrências em dez execuções. Para grupos com oito ou nove válidas, o limite é diferente. Use o denominador correto. |
| **Contagem de transições para avaliar a descontinuidade** | Uma contagem global não identifica efeito da fronteira $d=R$. Relacione cruzamentos da fronteira, sinal observado e transições, preferencialmente em um teste dirigido. |
| **Circularidade de $\Phi(s)$** | Explicar a ordem de cálculo ajuda, mas o estado com posição e bucket de $\lvert\Phi\rvert$ pode não determinar sinal, memória e configuração dos eventos. Considere notação temporal/observacional mais precisa. |
| **Carta anexada pelo portal** | A ausência da carta nos PDFs locais não prova qual slot causou a junção. Confirme o pacote de revisão antes de atribuir a causa. |
| **Adicionar 8–12 referências** | Selecione pelo que falta na argumentação, sem meta numérica. Os revisores pedem uma síntese mais crítica. |

## 8. O título proposto é adequado, mas retirar “Autonomous” não resolve sozinho a questão de escopo

O essencial é afirmar no resumo e na conclusão que a avaliação é em simulação, com percepção e localização idealizadas. A palavra “autonomous” não é, por si só, uma afirmação de validação em campo.

Também evitaria “stack industrial padrão” e usaria “stack de navegação ROS 2/Nav2”. Da mesma forma, “risk-aware navigation” como palavra-chave precisa corresponder ao tratamento efetivo de risco; detectar perigos e aplicar zonas proibidas não equivale automaticamente a modelar risco.

Na lista de contribuições, arquitetura e controlador atualmente se sobrepõem. Eu procuraria distinguir **o projeto da arquitetura**, **a avaliação comparativa** e **os resultados de atribuição e sensibilidade**, sem transformar cada componente em uma alegação separada de novidade.

## Recomendação para execução

**Minha recomendação é aprovar a direção do plano, com estas mudanças antes da execução:**

1. **Manter o reposicionamento e retirar QD/QD0 do escopo desta revisão.**
2. **Retirar ou reformular rigorosamente o lema.**
3. **Definir previamente HEU, cenários, métricas e contrastes.**
4. **Separar limiar de precedência, limiar de ação e histerese.**
5. **Avaliar confirmação com uma medida física independente.**
6. **Corrigir unidades, denominadores e afirmações causais antes da reescrita.**

O plano tem boa cobertura dos pareceres. O principal ganho agora será **torná-lo mais preciso e concentrado**, para que cada novo experimento responda a uma pergunta identificável e cada conclusão permaneça dentro do que os dados permitem afirmar.

