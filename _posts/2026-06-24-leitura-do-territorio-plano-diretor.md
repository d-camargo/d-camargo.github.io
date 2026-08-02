---
layout: post
title: "Leitura do Território: como diagnosticar a cidade real com dados abertos"
lang: pt
translation: /en/2026/06/24/reading-the-territory-master-plan.html
category: "Planejamento Urbano"
image: /assets/images/leitura_territorio.webp
---

A Leitura do Território é a etapa do Plano Diretor que troca a cidade idealizada no papel pela cidade que existe. São nove mapeamentos temáticos que viram diagnóstico, e este post mostra cada um deles com as bases de dados abertos que alimentam o mapa.

![Mapeamentos temáticos sobrepostos à malha de um território municipal](/assets/images/leitura_territorio.webp)

Já descrevi [as cinco etapas de elaboração do Plano Diretor](/2026/06/24/passo-a-passo-plano-diretor.html); a Leitura do Território é a segunda delas, e a que mais depende de geoprocessamento. O objetivo é **espacializar** os problemas: cruzar dados técnicos com a vivência da comunidade para descobrir com exatidão *onde* cada fenômeno acontece.

Essa leitura se apoia em dois tipos de levantamento. Os **básicos** são essenciais para municípios de qualquer porte e usam dados secundários (Censos do IBGE, MapBiomas) ou cadastros da própria prefeitura. Os **complementares** não são obrigatórios, mas aprofundam a análise e apontam caminhos mais especializados. Ambos exigem uma base cartográfica preferencialmente georreferenciada, organizada nos mapeamentos temáticos a seguir.

## 1. Mapeamento regional

**Básico:** localiza o sistema viário regional, os núcleos urbanos, as bacias hidrográficas e as Unidades de Conservação de impacto regional. **Complementar:** identifica fluxos e vínculos de emprego, educação e saúde entre municípios vizinhos, além de infraestruturas compartilhadas como aterros e represas.

**Fontes abertas:** IBGE (malhas municipais e a Base Cartográfica Contínua – BCIM); o estudo **REGIC** do IBGE para os fluxos e vínculos entre cidades; ANA/SNIRH para bacias hidrográficas; o Cadastro Nacional de Unidades de Conservação (MMA/ICMBio); e o OpenStreetMap ou o DNIT para o sistema viário.

## 2. Evolução da ocupação no território

**Básico:** por fotos aéreas comparativas em diferentes anos, mapeia o avanço da mancha urbana e novas ocupações rurais, inclusive áreas irregulares. **Complementar:** avalia a morfologia dessa ocupação (verticalização, densidade construtiva) e o avanço da fronteira agrícola.

**Fontes abertas:** a série histórica do **MapBiomas** (cobertura e uso do solo desde 1985) é o caminho mais direto; o INPE/TerraBrasilis para desmatamento e queimadas; e imagens Sentinel (Copernicus) e Landsat (USGS) para composições próprias entre datas.

## 3. Caracterização da população

**Básico:** identifica a concentração populacional e a distribui por faixas de renda, gênero, raça/cor e idade, mapeando também a presença de pessoas em situação de rua. **Complementar:** investiga a percepção das pessoas sobre segurança, iluminação e acesso a serviços.

**Fontes abertas:** o **Censo Demográfico do IBGE**, em especial a Base de Informações por Setor Censitário (o nível espacial mais fino disponível) e o SIDRA para os agregados; o CadÚnico (MDS) ajuda a localizar população de baixa renda e em situação de rua.

## 4. Uso e ocupação do solo

**Básico:** mapeia densidade populacional, lotes e glebas vazias (vazios urbanos), padrão construtivo (gabarito) e sobrepõe essas áreas ao sistema hidrográfico e às áreas de extração. **Complementar:** avança sobre chácaras de veraneio, terras públicas, situação fundiária e perfil das fachadas.

**Fontes abertas:** os setores censitários do IBGE para densidade; o cadastro imobiliário municipal (IPTU) para lotes e gabarito; o MapBiomas para uso do solo; a ANA/SNIRH para hidrografia; e o **SIGMINE da ANM** para concessões e áreas de extração mineral.

