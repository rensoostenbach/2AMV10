import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
import streamlit_bd_cytoscapejs


def write():
    check = st.checkbox('Click here to choose a different graph')

    if check:
        elements = [
            {'data': {'id': 'a'}},
            {'data': {'id': 'b'}},
            {'data': {
                'id': 'ab',
                'source': 'a',
                'target': 'b'
            }}
        ]
        layout = {}
        style = [
        {
          'selector': 'node',
          'style': {
            'background-color': 'red'
          }
        }, {
            'selector': 'edge',
            'style': {
                'background-color': 'yellow'
            }
        }
        ]
    else:
        elements = [
            {'data': {'id': 'c'}},
            {'data': {'id': 'd'}},
            {'data': {
                'id': 'cd',
                'source': 'c',
                'target': 'd'
            }}
        ]
        layout = {'name': 'random'}
        style = [
        {
          'selector': 'node',
          'style': {
              'background-image': "https://raw.githubusercontent.com/rensoostenbach/2AMV10/main/trained_models/faster_rcnn/inference/output/Person10_1.jpg",
              'background-width': '100%',
              'background-height': '100%'
          }
        }]

    node_id = streamlit_bd_cytoscapejs.st_bd_cytoscape(
        elements,
        layout=layout,
        key='foo',
        stylesheet=style
    )



    st.write(node_id)
