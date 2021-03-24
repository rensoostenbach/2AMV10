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
    ########
    # PAGE #
    ########
    objects = Object.getObjects()

    st.markdown("""
                # Objects
                """)

    object = st.selectbox("Select an object:", objects)

    st.write("You selected:", object)

    image = st.selectbox("Select an image:", object.images)

    st.image(image.get(),
             caption=image.getCaption(), use_column_width=True)