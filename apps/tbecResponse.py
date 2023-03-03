import streamlit as st
import folium as fl
from streamlit_folium import st_folium
import plotly.graph_objects as go

st.markdown("# 🔸TBEC-2018 Response Spectrum Creator")

def get_pos(lat,lng):
    return lat,lng

m = fl.Map(location=[39, 48], zoom_start=5)

m.add_child(fl.LatLngPopup())

map = st_folium(m, height=250, width=1500, center=[39, 48], zoom=5)

if map['last_clicked']:
    data = get_pos(map['last_clicked']['lat'],map['last_clicked']['lng'])
    st.write(data)

responseFig = go.Figure()
responseFig.update_xaxes(
                        title_text = 'Period (s)',
                        range = [0,3.5],
                        showgrid = True,
                        showline = True,
                    )

responseFig.update_yaxes(
                        title_text = 'pSa (g)',
                        showgrid = True,
                        showline = True
                    )

responseFig.update_layout(showlegend=True, 
                          plot_bgcolor = "#F0F2F6",
                          title = 'TBEC-2018 Response Spectrum', title_x=0.4,
                          height = 500,
                          legend = dict(
                            yanchor="top",
                            xanchor="right"
                        ))

inputCol, graphCol = st.columns([1,2])

with inputCol:
    with st.form('inputForm'):
        latitude = st.number_input("Latitude")
        longitude = st.number_input("Longitude")
        soil = st.selectbox("Soil Type", ('ZA', 'ZB', 'ZC', 'ZD', 'ZE'), 2)
        intensityLevel = st.selectbox("Intensity Level", ["DD1", "DD2", "DD3", "DD4"], 2)
        createButton = st.form_submit_button("Create Response Spectrum")

with graphCol:
    st.plotly_chart(responseFig, use_container_width=True)
