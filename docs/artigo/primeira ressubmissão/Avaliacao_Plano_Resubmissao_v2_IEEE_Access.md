# Avaliação do plano de ressubmissão — versão 2

**Manuscrito:** Access-2026-46291 — IEEE Access  
**Documento avaliado:** PLANO_RESUBMISSAO(1).md  
**Data:** 13 de outubro de 2026

**A versão 2 está substancialmente melhor. Eu a adotaria como base para executar a revisão, com alguns ajustes localizados antes de iniciar a bateria.** As correções mais importantes foram incorporadas: retirada do lema e de QD/QD0, separação dos cenários, delimitação de KOF e planejamento antecipado das comparações.

A auditoria também trouxe uma economia justificada: **se `inspect_confirm_dist` realmente só pontua o resultado, a reavaliação das mesmas trajetórias é a abordagem adequada**. Não há motivo para executar novamente o robô apenas para mudar esse critério.

Minha avaliação continua condicionada às informações da auditoria que você apresentou; não inspecionei diretamente o repositório.

## 1. A conclusão sobre a ausência de perigo marginal ainda precisa considerar o decaimento e as condições do FSM

A conta está correta **no instante de incorporação de um evento elegível**:

$$
1{,}5 \times 0{,}3 = 0{,}45.
$$

Mas isso não demonstra que a faixa intermediária nunca exista nos parâmetros atuais. Pela formulação do manuscrito, o canal de perigo tem memória e decai. Partindo de $h=0{,}45$, um passo de decaimento com $\lambda=0{,}85$ produz:

$$
h=0{,}3825.
$$

Nesse estado, ele continua acima de $\varepsilon=0{,}001$, portanto pode continuar governando o campo, mas está abaixo do limiar de entrada de $0{,}45$. **Essa condição pode surgir após a perda de observação do perigo, sem alterar o limiar de modalidade.** A ordem de atualização e o estado corrente do FSM precisam ser verificados.

Além disso, o manuscrito condiciona a retirada à disponibilidade de uma pose, ao período refratário e à habilitação do comportamento. Assim, “perigo elegível já dispara a retirada no mesmo instante” é uma afirmação mais forte do que a formulação permite.

Eu substituiria esse trecho por:

> Nos parâmetros atuais, um perigo recém-incorporado na intensidade mínima elegível atinge o limiar nominal de retirada. A ocorrência efetiva da transição depende das condições do FSM; após decaimento, o canal de perigo pode permanecer dominante abaixo desse limiar.

Isso não exige uma nova bateria: **inclua a perda de observação e o decaimento no ensaio marginal já planejado**.

Também evitaria afirmar antecipadamente que “o robô nem inspeciona nem recua”. Ele pode continuar a patrulha ou outro comportamento. O resultado a investigar é **supressão da investigação sem disparo de nova retirada**, não necessariamente imobilidade.

## 2. A análise das exclusões melhorou, mas “não enviesa RHM × APF” ainda não está demonstrado

O fato de ambos passarem de 2,7 para 3,0 mostra que **a diferença entre suas médias de inspeção permanece igual nesse resumo específico**. Não demonstra ausência de viés em tempo, distância, segurança ou outras propriedades das execuções excluídas.

Eu usaria:

> A inclusão das falhas de partida não altera a diferença observada entre as médias de inspeção de RHM e APF, mas modifica as estimativas absolutas de completude. Não se pressupõe independência entre falha de inicialização e configuração.

A proposta de reportar resultados com e sem exclusões é boa. Distinga explicitamente:

- **desempenho por tentativa de missão**, incluindo falhas de partida;
- **desempenho condicionado à inicialização bem-sucedida**.

Para segurança, uma execução em que o robô não se moveu não deve aumentar artificialmente a evidência de navegação sem contato.

Os limites de **25,9%, 28,3% e 31,2%** estão corretos para zero ocorrências em, respectivamente, dez, nove e oito execuções, sob o modelo binomial adotado. **Aplique-os apenas às configurações que realmente tiveram zero contatos**; isso precisa ser conferido especialmente nos controles destinados a evidenciar falhas de segurança.

## 3. TOST não precisa virar uma nova obrigação para KOF

Foi correto abandonar “KOF empata com RHM”. Entretanto, a solução não precisa ser automaticamente acrescentar um teste de equivalência.

Se a pergunta principal for se o *keepout* reproduz o benefício observado de segurança, apresente os contrastes, os intervalos e as limitações. **Se quiser afirmar equivalência**, aí sim é preciso especificar:

