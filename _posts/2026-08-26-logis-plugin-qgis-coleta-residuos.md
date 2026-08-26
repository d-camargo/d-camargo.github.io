---
layout: post
title: "Logis: roteirização de coleta de resíduos no QGIS"
lang: pt
category: "Engenharia de Transportes"
image: /assets/images/posts/logis-coleta-residuos.webp
translation: /en/2026/08/26/logis-plugin-qgis-coleta-residuos.html
---

O Logis, meu novo plugin para QGIS, foi aprovado no repositório oficial de complementos na versão **0.1.8**, marcada como experimental. Ele agrupa ferramentas de logística em três módulos, e o que motivou este post é o de coleta de resíduos urbanos: setorizar o município, traçar o percurso do caminhão rua por rua e medir quanto do trajeto é produtivo.

![Percurso de coleta de resíduos sobre uma malha viária urbana em vista isométrica](/assets/images/posts/logis-coleta-residuos.webp)

## Quase nada de graça para logística urbana

Quem precisa planejar coleta, entrega ou localização de instalações no Brasil tem hoje dois caminhos. O primeiro é software proprietário de roteirização, que resolve o problema e cobra uma licença anual fora do orçamento da maior parte dos municípios pequenos. O segundo é código de pesquisa, publicado como script ou notebook, que funciona mas pressupõe ambiente Python montado, dependências instaladas e alguém disposto a lidar com traceback.

O profissional que trabalha no QGIS, que é a ferramenta padrão em prefeitura e em consultoria de pequeno porte, fica sem porta de entrada. O Logis existe para ocupar esse espaço: os 25 algoritmos entram na Caixa de Ferramentas de Processamento como qualquer outro processo do QGIS, com camada de entrada, parâmetros e camada de saída.

## Coleta de resíduos é roteirização por arcos

A maior parte das ferramentas de rota disponíveis resolve um problema de visita a pontos: existe um conjunto de paradas com coordenadas conhecidas, e a pergunta é em que ordem visitá-las. É a formulação do caixeiro viajante e de suas variantes com capacidade, e ela descreve bem uma operação de entrega de encomendas.

A coleta domiciliar não funciona assim. O caminhão não visita pontos, ele percorre a extensão da via: o que precisa ser coberto é a rua inteira, e dos dois lados quando há contêiner nos dois lados. Modelar cada imóvel como uma parada gera um problema grande demais para resolver em tempo útil e ainda descreve mal a operação real, em que o veículo anda em marcha lenta com os coletores acompanhando a pé. A formulação adequada é a de roteirização por arcos, que tem três casos clássicos, todos no plugin:

* **CPP (Problema do Carteiro Chinês):** percorrer todas as ruas do setor pelo menos uma vez, voltando ao ponto de partida, com a menor distância total. Serve quando toda a malha do setor recebe coleta.
* **RPP (Problema do Carteiro Rural):** apenas um subconjunto das ruas precisa de coleta, e as demais servem só de passagem. É o caso mais comum, porque vias sem domicílio, trechos de rodovia e ruas atendidas por outro setor não geram resíduo.
* **CARP (Roteirização por Arcos com Capacidade):** o caminhão enche antes de terminar o setor e precisa descarregar. O percurso deixa de ser um circuito único e vira uma sequência de viagens, cada uma limitada pela capacidade do veículo, com ida e volta ao destino.

## Setorizar, dimensionar a frota, medir o que sobra

Traçar a rota é o meio do trabalho, não o começo nem o fim. O módulo cobre a cadeia inteira, e cada etapa é um algoritmo separado, encadeável em modelo gráfico.

Tudo começa pela **estimativa de geração**: a partir da população ou dos domicílios associados a cada trecho e de uma taxa de geração per capita, o plugin distribui a carga esperada sobre a malha viária. É esse peso por arco que alimenta o resto.

Com a carga distribuída, a **setorização** divide o município em setores contíguos e equilibrados: cada setor recebe uma fatia parecida de resíduo, e os trechos de um mesmo setor se conectam entre si, sem ilhas soltas do outro lado da cidade. Contiguidade e equilíbrio puxam em direções opostas, e o algoritmo expõe o parâmetro que arbitra entre os dois.

