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

def leeftijd():
    fig = go.Figure()

    fig.add_trace(go.Box(x=amsterdam['leeftijd'],
                         name='Amsterdam',
                         marker_color='indianred'))

    fig.add_trace(go.Box(x=df_denhaag['LEEFTIJD'],
                         name='Den Haag',
                         marker_color='lightseagreen'))

    fig.update_layout(xaxis_title='Leeftijd in jaren') #title_text="Leeftijd van bomen in Den Haag en Amsterdam",

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
                      #title_text='Histogram van de leeftijd van bomen in Amsterdam en Den Haag',
                      xaxis_title='Leeftijd in jaren',
                      yaxis_title='Aantal bomen')

    fig.update_traces(opacity=0.75)

    st.plotly_chart(fig, use_container_width=True)


def boomhoogte_leeftijd_amsterdam():
    fig = px.box(amsterdam, x='Boomhoogte', y='leeftijd',
                 category_orders={'Boomhoogte': ['tot 6 m.', '6 tot 9 m.', '6 tot 12 m.', '9 tot 12 m.', '12 tot 15 m.',
                                                 '12 tot 18 m.', '15 tot 18 m.', '18 tot 24 m.', '24 m. en hoger',
                                                 'Onbekend']})
    fig.update_layout(#title="Leeftijd per boomhoogte klasse",
                    yaxis_title="Leeftijd in jaren")
    st.plotly_chart(fig, use_container_width=True)

def radius_leeftijd_amsterdam():
    fig = px.box(amsterdam, x='RADIUS', y='leeftijd')
    fig.update_layout(
        #title="Radius klasse per Leeftijd",
        xaxis_title="Radiusklasse",
        yaxis_title="Leeftijd in jaren")
    st.plotly_chart(fig, use_container_width=True)

def radius_leeftijd_amsterdam_ols():
    fig = px.scatter(amsterdam, y='RADIUS', x='leeftijd', color = "Soortnaam_NL", trendline="ols", opacity= 0.5)#, trendline_color_override = "red")
    fig.update_layout(
        #title="Radius klasse per Leeftijd",
        legend_title_text= 'Soortnaam',
        yaxis_title="Radiusklasse",
        xaxis_title="Leeftijd in jaren")
    st.plotly_chart(fig, use_container_width=True)


def stamdia_leeftijd_denhaag():
    fig = px.box(df_denhaag, x='STAMDIAMETERKLASSE', y='LEEFTIJD',
                 category_orders={
                     'STAMDIAMETERKLASSE': ['0-10 cm', '10-25 cm', '25-50 cm', '50-75 cm', '75-100 cm', '>100 cm']})
    fig.update_layout(
        #title="Leeftijd per Stamdiameterklasse Denhaag",
        xaxis_title="Stamdiameterklasse",
        yaxis_title="Leeftijd in jaren")

    st.plotly_chart(fig, use_container_width=True)



def stadsdeel_leeftijd_denhaag():
    fig = px.box(df_denhaag, x='STADSDEEL', y='LEEFTIJD')
    fig.update_layout(
        #title = "Leeftijd per stadsdeel Den Haag",
        xaxis_title = "Stadsdeel",
        yaxis_title = "Leeftijd in jaren")
    st.plotly_chart(fig, use_container_width=True)


def stadsdeel_leeftijd_amsterdam():
    fig = px.box(amsterdam, x='Beheerder', y='leeftijd')
    fig.update_layout(
    #title = "Leeftijd per Beheerder Amsterdam",
    xaxis_title = "Beheerder",
    yaxis_title = "Leeftijd in jaren")
    st.plotly_chart(fig, use_container_width=True)

