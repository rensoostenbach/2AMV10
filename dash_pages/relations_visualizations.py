import dash_bootstrap_components as dbc
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_cytoscape as cyto
from dash.dependencies import Input, Output
import plotly.express as px

from app import app

from classes.BipartiteGraph import *
from classes.Person import *
from classes.Object import *

stylesheet = [{
        'selector': 'node',
        'style': {
            'content': 'data(label)'
        }
    },
    {
        'selector': '.object',
        'style': {
            'width': 50,
            'height': 50,
            'background-fit': 'cover',
            'background-image': 'data(url)'
        }
    },
    {
        'selector': '[weight <= 1]',
        'style': {
            'line-color': 'green'
        }
    },
    {
        'selector': '[weight <= 0.9]',
        'style': {
            'line-color': 'rgb(64,255,0)'
        }
    },
    {
        'selector': '[weight <= 0.8]',
        'style': {
            'line-color': 'rgb(128,255,0)'
        }
    },
    {
        'selector': '[weight <= 0.7]',
        'style': {
            'line-color': 'rgb(192,255,0)'
        }
    },
    {
        'selector': '[weight <= 0.6]',
        'style': {
            'line-color': 'yellow'
        }
    },
    {
        'selector': '[weight <= 0.5]',
        'style': {
            'line-color': 'rgb(255,192,0)'
        }
    },
    {
        'selector': '[weight <= 0.4]',
        'style': {
            'line-color': 'rgb(255,128,0)'
        }
    },
    {
        'selector': '[weight <= 0.3]',
        'style': {
            'line-color': 'rgb(255,64,0)'
        }
    },
    {
        'selector': '[weight <= 0.2]',
        'style': {
            'line-color': 'red'
        }
    }
]


def getContent():
    title = html.H1('People and their relationship to objects', style={"font-size": "40px"})

    graph = dcc.Loading(id='graph',
                        children=[html.Div(id='chosen-graph-model', children=[html.P('No model chosen yet'),
                                                                              cyto.Cytoscape(id='bipartite-graph')])])

    return html.Div(children=[title, graph])


@app.callback(
    Output('chosen-graph-model', 'children'),
    Input('model-dropdown', 'value'),
    Input('confidence-threshold', 'value'),
    Input('clusters', 'value'))
def update_graph(model_path, confidence_threshold, k):
    model_path = Path(model_path)
    persons = getPersonsFrom(model_path)
    objects = getObjects()

    elements = getElementsFrom(persons, objects, confidence_threshold)

    graph = cyto.Cytoscape(
        id='bipartite-graph',
        elements=elements,
        layout={'name': 'preset'},
        style={'width': '100%', 'height': '1500px', 'background': 'black'},
        stylesheet=stylesheet
    )

    return graph


@app.callback(Output('bipartite-graph', 'stylesheet'),
              Output('selected-person', 'children'),
              Output('selected-object', 'children'),
              Input('bipartite-graph', 'tapNodeData'))
def color_children(tapNodeData):
    if not tapNodeData:
        return stylesheet, "", ""

    children_style = []
    selected_person = ""
    selected_object = ""

    if 'parent' in tapNodeData:
        if tapNodeData['parent'] == 'persons':
            children_style = [{
                'selector': f'edge[source != "{tapNodeData["id"]}"]',
                'style': {
                    'opacity': '0.03'
                },
            }]
            selected_person = tapNodeData['id']
        else:
            children_style = [{
                'selector': f'edge[target != "{tapNodeData["id"]}"]',
                'style': {
                    'opacity': '0.03'
                }
            }]
            selected_object = tapNodeData['id']

    return stylesheet + children_style, selected_person, selected_object


def setStateWithTappedNode(tapNodeData):
    if not tapNodeData:
        return stylesheet

    if 'parent' in tapNodeData:
        if tapNodeData['parent'] == 'persons':
            pass
        else:
            pass
    else:
        pass

    return None


def getElementsFrom(persons, objects, confidence_threshold):
    elements = [
        {
            'data': {'id': 'persons', 'label': 'Persons'}
        },
        {
            'data': {'id': 'objects', 'label': 'Objects'}
        }]

    person_nodes = [{'data': {'id': person.id, 'label': person.id, 'parent': 'persons'},
                     'position': {'x': -1000, 'y': (i + 1) * 100}}
                    for i, person in enumerate(persons)]

    object_nodes = [{'classes': 'object',
                     'data': {'id': object.name, 'label': object.name, 'parent': 'objects',
                              'url': object.images[0].githubURL},
                     'position': {'x': 1000, 'y': (i + 1) * 100}}
                    for i, object in enumerate(objects)]

    edges = []
    for person in persons:
        for img in person.images:
            for prediction in img.predictions:
                if prediction.score >= confidence_threshold:
                    edge = {'data': {'source': person.id, 'target': prediction.label, 'weight': prediction.score}}
                    edges.append(copy.deepcopy(edge))

    return elements + person_nodes + object_nodes + edges
