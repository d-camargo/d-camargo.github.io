---
layout: post
title: "Como apurar o Ideb da rede federal quando o INEP não publica essa série"
lang: pt
translation: /en/2026/08/22/ideb-ensino-medio-rede-federal-painel.html
category: "Geral"
image: /assets/images/posts/ideb-ensino-medio-rede-federal-painel.webp
---

Entre 2019 e 2025 a média do Ideb do ensino médio subiu nas escolas estaduais e caiu nas escolas federais que apurei num painel balanceado (explico o método adiante): de 4,17 para 4,53 na rede estadual, de 5,63 para 5,42 na federal. Os dois movimentos têm a mesma causa, e essa causa não é a nota do Saeb.

![Duas curvas diagramáticas lado a lado, uma subindo e outra caindo, movidas pelo mesmo mecanismo dourado de catraca entre elas](/assets/images/posts/ideb-ensino-medio-rede-federal-painel.webp)

## O que o Ideb é, de fato

O Ideb é um produto: $Ideb = P \times N$. $N$ é a nota padronizada do Saeb em Português e Matemática. $P$ é o indicador de rendimento, que o INEP deriva das taxas de aprovação registradas no Censo Escolar. A planilha de divulgação do INEP traz $P$ e a taxa de aprovação bruta em colunas distintas, `VL_INDICADOR_REND` e `VL_APROVACAO`, e elas divergem: na rede estadual de Minas Gerais em 2021, $P$ = 0,8769 contra uma aprovação bruta de 91,3%. O que entra na identidade do índice é $P$, não a aprovação bruta que sai direto do Censo. É uma diferença pequena na maioria dos anos, mas é real, e confundir as duas colunas é o primeiro jeito de errar essa conta.

## O problema: o INEP não publica esse número

Quem quer o Ideb do ensino médio de uma rede estadual por UF encontra o número pronto na aba "UF e Regiões (EM)" da planilha de divulgação. Quem quer o mesmo número para a rede federal não encontra: essa aba só traz Total, Privada e Estadual. A rede federal simplesmente não tem linha ali. Nas duas planilhas de divulgação que uso aqui, o jeito de chegar num Ideb da rede federal é apurar escola a escola, na aba de divulgação por escola. Não conferi se alguma outra planilha do INEP, fora dessas duas, traz a rede federal já agregada.

## A armadilha da média direta

Isso parece resolvido com uma média simples das escolas federais que o INEP publicou naquele ano. Não é. Cobertura de escolas federais com Ideb divulgado, no Brasil: 135 em 2017, 151 em 2019, 35 em 2021, 157 em 2023, 236 em 2025. Em Minas Gerais: 21, 18, 4, 21, 37. Uma escola só tem Ideb publicado quando bate o mínimo de participantes no Saeb e o mínimo de conclusão do ciclo, e esse conjunto de escolas muda de composição a cada edição. A queda para 35 escolas em 2021, no Brasil todo, é a pandemia derrubando participação, não a rede federal encolhendo.

Uma média que mistura conjuntos diferentes de escola a cada ano não mede a evolução da rede: mede a composição de quem divulgou naquele ano. É a mesma razão pela qual já é proibido, nesta apuração, publicar a média anual agregada das unidades do CEFET-MG (nenhuma das 9 tem série completa nas 5 edições, e a composição de quem divulga muda ano a ano). O problema é o mesmo, só que em escala nacional.

## O método: painel balanceado e decomposição Shapley

A saída é restringir a comparação às escolas que têm dado divulgado nos dois anos comparados, um painel balanceado. Isso descarta a maior parte das 596 escolas federais listadas alguma vez (sobram 70 no recorte 2019 a 2025, no Brasil), mas garante que a variação medida vem da mesma escola nos dois pontos, não da entrada e saída de escolas na amostra.

Com o painel fechado, decomponho a variação do índice entre os dois fatores da identidade usando a decomposição Shapley do produto, que reparte a variação de $P \times N$ em duas parcelas que somam exatamente a variação observada:

$$efeito\_fluxo = (P_1 - P_0) \times \frac{N_0 + N_1}{2}$$

$$efeito\_aprendizagem = (N_1 - N_0) \times \frac{P_0 + P_1}{2}$$

A primeira isola o quanto do produto mudou porque a aprovação mudou, com a nota fixada na média dos dois anos; a segunda isola o quanto mudou porque a nota mudou, com a aprovação fixada na média. As duas somadas fecham com a variação do produto $P \times N$, sem resíduo.

## Testando o método antes de usar

