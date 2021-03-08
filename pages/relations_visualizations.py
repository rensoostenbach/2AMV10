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
    data_folder = Path("../2AMV10/data/raw/")

    persons = Person.getPersonsFrom(data_folder)

    st.markdown("""
                # People and their relation to objects
                """)

    person = st.selectbox("Select a person:", persons)

    st.write("You selected:", person)

    image = st.selectbox("Select an image:", person.images)

    st.image(Image.open(image.filepath), caption=image.getCaption(), use_column_width=True)

    for prediction in image.predictions:
        st.write(prediction.__str__())


