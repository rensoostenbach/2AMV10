import pandas as pd
import streamlit as st
import random
from pathlib import Path
from functions import draw_bbox
import glob


def write():
    # Let user decide person number
    person_number = st.sidebar.selectbox("Choose person number (1-40)", list(range(1, 41)))

    # Choose amount of images that user has
    data_folder = Path("../2AMV10/data/raw/")
    jpg_counter = len(glob.glob1(data_folder / f"Person{person_number}", "*.jpg"))
    file_number = st.sidebar.selectbox("Choose image number", list(range(1, jpg_counter+1)))

    # Add in confidence slider.
    confidence_threshold = st.sidebar.slider(
        'Confidence threshold: What is the minimum acceptable confidence level for displaying a bounding box?', 0.0,
        1.0, 0.5, 0.01)
    st.sidebar.text(f"The current threshold value is {confidence_threshold}")

    st.write(
        f"We are looking at a picture of person number {person_number} with image number {file_number}."
    )

    img = data_folder / f"Person{person_number}/Person{person_number}_{file_number}.jpg"

    predictions = (
        data_folder / f"Person{person_number}/Person{person_number}_{file_number}.csv"
    )
    df = pd.read_csv(predictions)
    df = df[df['Score'] >= confidence_threshold]

    image, bbox_image = draw_bbox(img, df)
    st.image(image, caption="Random picture", use_column_width=True)
    st.image(
        bbox_image, caption="Random picture with bounding boxes", use_column_width=True
    )

    st.write(df)