def boomstam_leeftijd_corr_dh():
    df_denhaag['STAMDIAMETERKLASSE2'] = df_denhaag['STAMDIAMETERKLASSE'].astype("str").apply(
        lambda x: "100" if x[-5:-3] == "00" else ("0" if x[-5:-3] == "" else x[-5:-3]))
    df_denhaag['STAMDIAMETERKLASSE2'] = df_denhaag['STAMDIAMETERKLASSE2'].astype("int")

    df = pd.DataFrame(df_denhaag, columns=['STAMDIAMETERKLASSE2', 'LEEFTIJD'])

    fig, ax = plt.subplots()
    sn.heatmap(df.corr(), ax=ax,annot=True)
    st.write(fig)
    #fig, ax = plt.subplots()
    #sn.regplot(x="STAMDIAMETERKLASSE2", y="LEEFTIJD", data=df_denhaag, ci=None, scatter_kws={'alpha': 0.5}, ax=ax)
    #st.write(fig)

    fig = px.scatter(df_denhaag, y='STAMDIAMETERKLASSE2', x='LEEFTIJD', color = 'BOOMSOORT_NEDERLANDS', trendline="ols", opacity= 0.5)#, trendline_color_override = "red")
    fig.update_layout(
        #title="Stamdiameterklasse per Leeftijd Denhaag",
        yaxis_title="Stamdiameterklasse in (cm)",
        xaxis_title="Leeftijd in jaren")

    st.plotly_chart(fig, use_container_width=True)

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
    st.header("Leeftijd Analyse")

    st.markdown("***")
    show_with_options(leeftijd,
                      "Boxplot van de Leeftijd van de bomen in Den Haag en Amsterdam")
    st.write("Om te kijken naar de verdeling van de leeftijd van de Bomen in Amsterdam en Den Haag zijn er twee boxplots geplot. Hiervoor zijn er outliers we gefilterd nadat de leeftijd van de oudste bomen in de twee steden is onderzocht. Omvallend is dat er in Amsterdam iets meer oudere bomen staan dan in Den Haag. De oudste bomen zijn echt wel in Den Haag te vinden.")
    st.markdown("***")

    show_with_options(leeftijd_hist,
                      "Histogram van de Leeftijd van de bomen in Den Haag en Amsterdam")
    st.write("Naast een boxplot is er een histogram gemaakt. Hierin is de verdeling te zien, maar er is ook te zien dat Amsterdam een stuk meer bomen heeft dan Den Haag. Opvallend hier in is ook de hoge piek van bomen van 0 jaar in Amsterdam.")
    st.markdown("***")

    col1, _, col3 = st.columns([3, 1, 3])

    with col1:
        st.image("assets/amsterdam.png", width=200)
        show_with_options(boomhoogte_leeftijd_amsterdam,
                          "Verdeling Leeftijd per Boomhoogteklasse")
        st.write("Er is gekeken naar de leeftijd van de bomen per boomhoogte. Hieruit valt op te maken dat hoe wanneer de bomen ouder zijn ze in een hogere hoogte-klasse vallen")
        st.markdown("***")

        show_with_options(stadsdeel_leeftijd_amsterdam,
                          "Verdeling Leeftijd per Beheerder Amsterdam")

        st.write("Er zijn boxplots gemaakt van de leeftijd van de bomen in Amsterdam tegenover de beheerder van de bomen. Wat opvalt is dat er een aantal stadsdelen zijn waarbij de box van de boxplots dicht bij de 0 ligt, wat betekend dat de meeste bomen in dit gebied korgeleden zijn geplant. De oudste bomen va Amsterdam zijn te vinden in Stadsdeel Zuid en Stadsdeel Oost.")
        st.markdown("***")


        show_with_options(radius_leeftijd_amsterdam,
                      "Verdeling Leeftijd per Radiusklasse")
        st.write("De leeftijd van de bomen per radiusklasse. Doordat de radius van de bomen alleen in hele meter wordt gemeten is het handiger om deze in boxplots te plotten in plaats van een scotterplot. Opvallend aan dit figuur is dat de data van klasse 6 ontbreekt. Daarnaast zou je kunnen zeggen dat vanaf de radiusklasse 2 de leeftijd van de bomen steeds hoger ligt bij een hogere radiusklasse.")
        st.markdown("***")
    with col3:
        st.image("assets/denhaag.png", width=200)
        show_with_options(stamdia_leeftijd_denhaag,
                          "Verdeling Leeftijd per stamdiameterklasse Den Haag")
        st.write("De leeftijd van de boom is geplot tegenover de stamdiameterklasse van de bomen. Hier is een duidelijke trend te zien dat wanneer de leeftijd toe neemt, de bomen vaker is een hohgere stamdiameterklasse vallen.")
        st.markdown("***")

        show_with_options(stadsdeel_leeftijd_denhaag,
                          "Leeftijd per stadsdeel Den Haag")
        st.write("Ook voor Den Haag is er gekeken naar de verdeling van leeftijd van de bomen per stadsdeel. Naast dat er minder stadsdelen zijn in Den Haag is er ook te zien dat de verdelingen veel meer op elkaar lijken. Alleen in Leidschvee-Ypenburg zijn de meeste bomen iets jonger dan in de rest van de stad. De oudste bomen van Den Haag zijn te vinden in Haagse Hout.")




