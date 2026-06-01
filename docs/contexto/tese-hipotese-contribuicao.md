---
name: tese-hipotese-contribuicao
description: Hipótese central e enquadramento científico da tese (Bellman atratora / Stay Alert)
metadata: 
  node_type: memory
  type: project
  originSessionId: 7d1d6c52-60a3-4558-a96a-9e0a8903c3c2
---

**Hipótese central da tese (defendida no artigo):** injetar um termo de atração/repulsão Φ(s,a), derivado de eventos sensoriais, DENTRO da própria equação de Bellman — modulando a função de valor em tempo real pela saliência sensorial. O robô "sente" a necessidade de se **aproximar** (Φ>0, ex.: ponto quente, descarga) ou **fugir** (Φ<0, perigo). Isso funde Q-learning/Bellman com a ideia de campos potenciais/"impulsos afetivos". Ver [[tese-simulacao-ambiente]].

**Insight que destrava o conceito (analogia do cão):** um agente puramente reativo só responde a estímulos DENTRO do alcance dos seus sensores; sem estímulo, fica parado ("deitadão"). Um cão detecta um acontecimento e decide aproximar/fugir, mas se o evento está longe dos sensores, ele não reage. Logo, faltava algo ANTES da reação: **levar os sensores até onde os eventos podem estar.** É isso que a **ronda de inspeção** faz — é uma camada de *sensoriamento ativo* (active sensing) que posiciona o robô; a camada reativa (Stay Alert/Bellman atratora) decide aproximar/fugir quando um evento entra no alcance.

**Arquitetura em 2 camadas (decorrência do insight):** (1) ronda deliberativa por waypoints (Nav2) = sensoriamento ativo; (2) resposta afetiva reativa (Φ na Bellman) = aproximar/fugir do evento sensoriado. O "detection_radius" do anomaly_simulator representa o alcance sensorial — coerente com a analogia.

**Suite de sensores idealizada (hardware-alvo, GO2 PRO):** câmera RGB, câmera térmica, microfone omnidirecional, LiDAR, ultrassom, reconhecimento de objetos (visão computacional). **Na simulação, abstrai-se a SAÍDA da cadeia sensor+percepção** como "eventos" (modalidade + intensidade + posição) — não se simulam os sensores crus. É uma simplificação defensável para uma contribuição focada no ALGORITMO.

**Implicações p/ os experimentos (S6):** para defender a hipótese de atração **E** repulsão, os experimentos devem mostrar os dois: aproximar de anomalias (térmica/acústica — melhora inspeção/detecção) E afastar-se de perigos (repulsão/segurança). Hoje o anomaly_simulator só modela atração; falta criar evento(s) de **repulsão** (tópico `/hazard` já existe no bellman_node, sem fonte). 

**Contexto temporal:** tese qualificada em ago/2024 (~10 meses antes de mai/2026); desde então o autor aprofundou no tema e o conceito amadureceu.
