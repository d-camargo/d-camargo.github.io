---
layout: post
title: "GisBR: redes de transporte prontas para roteamento e alocação no QGIS"
lang: pt
category: "Engenharia de Transportes"
image: /assets/images/posts/gisbr-redes-transporte.webp
translation: /en/2026/10/17/gisbr-transport-networks-routing-assignment.html
---

Para começar um modelo de rede de transporte, o roteiro de sempre é baixar o SNV do DNIT, o shapefile do DER e um extrato do OSM, cada um num formato, num sistema de coordenadas e sem nenhum nó em comum. Só depois de reprojetar e emendar tudo é que dá para rotear, e ainda sobra um risco: em Minas Gerais, 414 dos 945 trechos do DNIT estão marcados como `PLA`, rodovia planejada que daria rota falsa.

![Malha viária em linhas douradas que passa de trechos soltos, à esquerda, a uma rede conectada com fluxo de luz, à direita](/assets/images/posts/gisbr-redes-transporte.webp)

## O trabalho que vem antes do modelo

Roteamento e alocação de tráfego pressupõem um grafo: arcos que terminam em nós, nós compartilhados entre arcos vizinhos, atributos de velocidade e comprimento. Os dados de origem não chegam assim. Cada fonte tem sua geometria, seu CRS e seu critério de segmentação, e as pontas de linhas que deveriam se encontrar ficam a poucos metros uma da outra, sem se tocar.

Há ainda duplicidade. Em Contagem, o DNIT repete a geometria das BRs coincidentes: a BR-040 e a BR-135 aparecem sobrepostas ao longo de 23,5 km. Se isso entra no modelo sem tratamento, o mesmo trecho de pista é contado duas vezes. A coleta, a reprojeção e a limpeza de topologia consomem a primeira parte de qualquer projeto de rede, antes de a primeira rota ser calculada.

O GisBR, plugin para QGIS que desenvolvo, faz essa etapa. As seções a seguir mostram o que ele entrega no lugar de cada passo manual.

## Um município, um painel, um GeoPackage

O GisBR roda só com PyQGIS e a biblioteca padrão do Python, sem `pip install`. O fluxo começa no painel de diagnóstico: escolho a UF, escolho o município (ou um recorte regional), marco as fontes que quero e clico em **Carregar selecionadas**. Tudo sai em SIRGAS 2000 (EPSG:4674), gravado num GeoPackage.

As fontes estão organizadas em nove eixos temáticos. A rede de transporte fica no eixo **1. Transportes**, que é o assunto deste post; os outros eixos seguem o mesmo fluxo e não precisam de download separado. Há também o modo região metropolitana, com as 84 RMs do catálogo do IBGE, para quando o estudo cobre mais de um município.

O ponto é o que deixa de existir: a lista de portais para visitar, os formatos para converter e o projeto QGIS montado camada por camada.

## A malha do OSM com a topologia de verdade

A rede do OSM chega com os ways quebrados em arcos nos `node_id` compartilhados, ou seja, a topologia que o próprio OSM já registra. As camadas `osm_links` e `osm_nodes` trazem `arc_id`, `from_node` e `to_node`, componente conexa e grau do nó. Para modelagem, vêm `maxspeed`, `velocidade_kmh` e `comprimento_m`. É o que um grafo pede, sem etapa intermediária de construção.

A rede pode ser veicular ou pedonal, e a carga corre em segundo plano, com barra de progresso e botão Cancelar. Para uma região metropolitana, a rede OSM vem de uma base pré-construída, com checagem de sha256 e cache local.

