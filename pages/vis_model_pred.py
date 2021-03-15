import streamlit as st
from pathlib import Path
import classes.DataImage as DataImage
import classes.Person as Person
import classes.Object as Object
import os
import pytorch_cnn_visualizations.src.gradcam as gradcam
from PIL import Image


def write():
    train_test = st.sidebar.radio("Train images or person images", ['Train', 'Person'])
    # TODO: Make a button that loads the gradcam, so people know they have to wait perhaps
    if train_test == 'Train':
        trainimages_folder = Path("../2AMV10/data/raw/TrainingImages/")
        objects = sorted([f.name for f in os.scandir(trainimages_folder) if f.is_dir()])
        obj = st.selectbox("Select an object:", objects)
        object_class = objects.index(obj)
        object_number = st.selectbox("Choose object picture (1-12)", list(range(1, 13)))

        img_path = trainimages_folder / f"{obj}/{obj}_{object_number}.jpg"
        image = Image.open(img_path).convert('RGB')
        gradcam.run(image, obj, object_class)

        gradcam_img = Image.open(f"results/gradcam/{obj}_{object_class}_Cam_On_Image.png")
        st.image(gradcam_img, caption=f"Gradcam image of {obj}", use_column_width='auto')

    # TODO: Write it nicely for persons images
    else:
        # Hardcoded for YOLOv5l, as we will only be looking at this model
        model_path = Path("../2AMV10/trained_models/yolov5l_100epochs_16batchsize/inference/output/")
        persons = Person.getPersonsFrom(model_path)

        person = st.selectbox("Select a person:", persons)
        st.write("You selected:", person)
        image = st.selectbox("Select an image:", person.images)

        img_path = image.filepath
        image = Image.open(img_path).convert('RGB')
        gradcam_img = gradcam.run(image, person.id, None)
        st.image(gradcam_img, caption=f"Gradcam image of Person {person.id}", use_column_width='auto')

