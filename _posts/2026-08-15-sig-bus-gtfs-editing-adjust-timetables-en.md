---
layout: post
title: "SIG-Bus: editing a route's GTFS timetable without opening the .zip"
lang: en
translation: "/2026/08/15/sig-bus-edicao-gtfs-ajustar-horarios.html"
permalink: /en/2026/08/15/sig-bus-gtfs-editing-adjust-timetables.html
category: "Transport Engineering"
image: /assets/images/posts/sig-bus-edicao-gtfs.webp
---

The BHTrans feed is loaded in QGIS, route 3350 is selected, and a few morning trips need to leave ten minutes later. Done by hand, that means unzipping the `.zip`, opening a `stop_times.txt` with hundreds of thousands of records, finding the right rows among the trips of an entire city, fixing one time after another without breaking the references to `trip_id` and `stop_id`, and zipping it back up hoping the result is still a valid feed.

![bus route timetable grid with one shifted trip highlighted](/assets/images/posts/sig-bus-edicao-gtfs.webp)

Planning operations on top of an international standard is what makes it possible to use tools nobody wrote for your city: the same feed opens in QGIS, in a public validator, or in the passenger's app. The price of the standard is its structure, a set of tables tied together by foreign keys, and a time edited by hand in a text file gives no warning when one of those ties breaks. The **GTFS Editing** tab in SIG-Bus exists for that part of the job.

## A working copy, not the original feed

Before touching any field, the problem is data safety. **Enter edit mode** clones the analysis GeoPackage (`feed.gpkg`) into an isolated working copy, `feed_edit.gpkg`. Everything that follows happens in that copy, and the analysis feed is never modified directly.

That changes the cost of a mistake. If an edit session is already open, the plugin asks whether you want to **Resume** where you left off or **Start over** from a clean draft, and **Discard edits** deletes the draft, returning the tab to its initial state. The draft stays on disk until you export or discard it.

## Why `stop_times` only opens filtered

The bottleneck in editing GTFS inside a GIS is the size of one single table. In the Belo Horizonte feed, `stop_times.txt` is 136 MB, and in large feeds the table reaches millions of records: loaded whole, it freezes QGIS. That is why the **Route (route_short_name)** and **Trip (trip_id)** fields become active when `stop_times` is the selected table, and why both are required. Only the times of that one trip enter the editing session.

![SIG-Bus GTFS Editing tab, with the stop_times table selected and the route 3350 and trip filters filled in](/assets/images/posts/sigbus02/1.webp)

The editing engine is hybrid, and deliberately so: the plugin handles the cycle (enter, filter, validate, export, discard) and the editing itself happens in the QGIS attribute table, with undo, redo, and the field calculator. ID and foreign key fields open as read-only, so integrity does not break on a distracted click.

## The whole route as a matrix

Filtering by trip solves performance and creates a different limit: the attribute table shows one trip at a time, and anyone deciding a departure time is looking at the headway between departures, not at an isolated column.

The **Adjust timetables** button opens the whole route, with one tab per direction (`direction_id` 0 for outbound, 1 for inbound). Stops run down the rows and trips across the columns; each column is headed `V1`, `V2`, `V3` with the first departure in `HH:MM` right below it, and the `trip_id` in the tooltip. Under the matrix, separated by a draggable splitter, sits the block diagram for the same route.

![Adjust Timetables window for route 3350, with the stop and trip matrix on top and the block diagram below](/assets/images/posts/sigbus02/2.webp)

Two reading details prevent confusion. A cell with `-` is a stop that trip does not serve: it stays editable, but whatever you type there is ignored on save, because the window never creates a new stop on a trip. And times past midnight are written by going beyond 24 h (`25:10:00`), as the standard requires.

## Typing one time shifts the whole trip

Adjusting cell by cell would be trading one manual job for another. The design decision that changes this: typing a time into a cell shifts the entire trip, and the remaining times follow, preserving the running times between stops. Pushing V7's departure ten minutes later moves every subsequent stop on V7.

Selection is linked across both panels: clicking a bar in the diagram puts the cursor on that trip's column in the matrix, and clicking a cell selects the trip in the diagram, so the trip that caught your eye in the chart is found in the table without scanning column by column. For fine adjustments, with a trip selected in the diagram, `>` and `<` shift only the departure or only the arrival, while `+` and `-` shift the whole trip, using the increment in minutes from the **Step** field.

## Apply to the feed, validate, export

Up to this point nothing has touched a file: the draft lives in memory. **Apply to feed** validates the grid before writing (an error blocks, a warning asks) and writes only the trips whose times actually changed. What stays untouched matters as much as what changes: only `arrival_time` and `departure_time` are rewritten, and the alignment (`shape_id`), the `trip_id` values, the `block_id`, and the number of trips remain as they were.

With the window closed, **Validate** checks referential integrity and the format of times, dates, and coordinates, detailing each failure in the plugin log. **Export .zip** runs the validator again, aborts on a fatal error, asks on a warning alone, and rebuilds the coordinates in `stops.txt` and `shapes.txt` from the geometry sitting in the map. The output is a standard GTFS, ready to go back into any tool that reads the format.

It is worth noting where this fits. Public transport management software tends to be expensive, closed, and sold by subscription, and whoever works at a small city hall often ends up with no tool at all. QGIS is already on those desks, and SIG-Bus is a free plugin on top of it: that is the gap the project tries to cover. The [repository](https://github.com/d-camargo/sig-bus) is open for use, bug reports, or contributions.
