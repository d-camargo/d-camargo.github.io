---
layout: post
title: "Desire Lines 0.3.2: Portuguese interface and QGIS 4.x (Qt6) compatibility"
lang: en
translation: "/2026/07/14/desire-lines-pt-br-qt6-qgis4.html"
permalink: /en/2026/07/14/desire-lines-pt-br-qt6-qgis4.html
category: "Transport Engineering"
image: /assets/images/desire_lines_flow_map.png
---

The Desire Lines plugin picked up two updates that change who can use it and where. The interface is now translated into Portuguese, and the same package runs on both QGIS 3.x and QGIS 4.x, which moved from Qt5 to Qt6.

![Desire Lines flow map](/assets/images/desire_lines_flow_map.png)

## Portuguese interface

All 42 interface strings (labels, error messages, field hints) were translated into Brazilian Portuguese. There's nothing to configure: the plugin follows whatever language QGIS itself is set to. Users running QGIS in Portuguese see Desire Lines in Portuguese automatically; users on English QGIS keep seeing the original interface, with no extra option to hunt for in the menus.

## QGIS 4.x (Qt6) compatibility

QGIS 4 switched its graphics toolkit from Qt5 to Qt6, which breaks plugins that rely on unscoped PyQt enums (the older way of referencing constants from the graphics library). Desire Lines was updated to use scoped enum syntax, compatible with both Qt versions, and the hard-coded PyQt5 resource file was removed.

The result is a single codebase that passes the test suite on both QGIS 3.44 (Qt5) and QGIS 4.2 (Qt6), with no separate builds per version.

## Packaging fixes behind the scenes

Two quiet but relevant fixes for anyone installing from the official repository:

* **The translation actually ships now.** The compiled translation file (`.qm`) was excluded from version control by mistake, so published zips never contained the Portuguese interface, even though the strings were already translated.
* **The package shrank from ~14 MB to ~200 KB.** The example dataset folder (RMSP demo data) and the automated test suite were dropped from the published zip; both remain available in the GitHub repository for anyone who wants to reproduce them.

## How to update

In QGIS, go to **Plugins > Manage and Install Plugins**, find **Desire Lines**, and apply the available update. First-time installs find the plugin the same way, already at version 0.3.2.

To follow development or report issues, the source code is on the [official Desire Lines repository on GitHub](https://github.com/d-camargo/desire_lines).
