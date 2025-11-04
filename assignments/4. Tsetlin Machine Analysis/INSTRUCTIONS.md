# Assignment – dynamic visualization

<div style="display: flex; gap: 12px; align-items: flex-start;">
  <img src="/home/ignacio/Proyects/2025/Learning-Systems/assignments/4. Tsetlin Machine Analysis/images/distribution.png" alt="distribution" style="width: 49%; max-width: 49%;" />
  <img src="/home/ignacio/Proyects/2025/Learning-Systems/assignments/4. Tsetlin Machine Analysis/images/formulas.png" alt="formulas" style="width: 80%; max-width: 49%;" />
  
</div>

- Create an interactive stationary distribution bar chart for a Literal Automaton with eight states (see example bar chart to the left).
- Use the above equations to calculate the height of each of the eight bars.
- Create dynamic sliders for: s, P(L|Y), P(Y), P(L|Y)). The s-slider can go from 1.0 to 25.0. The other sliders go from 0.0 to 1.0.
- Note that: P(L|¬Y) = 1.0 − P(L|Y) and P(¬Y) = 1.0 − P(Y)
- Possible tool: https://dash.plotly.com/