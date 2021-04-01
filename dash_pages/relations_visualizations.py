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

numbers = { 0 : 'zero', 1 : 'one', 2 : 'two', 3 : 'three', 4 : 'four', 5 : 'five',
          6 : 'six', 7 : 'seven', 8 : 'eight', 9 : 'nine', 10 : 'ten',
          11 : 'eleven', 12 : 'twelve', 13 : 'thirteen', 14 : 'fourteen',
          15 : 'fifteen', 16 : 'sixteen', 17 : 'seventeen', 18 : 'eighteen',
          19 : 'nineteen', 20: 'twenty'}

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
    },
]

colors = ['#e6194B', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#42d4f4', '#f032e6', '#bfef45', '#fabed4', '#469990', '#dcbeff', '#9A6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#a9a9a9', '#ffffff', '#000000']

for number in numbers:
    stylesheet.append({
        'selector': '.' + numbers[number],
        'style': {
            'background-color': colors[number]
        }
    },)

def getContent():
    title = html.H1('People and their relationship to objects', style={"font-size": "40px"})
    desc = html.P('This bipartite graph shows the relation of people to objects. Clicking on a person will highlight'
                  ' the edges to the objects he/she is related to. Clicking on an object will highlight the edges to'
                  ' the people this object is related to. The color of an edge shows its confidence, which is a'
                  ' gradient going from low to high confidence: red, orange, yellow, green.'
                  ' The color of a node represents its cluster.', style={'font-size': '15px'})

    graph = dcc.Loading(
        id='graph',
        children=[html.Div(id='chosen-graph-model',
                           children=[html.P('No model chosen yet'), cyto.Cytoscape(id='bipartite-graph')],
                           style={'height': '100%'})],
        style={'height': '100%'},
    )

    return html.Div(children=[title, desc, graph], style={
        'background-color': 'black',
        'color': 'white',
        'height': '950px',
    })


@app.callback(
    Output('chosen-graph-model', 'children'),
    Input('model-dropdown', 'value'),
    Input('confidence-threshold', 'value'),
    Input('clusters', 'value'))
def update_graph(model_path, confidence_threshold, k):
    model_path = Path(model_path)
    objects = getObjects()
    persons = getPersonsFrom(model_path, objects, k, True)

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
            }, {
                'selector': f'edge[source == "{tapNodeData["id"]}"]',
                'style': {
                    'line-width': '6'
                },
            }]
            selected_person = tapNodeData['id']
        else:
            children_style = [{
                'selector': f'edge[target != "{tapNodeData["id"]}"]',
                'style': {
                    'opacity': '0.03'
                }
            }, {
                'selector': f'edge[source == "{tapNodeData["id"]}"]',
                'style': {
                    'line-width': '6'
                },
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

    person_nodes = [{'data': {'id': person.id, 'label': person.cluster, 'parent': 'persons'},
                     'position': {'x': -1000, 'y': (i + 1) * 100}, 'classes': numbers[int(person.cluster)]}
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
