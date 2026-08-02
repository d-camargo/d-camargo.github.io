---
layout: post
title: "Guia Prático: Modelos Digitais de Elevação (DEM) e Aplicações Essenciais no QGIS"
lang: pt
category: "Geoprocessamento"
image: /assets/images/dem_cover.png
---

O **Modelo Digital de Elevação (MDE ou DEM - *Digital Elevation Model*)** é a representação digital contínua das altitudes da superfície da Terra. Na engenharia civil, ambiental e no planejamento urbano, ele funciona como a base de dados fundamental para análises topográficas e modelagem espacial.

![Representação 3D de um Modelo Digital de Elevação](/assets/images/dem_cover.png)

Estruturado em um formato de grade (*raster*), cada célula ou pixel de um MDE armazena um valor específico de elevação em relação ao nível do mar. A partir dessa matriz, é possível derivar uma série de produtos essenciais para projetos de infraestrutura.

Neste artigo, vamos explicar as diferenças entre os modelos de superfície e de terreno, apresentar as principais fontes de dados globais e demonstrar como baixar e processar esses arquivos gratuitamente usando o QGIS.

## DSM x DTM: Qual é a diferença?

Dentro da engenharia e geoprocessamento, o MDE se divide em duas variações essenciais:

*   **Modelo Digital de Superfície (MDS ou DSM - *Digital Surface Model*):** Representa a elevação do solo somada a todas as feições naturais e artificiais presentes acima dele, como copas de árvores, florestas e edifícios. É o retrato de tudo o que está "por cima".
*   **Modelo Digital de Terreno (MDT ou DTM - *Digital Terrain Model*):** Representa estritamente a topografia do solo nu, com a remoção digital de todos os objetos e estruturas que estão acima da superfície.

![Ilustração mostrando a diferença entre o Modelo Digital de Superfície e o Modelo Digital de Terreno](/assets/images/dsm_dtm_concept.png)

Na prática da engenharia, os MDTs (ou DTMs) são a base para cálculos topográficos, permitindo extrair mapas de declividade, modelar padrões de escoamento de água, visualizar o terreno em 3D, analisar bacias hidrográficas e realizar estimativas de volume para corte e aterro em obras de infraestrutura.

### Como o LiDAR consegue "remover" a vegetação para criar o MDT (DTM)?

A mágica por trás do MDT muitas vezes vem da tecnologia **LiDAR** (*Light Detection and Ranging*). O LiDAR consegue remover a vegetação digitalmente graças à sua capacidade de gerar múltiplos retornos a partir de um único pulso de laser.

Quando o sensor emite a luz sobre uma floresta, parte do feixe de laser bate nas folhas e galhos e volta imediatamente (primeiros retornos). No entanto, uma parte dessa luz consegue passar pelas frestas da vegetação até atingir o solo nu abaixo (último retorno). O sistema registra todos esses retornos em frações de segundo, criando uma nuvem de pontos 3D altamente detalhada. Um software então filtra essa nuvem, separando árvores e construções do solo. Ao descartar a vegetação, sobra apenas a topografia real do terreno (MDT).

## Onde encontrar dados de Elevação?

As principais fontes de dados combinam missões de satélites com ampla cobertura e tecnologias recentes de varredura a laser para alta precisão.

**Fontes Globais Gratuitas (Mais Tradicionais):**
*   **SRTM (*Shuttle Radar Topography Mission*):** Levantado no ano 2000 por interferometria de radar (usando duas antenas a bordo de um ônibus espacial). É a base mais popular do mundo, oferecendo modelos de elevação gratuitos com resoluções de 30m e 90m.
*   **ASTER GDEM e ALOS (AW3D30):** Utilizam sensores ópticos para capturar pares de imagens estéreo (imagens do mesmo local em ângulos diferentes) para calcular a elevação. Oferecem dados gratuitos com resolução de 30m.

