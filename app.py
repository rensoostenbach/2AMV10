import pandas as pd
import numpy as np
import streamlit as st
import random
from PIL import Image

"""
# My first app
We will show some stuff about the data first:
"""

df = pd.DataFrame({"first column": [1, 2, 3, 4], "second column": [10, 20, 30, 40]})

st.write(df)

option = st.sidebar.selectbox("Which number do you like best?", df["first column"])

st.write("You selected:", option)

st.write("Let's show a random picture and the associated csv file with it.")
person_number = random.randint(1,40)
file_number = random.randint(1,5)

image = Image.open(f"data/Person{person_number}/Person{person_number}_{file_number}.jpg")
st.image(image, caption="Random picture", use_column_width=True)

csv = pd.read_csv(f"data/Person{person_number}/Person{person_number}_{file_number}.csv")
st.write(csv)
