import streamlit as st
from utils.helpers import fetchLaadPaalData, show_with_options
import plotly.express as px
import streamlit as st
import plotly.figure_factory as ff
import plotly.graph_objects as go
from statsmodels.formula.api import ols


main_df = fetchLaadPaalData("CTime")

def scatter():
    global main_df
    global x_col
    global y_col
    df = main_df.drop(main_df.loc[main_df["ChargeTime"]<0].index)
    fig = px.scatter(
        df,
        y=y_col,
        x=x_col
    )
    fig.update_layout(
        xaxis_title=x_col,
        yaxis_title=y_col)
    st.plotly_chart(fig, use_container_width=True)

def boxplot_chargetime():
    global main_df
    df = main_df.drop(main_df.loc[main_df["ChargeTime"]<0].index)
    fig = px.box(df, x='ChargeTime', title='Boxplot chargetime in uren')
    fig.update_layout(
        xaxis_title="Chargetime in uren",
        yaxis_title="Waarnemingen")
    st.plotly_chart(fig, use_container_width=True)

def boxplot_maxpower():
    global main_df
    fig = px.box(main_df, x='MaxPower', title='Boxplot maxpower')
    fig.update_layout(
        xaxis_title="Maximaal gevraagde vermogen (W)",
        yaxis_title="Waarnemingen")
    st.plotly_chart(fig, use_container_width=True)

def boxplot_totalenergy():
    global main_df
    fig = px.box(main_df, x='TotalEnergy', title='Boxplot TotalEnergy')
    fig.update_layout(
        xaxis_title="Totaal verbruikte energie in Wh",
        yaxis_title="Waarnemingen")
    st.plotly_chart(fig, use_container_width=True)

def histogram_chargetime():
    # Mediaan: 2.5003 en gem: 2.80 --> berekeningen
    # Exclusief de negatieve waarden en de uitschieter van boven de 50 
    global main_df
    df = main_df.drop(main_df.loc[(main_df["ChargeTime"]<0) | (main_df["ChargeTime"]>50)].index)
    group_labels = ['Chargetime']
    hist_data= [df["ChargeTime"]]
    fig = ff.create_distplot(hist_data, group_labels)
    fig.add_annotation(x=22, y=0.32,
                text="Gemiddelde: 2.80  |  Mediaan: 2.50",
                showarrow=False,
                yshift=1)
    fig.update_layout(title={"text":'Dichtheidsfunctie van chargetime in uren',
                            'x':0.5},
                    xaxis_title='Chargetime in uren',
                    yaxis_title='Kans')
    st.plotly_chart(fig, use_container_width=True)

def histogram_maxpower():
    global main_df
    fig=px.histogram(data_frame=main_df,
                 x='MaxPower') 
    fig.add_annotation(x=17000, y=2200,
                text="Gemiddelde: 4035.34  |  Mediaan: 3396",
                showarrow=False,
                yshift=1)
    fig.update_layout(title={'text':'Histogram maximaal gevraagde vermogen (W)', 'x':0.5},
                    yaxis_title='Frequentie',
                    xaxis_title='Maximaal gevraagde vermogen (W)')
    st.plotly_chart(fig, use_container_width=True)

def histogram_maxpower_nout():
    global main_df
    df33 = main_df["MaxPower"].between(2834, 4050, inclusive = True)
    fig=px.histogram(data_frame=main_df[df33],
                 x='MaxPower') 

    fig.add_annotation(x=3800, y=550,
          text="Gemiddelde: 3415.88  | Mediaan: 3392",
          showarrow=False,
           yshift=1)

    fig.update_layout(title={'text':'Histogram maximaal gevraagde vermogen tussen 2834 en 4050 (W)'},
                  yaxis_title='Frequentie',
                 xaxis_title='Maximaal gevraagde vermogen (W)')

    st.plotly_chart(fig, use_container_width=True)

def histogram_totalenergy():
    global main_df
    fig=px.histogram(data_frame=main_df,
                 x='TotalEnergy') 
    fig.add_annotation(x=70000, y=850,
                text="Gemiddelde: 10407.46  |  Mediaan: 7713",
                showarrow=False,
                yshift=1)
    fig.update_layout(title={'text':'Histogram totaal verbruikte energie in Wh', 'x':0.5},
                    yaxis_title='Frequentie',
                    xaxis_title='Totaal verbruikte energie in Wh')
    st.plotly_chart(fig, use_container_width=True)

def histogram_totalenergy_nout():
    global main_df
    df44 = main_df["TotalEnergy"].between(1, 19025, inclusive = True)
    fig=px.histogram(data_frame=main_df[df44],
        x='TotalEnergy') 

    fig.add_annotation(x=16000, y=450,
        text="Gemiddelde: 7372.82  |  Mediaan: 7380",
        showarrow=False,
        yshift=1)

    fig.update_layout(title={'text':'Histogram totaal verbruikte energie tussen 1 en 19025 in Wh', 'x':0.5},
        yaxis_title='Frequentie',
        xaxis_title='Totaal verbruikte energie in Wh')

    st.plotly_chart(fig, use_container_width=True)


