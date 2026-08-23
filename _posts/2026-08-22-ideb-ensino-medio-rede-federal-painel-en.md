---
layout: post
title: "How to Compute the Federal Network's Ideb When INEP Does Not Publish That Series"
lang: en
translation: "/2026/08/22/ideb-ensino-medio-rede-federal-painel.html"
permalink: /en/2026/08/22/ideb-ensino-medio-rede-federal-painel.html
category: "General"
image: /assets/images/posts/ideb-ensino-medio-rede-federal-painel.webp
math: true
---

Between 2019 and 2025 the average secondary-education Ideb rose in the state-run schools and fell in the federal schools I traced through a balanced panel (method explained below): from 4.17 to 4.53 in the state network, from 5.63 to 5.42 in the federal one. Both movements share the same cause, and that cause is not the Saeb score.

![Two diagrammatic curves side by side, one rising and one falling, driven by the same golden ratchet mechanism between them](/assets/images/posts/ideb-ensino-medio-rede-federal-painel.webp)

## What the Ideb actually is

The Ideb is a product: $$\text{Ideb} = P \times N$$. $$N$$ is the standardized Saeb score in Portuguese and Math. $$P$$ is the flow indicator, which INEP derives from the pass rates recorded in the School Census. INEP's release spreadsheet carries $$P$$ and the raw pass rate in separate columns, `VL_INDICADOR_REND` and `VL_APROVACAO`, and they diverge: in Minas Gerais's state network in 2021, $$P$$ = 0.8769 against a raw pass rate of 91.3%. What enters the index's identity is $$P$$, not the raw pass rate that comes straight out of the Census. The gap is small in most years, but it is real, and mixing up the two columns is the first way to get this arithmetic wrong.

## The problem: INEP does not publish this number

Anyone who wants a state network's secondary Ideb by state finds it ready-made in the "UF e Regiões (EM)" tab of INEP's release spreadsheet. Anyone who wants the same number for the federal network does not: that tab only carries Total, Private and State. The federal network simply has no row there. Across the two release spreadsheets I use here, the way to reach a federal-network Ideb is to compute it school by school, from the per-school release tab. I did not check whether some other INEP spreadsheet, outside these two, already carries the federal network aggregated.

## The trap of a direct average

This looks solved by taking a simple average of whatever federal schools INEP published that year. It is not. Coverage of federal schools with a published Ideb, nationally: 135 in 2017, 151 in 2019, 35 in 2021, 157 in 2023, 236 in 2025. In Minas Gerais: 21, 18, 4, 21, 37. A school only gets a published Ideb once it clears the minimum Saeb participation and the minimum completion of the cycle, and that set of schools changes composition every edition. The drop to 35 schools nationally in 2021 is the pandemic cutting participation, not the federal network shrinking.

An average that mixes a different set of schools every year does not measure the network's evolution: it measures who happened to report that year. It is the same reason this project already bans publishing an aggregated yearly average across CEFET-MG's own campuses (none of its 9 units has a complete five-edition series, and the set that reports changes year to year). The problem here is the same one, at national scale.

## The method: balanced panel and Shapley decomposition

The way out is to restrict the comparison to schools with published data in both years being compared, a balanced panel. That discards most of the 596 federal schools listed in the 2025 spreadsheet (leaving 70 in the 2019-to-2025 cut, nationally), but it guarantees the measured change comes from the same school at both points, not from schools entering and leaving the sample.

With the panel fixed, I decompose the index's change between the identity's two factors using the Shapley decomposition of a product, which splits the change in $$P \times N$$ into two terms that sum exactly to the observed change:

$$\text{flow effect} = (P_1 - P_0) \times \frac{N_0 + N_1}{2}$$

$$\text{learning effect} = (N_1 - N_0) \times \frac{P_0 + P_1}{2}$$

The first isolates how much of the product changed because the flow indicator changed, holding the score at the two years' average; the second isolates how much changed because the score changed, holding the indicator at the average. The two together close exactly against the change in $$P \times N$$, with no residual.

## Testing the method before using it

