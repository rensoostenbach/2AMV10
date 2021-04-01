import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

import pytorch_cnn_visualizations.src.gradcam as gradcam
from app import app
from classes.DataImage import *
from classes.Person import *
from classes.Object import *
from classes.Prediction import LABELS


def getContent():
    children = [html.H1("Objects", style={"font-size": "40px"}),
                html.P('This page will show the training pictures of the objects, to get an idea of what the objects '
                       'look like. By choosing precomputed images, you will see all twelve pictures per selected '
                       'object. By choosing the Grad-CAM option, the tool will compute the Grad-CAMs on the run, '
                       'and you can select two images from an object to compare to each other.'),
                html.Hr(),
                html.P('Select an object:'),
                dcc.Dropdown(id='object-dropdown', clearable=False, style={"font-size": "20px", 'width': "300px"}),
                html.P(),
                html.Div(id='image-dropdown', children=[
                    dcc.Dropdown(id='image-1-dropdown', clearable=False, style={"font-size": "20px", 'width': "300px"}),
                    dcc.Dropdown(id='image-2-dropdown', clearable=False,
                                 style={"font-size": "20px", 'width': "300px"})],
                         hidden=True),
                html.Div(id='chosen-object', children='No object chosen yet'),
                dcc.Loading(id="load-object-images",
                            children=[html.Div(id='chosen-object-image', children=[html.P('No image shown yet')])])
                ]

    return html.Div(children=children, style={"font-size": "20px"})


@app.callback(
    Output('object-dropdown', 'options'),
    Output('object-dropdown', 'value'),
    Input('gradcam-computation', 'value'),
    Input('selected-object', 'children'))
def update_object_dropdown(gradcam_comp, selected_object):
    data_folder = Path("../2AMV10/data/raw/TrainingImages/")
    objects = getObjectNamesFrom(data_folder)

    object_options = []

    for object_name in objects:
        object_options.append({'label': f'{object_name}', 'value': object_name})

    if selected_object == "":
        selected_object = object_options[0]['value']

    return object_options, selected_object


@app.callback(
    Output('image-1-dropdown', 'options'),
    Output('image-2-dropdown', 'options'),
    Output('image-1-dropdown', 'value'),
    Output('image-2-dropdown', 'value'),
    Output('image-dropdown', 'hidden'),
    Input('gradcam-computation', 'value'),
    Input('gradcam-group', 'hidden'))
def update_images_dropdown(must_compute, is_hidden):
    if is_hidden:
        raise PreventUpdate

    if must_compute:
        image_options = []
        for i in range(1, 13):
            image_options.append({'label': f'Image {i}', 'value': i})

        return image_options, image_options, image_options[0]['value'], image_options[1]['value'], False
    else:
        return [], [], None, None, True


@app.callback(
    Output('chosen-object', 'children'),
    Input('object-dropdown', 'value'))
def update_object_output(value):
    return 'You have chosen: {}'.format(value)


@app.callback(
    Output('chosen-object-image', 'children'),
    Input('gradcam-computation', 'value'),
    Input('object-dropdown', 'value'),
    Input('image-1-dropdown', 'value'),
    Input('image-2-dropdown', 'value'))
def update_output(must_compute, object_name, image_1, image_2):
    if image_1 == None and image_2 == None and must_compute:
        raise PreventUpdate

    data_folder = Path("../2AMV10/data/raw/TrainingImages/")

    rows = []
    obj = getObjectWithName(object_name)
    object_class = int(list(LABELS.keys())[list(LABELS.values()).index(obj.__str__())])
    if must_compute:
        # Run gradcam on selected two images
        for i in [image_1, image_2]:
            img_path = data_folder / f"{obj}/{obj}_{i}.jpg"
            image = Image.open(img_path).convert('RGB')
            gradcam.run(original_image=image.resize((208, 208)), obj=obj, object_class=object_class, number=i)

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
                    row.append(html.Img(src=image, title=f"Gradcam {type} image of {obj}", width='7.5%',
                                        style={'margin': '2px'}))

            rows.append(html.Div(children=copy.deepcopy(row)))

    return rows
