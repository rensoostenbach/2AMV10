import streamlit as st
import awesome_streamlit as ast


import pages.vis_model_pred

st.set_page_config(layout="wide")

PAGES = {
    "Understanding the model": pages.vis_model_pred,
    "People": pages.relations_visualizations,
}

def main():
    """Main function of the App"""
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))

    page = PAGES[selection]

    with st.spinner(f"Loading {selection} ..."):
        ast.shared.components.write_page(page)


if __name__ == "__main__":
    main()