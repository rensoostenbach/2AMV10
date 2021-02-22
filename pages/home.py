import pandas as pd
import numpy as np
import streamlit as st
import random
from PIL import Image
from pathlib import Path

def write():
    df = pd.DataFrame({"first column": [1, 2, 3, 4], "second column": [10, 20, 30, 40]})

    st.write(df)

    option = st.sidebar.selectbox("Which number do you like best?", df["first column"])

    st.write("You selected:", option)

    st.write("Let's show a random picture and the associated csv file with it.")
    person_number = random.randint(1,40)
    file_number = random.randint(1,5)

    data_folder = Path("../2AMV10/data/raw/")
    img = data_folder / f"Person{person_number}/Person{person_number}_{file_number}.jpg"

    image = Image.open(img)
    st.image(image, caption="Random picture", use_column_width=True)

    predictions = data_folder / f"Person{person_number}/Person{person_number}_{file_number}.csv"
    csv = pd.read_csv(predictions)
    st.write(csv)