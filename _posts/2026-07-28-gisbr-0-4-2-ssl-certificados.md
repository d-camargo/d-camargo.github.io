---
layout: post
title: "GisBR 0.4.2: certificados SSL para instalações novas de Windows/OSGeo4W"
lang: pt
category: "Geoprocessamento"
translation: /en/2026/07/28/gisbr-0-4-2-ssl-certificados.html
---

Alguém instala o QGIS do zero via OSGeo4W, abre o GisBR e tenta baixar qualquer camada oficial. A resposta é `unable to find issuer certificate`. Não é falta de internet nem instabilidade do servidor: é a cadeia de confiança SSL que o Windows recém-instalado não reconhece. A 0.4.2 fecha essa lacuna, mas ela é a terceira correção de infraestrutura desde a 0.3.2, e vale contar as três.

![Ícone do plugin GisBR](/assets/images/posts/gisbr-cover.webp)

## Duas correções silenciosas: 0.4.0 e 0.4.1

Depois da 0.3.2, publicada sem o rótulo experimental, vieram duas versões que não geraram post próprio porque eram pontuais. A 0.4.0 declarou compatibilidade explícita com o QGIS 4.x. A 0.4.1 corrigiu um bug mais sutil: a busca pelo diretório de cache usava o enum `QStandardPaths.CacheLocation` sem escopo, o que quebra no PyQt6 e derrubava a lista de municípios com o erro genérico "catálogo do geobr indisponível". O mesmo problema afetava a checagem de erro de rede do Overpass. As duas correções foram escopar o enum corretamente, além de fazer a mensagem de erro do catálogo mostrar a exceção real e o caminho de cache cair para o CSV offline embarcado em vez de abortar.

## O SSL que só cobria metade dos casos

Desde a 0.3.0, o GisBR já embarcava a cadeia de certificados do IPEA para contornar falhas de SSL no Windows, mas essa injeção estava presa ao downloader do geobr. Fazia sentido enquanto a única fonte HTTPS própria do plugin era o IPEA. O problema é que o diagnóstico municipal já consulta bem mais serviços: WFS e ArcGIS REST de fontes como SICAR, ANA/SNIRH, INDE, SGB e IBAMA, a API Overpass do OSM e o basemap de satélite. Em instalações novas do OSGeo4W, sem os certificados raiz que uma instalação de sistema mais antiga acumula, cada um desses serviços podia falhar com o mesmo erro de cadeia de certificado, e nenhum deles tinha o fallback que só existia para o IPEA.

A 0.4.2 move essa lógica para um módulo único, `core/ssl_support.py`, e aplica a mesma injeção de certificados aos conectores WFS, ArcGIS REST e Overpass, além da configuração SSL padrão usada pelo basemap XYZ. O plugin agora embarca as raízes autoassinadas usadas pelo espelho no GitHub, SICAR, ANA/SNIRH, INDE, SGB, IBAMA, Overpass e o basemap de satélite, todas num só lugar em vez de espalhadas pelo código.

Importante: os certificados são adicionados como âncoras de confiança adicionais, não como uma forma de contornar a verificação. Nenhuma configuração de verificação é relaxada, o plugin apenas passa a reconhecer cadeias que o Windows recém-instalado ainda não conhece. E quando uma requisição falha mesmo assim, a mensagem de erro agora inclui o host e a exceção original, não mais um aviso genérico de "erro de conexão".

A 0.4.2 já está disponível no repositório oficial de complementos do QGIS. O código é GPL-3.0 e está no [GitHub](https://github.com/d-camargo/gisbr). Se você instalar o GisBR numa máquina nova e ainda assim ver erro de certificado em algum serviço, abra uma issue com o host que falhou: é provável que falte alguma raiz nesse módulo.
