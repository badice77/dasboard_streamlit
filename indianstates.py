# https://un-mapped.carto.com/tables/states_india/public/map
# https://www.youtube.com/watch?v=aJmaw3QKMvk

import json
import pandas as pd
import streamlit as st
# python -m streamlit run indianstates.py

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


india_states = json.load(open("states_india.geojson", 'r'))

df = pd.read_csv("india_population.csv",delimiter=";")
st.write(df["Population Density"].apply(lambda x: int(x.split("/")[0].replace(",",""))))
df["Density"] = df["Population Density"].apply(lambda x: int(x.split("/")[0].replace(",","")))

# mapping besoin d'un ID : india_states['features'][0].keys() --> dict_keys(['type', 'geometry', 'properties'])
#st.write(india_states['features'][0].keys())
# st.write(india_states['features'][1]['properties'])
# {
# "cartodb_id":2
# "state_code":35
# "st_nm":"Andaman & Nicobar Island"
# }
state_id_map = {}
for feature in india_states['features']:
    feature['id'] = feature['properties']['state_code']
    state_id_map[feature['properties']['st_nm']] = feature['id']

#st.write(state_id_map)
# {
# "Telangana":0
# "Andaman & Nicobar Island":35
# "Andhra Pradesh":28
# "Arunanchal Pradesh":12
# "Assam":18
# "Bihar":10
# "Chhattisgarh":22
# "Daman & Diu":25

df['id'] = df['State or Union Territory'].apply(lambda x: state_id_map[x])

display_dataframe_details(df)

#Dadra and Nagar Haveli and Daman and Diu
# Dadara & Nagar Havelli