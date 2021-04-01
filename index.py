import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

import dash_pages.objects as objects
import dash_pages.people as people
import dash_pages.relations_visualizations as relations

from app import app

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "30rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    "font-size": "14px"
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "32rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "height": '100%',
}

models = [{'label':'Given model', 'value': "../2AMV10/data/raw/"},
          {'label':'Efficient DET', 'value': "../2AMV10/trained_models/efficientdet_d0_tensorflow_v2/inference/output/"},
          {'label':'RCNN', 'value': "../2AMV10/trained_models/faster_rcnn/inference/output/"},
          {'label':'YOLO v4 E:100 B:16', 'value': "../2AMV10/trained_models/scaled_yolov4_100epochs_16batchsize/inference/output/"},
          {'label':'YOLO v4 E:100 B:32', 'value': "../2AMV10/trained_models/scaled_yolov4_100epochs_32batchsize/inference/output/"},
          {'label': 'YOLO v4 E:150 B:16', 'value': "../2AMV10/trained_models/scaled_yolov4_150epochs_16batchsize/inference/output/"},
          {'label': 'YOLO v5 E:100 B:16', 'value': "../2AMV10/trained_models/yolov5l_100epochs_16batchsize/inference/output/"}]

sidebar = html.Div(
    [
        html.H2("Sidebar", className="display-4"),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("People", href="/", active="exact"),
                dbc.NavLink("Objects", href="/objects", active="exact"),
                dbc.NavLink("Relationship between person and object", href="/relations_visualizations", active="exact"),
            ],
            vertical=True,
            pills=True,
            style={"font-size": "20px"}
        ),
        html.Hr(),
        html.Div(id='confidence-threshold-group', children=[
            html.H3('Confidence threshold'),
            dcc.Slider(id='confidence-threshold', min=0.085, max=1, step=0.001, value=0.5,
                       marks={0.1: '0.1', 0.2: '0.2', 0.3: '0.3', 0.4: '0.4', 0.5: '0.5', 0.6: '0.6', 0.7: '0.7', 0.8: '0.8', 0.9: '0.9', 1: '1.0'}),
            html.Div(id='confidence-threshold-output')]
        ),
        html.P(),
        html.Div(id='model-group', children=[
            html.H3('Model'),
            dcc.Dropdown(id='model-dropdown', options=models, value='../2AMV10/data/raw/', clearable=False)
        ]),
        html.P(),
        html.Div(id='gradcam-group', children=[
            html.H3('Gradcam computation'),
            html.P('Run Grad-CAM (longer computation time) or use precomputed images'),
            dcc.RadioItems(id='gradcam-computation',
                           options=[{'label': 'Grad-CAM', 'value': 1}, {'label': 'Precomputed images', 'value': 0}],
                           value=0,
                           labelStyle={'display': 'block'})
        ], hidden=True),
        html.P(),
        html.Div(id='cluster-group', children=[
            html.H3('Select the number of clusters'),
            dcc.Slider(id='clusters',
                       min=1, max=20, step=1, value=1,
                       marks={1: '1', 10: '10', 20: '20', 30: '30', 40: '40'})
        ], hidden=True)
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(
    Output("page-content", "children"),
    Output("confidence-threshold-group", "hidden"),
    Output("model-group", "hidden"),
    Output("gradcam-group", "hidden"),
    Output("cluster-group", "hidden"),
    [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return people.getContent(), False, False, True, True
    elif pathname == "/objects":
        return objects.getContent(), True, True, False, True
    elif pathname == "/relations_visualizations":
        return relations.getContent(), False, False, True, False
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    ), True, True, True, True

@app.callback(
    dash.dependencies.Output('confidence-threshold-output', 'children'),
    [dash.dependencies.Input('confidence-threshold', 'value')])
def update_output(value):
    return 'The current threshold value is {}'.format(value)


if __name__ == '__main__':
    app.run_server(debug=True)