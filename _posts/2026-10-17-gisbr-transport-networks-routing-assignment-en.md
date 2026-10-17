---
layout: post
title: "GisBR: transport networks ready for routing and traffic assignment in QGIS"
lang: en
category: "Transport Engineering"
image: /assets/images/posts/gisbr-redes-transporte.webp
permalink: /en/2026/10/17/gisbr-transport-networks-routing-assignment.html
translation: "/2026/10/17/gisbr-redes-transporte-roteamento-alocacao.html"
---

The usual way to start a transport network model is to download the SNV from DNIT (Brazil's federal highway agency; SNV is the national highway system), a shapefile from the DER (the state highway departments) and an OSM extract, each in its own format and coordinate system, with no node in common. Only after reprojecting and stitching everything together can you route, and one risk remains: in Minas Gerais, 414 of the 945 DNIT segments are flagged `PLA`, a planned highway that would produce a false route.

![Road network in gold lines that goes from loose segments on the left to a connected network with a stream of light on the right](/assets/images/posts/gisbr-redes-transporte.webp)

## The work that comes before the model

Routing and traffic assignment assume a graph: arcs that end at nodes, nodes shared between neighboring arcs, speed and length attributes. Source data does not arrive that way. Each source has its own geometry, its own CRS and its own segmentation criterion, and line endpoints that should meet end up a few meters apart without touching.

There is also duplication. In Contagem, DNIT repeats the geometry of coinciding federal highways: BR-040 and BR-135 appear overlapped along 23.5 km. If that goes into the model untreated, the same stretch of road is counted twice. Collecting, reprojecting and cleaning topology take up the first part of any network project, before the first route is computed.

GisBR, a QGIS plugin I develop, handles that stage. The sections below show what it delivers in place of each manual step.

## One municipality, one panel, one GeoPackage

GisBR runs on PyQGIS and the Python standard library only, with no `pip install`. The flow starts in the diagnostics panel: I pick the state, pick the municipality (or a regional cut), tick the sources I want and click **Carregar selecionadas** (load selected). Everything comes out in SIRGAS 2000 (EPSG:4674), saved in a GeoPackage.

Sources are organized into nine thematic axes. The transport network sits in axis **1. Transportes**, which is the subject of this post; the other axes follow the same flow and need no separate download. There is also a metropolitan region mode, with the 84 metropolitan regions (RMs) in the IBGE catalog (IBGE is Brazil's national statistics office), for studies that cover more than one municipality.

What matters is what no longer exists: the list of portals to visit, the formats to convert and the QGIS project assembled layer by layer.

## The OSM network with its real topology

The OSM network arrives with ways split into arcs at shared `node_id` values, which is the topology OSM itself already records. The `osm_links` and `osm_nodes` layers carry `arc_id`, `from_node` and `to_node`, connected component and node degree. For modeling, they include `maxspeed`, `velocidade_kmh` and `comprimento_m`. That is what a graph requires, with no intermediate construction step.

The network can be vehicular or pedestrian, and loading runs in the background, with a progress bar and a Cancel button. For a metropolitan region, the OSM network comes from a prebuilt base, with a sha256 check and a local cache.

The [July post on the OSM network](/en/2026/07/06/gisbr-0-3-2-osm-fim-experimental.html) introduced the first version of this layer. The topology has been rebuilt since then, and the [OSM network guide](https://gisbr.dcamargo.com.br/guias/vias/) describes the fields in detail.

## Official highways and railways as a routable network

The intercity network is usually the harder part. From 1.2.0 on, six official sources become a routable network, each with links, nodes, problems and removed segments:

- DNIT/SNV
- DER-MG
- DER-PR
- Siga-GO (road network, from the state of Goiás)
- Ministry of Infrastructure (MInfra) railways
- IBGE BC250 (railways)

BC250 highways are left out, because that layer mixes jurisdictions.

When building the network, GisBR applies automatic corrections: endpoints within 1 m are merged, a T-junction within 10 m splits the target line and connects the endpoint there, and coinciding arcs are collapsed. That is what happens with the repeated federal highways in Contagem. Each correction is recorded with `severidade=corrigido`, so nothing changes silently.

What does not exist is removed from the network. A planned segment (`PLA`, or a railway marked Planned, Under Study or Under Construction) goes to the removed layer, which drops in one go the 414 DNIT segments that in MG would yield a false route. A federal highway that DER repeats is also removed when DNIT is ticked alongside it: in the Contagem cut, 22 of the 44 DER-MG segments were federal.

One limit: the official networks carry no traffic direction, so the resulting network is bidirectional.

## A list of what is wrong with the network

A network generated from real data has defects, and the point is to find them before running the model, instead of in the assignment result. So GisBR saves, alongside the links and nodes layers, a problems layer (`osm_problemas` for the OSM network) with type and severity, which you can filter and inspect on the map.

Some of the types: `ilha`, a set of arcs disconnected from the rest, which no route reaches; `mao_unica_sem_saida`, where a one-way street traps the flow; `ponta_quase_conectada`, two endpoints that almost touch and probably should; and `cruzamento_sem_no`, lines that cross without a node, which may be an error or may be an overpass. On the official networks, that last one is only flagged and never altered.

A dangling endpoint, the ordinary dead end, is not listed, because it is a normal situation in a road network.

## From network to routing and traffic assignment

With the network ready, what comes next depends on the study. Desire Lines, another plugin of mine, has an **Alocação em rodovias** (highway assignment) tab that works on the DNIT/SNV plus DER network obtained through GisBR, which is a declared dependency. Directional capacity follows the HCM 6th edition, assignment can be all-or-nothing or equilibrium (MSA, the method of successive averages, with the BPR function), and level of service comes from the v/c ratio. The focus is highways, not urban streets; more details on the [project page](/en/portfolio/desire-lines.html).

[Logis](/en/2026/08/26/logis-plugin-qgis-coleta-residuos.html) uses the municipal network downloaded by GisBR in the Rede Viária panel to route waste collection (TSP and CVRP).

If you prefer scripting, you can call the OSM network straight from Processing, with the `gisbr:osm_network` algorithm, which returns `LINKS`, `NODES` and `PROBLEMAS`:

```python
processing.run("gisbr:osm_network", {
    "CODE": "3118601",   # código IBGE do município
    "REDE": 0,           # 0 = veicular
    "LINKS": "TEMPORARY_OUTPUT",
    "NODES": "TEMPORARY_OUTPUT",
    "PROBLEMAS": "TEMPORARY_OUTPUT",
})
```

For demand, GisBR loads the OSM POIs (`osm_pois`) using the osm2gmns predicate, and the `gisbr:export_poi_gmns` algorithm writes a `poi.csv` in the osm2gmns and grid2demand layout.

## Getting started

GisBR is in the [official QGIS plugin repository](https://plugins.qgis.org/plugins/gisbr/). The step-by-step is on the [installation](https://gisbr.dcamargo.com.br/instalacao/) page, and the code is on [GitHub](https://github.com/d-camargo/gisbr).

After installing, open the panel, choose a municipality and tick the sources in the Transportes axis. The [transport networks guide](https://gisbr.dcamargo.com.br/guias/redes-transporte/) and the [documentation](https://gisbr.dcamargo.com.br/en/) explain each layer (the guides are in Portuguese; the documentation has an English version). To try it, load your municipality's network and open the problems layer before anything else.
