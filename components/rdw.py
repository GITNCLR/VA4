import components.base as gSlider
import pandas as pd
import streamlit as st
from utils.helpers import fetchLaadPaalData, show_with_options
import plotly.express as px

merk_list = ["All", "Volkswagen", "Opel", "Peugeot", "Renault", "Ford", "Toyota", "Mercedes-Benz", "Citroen", "Tesla"]
MERK_list = [(each_string.upper()+".csv") for each_string in merk_list]
line_dict = dict.fromkeys(merk_list)

for i, file in enumerate(MERK_list):
    with open("data/csv/line/"+file) as csv:
        line_dict[merk_list[i]] = pd.read_csv(csv, index_col="Datum tenaamstelling", parse_dates=["Datum tenaamstelling"])



fuel_list = ["Elektriciteit", "Benzine", "Diesel", "LPG", "CNG", "LNG", "Alcohol","Waterstof"]
fuel_file_list = [(each_string +".csv") for each_string in fuel_list]
scatter_dict = dict.fromkeys(fuel_list)

for i, file in enumerate(fuel_file_list):
    with open("data/csv/scatter/"+file) as csv:
        scatter_dict[fuel_list[i]] = pd.read_csv(csv, index_col="Datum tenaamstelling", parse_dates=["Datum tenaamstelling"])



def line():
    df_merk = line_dict[selectedMerk]
    start, end = gSlider.start_h, gSlider.end_h

    fuel_color_map = {'Benzine' : "brown", 'Diesel': "black", 'LPG' : "orange", 'Elektriciteit': "blue", 'CNG': "yellow", 'Alcohol' : "red",
           'Waterstof' : "aqua", 'LNG' : "green"}

    fig = px.line(df_merk[start:end], y="Kenteken",
                  color="Brandstof omschrijving",
                  color_discrete_map = fuel_color_map)

    fig.update_layout(yaxis_title="Aantal Autos cumulatief", xaxis_title = "Datum",
                      title={'text': 'Cumulatief nieuwe registraties per brandstoftype', 'x': 0.5})

    st.plotly_chart(fig, use_container_width=True)

def scatter():
    df_fuel = scatter_dict[selectedFuel]
    start, end = gSlider.start_h, gSlider.end_h

    fig = px.scatter(df_fuel[start:end], y="Brandstof omschrijving", trendline="rolling",
                     trendline_options=dict(window=30),
                     trendline_color_override="red", labels = {"Brandstof omschrijving": selectedFuel })

    fig.update_layout(title={'text': 'Nieuwe registraties per dag per brandstof: '+ selectedFuel, 'x': 0.5},
                      xaxis_title='Datum',
                      yaxis_title='Aantal nieuwe registraties',
                      coloraxis_colorbar=dict(title="Totaal verbruikte energie <br> in Wh"))

    st.plotly_chart(fig, use_container_width=True)


def main():
    st.header("RDW Data")
    col1, _, col3 = st.columns([6, 1, 3])
    col4, _, col6 = st.columns([6, 1, 3])

    with col3:
        global selectedMerk

        selectedMerk = st.selectbox(
            "Merk", merk_list)

    with col1:
        show_with_options(line, "In dit figuur zijn de cumulatieve nieuwe registraties per brandstoftype te zien. Met de slider is de periode te selecteren. Met de dropdown zijn de top 8 populairste automerken (RDW data) te selecteren. Ook is Tesla toegevoegd, vanwege de toenemende populariteit. Deze toenemende populariteit is dan ook te zien in het figuur. Verder is in het figuur te zien dat benzine de meest voorkomende brandstof is, gevolgd door diesel. Ook is opvallend dat er vanaf 2010 bij de meeste merken er een toename is te zien.")

    with col6:
        global selectedFuel

        selectedFuel = st.selectbox(
            "Brandstof", fuel_list)

    with col4:
        show_with_options(scatter, "In dit figuur is een scatterplot te zien van het aantal nieuwe registraties per brandstoftype per dag. Met de dropdown is de brandstofsoort te selecteren. Ook bij dit figuur is de periode te selecteren door middel van de slider. Opvallend is dat vrijwel alle brandstofsoorten in frequentie toenemen naarmate de jaren toenemen. Ook is bij elektriciteit in de maand van december 2019 en 2020 een piek te zien. Een mogelijke verklaring kan het naderen van het einde van het fiscale jaar zijn.")

    st.write("*De volledige RDW database is verkregen door de csv's te downloaden van de site en deze lokaal samen te voegen op overeenkomende nummerborden. Vervolgens is de dataset gecontroleerd op duplicaten en zijn enkel de laatste waardes behouden, ook hebben wij er voor gekozen om enkel de Peronenauto's en de Bedrijfauto's te behouden. Er is ook gechecked op NaN waardes, deze zijn verwijderd. Op basis van deze dataset zijn er berekeningen gemaakt. De resultaten zijn geexporteerd als csv's om de figuren mee te maken. De reden hiervoor is simpelweg het bestandsgrote limiet van Streamlit en Git aangezien de samengevoegde csv meer dan 10 miljoen rijen bevatten en 600mb groot was na pogingen om deze te verkleinen. Deze stap was noodzakelijk om een accuraat beeld te schetsen met de figuren.")

    st.markdown("*Brandstof dataset: https://opendata.rdw.nl/Voertuigen/Open-Data-RDW-Gekentekende_voertuigen_brandstof/8ys7-d773 *")
    st.markdown("*Kenteken dataset: https://opendata.rdw.nl/Voertuigen/Open-Data-RDW-Gekentekende_voertuigen/m9d7-ebf2*")
    st.markdown("*Samengevoegde csv vóór berekeningen - 1915 tm heden(Download): https://drive.google.com/file/d/1aSRnZ5GQeGwCGPO-RbroyRBf9JqXhvAL/view?usp=sharing*")
