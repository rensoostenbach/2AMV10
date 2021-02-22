import pandas as pd
import streamlit as st
import random
from pathlib import Path
from functions import draw_bbox


def write():
    df = pd.DataFrame({"first column": [1, 2, 3, 4], "second column": [10, 20, 30, 40]})

    st.write(df)

    option = st.sidebar.selectbox("Which number do you like best?", df["first column"])

    st.write("You selected:", option)

    st.write("Let's show a random picture and the associated csv file with it.")
    person_number = random.randint(1, 40)
    file_number = random.randint(1, 5)
    st.write(
        f"We are looking at a picture of person nummber {person_number} with image number {file_number}."
    )

    data_folder = Path("../2AMV10/data/raw/")
    img = data_folder / f"Person{person_number}/Person{person_number}_{file_number}.jpg"

    predictions = (
        data_folder / f"Person{person_number}/Person{person_number}_{file_number}.csv"
    )
    csv = pd.read_csv(predictions)

    image, bbox_image = draw_bbox(img, csv)
    st.image(image, caption="Random picture", use_column_width=True)
    st.image(
        bbox_image, caption="Random picture with bounding boxes", use_column_width=True
    )

    st.write(csv)
