from __future__ import annotations
import numpy as np

from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
from layout.styles import (
    CONTAINER_STYLE,
    TITLE_STYLE,
    GRAPH_STYLE,
    CONTROLS_WRAPPER_STYLE,
    CONTROL_BLOCK_STYLE,
    LABEL_STYLE,
)

NUM_STATES = 8


def calculate_stationary_distribution(s: float, p_l_given_y: float, p_y: float, p_notl_given_noty: float) -> np.ndarray:
    """
    Calculate stationary distribution directly using the formulas from the lecture images.

    Parameters
    - s: sensitivity parameter
    - p_l_given_y: P(L|Y)
    - p_y: P(Y)
    - p_notl_given_noty: P(NOT L | NOT Y)

    Returns normalized array [π1, π2, ..., π8] representing bar heights.
    """
    # Complements
    p_not_y = 1.0 - p_y
    p_notl_given_y = 1.0 - p_l_given_y

    # Shorthand used in the formulas
    A = p_l_given_y * p_y + p_notl_given_noty * p_not_y

    # Unnormalized pi_i (exactly following the image)
    pi1 = (p_y**4)         * (p_notl_given_y**7)
    pi2 = (p_y**3)         * (p_notl_given_y**6) * (s**1) * (A**1)
    pi3 = (p_y**2)         * (p_notl_given_y**5) * (s**2) * (A**2)
    pi4 = (p_y**1)         * (p_notl_given_y**4) * (s**3) * (A**3)
    pi5 =                    (p_notl_given_y**3) * (s**4) * (A**4)
    pi6 = (p_l_given_y**1) * (p_notl_given_y**2) * (s**5) * (A**4)
    pi7 = (p_l_given_y**2) * (p_notl_given_y**1) * (s**6) * (A**4)
    pi8 = (p_l_given_y**3)                       * (s**7) * (A**4)

    pis = np.array([pi1, pi2, pi3, pi4, pi5, pi6, pi7, pi8], dtype=float)

    # Normalize with α so that sum pi_i = 1
    total = pis.sum()

    return pis / total


# --------------------------------------------------------------------
# FROM HERE ONWARDS IS FRONTEND CODE, NOT IMPORTANT FOR THE ASSIGNMENT
# --------------------------------------------------------------------

app = Dash(__name__)

app.layout = html.Div([
    html.H2("Literal Automaton Stationary Distribution (8 states)", style=TITLE_STYLE),
    dcc.Graph(id='bar', style=GRAPH_STYLE),
    html.Div([
        html.Div([
            html.Label("s (sensitivity):", style=LABEL_STYLE),
            dcc.Slider(
                id='s', min=1.0, max=25.0, step=0.5, value=10.0,
                marks={1: '1', 5: '5', 10: '10', 15: '15', 20: '20', 25: '25'}
            )
        ], style=CONTROL_BLOCK_STYLE),
        html.Div([
            html.Label("P(L|Y):", style=LABEL_STYLE),
            dcc.Slider(
                id='p_l_given_y', min=0.0, max=1.0, step=0.01, value=0.7,
                marks={0: '0.0', 0.5: '0.5', 1.0: '1.0'}
            )
        ], style=CONTROL_BLOCK_STYLE),
        html.Div([
            html.Label("P(NOT L | NOT Y):", style=LABEL_STYLE),
            dcc.Slider(
                id='p_notl_given_noty', min=0.0, max=1.0, step=0.01, value=0.7,
                marks={0: '0.0', 0.5: '0.5', 1.0: '1.0'}
            )
        ], style=CONTROL_BLOCK_STYLE),
        html.Div([
            html.Label("P(Y):", style=LABEL_STYLE),
            dcc.Slider(
                id='p_y', min=0.0, max=1.0, step=0.01, value=0.5,
                marks={0: '0.0', 0.5: '0.5', 1.0: '1.0'}
            )
        ], style={'width': '100%'})
    ], style=CONTROLS_WRAPPER_STYLE)
], style=CONTAINER_STYLE)


@app.callback(
    Output('bar', 'figure'),
    Input('s', 'value'),
    Input('p_l_given_y', 'value'),
    Input('p_y', 'value'),
    Input('p_notl_given_noty', 'value')
)
def update_chart(s: float, p_l_given_y: float, p_y: float, p_notl_given_noty: float):
    pi = calculate_stationary_distribution(s, p_l_given_y, p_y, p_notl_given_noty)
    x = [f"S{i+1}" for i in range(NUM_STATES)]
    fig = go.Figure(go.Bar(x=x, y=pi, marker_color="#154360"))
    fig.update_layout(
        yaxis_title="Stationary probability",
        xaxis_title="States (Include: S1-S4, Exclude: S5-S8)",
        template="plotly_white",
        margin=dict(l=40, r=20, t=30, b=40)
    )
    return fig


if __name__ == "__main__":
    app.run(debug=True)