**Fontes de Alta Precisão (Mais Recentes):**
*   **LiDAR e Drones:** O levantamento é feito por aviões, helicópteros ou drones. Satélites de radar recentes, como o Tandem-X, também fornecem resoluções altíssimas (cerca de 12 metros) em escala global. Localmente, drones com câmeras de alta resolução ou sensores LiDAR leves são cada vez mais usados para modelos exatos de canteiros de obras. Você pode encontrar dados LiDAR e MDTs gratuitos em plataformas como o **OpenTopography**.

## Tutorial: Baixando e Preparando Dados no QGIS

Para trabalhar com esses dados na prática, o QGIS é uma das ferramentas mais poderosas e acessíveis.

### 1. Como baixar dados SRTM pelo OpenTopography no QGIS

A maneira mais prática de obter dados gratuitos é através de plugins:
1. **Instalação do Plugin:** Vá em *Complementos > Gerenciar e Instalar Complementos*. Pesquise por "OpenTopography DEM Downloader" e instale-o.
2. **Criação da Chave API:** Crie uma conta gratuita no portal do [OpenTopography](https://portal.opentopography.org). Na seção *API Key*, solicite sua chave e copie o código.
3. **Seleção da Área:** No QGIS, aproxime o mapa (zoom) na sua área de interesse.
4. **Download:** Abra o plugin, selecione o tipo de DEM (como o SRTM), defina a extensão clicando em "Use Map Canvas Extent", cole sua chave API e clique em *Run*. (Limite máximo da área: 4.050.000 km²).

### 2. Recortando e Reprojetando seu DEM

Antes de analisar, é fundamental preparar o dado espacial:
*   **Reprojetar (Warp):** Acesse *Raster > Projeções > Reprojetar (Warp)*. Selecione o MDE, escolha o sistema de coordenadas (CRS) de destino (como SIRGAS 2000 UTM) e insira "-9999" no campo "Sem dados" (NoData). Execute.
*   **Recortar (Clip):** Com um polígono da sua área de estudo, vá em *Raster > Extração > Recortar Raster pela Camada de Máscara*. Selecione o MDE reprojetado, a camada de máscara e execute.

## Gerando e Utilizando Mapas de Declividade (Slope)

Com o MDE pronto, podemos extrair o mapa de declividade, que indica a inclinação do terreno (o ângulo formado entre a superfície e um plano horizontal). Geralmente, é expresso em graus (0° a 90°) ou porcentagem.

**Como gerar no QGIS:**
Acesse *Raster > Análise > Declividade (Slope)*. Selecione o seu MDE como arquivo de entrada, escolha onde salvar e execute.

**Aplicações Práticas na Engenharia:**
*   **Análise de estabilidade:** Identificar encostas íngremes com risco de deslizamentos.
*   **Modelagem hidrológica:** Prever padrões de escoamento e mapear zonas de inundação.
*   **Planejamento de uso do solo:** Localizar áreas planas adequadas para construção, reduzindo custos de movimentação de terra.

### Classificando Declividades com a Calculadora Raster

Para facilitar a leitura, costumamos agrupar os ângulos em "classes" temáticas. Na **Calculadora Raster** (*Raster > Calculadora Raster*), usamos testes lógicos.

Por exemplo, para classificar declividades de até 10° (Classe 1 - Adequado) e maiores que 10° (Classe 2 - Inadequado), a fórmula seria:
`("Slope@1" <= 10) * 1 + ("Slope@1" > 10) * 2`

### Identificação de Áreas de Risco

O mapa de declividade atinge seu potencial máximo quando cruzado com outras camadas de informação ambiental (uso do solo, geologia, índices pluviométricos):
*   **Risco de Deslizamentos:** Áreas com declividade acentuada + solos instáveis + falta de vegetação.
*   **Risco de Inundações:** Áreas de declividade muito baixa (planícies) + proximidade a rios.

O resultado é um **mapa de zoneamento de risco**, vital para evitar construções em locais perigosos e planejar medidas de contenção.

---
**Referências Bibliográficas:**
*   Ramdani, Fatwa. *Exploring the Earth with QGIS: A Guide to Using Satellite Imagery at Its Full Potential* (Springer, 2023).
*   Garg, P.K. *Remote Sensing. Theory and Applications* (Mercury Learning and Information, 2024).
