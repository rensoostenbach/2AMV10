import pandas as pd
import streamlit as st
from pathlib import Path

from bokeh.models import StaticLayoutProvider

import classes.Person as Person
import classes.Object as Object
import classes.CytoscapeBipartiteGraph as BipartiteGraph
import networkx as nx
from bokeh.io import output_file, show
from bokeh.plotting import figure, from_networkx


def write():
    ###########
    # SIDEBAR #
    ###########
    confidence_threshold = st.sidebar.slider(
        'Confidence threshold: What is the minimum acceptable confidence level for displaying a prediction?', 0.085,
        1.0, 0.1, 0.01)
    k = st.sidebar.slider(
        'How many clusters (node colors) do you want to predict?', 1, 40, 5, 1
    )
    st.sidebar.text(f"The current threshold value is {confidence_threshold}")

    models = pd.DataFrame({'Models': ['Given model', 'Efficient DET', 'RCNN', 'YOLO v4 E:100 B:16',
                                      'YOLO v4 E:100 B:32', 'YOLO v4 E:150 B:16', 'YOLO v5 E:100 B:16'],
                           'Paths': [Path("../2AMV10/data/raw/"),
                                     Path("../2AMV10/trained_models/efficientdet_d0_tensorflow_v2/inference/output/"),
                                     Path("../2AMV10/trained_models/faster_rcnn/inference/output/"),
                                     Path("../2AMV10/trained_models/scaled_yolov4_100epochs_16batchsize/inference/output/"),
                                     Path("../2AMV10/trained_models/scaled_yolov4_100epochs_32batchsize/inference/output/"),
                                     Path("../2AMV10/trained_models/scaled_yolov4_150epochs_16batchsize/inference/output/"),
                                     Path("../2AMV10/trained_models/yolov5l_100epochs_16batchsize/inference/output/")]})

    model = st.sidebar.selectbox('Choose your model: ', models['Models'])
    model_path = models.loc[models['Models'] == model, 'Paths'].iloc[0]

    ########
    # PAGE #
    ########
    st.markdown("""
                # People and their relation to objects
                """)

    persons = Person.getPersonsFrom(model_path)
    objects = Object.getObjects()

    relation_graph = BipartiteGraph.BipartiteGraph(persons, objects, confidence_threshold, k)
    # plot = figure(x_range=(0, 8), y_range=(0, 25))
    # graph = from_networkx(relation_graph.graph, nx.spring_layout)
    # fixed_layout_provider = StaticLayoutProvider(graph_layout=relation_graph.getNodeLayout())
    # graph.layout_provider = fixed_layout_provider
    # plot.renderers.append(graph)
    st.plotly_chart(relation_graph)

    # person = st.selectbox("Select a person:", persons)
    #
    # st.write("You selected:", person)
    #
    # image = st.selectbox("Select an image:", person.images)
    #
    # st.image(image.getImageWithBoundingBoxesWithPredictionScoreAbove(confidence_threshold),
    #          caption=image.getCaption(), use_column_width=True)
    #
    # for prediction in image.predictions:
    #     if prediction.score >= confidence_threshold:
    #         st.write(prediction.toHTML(), unsafe_allow_html=True)
