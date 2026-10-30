---
layout: post
title: "Sioux Falls and Frank-Wolfe: equilibrium assignment in Desire Lines"
lang: en
category: "Transport Engineering"
image: /assets/images/posts/desire-lines-frank-wolfe-sioux-falls.webp
permalink: /en/2026/10/30/desire-lines-frank-wolfe-sioux-falls.html
translation: "/2026/10/30/desire-lines-frank-wolfe-sioux-falls.html"
---

Equilibrium assignment is the problem that transport planning tools solve when they take congestion into account. The 1975 paper by LeBlanc, Morlok and Pierskalla showed how to compute it on a road network, and the network it uses, Sioux Falls, became the test on which implementations are measured. Version 0.7.1 of **Desire Lines** now assigns by equilibrium with the Frank-Wolfe algorithm, and I validated the result on that same network.

![Sioux Falls network drawn with flow lines of varying width on a dark background](/assets/images/posts/desire-lines-frank-wolfe-sioux-falls.webp)

## Why the 1975 paper matters

The history leading up to it has four steps:

- **1952:** Wardrop states the user equilibrium principle: no driver can reduce their travel time by switching routes alone.
- **1956:** Beckmann, McGuire and Winsten show that this equilibrium is the solution of a convex optimisation problem. Ortúzar and Willumsen (2011) summarise what followed: the principle dates from 1952, the mathematical formulation came four years later, and "it took several more years" before suitable algorithms for practical implementation were proposed and tested.
- **1956:** Frank and Wolfe publish a nonlinear programming algorithm.
- **1975:** LeBlanc, Morlok and Pierskalla (*Transportation Research* 9, 309-318) apply Frank-Wolfe to Beckmann's formulation and show that the equilibrium on a road network is computable. The test case is Sioux Falls.

