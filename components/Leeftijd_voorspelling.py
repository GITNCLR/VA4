import streamlit as st
from utils.helpers import show_with_options
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
amsterdam["leeftijd"] = amsterdam["leeftijd"].replace(2021,0)
amsterdam = amsterdam.drop(columns=['Unnamed: 17'])


df_denhaag=pd.read_csv('data/bomen_denhaag.csv',sep=";", encoding="latin-1")
naless_denhaag = df_denhaag.dropna(subset = ['BOOMSOORT_NEDERLANDS'])

amsterdam = amsterdam[amsterdam['leeftijd']<250]
df_denhaag = df_denhaag[df_denhaag['LEEFTIJD']<300]








def radius_leeftijd_amsterdam_ols():
    global amsterdam
    amsterdam = amsterdam.sort_values("Soortnaam_NL")
    fig = px.scatter(amsterdam, y='RADIUS', x='leeftijd', trendline="ols", opacity= 0.5, trendline_color_override = "red")
    fig.update_layout(

        legend_title_text= 'Soortnaam',
        yaxis_title="Radiusklasse in (m)",
        xaxis_title="Leeftijd in jaren")

    fig2 = px.scatter(amsterdam, y='RADIUS', x='leeftijd', color = "Soortnaam_NL", trendline="ols", opacity= 0.5)#, trendline_color_override = "red")
    fig2.update_layout(
        title="Voorspelling van Radiusklasse op basis van Leeftijd per Soort in Amsterdam",
        legend_title_text= 'Soortnaam',
        yaxis_title="Radiusklasse in (m)",
        xaxis_title="Leeftijd in jaren")

    st.plotly_chart(fig, use_container_width=True)
    with st.expander("Voorspelling per soort Amsterdam", False):
        st.plotly_chart(fig2, use_container_width=True)
        st.write("Dubbelklik op een boomsoort in de legenda om de andere boomsoorten te verbergen.")



def boomstam_leeftijd_corr_dh():
    global df_denhaag
    df_denhaag['STAMDIAMETERKLASSE2'] = df_denhaag['STAMDIAMETERKLASSE'].astype("str").apply(
        lambda x: "100" if x[-5:-3] == "00" else ("0" if x[-5:-3] == "" else x[-5:-3]))
    df_denhaag['STAMDIAMETERKLASSE2'] = df_denhaag['STAMDIAMETERKLASSE2'].astype("int")
    df_denhaag['Soortnaam'] = df_denhaag['BOOMSOORT_NEDERLANDS'].str.title()
    df_denhaag = df_denhaag.sort_values("Soortnaam")

    df = pd.DataFrame(df_denhaag, columns=['STAMDIAMETERKLASSE2', 'LEEFTIJD'])

    fig, ax = plt.subplots()
    sn.heatmap(df.corr(), ax=ax,annot=True)
    st.write(fig)
    st.write("In het bovenstaande figuur is de correlatie van de stamdiameter en de leeftijd van de bomen in Den Haag weergegeven. Uit dit figuur blijkt een positieve correlatie tussen de stamdiameter en de leeftijd van de bomen.")
    st.markdown("***")
    #fig, ax = plt.subplots()
    #sn.regplot(x="STAMDIAMETERKLASSE2", y="LEEFTIJD", data=df_denhaag, ci=None, scatter_kws={'alpha': 0.5}, ax=ax)
    #st.write(fig)
    st.subheader("Voorspelling van Stamdiameterklasse op basis van leeftijd voor Den Haag")
    fig = px.scatter(df_denhaag, y='STAMDIAMETERKLASSE2', x='LEEFTIJD', color = 'Soortnaam', trendline="ols", opacity= 0.5)#, trendline_color_override = "red")
    fig.update_layout(
        title="Voorspelling van Stamdiameterklasse op basis van Leeftijd per Soort in Den Haag",
        yaxis_title="Stamdiameterklasse in (cm)",
        xaxis_title="Leeftijd in jaren")

    fig2 = px.scatter(df_denhaag, y='STAMDIAMETERKLASSE2', x='LEEFTIJD', trendline="ols", opacity= 0.5, trendline_color_override = "red")
    fig2.update_layout(
        #title="Stamdiameterklasse per Leeftijd Denhaag",
        yaxis_title="Stamdiameterklasse in (cm)",
        xaxis_title="Leeftijd in jaren")

    st.plotly_chart(fig2, use_container_width=True)
    with st.expander("Voorspelling per soort Den Haag", False):
        st.plotly_chart(fig, use_container_width=True)
        st.write("Dubbelklik op een boomsoort in de legenda om de andere boomsoorten te verbergen.")

