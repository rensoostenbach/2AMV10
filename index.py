import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

import dash_pages.objects as objects
import dash_pages.people as people
import dash_pages.relations_visualizations as relations
import dash_pages.distributions as distributions
import sidebar

from app import app

# the styles for the main content position it to the right of the sidebar and add some padding.
CONTENT_STYLE = {
    "margin-left": "32rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "height": "100%",
}

models = [
    {"label": "Given model", "value": "../2AMV10/data/raw/"},
    {
        "label": "Efficient DET",
        "value": "../2AMV10/trained_models/efficientdet_d0_tensorflow_v2/inference/output/",
    },
    {
        "label": "RCNN",
        "value": "../2AMV10/trained_models/faster_rcnn/inference/output/",
    },
    {
        "label": "YOLO v4 E:100 B:16",
        "value": "../2AMV10/trained_models/scaled_yolov4_100epochs_16batchsize/inference/output/",
    },
    {
        "label": "YOLO v4 E:100 B:32",
        "value": "../2AMV10/trained_models/scaled_yolov4_100epochs_32batchsize/inference/output/",
    },
    {
        "label": "YOLO v4 E:150 B:16",
        "value": "../2AMV10/trained_models/scaled_yolov4_150epochs_16batchsize/inference/output/",
    },
    {
        "label": "YOLO v5 E:100 B:16",
        "value": "../2AMV10/trained_models/yolov5l_100epochs_16batchsize/inference/output/",
    },
]

sidebar = sidebar.getSidebar(models)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(
    Output("page-content", "children"),
    Output("confidence-threshold-group", "hidden"),
    Output("model-group", "hidden"),
    Output("gradcam-group", "hidden"),
    Output("distribution-group", "hidden"),
    Output("cluster-group", "hidden"),
    [Input("url", "pathname")],
)
def render_page_content(pathname):
    if pathname == "/":
        return people.getContent(), False, False, True, True, True
    elif pathname == "/objects":
        return objects.getContent(), True, True, False, True, True
    elif pathname == "/relations_visualizations":
        return relations.getContent(), False, False, True, True, False
    elif pathname == "/distributions":
        return distributions.getContent(), False, False, True, False, True
    # If the user tries to reach a different page, return a 404 message
    return (
        dbc.Jumbotron(
            [
                html.H1("404: Not found", className="text-danger"),
                html.Hr(),
                html.P(f"The pathname {pathname} was not recognised..."),
            ]
        ),
        True,
        True,
        True,
        True,
    )


@app.callback(
    dash.dependencies.Output("confidence-threshold-output", "children"),
    [dash.dependencies.Input("confidence-threshold", "value")],
)
def update_output(value):
    return "The current threshold value is {}".format(value)


if __name__ == "__main__":
    app.config["suppress_callback_exceptions"] = True
    app.run_server(debug=False)
