import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')

#https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/

st.set_page_config(page_title="superstore", page_icon=":bar_chart:", layout="wide")

st.title(" :bar_chart: Sample SuperStore EDA")
st.markdown('<style>div.block-container{padding-top:1rem}</style>', unsafe_allow_html=True)

fl = st.file_uploader(":file_folder: Upload a file", type=(["csv", "txt", "xlsx", "xls"]))
if fl is not None:
    filename = fl.name
    st.write(filename)
    df = pd.read_csv(filename, encoding= "iso-8859-1")
else:
    os.chdir(r"D:\Dev\dasboard_streamlit")
    df = pd.read_csv("Sample - Superstore.csv", encoding= "iso-8859-1")


df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Order Date"] = df["Order Date"].dt.strftime("%m/%d/%Y")

print(df["Order Date"])

col1, col2 = st.columns((2))
#df['Order Date'] = pd.to_datetime(df["Order Date"])
df['Order Date'] = pd.to_datetime(df["Order Date"])

# Getting the min and max date
startdate = pd.to_datetime(df["Order Date"]).min()
enddate = pd.to_datetime(df["Order Date"]).max()

with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startdate))

with col2:
    date2 = pd.to_datetime(st.date_input("End Date", enddate))

df = df[(df["Order Date"] >= date1) & (df["Order Date"] <= date2)].copy()

