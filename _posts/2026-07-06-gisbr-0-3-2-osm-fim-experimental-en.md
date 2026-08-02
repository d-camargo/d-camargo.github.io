---
layout: post
title: "GisBR 0.3.2: OSM Road Networks and the End of the Experimental Label"
lang: en
translation: "/2026/07/06/gisbr-0-3-2-osm-fim-experimental.html"
permalink: /en/2026/07/06/gisbr-0-3-2-osm-fim-experimental.html
category: "Geoprocessing"
image: /assets/images/posts/gisbr-osm-belem.webp
---

About two years ago I talked with professor Xuesong (Simon) Zhou, from Arizona State University, one of the authors of [osm2gmns](https://github.com/jiawlu/OSM2GMNS), a tool that turns OpenStreetMap data into transport networks ready for modeling. Two years later, that link-and-node mechanic lands in my plugin: GisBR 0.3.2 downloads the road network of any Brazilian municipality straight from OSM. It is also the first release published without the **experimental** label in the official QGIS plugin repository.

![OpenStreetMap road network downloaded by GisBR over the municipal boundary of Belém (PA), in QGIS](/assets/images/posts/gisbr-osm-belem.webp)

## The source that was missing: the circulation network

GisBR's municipal diagnosis already gathered 29 official sources across 8 thematic axes (transport, sanitation, demographics, environment, education, health, urban and political-administrative), all written to a local GeoPackage. You could map almost everything about a municipality, except its streets. For anyone working in transport planning, that gap is hard to justify.

Version 0.3.2 closes it. The plugin queries OpenStreetMap's Overpass API, downloads the roads of the chosen municipality and builds two layers with minimal topology: **links** (road segments) and **nodes** (the connections between them). Not a dump of loose geometries: a network, in the sense transport modeling uses the word.

> **Heads up:** the roads come from OpenStreetMap, a collaborative map fed by volunteer mappers. Coverage and detail vary from one municipality to the next: where the local community is active the network is rich; where it is not, roads or attributes may be missing. Check the result before using it in analysis.

The mechanics behind this assembly have a declared origin. osm2gmns, by Jiawei Lu and professor Zhou, converts OSM extracts into networks in the GMNS format (General Modeling Network Specification), the open spec the modeling community has been adopting to describe networks as node and link files. GisBR applies the same logic inside QGIS: instead of CSVs, the result becomes layers in the diagnosis GeoPackage, in SIRGAS 2000 (EPSG:4674), ready for the plugin's 55 Processing algorithms.

The behavior follows the same rule as the existing WFS and ArcGIS sources: if the layer is already in the GeoPackage, the download is skipped. To force a refresh, tick the "Update downloaded datasets" checkbox. No accidental repeated requests to Overpass, which is exactly the kind of usage that burns through a public server's quota.

## The timeout that never arrived

In the middle of this work I hit the most annoying bug of the release, and it was not in the new code. The function that builds the Overpass query accepted a per-source configurable timeout, but the value died along the way and was never applied to the request. It worked on the server's good days. It blew up on the bad ones.

Version 0.3.2 closes the loop, and error handling got more honest along the way: a network error is reported as a network error, and a response that is not valid JSON raises a dedicated exception (`OverpassError`) with a readable message, instead of a cryptic traceback in the middle of the panel.

## SSL on Windows

Since 0.3.0, some Windows users saw the IPEA metadata load fail with an SSL certificate error. On Linux, nothing. In QGIS on Windows, chain validation broke. The fix in 0.3.2: the plugin now ships the certificate chain of IPEA's server (`core/certs/ipea_chain.pem`) and uses a safe fallback when the system's default validation fails. No disabling certificate verification, no asking the user to touch QGIS settings.

This was the last item holding me back from dropping the experimental label. It made no sense to promote a plugin that broke on the platform where most QGIS users are.

Version 0.3.2 is available in the official QGIS plugin repository (no need to enable experimental plugins anymore). The code is GPL-3.0 and lives on [GitHub](https://github.com/d-camargo/gisbr). If your municipality's network comes out looking odd, open an issue: OSM road data quality is uneven across Brazil, and real cases are what calibrate the tool.
