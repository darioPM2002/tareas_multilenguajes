from random_agents.agent import DrawAgent, Basura, EstacionCarga, ObstacleAgent, Roomba, greenAgent
from random_agents.model import RandomModel

from mesa.visualization import (
    Slider,
    SolaraViz,
    make_space_component,
    make_plot_component,
)

from mesa.visualization.components import AgentPortrayalStyle

def random_portrayal(agent):
    if agent is None:
        return

    portrayal = AgentPortrayalStyle(
        size=28,
        marker="s",
    )

    if isinstance(agent, DrawAgent):
        portrayal.color = "#40FF001E"
        portrayal.marker = "s"
        portrayal.size = 100
    if isinstance(agent, EstacionCarga):
        portrayal.color = "#66FF00FF"
        portrayal.marker = "p"
        portrayal.size = 100
    elif isinstance(agent, ObstacleAgent):
        portrayal.color = "red"
        portrayal.marker = "h"
        portrayal.size = 100
    elif isinstance(agent, Roomba):
       portrayal.color = "purple"
       portrayal.marker = "s"
       portrayal.size = 100
    elif isinstance(agent, greenAgent):
            portrayal.color = "green"
            portrayal.marker = "s"
            portrayal.size = 100

    return portrayal

def post_process(ax):
    ax.set_aspect("equal")

def post_process_lines(ax):
    ax.legend(loc="center left", bbox_to_anchor=(1, 0.9))
model_params = {
    "seed": {
        "type": "InputText",
        "value": 42,
        "label": "Random Seed",
    },
    "num_agents": Slider("Número total de elementos (basura + obstáculos)", 20, 1, 200),

    # NUEVOS SLIDERS
 "porcentaje_basura": Slider("Porcentaje basura", 0.3, 0, 1, step=0.05),
"porcentaje_obstaculos": Slider("Porcentaje obstáculos", 0.3, 0, 1, step=0.05),

    "width": Slider("Grid width", 28, 1, 50),
    "height": Slider("Grid height", 28, 1, 50),
}

# Create the model using the initial parameters from the settings
model = RandomModel(
    num_agents=model_params["num_agents"].value,
    width=model_params["width"].value,
    height=model_params["height"].value,
    seed=model_params["seed"]["value"],
    porcentaje_basura=model_params["porcentaje_basura"].value,
    porcentaje_obstaculos=model_params["porcentaje_obstaculos"].value
)

space_component = make_space_component(
        random_portrayal,
        draw_grid = False,
        post_process=post_process
)

# Componente de gráfica para monitorear batería, basuras y celdas mapeadas
lineplot_component = make_plot_component(
    {
        "Batería": "tab:green",
        "Basuras": "tab:red", 
        "Celdas Mapeadas": "tab:blue"
    },
    post_process=post_process_lines,
)

page = SolaraViz(
    model,
    components=[space_component, lineplot_component],
    model_params=model_params,
    name="Random Model",
)