- em qual medida de segurança;
- qual diferença seria operacionalmente desprezível;
- qual margem corresponde a essa diferença.

A margem de **±5 segundos**, usada anteriormente para tempo, não se transfere para *clearance* ou TTC. E dez execuções podem produzir uma conclusão inconclusiva, mesmo quando as estimativas forem próximas.

## 4. Os pares de histerese ainda não separam completamente limiar e largura

A comparação:

- $(0{,}45,\ 0{,}25)$: largura $0{,}20$;
- $(0{,}55,\ 0{,}25)$: largura $0{,}30$;

altera simultaneamente o limiar de entrada e a largura.

Se a intenção for avaliar **largura versus posição da faixa**, uma opção mais clara, mantendo três condições, seria:

| Condição | Entrada | Saída | Largura |
|---|---:|---:|---:|
| Referência | 0,45 | 0,25 | 0,20 |
| Faixa mais estreita, entrada fixa | 0,45 | 0,35 | 0,10 |
| Faixa deslocada, largura fixa | 0,55 | 0,35 | 0,20 |

Isso não transforma o estudo em um experimento fatorial completo, mas deixa os contrastes mais interpretáveis **sem acrescentar configurações**.

## 5. Eu retiraria também o ponto fixo descritivo opcional

O exemplo de um estado com auto-laço foi útil para detectar o erro do lema. Ele não caracteriza automaticamente a tabela do sistema real.

A expressão:

$$
Q^*=\frac{r+\eta\Phi/\alpha}{1-\gamma}
$$

pressupõe aquele caso simplificado, com recompensa e campo constantes. O resultado $20+100\Phi$ ainda pressupõe $r=1$. Não permite concluir que toda a tabela seja “essencialmente um acumulador de Φ reescalado”.

**As diferenças em Q não explicam a ausência de diferenças comportamentais. A explicação é estrutural: Q não seleciona as ações executadas.** Essa frase já resolve o ponto com mais precisão.

Portanto, minha resposta à decisão 3 do plano é: **deixar esse desenvolvimento de fora**.

## 6. A verificação do resíduo deve ocorrer antes de decidir o destino da Figura 7

A suspeita levantada pela auditoria merece investigação. Verifique, no mesmo passo e no mesmo par estado–ação:

$$
Q_{\text{depois}}-Q_{\text{antes}}
\quad\text{e}\quad
\alpha\delta+\eta\Phi.
$$

Confira também se o campo registrado é aquele efetivamente usado na atualização e se a coluna representa valor assinado, módulo ou agregação.

**Igualdade entre magnitudes, isoladamente, não prova que $\Phi=0$**. E séries parecidas entre diferentes valores de $\eta$ não distinguem, sozinhas, ausência de campo, efeito transitório ou problema de instrumentação.

Se for apenas efeito da janela final, explique. Se houver erro de registro, corrija-o e identifique quais resultados precisam ser recalculados. **Mover a figura para o apêndice não substitui resolver essa dúvida.** Pelo reposicionamento editorial, ela pode ir para o apêndice independentemente de as curvas serem semelhantes.

## Cuidados finais para fechar o protocolo

Há ainda três cuidados pequenos para fechar o protocolo:

- **HEU-sel:** confirme que trocar o alvo selecionado não altera indiretamente a magnitude do campo usada no disparo. Se isso ocorrer, documente essa consequência; não descreva o contraste como alteração apenas da ordem de atendimento.
- **Métrica de prioridade:** maior intensidade verdadeira é uma candidata, mas sua relação com prioridade operacional precisa ser justificada, sobretudo entre modalidades distintas. Defina também como tratar um alvo que nunca é inspecionado.
- **Reavaliação da confirmação:** se `robot_dist_m` é registrado no encerramento, descreva-o como distância ao alvo **no encerramento da investigação**, não como distância mínima de toda a aproximação.

**Minha decisão sobre a v2: favorável à execução após esses ajustes.** Não vejo necessidade de ampliar novamente o escopo. O trabalho agora é fechar o protocolo, manter as comparações interpretáveis e resolver a dúvida de instrumentação do resíduo.

E, na redação, chamaria o documento de **plano de análise definido antes das novas execuções**. Caso não haja registro formal, “pré-registro” pode sugerir um procedimento que ainda não foi realizado. As análises sobre dados antigos continuam sendo retrospectivas, mesmo que sua reanálise seja planejada agora.

