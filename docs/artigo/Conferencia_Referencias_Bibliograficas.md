# Conferência das referências bibliográficas

**Arquivo examinado:** `references.bib`  
**Data da verificação:** 12 de setembro de 2026  
**Resultado:** **as 21 referências correspondem a trabalhos reais. Não identifiquei referência fictícia nem DOI informado que corresponda a outro trabalho.**

Há uma correção de classificação bibliográfica, duas entradas com paginação incompleta e oportunidades de completar identificadores. Os dois trabalhos citados como preprints também têm versões publicadas em anais de congressos.

## 1. Escopo e método

Examinei diretamente as 21 entradas do `.bib`, sem utilizar o PDF do manuscrito. Comparei título, autoria, ano, veículo, volume, número, páginas ou identificador de artigo e DOI, conforme aplicável.

Consultei os metadados depositados pelos editores no Crossref, páginas editoriais, registros do arXiv e fontes institucionais. Para os 16 artigos e trabalhos de congresso que não estavam citados como preprints, obtive registros individuais do Crossref. Também localizei os registros das versões publicadas dos dois preprints. As fontes de cada entrada estão indicadas abaixo; os links DOI identificam as respectivas publicações.

A confirmação de existência não significa que cada trabalho sustente todas as afirmações associadas a ele no manuscrito. Essa correspondência exigiria examinar os trechos citantes e o conteúdo das fontes. Também não fiz uma investigação específica de retratações, integridade editorial ou qualidade científica das publicações.

| Item verificado | Resultado |
|---|---:|
| Entradas no arquivo | 21 |
| Trabalhos com existência confirmada | 21 |
| Trabalhos não localizados | 0 |
| DOIs já presentes no arquivo | 7 |
| DOIs presentes que correspondem ao trabalho citado | 7 de 7 |
| DOIs adicionais localizados para as versões já citadas de artigos/congressos | 9 |
| Entradas de congresso classificadas incorretamente como periódico | 1 |
| Entradas de congresso sem páginas, recuperadas nesta conferência | 2 |
| Entradas citadas pelo arXiv com versão publicada localizada | 2 |

As categorias de correção e complementação podem se sobrepor.

## 2. Resultado individual

