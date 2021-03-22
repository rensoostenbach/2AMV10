import copy
import pandas as pd
import numpy as np
import streamlit as st
import random
from PIL import Image
from pathlib import Path
import classes.DataImage as DataImage
import classes.Person as Person
import classes.Object as Object


def write():
    confidence_threshold = st.sidebar.slider(
        'Confidence threshold: What is the minimum acceptable confidence level for displaying a bounding box?', 0.085,
        1.0, 0.1, 0.01)
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

    persons = Person.getPersonsFrom(model_path)

    st.markdown("""
                # People and their relation to objects
                """)

    person = st.selectbox("Select a person:", persons)

    st.write("You selected:", person)

    image = st.selectbox("Select an image:", person.images)

    st.image(image.getImageWithBoundingBoxesWithPredictionScoreAbove(confidence_threshold),
             caption=image.getCaption(), use_column_width=True)

    for prediction in image.predictions:
        if prediction.score >= confidence_threshold:
            st.write(prediction.toHTML(), unsafe_allow_html=True)
