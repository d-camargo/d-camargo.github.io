---
layout: post
title: "SIG-Bus: editar os horários de uma linha de GTFS sem abrir o .zip"
lang: pt
translation: /en/2026/08/15/sig-bus-gtfs-editing-adjust-timetables.html
category: "Engenharia de Transportes"
image: /assets/images/posts/sig-bus-edicao-gtfs.webp
---

O feed da BHTrans está carregado no QGIS, a linha 3350 está selecionada e algumas viagens da manhã precisam sair dez minutos mais tarde. Pelo caminho manual, isso quer dizer descompactar o `.zip`, abrir um `stop_times.txt` com centenas de milhares de registros, achar as linhas certas no meio das viagens de toda a cidade, corrigir horário por horário sem quebrar a referência a `trip_id` e `stop_id`, e recompactar torcendo para o resultado ainda ser um feed válido.

![grade de horários de uma linha de ônibus, com uma viagem deslocada em destaque](/assets/images/posts/sig-bus-edicao-gtfs.webp)

Planejar a operação sobre um padrão internacional é o que permite usar ferramenta que ninguém escreveu para aquela cidade: o mesmo feed abre no QGIS, num validador público ou no aplicativo do passageiro. O preço do padrão é a estrutura, um conjunto de tabelas amarradas por chave estrangeira, e um horário editado na mão num arquivo de texto não avisa quando a amarração se perde. A aba **Edição GTFS** do SIG-Bus existe para essa parte do trabalho.

## Uma cópia de trabalho, não o feed original

Antes de mexer em qualquer campo, o problema é de segurança do dado. **Entrar no modo edição** clona o GeoPackage de análise (`feed.gpkg`) numa cópia de trabalho isolada, o `feed_edit.gpkg`. Tudo o que vem depois acontece nessa cópia, e o feed de análise nunca é alterado diretamente.

Isso muda o custo de errar. Se já houver edição em andamento, o plugin pergunta se você quer **Retomar** de onde parou ou **Recomeçar** de um rascunho limpo, e **Descartar edição** apaga o rascunho, devolvendo a aba ao estado inicial. O rascunho fica salvo até você exportar ou descartar.

## Por que `stop_times` só abre filtrada

O gargalo de editar GTFS num SIG é o tamanho de uma tabela só. No feed de Belo Horizonte o `stop_times.txt` tem 136 MB, e em feeds grandes a tabela chega a milhões de registros: carregada inteira, trava o QGIS. Por isso os campos **Linha (route_short_name)** e **Viagem (trip_id)** ficam ativos quando `stop_times` é a tabela escolhida, com preenchimento obrigatório. Só os horários daquela viagem entram na sessão de edição.

![aba Edição GTFS do SIG-Bus, com a tabela stop_times selecionada e os filtros de linha 3350 e de viagem preenchidos](/assets/images/posts/sigbus02/1.webp)

O motor de edição é híbrido, e de propósito: o plugin cuida do ciclo (entrar, filtrar, validar, exportar, descartar) e quem edita é a tabela de atributos do QGIS, com desfazer, refazer e calculadora de campos. Os campos de ID e de chave estrangeira abrem como somente leitura, para a integridade não se quebrar num clique distraído.

## A linha inteira numa matriz

Filtrar por viagem resolve o desempenho e cria outro limite: a tabela de atributos mostra uma viagem por vez, e quem decide um horário está olhando o intervalo entre partidas, não uma coluna isolada.

O botão **Ajustar horários** abre a linha inteira, com uma aba por sentido (`direction_id` 0 para Ida, 1 para Volta). As paradas ficam nas linhas e as viagens nas colunas; cada coluna traz `V1`, `V2`, `V3` com a primeira saída em `HH:MM` logo abaixo, e o `trip_id` no tooltip. Embaixo da matriz, separado por um divisor arrastável, fica o diagrama de blocos da mesma linha.

![janela Ajustar Horários da linha 3350, com a matriz de paradas e viagens em cima e o diagrama de blocos embaixo](/assets/images/posts/sigbus02/2.webp)

Dois detalhes de leitura evitam confusão. Célula com `-` é parada que aquela viagem não faz: segue editável, mas o que for digitado ali é ignorado na gravação, porque a janela nunca cria parada nova numa viagem. E horário depois da meia-noite se escreve passando de 24 h (`25:10:00`), como manda o padrão.

## Digitar um horário desloca a viagem inteira

Ajustar célula a célula seria trocar um trabalho manual por outro. A decisão de projeto que muda isso: digitar um horário numa célula desloca a viagem inteira, e os demais horários acompanham preservando os tempos de percurso entre paradas. Atrasar a saída de V7 em dez minutos move todas as paradas seguintes de V7.

A seleção é casada nos dois painéis: clicar numa barra do diagrama põe o cursor na coluna daquela viagem na matriz, e clicar numa célula seleciona a viagem no diagrama, então a viagem que chamou atenção no gráfico se acha na tabela sem procurar coluna por coluna. Para o ajuste fino, com uma viagem selecionada no diagrama, `>` e `<` deslocam só a saída ou só a chegada e `+` e `-` deslocam a viagem inteira, com o passo em minutos vindo do campo **Passo**.

## Aplicar ao feed, validar, exportar

Até aqui nada tocou arquivo: o rascunho vive em memória. **Aplicar ao feed** valida a grade antes de gravar (erro bloqueia, aviso pergunta) e grava apenas as viagens cujos horários mudaram. O que fica intocado importa tanto quanto o que muda: só `arrival_time` e `departure_time` são reescritos, e o traçado (`shape_id`), os `trip_id`, o `block_id` e o número de viagens permanecem como estavam.

Fechada a janela, **Validar** confere a integridade referencial e o formato de horário, data e coordenada, detalhando cada falha no log do plugin. **Exportar .zip** roda o validador de novo, aborta se houver erro fatal, pergunta se houver apenas aviso, e reconstrói as coordenadas de `stops.txt` e `shapes.txt` a partir da geometria que está no mapa. Sai um GTFS padrão, que volta para qualquer ferramenta que leia o formato.

Vale registrar onde isso se encaixa: software de gestão de transporte público costuma ser caro, fechado e vendido por assinatura, e quem trabalha numa prefeitura pequena acaba sem ferramenta alguma. O QGIS já está nessas mesas, e o SIG-Bus é um plugin livre em cima dele: é essa lacuna que o projeto tenta cobrir. O [repositório](https://github.com/d-camargo/sig-bus) está aberto para usar, relatar problema ou contribuir.
