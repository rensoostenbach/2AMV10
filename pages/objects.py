import copy
import pandas as pd
import numpy as np
import streamlit as st
import random
import os
from PIL import Image
from pathlib import Path
import classes.DataImage as DataImage
import classes.Person as Person
import classes.Object as Object
import pytorch_cnn_visualizations.src.gradcam as gradcam


def write():
    ###########
    # SIDEBAR #
    ###########
    run_gradcam = st.sidebar.radio('Run Grad-CAM (longer computation time) or use precomputed images',
                                   ['Grad-CAM', 'Precomputed images'], 1)
    ########
    # PAGE #
    ########
    objects = Object.getObjects()

    st.markdown("""
                # Objects
                """)

    obj = st.selectbox("Select an object:", objects)

    st.write("You selected:", obj)

    if run_gradcam == 'Grad-CAM':
        # Get train images and object class
        trainimages_folder = Path("../2AMV10/data/raw/TrainingImages/")
        object_class = objects.index(obj)

        # Run gradcam on all object images
        for i in range(1, 13):
            img_path = trainimages_folder / f"{obj}/{obj}_{i}.jpg"
            image = Image.open(img_path).convert('RGB')
            gradcam.run(original_image=image, obj=obj, object_class=object_class, number=i)

            gradcam_img1 = Image.open(f"results/gradcam/{obj}_{i}_Cam_On_Image.png")
            gradcam_img2 = Image.open(f"results/gradcam/{obj}_{i}_Cam_Grayscale.png")
            gradcam_img3 = Image.open(f"results/gradcam/{obj}_{i}_Cam_Heatmap.png")

            col1, col2, col3, col4 = st.beta_columns(4)
            with col1:
                st.image(image.resize((416, 416)), caption=f"Image {i} of {obj}", use_column_width='auto')
            with col2:
                st.image(gradcam_img1, caption=f"Gradcam image of {obj}", use_column_width='auto')
            with col3:
                st.image(gradcam_img2, caption=f"Gradcam grayscale image of {obj}", use_column_width='auto')
            with col4:
                st.image(gradcam_img3, caption=f"Gradcam heatmap image of {obj}", use_column_width='auto')

    else:
        # Get train images
        trainimages_folder = Path("../2AMV10/data/raw/TrainingImages/")

        image_types = ['train', 'On_Image', 'Grayscale', 'Heatmap']

        for idx, type in enumerate(image_types):
            cols = st.beta_columns(12)
            for i in range(1, 13):
                if type == 'train':
                    img_path = trainimages_folder / f"{obj}/{obj}_{i}.jpg"
                    image = Image.open(img_path).convert('RGB').resize((104, 104))
                    cols[i-1].image(image,
                                    # caption=f"Image {i} of {obj}"
                                    )
                else:  # Grad-CAM images
                    image = Image.open(f"results/gradcam/{obj}_{i}_Cam_{type}.png")
                    cols[i-1].image(image,
                                    # caption=f"Gradcam {type} image of {obj}",
                                    width=104)
