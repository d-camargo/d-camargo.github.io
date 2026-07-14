---
layout: post
title: "Desire Lines 0.3.2: interface em português e compatibilidade com QGIS 4.x (Qt6)"
lang: pt
translation: /en/2026/07/14/desire-lines-pt-br-qt6-qgis4.html
category: "Engenharia de Transportes"
---

O plugin Desire Lines ganhou duas atualizações que mudam quem consegue usá-lo e onde. A interface agora está traduzida para português e o mesmo pacote passou a rodar tanto no QGIS 3.x quanto no QGIS 4.x, que migrou de Qt5 para Qt6.

![Mapa de Fluxo com Desire Lines](/assets/images/desire_lines_flow_map.png)

## Interface em português

As 42 strings da interface (rótulos, mensagens de erro, dicas de campo) foram traduzidas para PT-BR. Não há nada para configurar: o plugin segue o idioma definido no próprio QGIS. Quem já usa o QGIS em português vê o Desire Lines em português automaticamente; quem prefere inglês continua vendo a interface original, sem nenhuma opção extra para procurar nos menus.

## Compatibilidade com QGIS 4.x (Qt6)

O QGIS 4 trocou sua base gráfica de Qt5 para Qt6, o que quebra plugins que dependem de enums não escopados do PyQt (a forma antiga de referenciar constantes da biblioteca gráfica). O Desire Lines foi ajustado para usar a sintaxe escopada, compatível com as duas versões do Qt, e o arquivo de recursos gráficos que carregava PyQt5 de forma fixa foi removido.

O resultado é um único código-fonte que passa na suíte de testes tanto no QGIS 3.44 (Qt5) quanto no QGIS 4.2 (Qt6), sem builds separados para cada versão.

## Bastidores do empacotamento

Duas correções silenciosas, mas relevantes para quem instala pelo repositório oficial:

* **A tradução realmente vai no pacote.** O arquivo compilado da tradução (`.qm`) estava fora do controle de versão por engano, então os zips publicados nunca continham a interface em português, mesmo com as strings já traduzidas.
* **O pacote encolheu de ~14 MB para ~200 KB.** A pasta de exemplos (dados de demonstração da RMSP) e os testes automatizados saíram do zip publicado; eles continuam disponíveis no repositório do GitHub para quem quiser reproduzi-los.

## Como atualizar

No QGIS, acesse **Complementos > Gerenciar e Instalar Complementos**, localize **Desire Lines** e aplique a atualização disponível. Quem instala pela primeira vez encontra o plugin pelo mesmo caminho, já na versão 0.3.2.

Para acompanhar o desenvolvimento ou reportar problemas, o código-fonte está no [repositório oficial do Desire Lines no GitHub](https://github.com/d-camargo/desire_lines).
