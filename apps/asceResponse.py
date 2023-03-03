import streamlit as st
import folium as fl
from streamlit_folium import st_folium

st.markdown("# 🔹ASCE7-22 Response Spectrum Creator")

def get_pos(lat,lng):
    return lat,lng

m = fl.Map(location=[40, -55], zoom_start=4)

m.add_child(fl.LatLngPopup())

map = st_folium(m, height=250, width=1500, center=[40, -55], zoom=3)

if map['last_clicked']:
    data = get_pos(map['last_clicked']['lat'],map['last_clicked']['lng'])
    st.write(data)