import math

import solara
from agents import State
from model import FakeNewsModel

from mesa.visualization import (
    Slider,
    SolaraViz,
    SpaceRenderer,
    make_plot_component,
)
from mesa.visualization.components import AgentPortrayalStyle


def agent_portrayal(agent):
    node_color_dict = {
        State.SUSCEPTIBLE: "gray",
        State.BELIEVE: "red",
        State.DENY: "blue",
        State.CURED: "green",
    }
    return AgentPortrayalStyle(color=node_color_dict[agent.state], size=10)

model_params = {
    "seed": {
        "type": "InputText",
        "value": 42,
        "label": "Random Seed",
    },
    "p_infl": Slider(
        label="p_infl",
        value=0.05,
        min=0.0,
        max=1,
        step=0.01,
    ),
}


def post_process_lineplot(chart):
    chart = chart.properties(
        width=400,
        height=400,
    ).configure_legend(
        strokeColor="black",
        fillColor="#ECE9E9",
        orient="right",
        cornerRadius=5,
        padding=10,
        strokeWidth=1,
    )
    return chart


model1 = FakeNewsModel()
renderer = SpaceRenderer(model1, backend="altair")
renderer.draw_structure(
    node_kwargs={"color": "black", "filled": False},
    edge_kwargs={"strokeDash": [6, 1]},
)  # Do this to draw the underlying network and customize it
renderer.draw_agents(agent_portrayal)

# Plot components can also be in altair and support post_process
StatePlot = make_plot_component(
    {"Susceptible": "gray", "Believe": "red", "Deny": "blue", "Cured": "green"},
    backend="altair",
    post_process=post_process_lineplot,
)

page = SolaraViz(
    model1,
    renderer,
    components=[
        StatePlot,
    ],
    model_params=model_params,
    name="Fake News Model",
)
page  # noqa
