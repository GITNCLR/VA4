import streamlit as st
import components.laadpalen
import components.ocm
import components.rdw

def main():
    st.title("Elektrisch Vervoer dashboard")
    col1, col2 = st.columns([2, 1])
    with col2:
        st.image("assets/auto.png")
    with col1:
        st.markdown("*Welkom bij het Elektrisch Vervoer dashboard van team 1. U bevindt zich op de landingspagina waarin alle grafieken worden laten zien. Links staan er een aantal opties waar u van gebruik kunt maken, waaronder navigatie, filteren van de datum en het displayen van de code. Onderaan de sidebar is er ook een link naar een [README.md](https://github.com/ItsMeSafak/electric-energy-dashboard/blob/master/README.md) bestand. Hier staat de technische deel van de documentatie.*")
        st.header("Data gebruik")
        st.subheader("Laadpalen")
        st.markdown("*De laadpalen csv-bestand bestaat uit laadmomenten van een enkele laadpaal. Wat we eerst hebben gedaan is de data analyseren en controleren of alles klopt. We hebben gemerkt dat een paar rijen onjuiste gegevens bevatten, waarbij de einddatum eerder zou zijn dan de startdatum. Er waren ook enkele kolommen die een langere oplaadtijd hadden dan de aangesloten tijd. Deze rijen zijn eruit gefilterd.*")
        st.subheader("Open Charge Map")
        st.markdown("*Referenties: https://openchargemap.org/site/develop/api*")
        st.markdown("*Een andere dataset waar we gebruik van hebben gemaakt is de OCM API. Deze API laadt veel gegevens in over oplaadpunten voor voertuigen over de hele wereld. In ons geval hebben we op Nederland gericht.*")
        st.subheader("RDW Data")
        st.markdown("*Referenties: https://opendata.rdw.nl/Voertuigen/Open-Data-RDW-Gekentekende_voertuigen_brandstof/8ys7-d773, https://opendata.rdw.nl/Voertuigen/Open-Data-RDW-Gekentekende_voertuigen/m9d7-ebf2*")
        st.markdown("*De RDW-dataset is een set die bestaat uit geregistreerde autos in Nederland. De RDW heeft veel verschillende datasets met betrekking tot de autos in Nederland. We hebben gekozen voor degene die alle geregistreerde autos waarbij de datum vermeldt staat en een andere dataset die het brandstoftype van de auto laat zien. We hebben dit samengevoegd tot één dataframe en meer dan de helft van de kolommen verwijderd. We hebben ook gecontroleerd of er dubbele registraties in de dataset waren en dit bleek waar te zijn. We analyseerden deze records en kwamen tot de conclusie dat de records precies hetzelfde zijn.*")

        st.markdown("***")
    components.laadpalen.main()
    components.ocm.main()
    components.rdw.main()

