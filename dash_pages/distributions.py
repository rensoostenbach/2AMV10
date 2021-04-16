import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output

from app import app
from classes.Object import *
from classes.Person import *


def getContent():
    text = [
        html.H1("Distributions", style={"font-size": "40px"}),
        html.P(
            "This page will show the distributions of people and objects. You can choose whether you would "
            "like to see the objects that people have in their pictures, or the people that have a certain "
            "object in their pictures."
        ),
        html.Hr(),
    ]

    graph = [
        dcc.Loading(
            id="dist-graph",
            children=dcc.Graph(
                id="dist-graph-model", figure={"layout": {"height": 700}}
            ),
        )
    ]

    return html.Div(
        children=text + graph, style={"font-size": "20px", "height": "700px"}
    )


@app.callback(
    Output("dist-graph-model", "figure"),
    Input("distribution-selection", "value"),
    Input("model-dropdown", "value"),
    Input("confidence-threshold", "value"),
)
def update_output(pers_obj, model_path, confidence_threshold):
    model_path = Path(model_path)
    persons = getPersonsFrom(model_path)
    persons_ids = getPersonIdsFrom(model_path)
    objects = getObjectNamesFrom(Path("../2AMV10/data/raw/TrainingImages/"))

    df = getDataframeWithObjectsPersonsAndPredictions(
        confidence_threshold, objects, persons, persons_ids
    )

    bars = []
    if pers_obj == 0:  # Persons
        for obj in objects:
            bars.append(go.Bar(name=obj, x=persons_ids, y=df[obj]))
    else:  # Objects
        for person_id in persons_ids:
            bars.append(
                go.Bar(name=person_id, x=objects, y=df.iloc[int(person_id) - 1])
            )

    fig = go.Figure(data=bars)
    fig.update_layout(barmode="stack")
    return fig


def getDataframeWithObjectsPersonsAndPredictions(
    confidence_threshold, objects, persons, persons_ids
):
    df = pd.DataFrame(0, columns=objects, index=persons_ids)
    setPredictionsAboveConfidenceThreshold(df, confidence_threshold, persons)
    return df


def setPredictionsAboveConfidenceThreshold(df, confidence_threshold, persons):
    for person in persons:
        for img in person.images:
            for prediction in img.predictions:
                if prediction.score >= confidence_threshold:
                    df[prediction.label][person.id] += 1
