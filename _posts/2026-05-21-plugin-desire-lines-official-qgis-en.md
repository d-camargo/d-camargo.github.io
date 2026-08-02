---
layout: post
title: "Desire Lines plugin available in the official QGIS repository"
lang: en
translation: "/2026/05/21/plugin-desire-lines-oficial-qgis.html"
permalink: /en/2026/05/21/plugin-desire-lines-oficial-qgis.html
category: "Transport Engineering"
image: /assets/images/desire_lines_flow_map.png
---

The Desire Lines plugin is now integrated into the official QGIS plugin repository. This approval makes installation straightforward via the software's plugin manager, removing the need for external file downloads.

![Flow Map with Desire Lines](/assets/images/desire_lines_flow_map.png)

## Version Updates

The inclusion in the official repository comes with technical improvements to the plugin:

* **Bug fixes:** Resolved issues reported in the initial version.
* **Stability:** Under-the-hood adjustments improved performance when rendering flow geometries.

## Feature: Desire Lines

Desire Lines is tailored for urban mobility professionals, logistics analysts, and spatial analysts working with origin-destination matrices. The tool converts tabular data into visual geometries connecting origin and destination points.

It is important to note that the plugin generates **straight desire lines** rather than routing based on street networks. It illustrates the volume and direction of flow, indicating movement intent in the territory. This abstraction is useful for transportation demand analysis, migration patterns, and distribution.

## Supporting Material

To deepen the practical and theoretical understanding of flow analysis, I published two detailed articles on Medium (in Portuguese):

1. [**Você sabe o que é uma matriz O-D?**](https://medium.com/@eng.diegocamargo/você-sabe-o-que-é-uma-matriz-o-d-7b66a922018d): Fundamental concepts about Origin-Destination Matrices and their role in planning.
2. [**Mapa de fluxo no QGIS com DesireLines**](https://medium.com/@eng.diegocamargo/mapa-de-fluxo-no-qgis-com-desirelines-49591953c173): Step-by-step tutorial on how to generate flow maps using the tool.

## How to Install

In QGIS, go to **Plugins > Manage and Install Plugins**, search for **Desire Lines** and click Install.

For additional information or to report issues, visit the [official plugin page in the QGIS repository](https://plugins.qgis.org/plugins/desire_lines/).
