import requests as rq
import streamlit as st
import pandas as pd
import utils.constants as constants
import inspect

@st.cache
def fetchRDWData(isBrandstof=False):
    url = constants.RDW_KENTEKEN_URL
    if (isBrandstof):
        url = constants.RDW_BRANDSTOF_API_URL
    response = rq.get(url, 
    headers={"X-App-Token": st.secrets['RDW_API_KEY']})
    df = pd.read_json(response.json())

@st.cache
def fetchOCMData(token, isFilters=False):
    response = rq.get(constants.OCM_API_URL, 
    headers={"X-API-Key": token}, params={"maxresults": 500}).json()
    df = pd.json_normalize(response)
    fitlers = pd.json_normalize(response, record_path=["Connections"])
    listOfCols = ['IsRecentlyVerified', 'UsageType.Title', 'AddressInfo.Latitude', 'AddressInfo.Longitude', 'AddressInfo.StateOrProvince', 
    'Connections', 'NumberOfPoints', 'StatusTypeID']
    df['Connections'] = df['Connections'].apply(lambda x: [y['ConnectionType']['Title'] for y in x])
    df.drop(columns=df.columns[~df.columns.isin(listOfCols)].values, axis=1, inplace=True)
    if (isFilters):
        return fitlers['ConnectionType.Title'].unique()
    return df

# Started earlier than Ended
# Charge time smaller than Connected time
# Charge time and connected time format to hours:minutes:seconds
# 'Schrikkeljaar' entry is incorrect (2018-02-29)
@st.cache
def fetchLaadPaalData(type=None):
    df = pd.read_csv('data/laadpaaldata.csv', delimiter=',')
    df['Started'] = pd.to_datetime(df['Started'], errors='coerce')
    df['Ended'] = pd.to_datetime(df['Ended'], errors='coerce')

    if (type == "Dates"):
        return df[df['Started'] < df['Ended']]
    elif (type == "CTime"):
        return df[df['ConnectedTime'] > df['ChargeTime']]
    return df[(df['Started']) < df['Ended'] & (df['ConnectedTime'] > df['ChargeTime'])]

def show_with_options(func, text=''):
    import components.base as base
    if (text != ''):
        st.markdown('*' + text + '*')
    if base.showPlots: func()
    if base.showCode: st.code(inspect.getsource(func))