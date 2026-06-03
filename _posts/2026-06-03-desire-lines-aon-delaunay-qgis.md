---
layout: post
title: "Desire Lines 0.2.0: Alocação AoN sobre redes Delaunay e melhorias de usabilidade no QGIS"
lang: pt
---

A nova atualização do plugin Desire Lines (versão 0.2.0) introduz ferramentas avançadas de alocação de fluxo e melhorias significativas na experiência do usuário. O principal destaque da versão é a possibilidade de realizar alocações do tipo *All-or-Nothing* (Tudo ou Nada) em uma rede estruturada a partir de triangulações Delaunay, oferecendo uma nova camada de análise espacial para engenheiros de transportes e planejadores urbanos.

![Conceito de Desire Lines e triangulação Delaunay no QGIS](/assets/images/posts/desire_lines_v020.png)

## Alocação AoN (Delaunay): Roteamento por menor custo

A grande novidade desta versão é a aba **AoN (Delaunay)**. Tradicionalmente, o plugin conectava origens e destinos por meio de linhas retas simples. Agora, o plugin é capaz de:

1. Gerar automaticamente uma **rede de conexões baseada na Triangulação Delaunay** a partir dos centroides das zonas fornecidas.
2. Alocar a demanda da matriz Origem-Destino (O-D) sobre essa rede recém-criada, canalizando os fluxos pelos caminhos de menor custo (menor distância geométrica).

Esta abordagem é ideal para análises preliminares de rede quando não se dispõe de uma malha viária completa digitalizada, permitindo compreender como o tráfego se distribui estruturalmente pelo território.

> O plugin também oferece a opção **Split by direction**, que gera atributos separados para cada sentido do fluxo (`flow_ab` e `flow_ba`), facilitando a análise de assimetrias nos padrões de deslocamento.

## Exemplo Prático: Matriz O-D de Passageiros da RMSP

Para demonstrar o poder da alocação sobre redes Delaunay, o repositório do plugin disponibiliza o conjunto de dados da **Matriz de Origem-Destino de passageiros da Região Metropolitana de São Paulo (RMSP)**.

Ao carregar as zonas de tráfego paulistas e sua matriz de viagens correspondente, o plugin constrói a malha de Delaunay e faz a distribuição do fluxo de viagens de forma automatizada. Esse processamento evidencia os grandes eixos de deslocamento da metrópole, destacando a forte demanda radial em direção ao centro e os fluxos de integração perimetral, tudo de forma leve e rápida, sem a complexidade de um grafo de ruas completo.

![Matriz O-D de passageiros da Região Metropolitana de São Paulo com alocação Delaunay no QGIS](/assets/images/posts/Delaunay_matriz_od_saopaulo.png)

Os dados completos e as instruções para reproduzir este mapa de fluxo estão disponíveis na [pasta de exemplos RMSP no repositório oficial](https://github.com/d-camargo/desire_lines/tree/main/examples/RMSP).

## Automação de Sistemas de Referência (CRS)

Para realizar cálculos de menor caminho e distâncias métricas precisas, o plugin necessita operar em coordenadas projetadas (métricas) e não geográficas (graus). A versão 0.2.0 automatiza essa etapa complexa:

* **Detecção automática da zona UTM** local correspondente aos dados inseridos.
* **Fallback para áreas amplas**: caso a análise cubra uma região muito extensa (que cruza múltiplas zonas UTM), o plugin seleciona automaticamente a projeção **SIRGAS 2000 / Brazil Albers (EPSG:10857)**, garantindo a consistência métrica dos cálculos cartográficos em território nacional.

## Flexibilidade nas Entradas e Validação em Tempo Real

A usabilidade foi refinada para se integrar de forma orgânica ao fluxo de trabalho do QGIS. Agora, qualquer camada ativa no painel do projeto pode ser selecionada diretamente nos menus suspensos de entrada do plugin, eliminando a obrigatoriedade de trabalhar apenas com nomes de arquivos específicos importados.

Além disso, o plugin agora realiza uma **validação em tempo real das tabelas de atributos**, checando a existência das colunas necessárias antes que o processo de modelagem seja iniciado. O arquivo GeoPackage gerado na saída também se tornou completamente configurável, com caminhos de salvamento amigáveis e padrões automáticos seguros.

## Visualização Facilitada com Estilo Graduado

A análise visual dos resultados ficou mais intuitiva com a aplicação automática de um estilo graduado baseado no algoritmo **Natural Breaks (Jenks)**. Ao finalizar o processamento, as camadas geradas são coloridas automaticamente de acordo com o volume de fluxo alocado, destacando de forma instantânea os principais eixos de desejo e canais de tráfego. O estilo permanece 100% editável e integrado ao painel de simbologia padrão do QGIS.

## Como Instalar

A versão 0.2.0 do plugin está disponível para download e instalação manual:

1. Baixe o pacote compactado `desirelines-0.2.0.zip` diretamente no repositório de lançamentos.
2. No QGIS, acesse o menu **Complementos > Gerenciar e Instalar Complementos**.
3. Selecione a opção **Instalar a partir de ZIP** e aponte para o arquivo baixado.

Para consultar o código-fonte completo ou acompanhar o desenvolvimento, acesse o repositório oficial do [Desire Lines no GitHub](https://github.com/d-camargo/desire_lines).
