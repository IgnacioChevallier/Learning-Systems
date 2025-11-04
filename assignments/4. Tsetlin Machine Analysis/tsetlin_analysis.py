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

def build_transition_matrix(s: float, p_l_given_y: float, p_y: float, p_notl_given_noty: float) -> np.ndarray:
    """
    Build an 8x8 transition matrix for a simplified literal automaton.

    Parameters
    - s: sensitivity parameter (here used to modulate step strength)
    - p_l_given_y: P(L|Y)
    - p_y: P(Y)
    - p_notl_given_noty: P(NOT L | NOT Y)

    Derived:
    - p_l_given_not_y = 1 - p_notl_given_noty
    - p_not_y = 1 - p_y
    - reward prob (towards extreme): p_reward = p_y * p_l_given_y
    - penalty prob (towards center): p_penalty = p_y * (1 - p_l_given_y) + p_not_y * p_l_given_not_y
    - stay = 1 - p_reward - p_penalty (clipped to [0,1])
    """
    p_l_given_not_y = 1.0 - p_notl_given_noty
    p_not_y = 1.0 - p_y

    p_reward = p_y * p_l_given_y
    p_penalty = p_y * (1.0 - p_l_given_y) + p_not_y * p_l_given_not_y
    p_stay = max(0.0, min(1.0, 1.0 - p_reward - p_penalty))

    # Modulate step intensity slightly with s (bounded factor)
    # Higher s -> slightly stronger movement per step.
    step_scale = 0.5 + 0.5 * min(max((s - 1.0) / 24.0, 0.0), 1.0)
    r = p_reward * step_scale
    q = p_penalty * step_scale
    z = max(0.0, min(1.0, 1.0 - r - q))  # re-normalized stay

    T = np.zeros((NUM_STATES, NUM_STATES), dtype=float)

    # Include side: 0..3 (0 extreme)
    for i in range(0, 4):
        to_extreme = max(0, i - 1)  # move left
        to_center = min(3, i + 1)   # move right
        T[i, to_extreme] += r
        T[i, to_center] += q
        T[i, i] += z

    # Exclude side: 4..7 (7 extreme)
    for i in range(4, 8):
        to_center = max(4, i - 1)   # move left (toward boundary)
        to_extreme = min(7, i + 1)  # move right (toward extreme)
        T[i, to_extreme] += r
        T[i, to_center] += q
        T[i, i] += z

    # Small bleed across boundary to avoid trapping (optional, very small)
    epsilon = 1e-6
    T[3, 4] += epsilon
    T[4, 3] += epsilon
    T = T / T.sum(axis=1, keepdims=True)
    return T


def stationary_distribution(T: np.ndarray, tol: float = 1e-10, iters: int = 20000) -> np.ndarray:
    """
    Power iteration to approximate the stationary distribution.
    """
    n = T.shape[0]
    p = np.full(n, 1.0 / n, dtype=float)
    for _ in range(iters):
        p_next = p @ T
        if np.max(np.abs(p_next - p)) < tol:
            return p_next / p_next.sum()
        p = p_next
    return p / p.sum()


## -------------------------------------------------------------
## DASH APP CREATION
## -------------------------------------------------------------

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
    T = build_transition_matrix(s, p_l_given_y, p_y, p_notl_given_noty)
    pi = stationary_distribution(T)
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


