import streamlit as st
from datetime import date
import components.laadpalen
import components.ocm
import components.rdw
import components.landingpage

def sidebar():
    # Global variables to check on plots
    global showPlots
    global showCode


    st.sidebar.header('Dashboard setings')
    st.sidebar.write('Display settings:')

    # Checkboxes for showing plots/code
    showPlots = st.sidebar.checkbox('Show plots', True)
    showCode = st.sidebar.checkbox('Show code', False)

    start_h, end_h = (date(1970, 2, 1), date.today())

    pages = {
        "Alles": components.landingpage,
        "Laadpalen": components.laadpalen,
        "Open charge map": components.ocm,
        "RDW Data": components.rdw
    }
    st.sidebar.title("Navigatie")
    select = st.sidebar.selectbox(
        "Pagina",
        pages.keys()
    )
    st.sidebar.header("Selecteer een start en eind datum:")
    with st.sidebar.expander("Datum filter", False):
        test = date_test()
       # if (select == "RDW Data" or select == "Alles"):
       #     # Date selector

       #     start_h = st.sidebar.date_input('Start datum', start_h, key = "startd")
       #     end_h = st.sidebar.date_input('Eind datum', end_h, key = "endd")

            # Slider for date
       #     start_h, end_h = st.sidebar.slider("Selecteer een periode", start_h, end_h,
       #                                     (start_h, end_h), key="Globalslider")
    
    pages[select].main()

    st.sidebar.markdown('[README.md](https://github.com/GITNCLR/VA4/blob/main/README.md)')

def date_test():

    global start_h
    global end_h
    start_h, end_h = (date(1970, 2, 1), date.today())

    # Date selector
    start_h = st.date_input('Start datum', start_h, key = "startd")
    end_h = st.date_input('Eind datum', end_h, key = "endd")

    # Slider for date
    start_h, end_h = st.slider("Selecteer een periode", start_h, end_h,
                                            (start_h, end_h), key="Globalslider")

def main():
    sidebar()
