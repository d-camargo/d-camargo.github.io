---
layout: post
title: "Plugin Desire Lines disponível no repositório oficial do QGIS"
lang: pt
translation: /en/2026/05/21/plugin-desire-lines-oficial-qgis.html
category: "Engenharia de Transportes"
image: /assets/images/desire_lines_flow_map.png
---

O plugin Desire Lines agora integra o repositório oficial de complementos do QGIS. A aprovação facilita a instalação direta pelo gerenciador do software, dispensando o download de arquivos externos.

![Mapa de Fluxo com Desire Lines](/assets/images/desire_lines_flow_map.png)

## Atualizações da versão

A inclusão no repositório oficial acompanha melhorias técnicas no plugin:

* **Correção de bugs:** Falhas reportadas na versão inicial foram resolvidas.
* **Estabilidade:** Ajustes internos melhoraram o desempenho na renderização das geometrias de fluxo.

## Funcionalidade: Linhas de desejo

O Desire Lines é voltado para profissionais de mobilidade urbana, logística e análise espacial que trabalham com matrizes de deslocamento. A ferramenta converte dados tabulares em geometrias visuais que conectam pontos de origem e destino.

É importante ressaltar que o plugin gera **linhas retas de desejo (desire lines)**, e não rotas baseadas em malhas viárias. Ele ilustra o volume e a direção do fluxo, indicando a intenção de movimento no território. Essa abstração é útil para análises de demanda de transporte, padrões de migração e distribuição.

## Material de apoio

Para aprofundar o entendimento prático e teórico sobre análise de fluxos, publiquei dois artigos detalhados no Medium:

1. [**Você sabe o que é uma matriz O-D?**](https://medium.com/@eng.diegocamargo/você-sabe-o-que-é-uma-matriz-o-d-7b66a922018d): Conceitos fundamentais sobre Matrizes de Origem-Destino e seu papel no planejamento.
2. [**Mapa de fluxo no QGIS com DesireLines**](https://medium.com/@eng.diegocamargo/mapa-de-fluxo-no-qgis-com-desirelines-49591953c173): Tutorial passo a passo sobre como gerar mapas de fluxo utilizando a ferramenta.

## Como instalar

No QGIS, acesse o menu **Complementos > Gerenciar e Instalar Complementos**, busque por **Desire Lines** e clique em Instalar.

Para consultar informações adicionais ou reportar problemas, acesse a [página oficial do plugin no repositório do QGIS](https://plugins.qgis.org/plugins/desire_lines/).