## 5. Condições de infraestrutura

**Básico:** levanta o alcance e a capacidade das redes de água, esgoto, coleta de resíduos, iluminação pública e equipamentos (escolas, hospitais, praças), revelando sobretudo as *áreas não cobertas*. **Complementar:** localiza drenagem, falhas de telecomunicações, pontos viciados de descarte e áreas de alagamento crônico.

**Fontes abertas:** o **SNIS** para água, esgoto, resíduos e drenagem; o CNES/DATASUS para estabelecimentos de saúde; o Censo Escolar do INEP (e o QEdu) para escolas; e os dados abertos da **ANATEL** para cobertura de telecomunicações.

## 6. Sistema ambiental e serviços ecossistêmicos

**Básico:** usa o Cadastro Ambiental Rural (CAR) e imagens de satélite para localizar nascentes, matas, Áreas de Preservação Permanente (APPs) e parques. **Complementar:** mapeia áreas degradadas, cartas geotécnicas e as áreas responsáveis pelos principais serviços ecossistêmicos do município.

**Fontes abertas:** o **SICAR** (base do CAR, com APPs, Reserva Legal e hidrografia dos imóveis); o MapBiomas e o MapBiomas Água para cobertura e recursos hídricos; e o **Serviço Geológico do Brasil (SGB/CPRM)** para cartas geotécnicas e de suscetibilidade.

## 7. Condições de mobilidade

**Básico:** mapeia a hierarquia viária, linhas e pontos de ônibus, áreas servidas e não servidas por transporte coletivo, ciclovias e rotas acessíveis. **Complementar:** mapeia o fluxo de transporte de cargas e os pontos de maior incidência de acidentes.

**Fontes abertas:** o **OpenStreetMap** para viário, ciclovias e equipamentos; os feeds **GTFS** publicados nos portais municipais de dados abertos para o transporte coletivo; e, para acidentes, os portais municipais/estaduais ou os dados abertos da PRF (rodovias federais) e do RENAEST/SENATRAN.

## 8. Condições de moradia

**Básico:** espacializa assentamentos precários, favelas, cortiços e loteamentos irregulares, cruzando-os com áreas de risco e déficit habitacional. **Complementar:** identifica onde houve produção de moradia de baixa renda na última década, a oferta de terra barata e o padrão construtivo dessa habitação.

**Fontes abertas:** os **Aglomerados Subnormais do IBGE** para favelas e assentamentos precários; a **Fundação João Pinheiro** para o déficit habitacional municipal; e o SGB/CPRM com o CEMADEN para as áreas de risco geológico e hidrológico.

## 9. Emissões e riscos climáticos

**Complementar:** mapeia as principais fontes emissoras de gases de efeito estufa (GEE) do município nos setores de energia, uso da terra, agropecuária, indústria e resíduos, orientando ações de mitigação.

**Fontes abertas:** o **SEEG** (estimativas de emissões por município e por setor); o MapBiomas para as mudanças de uso da terra; e o **AdaptaBrasil (MCTI)** para índices de risco e vulnerabilidade climática.

## Do mapa ao Quadro-Síntese

A consolidação desses nove mapeamentos, somada aos debates comunitários, produz o **Quadro-Síntese da Leitura do Território**: o diagnóstico espacial que aponta objetivamente onde estão os problemas a enfrentar na etapa de propostas. Vale um lembrete prático: cada base abre em escala, recorte e data de referência diferentes; padronizar o sistema de coordenadas, o ano-base e a unidade territorial é metade do trabalho antes que qualquer mapa faça sentido.

Se você vai montar a base cartográfica de uma Leitura do Território e quer trocar ideia sobre como cruzar essas fontes no QGIS, é só chamar por e-mail ([eng.dcamargo@outlook.com.br](mailto:eng.dcamargo@outlook.com.br)) ou por [WhatsApp](https://wa.me/553135653353).

---

### Referência

MINISTÉRIO DO DESENVOLVIMENTO REGIONAL; MINISTÉRIO DO MEIO AMBIENTE. *Guia para Elaboração e Revisão de Planos Diretores*. [S.l.: s.n., 2022].