Before applying this panel to a number INEP does not publish, I tested it against one INEP does publish: the official state series for Minas Gerais, computed by INEP itself over the whole network, and already decomposed earlier in this project. If the balanced panel reproduces the official decomposition within a small margin, the method is not distorting the reading by restricting the sample.

Over 2017 to 2025, the state panel for Minas Gerais returns 79.2% flow effect, against 80.6% in INEP's official series. Over 2019 to 2025, it returns 104.5%, against 106.4% official. The gap stays under 2 percentage points in both cases. That is how a method gets validated before it is used on a cut with no official counterpart to check against.

## The result: Brazil, 2019 to 2025

With the method validated, I apply the same panel to the cut that started this: the secondary-education Ideb of the federal network nationally, which INEP does not publish as a series.

| Network (panel) | Year | Average Ideb | P (indicator) | Raw pass rate | Saeb score (N) |
|---|---|---|---|---|---|
| Federal (70 schools) | 2019 | 5.63 | 0.9203 | 91.77% | 6.10 |
| Federal (70 schools) | 2025 | 5.42 | 0.9362 | 93.47% | 5.79 |
| State (10,713 schools) | 2019 | 4.17 | 0.8930 | 89.12% | 4.65 |
| State (10,713 schools) | 2025 | 4.53 | 0.9622 | 96.12% | 4.70 |

The Average Ideb column is the average of the Ideb INEP published school by school. The decomposition below operates on the product of the averages of $$P$$ and $$N$$, which goes from 5.618 to 5.416 in the federal network and from 4.156 to 4.520 in the state one: that is the change the two terms close against with no residual, hence the difference of a few hundredths against the Average Ideb column.

And the Shapley decomposition of the $$P \times N$$ product in each network:

| Network | Flow effect | % of total | Learning effect | % of total |
|---|---|---|---|---|
| Federal | +0.0943 | -46.8% | -0.2959 | 146.8% |
| State | +0.3238 | 88.8% | +0.0407 | 11.2% |

The reading is the same in both networks, and it is the point of this post: where the flow indicator still had room to rise, the index rose with the Saeb score essentially flat (in the state network, close to 90% of the gain comes from flow). Where it was already near its ceiling, as in the federal network, the room ran out, and the falling score showed up almost entirely in the index: the negative learning effect (-0.2959) is larger in absolute value than the product's own drop (-0.2017), because flow still pulled a little upward without offsetting the score's fall.

## The caveats, unsoftened

This number is not the federal network's official Ideb, for five concrete reasons.

**It is not weighted by enrollment.** What the panel computes is a simple average of the Ideb across schools. The official Ideb INEP publishes for a network is computed from the network's pooled students, not from an average across schools. These are different calculations, and a simple average can drift when large and small schools behave differently.

**Selection bias.** The panel uses 70 of the 596 federal schools listed in the 2025 spreadsheet. These are the schools that managed to keep reporting in both years compared, which is already, by itself, a non-random trait.

**The federal panel for Minas Gerais is not part of this comparison.** It has 10 schools in the 2019-to-2025 cut, below what can be treated as representative, so it was left out.

**Composition of the national federal panel.** Of the 70 schools, 63 are federal institutes, CEFETs or technical schools tied to universities; 5 are application schools or similar; 2 are military schools. Excluding the two military schools from the calculation does not change the result.

**2021 is excluded from any comparison.** The pandemic artificially inflated the flow indicator in nearly every network, through automatic promotion and reduced Saeb participation, which makes any reading that includes 2021 as a comparison point unreliable.

## What remains

The index measures two things, and only one of them is learning. It is possible to raise the Ideb without raising learning, and the state network did exactly that between 2019 and 2025. It is also possible for the score to fall and the index to fall with it, even as the pass rate keeps rising, because the room in flow had already run out: that is what happened in the federal network. Both are the same mechanism seen from two different starting points, and neither shows up if the reading stops at the published number without opening up the product.

---

*Source: INEP, per-school Ideb release spreadsheet for secondary education, 2025 edition (`divulgacao_ensino_medio_escolas_2025.xlsx`, tab "IDEB_Escolas (ENSINO MÉDIO)"). The raw file has a registered sha256, and the computation, including the balanced panel and the Shapley decomposition, is reproducible from it.*
