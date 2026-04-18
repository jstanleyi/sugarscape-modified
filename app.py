from model import SugarScapeModel
from mesa.visualization import Slider, SolaraViz, make_plot_component
from mesa.visualization.components.matplotlib_components import make_mpl_space_component
from mesa.visualization.components import AgentPortrayalStyle, PropertyLayerStyle

def agent_portrayal(agent):
    return AgentPortrayalStyle(
        color="red",
        marker="o",
        size=10,
    )

def propertylayer_portrayal(layer):
    return PropertyLayerStyle(
        color="yellow", alpha=0.8, colorbar=True, vmin=0, vmax=10
    )

sugarscape_space = make_mpl_space_component(
    agent_portrayal=agent_portrayal,
    propertylayer_portrayal=propertylayer_portrayal,
    post_process=None,
    draw_grid=False,
)

# Modification: more plots
GiniPlot = make_plot_component("Gini")
PopulationPlot = make_plot_component("Population")
MeanSugarPlot = make_plot_component("MeanSugar")

model_params = {
    "seed": {
        "type": "InputText",
        "value": 42,
        "label": "Random Seed",
    },
    "width": 50,
    "height": 50,
    "initial_population": Slider(
        "Initial Population", value=200, min=50, max=500, step=10
    ),
    
    "endowment_min": Slider("Min Initial Endowment", value=25, min=5, max=30, step=1),
    "endowment_max": Slider("Max Initial Endowment", value=50, min=30, max=100, step=1),
    
    "metabolism_min": Slider("Min Metabolism", value=1, min=1, max=3, step=1),
    "metabolism_max": Slider("Max Metabolism", value=5, min=3, max=8, step=1),
    
    "vision_min": Slider("Min Vision", value=1, min=1, max=3, step=1),
    "vision_max": Slider("Max Vision", value=5, min=3, max=8, step=1),
}

model = SugarScapeModel()

# Modification: more plots
page = SolaraViz(
    model,
    components=[
        sugarscape_space,
        GiniPlot,
        PopulationPlot,
        MeanSugarPlot,
    ],
    model_params=model_params,
    name="Sugarscape",
    play_interval=150,
)

page