def boomstam_leeftijd_corr_A():

    df = pd.DataFrame(amsterdam, columns=['Boomnummer','Plantjaar', 'RADIUS', 'leeftijd'])

    #corr_mat_dh = df.corr()
    #fig = sn.heatmap(corr_mat_dh, annot=True)
    #st.pyplot(fig, use_container_width=True)

    fig, ax = plt.subplots()
    sn.heatmap(df.corr(), ax=ax,annot=True)
    st.write(fig)

    #fig, ax = plt.subplots()
    #sn.regplot(x="RADIUS", y="leeftijd", data=amsterdam, ci=None, scatter_kws={'alpha': 0.5}, ax=ax)
    #st.write(fig)

def boomnummer_leeftijd_amsterdam():
    fig = px.scatter(amsterdam, y='Boomnummer', x='leeftijd', opacity= 0.5, trendline="ols", trendline_color_override = "red")
    fig.update_layout(
    #title = "Leeftijd per Boomnummer Amsterdam",
    yaxis_title = "Boomnummer",
    xaxis_title = "Leeftijd in jaren")
    st.plotly_chart(fig, use_container_width=True)

def boomnummer_leeftijd_denhaag():
    fig = px.scatter(df_denhaag, y='BOOMNUMMER', x='LEEFTIJD', opacity= 0.5, trendline="ols", trendline_color_override = "red")
    fig.update_layout(
    #title = "Leeftijd per Boomnummer Den Haag",
    yaxis_title = "Boomnummer",
    xaxis_title = "Leeftijd in jaren")
    st.plotly_chart(fig, use_container_width=True)

def main():
    st.header("Leeftijd")

    st.markdown("***")

    col1, _, col3 = st.columns([3, 1, 3])

    with col1:
        st.image("assets/amsterdam.png", width=200)

    with col3:
        st.image("assets/denhaag.png", width=200)





    with col1:
        show_with_options(boomstam_leeftijd_corr_A, "Correlaties van de variabelen van bomen in Amsterdam")
        st.write("In het bovenstaande figuur zijn de correlaties van verschillende variabelen met betrekking tot de bomen in Amsterdam weergegeven. Uit dit figuur blijkt dat er een positieve correlatie is tussen leeftijd en de radius van de bomen. Ook blijkt er een positieve correlatie tussen de leeftijd en het plantjaar van de bomen te zijn.")
        st.markdown("***")

        show_with_options(radius_leeftijd_amsterdam_ols, "Voorspelling van Radiusklasse op basis van leeftijd voor Amsterdam")
        st.write("In het bovenstaande figuur is een regressieanalyse te zien van de radius klasse per leeftijd. Uit dit figuur blijkt dat wanneer de leeftijd van de bomen hoger is de radius ook hoger is. De voorspelling is het meest betrouwbaar voor de bomen onder de 100 jaar, omdat de dataset voornamelijk bomen onder de 100 jaar bevat. Ook kan de voorspelling minder nauwkeurig zijn, omdat bomen niet altijd even snel blijven groeien.")
        st.markdown("***")

        show_with_options(boomnummer_leeftijd_amsterdam, "Leeftijd per Boomnummer Amsterdam")
        st.write("In het bovenstaande figuur is een regressieanalyse te zien van de leeftijd van de bomen per boomnummer in Amsterdam. Uit dit figuur blijkt over het algemeen dat hoe ouder de bomen zijn hoe lager het boomnummer is.")

    with col3:
        show_with_options(boomstam_leeftijd_corr_dh, "Correlatie van de stamdiameter en leeftijd van de bomen in Den Haag")
        st.write("In dit figuur is een regressieanalyse te zien van de stamdiameterklasse per leeftijd van de bomen in Den Haag. In dit figuur is een stijgende lijn te zien. Dit betekent dat wanneer de leeftijd van de bomen stijgt, de stamdiameter toeneemt.")
        st.markdown("***")

        show_with_options(boomnummer_leeftijd_denhaag,"Leeftijd per Boomnummer Den Haag")
        st.write("In het bovenstaande figuur is een regressieanalyse te zien van de leeftijd van de bomen per boomnummer in Den Haag. Uit dit figuur blijkt over het algemeen dat hoe ouder de bomen zijn hoe lager het boomnummer is. Dit is voornamelijk te zien aan de spreiding en niet zo zeer aan de regressieplot")




