# Auditoria de atribuições técnicas

Registro de conferência afirmação por afirmação para as passagens que sustentam a
lacuna declarada e a comparação entre mecanismos de supervisão. Última revisão:
14/11/2026.

**Escopo.** Este registro cobre as atribuições que sustentam a lacuna e a comparação
entre mecanismos, e as corrigidas em 13 e 14/11/2026. **Não** é uma certificação das
146 entradas da bibliografia. Conferir DOI, autoria e título não valida frases sobre
algoritmo, ambiente experimental, garantia ou resultado — foi justamente essa a
distinção que as correções abaixo exigiram.

| Afirmação da tese (onde) | O que a fonte sustenta | Interpretação adotada | Estado |
|---|---|---|---|
| Navegação baseada em mapas combina RL com SLAM (§2.2.4) | `Tai2017` é *"continuous control of mobile robots for **mapless** navigation"* — navegação **sem** mapa | A fonte não sustenta a afirmação: é a categoria oposta. Citação retirada do item e passada ao item reativo, onde descreve corretamente o trabalho | **corrigido** 14/11 |
| `Tai2017` demonstrou DQN para navegação com laser (§3.1.1) | Controle **contínuo** treinado por DDPG assíncrono; DQN opera sobre ações discretas | Trocado para DDPG assíncrono e navegação sem mapa, com transferência simulador→real | **corrigido** 14/11 |
| `Zhu2017` expandiu `Tai2017` (§3.1.1) e `Tai2017` expandiu `Zhu2017` (§3.4) | Ambos de 2017; o artigo de Tai discute Zhu como trabalho relacionado, não como base | Genealogia não demonstrável, e afirmada nos dois sentidos em seções diferentes. Substituída por comparação factual da entrada sensorial | **corrigido** 14/11 |
| `Thananjeyan2021` usa funções de barreira para garantir permanência em conjunto seguro (§3.1.3) | Título: *"Recovery RL: safe RL with **learned recovery zones**"*. Mecanismo: crítico de segurança **aprendido** + políticas de tarefa e de recuperação | Nenhuma garantia de invariância é oferecida pela fonte, e os ensaios não são de navegação industrial. Reescrito como salvaguarda aprendida e probabilística | **corrigido** 14/11 |
| RoboTHOR expandiu o ManipulaTHOR (§3.4.2) | `Deitke2020RoboTHOR` é de **2020**; `Ehsani2021` (ManipulaTHOR) é de **2021** | Sequência cronologicamente impossível. Reescrito como extensões irmãs da mesma plataforma, em eixos distintos (transferência e manipulação) | **corrigido** 14/11 |
| `Brooks1986` não tem persistência temporal explícita (Tabela 2) | Subsunção usa máquinas de estado **aumentadas**, com estado interno e **constantes de tempo** na supressão e na inibição | Ausência de acumulador com decaimento não é ausência de persistência temporal. A coluna passou a nomear o mecanismo específico; a célula passou a "outro mecanismo", nomeando-o | **corrigido** 14/11 |
| `Arkin1989,Arkin1998` sem acumulador com decaimento (Tabela 2) | A soma vetorial de esquemas motores é função das percepções do instante | "Não possui" é defensável para o esquema motor, e a célula passou a dizer por quê | conferido |
| Campos potenciais sem acumulador com decaimento (Tabela 2) | O campo é função da configuração corrente de obstáculos | "Não possui" é defensável, e a célula passou a dizer por quê | conferido |
| `Bonasso1997` tem temporizadores do sequenciador (Tabela 2) | O sequenciador reativo interpõe-se entre planejador e habilidades, com temporização própria | Mantido: a célula já nomeava o mecanismo em vez de negar persistência | conferido |
| Políticas aprendidas fim a fim: persistência implícita no estado ou no modelo (Tabela 2) | Em `Zhu2017`, `Tai2017`, `Kahn2021` a arbitragem não é módulo separável | Mantido, e a legenda passou a declarar que agrupar na mesma linha não iguala os trabalhos em todos os atributos | conferido |
| `Wijayathunga et al.`, `Ou et al.` — autoria | Conferida na rodada 01 | Corrigida | corrigido 13/11 |
| Referência truncada | Retirada na rodada 01 | — | corrigido 13/11 |
| Aplicação bem-sucedida de RL à inspeção de subestações (§2.2.4) | Referência anterior não localizada em nenhuma base | Alegação retirada | corrigido 13/11 |

## Pendências deste registro

1. As 146 entradas **não** foram certificadas individualmente. O que este registro
   cobre é o conjunto de atribuições que sustentam a lacuna e a comparação entre
   mecanismos, mais as já sinalizadas.
2. As duas correções relativas a `Tai2017` haviam sido sinalizadas na rodada 01 e não
   chegaram ao PDF daquela rodada. Não são exigências novas; são correções atrasadas.
