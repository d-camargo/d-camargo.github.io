---
layout: post
title: "Sioux Falls e o Frank-Wolfe: alocação de equilíbrio no Desire Lines"
lang: pt
category: "Engenharia de Transportes"
image: /assets/images/posts/desire-lines-frank-wolfe-sioux-falls.webp
translation: "/en/2026/10/30/desire-lines-frank-wolfe-sioux-falls.html"
---

Alocação de equilíbrio é o problema que as ferramentas de planejamento de transporte resolvem quando levam o congestionamento em conta. O artigo de LeBlanc, Morlok e Pierskalla, de 1975, mostrou como calculá-la em uma rede viária, e a rede que ele usa, Sioux Falls, virou o teste em que as implementações se medem. A versão 0.7.1 do **Desire Lines** passou a alocar por equilíbrio com o algoritmo de Frank-Wolfe, e validei o resultado nessa mesma rede.

![Rede de Sioux Falls desenhada com linhas de fluxo de espessura variável sobre fundo escuro](/assets/images/posts/desire-lines-frank-wolfe-sioux-falls.webp)

## Por que o artigo de 1975 importa

A história até ele tem quatro passos:

- **1952:** Wardrop enuncia o princípio do equilíbrio do usuário: nenhum motorista reduz seu tempo de viagem trocando de rota sozinho.
- **1956:** Beckmann, McGuire e Winsten mostram que esse equilíbrio é a solução de um problema de otimização convexa. Ortúzar e Willumsen (2011) resumem a continuação: o princípio data de 1952, a formulação matemática veio quatro anos depois, e "it took several more years" até surgirem algoritmos adequados à prática.
- **1956:** Frank e Wolfe publicam um algoritmo de programação não linear.
- **1975:** LeBlanc, Morlok e Pierskalla (*Transportation Research* 9, 309-318) aplicam o Frank-Wolfe à formulação de Beckmann e mostram que o equilíbrio em rede viária é calculável. O caso de teste é Sioux Falls.

