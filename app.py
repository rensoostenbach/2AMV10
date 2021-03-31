import streamlit as st
import awesome_streamlit as ast
import pages.relations_visualizations
import pages.people
import pages.objects
import pages.test

st.set_page_config(layout="wide")

PAGES = {
    "People": pages.people,
    "Objects": pages.objects,
    "People and predicted objects": pages.relations_visualizations,
    "Test": pages.test
}


def main():
    """Main function of the App"""
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(PAGES.keys()), 3)

    page = PAGES[selection]

    with st.spinner(f"Loading {selection} ..."):
        ast.shared.components.write_page(page)


if __name__ == "__main__":
    main()
