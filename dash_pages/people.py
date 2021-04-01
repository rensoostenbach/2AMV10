import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from pathlib import Path
import pytorch_cnn_visualizations.src.gradcam as gradcam
from dash.exceptions import PreventUpdate

from classes.Person import *
from classes.DataImage import *

from app import app


def getContent():
    children = [html.H1("People and their photos", style={"font-size": "40px"}),
                html.P('Select a person:'),
                dcc.Dropdown(id='person-dropdown', clearable=False, style={"font-size": "20px", 'width': "300px"}),
                html.P(),
                html.Div(id='chosen-person', children='No person chosen yet'),
                html.Hr(),
                html.P('Select an image:'),
                dcc.Dropdown(id='image-dropdown', clearable=False, style={"font-size": "20px", 'width': "300px"}),
                html.P(),
                html.P('All the coordinates that are given, are relative to the size of the picture where (0,'
                       '0) resembles the top left corner and (1,1) the bottom right corner.'),
                dcc.Loading(id="load-image",
                            children=[html.Div(id='chosen-image', children=[html.P('No image chosen yet')])])
                ]

    return html.Div(children=children, style={"font-size": "20px"})


@app.callback(
    Output('person-dropdown', 'options'),
    Output('person-dropdown', 'value'),
    Input('model-dropdown', 'value'),
    Input('selected-person', 'children'))
def update_person_dropdown(model_filepath, selected_person):
    model_filepath = Path(model_filepath)

    person_ids = getPersonIdsFrom(model_filepath)

    person_options = []

    for person_id in person_ids:
        person_options.append({'label': f'Person {person_id}', 'value': person_id})

    if selected_person == "":
        selected_person = person_options[0]['value']

    return person_options, selected_person


@app.callback(
    Output('chosen-person', 'children'),
    Input('person-dropdown', 'value'))
def update_output(value):
    return 'You have chosen person {}'.format(value)


@app.callback(
    Output('image-dropdown', 'options'),
    Output('image-dropdown', 'value'),
    Input('model-dropdown', 'value'),
    Input('person-dropdown', 'value'))
def update_image_dropdown(model_filepath, person_id):
    model_filepath = Path(model_filepath)
    person = getPersonFrom(person_id, model_filepath)

    image_options = []

    for image in person.images:
        image_options.append({'label': image.__str__(), 'value': image.id})

    return image_options, image_options[0]['value']


@app.callback(
    Output('chosen-image', 'children'),
    Input('model-dropdown', 'value'),
    Input('person-dropdown', 'value'),
    Input('image-dropdown', 'value'),
    Input('confidence-threshold', 'value'))
def update_output(model_filepath, person_id, image_id, confidence_threshold):
    model_filepath = Path(model_filepath)
    text = html.P('You have chosen image {}'.format(image_id))

    person = getPersonFrom(person_id, model_filepath)
    image = person.getImage(image_id)

    predictions = []

    for prediction in image.predictions:
        if prediction.score >= confidence_threshold:
            predictions.append(prediction.toHTMLDash())

    if predictions == []:
        predictions.append(html.P('There are no predictions above the chosen confidence threshold.'))

    if model_filepath.match('*yolov5l_100epochs_16batchsize/inference/output*'):
        image_component = getGradcamImages(confidence_threshold, image, person)
    else:
        image_component = html.Img(src=image.getImageWithBoundingBoxesWithPredictionScoreAbove(confidence_threshold),
                                   title=image.getCaption(), width="98%")

    return [text, image_component, html.Div(children=predictions)]


def getGradcamImages(confidence_threshold, image, person):
    person_str = f"Person{person.id}"
    data_folder = Path("../2AMV10/data/raw/")
    image_path = data_folder / f"Person{person.id}/Person{person.id}_{image.id}.jpg"
    original_image = Image.open(image_path).convert('RGB')

    gradcam.run(original_image=original_image, obj=person.id, object_class=None, number=image.id,
                person=person_str)

    gradcam_img1 = Image.open(f"results/gradcam/{person_str}_{image.id}_Cam_On_Image.png")
    gradcam_img2 = Image.open(f"results/gradcam/{person_str}_{image.id}_Cam_Grayscale.png")
    gradcam_img3 = Image.open(f"results/gradcam/{person_str}_{image.id}_Cam_Heatmap.png")

    row_1 = html.Div(children=[
        html.Div(children=[
            html.Img(src=image.getImageWithBoundingBoxesWithPredictionScoreAbove(confidence_threshold),
                     title=image.getCaption()),
            html.P(image.getCaption())], style={'width': '48%', 'float': 'left'}),
        html.Div(children=[
            html.Img(src=gradcam_img1, title=f"Gradcam image of {person}, picture {image.id}"),
            html.P(f"Gradcam image of {person}, picture {image.id}")],
            style={'width': '48%', 'float': 'left'})
    ], style={'width': '100%'})
    row_2 = html.Div(children=[
        html.Div(children=[
            html.Img(src=gradcam_img2, title=f"Gradcam grayscale image of {person}, picture {image.id}"),
            html.P(f"Gradcam grayscale image of {person}, picture {image.id}")],
            style={'width': '48%', 'float': 'left'}),
        html.Div(children=[
            html.Img(src=gradcam_img3, title=f"Gradcam heatmap image of {person}, picture {image.id}"),
            html.P(f"Gradcam heatmap image of {person}, picture {image.id}")],
            style={'width': '48%', 'float': 'left'})
    ], style={'width': '100%'})

    return html.Div(children=[row_1, row_2])

