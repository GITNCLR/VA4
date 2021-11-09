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


def boomsoorten_amsterdam():
    fig = px.histogram(amsterdam, x='Soortnaam_NL')
    fig.update_layout(
        title="Boomsoorten in Amsterdam",
        xaxis_title="Boomsoort",
        yaxis_title="Aantal")
    st.plotly_chart(fig, use_container_width=True)


def boomsoorten_denhaag():
    fig = px.histogram(naless_denhaag, x='BOOMSOORT_NEDERLANDS')
    fig.update_layout(
        title="Boomsoorten in Den Haag",
        xaxis_title="Boomsoort",
        yaxis_title="Aantal")
    st.plotly_chart(fig, use_container_width=True)


def boomsoorten_t5_a():
    top5_amsterdam = amsterdam['Soortnaam_NL'].value_counts(ascending=False)[0:5]
    st.write(top5_amsterdam)
    top5_amsterdam2 = pd.DataFrame(top5_amsterdam)
    fig = px.histogram(top5_amsterdam2, x=top5_amsterdam2.index, y='Soortnaam_NL', color=top5_amsterdam2.index)

    fig.update_layout(
        title="Top 5 boomsoorten in Amsterdam",
        xaxis_title="Boomsoort",
        yaxis_title="Aantal")
    st.plotly_chart(fig, use_container_width=True)

def boomsoorten_t5_d():
    top5_denhaag = naless_denhaag['BOOMSOORT_NEDERLANDS'].value_counts(ascending=False)[0:5]
    st.write(top5_denhaag)
    top5_denhaag2 = pd.DataFrame(top5_denhaag)
    fig = px.histogram(top5_denhaag2, x=top5_denhaag2.index, y='BOOMSOORT_NEDERLANDS', color=top5_denhaag2.index)
    fig.update_layout(
        title="Top 5 boomsoorten in Den Haag",
        xaxis_title="Boomsoort",
        yaxis_title="Aantal")
    st.plotly_chart(fig, use_container_width=True)

def aantal_bomen():
    dict = {"Count": [259431, 162203]}

    brics = pd.DataFrame(dict)
    brics.index = ['Amsterdam', 'Den Haag']
    fig = px.bar(brics, x=['Amsterdam', 'Den Haag'], y='Count', color=['Amsterdam', 'Den Haag'])
    fig.update_layout(
        title="Aantal bomen in Amsterdam en Den Haag",
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
        title="Aantal soorten bomen in Amsterdam en Den Haag",
        xaxis_title="Stad",
        yaxis_title="Aantal soorten bomen",
        legend_title="Stad")
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
        st.image("assets/amsterdam.png", width=200)
        show_with_options(boomsoorten_amsterdam, "In dit figuur kunt u zelf de x-en y as van een scatterplot bepalen door middel van de dropdown menu’s.")
    with col3:
        st.image("assets/denhaag.png", width=200)
        show_with_options(boomsoorten_denhaag, "In dit figuur kunt u zelf de x-en y as van een scatterplot bepalen door middel van de dropdown menu’s.")
    st.markdown("***")
    with col1:
        show_with_options(boomsoorten_t5_a, "In dit figuur kunt u zelf de x-en y as van een scatterplot bepalen door middel van de dropdown menu’s.")

    with col3:
        show_with_options(boomsoorten_t5_d, "In dit figuur kunt u zelf de x-en y as van een scatterplot bepalen door middel van de dropdown menu’s.")

    show_with_options(aantal_bomen,
                      "In dit figuur kunt u zelf de x-en y as van een scatterplot bepalen door middel van de dropdown menu’s.")
    show_with_options(aantal_soorten_bomen,
                      "In dit figuur kunt u zelf de x-en y as van een scatterplot bepalen door middel van de dropdown menu’s.")
st.markdown("***")





