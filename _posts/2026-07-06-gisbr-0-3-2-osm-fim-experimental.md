---
layout: post
title: "GisBR 0.3.2: malha viária do OSM e o fim do rótulo experimental"
lang: pt
category: "Geoprocessamento"
image: /assets/images/posts/gisbr-osm-belem.webp
translation: /en/2026/07/06/gisbr-0-3-2-osm-fim-experimental.html
---

Há uns dois anos conversei com o professor Xuesong (Simon) Zhou, da Arizona State University, um dos autores do [osm2gmns](https://github.com/jiawlu/OSM2GMNS), uma ferramenta que transforma dados do OpenStreetMap em redes de transporte prontas para modelagem. Dois anos depois, aquela mecânica de links e nós chega ao meu plugin: a versão 0.3.2 do GisBR baixa a malha viária de qualquer município brasileiro direto do OSM. E é a primeira versão publicada sem o rótulo **experimental** no repositório oficial do QGIS.

![Malha viária do OpenStreetMap baixada pelo GisBR sobre o limite municipal de Belém (PA), no QGIS](/assets/images/posts/gisbr-osm-belem.webp)

## A fonte que faltava: a rede de circulação

O diagnóstico municipal do GisBR já reunia 29 fontes oficiais em 8 eixos (transporte, saneamento, demografia, ambiental, educação, saúde, urbano e político-administrativo), tudo gravado num GeoPackage local. Dava para mapear quase tudo de um município, menos as ruas dele. Para quem trabalha com planejamento de transportes, é uma ausência difícil de justificar.

A 0.3.2 fecha essa lacuna. O plugin consulta a API Overpass do OpenStreetMap, baixa as vias do município escolhido e monta duas camadas com topologia mínima: **links** (trechos de via) e **nós** (as conexões entre eles). Não é um despejo de geometrias soltas: é uma rede, no sentido que a modelagem de transportes usa.

> **Aviso:** as vias vêm do OpenStreetMap, uma base cartográfica colaborativa, abastecida por mapeadores voluntários. A cobertura e o detalhamento variam de município para município: onde a comunidade local é ativa, a malha é rica; onde não é, podem faltar vias ou atributos. Confira o resultado antes de usar em análise.

A mecânica dessa montagem tem origem declarada. O osm2gmns, do Jiawei Lu e do professor Zhou, converte extratos do OSM em redes no formato GMNS (General Modeling Network Specification), a especificação aberta que a comunidade de modelagem vem adotando para descrever redes por arquivos de nós e links. O GisBR aplica essa mesma lógica dentro do QGIS: em vez de CSVs, o resultado vira camadas no GeoPackage do diagnóstico, em SIRGAS 2000 (EPSG:4674), prontas para os 55 algoritmos de Processing do plugin.

O comportamento segue a regra das fontes WFS e ArcGIS que já existiam: se a camada já está no GeoPackage, o download é pulado. Quem quiser rebaixar marca o checkbox "Atualizar bases já baixadas". Nada de requisição repetida ao Overpass por descuido, que é exatamente o tipo de uso que derruba a cota de um servidor público.

## O bug do timeout que nunca chegava

No meio desse trabalho apareceu o bug mais irritante da release, e ele não estava no código novo. A função que monta a consulta Overpass recebia um timeout configurável por fonte, só que o valor morria no caminho e nunca era aplicado à requisição. Funcionava no dia bom do servidor. Estourava no dia ruim.

A 0.3.2 fecha o circuito, e de quebra o tratamento de erro ficou mais honesto: erro de rede é reportado como erro de rede, e resposta que não é JSON válido vira uma exceção própria (`OverpassError`) com mensagem legível, em vez de um traceback críptico no meio do painel.

## O SSL do Windows

Desde a 0.3.0, alguns usuários de Windows viam o carregamento dos metadados do IPEA falhar com erro de certificado SSL. No Linux, nada. No QGIS do Windows, a validação da cadeia quebrava. A solução da 0.3.2: o plugin passou a embarcar a cadeia de certificados do servidor do IPEA (`core/certs/ipea_chain.pem`) e usa um fallback seguro quando a validação padrão do sistema falha. Sem desligar verificação de certificado, sem pedir para o usuário mexer em configuração do QGIS.

Era o último item que me segurava antes de tirar o experimental. Não fazia sentido promover um plugin que quebrava na plataforma onde está a maioria dos usuários de QGIS.

A 0.3.2 já está disponível no repositório oficial de complementos do QGIS (agora sem precisar habilitar a opção de plugins experimentais). O código é GPL-3.0 e está no [GitHub](https://github.com/d-camargo/gisbr). Se a malha do seu município vier estranha, abra uma issue: rede viária de OSM tem qualidade desigual pelo Brasil, e casos reais são o que calibra a ferramenta.