Depois disso, a rede ficou. Ela está na coleção pública **Transportation Network Test Problems** (TNTP, de Hillel Bar-Gera), mantida no repositório [bstabler/TransportationNetworks](https://github.com/bstabler/TransportationNetworks/tree/master/SiouxFalls). O README da coleção diz que a rede "was used in many publications" e que serve para depurar código ("good for code debugging"). É esse o uso que faço dela aqui.

## O problema e a rede

Com congestionamento, o tempo de viagem depende do fluxo no link, e o fluxo depende do tempo, porque os motoristas escolhem rota pelo tempo. O **tudo-ou-nada** (AoN) ignora essa volta: carrega toda a demanda no caminho mais curto em fluxo livre. Serve de diagnóstico de onde faltaria capacidade, mas não é um equilíbrio.

O **Frank-Wolfe** (FW) resolve a volta iterando. Em cada iteração, ele carrega tudo-ou-nada com os tempos atuais, o que dá uma direção, e decide quanto andar nela por uma **busca linear** sobre a função de Beckmann. Ortúzar e Willumsen descrevem o mesmo mecanismo: o último tudo-ou-nada fornece uma direção de descida. O **MSA** (médias sucessivas) usa a mesma direção, mas anda um passo fixo de 1/k na iteração k, sem busca.

O tempo em cada link segue a função **BPR**, com os parâmetros usuais da coleção:

`t = t0 · (1 + 0,15 · (v/c)^4)`

em que `t0` é o tempo em fluxo livre, `v` o volume e `c` a capacidade.

Os fatos da rede, conforme o README do TNTP:

- 24 zonas e nós, 76 links direcionados, 528 pares O/D com demanda e 360.600 viagens.
- A própria coleção avisa que a rede "is not considered as a realistic one".
- As coordenadas dos nós foram geradas artificialmente para reproduzir o diagrama do artigo.
- A demanda do artigo (Tabela 1) está em milhares de veículos por dia. No TNTP ela foi multiplicada por 100, o que equivale a 0,1 do fluxo diário, e pode ser lida como fluxo horário aproximado.
- Os tempos de fluxo livre estão em 0,01 h.
- Existem outras versões, ligeiramente diferentes, da rede em outras publicações. Por isso a comparação abaixo é com a versão TNTP, e não "com o artigo".

![Rede de Sioux Falls com 24 nós numerados e 76 links direcionados desenhados em pares; a espessura de cada link é proporcional à sua capacidade](/assets/images/posts/desirelines01/1.webp)

*Figura 1. A rede. Cada par de linhas é um par de links de sentidos opostos. A espessura é a capacidade, e a legenda mostra quatro valores de referência (5.000, 10.000, 20.000 e 25.000).*

A figura 2 mostra a mesma rede com a demanda por cima. Essas são as **linhas de desejo**, o mesmo conceito que apareceu no [post sobre a matriz Origem e Destino](/2026/10/27/matriz-origem-e-destino-como-ler-a-tabela-e-quando-empilhar.html): a linha de desejo mostra para onde as pessoas querem ir, e a alocação mostra por onde elas vão.

![Linhas de desejo de Sioux Falls: retas entre os 24 nós, com espessura e opacidade crescentes com o número de viagens entre cada par; as mais grossas se concentram em torno do nó 10](/assets/images/posts/desirelines01/2.webp)

*Figura 2. Linhas de desejo. Cada reta liga um par de zonas, somando as viagens de ida e de volta. A espessura é o número de viagens do par (legenda: 200, 800, 1.600 e 2.400).*

## O Desire Lines nessa temática

O painel **Alocação em rodovias** do plugin oferece três métodos: AoN, MSA e Frank-Wolfe. O FW é o padrão do painel, com 100 iterações e gap relativo de 0,001. Antes da versão 0.7, o padrão eram 10 iterações de MSA.

A figura 3 é o resultado do FW com 100 iterações na rede de Sioux Falls.

![Rede de Sioux Falls com o fluxo alocado pelo Frank-Wolfe em 100 iterações; a espessura do link é o volume e a cor vai do cinza claro ao marrom escuro conforme a razão volume/capacidade](/assets/images/posts/desirelines01/3.webp)

*Figura 3. Fluxo alocado pelo FW em 100 iterações. A espessura é o volume (legenda: 2.000, 5.000, 10.000 e 20.000, na unidade da demanda do TNTP, lida como fluxo horário aproximado) e a cor é a razão v/c, de 0 a 2,56 na barra de cores. A maior razão aparece nos links entre os nós 6 e 8.*

### Validação contra a solução de referência

Para cada link, o erro é `|v − vref| / vref`, com `vref` tirado da solução de referência do TNTP (`SiouxFalls_flow.tntp`). O tempo total de viagem no sistema (TSTT) de referência é 7.480.225.

| Cenário | Erro máximo | Erro médio | TSTT | Gap relativo |
|---|---|---|---|---|
| MSA, 10 iterações (padrão anterior) | 69,6 % | 13,7 % | 9.342.350 | 0,102 |
| MSA, 100 iterações | 8,9 % | 1,5 % | 7.622.065 | 0,0092 |
| Frank-Wolfe, 50 iterações | 5,3 % | 0,96 % | 7.484.340 | 0,0031 |
| **Frank-Wolfe, 100 iterações (padrão)** | **2,3 %** | **0,46 %** | **7.476.227** | **0,0014** |
| Frank-Wolfe, 300 iterações | 0,71 % | 0,14 % | 7.478.543 | 0,0004 |

A figura 4 põe lado a lado o erro por link do padrão anterior e do padrão atual.

![Dois mapas de Sioux Falls lado a lado com o erro por link: à esquerda MSA com 10 iterações, com muitos links em marrom escuro; à direita Frank-Wolfe com 100 iterações, quase todos em cinza claro](/assets/images/posts/desirelines01/4.webp)

*Figura 4. Erro por link contra a solução de referência. A escala vai de 0 a 10 %, e valores acima disso aparecem na cor do extremo da barra. À esquerda, MSA com 10 iterações (erro máximo 69,6 %, médio 13,7 %). À direita, Frank-Wolfe com 100 iterações (erro máximo 2,3 %, médio 0,46 %).*

Um detalhe do gap. Com 100 iterações, o FW termina com gap de 0,0014, acima da tolerância de 0,001. Quem encerra a execução no padrão do painel é o limite de iterações, e não a tolerância. Nesta rede, o gap do FW passa pela primeira vez de 0,001 para baixo na iteração 132. Ele não decresce de forma monótona: oscila de uma iteração para outra, como se vê na figura 5.

![Gráfico do gap relativo em escala logarítmica contra a iteração k, de 1 a 300, para MSA em cinza e Frank-Wolfe em dourado, com uma linha tracejada em 10 elevado a menos 3](/assets/images/posts/desirelines01/5.webp)

*Figura 5. Convergência. Eixo x: iteração k. Eixo y: gap relativo em escala logarítmica. A linha tracejada marca 10⁻³, a tolerância padrão do painel.*

### Quantas iterações a menos

Em vez de repetir um fator da documentação, medi nas séries de gap das duas execuções de 300 iterações:

- O FW chega a gap 0,0031 na iteração 50. O MSA só chega a esse nível na iteração 297, cerca de 6 vezes mais.
- O FW com 100 iterações tem gap 0,0014. O MSA, ao fim de 300 iterações, está em 0,0031, mais que o dobro, e nunca alcança 0,0014 dentro das 300.

O que isso diz vale para esta rede e para este critério (o gap). Em outras redes a razão pode mudar.

## Limites do Frank-Wolfe

Ortúzar e Willumsen descrevem o comportamento que a figura 5 mostra: o Frank-Wolfe "tends to converge rapidly over early iterations but less so as it starts to approach the optimum", e os fluxos nos links tendem a oscilar entre iterações, o que dificulta a precisão final. Os mesmos autores apresentam alternativas que trabalham no espaço dos fluxos por caminho, como o algoritmo de projeção de gradiente de Jayakrishnan et al. (1994), e dizem que elas têm melhores propriedades de convergência em redes grandes e congestionadas. O Desire Lines hoje oferece AoN, MSA e FW. Não há método baseado em caminho no plugin, e este post não promete um.

## Uma lição de preparo de dados

O erro nem sempre vem do algoritmo. A seção 6 da documentação de métodos registra um caso: com os mesmos dados do TNTP e a mesma configuração, tratar **cada feição como mão dupla** em vez de mão única leva o erro máximo a 73,6 %, o erro médio a 19,4 % e o TSTT a 3.743.234, cerca de metade do valor de referência.

O motivo é a capacidade. A rede do TNTP já traz os dois sentidos como links separados, 38 pares de links opostos. Se o plugin gera os dois sentidos para cada feição, cada sentido passa a ter dois arcos paralelos, com a mesma capacidade, e a capacidade efetiva dobra. Com o dobro de capacidade, o tempo de viagem cai e o TSTT cai junto.

No QGIS, confira o **campo de sentido** da camada de rodovias antes de alocar. O plugin lê `mao_unica` (também reconhece `oneway`, `one_way` e `sentido_unico`). Se for verdadeiro, gera só o arco no sentido da geometria. Se for falso, gera os dois sentidos. Uma malha que já veio com um registro por sentido precisa estar marcada como mão única.

## Reproduzir e conferir

Os dados e o teste estão no repositório do plugin, em [github.com/d-camargo/desire_lines](https://github.com/d-camargo/desire_lines): a rede em `test/data/sioux_falls` e o teste em `test/test_sioux_falls_ue.py`. O teste roda o FW com 300 iterações e o MSA com 500, e compara com a solução de referência, com tolerâncias de 2 % no erro máximo, 0,5 % no erro médio e 0,5 % no TSTT para o FW. Se uma mudança no código piorar o resultado, o teste falha. É o benchmark como contrato.

## Próximo passo

Sioux Falls é um laboratório. O próximo passo é rodar o mesmo motor sobre a malha real que o GisBR entrega, descrita no [post sobre redes de transporte e alocação](/2026/10/17/gisbr-redes-transporte-roteamento-alocacao.html). Esse é o assunto do próximo post.

A versão 0.7.1 está disponível no repositório do plugin no GitHub, e a [documentação](https://desirelines.dcamargo.com.br) descreve o painel.

## Referências

- Wardrop, J. G. (1952). Some theoretical aspects of road traffic research. *Proceedings of the Institution of Civil Engineers*, Part II, 1, 325-378.
- Beckmann, M., McGuire, C. B., Winsten, C. B. (1956). *Studies in the Economics of Transportation*. Yale University Press.
- Frank, M., Wolfe, P. (1956). An algorithm for quadratic programming. *Naval Research Logistics Quarterly*, 3, 95-110.
- LeBlanc, L. J., Morlok, E. K., Pierskalla, W. P. (1975). An efficient approach to solving the road network equilibrium traffic assignment problem. *Transportation Research*, 9, 309-318.
- Ortúzar, J. de D., Willumsen, L. G. (2011). *Modelling Transport*. Wiley.
- Bar-Gera, H. *Transportation Network Test Problems* (TNTP). Repositório [bstabler/TransportationNetworks](https://github.com/bstabler/TransportationNetworks), pasta SiouxFalls.
