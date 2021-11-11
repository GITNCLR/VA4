import streamlit as st
from utils.helpers import show_with_options
import components.base as SampleS
import plotly.express as px
import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static

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
df_denhaag['BOOMSOORT_NEDERLANDS'] = df_denhaag['BOOMSOORT_NEDERLANDS'].str.title()
naless_denhaag = df_denhaag.dropna(subset = ['BOOMSOORT_NEDERLANDS', 'EIGENAAR'])


def boomsoorten_amsterdam():
    fig = px.histogram(amsterdam, x='Soortnaam_NL')
    fig.update_layout(
        #title="Aantal bomen per boomsoort in Amsterdam",
        xaxis_title="Boomsoort",
        yaxis_title="Aantal bomen")
    st.plotly_chart(fig, use_container_width=True)


def boomsoorten_denhaag():
    fig = px.histogram(naless_denhaag, x='BOOMSOORT_NEDERLANDS')
    fig.update_layout(
        #title="Aantal bomen per boomsoort in Den Haag",
        xaxis_title="Boomsoort",
        yaxis_title="Aantal bomen")
    st.plotly_chart(fig, use_container_width=True)


def boomsoorten_t5_a():
    top5_amsterdam = amsterdam['Soortnaam_NL'].value_counts(ascending=False)[0:5]
    #st.write(top5_amsterdam)
    top5_amsterdam2 = pd.DataFrame(top5_amsterdam)
    fig = px.histogram(top5_amsterdam2, x=top5_amsterdam2.index, y='Soortnaam_NL', color=top5_amsterdam2.index, color_discrete_sequence=["green", "yellow", "orange", 'red', "lightblue"])

    fig.update_layout(
        #title="Top 5 boomsoorten in Amsterdam",
        xaxis_title="Boomsoort",
        yaxis_title="Aantal bomen")

    st.plotly_chart(fig, use_container_width=True)

def boomsoorten_t5_d():
    top5_denhaag = naless_denhaag['BOOMSOORT_NEDERLANDS'].value_counts(ascending=False)[0:5]
    #st.write(top5_denhaag)
    top5_denhaag2 = pd.DataFrame(top5_denhaag)
    fig = px.histogram(top5_denhaag2, x=top5_denhaag2.index, y='BOOMSOORT_NEDERLANDS', color=top5_denhaag2.index, color_discrete_sequence=["lightblue", "red", "pink",'Yellow','Orange'])
    fig.update_layout(
        #title="Top 5 boomsoorten in Den Haag",
        xaxis_title="Boomsoort",
        yaxis_title="Aantal bomen")
    st.plotly_chart(fig, use_container_width=True)

def aantal_bomen():
    dict = {"Count": [259431, 162203]}

    brics = pd.DataFrame(dict)
    brics.index = ['Amsterdam', 'Den Haag']
    fig = px.bar(brics, x=['Amsterdam', 'Den Haag'], y='Count', color=['Amsterdam', 'Den Haag'])
    fig.update_layout(
        #title="Aantal bomen in Amsterdam en Den Haag",
        xaxis_title="Stad",
        yaxis_title="Aantal bomen",
        legend_title="Stad")
    st.plotly_chart(fig, use_container_width=True)

def aantal_soorten_bomen():
    dict2 = {"Count": [625, 377]}

    brics2 = pd.DataFrame(dict2)
    brics2.index = ['Amsterdam', 'Den Haag']
    fig = px.bar(brics2, x=['Amsterdam', 'Den Haag'], y='Count', color=['Amsterdam', 'Den Haag'])
    fig.update_layout(
        #title="Aantal soorten bomen in Amsterdam en Den Haag",
        xaxis_title="Stad",
        yaxis_title="Aantal soorten bomen",
        legend_title="Stad")
    st.plotly_chart(fig, use_container_width=True)

def map_amsterdam():
    amsterdamm = amsterdam.sample(n = SampleS.sample)
    m = folium.Map(location=["52.380858", "4.862874"])

    marker_cluster = MarkerCluster(name="key", disableClusteringAtZoom=18).add_to(m)

    amsterdamm.apply(lambda x: folium.Marker([x["LAT"], x["LNG"]],
                                            popup="Boomnummer: " + str(x["Boomnummer"]) + "<br><br>"
                                                + "Soortnaam: " + x["Soortnaam_NL"] + "<br><br>"
                                                + "Leeftijd: " + str(int(x["leeftijd"])) + " Jaar",
                                            icon=folium.Icon(color='green', icon_color='#FFFFFF')).add_to(marker_cluster),
                     axis=1)

    #folium.LayerControl().add_to(m)
    #st.write("Map van de bomen in Amsterdam")
    folium_static(m)

def map_denhaag():
    denhaag = df_denhaag.dropna(subset = ["BOOMNUMMER"]).sample(n = SampleS.sample)
    denhaag["BOOMNUMMER"] = denhaag["BOOMNUMMER"].astype("int").astype("str")

    m = folium.Map(location=["52.074947", "4.304368"])

    marker_cluster = MarkerCluster(name="key", disableClusteringAtZoom=16).add_to(m)

    denhaag.apply(lambda x: folium.Marker([x["LAT"], x["LONG"]],
                                          popup="Boomnummer: " + str(x["BOOMNUMMER"]) + "<br><br>"
                                                + "Soortnaam: " + str(x["BOOMSOORT_NEDERLANDS"]) + "<br><br>"
                                                + "Leeftijd: " + str(x["LEEFTIJD"]).split(".")[0] + " Jaar",
                                          icon=folium.Icon(color='green', icon_color='#FFFFFF')).add_to(marker_cluster),
                  axis=1)

    #folium.LayerControl().add_to(m)
    #st.write("Map van de bomen in Den Haag")
    folium_static(m)