The network stayed in use. It is part of the public **Transportation Network Test Problems** collection (TNTP, by Hillel Bar-Gera), kept in the [bstabler/TransportationNetworks](https://github.com/bstabler/TransportationNetworks/tree/master/SiouxFalls) repository. The collection's README says the network "was used in many publications" and that it is "good for code debugging". That is how I use it here.

## The problem and the network

With congestion, travel time on a link depends on the flow, and the flow depends on the time, because drivers choose routes by time. **All-or-nothing** (AoN) ignores that loop: it loads all the demand onto the free-flow shortest path. It works as a diagnosis of where capacity would be short, but it is not an equilibrium.

**Frank-Wolfe** (FW) solves the loop by iterating. In each iteration it runs an all-or-nothing loading with the current times, which gives a direction, and decides how far to move along it with a **line search** on the Beckmann function. Ortúzar and Willumsen describe the same mechanism: the latest all-or-nothing assignment provides a descent direction. **MSA** (method of successive averages) uses the same direction but moves a fixed step of 1/k at iteration k, with no search.

Link time follows the **BPR** function, with the collection's usual parameters:

`t = t0 · (1 + 0.15 · (v/c)^4)`

where `t0` is the free-flow time, `v` the volume and `c` the capacity.

The facts about the network, according to the TNTP README:

- 24 zones and nodes, 76 directed links, 528 O/D pairs with demand and 360,600 trips.
- The collection itself warns that the network "is not considered as a realistic one".
- Node coordinates were generated artificially to reproduce the diagram in the paper.
- The paper's demand (Table 1) is in thousands of vehicles per day. In the TNTP it was multiplied by 100, which is 0.1 of the daily flow, and can be read as an approximate hourly flow.
- Free-flow times are in 0.01 h.
- Other, slightly different versions of the network exist in other publications. That is why the comparison below is against the TNTP version, not "against the paper".

![Sioux Falls network with 24 numbered nodes and 76 directed links drawn in pairs; the width of each link is proportional to its capacity](/assets/images/posts/desirelines01/1.webp)

*Figure 1. The network. Each pair of lines is a pair of links in opposite directions. Width is capacity, and the legend shows four reference values (5,000, 10,000, 20,000 and 25,000).*

Figure 2 shows the same network with the demand on top. These are **desire lines**, the same concept from the [post on the Origin-Destination matrix](/en/2026/10/27/origin-destination-matrix-how-to-read-the-table-and-when.html): a desire line shows where people want to go, and assignment shows which way they go.

![Sioux Falls desire lines: straight lines between the 24 nodes, with width and opacity growing with the number of trips between each pair; the thickest ones concentrate around node 10](/assets/images/posts/desirelines01/2.webp)

*Figure 2. Desire lines. Each straight line joins a pair of zones, adding the trips in both directions. Width is the number of trips for the pair (legend: 200, 800, 1,600 and 2,400).*

## Desire Lines on this topic

The plugin's **Highway Assignment** panel offers three methods: AoN, MSA and Frank-Wolfe. FW is the panel default, with 100 iterations and a relative gap of 0.001. Before version 0.7, the default was 10 iterations of MSA.

Figure 3 is the result of FW with 100 iterations on the Sioux Falls network.

![Sioux Falls network with the flow assigned by Frank-Wolfe in 100 iterations; link width is the volume and colour goes from light grey to dark brown with the volume/capacity ratio](/assets/images/posts/desirelines01/3.webp)

*Figure 3. Flow assigned by FW in 100 iterations. Width is volume (legend: 2,000, 5,000, 10,000 and 20,000, in the unit of the TNTP demand, read as an approximate hourly flow) and colour is the v/c ratio, from 0 to 2.56 on the colour bar. The highest ratio appears on the links between nodes 6 and 8.*

### Validation against the reference solution

For each link, the error is `|v − vref| / vref`, with `vref` taken from the TNTP reference solution (`SiouxFalls_flow.tntp`). The reference total system travel time (TSTT) is 7,480,225.

| Scenario | Max error | Mean error | TSTT | Relative gap |
|---|---|---|---|---|
| MSA, 10 iterations (previous default) | 69.6 % | 13.7 % | 9,342,350 | 0.102 |
| MSA, 100 iterations | 8.9 % | 1.5 % | 7,622,065 | 0.0092 |
| Frank-Wolfe, 50 iterations | 5.3 % | 0.96 % | 7,484,340 | 0.0031 |
| **Frank-Wolfe, 100 iterations (default)** | **2.3 %** | **0.46 %** | **7,476,227** | **0.0014** |
| Frank-Wolfe, 300 iterations | 0.71 % | 0.14 % | 7,478,543 | 0.0004 |

Figure 4 puts the per-link error of the previous default and the current default side by side.

![Two Sioux Falls maps side by side showing per-link error: on the left MSA with 10 iterations, with many links in dark brown; on the right Frank-Wolfe with 100 iterations, almost all in light grey](/assets/images/posts/desirelines01/4.webp)

*Figure 4. Per-link error against the reference solution. The scale runs from 0 to 10 %, and larger values appear in the colour of the bar's end. On the left, MSA with 10 iterations (max error 69.6 %, mean 13.7 %). On the right, Frank-Wolfe with 100 iterations (max error 2.3 %, mean 0.46 %).*

One detail about the gap. With 100 iterations, FW ends with a gap of 0.0014, above the 0.001 tolerance. In the panel default, the run is stopped by the iteration limit, not by the tolerance. On this network, the FW gap first drops below 0.001 at iteration 132. It does not decrease monotonically: it oscillates from one iteration to the next, as figure 5 shows.

![Chart of the relative gap on a logarithmic scale against iteration k, from 1 to 300, for MSA in grey and Frank-Wolfe in gold, with a dashed line at 10 to the power minus 3](/assets/images/posts/desirelines01/5.webp)

*Figure 5. Convergence. x axis: iteration k. y axis: relative gap on a logarithmic scale. The dashed line marks 10⁻³, the panel's default tolerance.*

### How many fewer iterations

Instead of repeating a factor from the documentation, I measured it on the gap series of the two 300-iteration runs:

- FW reaches a gap of 0.0031 at iteration 50. MSA only reaches that level at iteration 297, about 6 times more.
- FW with 100 iterations has a gap of 0.0014. MSA, after 300 iterations, is at 0.0031, more than double, and never reaches 0.0014 within the 300.

This holds for this network and this criterion (the gap). On other networks the ratio may change.

## Limits of Frank-Wolfe

Ortúzar and Willumsen describe the behaviour that figure 5 shows: Frank-Wolfe "tends to converge rapidly over early iterations but less so as it starts to approach the optimum", and link flows tend to oscillate between iterations, which makes the final precision harder to reach. The same authors present alternatives that work in path-flow space, such as the gradient projection algorithm of Jayakrishnan et al. (1994), and say they have better convergence properties on large, congested networks. Desire Lines currently offers AoN, MSA and FW. The plugin has no path-based method, and this post does not promise one.

## A data preparation lesson

The error does not always come from the algorithm. Section 6 of the methods documentation records a case: with the same TNTP data and the same configuration, treating **each feature as two-way** instead of one-way takes the maximum error to 73.6 %, the mean error to 19.4 % and the TSTT to 3,743,234, about half the reference value.

The reason is capacity. The TNTP network already carries both directions as separate links, 38 pairs of opposite links. If the plugin generates both directions for each feature, each direction ends up with two parallel arcs of the same capacity, and the effective capacity doubles. With double the capacity, travel time falls and the TSTT falls with it.

In QGIS, check the **direction field** of the highway layer before assigning. The plugin reads `mao_unica` (it also recognises `oneway`, `one_way` and `sentido_unico`). If true, it generates only the arc in the geometry's direction. If false, it generates both directions. A network that already comes with one record per direction must be marked as one-way.

## Reproduce and check

The data and the test are in the plugin repository, at [github.com/d-camargo/desire_lines](https://github.com/d-camargo/desire_lines): the network in `test/data/sioux_falls` and the test in `test/test_sioux_falls_ue.py`. The test runs FW with 300 iterations and MSA with 500, and compares against the reference solution, with FW tolerances of 2 % on the maximum error, 0.5 % on the mean error and 0.5 % on the TSTT. If a code change makes the result worse, the test fails. This is the benchmark as a contract.

## Next step

Sioux Falls is a laboratory. The next step is to run the same engine on the real network that GisBR delivers, described in the [post on transport networks and assignment](/en/2026/10/17/gisbr-transport-networks-routing-assignment.html). That is the subject of the next post.

Version 0.7.1 is available in the plugin repository on GitHub, and the [documentation](https://desirelines.dcamargo.com.br) describes the panel.

## References

- Wardrop, J. G. (1952). Some theoretical aspects of road traffic research. *Proceedings of the Institution of Civil Engineers*, Part II, 1, 325-378.
- Beckmann, M., McGuire, C. B., Winsten, C. B. (1956). *Studies in the Economics of Transportation*. Yale University Press.
- Frank, M., Wolfe, P. (1956). An algorithm for quadratic programming. *Naval Research Logistics Quarterly*, 3, 95-110.
- LeBlanc, L. J., Morlok, E. K., Pierskalla, W. P. (1975). An efficient approach to solving the road network equilibrium traffic assignment problem. *Transportation Research*, 9, 309-318.
- Ortúzar, J. de D., Willumsen, L. G. (2011). *Modelling Transport*. Wiley.
- Bar-Gera, H. *Transportation Network Test Problems* (TNTP). Repository [bstabler/TransportationNetworks](https://github.com/bstabler/TransportationNetworks), SiouxFalls folder.
