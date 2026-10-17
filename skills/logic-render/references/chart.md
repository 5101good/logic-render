# Data charts and report layouts

Open [sheet 01](../assets/chart-01.png) and [sheet 02](../assets/chart-02.png).
Each sheet contains four complete compositions in a 2×2 grid. Read left to
right, top to bottom. Sheet 01 contains 01–04; sheet 02 contains 05–08.

| ID | Panel | Appropriate relationship |
| --- | --- | --- |
| C01 | 趋势分析与指标 | A time trend with summary metrics and underlying detail |
| C02 | 分类对比与排序 | Comparing comparable series and ranking categories |
| C03 | 构成分析与明细 | Parts of a known whole, with an exact breakdown |
| C04 | 横向排名与分布 | Ranking measured amounts and showing their distribution |
| C05 | 进度与资源看板 | Progress against targets, alongside a task timeline |
| C06 | 规模趋势与结构 | Changes over time alongside composition |
| C07 | 指标小多图 | Comparable trends with common scales and a detail table |
| C08 | 监测报告 | A requested dark monitoring report with related views |

**These report layouts use synthetic demonstration data.** Values, shapes and
ring segments illustrate composition; actual charts require the user's data.
Use the hierarchy, spacing, legends, fine gridlines, annotation areas and detail
tables as the visual reference. Recompute every mark from the user's values.

Collect values, units, denominator, timeframe and source before plotting. Request
missing essentials; “faster” does not supply a percentage. Synthetic output data
requires explicit permission and a visible demonstration label.

- Prefer deterministic plotting or SVG for exact quantitative geometry. Choose
  chart types and report layout to answer the user's analytical question. Apply
  the reference's palette, fine rules, typography and spacing while calculating
  all marks from data; its chart selection and panel count are not mandatory.
- Bars start at zero; negatives extend from a common zero in the correct
  direction. Do not truncate a bar baseline to exaggerate differences.
- Check lengths, angles, areas, ticks, labels and percentages independently.
  Preserve measurement conditions, missingness, units and uncertainty.
- Keep axes and data marks front-facing. Use gradients and shadows in framing
  without changing the apparent encoded length or area.
- Choose a composite report only when its views answer related user questions.
  C08 alone is the dark navy/blue-violet variant.
- If precise geometry cannot be verified, say so and provide an exact plotted
  alternative when possible. A generated chart image is not numerical evidence.
