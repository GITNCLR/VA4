import streamlit as st
from utils.helpers import fetchLaadPaalData, show_with_options
import components.base as SampleS
import plotly.express as px
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sn

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
amsterdam = amsterdam.drop(columns=['Unnamed: 17'])


df_denhaag=pd.read_csv('data/bomen_denhaag.csv',sep=";", encoding="latin-1")
naless_denhaag = df_denhaag.dropna(subset = ['BOOMSOORT_NEDERLANDS'])

amsterdam = amsterdam[amsterdam['leeftijd']<250]
df_denhaag = df_denhaag[df_denhaag['LEEFTIJD']<300]

def leeftijd():
    fig = go.Figure()

    fig.add_trace(go.Box(x=amsterdam['leeftijd'],
                         name='Amsterdam',
                         marker_color='indianred'))

    fig.add_trace(go.Box(x=df_denhaag['LEEFTIJD'],
                         name='Den Haag',
                         marker_color='lightseagreen'))

    fig.update_layout(title_text="Leeftijd van bomen in Den Haag en Amsterdam", xaxis_title='Leeftijd in jaren')

    st.plotly_chart(fig, use_container_width=True)

def leeftijd_hist():
    fig = go.Figure()

    fig.add_trace(go.Histogram(x=amsterdam['leeftijd'],
                               name='Amsterdam',
                               marker_color='indianred'))

    fig.add_trace(go.Histogram(x=df_denhaag['LEEFTIJD'],
                               name='Den Haag',
                               marker_color='lightseagreen'))

    fig.update_layout(barmode='overlay',
                      title_text='Histogram van de leeftijd van bomen in Amsterdam en Den Haag',
                      xaxis_title='Leeftijd in jaren',
                      yaxis_title='Aantal bomen')

    fig.update_traces(opacity=0.75)

    st.plotly_chart(fig, use_container_width=True)


def boomhoogte_leeftijd_amsterdam():
    fig = px.box(amsterdam, x='Boomhoogte', y='leeftijd',
                 category_orders={'Boomhoogte': ['tot 6 m.', '6 tot 9 m.', '6 tot 12 m.', '9 tot 12 m.', '12 tot 15 m.',
                                                 '12 tot 18 m.', '15 tot 18 m.', '18 tot 24 m.', '24 m. en hoger',
                                                 'Onbekend']})
    st.plotly_chart(fig, use_container_width=True)

def radius_leeftijd_amsterdam():
    fig = px.box(amsterdam, x='RADIUS', y='leeftijd')
    st.plotly_chart(fig, use_container_width=True)

def stamdia_leeftijd_denhaag():
    fig = px.box(df_denhaag, x='STAMDIAMETERKLASSE', y='LEEFTIJD',
                 category_orders={
                     'STAMDIAMETERKLASSE': ['0-10 cm', '10-25 cm', '25-50 cm', '50-75 cm', '75-100 cm', '>100 cm']})

    st.plotly_chart(fig, use_container_width=True)

def stadsdeel_leeftijd_denhaag():
    fig = px.box(df_denhaag, x='STADSDEEL', y='LEEFTIJD')
    st.plotly_chart(fig, use_container_width=True)

def stadsdeel_leeftijd_amsterdam():
    fig = px.box(amsterdam, x='Beheerder', y='leeftijd')
    st.plotly_chart(fig, use_container_width=True)

def boomstam_leeftijd_corr_dh():
    df_denhaag['STAMDIAMETERKLASSE2'] = df_denhaag['STAMDIAMETERKLASSE'].astype("str").apply(
        lambda x: "100" if x[-5:-3] == "00" else ("0" if x[-5:-3] == "" else x[-5:-3]))
    df_denhaag['STAMDIAMETERKLASSE2'] = df_denhaag['STAMDIAMETERKLASSE2'].astype("int")
    df_denhaag['STAMDIAMETERKLASSE2']

    df = pd.DataFrame(df_denhaag, columns=['STAMDIAMETERKLASSE2', 'LEEFTIJD'])

    #corr_mat_dh = df.corr()
    #fig = sn.heatmap(corr_mat_dh, annot=True)
    #st.pyplot(fig, use_container_width=True)

    fig, ax = plt.subplots()
    sn.heatmap(df.corr(), ax=ax,annot=True)
    st.write(fig)

def main():
    st.header("Leeftijd")

    st.markdown("***")
    show_with_options(leeftijd,
                      "In dit figuur kunt u zelf de x-en y as van een scatterplot bepalen door middel van de dropdown menu’s.")
    show_with_options(leeftijd_hist,
                      "In dit figuur kunt u zelf de x-en y as van een scatterplot bepalen door middel van de dropdown menu’s.")
    st.markdown("***")

    col1, _, col3 = st.columns([3, 1, 3])

    with col1:
        st.image("assets/amsterdam.png", width=200)
        show_with_options(boomhoogte_leeftijd_amsterdam,
                          "In dit figuur kunt u zelf de x-en y as van een scatterplot bepalen door middel van de dropdown menu’s.")
        show_with_options(stadsdeel_leeftijd_amsterdam,
                          "In dit figuur kunt u zelf de x-en y as van een scatterplot bepalen door middel van de dropdown menu’s.")
        show_with_options(radius_leeftijd_amsterdam,
                          "In dit figuur kunt u zelf de x-en y as van een scatterplot bepalen door middel van de dropdown menu’s.")
    with col3:
        st.image("assets/denhaag.png", width=200)
        show_with_options(stamdia_leeftijd_denhaag,
                          "In dit figuur kunt u zelf de x-en y as van een scatterplot bepalen door middel van de dropdown menu’s.")
        show_with_options(stadsdeel_leeftijd_denhaag,
                          "In dit figuur kunt u zelf de x-en y as van een scatterplot bepalen door middel van de dropdown menu’s.")
        show_with_options(boomstam_leeftijd_corr_dh,
                          "In dit figuur kunt u zelf de x-en y as van een scatterplot bepalen door middel van de dropdown menu’s.")







