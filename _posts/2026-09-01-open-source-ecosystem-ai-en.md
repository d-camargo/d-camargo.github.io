---
layout: post
title: "Nobody has time to learn one more piece of software: AI and open source"
lang: en
translation: "/2026/09/01/ecossistema-open-source-ia.html"
permalink: /en/2026/09/01/open-source-ecosystem-ai.html
category: "General"
image: /assets/images/posts/ecossistema-open-source-ia.webp
---

Last month I needed a photogrammetric flight grid over an area that was already open in QGIS, with the property boundary and the terrain sitting right beside it. There were three ways out: learn QGroundControl and redraw the polygon inside it, on top of a satellite image with none of those layers; work the transects out by hand in a spreadsheet; or read the QGroundControl source and bring that calculation into QGIS.

![Isometric wall of closed dark boxes with a single open box lit in gold](/assets/images/posts/ecossistema-open-source-ia.webp)

I took the third, which cost weeks instead of the two afternoons the others would have taken, and it still paid for itself. The question it left behind: when is adding the feature to the software you already have open worth more than learning one more?

## The arithmetic that does not close

The catalogue of open tools grows every month: a new plugin in the QGIS repository, a new Python library for geospatial data, a new application to validate or convert something. Almost all of it free, and much of it solving a real problem.

What does not grow is the time. Every new tool charges a learning curve before it gives anything back: install it, understand the data model, find out where its output stops matching the rest of the workflow. That curve is paid in working hours, taken from the same place the deadline comes from. The bottleneck in the open ecosystem today is not the supply of tools, it is the attention available to spread across the ones that already exist.

## Learning the tool or asking for the result

Sequoia published, in [Services: The New Software](https://sequoiacap.com/article/services-the-new-software), an argument that reads this deadlock from below. It separates copilot from autopilot: the copilot sells the tool to the professional, who stays answerable for the result; the autopilot sells the result straight to whoever needs it. The bet rests on budget, since spending on services runs around six times the spending on the equivalent tool.

> "If you sell the tool, you're in a race against the model. But if you sell the work, every improvement makes your service faster, cheaper, and harder to compete with."

The article looks at the selling side; from the using side, the same sentence describes something else. The engineer who has to deliver the collection sectors by Friday does not want routing software, they want the sectors. Except the tool does not disappear when it leaves sight: it keeps running somewhere, and someone keeps answering for what it produced.

## Why open source shortens the path

Customising closed software has one route: open a ticket and wait on the vendor's roadmap, which is not going to prioritise what matters to a handful of clients.

With open source you can read it, change it and run it the same day. What always made that route expensive was understanding somebody else's codebase before touching a single line, and that is the price that has fallen: I hand the repository to an AI, ask where the calculation I care about lives, and the reading that would have taken days takes an afternoon.

QGC4QGIS depends on this twice. It reimplements QGroundControl's grid generator inside QGIS, the `SurveyComplexItem` class: one open project to read the algorithm from, another to receive the result. With the code in hand, changing the software got fast; where the change is delivered is another question.

## Growing what is already installed

A new feature can be delivered as one more site or application, which the user installs and then carries, or as an extension of the software they already have open. The second one charges no new learning curve.

**The data is already there.** The plugin runs on the layers of the open project, in the coordinate system already defined, with the symbology already tuned. A new application forces an export, a conversion and a reimport, and that round trip usually costs more than the feature saves. In [SIG-Bus timetable editing](/en/2026/08/15/sig-bus-gtfs-editing-adjust-timetables.html), the GTFS feed is already in QGIS when the planner decides to push the morning trips later.

**The platform has solved the rest.** Writing inside QGIS, you inherit format reading, reprojection, editing, layout printing and the processing toolbox without writing a line of any of it. Outside it, that rest becomes the whole project.

**The gains pile up in one place.** Thirty features spread across thirty applications compete for the same scarce attention; the same thirty inside QGIS reach whoever already opened the program this morning.

The limit here is clear, and ignoring it turns the argument into a universal rule: it holds while whoever will use the result is already inside the platform. For a manager who has never opened QGIS, packaging the analysis as a plugin delivers nothing, and there the page or the dashboard is the right choice.

## The cost that shows up later

Writing the customisation got cheap. Maintaining it did not. Each one is a fork or a plugin that somebody carries over time: QGIS moves from the 3.34 series to 4.x, Qt5 becomes Qt6, NumPy 2.x breaks a GDAL import that had worked for years. AI speeds up the writing, not the maintaining, because maintaining means keeping up with four projects that agreed on nothing with each other.

That is the difference between an afternoon's script and the plugin that still installs two years from now. With [Logis](/en/2026/08/26/logis-plugin-qgis-coleta-residuos.html), getting into the official repository was where the work started: every new QGIS release is a chance for something to break on a machine I have no way to test.

## Who checks the result

If the move is to ask for the result instead of learning the tool, one question is left over: who notices when the result came out wrong?

The same source gives the vocabulary, separating execution from judgement. AI already executes well whatever has a defined rule; the decision that rests on experience and on accountability, not yet. In transport the error does not stay on the screen: a sectorisation the truck cannot run becomes overtime and a street with no collection, and the person who signs off on it is the professional.

I have written here about [Linux with AI](/en/2026/08/03/linux-ai-autonomy-dependency.html), and there the doubt was personal, about what is left of me once the problem is solved. Here it is professional, because whoever pays for the error is not whoever made it.

## What I do in practice

The question I ask before starting is always the same: do I want the tool or do I want the result?

If the result is one-off, it is a throwaway script, and I do not spend a minute making it presentable. If it turns into routine, it turns into a plugin of the tool that is already open, not a new thing to install. Then comes the second test, the more honest one: could I maintain this without the AI beside me? When the answer is no, what I have is a debt with no due date.

And once it is a plugin, I publish it in the official repository instead of keeping the fork at home. Published, the maintenance cost shows up: a user opens an issue, a new release breaks something. Kept at home it still exists, only invisible, and the benefit sits still with me.