O **dimensionamento de frota** converte o volume de cada setor em número de veículos, considerando a capacidade útil do compactador, o número de viagens ao destino por turno e a jornada disponível. A resposta é quantos caminhões o desenho exige, que é a variável que aparece no contrato de terceirização.

O ciclo fecha nos indicadores. A **razão de deadhead** mede a fração do percurso rodada sem coletar, que é custo puro de combustível e hora de equipe. O **equilíbrio entre setores** mostra a dispersão de carga entre eles. A **cobertura por setor** aponta os trechos com geração que ficaram fora de qualquer rota. A **distância ao destino** mede o quanto cada setor paga para chegar ao aterro ou à unidade de transbordo. Um desenho de coleta só pode ser comparado a outro quando esses números existem.

## Os outros dois módulos

A **Logística Urbana** trabalha na escala do município a partir da malha viária do OpenStreetMap, com o mesmo pipeline de aquisição e limpeza que desenvolvi no GisBR. São oito algoritmos de diagnóstico: densidade e conectividade da rede, circuidade média, restrição de circulação de carga, densidade de demanda, acessibilidade gravitacional, intermediação de arcos e distância de entrega. É a camada que responde onde a rede já é o gargalo, antes de qualquer rota ser traçada.

A **Logística Regional** sobe a escala e usa dado oficial: a base do SNV/DNIT, as malhas do geobr e as infraestruturas de dados espaciais estaduais. São três indicadores de rede rodoviária: densidade, percentual pavimentado e identificação de ligações críticas, os trechos cuja remoção parte a rede em duas.

Completam o conjunto quatro algoritmos transversais: localização de instalações por p-mediana, MCLP e LSCP, e roteirização de veículos com capacidade. Cada módulo tem seu painel no QGIS, mas os 25 algoritmos também estão na Caixa de Ferramentas sob o provedor `logis`, o que permite encadeá-los em modelo gráfico e rodar o diagnóstico inteiro em lote.

## Zero dependência obrigatória

O plugin roda com PyQGIS e a biblioteca padrão do Python, sem instalar nada. A construção do grafo e os caminhos mínimos usam as classes nativas do QGIS (`QgsGraph`, `QgsGraphBuilder` e `QgsGraphAnalyzer`), e as heurísticas estão escritas em Python puro: Clarke-Wright e varredura para as rotas de veículo, 2-opt para melhoria local, Teitz-Bart para a p-mediana e emparelhamento dos vértices de grau ímpar, que é o passo que torna o grafo euleriano no carteiro chinês.

A razão dessa escolha é operacional. Instalar pacote Python em máquina de prefeitura esbarra em usuário sem privilégio de administrador, em proxy que bloqueia o PyPI e em política de TI que não abre exceção para um plugin. O OR-Tools e o pyarrow continuam sendo aproveitados quando estão presentes, com importação tardia e retorno automático às heurísticas quando não estão: a instalação padrão do QGIS basta para rodar tudo.

O fluxo assume SIRGAS 2000 (EPSG:4674) na entrada e na saída, e a projeção métrica aparece apenas nos cálculos intermediários de distância e área, sem que o usuário precise administrar isso.

## Como instalar

Por ser experimental, o Logis exige um ajuste único no QGIS: em **Complementos > Gerenciar e Instalar Complementos > Configurações**, marque **Mostrar também os plugins experimentais**. Depois busque por **Logis** e clique em Instalar. A versão publicada pede QGIS 3.16 ou superior e roda tanto no Qt5 quanto no Qt6.

A página oficial está no [repositório de complementos do QGIS](https://plugins.qgis.org/plugins/logis). A documentação, com a descrição de cada algoritmo e de seus parâmetros, fica em [logis.dcamargo.com.br](https://logis.dcamargo.com.br), e o código, sob licença GPL-3.0, está no [GitHub](https://github.com/d-camargo/logis).

Por ser uma versão experimental, o retorno de quem usar vale mais do que qualquer teste que eu faça sozinho: relato de erro, camada que quebrou um algoritmo ou sugestão de indicador são bem-vindos nas issues do repositório. Há também uma [página do projeto no portfólio](/portfolio/logis.html), com o histórico do desenvolvimento.
