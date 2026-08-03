---
layout: post
title: "Dois anos de Linux com IA: emancipação ou troca de dependência?"
lang: pt
translation: /en/2026/08/03/linux-ai-autonomy-dependency.html
category: "Geral"
image: /assets/images/posts/linux-ia-autonomia-dependencia.webp
---

Semana passada o notebook parou de voltar do suspend. Tela preta, ventilador ligado, e só um `Ctrl+Alt+F3` devolvia terminal. Colei a saída do `journalctl -b -1 -p err` numa conversa com a IA, recebi duas hipóteses em ordem de probabilidade, testei a primeira e em vinte minutos estava de volta ao trabalho. Em 2020, esse mesmo erro teria consumido uma noite de fórum e provavelmente terminado em reinstalação.

![Labirinto isométrico atravessado por um fio dourado que segue para fora do quadro](/assets/images/posts/linux-ia-autonomia-dependencia.webp)

O ganho é real e eu o uso todo dia. O que eu não sei dizer é o que ele é: a IA me deu a autonomia que eu não tinha sozinho, ou apenas trocou a dependência de um lugar por outro, mais confortável?

## Duas tentativas de Linux, com anos entre elas

Eu já tinha tentado migrar antes, mais de uma vez. O padrão era sempre o mesmo: instalava, usava bem por duas semanas, aí aparecia um problema qualquer (placa de rede, driver de vídeo, impressora) e eu caía numa busca que devolvia threads de fórum de 2014, uma resposta marcada como solução que não funcionava na minha versão e um comentário dizendo "resolvi, obrigado" sem explicar o que foi feito. Depois de algumas horas assim, eu voltava para o sistema anterior.

Hoje faz mais de dois anos que não volto. O desktop roda Pop!\_OS e o notebook roda Ubuntu, e nenhum dos dois é projeto de fim de semana: é onde o trabalho acontece. A diferença entre essas duas fases é o que este post persegue.

## O que mudou não foi o sistema

O Linux melhorou nesses anos, mas não a ponto de explicar a mudança sozinho. Placa de vídeo proprietária ainda dá trabalho, atualização de kernel ainda quebra coisa. O que encurtou de verdade foi o laço de diagnóstico. Antes eu precisava traduzir o meu erro para os termos de alguém que tinha passado por algo parecido, e torcer para a busca aproximar as duas coisas. Agora entrego a mensagem de erro exata, com a minha distribuição e a minha versão, e recebo uma hipótese que dá para testar em seguida. Errou? Colo o novo erro e continuo. A curva de aprendizagem ficou mais rápida porque cada tentativa ficou mais barata.

Isso vem com uma ressalva que não dá para omitir: a IA também devolve comando errado com a mesma segurança com que devolve o certo. Já recebi flag que não existe na versão instalada e sugestão de mexer em partição que eu não ia executar sem conferir. A verificação continua sendo minha, e quem não verifica troca uma noite de fórum por um `rm` mal explicado.

## Linux empurra para o software livre

Tem um efeito colateral do Linux que eu demorei a valorizar. Quando o sistema é livre, a solução que aparece primeiro também costuma ser: em vez de comprar a licença, você procura o pacote, o script, o plugin. É o mesmo terreno de onde sai boa parte do que eu publico aqui, QGIS e Python: quem já leu documentação de plugin para resolver um problema de projeção não estranha ler `man` de utilitário de sistema.

## Emancipação ou troca de dependência?

A leitura otimista tem um argumento forte. Hoje eu escolho o sistema operacional pelo que ele faz por mim, e não pelo tamanho do prejuízo se algo quebrar. Essa escolha antes não estava disponível: o medo de ficar preso num erro me mantinha onde estava. Ganhar acesso a uma decisão que antes era proibitiva se parece bastante com autonomia.

A leitura desconfiada tem um argumento igualmente forte. O StackOverflow saiu de cena e a IA entrou no lugar, e a segunda é mais confortável, o que a torna mais difícil de enxergar como dependência. Há uma diferença concreta entre as duas. A resposta do fórum vinha grudada no problema de outra pessoa: o contexto era diferente do meu, a versão era outra, e eu era obrigado a entender o suficiente para adaptar. Esse trabalho de tradução era chato e era exatamente onde eu aprendia. A resposta da IA chega pronta para o meu caso exato, o que elimina o atrito e, junto com ele, elimina a obrigação de entender.

Não tenho um veredito. As duas leituras descrevem bem o que acontece comigo.

## O critério que eu uso

Sem veredito, sobra um teste prático, que eu aplico depois de resolver o problema: sobrou algo reutilizável ou só um comando colado? Se amanhã eu souber refazer aquilo sozinho, ou pelo menos souber onde procurar, foi aprendizado. Se eu não souber nem dizer o que o comando fez, foi só o problema saindo da frente.

Na prática isso vira dois hábitos pequenos. Pedir o porquê junto com o comando, porque a explicação é a parte que fica. E conferir o que o comando faz antes de rodar, porque a verificação é o que separa usar de obedecer.

## O mesmo dilema na sala de aula

No CEFET-MG a pergunta chega em outro formato, com código e trabalho entregue, e ali ela pesa mais. Vejo uma diferença que importa entre dois usos: quem já entende o assunto usa a IA para ir mais rápido no que já sabe fazer, e quem ainda não entende usa para pular justamente a parte que ensina. O comando funciona nos dois casos e o trabalho entregue é parecido. O que muda é o que sobra depois.

Continuo sem resposta fechada, para mim e para eles. Por enquanto o que tenho é o critério: olhar para o que ficou depois que o problema foi resolvido.
