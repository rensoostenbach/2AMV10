import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pytorch_cnn_visualizations.src.gradcam as gradcam
from app import app
from classes.DataImage import *
from classes.Person import *
from classes.Object import *
from classes.Prediction import LABELS


def getContent():
    children = [html.H1("Objects", style={"font-size": "40px"}),
                html.P('Select an object:'),
                dcc.Dropdown(id='object-dropdown', clearable=False, style={"font-size": "20px", 'width': "300px"}),
                html.P(),
                html.Div(id='chosen-object', children='No object chosen yet'),
                dcc.Loading(id="load-object-images",
                            children=[html.Div(id='chosen-object-image', children=[html.P('No image shown yet')])])
                ]

    return html.Div(children=children, style={"font-size": "20px"})


@app.callback(
    Output('object-dropdown', 'options'),
    Output('object-dropdown', 'value'),
    Input('gradcam-computation', 'value'))
def update_object_dropdown(gradcam_comp):
    data_folder = Path("../2AMV10/data/raw/TrainingImages/")
    objects = getObjectNamesFrom(data_folder)

    object_options = []

    for object_name in objects:
        object_options.append({'label': f'{object_name}', 'value': object_name})

    return object_options, object_options[0]['value']


@app.callback(
    Output('chosen-object', 'children'),
    Input('object-dropdown', 'value'))
def update_object_output(value):
    return 'You have chosen: {}'.format(value)


@app.callback(
    Output('chosen-object-image', 'children'),
    Input('gradcam-computation', 'value'),
    Input('object-dropdown', 'value'))
def update_output(must_compute, object_name):
    data_folder = Path("../2AMV10/data/raw/TrainingImages/")

    rows = []
    obj = getObjectWithName(object_name)
    object_class = int(list(LABELS.keys())[list(LABELS.values()).index(obj.__str__())])
    if must_compute:
        # Run gradcam on all object images
        for i in range(1, 13):
            img_path = data_folder / f"{obj}/{obj}_{i}.jpg"
            image = Image.open(img_path).convert('RGB')
            gradcam.run(original_image=image.resize((208,208)), obj=obj, object_class=object_class, number=i)

            gradcam_img1 = Image.open(f"results/gradcam/{obj}_{i}_Cam_On_Image.png")
            gradcam_img2 = Image.open(f"results/gradcam/{obj}_{i}_Cam_Grayscale.png")
            gradcam_img3 = Image.open(f"results/gradcam/{obj}_{i}_Cam_Heatmap.png")

            rows.append(html.Div(children=[
                html.Div(children=[
                    html.Img(src=image.resize((416, 416)), title=f"Image {i} of {obj}", width='98%'),
                    html.P(f"Image {i} of {obj}")],
                    style={'width': '24%', 'float': 'left'}),
                html.Div(children=[
                    html.Img(src=gradcam_img1, title=f"Gradcam image of {obj}", width='98%'),
                    html.P(f"Gradcam image of {obj}")],
                    style={'width': '24%', 'float': 'left'}),
                html.Div(children=[
                    html.Img(src=gradcam_img2, title=f"Gradcam grayscale image of {obj}", width='98%'),
                    html.P(f"Gradcam grayscale image of {obj}")],
                    style={'width': '24%', 'float': 'left'}),
                html.Div(children=[
                    html.Img(src=gradcam_img3, title=f"Gradcam heatmap image of {obj}", width='98%'),
                    html.P(f"Gradcam heatmap image of {obj}")],
                    style={'width': '24%', 'float': 'left'})
            ], style={'width': '100%', 'margin-bottom': '10px', 'font-size': '16px'}))
    else:
        image_types = ['train', 'On_Image', 'Grayscale', 'Heatmap']

        for idx, type in enumerate(image_types):
            row = []
            for i in range(0, 12):
                if type == 'train':
                    img_path = data_folder / f"{obj}/{obj}_{i + 1}.jpg"
                    image = Image.open(img_path).convert('RGB').resize((104, 104))
                    row.append(html.Img(src=image, title=f"Image {i} of {obj}", width='7.5%', style={'margin': '2px'}))
                else:  # Grad-CAM images
                    image = Image.open(f"results/gradcam/{obj}_{i + 1}_Cam_{type}.png")
                    row.append(html.Img(src=image, title=f"Gradcam {type} image of {obj}", width='7.5%', style={'margin': '2px'}))

            rows.append(html.Div(children=copy.deepcopy(row)))

    return rows