def eigenaren_amsterdam():
    fig = px.histogram(amsterdam, x='Eigenaar', color='Eigenaar')
    fig.update_layout(
        #title="Het aantal bomen per eigenaar in Amsterdam",
        xaxis_title="Eigenaar",
        yaxis_title="Aantal bomen")
    st.plotly_chart(fig, use_container_width=True)

def eigenaren_denhaag():
    fig = px.histogram(naless_denhaag, x='EIGENAAR', color='EIGENAAR')
    fig.update_layout(
        #title="Het aantal bomen per eigenaar in Den Haag",
        legend = { "title" : "Eigenaar"},
        xaxis_title="Eigenaar",
        yaxis_title="Aantal bomen")
    st.plotly_chart(fig, use_container_width=True)




def main():
    st.header("Bomen Algemeen")
    st.markdown("***")
    col1, _, col3 = st.columns([3, 1, 3])

    with col1:
        st.image("assets/amsterdam.png", width=200)
        show_with_options(boomsoorten_amsterdam, "Aantal bomen per boomsoort in Amsterdam")
    with col3:
        st.image("assets/denhaag.png", width=200)
        show_with_options(boomsoorten_denhaag, "Aantal bomen per boomsoort in Den Haag")


    col1,col2, col3 = st.columns([1, 8, 1])
    with col2:
        st.markdown("In de bovenstaande figuren zijn het aantal bomen per boomsoort in Amsterdam en Den Haag te zien. Links zijn de boomsoorten van Amsterdam te zien en rechts de boomsoorten van Den Haag. Vanwege de grote hoeveelheid boomsoorten worden niet alle boomsoorten in tekst weergegeven. Voor een duidelijker beeld kan er ingezoomd worden.")
        st.markdown("***")

    col1, _, col3 = st.columns([3, 1, 3])
    with col1:
        show_with_options(boomsoorten_t5_a, "Top 5 Boomsoorten in Amsterdam")

    with col3:
        show_with_options(boomsoorten_t5_d, "Top 5 Boomsoorten in Den Haag")

    col1,col2, col3 = st.columns([1, 8, 1])
    with col2:
        st.markdown("In de bovenstaande figuren is ingezoomd op de top vijf meest voorkomende boomsoorten in Amsterdam en Den Haag. In het linker figuur is te zien dat de meest voorkomende boomsoort in Amsterdam de gewone plataan is. In het rechter figuur is te zien dat de meest voorkomende boomsoort in Den Haag de es is.")
        st.markdown("***")
    col1, _, col3 = st.columns([3, 1, 3])

    col1,col2, col3 = st.columns([1, 8, 1])
    with col2:
        show_with_options(aantal_soorten_bomen,"Aantal verschillende soorten bomen in Amsterdam en Den Haag")
        st.markdown("In het bovenstaande figuur zijn het aantal soorten bomen in Amsterdam en Den Haag te zien. Uit dit figuur blijkt dat Amsterdam meer soorten bomen heeft dan Den Haag. Amsterdam heeft namelijk 625 verschillende boomsoorten en Den Haag 377.")
        st.markdown("***")
        show_with_options(aantal_bomen,"Aantal bomen in Amsterdam en Denhaag")
        st.markdown("In het bovenstaande figuur zijn het aantal bomen in Amsterdam en Den Haag te zien. Uit dit figuur blijkt dat Amsterdam meer bomen heeft dan Den Haag.")
        st.markdown("***")

    col1, _, col3 = st.columns([3, 1, 3])
    with col1:
        show_with_options(map_amsterdam, "Map van de bomen in Amsterdam")
    with col3:
        show_with_options(map_denhaag,"Map van de bomen in Den Haag")

    col1,col2, col3 = st.columns([1, 8, 1])
    with col2:
        st.markdown("In de linker kaart zijn de bomen in Amsterdam te zien en in de rechterkaart de bomen in Den Haag. Als er een specifieke boom wordt geselecteerd staat er informatie over de leeftijd van de boom, het boomnummer en de soortnaam.")
        st.markdown("***")
    col1, _, col3 = st.columns([3, 1, 3])

    with col1:
        show_with_options(eigenaren_amsterdam, "Het aantal bomen per eigenaar in Amsterdam")
    with col3:
        show_with_options(eigenaren_denhaag, "Het aantal bomen per eigenaar in Den Haag")

    col1,col2, col3 = st.columns([1, 8, 1])
    with col2:
        st.markdown("In de bovenstaande figuren zijn het aantal bomen per eigenaar in Amsterdam en Den Haag te zien. Uit het linker figuur blijkt dat er in Amsterdam 7 verschillende eigenaren van bomen bestaan. De gemeente Amsterdam bezit de meeste bomen. In het rechter figuur zijn de verschillende eigenaren van de bomen in Den Haag te zien. Ook uit dit figuur blijkt dat de gemeente Den Haag de meeste bomen bezit.")
        st.markdown("***")
    col1, _, col3 = st.columns([3, 1, 3])

st.markdown("***")






