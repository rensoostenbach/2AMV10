import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc


# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "30rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    "font-size": "14px",
}


def getSidebar(models):
    return html.Div(
        [
            html.H2("Sidebar", className="display-4"),
            html.Hr(),
            getNavigation(),
            html.Hr(),
            getConfidenceThresholdSlider(),
            html.P(),
            getModelDropdown(models),
            html.P(),
            getGradcamComputationSelector(),
            html.P(),
            getDistributionSelector(),
            html.P(),
            getClusterSelector(),
            html.Div(id="selected-person", children="", hidden=True),
            html.Div(id="selected-object", children="", hidden=True),
        ],
        style=SIDEBAR_STYLE,
    )


def getNavigation():
    return dbc.Nav(
        [
            dbc.NavLink("People", href="/", active="exact"),
            dbc.NavLink("Objects", href="/objects", active="exact"),
            dbc.NavLink("Distributions", href="/distributions", active="exact"),
            dbc.NavLink(
                "Relationship between person and object",
                href="/relations_visualizations",
                active="exact",
            ),
        ],
        vertical=True,
        pills=True,
        style={"font-size": "20px"},
    )


def getConfidenceThresholdSlider():
    return html.Div(
        id="confidence-threshold-group",
        children=[
            html.H3("Confidence threshold"),
            dcc.Slider(
                id="confidence-threshold",
                min=0.085,
                max=1,
                step=0.001,
                value=0.5,
                marks={
                    0.1: "0.1",
                    0.2: "0.2",
                    0.3: "0.3",
                    0.4: "0.4",
                    0.5: "0.5",
                    0.6: "0.6",
                    0.7: "0.7",
                    0.8: "0.8",
                    0.9: "0.9",
                    1: "1.0",
                },
            ),
            html.Div(id="confidence-threshold-output"),
            html.P("All predictions with a score below this threshold are not shown."),
        ],
    )


def getModelDropdown(models):
    return html.Div(
        id="model-group",
        children=[
            html.H3("Model"),
            dcc.Dropdown(
                id="model-dropdown",
                options=models,
                value="../2AMV10/data/raw/",
                clearable=False,
            ),
        ],
    )


def getGradcamComputationSelector():
    return html.Div(
        id="gradcam-group",
        children=[
            html.H3("Gradcam computation"),
            html.P("Run Grad-CAM (longer computation time) or use precomputed images"),
            dcc.RadioItems(
                id="gradcam-computation",
                options=[
                    {"label": "Grad-CAM", "value": 1},
                    {"label": "Precomputed images", "value": 0},
                ],
                value=0,
                labelStyle={"display": "block"},
            ),
        ],
        hidden=True,
    )


def getDistributionSelector():
    return html.Div(
        id="distribution-group",
        children=[
            html.H3("People or objects"),
            html.P("Choose whether you want people or objects on the x-axis"),
            dcc.RadioItems(
                id="distribution-selection",
                options=[
                    {"label": "People", "value": 0},
                    {"label": "Objects", "value": 1},
                ],
                value=0,
                labelStyle={"display": "block"},
            ),
        ],
        hidden=True,
    )


def getClusterSelector():
    return html.Div(
        id="cluster-group",
        children=[
            html.H3("Select the number of clusters"),
            dcc.Slider(
                id="clusters",
                min=1,
                max=20,
                step=1,
                value=1,
                marks={1: "1", 10: "10", 20: "20", 30: "30", 40: "40"},
            ),
        ],
        hidden=True,
    )