Antes de aplicar esse painel a um dado que o INEP não publica, testei ele contra um dado que o INEP publica: a série oficial estadual de Minas Gerais, calculada pelo próprio INEP sobre toda a rede, e já decomposta anteriormente nesta apuração. Se o painel balanceado reproduzir a decomposição oficial dentro de uma margem pequena, o método não está distorcendo a leitura ao restringir a amostra.

No intervalo 2017 a 2025, o painel estadual mineiro devolve 79,2% de efeito fluxo, contra 80,6% na série oficial do INEP. No intervalo 2019 a 2025, devolve 104,5%, contra 106,4% oficial. A diferença fica abaixo de 2 pontos percentuais nos dois casos. É assim que se valida um método antes de usar num recorte que não tem contraponto oficial para conferir.

## O resultado: Brasil, 2019 a 2025

Com o método validado, aplico o mesmo painel ao recorte que motivou a apuração: o Ideb do ensino médio da rede federal no Brasil, que o INEP não publica como série.

| Rede (painel) | Ano | Ideb médio | P (indicador) | Aprovação bruta | Nota Saeb (N) |
|---|---|---|---|---|---|
| Federal (70 escolas) | 2019 | 5,63 | 0,9203 | 92,03% | 6,10 |
| Federal (70 escolas) | 2025 | 5,42 | 0,9362 | 93,62% | 5,79 |
| Estadual (10.713 escolas) | 2019 | 4,17 | 0,8930 | 89,30% | 4,65 |
| Estadual (10.713 escolas) | 2025 | 4,53 | 0,9622 | 96,22% | 4,70 |

E a decomposição Shapley do produto $P \times N$ em cada rede:

| Rede | Efeito fluxo | % do total | Efeito aprendizagem | % do total |
|---|---|---|---|---|
| Federal | +0,0943 | -46,8% | -0,2959 | 146,8% |
| Estadual | +0,3238 | 88,8% | +0,0407 | 11,2% |

A leitura é a mesma nas duas redes, e é o ponto central deste post: onde a aprovação ainda tinha folga para subir, o índice subiu com a nota do Saeb praticamente parada (na estadual, quase 90% do ganho vem do fluxo). Onde a aprovação já estava perto do teto, como na rede federal, a folga acabou, e a queda da nota apareceu quase inteira no índice: o efeito aprendizagem negativo (-0,2959) é maior em módulo do que a própria queda do produto, porque o fluxo ainda puxou um pouco para cima e não foi suficiente para compensar.

## As ressalvas, sem suavizar

Este número não é o Ideb oficial da rede federal, por cinco motivos concretos:

**Não é ponderado por aluno.** O que o painel calcula é a média simples do Ideb entre escolas. O Ideb oficial que o INEP publica para uma rede sai do conjunto dos alunos da rede, não da média das escolas. São contas diferentes, e a média simples pode se afastar quando escolas grandes e pequenas se comportam de forma diferente.

**Viés de seleção.** O painel usa 70 das 596 escolas federais já listadas em alguma edição. São as escolas que conseguiram manter divulgação nos dois anos comparados, o que já é, em si, uma característica não aleatória.

**O painel federal de Minas Gerais não entra nesta comparação.** Tem 10 escolas no recorte 2019 a 2025, abaixo do que dá para tratar como representativo, e por isso ficou fora.

**Composição do painel federal nacional.** Das 70 escolas, 63 são institutos federais, CEFETs ou escolas técnicas vinculadas a universidades; 5 são colégios de aplicação ou correlatos; 2 são colégios militares. Excluir os dois colégios militares do cálculo não muda o resultado.

**2021 fica fora de qualquer comparação.** A pandemia inflou artificialmente o indicador de fluxo em praticamente todas as redes, com aprovação automática e participação reduzida no Saeb, o que torna qualquer leitura que inclua 2021 como ponto de comparação não confiável.

## O que fica

O índice mede duas coisas, e só uma delas é aprendizado. É possível subir o Ideb sem subir o aprendizado, e a rede estadual fez exatamente isso entre 2019 e 2025. É possível também que a nota caia e o índice caia junto, mesmo com a aprovação subindo, porque a folga do fluxo já tinha acabado: foi o que aconteceu na rede federal. As duas coisas são o mesmo mecanismo visto de dois pontos de partida diferentes, e nenhuma das duas aparece se a leitura para no número publicado sem abrir o produto.

---

*Fonte: INEP, planilha de divulgação do Ideb por escola do ensino médio, edição 2025 (`divulgacao_ensino_medio_escolas_2025.xlsx`, aba "IDEB_Escolas (ENSINO MÉDIO)"). O arquivo bruto tem sha256 registrado e a apuração, incluindo o painel balanceado e a decomposição Shapley, é reprodutível a partir dele.*
