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
naless_denhaag = df_denhaag.dropna(subset = ['BOOMSOORT_NEDERLANDS', 'EIGENAAR'])



def eigenaren_amsterdam():
    fig = px.histogram(amsterdam, x='Eigenaar', color='Eigenaar')
    fig.update_layout(
        title="Eigenaren van de bomen in Amsterdam",
        xaxis_title="Eigenaar",
        yaxis_title="Aantal")
    st.plotly_chart(fig, use_container_width=True)


def eigenaren_denhaag():
    fig = px.histogram(naless_denhaag, x='EIGENAAR', color='EIGENAAR')
    fig.update_layout(
        title="Eigenaren van de bomen in Den Haag",
        xaxis_title="Eigenaar",
        yaxis_title="Aantal")
    st.plotly_chart(fig, use_container_width=True)



def main():
    st.header("Eigenaren")
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
        st.image("assets/amsterdam.png", width=200)

    with col3:
        st.image("assets/denhaag.png", width=200)

    with col1:
        show_with_options(eigenaren_amsterdam, "In dit figuur kunt u zelf de x-en y as van een scatterplot bepalen door middel van de dropdown menu’s.")
    with col3:
        show_with_options(eigenaren_denhaag, "In dit figuur kunt u zelf de x-en y as van een scatterplot bepalen door middel van de dropdown menu’s.")

st.markdown("***")




