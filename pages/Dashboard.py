import streamlit as st
import pandas as pd
import seaborn as sns
import altair as alt
from connect import *
import time
from helper_functions import dataHandler

st.set_page_config(layout="wide")  
st.title("Dashboard Visualizations")

data = dataHandler.load_data()


filtered_data, provinsi_selected, kota_selected = dataHandler.sidebar_filters(data, page = "Statistik Kemiskinan")