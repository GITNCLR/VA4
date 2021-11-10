import streamlit as st
from utils.helpers import fetchLaadPaalData, show_with_options
import components.base as SampleS
import plotly.express as px
import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
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
amsterdam["leeftijd"] = amsterdam["leeftijd"].replace(2021,0)

df_denhaag=pd.read_csv('data/bomen_denhaag.csv',sep=";", encoding="latin-1")
naless_denhaag = df_denhaag.dropna(subset = ['BOOMSOORT_NEDERLANDS'])

eik_denhaag = naless_denhaag['BOOMSOORT_NEDERLANDS'].str.contains("eik")
df_eik_denhaag=naless_denhaag[eik_denhaag]['BOOMSOORT_NEDERLANDS'].value_counts()
df_eik_denhaag= pd.DataFrame(df_eik_denhaag)


eik_amsterdam= amsterdam['Soortnaam_NL'].str.contains("eik")
df_eik_amsterdam=amsterdam[eik_amsterdam]['Soortnaam_NL'].value_counts()
df_eik_amsterdam= pd.DataFrame(df_eik_amsterdam)
df_eik_denhaag["Soortnaam"] = df_eik_denhaag.index.str.title()
#print(df_denhaag['BOOMSOORT_NEDERLANDS'].isna().sum())
#df_denhaag['BOOMSOORT_NEDERLANDS'] = df_denhaag['BOOMSOORT_NEDERLANDS'].astype("str").str.title()

def eikenbomen_amsterdam():
    fig = px.histogram(df_eik_amsterdam, x=df_eik_amsterdam.index, y='Soortnaam_NL')

    fig.update_layout(
        title="Eikenbomen in Amsterdam",
        xaxis_title="Boomsoort",
        yaxis_title="Aantal")
    st.plotly_chart(fig, use_container_width=True)


def eikenbomen_denhaag():
    fig = px.histogram(df_eik_denhaag, x="Soortnaam", y='BOOMSOORT_NEDERLANDS')

    fig.update_layout(
        title="Eikenbomen in Den Haag",
        xaxis_title="Boomsoort",
        yaxis_title="Aantal")
    st.plotly_chart(fig, use_container_width=True)

def map_amsterdam():
    sample = SampleS.sample
    amsterdamm = amsterdam[amsterdam['Soortnaam_NL'].str.contains("eik")]

    if len(amsterdamm) < sample:
        sample = len(amsterdamm)

    amsterdamm = amsterdamm.sample(n = sample)
    m = folium.Map(location=["52.380858", "4.862874"])

    marker_cluster = MarkerCluster(name="key", disableClusteringAtZoom=18).add_to(m)

    amsterdamm.apply(lambda x: folium.Marker([x["LAT"], x["LNG"]],
                                             popup="Boomnummer: " + str(x["Boomnummer"]) + "<br><br>"
                                                    + "Soortnaam: " + x["Soortnaam_NL"] + "<br><br>"
                                                    + "Leeftijd: " + str(int(x["leeftijd"])) + " Jaar",
                                             icon=folium.Icon(color='green', icon_color='#FFFFFF')).add_to(
        marker_cluster),
                     axis=1)

    #folium.LayerControl().add_to(m)
    folium_static(m)

def map_denhaag():

    sample = SampleS.sample

    denhaag = df_denhaag.dropna(subset = ["BOOMNUMMER", 'BOOMSOORT_NEDERLANDS'])
    denhaag = denhaag[denhaag['BOOMSOORT_NEDERLANDS'].str.contains("eik")]
    if len(denhaag) < sample:
        sample = len(denhaag)

    denhaag = denhaag.sample(n = sample)

    denhaag["BOOMNUMMER"] = denhaag["BOOMNUMMER"].astype("int").astype("str")

    m = folium.Map(location=["52.074947", "4.304368"])

    marker_cluster = MarkerCluster(name="key", disableClusteringAtZoom=16).add_to(m)

    denhaag.apply(lambda x: folium.Marker([x["LAT"], x["LONG"]],
                                          popup="Boomnummer: " + str(x["BOOMNUMMER"]) + "<br><br>"
                                                + "Soortnaam: " + str(x["BOOMSOORT_NEDERLANDS"]) + "<br><br>"
                                                + "Leeftijd: " + str(int(x["LEEFTIJD"])) + " Jaar",
                                          icon=folium.Icon(color='green', icon_color='#FFFFFF')).add_to(marker_cluster),
                  axis=1)

    #folium.LayerControl().add_to(m)
    folium_static(m)

def aantal_eiken():

    denhaag = df_denhaag.dropna(subset=["BOOMNUMMER", 'BOOMSOORT_NEDERLANDS'])
    denhaag = denhaag[denhaag['BOOMSOORT_NEDERLANDS'].str.contains("eik")]
    n_eik_d = len(denhaag)
    n_eik_a = len(amsterdam[amsterdam['Soortnaam_NL'].str.contains("eik")])

    dict2 = {"Count": [n_eik_a, n_eik_d]}
    brics2 = pd.DataFrame(dict2)
    brics2.index = ['Amsterdam', 'Den Haag']
    fig = px.bar(brics2, x=['Amsterdam', 'Den Haag'], y='Count', color=['Amsterdam', 'Den Haag'])
    fig.update_layout(
        title="Aantal Eikenbomen in Amsterdam en Den Haag",
        xaxis_title="Stad",
        yaxis_title="Aantal soorten bomen",
        legend_title="Stad")
    st.plotly_chart(fig, use_container_width=True)


def main():
    st.header("Eikenbomen")
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.image("assets/rups.jpg")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        st.image("assets/amsterdam.png", width=200)
    with col3:
        st.image("assets/denhaag.png", width=200)
    col1, _, col3 = st.columns([3, 1, 3])

    with col1:
        show_with_options(eikenbomen_amsterdam, "In dit figuur kunt u zelf de x-en y as van een scatterplot bepalen door middel van de dropdown menu’s.")
    with col3:
        show_with_options(eikenbomen_denhaag, "In dit figuur kunt u zelf de x-en y as van een scatterplot bepalen door middel van de dropdown menu’s.")
    with col1:
        show_with_options(map_amsterdam,
                          "In dit figuur kunt u zelf de x-en y as van een scatterplot bepalen door middel van de dropdown menu’s.")
    with col3:
        show_with_options(map_denhaag,
                          "In dit figuur kunt u zelf de x-en y as van een scatterplot bepalen door middel van de dropdown menu’s.")
    st.markdown("***")
    show_with_options(aantal_eiken,
                  "In dit figuur kunt u zelf de x-en y as van een scatterplot bepalen door middel van de dropdown menu’s.")






