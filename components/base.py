import streamlit as st
from datetime import date
import components.Bomen
import components.landingpage
import components.Eikenbomen
import components.Eigenaren
def sidebar():
    # Global variables to check on plots
    global showPlots
    global showCode

    st.sidebar.header('Dashboard setings')
    st.sidebar.write('Display settings:')

    # Checkboxes for showing plots/code
    showPlots = st.sidebar.checkbox('Show plots', True)
    showCode = st.sidebar.checkbox('Show code', False)

    pages = {
        "Home": components.landingpage,
        "Bomen": components.Bomen,
        "Eikenbomen": components.Eikenbomen,
        "Eigenaren": components.Eigenaren
    }

    st.sidebar.title("Navigatie")
    select = st.sidebar.selectbox(
        "Pagina",
        pages.keys()
    )

    st.sidebar.header("Selecteer een start en eind datum:")
    with st.sidebar.expander("Datum filter", False):
        date_selector()
    
    pages[select].main()

    st.sidebar.markdown('[README.md](https://github.com/GITNCLR/VA4/blob/main/README.md)')

def date_selector():

    global start_h
    global end_h
    start_h, end_h = (date(2000, 1, 1), date.today())

    col1, col2, col3 = st.columns([1, 9, 1])
    with col2:
    # Date selector
        start_h = st.date_input('Start datum', start_h, key = "startd")
        end_h = st.date_input('Eind datum', end_h, key = "endd")

    # Slider for date
        start_h, end_h = st.slider("Selecteer een periode", start_h, end_h,
                                            (start_h, end_h), key="Globalslider")

def main():
    sidebar()


