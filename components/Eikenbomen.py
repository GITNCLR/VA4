import streamlit as st
from utils.helpers import fetchLaadPaalData, show_with_options
import plotly.express as px
import streamlit as st
import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objects as go
from statsmodels.formula.api import ols

file = "data/BOMEN1.csv"
file1 = "data/BOMEN2.csv"
file2 = "data/BOMEN3.csv"
file3 = "data/BOMEN4.csv"

with open(file):
    amsterdam = pd.read_csv(file, sep=";")

with open(file1):
    amsterdam = pd.concat([amsterdam, pd.read_csv(file1, sep=";")])

with open(file2):
    amsterdam = pd.concat([amsterdam, pd.read_csv(file2, sep=";")])

with open(file3):
    amsterdam = pd.concat([amsterdam, pd.read_csv(file3, sep=";")])

amsterdam = amsterdam.assign(leeftijd=lambda x: 2021 - x['Plantjaar'])

df_denhaag=pd.read_csv('data/bomen_denhaag.csv',sep=";", encoding="latin-1")
naless_denhaag = df_denhaag.dropna(subset = ['BOOMSOORT_NEDERLANDS'])

eik_denhaag = naless_denhaag['BOOMSOORT_NEDERLANDS'].str.contains("eik")
df_eik_denhaag=naless_denhaag[eik_denhaag]['BOOMSOORT_NEDERLANDS'].value_counts()
df_eik_denhaag= pd.DataFrame(df_eik_denhaag)


eik_amsterdam= amsterdam['Soortnaam_NL'].str.contains("eik")
df_eik_amsterdam=amsterdam[eik_amsterdam]['Soortnaam_NL'].value_counts()
df_eik_amsterdam= pd.DataFrame(df_eik_amsterdam)


def eikenbomen_amsterdam():
    fig = px.histogram(df_eik_amsterdam, x=df_eik_amsterdam.index, y='Soortnaam_NL')

    fig.update_layout(
        title="Eikenbomen in Amsterdam",
        xaxis_title="Boomsoort",
        yaxis_title="Aantal")
    st.plotly_chart(fig, use_container_width=True)


def eikenbomen_denhaag():
    fig = px.histogram(df_eik_denhaag, x=df_eik_denhaag.index, y='BOOMSOORT_NEDERLANDS')

    fig.update_layout(
        title="Eikenbomen in Den Haag",
        xaxis_title="Boomsoort",
        yaxis_title="Aantal")
    st.plotly_chart(fig, use_container_width=True)



def main():
    st.header("Bomen")
    col1, _, col3 = st.columns([3, 1, 3])
    #with col3:
        #global x_col
        #global y_col
        #x_col = st.selectbox(
        #    "X Waarde",
        #    main_df.columns)
        #y_col = st.selectbox(
        #    "Y Waarde",
        #    main_df.columns,
        #    index=2)
    with col1:
        show_with_options(eikenbomen_amsterdam, "In dit figuur kunt u zelf de x-en y as van een scatterplot bepalen door middel van de dropdown menu’s.")
    with col3:
        show_with_options(eikenbomen_denhaag, "In dit figuur kunt u zelf de x-en y as van een scatterplot bepalen door middel van de dropdown menu’s.")

    #with col1:
    #    show_with_options(boomsoorten_t5_a, "In dit figuur kunt u zelf de x-en y as van een scatterplot bepalen door middel van de dropdown menu’s.")

    #with col3:
    #    show_with_options(boomsoorten_t5_d, "In dit figuur kunt u zelf de x-en y as van een scatterplot bepalen door middel van de dropdown menu’s.")

    #show_with_options(histogram_chargetime, "In het figuur van de dichtheid functie is te zien dat de meeste waarden liggen tussen de 30 minuten en 5 uur. Dit wordt ondersteunt door het gemiddelde van 2,8 uur en de mediaan van 2,5 uur.")
    #with st.expander("Boxplot", False):
    #    show_with_options(boxplot_chargetime, "In deze boxplot is de spreiding van de chargetime in uren te zien. Voorafgaand aan het maken van de boxplot zijn alle negatieve waarden verwijderd, aangezien chargetime niet negatief kan zijn. Wat er opvalt aan deze boxplot is dat er een aantal outliers zitten in de dataset. De grootste uitschieter, met een waarde van 52 is verwijderd bij het maken van het figuur van de dichtheidsfunctie.")

    #show_with_options(histogram_maxpower, "")
    #show_with_options(histogram_maxpower_nout, "In de eerste histogram is net zoals in de boxplot te zien dat er een enorme spreiding is. Om een beter beeld te krijgen is er een tweede histogram gemaakt, ingezoomd op de data die binnen de boxplot valt . Hieruit is een nieuw gemiddelde berekent van 3415 en een mediaan van 3392. Dit komt omdat de meeste data die weg gefilterd is hoge waarden bevatten.  Uit het figuur blijkt dat de meeste waarden tussen de 3200 en 3600 wat liggen.")
    #with st.expander("Boxplot", False):
    #    show_with_options(boxplot_maxpower, "In deze boxplot is te zien dat er een grote spreiding is van het maximaal gevraagde vermogen. De data is gegeven in Jules per seconde (W). Omdat weten dat de data afkomstig is van een soort laadpaal is een logische verklaring dat dit komt door de verschillende soorten auto met bijbehorende (snel)laders die op de markt zijn. Het gemiddelde van de data is 4035 en de mediaan is 3396.")

    #show_with_options(histogram_totalenergy, "")
    #show_with_options(histogram_totalenergy_nout, "Deze figuren geeft de totaal verbruikte energie per laadsessie weer. Deze boxplot laat zien dat de data wederom een grote spreiding bevat, met veel hoge uitschieters. Net als bij het vorige figuur van het maximaal gevraagde vermogen is er voor dit figuur een extra histogram toegevoegd om te kijken naar de data die binnen de histogram valt.  Een verklaring voor de grote spreiding is dat de totaal verbruikte energie sterk wordt beïnvloed door de maximaal gevraagde vermogen en door de charge time per sessie. Het gemiddelde van de totaal verbruikte energie per sessie is 10407 Wh. De mediaan is 7713 Wh.")
    #with st.expander("Boxplot", False):
    #    show_with_options(boxplot_totalenergy, "")
    #show_with_options(regression, "In het volgende figuur is een scatterplot met daarin een lineaire regressie te zien. Op de y-as van de scatterplot is de totaal verbruikte energie per laadsessie te zien. Op de x-as  is de chargetime per sessie te zien. Door middel van een lineaire regressie is er op basis van de chargetime  voorspeld wat de de totaal verbruikte energie zal worden. De voorspellende data is af te lezen met behulp van de lijn die door het figuur loopt. De voorspelling is gemaakt op basis van de data van de meerderheid groep die valt tussen een gevraagd vermogen tussen 3000 W en 3800 W. Een mogelijke verklaring voor het afwijken van de voorspelling voor hoge charge time waardes kan te maken hebben met de oplaad curve van batterijen.")
    st.markdown("***")

