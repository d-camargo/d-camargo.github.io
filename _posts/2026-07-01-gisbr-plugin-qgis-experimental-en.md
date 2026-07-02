---
layout: post
title: "GisBR: Brazil's Official Spatial Datasets Straight into QGIS"
lang: en
translation: "/geoprocessamento/2026/07/01/gisbr-plugin-qgis-experimental.html"
permalink: /en/2026/07/01/gisbr-plugin-qgis-experimental.html
category: "Geoprocessing"
---

GisBR, my new QGIS plugin, has been approved in the official plugin repository as an experimental release. It brings the "one line → one layer" access of IPEA's **geobr** and **censobr** packages into QGIS, no R or Python skills required.

![GisBR plugin icon](/assets/images/posts/gisbr-cover.webp)

## The problem it solves

Anyone doing spatial analysis in Brazil knows the routine: to build a municipal map, you browse IBGE's FTP server, find the boundary files for the right year, download the archive, extract it, and only then load it into QGIS. The geobr package solved this elegantly for R and Python users: one function call returns a ready-to-use layer. But a large share of GIS professionals work directly in QGIS and were left out of that workflow.

GisBR closes that gap. Each geobr geography becomes an algorithm in the Processing Toolbox: pick a year, filter by state or IBGE code, and the layer lands in your project, already in SIRGAS 2000 (EPSG:4674). The use case driving the project is work at the **municipal scale**: quickly assembling a municipality's official layers for diagnosis and planning.

## What is available

Version 0.2.0 ships **55 algorithms**, in two phases. Phase 1, backed by GeoPackage files (geobr v1.7.0), covers 26 geographies organized in groups:

* **Administrative boundaries:** country, regions, states, meso- and microregions, intermediate and immediate regions, municipalities, and municipal seats.
* **Census:** census tracts, weighting areas, the statistical grid, and neighborhoods.
* **Urban and metropolitan:** metropolitan areas, urbanized areas, urban concentrations, and population arrangements.
* **Environment:** biomes, the Legal Amazon, the semiarid region, conservation units, indigenous lands, and disaster risk areas.
* **Sectoral:** health regions, health facilities, and schools.

Phase 2 adds 28 `read_*_v2` algorithms on top of geobr v2.0.0's Parquet catalog, with more recent data (up to 2022/2025) and geographies that only exist in the new version, such as **favelas, polling places, and quilombola lands**. The set is completed by the **join_censo** algorithm, which joins geobr's census tracts with censobr's demographic tables.

Every algorithm takes the same parameters: year (defaulting to the most recent), a filter by IBGE code or state abbreviation, and an optional simplified geometry that speeds up rendering when boundary precision is not critical.

## Technical decisions

One design choice guided the development: **zero external dependencies**. The plugin uses only the native QGIS/Qt API and Python's standard library. No geopandas, pandas, or requests. This removes the package-installation step that often blocks less technical users and avoids conflicts with other plugins. The only exception is optional: Phase 2 algorithms read Parquet through QGIS's own GDAL driver and, when it is not available, accept pyarrow as a fallback.

Downloads go to a disk cache with automatic fallback: if IPEA's server is down, the plugin fetches the same files from a GitHub mirror.

## Where the project is headed

The geobr mirror is the foundation for something more specific: GisBR is evolving into a **municipal diagnostic system** aimed at cities that need to draft or revise their Master Plan. The idea is to pick a municipality in a panel and receive the official datasets (transport, drainage and sanitation, demographics, environment, education, and health) already clipped to the municipal boundary and organized in a GeoPackage. It automates the work I described in the [reading the territory](/en/2026/06/24/reading-the-territory-master-plan.html) post. That layer is still under development and will land in a future release.

## How to install

Since the plugin is experimental, one adjustment is needed first: in QGIS, open **Plugins > Manage and Install Plugins > Settings** and check **Show also experimental plugins**. Then search for **GisBR** and click Install.

The code is open source (GPL) and lives on [GitHub](https://github.com/d-camargo/gisbr). Issues reporting problems or requesting new geographies are welcome. The plugin's official page is in the [QGIS repository](https://plugins.qgis.org/plugins/gisbr/).
