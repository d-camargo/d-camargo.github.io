---
layout: post
title: "SIG-Bus: GTFS Reader and Passenger Demand Integration for QGIS"
lang: en
translation: "/2026/06/16/sig-bus-gtfs-demanda-qgis.html"
permalink: /en/2026/06/16/sig-bus-gtfs-demand-qgis.html
category: "Transport Engineering"
image: /assets/images/posts/sig_bus_mapa_carga.png
---

SIG-Bus has a well-defined purpose: read GTFS feeds inside QGIS, cross-reference them with per-stop boarding records, and deliver synthetic reports per line, with no external dependencies beyond QGIS itself. The project started as a PIBIC undergraduate research initiative at CEFET-MG in 2020 (with the application filed in 2019) and was presented at the institution's Science and Technology Week in 2025.

![SIG-Bus: passenger load map by route segment in QGIS](/assets/images/posts/sig_bus_mapa_carga.png)

## The integration problem

QGIS has no native GTFS support beyond basic geometry loading. Analyzing a bus network means cross-referencing three pieces of information that live in separate sources: route geometry, scheduled trips, and real passenger demand. Without a dedicated tool, bringing them together is manual, repetitive work.

Boarding data is available on the [City of BH's open data portal](https://dados.pbh.gov.br/dataset/estimativa-de-embarque-nos-pontos-de-parada) as CSV files with their own coordinate system and line codes that don't map directly to GTFS identifiers. Building a reliable spatial link between the two datasets, without generating false matches with nearby parallel routes, was the core technical challenge.

## How the plugin works

SIG-Bus organizes the workflow into six sequential steps:

1. **GTFS Validation:** checks feed integrity and generates synthetic calendars when `calendar.txt` is missing.
2. **GTFS Import:** converts files to GeoPackage, creating indexed spatial layers for stops, route shapes, and trips.
3. **Demand Import:** loads the boarding CSV and spatially links demand points to GTFS stops, restricted to each line's dominant service pattern to prevent false positives.
4. **Route and time period selection:** the user picks a line and a time slot (full day or a specific hour, 0h to 23h).
5. **Demand allocation:** generates the `tramos_demanda` layer with accumulated load and trip counts per segment.
6. **Visualization:** graduated styles are applied automatically, highlighting the highest-volume segments.

## The departure schedule layer

When filtering a line, the plugin automatically generates the **`horarios_paradas`** layer, a point layer with scheduled times for all trips on the selected route.

For each stop, the layer records:

- `arrival_time` and `departure_time`
- `stop_sequence` and `stop_name`
- `trip_id`, `shape_id`, and `direction_id`

The layer is built from a direct join across the `stop_times`, `trips`, and `stops` tables in the GeoPackage database, indexed by `trip_id`. It makes it straightforward to visualize service distribution throughout the day, identify stops with irregular headways, or check hourly coverage for a specific line.

> Like all SIG-Bus layers, `horarios_paradas` is memory-based and must be regenerated after reopening QGIS.

## Segment demand allocation

The `tramos_demanda` layer is the plugin's main analytical output. The load on each segment is calculated using **flow conservation**: boardings at stop *i* add to the load from the previous segment.

Since the fare system records only boardings, without alighting data, the method assumes all passengers alight at the final stop. This produces an **upper bound on actual occupancy**, appropriate for:

- Relative comparison between segments on the same line
- Identifying the most loaded sections by time period
- Analyzing hourly demand distribution

The `METHODS.md` file in the repository details the assumptions, edge cases, and interpretation guidelines.

## Science and Technology Week 2025 and current state

The project was presented at CEFET-MG's Science and Technology Week in 2025. After that version, two additions were incorporated: **cluster-based categorization of demand segments** with automatic graduated styling, and **PDF report generation** with two maps (accumulated load and cluster grouping) overlaid on the route geometry.

The full repository is available on [GitHub](https://github.com/d-camargo/sig-bus). All testing was done with the real GTFS feed for the city of Belo Horizonte, and the `docs/gtfsfiles.zip` file contains that same data for anyone who wants to reproduce the analyses.

If you'd like to try the plugin and don't have the file at hand, I can send the `.zip` directly. Just ask by email ([eng.dcamargo@outlook.com.br](mailto:eng.dcamargo@outlook.com.br)) or [WhatsApp](https://wa.me/553135653353) (+55 31 3565-3353).