| Chave BibTeX | Publicação confirmada | Resultado e ação |
|---|---|---|
| `suttonbarto2018` | Richard S. Sutton e Andrew G. Barto, *Reinforcement Learning: An Introduction*, 2ª ed., MIT Press, 2018. [MIT Press](https://mitpress.mit.edu/9780262039246/reinforcement-learning/) | **Confirmada.** Autores, edição, editora e ano compatíveis. ISBN da edição de capa dura: `9780262039246`, caso deseje acrescentá-lo. |
| `bellman1957` | Richard Bellman, *Dynamic Programming*, Princeton University Press, 1957. [Registro institucional da University of Texas](https://www.cs.utexas.edu/~shivaram/readings/b2hd-Bellman1957.html); [fac-símile da edição original](https://gwern.net/doc/statistics/decision/1957-bellman-dynamicprogramming.pdf) | **Confirmada.** Manter a associação Princeton/1957. Não substituir a editora por Dover mantendo o ano da edição original. |
| `ng1999` | Andrew Y. Ng, Daishi Harada e Stuart Russell, *Policy Invariance Under Reward Transformations: Theory and Application to Reward Shaping*, ICML 1999, pp. 278–287. [Publicações do coautor](https://people.eecs.berkeley.edu/~russell/publications.html); [registro ACM](https://dl.acm.org/doi/10.5555/645528.657613) | **Confirmada.** Título, autores, evento, páginas e ano compatíveis. Pode acrescentar `publisher = {Morgan Kaufmann}`. A ausência de DOI não invalida a referência. |
| `khatib1986` | Oussama Khatib, *Real-Time Obstacle Avoidance for Manipulators and Mobile Robots*, *The International Journal of Robotics Research*, 5(1), 90–98, 1986. [DOI](https://doi.org/10.1177/027836498600500106) | **Confirmada.** Dados compatíveis; acrescentar DOI. As páginas `90--98` do arquivo estão corretas. |
| `koren1991` | Yoram Koren e Johann Borenstein, *Potential Field Methods and Their Inherent Limitations for Mobile Robot Navigation*, IEEE ICRA 1991, pp. 1398–1404. [DOI](https://doi.org/10.1109/ROBOT.1991.131810) | **Confirmada, com correção necessária no tipo.** Usar `@inproceedings` e `booktitle`, em lugar de `@article` e `journal`. Acrescentar DOI. |
| `fox1997` | Dieter Fox, Wolfram Burgard e Sebastian Thrun, *The Dynamic Window Approach to Collision Avoidance*, *IEEE Robotics & Automation Magazine*, 4(1), 23–33, 1997. [DOI](https://doi.org/10.1109/100.580977) | **Confirmada.** Dados compatíveis; acrescentar DOI. |
| `macenski2020nav2` | Steve Macenski, Francisco Martín, Ruffin White e Jonatan Ginés Clavero, *The Marathon 2: A Navigation System*, IROS 2020, pp. 2718–2725. [DOI](https://doi.org/10.1109/IROS45743.2020.9341207); [registro dos autores no arXiv](https://arxiv.org/abs/2003.00368) | **Confirmada, mas incompleta.** Acrescentar páginas e DOI. Os quatro autores correspondem ao trabalho. |
| `williams2017mppi` | Grady Williams, Andrew Aldrich e Evangelos A. Theodorou, *Model Predictive Path Integral Control: From Theory to Parallel Computation*, *Journal of Guidance, Control, and Dynamics*, 40(2), 344–357, 2017. [DOI](https://doi.org/10.2514/1.G001921) | **Confirmada.** Dados compatíveis; acrescentar DOI. |
| `bajcsy1988` | Ruzena Bajcsy, *Active Perception*, *Proceedings of the IEEE*, 76(8), 966–1005, 1988. [DOI](https://doi.org/10.1109/5.5968) | **Confirmada.** É artigo de periódico, apesar de “Proceedings” integrar o nome da revista. Manter `@article`; acrescentar DOI. |
| `breazeal2003` | Cynthia Breazeal, *Emotion and Sociable Humanoid Robots*, *International Journal of Human-Computer Studies*, 59(1–2), 119–155, 2003. [DOI](https://doi.org/10.1016/S1071-5819(03)00018-1) | **Confirmada.** Dados compatíveis; acrescentar DOI. |
| `zhang2025substation` | Hongwei Zhang, Lijun Sun, Weihong Tan, Siyu Bao, Xing He e Jinguo Chen, *A Substation Robot Path Planning Algorithm Based on Deep Reinforcement Learning Enhanced by Ant Colony Optimization*, *Frontiers in Robotics and AI*, 12, artigo 1759501, 2026. [Página editorial](https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2025.1759501/full) | **Confirmada.** Manter `year = {2026}` e volume 12. O segmento `2025` do DOI não torna o ano 2026 incorreto. Acrescentar DOI. |
| `li2024state` | Li Li, Ke Xu, Fei Ye, Zhichao Liu, Yanhong Liu e Hao Hu, *State of the Art and Development Trends for Inspection Robots Applied in Substations*, ICCIR 2024, pp. 44–48. [ACM](https://dl.acm.org/doi/10.1145/3687488.3687496) | **Confirmada.** Os seis autores, evento, ano e páginas correspondem. Acrescentar DOI. |
| `zhang2023apf` | Dengyu Zhang, Guobin Zhu e Qingrui Zhang, *Multi-Robot Motion Planning: A Learning-Based Artificial Potential Field Solution*, arXiv:2306.07647, 2023. [arXiv](https://arxiv.org/abs/2306.07647) | **Confirmada como preprint.** Autores, título, identificador e ano corretos. Existe versão publicada no CFASTA 2023, pp. 233–238. [DOI da versão publicada](https://doi.org/10.1109/CFASTA57821.2023.10243195) |
| `zhang2020reward` | Daniel Zhang e Colleen P. Bailey, *Obstacle Avoidance and Navigation Utilizing Reinforcement Learning with Reward Shaping*, arXiv:2003.12863, 2020. [arXiv](https://arxiv.org/abs/2003.12863) | **Confirmada como preprint.** Existe versão publicada em *Proceedings of SPIE*, vol. 11413, artigo 114131H, 2020. [DOI da versão publicada](https://doi.org/10.1117/12.2558212) |
| `brunke2022safe` | Lukas Brunke e seis coautores, *Safe Learning in Robotics: From Learning-Based Control to Safe Reinforcement Learning*, *Annual Review of Control, Robotics, and Autonomous Systems*, 5, 411–444, 2022. [DOI](https://doi.org/10.1146/annurev-control-042920-020211) | **Confirmada.** Os sete autores, título, volume, páginas, ano e DOI correspondem. O registro também informa número 1, cuja inclusão é opcional. |
| `substationpp2024review` | Jianhua Zheng, Tong Chen, Jiahong He, Zhunian Wang e Bingtuan Gao, *Review on Security Range Perception Methods and Path-Planning Techniques for Substation Mobile Robots*, *Energies*, 17(16), artigo 4106, 2024. [DOI](https://doi.org/10.3390/en17164106) | **Confirmada.** Autores e demais metadados correspondem, inclusive DOI. |
| `ipp2024nonconvex` | Mobolaji Orisatoki, Weihua Sheng, Ebubekir Pinar, Ali Rasoulzadeh, Mahdi Amouzadi e Arash M. Dizqah, *Informative Path Planning for Autonomous Mapping of Unknown Non-Convex Environments: Design, Benchmarking, and Validation*, *Information*, 17(5), artigo 457, 2026. [DOI](https://doi.org/10.3390/info17050457) | **Confirmada.** Os seis autores e todos os dados centrais correspondem. Manter 2026; o `2024` na chave é apenas um identificador interno. |
| `substation2025segnav` | Changqing Cai, Yongkang Yang, Kaiqiao Tian, Yuxin Yan, Kazuyuki Kobayashi e Ka C. Cheok, *Attention-Enhanced Semantic Segmentation for Substation Inspection Robot Navigation*, *Sensors*, 25(19), artigo 6252, 2025. [DOI](https://doi.org/10.3390/s25196252) | **Confirmada.** Autores, título, ano, volume, número, identificador e DOI correspondem. |
| `substation2024uhvdl` | Zhao-lei Wang, Rong Meng e Zhi-long Zhao, *Autonomous Inspection Method of UHV Substation Robot Based on Deep Learning in Cloud Computing Environment*, *Journal of Circuits, Systems and Computers*, 33(5), artigo 2450088, 2024. [DOI](https://doi.org/10.1142/S0218126624500889) | **Confirmada.** Manter 2024 para a edição do periódico. A publicação antecipada on-line ocorreu em 2023. |
| `drlrobotics2024survey` | Chen Tang, Ben Abbatematteo, Jiaheng Hu, Rohan Chandra, Roberto Martín-Martín e Peter Stone, *Deep Reinforcement Learning for Robotics: A Survey of Real-World Successes*, *Annual Review of Control, Robotics, and Autonomous Systems*, 8, 153–188, 2025. [Editora](https://www.annualreviews.org/content/journals/10.1146/annurev-control-030323-022510) | **Confirmada.** Os seis autores e demais dados correspondem. Manter 2025 para a versão no volume 8. |
| `hybrid2015delibreact` | Elvis Ruiz, Raul Acuna, Pedro Velez e Gerardo Fernandez-Lopez, *Hybrid Deliberative Reactive Navigation System for Mobile Robots Using ROS and Fuzzy Logic Control*, LARS-SBR 2015, pp. 67–72. [DOI](https://doi.org/10.1109/LARS-SBR.2015.24) | **Confirmada, mas incompleta.** Autores, evento, título, ano e DOI correspondem. Acrescentar páginas. |

## 3. Correção efetiva: Koren e Borenstein

O trabalho é uma publicação em anais de congresso. Seu cadastro como `@article` com o evento no campo `journal` é a inconsistência objetiva encontrada no arquivo. Não é uma referência inexistente. O registro editorial a classifica como `proceedings-article`. [Metadados Crossref](https://api.crossref.org/works/10.1109/ROBOT.1991.131810)

Substituição sugerida, preservando a chave usada no LaTeX:

```bibtex
@inproceedings{koren1991,
  author    = {Koren, Yoram and Borenstein, Johann},
  title     = {Potential Field Methods and Their Inherent Limitations
               for Mobile Robot Navigation},
  booktitle = {Proceedings of the 1991 IEEE International Conference
               on Robotics and Automation},
  pages     = {1398--1404},
  year      = {1991},
  publisher = {IEEE},
  doi       = {10.1109/ROBOT.1991.131810}
}
```

## 4. Campos que podem ser completados

### 4.1. Páginas ausentes

| Chave | Campo a acrescentar | Comprovação |
|---|---|---|
| `macenski2020nav2` | `pages = {2718--2725},` | [Crossref](https://api.crossref.org/works/10.1109/IROS45743.2020.9341207) |
| `hybrid2015delibreact` | `pages = {67--72},` | [Crossref](https://api.crossref.org/works/10.1109/LARS-SBR.2015.24) |

### 4.2. Nove DOIs ausentes, confirmados para as versões já citadas

| Chave | Valor do campo `doi` |
|---|---|
| `khatib1986` | [10.1177/027836498600500106](https://doi.org/10.1177/027836498600500106) |
| `koren1991` | [10.1109/ROBOT.1991.131810](https://doi.org/10.1109/ROBOT.1991.131810) |
| `fox1997` | [10.1109/100.580977](https://doi.org/10.1109/100.580977) |
| `macenski2020nav2` | [10.1109/IROS45743.2020.9341207](https://doi.org/10.1109/IROS45743.2020.9341207) |
| `williams2017mppi` | [10.2514/1.G001921](https://doi.org/10.2514/1.G001921) |
| `bajcsy1988` | [10.1109/5.5968](https://doi.org/10.1109/5.5968) |
| `breazeal2003` | [10.1016/S1071-5819(03)00018-1](https://doi.org/10.1016/S1071-5819(03)00018-1) |
| `zhang2025substation` | [10.3389/frobt.2025.1759501](https://doi.org/10.3389/frobt.2025.1759501) |
| `li2024state` | [10.1145/3687488.3687496](https://doi.org/10.1145/3687488.3687496) |

Exemplo de preenchimento: `doi = {10.1109/100.580977}`. A ausência desses campos é uma lacuna de identificação, não indício de referência falsa.

## 5. Duas referências podem apontar para versões publicadas

Os registros atuais de arXiv são reais e estão corretamente identificados. Recomendo considerar as versões publicadas se forem as versões que sustentam as passagens citadas. Não se deve simplesmente colocar um DOI de congresso dentro de uma entrada que continua descrevendo somente o preprint.

### 5.1. Zhang, Zhu e Zhang, 2023

O mesmo título e os mesmos três autores constam dos anais do CFASTA 2023, páginas 233–238. [Registro publicado](https://doi.org/10.1109/CFASTA57821.2023.10243195)

```bibtex
@inproceedings{zhang2023apf,
  author    = {Zhang, Dengyu and Zhu, Guobin and Zhang, Qingrui},
  title     = {Multi-Robot Motion Planning: A Learning-Based
               Artificial Potential Field Solution},
  booktitle = {2023 2nd Conference on Fully Actuated System Theory
               and Applications (CFASTA)},
  pages     = {233--238},
  year      = {2023},
  publisher = {IEEE},
  doi       = {10.1109/CFASTA57821.2023.10243195}
}
```

Se mantiver a referência ao preprint, pode completar `url = {https://arxiv.org/abs/2306.07647}` e `doi = {10.48550/arXiv.2306.07647}`. Esse DOI identifica o preprint, e não os anais. [arXiv](https://arxiv.org/abs/2306.07647)

### 5.2. Zhang e Bailey, 2020

Há uma versão nos anais *Artificial Intelligence and Machine Learning for Multi-Domain Operations Applications II*, *Proceedings of SPIE*, volume 11413, artigo 114131H, DOI `10.1117/12.2558212`. A página institucional da coautora também informa o intervalo 500–506. [SPIE](https://www.spiedigitallibrary.org/conference-proceedings-of-spie/11413/114131H/Obstacle-avoidance-and-navigation-utilizing-reinforcement-learning-with-reward-shaping/10.1117/12.2558212.short); [University of North Texas](https://facultyinfo.unt.edu/faculty-profile?profile=cpb0096)

```bibtex
@inproceedings{zhang2020reward,
  author    = {Zhang, Daniel and Bailey, Colleen P.},
  title     = {Obstacle Avoidance and Navigation Utilizing
               Reinforcement Learning with Reward Shaping},
  booktitle = {Artificial Intelligence and Machine Learning
               for Multi-Domain Operations Applications II},
  series    = {Proceedings of SPIE},
  volume    = {11413},
  pages     = {500--506},
  year      = {2020},
  publisher = {SPIE},
  doi       = {10.1117/12.2558212}
}
```

**Cuidado com a importação automática:** o registro Crossref recuperado traz `page = 12`, valor que não corresponde ao intervalo informado pela instituição da coautora nem ao identificador 114131H do editor. Por isso, não recomendo copiar esse campo isoladamente. Essa discrepância está no metadado externo; não é erro do seu `.bib`, que cita o arXiv. [Crossref](https://api.crossref.org/works/10.1117/12.2558212)

Se mantiver o preprint, use `url = {https://arxiv.org/abs/2003.12863}` e, opcionalmente, `doi = {10.48550/arXiv.2003.12863}`. [arXiv](https://arxiv.org/abs/2003.12863)

## 6. Anos que parecem estranhos, mas estão corretos

| Entrada | Aparente divergência | Orientação |
|---|---|---|
| `zhang2025substation` | DOI e volume editorial associados a 2025; publicação em 4 de fevereiro de 2026. | **Manter 2026**, como na citação recomendada pelo próprio editor. [Frontiers](https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2025.1759501/full) |
| `ipp2024nonconvex` | A chave contém 2024, mas o artigo é de 2026. | **Manter 2026** no campo `year`. A chave não determina o ano bibliográfico. [Crossref](https://api.crossref.org/works/10.3390/info17050457) |
| `drlrobotics2024survey` | Disponibilização antecipada em 2024; versão no volume 8 publicada em 2025. | **Manter 2025** quando a referência informa volume 8 e páginas 153–188. [Annual Reviews](https://www.annualreviews.org/content/journals/10.1146/annurev-control-030323-022510) |
| `substation2024uhvdl` | Publicação on-line em 26 de outubro de 2023; edição impressa em 30 de março de 2024. | **Manter 2024** para volume 33, número 5. [Crossref](https://api.crossref.org/works/10.1142/S0218126624500889) |

Não é necessário renomear as chaves. Preservá-las evita alterações desnecessárias nos comandos `\cite{...}`.

## 7. Encaminhamento

A lista passou na verificação de existência e identidade bibliográfica. **Não há referência a excluir por inexistência com base nesta conferência.**

Para finalizar a bibliografia, recomendo corrigir a classificação de `koren1991`, completar as duas paginações e os nove DOIs listados e decidir se os dois preprints devem ser substituídos pelas versões publicadas. São ajustes bibliográficos; esta conferência não cria uma nova exigência de experimentos ou de revisão metodológica.

O arquivo `references.bib` recebido foi preservado. Os blocos acima são sugestões de alteração, com as chaves originais mantidas.