O [post de julho sobre a malha OSM](/2026/07/06/gisbr-0-3-2-osm-fim-experimental.html) apresentou a primeira versão dessa camada. A topologia foi refeita desde então, e o [guia da malha OSM](https://gisbr.dcamargo.com.br/guias/vias/) descreve os campos em detalhe.

## Rodovias e ferrovias oficiais como rede roteável

A malha interurbana é a que costuma dar mais trabalho. A partir da 1.2.0, seis fontes oficiais viram rede roteável, cada uma com links, nós, problemas e removidos:

- DNIT/SNV
- DER-MG
- DER-PR
- Siga-GO (malha viária)
- Ministério da Infraestrutura (ferrovias)
- IBGE BC250 (ferrovias)

As rodovias do BC250 ficam de fora, porque a camada mistura jurisdições.

Na construção da rede, o GisBR aplica correções automáticas: pontas a até 1 m são unificadas, uma junção em T a até 10 m quebra a linha alvo e liga a ponta ali, e arcos coincidentes são colapsados. É o caso das BRs repetidas de Contagem. Cada correção fica registrada com `severidade=corrigido`, então nada muda em silêncio.

O que não existe sai da rede. Trecho planejado (`PLA`, ou ferrovia Planejada, Em Estudo, Em Obra) vai para a camada de removidos, o que tira de uma vez os 414 trechos do DNIT que em MG dariam rota falsa. A rodovia federal que o DER repete também sai quando o DNIT é marcado junto: no recorte de Contagem, 22 dos 44 trechos do DER-MG eram federais.

Um limite: as malhas oficiais não trazem sentido de tráfego, então a rede resultante é bidirecional.

## Uma lista do que a rede tem de errado

Rede gerada de dados reais tem defeitos, e o que importa é encontrá-los antes de rodar o modelo, não no resultado da alocação. Por isso o GisBR grava, junto das camadas de links e nós, uma camada de problemas (`osm_problemas` na rede do OSM) com tipo e severidade, para filtrar e olhar no mapa.

Alguns tipos: `ilha`, um conjunto de arcos desconectado do resto, que nenhuma rota alcança; `mao_unica_sem_saida`, onde o sentido único prende o fluxo; `ponta_quase_conectada`, duas pontas que quase se tocam e provavelmente deveriam; e `cruzamento_sem_no`, linhas que se cruzam sem nó, o que pode ser erro ou pode ser um viaduto. Nas malhas oficiais, esse último só é apontado, nunca alterado.

Ponta solta, ou seja, o beco sem saída comum, não é listada, porque é uma situação normal da malha viária.

## Da rede ao roteamento e à alocação de tráfego

Com a rede pronta, o que vem depois depende do estudo. O Desire Lines, outro plugin meu, tem uma aba de **Alocação em rodovias** que trabalha sobre a malha DNIT/SNV mais DER obtida pelo GisBR, que é uma dependência declarada. A capacidade por sentido segue o HCM 6ª edição, a alocação pode ser tudo-ou-nada ou equilíbrio (MSA com função BPR), e o nível de serviço sai pela relação v/c. O foco são rodovias, não vias urbanas; mais detalhes na [página do projeto](/portfolio/desire-lines.html).

O [Logis](/2026/08/26/logis-plugin-qgis-coleta-residuos.html) usa a malha municipal baixada pelo GisBR no painel Rede Viária, para roteirizar coleta (TSP e CVRP).

Quem prefere script pode chamar a rede OSM direto pelo Processing, com o algoritmo `gisbr:osm_network`, que devolve `LINKS`, `NODES` e `PROBLEMAS`:

```python
processing.run("gisbr:osm_network", {
    "CODE": "3118601",   # código IBGE do município
    "REDE": 0,           # 0 = veicular
    "LINKS": "TEMPORARY_OUTPUT",
    "NODES": "TEMPORARY_OUTPUT",
    "PROBLEMAS": "TEMPORARY_OUTPUT",
})
```

Para a demanda, o GisBR carrega os POIs do OSM (`osm_pois`) com o predicado do osm2gmns, e o algoritmo `gisbr:export_poi_gmns` grava um `poi.csv` no layout do osm2gmns e do grid2demand.

## Como começar

O GisBR está no [repositório oficial de complementos do QGIS](https://plugins.qgis.org/plugins/gisbr/). O passo a passo está na página de [instalação](https://gisbr.dcamargo.com.br/instalacao/), e o código fica no [GitHub](https://github.com/d-camargo/gisbr).

Depois de instalar, abra o painel, escolha um município e marque as fontes do eixo Transportes. O [guia de redes de transporte](https://gisbr.dcamargo.com.br/guias/redes-transporte/) e a [documentação](https://gisbr.dcamargo.com.br/) explicam cada camada. Para testar, carregue a rede do seu município e abra a camada de problemas antes de qualquer outra coisa.
