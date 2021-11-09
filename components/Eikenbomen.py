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
    st.header("Eikenbomen")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("assets/rups.jpg")
    col1, _, col3 = st.columns([3, 1, 3])

    with col1:
        show_with_options(eikenbomen_amsterdam, "In dit figuur kunt u zelf de x-en y as van een scatterplot bepalen door middel van de dropdown menu’s.")
    with col3:
        show_with_options(eikenbomen_denhaag, "In dit figuur kunt u zelf de x-en y as van een scatterplot bepalen door middel van de dropdown menu’s.")
st.markdown("***")




