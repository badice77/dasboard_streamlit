import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

#https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/
APP_TITLE = " :world_map: Fraud and Identiy Theft Report"
APP_SUB_TITLE = "Source: Federal Trade Commission"

# python -m streamlit run state.py

# Block comment : Ctrl + K + C
# Duplicate line : Shift + Alt + Down/Up
# Select word : Ctrl + D
# Select current line : Ctrl + L
# Multi cursor selection : Alt + Click

def display_dataframe_details(Dataframe):
    st.write(Dataframe.shape)
    st.write(Dataframe.head())
    st.write(Dataframe.columns)
    st.write(Dataframe.dtypes)


def display_fraud_facts(df, quarter, report_type,state_name,field_name, metric_title, is_medium=False):
#def display_fraud_facts(df, year, quarter, report_type,state_name,field_name, metric_title):
    df = df[(df['Quarter'] == quarter) & (df['Report Type'] == report_type)]
    if state_name:
        df = df[df['State Name'] == state_name]
    df.drop_duplicates(inplace=True)
    if is_medium:
        total = df[field_name].sum() / len(df) if len(df) else 0
    else:
        total = df[field_name].sum()
    st.metric(metric_title, '{:,}'.format(total))

def display_map(df, year, quarter):
    df = df[(df['Quarter'] == quarter) ]

    map = folium.Map(location=[38, -96.5], zoom_start=4, scrollWheelZoom=False, tiles='CartoDB positron')

    choropleth = folium.Choropleth(
        geo_data='us-state-boundaries.geojson',
        data = df,
        columns=('State Name','State Total Reports Quarter'),
        key_on = 'feature.properties.name',
        line_opacity=0.5,
        highlight=True
        )
    choropleth.geojson.add_to(map)

    df = df.set_index('State Name')
    state_name = 'North Carolina'
    #st.write(df.loc[state_name , 'State Pop'][0])

    for feature in choropleth.geojson.data['features']:
        state_name = feature['properties']['name']
        feature['properties']['population'] = 'Population : ' + str('{:,}'.format(round(df.loc[state_name , 'State Pop'][0])) if state_name in list(df.index) else 'N/A')
        feature['properties']['per_100k'] = 'Reports/100k Population' + str('{:,}'.format(round(df.loc[state_name , 'Reports per 100K-F&O together'][0])) if state_name in list(df.index) else 'N/A')

    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(['name', 'population','per_100k'], labels=False)
    )

    st_map = st_folium(map, width=700, height=550)
    #display_dataframe_details(df)
    state_name = ''
    if st_map['last_active_drawing']:
        #st.write(st_map['last_active_drawing']['properties']['name'])
        state_name = st_map['last_active_drawing']['properties']['name']
    return state_name

#State Total Reports Quarter

def display_time_filters(df):
    year_list = list(df['Year'].unique())
    year_list.sort(reverse=True)
    #st.write(year_list)
    year = st.sidebar.selectbox('Year', year_list)
    quarter_list = list(df['Quarter'].unique())
    quarter_list.sort(reverse=False)
    quarter = st.sidebar.radio('Quarter', quarter_list)
    st.header(f' {year} Q{quarter}')
    return year, quarter

def display_state_filter(df, state_name):
    state_list = [''] + list(df['State Name'].unique()) 
    state_list.sort()
    state_index = state_list.index(state_name) if state_name and state_name in state_list else 0
    state_name = st.sidebar.selectbox('State', state_list, state_index)
    return state_name

def display_report_type(df):
    report_list = list(df['Fraud'].unique())
    report_list.sort()
    report_type = st.sidebar.radio('Fraud Type', report_list)
    return report_type


def main():
    #https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/
    st.set_page_config(APP_TITLE, layout="wide", page_icon=":world_map:")
    st.title(APP_TITLE)
    st.caption(APP_SUB_TITLE)

    # Load data
    # AxS-Fraud Box_Full Data_data.csv   
    df_continental = pd.read_csv("AxS-Continental_Full Data_data.csv")
    df_fraud = pd.read_csv("AxS-Fraud Box_Full Data_data.csv")

    #df_fraud['Year'] = pd.to_datetime(df_fraud['Year'], format='%Y')
    #df_fraud['Year2'] = df_fraud['Year'].df.strftime('%Y')
    # AxS-Losses Box_Full Data_data.csv
    ds_loss = pd.read_csv("AxS-Losses Box_Full Data_data.csv")
    ds_medium = pd.read_csv("AxS-Median Box_Full Data_data.csv")

    # year = 2022
    # quarter = 1
    # state_name = 'Texas'
    report_type = "Fraud"
    field_name = 'State Fraud/Other Count'

    #display_dataframe_details(ds_medium)


    # DISPLAY FILTRERS AND MAP
    year, quarter = display_time_filters(df_continental)
    state_name = display_map(df_continental, year, quarter)
    state_name = display_state_filter(df_continental,state_name)
    report_type = display_report_type(df_fraud)

    # DISPLAY MATRICS
    st.subheader(f'{state_name} {report_type} Facts')
    col1 , col2 , col3 = st.columns(3)
    with col1:
        #display_fraud_facts(df_fraud, year, quarter, report_type, state_name, field_name, f'# of {report_type} Reports')
        display_fraud_facts(df_fraud, quarter, report_type, state_name, field_name, f'# of {report_type} Reports')
    with col2:
        display_fraud_facts(ds_medium, quarter, report_type, state_name, 'Overall Median Losses Qtr', 'Medium $ Loss', is_medium=True)
    with col3:
        display_fraud_facts(ds_loss, quarter, report_type, state_name, 'Total Losses', 'Total $ Loss')

if __name__ == "__main__":
    main()

# python -m streamlite run state.py