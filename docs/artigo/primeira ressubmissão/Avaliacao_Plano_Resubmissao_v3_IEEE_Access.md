# Avaliação do plano de ressubmissão — versão 3

**Manuscrito:** Access-2026-46291 — IEEE Access  
**Documento avaliado:** PLANO_RESUBMISSAO(2).md  
**Data:** 13 de outubro de 2026

## Parecer

**A versão 3 é uma base adequada para executar a revisão. Não recomendo outra reestruturação do plano nem ampliar a bateria experimental por padrão.** As pendências remanescentes são de definição operacional, apresentação dos resultados e fechamento do protocolo.

Esta avaliação considera o documento e as informações da auditoria relatadas nele. **Não constitui uma auditoria independente do código, dos logs ou dos dados brutos.** Os itens descritos como “verificados” no plano permanecem resultados da auditoria dos autores.

## 1. O que considero resolvido

| Pendência anterior | Situação na v3 |
|---|---|
| Bellman/RL como contribuição central sem controlar o robô | Reposicionamento consistente, sem tentar compensá-lo com novas alegações teóricas. |
| Lema e extrapolação do ponto fixo | Retirados. |
| Inclusão de QD/QD0 | Retirada do escopo desta ressubmissão. |
| Comparação entre cenários diferentes | Painéis separados. |
| Equivalência presumida entre KOF e RHM | Substituída por contrastes e intervalos; TOST condicionado a margem justificada. |
| Execução de cenários adicionais condicionada ao resultado inicial | Substituída por plano de análise anterior às novas execuções. |
| Perigo marginal e memória do campo | Decaimento e perda de observação incorporados ao ensaio. |
| Exclusões e denominadores | Separação entre desempenho por tentativa e condicionado à partida. |
| Dúvida sobre o resíduo | Tratada como verificação de instrumentação, antes da decisão editorial sobre a figura. |
| Acoplamento de HEU-sel | Explicitados a alteração na seleção e seus efeitos posteriores sobre o campo. |

O documento agora faz uma distinção útil entre **o que o sistema executa, o que cada componente explica e o que os instrumentos medem**.

## 2. A distinção entre os dois raios é importante, mas “contato efetivo” precisa ser corrigido

A descoberta relatada sobre os raios de 0,5 m e 2,0 m melhora a interpretação dos resultados. Porém, a tabela chama o raio de 0,5 m de “contato efetivo”.

**Um contador baseado em distância não comprova, por si só, contato físico.** Se a variável é calculada por entrada em uma região geométrica, a descrição adequada é:

> Entrada na região de contato definida operacionalmente por raio de 0,5 m.

“Colisão física detectada” só seria uma descrição adequada se o instrumento utilizasse efetivamente contatos do simulador, geometria de colisão ou outro mecanismo correspondente.

A distinção vale também para os limites binomiais: eles se referem à **probabilidade por execução do evento operacionalmente contado**, nas condições estudadas. Não representam um limite geral para qualquer falha de segurança, colisão física ou operação em uma subestação real.

Quanto aos 2,0 m:

- se forem um requisito mínimo definido pelo estudo, 1,71 m representa descumprimento desse requisito, embora haja melhora sobre a referência;
- se forem um limiar diagnóstico para medir exposição, descreva-os como tal;
- não apresente nenhum desses valores como distância regulamentar de segurança elétrica sem fundamentação específica.

Uma redação possível para a discussão, condicionada à confirmação dos números, seria:

> No cenário com perigo na rota, o sistema completo aumentou a distância mínima de aproximadamente 0,71 m para 1,71 m. Ainda ocorreram incursões abaixo do limiar de 2,0 m adotado na avaliação, embora não tenham sido registradas entradas na região de contato definida por raio de 0,5 m.

Essa apresentação preserva o ganho observado e explicita seu alcance. Não exige novo experimento.

## 3. A distância no encerramento já é uma medida física válida

**Eu não tornaria obrigatória a repetição de E3/N2 apenas para registrar a distância mínima.**

A ressalva da avaliação anterior era sobre o nome e a interpretação da variável: distância no encerramento não é distância mínima. Isso **não torna a medida existente desprovida de significado físico**.

A distância ao alvo verdadeiro no encerramento da investigação permite examinar:

- quão perto o robô estava ao finalizar a ação;
- como essa distância varia entre ausência de ruído e níveis de ruído;
- quantos resultados mudam de classificação quando o limiar de confirmação é alterado.

Portanto, a afirmação da v3 de que o re-scoring “não dá a qualidade física da aproximação” é excessiva. Ele fornece informação física sobre o **ponto de encerramento**, embora não descreva toda a trajetória.

Além disso, uma distância mínima pequena, atingida apenas momentaneamente, não comprova que uma inspeção tenha sido realizada adequadamente.

**Recomendação:** executar primeiro a análise retrospectiva de E3/N1/N2 com a variável disponível. Manter a medição de distância mínima como opcional, acionada apenas se surgir uma dúvida que essa análise não consiga resolver. Se já houver trajetórias ou registros de posição suficientes, verificar a possibilidade de reconstrução antes de repetir execuções.

Isso pode preservar as aproximadamente 150 min previstas para o bloco opcional, sem deixar de responder à sensibilidade do critério solicitada pelo revisor.

