---
layout: post
title: "SIG-Bus: Leitura de GTFS e Integração de Demanda de Passageiros no QGIS"
lang: pt
translation: /en/2026/06/16/sig-bus-gtfs-demand-qgis.html
category: "Engenharia de Transportes"
image: /assets/images/posts/sig_bus_mapa_carga.png
---

O SIG-Bus tem um objetivo bem delimitado: ler feeds GTFS dentro do QGIS, cruzá-los com os dados de embarque por parada e entregar relatórios sintéticos por linha, tudo sem dependências externas além do próprio QGIS. O projeto nasceu como PIBIC no CEFET-MG em 2020 (com aplicação ao edital em 2019) e foi apresentado na Semana de Ciência e Tecnologia de 2025.

![SIG-Bus: mapa de carga de passageiros por trecho no QGIS](/assets/images/posts/sig_bus_mapa_carga.png)

## O problema de integração

O QGIS não oferece suporte nativo a GTFS além da leitura básica de geometrias. Analisar uma rede de ônibus exige cruzar três informações que vivem em fontes distintas: a geometria das rotas, os horários programados e a demanda real de passageiros. Sem uma ferramenta dedicada, juntar tudo isso é um trabalho manual e repetitivo.

Os dados de embarque estão disponíveis no [portal de dados abertos da Prefeitura de BH](https://dados.pbh.gov.br/dataset/estimativa-de-embarque-nos-pontos-de-parada), em formato CSV com coordenadas e códigos de linha próprios. Esses identificadores não coincidem diretamente com os do feed GTFS. Construir esse elo espacial de forma confiável, sem gerar associações incorretas com rotas paralelas, foi o núcleo técnico do trabalho.

## Como o plugin funciona

O SIG-Bus organiza o fluxo em seis etapas sequenciais:

1. **Verificação do GTFS:** valida a integridade do feed e gera calendários sintéticos quando o arquivo `calendar.txt` está ausente.
2. **Importação GTFS:** converte os arquivos para GeoPackage, criando camadas espaciais de paradas, geometrias de rota e viagens, com índices otimizados para consulta.
3. **Importação da demanda:** carrega o CSV de embarques e vincula os pontos de demanda às paradas GTFS por junção espacial, restrita ao padrão de serviço dominante da linha para evitar falsos positivos.
4. **Seleção de rota e período:** o usuário escolhe a linha e o intervalo horário (dia completo ou hora específica, de 0h a 23h).
5. **Alocação de demanda:** gera a camada `tramos_demanda` com carga acumulada e contagem de viagens por trecho.
6. **Visualização:** estilos graduados são aplicados automaticamente, destacando os trechos de maior volume.

## A camada de horários por parada

Ao filtrar uma linha, o plugin gera automaticamente a camada **`horarios_paradas`**, uma camada de pontos com os horários de todas as viagens da rota selecionada.

Para cada parada, a camada registra:

- `arrival_time` e `departure_time`
- `stop_sequence` e `stop_name`
- `trip_id`, `shape_id` e `direction_id`

A camada é construída por uma junção direta entre as tabelas `stop_times`, `trips` e `stops` no banco GeoPackage, indexada por `trip_id`. Com ela é possível visualizar a distribuição dos serviços ao longo do dia, identificar paradas com intervalos irregulares ou conferir a cobertura horária de uma linha específica.

> Como todas as camadas do SIG-Bus, a `horarios_paradas` é baseada em memória e precisa ser regenerada após reabrir o QGIS.

## Alocação de demanda por trecho

A camada `tramos_demanda` é o principal produto analítico do plugin. A carga em cada trecho é calculada por **conservação de fluxo**: os embarques na parada *i* somam-se à carga do trecho anterior.

Como os dados de bilhetagem registram apenas embarques, sem desembarques, o método assume que todos os passageiros desembarcam no ponto final. Isso produz um **limite superior da ocupação real**, adequado para:

- Comparação relativa entre trechos de uma mesma linha
- Identificação dos segmentos mais carregados por período
- Análise da distribuição horária da demanda

O arquivo `METHODS.md` no repositório detalha as hipóteses, casos-limite e recomendações de interpretação.

## Semana C&T 2025 e o estado atual

O projeto foi apresentado na Semana de Ciência e Tecnologia do CEFET-MG em 2025. Após essa versão, duas adições foram incorporadas: **categorização dos trechos por cluster de demanda** com aplicação automática de estilos graduados, e **geração de relatório PDF** com dois mapas (carga acumulada e agrupamento por cluster) sobrepostos à geometria da rota.

O repositório completo está no [GitHub](https://github.com/d-camargo/sig-bus). Todos os testes foram feitos com o feed GTFS real da cidade de Belo Horizonte, e o arquivo `docs/gtfsfiles.zip` traz esses mesmos dados para quem quiser reproduzir as análises.

Se você quiser experimentar o plugin e não tiver o arquivo em mãos, posso enviar o `.zip` diretamente. É só pedir por e-mail ([eng.dcamargo@outlook.com.br](mailto:eng.dcamargo@outlook.com.br)) ou por [WhatsApp](https://wa.me/553135653353) (+55 31 3565-3353).
