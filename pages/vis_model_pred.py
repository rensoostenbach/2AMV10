import streamlit as st
from pathlib import Path
import classes.DataImage as DataImage
import classes.Person as Person
import classes.Object as Object
import os
import pytorch_cnn_visualizations.src.gradcam as gradcam
from PIL import Image
import glob


def write():
    train_test = st.sidebar.radio("Train images or person images", ['Train', 'Person'])
    # TODO: Maybe make a button that loads the gradcam, so people know they have to wait a little bit
    # TODO: Get rid of the person images here, since they are also implemented somewhere else.
    # TODO: Show all images of a certain object on a single page.
    if train_test == 'Train':
        # Get train images and object class
        trainimages_folder = Path("../2AMV10/data/raw/TrainingImages/")
        objects = sorted([f.name for f in os.scandir(trainimages_folder) if f.is_dir()])
        obj = st.selectbox("Select an object:", objects)
        object_class = objects.index(obj)
        object_number = st.selectbox("Choose object picture (1-12)", list(range(1, 13)))

        # Run gradcam on chosen image
        img_path = trainimages_folder / f"{obj}/{obj}_{object_number}.jpg"
        image = Image.open(img_path).convert('RGB')
        gradcam.run(original_image=image, obj=obj, object_class=object_class, number=object_number)

        gradcam_img1 = Image.open(f"results/gradcam/{obj}_{object_number}_Cam_On_Image.png")
        gradcam_img2 = Image.open(f"results/gradcam/{obj}_{object_number}_Cam_Grayscale.png")
        gradcam_img3 = Image.open(f"results/gradcam/{obj}_{object_number}_Cam_Heatmap.png")

        col1, col2, col3 = st.beta_columns(3)
        with col1:
            st.image(gradcam_img1, caption=f"Gradcam image of {obj}", use_column_width='auto')
        with col2:
            st.image(gradcam_img2, caption=f"Gradcam grayscale image of {obj}", use_column_width='auto')
        with col3:
            st.image(gradcam_img3, caption=f"Gradcam heatmap image of {obj}", use_column_width='auto')

    else:
        data_folder = Path("../2AMV10/data/raw/")
        # Let user decide person number
        person_number = st.selectbox("Choose person number (1-40)", list(range(1, 41)))
        # Choose amount of images that user has
        jpg_counter = len(glob.glob1(data_folder / f"Person{person_number}", "*.jpg"))
        file_number = st.selectbox("Choose image number", list(range(1, jpg_counter + 1)))
        person = f"Person{person_number}"

        image_path = data_folder / f"Person{person_number}/Person{person_number}_{file_number}.jpg"
        image = Image.open(image_path).convert('RGB')
        gradcam.run(original_image=image, obj=person_number, object_class=None, number=file_number, person=person)

        gradcam_img1 = Image.open(f"results/gradcam/{person}_{file_number}_Cam_On_Image.png")
        gradcam_img2 = Image.open(f"results/gradcam/{person}_{file_number}_Cam_Grayscale.png")
        gradcam_img3 = Image.open(f"results/gradcam/{person}_{file_number}_Cam_Heatmap.png")

        col1, col2, col3 = st.beta_columns(3)
        with col1:
            st.image(gradcam_img1, caption=f"Gradcam image of {person}, picture {file_number}", use_column_width='auto')
        with col2:
            st.image(gradcam_img2, caption=f"Gradcam grayscale image of {person}", use_column_width='auto')
        with col3:
            st.image(gradcam_img3, caption=f"Gradcam heatmap image of {person}", use_column_width='auto')

