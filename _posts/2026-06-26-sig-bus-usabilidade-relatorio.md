---
layout: post
title: "SIG-Bus: da interface ao relatório em PDF"
lang: pt
translation: /en/2026/06/26/sig-bus-usability-report.html
category: "Engenharia de Transportes"
---

A interface do SIG-Bus é contida por decisão: cada botão corresponde a uma etapa do fluxo de análise, e nenhum campo pede uma informação que o plugin poderia derivar sozinho. O resultado é um painel com poucas ações, todas em ordem.

![Tela de entrada de dados do SIG-Bus no QGIS](/assets/images/posts/sigbus01/1.png)

Na imagem acima é apresentada a tela de entrada de dados, tanto para os arquivos GTFS quanto para os arquivos de demanda. O caso usado como exemplo é o do município de Belo Horizonte, e os dados estão disponíveis nos links:

1. [GTFS](https://dados.pbh.gov.br/dataset/gtfs)
2. [Demanda por ponto](https://dados.pbh.gov.br/dataset/estimativa-de-embarque-nos-pontos-de-parada-anterior)

O botão **Reconectar GeoPackage** é usado quando já existe um projeto do QGIS com todas as camadas e basta reconectar ao plugin para refazer os filtros.

## A organização em duas abas

A interface está dividida em **Entrada de Dados** e **Análise**. A divisão reflete uma assimetria real no trabalho: preparar os dados é feito uma vez por análise; filtrar linha, alocar e exportar é onde o usuário repete ciclos até chegar no recorte que precisa.

A aba de **Entrada de Dados** tem três ações em sequência:

1. **Verificar GTFS:** valida o feed e, quando necessário, sintetiza o `calendar.txt`. Muitos feeds não trazem esse arquivo no formato convencional; usam o modo por exceção (`calendar_dates`), registrando cada data de operação individualmente. O plugin detecta o caso e produz um calendário semanal derivado das datas reais de operação, salvo como `gtfs_corrigido.zip`.
2. **Carregar GTFS:** converte os arquivos para um GeoPackage (`feed.gpkg`) e adiciona as camadas ao projeto. O carregamento roda em thread de fundo (`QgsTask`) para não congelar a interface durante a leitura do `stop_times.txt`, que no feed de Belo Horizonte tem 136 MB.
3. **Inserir CSV de Demanda:** importa os dados de embarque por parada do SIU da BHTrans e armazena num segundo GeoPackage (`sigt.gpkg`).

A escolha do GeoPackage como formato de armazenamento foi deliberada. Diferente de camadas temporárias ou shapefiles, o `.gpkg` persiste entre sessões e pode ser inspecionado com qualquer ferramenta SQLite, o que simplifica depuração e torna o dado explorável por outros sistemas.

![Tela de análise do SIG-Bus no QGIS](/assets/images/posts/sigbus01/2.png)

A aba **Análise** concentra os passos de processamento: escolher a linha, definir o período, alocar a demanda e gerar o relatório.

## Filtrar e alocar

Na aba **Análise**, o usuário informa o `route_short_name` da linha (ex.: `101`) e escolhe o intervalo de tempo (dia completo ou uma hora específica, 0h–23h). Ao confirmar, três operações acontecem em paralelo:

- O traçado da linha é destacado na camada `shapes` por filtro de subconjunto.
- A demanda é filtrada para aquela linha na camada `dados_demanda`.
- A camada `horarios_paradas` é construída em background: une `stop_times`, `trips` e `stops` para exibir os horários de partida e chegada de todas as viagens da linha.

![Mapa com os pontos de demanda filtrados para a linha selecionada](/assets/images/posts/sigbus01/3.png)

No mapa acima, apenas os pontos de embarque da linha selecionada permanecem visíveis, sobre o traçado destacado da rota.

**Alocar Demanda** gera a camada `tramos_demanda`: um segmento por par de paradas consecutivas, com os campos `embarques`, `passageiros_acum` e `n_viagens`. A carga é calculada por acumulação: os embarques na parada *i* somam ao total das paradas anteriores. Como o CSV do SIU registra apenas embarques, sem desembarques, o resultado é um **limite superior da carga real**, adequado para comparar trechos de uma mesma linha e identificar os segmentos de maior volume.

![Janela do plugin após a aplicação da alocação de demanda](/assets/images/posts/sigbus01/4.png)

Um detalhe de implementação relevante: os pontos do SIU não têm `stop_id`. A associação com as paradas GTFS é feita por proximidade geográfica, mas o conjunto candidato é restrito às paradas do **shape dominante** da linha e sentido selecionados, o que evita que o join espacial capture paradas de rotas paralelas no mesmo corredor.

![Zoom no traçado: a espessura da linha cresce com a carga acumulada por tramo](/assets/images/posts/sigbus01/5.png)

A simbologia graduada é aplicada automaticamente. Com o zoom no traçado, a leitura fica imediata: a espessura de cada tramo cresce com a carga acumulada, tornando visível onde a linha carrega mais passageiros.

## O relatório PDF

O botão **Gerar Relatório** exporta um PDF em A4 paisagem, com uma página por sentido. Cada página tem três elementos:

- **Mapa de carga:** simbologia graduada em `passageiros_acum`, sobreposta ao traçado da linha.
- **Mapa de clusters:** agrupamento K-means das paradas de embarque, gerado pelo `native:kmeansclustering` do QGIS, com simbologia por cluster.
- **Gráfico de barras:** embarques por parada, desenhado com `QPainter` e `QImage` diretamente. O matplotlib não está disponível na instalação padrão do QGIS, então o gráfico é produzido pela API gráfica do Qt.

O relatório usa `QgsPrintLayout`, a API de impressão nativa do QGIS. A escolha mantém a consistência com o restante do plugin (sem dependências externas) e integra os mapas já renderizados no projeto, escala e simbologia incluídas.

---

O [post anterior desta série](https://www.dcamargo.com.br/2026/06/16/sig-bus-gtfs-demanda-qgis.html) detalha o modelo de alocação de demanda e as decisões de estrutura de dados. A próxima parte vai cobrir o Diagrama de Blocos, a ferramenta de alocação de frota do plugin.

O repositório está disponível no [GitHub](https://github.com/d-camargo/sig-bus). O feed GTFS de Belo Horizonte para reproduzir as análises está em `docs/gtfsfiles.zip`.