## 4. A matriz está definida, mas falta explicitar quais execuções serão reutilizadas

O plano determina comparar método, HEU e HEU-sel nos três cenários. O orçamento, entretanto, contabiliza os dois novos comparadores, sem uma linha explícita para o método original.

**Isso é aceitável se os resultados existentes forem reutilizáveis.** Basta declarar essa decisão e sua justificativa antes da execução.

Acrescente ao protocolo uma tabela curta:

| Comparação | Dados do método original | Dados novos | Condição de comparabilidade |
|---|---|---|---|
| Método × HEU × HEU-sel, por cenário | Reutilizados ou repetidos, explicitamente identificados | HEU e HEU-sel | Mesmas definições de cenário, parâmetros comuns, métricas e condições relevantes. |
| RHM/RHB/KOa/KOb × KOF | Identificar os grupos existentes | KOF | Mesmo cenário de perigo na rota e mesma definição dos instrumentos. |
| Sensibilidades | Identificar a referência | Variantes previstas | Alterações deliberadas documentadas. |

Registre a versão do código e as mudanças introduzidas. Se forem apenas parâmetros novos, modos alternativos e instrumentação sem efeito comportamental, a reutilização pode ser justificável. Se a correção do resíduo revelar uma alteração no comportamento ou na métrica comparada, determine especificamente quais grupos ficaram incompatíveis.

Não é necessário repetir toda a bateria por rotina. É necessário impedir que uma diferença entre versões de implementação seja confundida com efeito do método.

## 5. A métrica de prioridade e o tratamento das não inspeções precisam de uma decisão final

A opção de comparar intensidade verdadeira **dentro da mesma modalidade** evita parte do problema de comparar escalas distintas. Ainda assim, defina explicitamente:

- como o evento prioritário é identificado, independentemente da decisão tomada pelo controlador;
- como resolver empates;
- a partir de qual instante o tempo é contado;
- qual orçamento temporal será usado;
- como serão apresentados os eventos não inspecionados.

Se a escolha for atribuir o teto do orçamento a eventos nunca inspecionados, não apresente esse número como tempo observado de inspeção.

Uma formulação operacional clara é:

> Tempo limitado ao horizonte H: utiliza-se o instante da inspeção quando ela ocorre até H; caso contrário, atribui-se H ao escore e registra-se separadamente que não houve inspeção até o horizonte.

Relate junto a proporção de eventos inspecionados até H. Assim, um evento inspecionado exatamente no limite não fica indistinguível de outro que jamais foi inspecionado.

Não é necessário adicionar uma análise estatística complexa para resolver isso. O essencial é definir e nomear o resultado corretamente antes das novas execuções.

## 6. Pequenas precisões de redação e ensaio

- **Tabela do decaimento:** trocar “dispara retirada” por “atinge o limiar nominal de entrada”. A transição efetiva depende das condições do FSM já reconhecidas no plano.
- **Supressão por aproximadamente 38 s:** apresentar como duração calculada para o exemplo de h inicial igual a 0,45, decaimento de 0,85 por período de 1 s e ausência de renovação ou reinicialização. Não é uma duração universal de supressão.
- **Papel de ε:** embora implementado como tolerância numérica, ele também determina quando a memória do perigo deixa de dominar o campo. O limiar de modalidade controla a entrada de novos eventos; ε participa do encerramento da precedência durante o decaimento.
- **Ensaio em d = R:** garantir cruzamentos efetivos de dentro para fora e de fora para dentro. Uma trajetória estritamente tangente pode apenas tocar a fronteira e não testar a descontinuidade que se pretende observar.
- **Diagnóstico inicial:** substituir “o único item que exige descoberta nova” por “o principal contraste experimental ainda ausente”. As sensibilidades e a verificação do resíduo também podem produzir resultados relevantes.
- **Título de subseção:** substituir o remanescente “Cenários pré-registrados” por “Cenários definidos no plano de análise”.
- **Estimativa de duração:** as linhas obrigatórias somam 1.015 min, ou 16 h 55 min; com o bloco opcional de 150 min, 19 h 25 min. As aproximações do plano estão coerentes, antes de considerar eventuais repetições identificadas na verificação dos instrumentos.

Essas precisões não exigem outra reformulação do projeto.

## Recomendação de execução

**Parecer favorável à execução da v3, após fechar as definições operacionais acima.**

A sequência recomendada é:

1. Verificar a instrumentação do resíduo e delimitar os resultados eventualmente afetados.
2. Confirmar os instrumentos geométricos de segurança e o funcionamento isolado de KOF.
3. Fechar a métrica de prioridade, o horizonte temporal, os contrastes e a reutilização de dados.
4. Executar a matriz planejada de HEU, HEU-sel e sensibilidades.
5. Fazer a reavaliação retrospectiva da confirmação e das exclusões.
6. Reescrever o manuscrito e a resposta aos revisores a partir dos resultados obtidos.

**Não acrescentaria novas configurações nesta etapa.** A prioridade passou de redesenhar o plano para executá-lo com definições estáveis, preservar a rastreabilidade dos dados e limitar as conclusões ao que cada comparação demonstra.

