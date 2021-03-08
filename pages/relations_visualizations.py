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

    print(persons[0].images)

    st.markdown("""
            # People and their relation to objects
            """)



