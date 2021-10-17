import streamlit as st
import components.laadpalen
import components.ocm
import components.rdw

def main():
    st.title("VA 4 dashboard")
    col1, col2 = st.columns([2, 1])
    with col2:
        st.image("assets/auto.png")
    with col1:
        st.markdown("*Welkom bij het Elektrisch Vervoer dashboard van team 1. U bevindt zich op de landingspagina waarin alle grafieken worden laten zien. Links staan er een aantal opties waar u van gebruik kunt maken, waaronder navigatie, filteren van de datum en het displayen van de code. Onderaan de sidebar is er ook een link naar een [README.md](https://github.com/ItsMeSafak/electric-energy-dashboard/blob/master/README.md) bestand. Hier staat de technische deel van de documentatie.*")
        st.header("Test")
        st.subheader("test")
        st.markdown("*Referenties: https://github.com/GITNCLR/VA4 *")
        st.markdown("*italic*")

    st.markdown("***")
    #components.laadpalen.main()
    #components.ocm.main()
    #components.rdw.main()