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
import pytorch_cnn_visualizations.src.gradcam as gradcam


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

    if model == 'YOLO v5 E:100 B:16':
        person_str = f"Person{person.id}"
        data_folder = Path("../2AMV10/data/raw/")
        image_path = data_folder / f"Person{person.id}/Person{person.id}_{image.id}.jpg"
        original_image = Image.open(image_path).convert('RGB')
        gradcam.run(original_image=original_image, obj=person.id, object_class=None, number=image.id,
                    person=person_str)

        gradcam_img1 = Image.open(f"results/gradcam/{person_str}_{image.id}_Cam_On_Image.png")
        gradcam_img2 = Image.open(f"results/gradcam/{person_str}_{image.id}_Cam_Grayscale.png")
        gradcam_img3 = Image.open(f"results/gradcam/{person_str}_{image.id}_Cam_Heatmap.png")

        col1, col2 = st.beta_columns(2)
        with col1:
            st.image(image.getImageWithBoundingBoxesWithPredictionScoreAbove(confidence_threshold),
                     caption=image.getCaption(), width=416)
        with col2:
            st.image(gradcam_img1, caption=f"Gradcam image of {person}, picture {image.id}", use_column_width='auto')

        col1, col2 = st.beta_columns(2)
        with col1:
            st.image(gradcam_img2, caption=f"Gradcam grayscale image of {person}", use_column_width='auto')
        with col2:
            st.image(gradcam_img3, caption=f"Gradcam heatmap image of {person}", use_column_width='auto')
    else:
        st.image(image.getImageWithBoundingBoxesWithPredictionScoreAbove(confidence_threshold),
             caption=image.getCaption(), use_column_width=True)

    for prediction in image.predictions:
        if prediction.score >= confidence_threshold:
            st.write(prediction.toHTML(), unsafe_allow_html=True)
