---
layout: post
title: "GisBR: dados espaciais oficiais do Brasil direto no QGIS"
lang: pt
translation: /en/2026/07/01/gisbr-plugin-qgis-experimental.html
category: "Geoprocessamento"
---

O GisBR, meu novo plugin para QGIS, foi aprovado no repositório oficial de complementos como versão experimental. Ele traz para dentro do QGIS o acesso "uma linha → uma camada" dos pacotes **geobr** e **censobr**, do IPEA, sem exigir que o usuário saiba programar em R ou Python.

![Ícone do plugin GisBR](/assets/images/posts/gisbr-cover.webp)

## O problema que ele resolve

Quem trabalha com análise espacial no Brasil conhece a rotina: para montar um mapa municipal, é preciso navegar pelo FTP do IBGE, localizar a malha do ano correto, baixar o arquivo compactado, extrair e só então carregar no QGIS. O pacote geobr resolveu isso de forma elegante para quem usa R ou Python: uma função retorna a camada pronta. Mas grande parte dos profissionais de geoprocessamento trabalha direto no QGIS e ficava de fora desse fluxo.

O GisBR fecha essa lacuna. Cada geografia do geobr vira um algoritmo na Caixa de Ferramentas de Processamento: o usuário escolhe o ano, filtra por estado ou código IBGE e recebe a camada carregada no projeto, já em SIRGAS 2000 (EPSG:4674). O caso de uso que orienta o projeto é o trabalho na **escala municipal**: reunir rapidamente as camadas oficiais de um município para diagnóstico e planejamento.

## O que está disponível

A versão 0.2.0 traz **55 algoritmos**, em duas fases. A Fase 1, com backend em GeoPackage (geobr v1.7.0), cobre 26 geografias organizadas em grupos:

* **Divisão administrativa:** país, regiões, estados, mesorregiões, microrregiões, regiões intermediárias e imediatas, municípios e sedes municipais.
* **Censo:** setores censitários, áreas de ponderação, grade estatística e bairros.
* **Urbano e metropolitano:** regiões metropolitanas, áreas urbanizadas, concentrações urbanas e arranjos populacionais.
* **Meio ambiente:** biomas, Amazônia Legal, semiárido, unidades de conservação, terras indígenas e áreas de risco de desastre.
* **Setoriais:** regiões de saúde, estabelecimentos de saúde e escolas.

A Fase 2 adiciona 28 algoritmos `read_*_v2` sobre o catálogo Parquet do geobr v2.0.0, com dados mais recentes (até 2022/2025) e geografias que só existem na nova versão, como **favelas, locais de votação e terras quilombolas**. Completa o conjunto o algoritmo **join_censo**, que cruza os setores censitários do geobr com as tabelas demográficas do censobr.

Cada algoritmo aceita os mesmos parâmetros: ano (com padrão no mais recente), filtro por código IBGE ou sigla de estado e a opção de geometria simplificada, que acelera a renderização quando a precisão do traçado não é crítica.

## Decisões técnicas

Uma escolha de projeto orientou o desenvolvimento: **zero dependências externas**. O plugin usa apenas a API nativa do QGIS/Qt e a biblioteca padrão do Python. Nada de geopandas, pandas ou requests. Isso elimina a etapa de instalação de pacotes que costuma travar usuários menos técnicos e reduz o risco de conflitos com outros plugins. A única exceção é opcional: os algoritmos da Fase 2 leem Parquet pelo driver GDAL do próprio QGIS e, se ele não estiver disponível, aceitam o pyarrow como alternativa.

Os downloads vão para um cache em disco, com fallback automático: se o servidor do IPEA estiver fora do ar, o plugin busca os mesmos arquivos em um espelho no GitHub.

## Para onde o projeto vai

O espelho do geobr é a fundação de algo mais específico: o GisBR está evoluindo para um **sistema de diagnóstico municipal** voltado a cidades que precisam elaborar ou revisar o Plano Diretor. A ideia é escolher o município em um painel e receber as bases oficiais (transportes, drenagem e saneamento, demografia, meio ambiente, educação e saúde) já recortadas pelo polígono municipal e organizadas em um GeoPackage. É a automação do trabalho que descrevi no post sobre [leitura do território](/2026/06/24/leitura-do-territorio-plano-diretor.html). Essa camada ainda está em desenvolvimento e entra em uma versão futura.

## Como instalar

Por ser experimental, o plugin exige um ajuste único: no QGIS, acesse **Complementos > Gerenciar e Instalar Complementos > Configurações** e marque **Mostrar também os plugins experimentais**. Depois, busque por **GisBR** e clique em Instalar.

O código é aberto (GPL) e está no [GitHub](https://github.com/d-camargo/gisbr). Issues com relatos de problemas ou sugestões de novas geografias são bem-vindas. A página oficial do plugin está no [repositório do QGIS](https://plugins.qgis.org/plugins/gisbr/).