def regression():
    global main_df


    df_reg = main_df[main_df["ChargeTime"].between(0,40)]
    df_reg = df_reg[df_reg["MaxPower"].between(3000,3800)]

    mdl_chargetime_vs_totalenergy = ols("TotalEnergy ~ ChargeTime", data=df_reg).fit()
    explanatory_data = df_reg[['ChargeTime']]
    mdl_chargetime_vs_totalenergy.predict(explanatory_data)
    prediction_data = explanatory_data.assign(TotalEnergy=mdl_chargetime_vs_totalenergy.predict(explanatory_data))
    fig = px.scatter(df_reg, y="TotalEnergy", x="ChargeTime",color = "TotalEnergy",
                 title="REG")

    fig.add_trace(
        go.Scatter(
            y=prediction_data["TotalEnergy"],
            x=prediction_data["ChargeTime"], showlegend= False)
    )
    fig.update_traces(name='Voorspelling')
    fig.update_layout(title={'text': 'Voorspelling voor "Totaal verbruikte energie" op basis van "Oplaadtijd" met Ols ', 'x': 0.5},
                      xaxis_title='Oplaadtijd',
                      yaxis_title='Totaal verbruikte energie in Wh',
                    coloraxis_colorbar=dict(title="Totaal verbruikte energie <br> in Wh")
    )

    st.plotly_chart(fig, use_container_width=True)


def main():
    st.header("Laadpalen")
    col1, _, col3 = st.columns([6, 1, 3])
    with col3:
        global x_col
        global y_col
        x_col = st.selectbox(
            "X Waarde",
            main_df.columns)
        y_col = st.selectbox(
            "Y Waarde",
            main_df.columns,
            index=2)
    with col1:
        show_with_options(scatter, "In dit figuur kunt u zelf de x-en y as van een scatterplot bepalen door middel van de dropdown menu’s.")

    show_with_options(histogram_chargetime, "In het figuur van de dichtheid functie is te zien dat de meeste waarden liggen tussen de 30 minuten en 5 uur. Dit wordt ondersteunt door het gemiddelde van 2,8 uur en de mediaan van 2,5 uur.")
    with st.expander("Boxplot", False):
        show_with_options(boxplot_chargetime, "In deze boxplot is de spreiding van de chargetime in uren te zien. Voorafgaand aan het maken van de boxplot zijn alle negatieve waarden verwijderd, aangezien chargetime niet negatief kan zijn. Wat er opvalt aan deze boxplot is dat er een aantal outliers zitten in de dataset. De grootste uitschieter, met een waarde van 52 is verwijderd bij het maken van het figuur van de dichtheidsfunctie.")

    show_with_options(histogram_maxpower, "")
    show_with_options(histogram_maxpower_nout, "In de eerste histogram is net zoals in de boxplot te zien dat er een enorme spreiding is. Om een beter beeld te krijgen is er een tweede histogram gemaakt, ingezoomd op de data die binnen de boxplot valt . Hieruit is een nieuw gemiddelde berekent van 3415 en een mediaan van 3392. Dit komt omdat de meeste data die weg gefilterd is hoge waarden bevatten.  Uit het figuur blijkt dat de meeste waarden tussen de 3200 en 3600 wat liggen.")
    with st.expander("Boxplot", False):
        show_with_options(boxplot_maxpower, "In deze boxplot is te zien dat er een grote spreiding is van het maximaal gevraagde vermogen. De data is gegeven in Jules per seconde (W). Omdat weten dat de data afkomstig is van een soort laadpaal is een logische verklaring dat dit komt door de verschillende soorten auto met bijbehorende (snel)laders die op de markt zijn. Het gemiddelde van de data is 4035 en de mediaan is 3396.")

    show_with_options(histogram_totalenergy, "")
    show_with_options(histogram_totalenergy_nout, "Deze figuren geeft de totaal verbruikte energie per laadsessie weer. Deze boxplot laat zien dat de data wederom een grote spreiding bevat, met veel hoge uitschieters. Net als bij het vorige figuur van het maximaal gevraagde vermogen is er voor dit figuur een extra histogram toegevoegd om te kijken naar de data die binnen de histogram valt.  Een verklaring voor de grote spreiding is dat de totaal verbruikte energie sterk wordt beïnvloed door de maximaal gevraagde vermogen en door de charge time per sessie. Het gemiddelde van de totaal verbruikte energie per sessie is 10407 Wh. De mediaan is 7713 Wh.")
    with st.expander("Boxplot", False):
        show_with_options(boxplot_totalenergy, "")
    show_with_options(regression, "In het volgende figuur is een scatterplot met daarin een lineaire regressie te zien. Op de y-as van de scatterplot is de totaal verbruikte energie per laadsessie te zien. Op de x-as  is de chargetime per sessie te zien. Door middel van een lineaire regressie is er op basis van de chargetime  voorspeld wat de de totaal verbruikte energie zal worden. De voorspellende data is af te lezen met behulp van de lijn die door het figuur loopt. De voorspelling is gemaakt op basis van de data van de meerderheid groep die valt tussen een gevraagd vermogen tussen 3000 W en 3800 W. Een mogelijke verklaring voor het afwijken van de voorspelling voor hoge charge time waardes kan te maken hebben met de oplaad curve van batterijen.")
    st.markdown("***")

