import streamlit as st
#import components.filename1
#import components.filename2


def main():

    col1, col2, col3 = st.columns([4, 1,1])
    with col1: st.title("VA 4 dashboard - Bomen in Den Haag en Amsterdam")
    with col2:
        st.image("assets/amsterdam.png", width=200)
    with col3:
        st.image("assets/denhaag.png", width=200)

    col1, col2 = st.columns([2, 1])
    with col2:
        st.image("assets/bomen.jpg")


    with col1:

        st.markdown("Welkom bij het informatieve dashboard van groep 1. Het dashboard geeft informatie over de bomen in Den Haag en Amsterdam weer. Er worden bijvoorbeeld bevindingen weergegeven over het aantal bomen per stad, de soorten en de leeftijd van de bomen. Ook zijn er bevindingen gedaan over een specifieke boomsoort, namelijk de eikenbomen in Amsterdam en Den Haag. Met de navigatie aan de linkerkant kan er een onderwerp worden gekozen. Ook kan aan de linkerkant van het dasboard een keuze gemaakt worden in het wel of niet laten zien van de code. De sample size heeft alleen betrekking op de kaarten. Deze kaarten zijn weergegeven in de pagina’s Bomen en Eikenbomen. Met de sample size wordt er ingesteld hoeveel bomen er op de kaarten worden weergegeven. Een hogere sample size zorgt voor een langere laadtijd.")
        st.markdown("***")
        st.markdown("*Bronnen:*")
        st.markdown("*Amsterdam Bomen 1: https://maps.amsterdam.nl/open_geodata/?k=254*")
        st.markdown("*Amsterdam Bomen 2: https://maps.amsterdam.nl/open_geodata/?k=255*")
        st.markdown("*Amsterdam Bomen 3: https://maps.amsterdam.nl/open_geodata/?k=256*")
        st.markdown("*Amsterdam Bomen 4: https://maps.amsterdam.nl/open_geodata/?k=257*")
        st.markdown("*Den Haag Bomen: https://ckan.dataplatform.nl/dataset/bomen-csv*")
    st.markdown("***")
    #components.filename1.main()
    #components.filename2.main()

