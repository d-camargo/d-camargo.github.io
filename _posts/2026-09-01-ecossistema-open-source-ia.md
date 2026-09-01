---
layout: post
title: "Ninguém tem tempo de aprender mais um software: a IA e o código aberto"
lang: pt
category: "Geral"
image: /assets/images/posts/ecossistema-open-source-ia.webp
translation: /en/2026/09/01/open-source-ecosystem-ai.html
---

Mês passado eu precisava de uma grade de voo fotogramétrico sobre uma área que já estava aberta no QGIS, com o limite do terreno e o relevo ao lado. Havia três saídas: aprender o QGroundControl e redesenhar o polígono lá dentro, sobre uma imagem de satélite sem nenhuma daquelas camadas; calcular os transectos na mão, numa planilha; ou ler o código do QGroundControl e trazer esse cálculo para dentro do QGIS.

![Parede isométrica de caixas escuras fechadas com uma única caixa aberta e iluminada em dourado](/assets/images/posts/ecossistema-open-source-ia.webp)

Escolhi a terceira, que custou semanas em vez das duas tardes das outras, e mesmo assim se pagou. A pergunta que sobrou: quando acrescentar a função ao software que já está aberto vale mais do que aprender mais um?

## A conta que não fecha

O catálogo de ferramentas abertas cresce todo mês: plugin novo no repositório do QGIS, biblioteca nova de dado geoespacial em Python, aplicativo novo para validar ou converter alguma coisa. Quase tudo de graça, e muita coisa resolvendo problema real.

O que não cresce é o tempo. Cada ferramenta nova cobra uma curva de aprendizagem antes de devolver qualquer coisa: instalar, entender o modelo de dados, descobrir onde a saída não bate com o resto do fluxo. Essa curva é paga em hora de trabalho, tirada do mesmo lugar de onde sai o prazo. O gargalo do ecossistema aberto hoje não está na oferta de ferramenta, e sim na atenção disponível para distribuir entre as que já existem.

## Aprender a ferramenta ou pedir o resultado

A Sequoia publicou em [Services: The New Software](https://sequoiacap.com/article/services-the-new-software) um argumento que serve para ler esse impasse de baixo. Ela separa copiloto de piloto automático: o copiloto vende a ferramenta ao profissional, que continua respondendo pelo resultado; o piloto automático vende o resultado direto a quem precisa dele. A aposta se sustenta em orçamento: o gasto com serviço é da ordem de seis vezes o gasto com a ferramenta equivalente.

> "If you sell the tool, you're in a race against the model. But if you sell the work, every improvement makes your service faster, cheaper, and harder to compete with."

O artigo olha para quem vende; do lado de quem usa, a mesma frase descreve outra coisa. O engenheiro que precisa entregar a setorização da coleta na sexta não quer o software de roteirização, quer os setores. Só que a ferramenta não desaparece quando sai de vista: ela continua rodando em algum lugar, e alguém continua respondendo pelo que ela produziu.

## Por que o código aberto encurta o caminho

Personalizar software fechado tem um caminho só: abrir chamado e esperar o roadmap do fornecedor, que não vai priorizar o que interessa a poucos clientes.

Com código aberto dá para ler, mudar e rodar no mesmo dia. O que sempre encareceu essa rota foi entender a base de código alheia antes de tocar em qualquer linha, e é esse preço que caiu: entrego o repositório à IA, pergunto onde mora o cálculo que me interessa, e a leitura que levaria dias leva uma tarde.

O QGC4QGIS depende disso duas vezes. Ele reimplementa no QGIS o gerador de grade do QGroundControl, a classe `SurveyComplexItem`: um projeto aberto para ler o algoritmo, outro para receber o resultado. Com o código na mão, mudar o software ficou rápido; onde a mudança é entregue é outra questão.

## Crescer o que já está instalado

Uma funcionalidade nova pode ser entregue como mais um site ou aplicativo, que o usuário instala e passa a carregar, ou como extensão do software que ele já tem aberto. A segunda cobra zero curva de aprendizagem nova.

**O dado já está lá.** O plugin roda sobre as camadas do projeto aberto, no sistema de coordenadas já definido, com a simbologia já ajustada. Um aplicativo novo obriga a exportar, converter e reimportar, e essa ida e volta costuma custar mais do que a funcionalidade economiza. Na [edição de horários do SIG-Bus](/2026/08/15/sig-bus-edicao-gtfs-ajustar-horarios.html), o feed GTFS já está no QGIS quando o planejador decide atrasar as viagens da manhã.

**A plataforma já resolveu o resto.** Quem escreve dentro do QGIS herda leitura de formato, reprojeção, edição, impressão e a caixa de ferramentas de processamento sem escrever uma linha disso. Fora dele, esse resto vira o projeto inteiro.

**O ganho se acumula no mesmo lugar.** Trinta funcionalidades espalhadas por trinta aplicativos disputam a mesma atenção escassa; as mesmas trinta dentro do QGIS chegam a quem já abriu o programa hoje de manhã.

O limite disso é claro, e ignorá-lo vira regra universal: vale enquanto quem for usar o resultado já estiver dentro da plataforma. Para um gestor que nunca abriu o QGIS, empacotar a análise como plugin não entrega nada, e aí a página ou o painel é a escolha certa.

## O custo que aparece depois

Escrever a personalização ficou barato. Mantê-la não ficou. Cada uma é um fork ou um plugin que alguém carrega no tempo: o QGIS caminha da série 3.34 para a 4.x, o Qt5 vira Qt6, o NumPy 2.x quebra uma importação do GDAL que funcionava havia anos. A IA acelera escrever, e não manter, porque manter consiste em acompanhar quatro projetos que não combinaram nada entre si.

É a diferença entre o script de uma tarde e o complemento que continua instalando daqui a dois anos. Com o [Logis](/2026/08/26/logis-plugin-qgis-coleta-residuos.html), entrar no repositório oficial foi o começo do trabalho: cada versão nova do QGIS é uma chance de algo quebrar em máquina que eu não tenho como testar.

## Quem confere o resultado

Se a saída é pedir o resultado em vez de aprender a ferramenta, sobra uma pergunta: quem percebe quando o resultado saiu errado?

A própria fonte dá o vocabulário, ao separar execução de julgamento. A IA já executa bem o que tem regra definida; a decisão que depende de experiência e de responsabilidade ainda não. Em transportes o erro não fica na tela: uma setorização que o caminhão não cumpre vira hora extra e rua sem atendimento, e quem assina isso é o profissional.

Já escrevi aqui sobre [Linux com IA](/2026/08/03/linux-ia-autonomia-dependencia.html), e lá a dúvida era pessoal, sobre o que sobra depois que o problema é resolvido. Aqui ela é profissional, porque quem paga o erro não é quem o cometeu.

## O que eu faço na prática

A pergunta que eu faço antes de começar é sempre a mesma: eu quero a ferramenta ou quero o resultado?

Se o resultado é de uma vez só, script descartável, e eu não invisto um minuto em deixá-lo apresentável. Se vira rotina, vira plugin da ferramenta que já está aberta, e não coisa nova para instalar. Aí entra o segundo teste, o mais honesto: eu conseguiria manter isto sem a IA do lado? Quando a resposta é não, o que eu tenho é uma dívida com prazo indefinido.

E, virando plugin, publico no repositório oficial em vez de guardar o fork em casa. Publicado, o custo de manutenção aparece: usuário abre issue, versão nova quebra. Guardado, ele continua existindo, só que invisível, e o benefício fica parado comigo.
