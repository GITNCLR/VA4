import streamlit as st
from utils.helpers import fetchOCMData, show_with_options
import folium
from streamlit_folium import folium_static
import numpy as np

df = fetchOCMData(st.secrets['OCM_API_KEY'])
filters = fetchOCMData(st.secrets['OCM_API_KEY'], True)
selectedProvince = ""
chargingTypes = []

def map():
    global df
    colors = {True : 'green', False : 'red'}
    if (selectedProvince == 'Nederland (centraal)'):
        map = folium.Map(location=[52.358993, 4.903005], zoom_start=7, control_scale=True, width=850, height=500) 
    else:
        central = df.loc[df['AddressInfo.StateOrProvince'] == selectedProvince].iloc[0]
        lat, lon = (central['AddressInfo.Latitude'], central['AddressInfo.Longitude'])
        map = folium.Map(location=[lat, lon], zoom_start=10, control_scale=True, width=850, height=500)
    new_df = df[[set(x).issubset(set(chargingTypes)) for x in df['Connections']]]
    
    new_df.apply(lambda row: folium.Marker(location=[row["AddressInfo.Latitude"], row["AddressInfo.Longitude"]], 
                                            icon=folium.Icon(color=colors[row['IsRecentlyVerified']]), popup=row['IsRecentlyVerified'], fill_opacity=1)
                                            .add_to(map), axis=1)
    folium_static(map)

def main():
    st.header("Open Charge Map")
    col1, _, col3 = st.columns([6, 1, 3])
    with col3:
        global selectedProvince
        global chargingTypes
        listOfProvinces = np.insert(df.sort_values(by=['AddressInfo.StateOrProvince'])['AddressInfo.StateOrProvince']
            .dropna().unique(), 0, 'Nederland (centraal)')
        selectedProvince = st.selectbox(
            "Provincie",
            listOfProvinces)
        chargingTypes = st.multiselect(
            "Oplaad type",
            filters, default=filters)
        
    with col1:
        show_with_options(map, "Met de data van de OpenChargeMap is er een map van Nederland gemaakt van het aantal laadpunten. Met de dropdown kan een specifieke provincie geselecteerd worden en met de checkbox zijn één of meerdere oplaadtypes te selecteren. De kleur groen geeft de recent geverifieerde laadpunten weer en de kleur rood geeft de niet recent geverifieerde laadpunten aan. Opvallend is dat er met een limiet van 500 rows een klein percentage van de laadpunten geverifieerd zijn. Verder is opvallend dat het merk CHadeMO weinig laadpunten heeft.")
    st.markdown("***")

