---
layout: post
title: "GisBR 0.4.3: SSL Certificates for Fresh Windows/OSGeo4W Installs"
lang: en
translation: "/2026/07/28/gisbr-0-4-3-ssl-certificados.html"
permalink: /en/2026/07/28/gisbr-0-4-3-ssl-certificados.html
category: "Geoprocessing"
---

Someone installs QGIS from scratch through OSGeo4W, opens GisBR and tries to download any official layer. The answer is `unable to find issuer certificate`. It is not a connectivity problem or a flaky server: it is the SSL trust chain a freshly installed Windows machine does not yet recognize. Version 0.4.3 closes that gap, but it is the third infrastructure fix since 0.3.2, and all three are worth telling together.

![GisBR plugin icon](/assets/images/posts/gisbr-cover.webp)

## Two quiet fixes: 0.4.0 and 0.4.1

After 0.3.2, published without the experimental label, two versions shipped without a post of their own because they were narrow fixes. 0.4.0 declared explicit compatibility with QGIS 4.x. 0.4.1 fixed a subtler bug: the cache directory lookup used the unscoped `QStandardPaths.CacheLocation` enum, which raises on PyQt6 and took down the municipality list with a generic "geobr catalog unavailable" error. The same issue affected the Overpass network error check. Both fixes scoped the enum correctly, made the catalog error message show the real underlying exception, and had the cache path fall back to the bundled offline CSV instead of aborting.

## The SSL fix that only covered half the cases

Since 0.3.0, GisBR already shipped IPEA's certificate chain to work around SSL failures on Windows, but that injection was tied to the geobr downloader. That made sense while IPEA was the plugin's only own HTTPS source. The problem is that the municipal diagnosis already queries far more services: WFS and ArcGIS REST endpoints from sources like SICAR, ANA/SNIRH, INDE, SGB and IBAMA, OSM's Overpass API, and the satellite basemap. On fresh OSGeo4W installs, without the root certificates an older system installation tends to accumulate, each of those services could fail with the same certificate chain error, and none of them had the fallback that only existed for IPEA.

Version 0.4.3 moves that logic into a single module, `core/ssl_support.py`, and applies the same certificate injection to the WFS, ArcGIS REST and Overpass connectors, plus the default SSL configuration used by the XYZ basemap. The plugin now ships the self-signed roots used by the GitHub mirror, SICAR, ANA/SNIRH, INDE, SGB, IBAMA, Overpass and the satellite basemap, all in one place instead of scattered across the codebase.

To be clear: the certificates are added as additional trust anchors, not as a way around verification. No verification setting is ever relaxed; the plugin simply learns to recognize chains a freshly installed Windows machine does not yet know about. And when a request still fails, the error message now includes the host and the underlying exception instead of a generic connection warning.

Version 0.4.3 is available in the official QGIS plugin repository. The code is GPL-3.0 and lives on [GitHub](https://github.com/d-camargo/gisbr). If you install GisBR on a new machine and still hit a certificate error on some service, open an issue with the host that failed: it likely means a root is missing from that module.
