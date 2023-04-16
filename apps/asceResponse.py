import streamlit as st
import folium as fl
from streamlit_folium import st_folium
import plotly.graph_objects as go
from functions.asceResponse.accessAsce import getAsceDataMulti, getAsceDataMultiMCEr, getAsceDataTwo, getAsceDataTwoMCEr
from injections import addLogo

# set title
st.markdown("# 🔹ASCE7-22 Response Spectrum Creator")
addLogo()

# create a function for get position from map
def get_pos(lat,lng):
    return lat,lng

# create folium map and zoom in usa
m = fl.Map(location=[40, -55], zoom_start=3)
m.add_child(fl.LatLngPopup())
map = st_folium(m, height=250, width=1500, center=[40, -55], zoom=3)

# get location data from click event
locationData = [37.0, -81.0]
if map['last_clicked']:
    clickedData = get_pos(map['last_clicked']['lat'],map['last_clicked']['lng'])
    locationData[0] = clickedData[0]
    locationData[1] = clickedData[1]

# create default figure for multi period spectrum
multiDefaultFig = go.Figure()
multiDefaultFig.update_xaxes(
                    title_text = 'Period (s)',
                    range = [0,3.5],
                    showgrid = True,
                    showline = True,
                )

multiDefaultFig.update_yaxes(
                    title_text = 'pSa (g)',
                    showgrid = True,
                    showline = True,
                )

multiDefaultFig.update_layout(showlegend=False, 
                              plot_bgcolor = "#F0F2F6",
                              title = 'ASCE7-22 Multi Period Design Spectrum', title_x=0.35,
                              height = 500
                        )

# create default figure for multi period mcer spectrum
multiMcerDefaultFig = go.Figure()
multiMcerDefaultFig.update_xaxes(
                    title_text = 'Period (s)',
                    range = [0,3.5],
                    showgrid = True,
                    showline = True,
                )

multiMcerDefaultFig.update_yaxes(
                    title_text = 'pSa (g)',
                    showgrid = True,
                    showline = True,
                )

multiMcerDefaultFig.update_layout(showlegend=False, 
                              plot_bgcolor = "#F0F2F6",
                              title = 'ASCE7-22 Multi Period MCEr Design Spectrum', title_x=0.35,
                              height = 500
                        )

# create default figure for two period spectrum
twoPeriodDefaultFig = go.Figure()
twoPeriodDefaultFig.update_xaxes(
                    title_text = 'Period (s)',
                    range = [0,3.5],
                    showgrid = True,
                    showline = True,
                )

twoPeriodDefaultFig.update_yaxes(
                    title_text = 'pSa (g)',
                    showgrid = True,
                    showline = True,
                )

twoPeriodDefaultFig.update_layout(showlegend=False, 
                              plot_bgcolor = "#F0F2F6",
                              title = 'ASCE7-22 Two Period Design Spectrum', title_x=0.35,
                              height = 500
                            )

# create default figure for two period mcer spectrum
twoPeriodMcerDefaultFig = go.Figure()
twoPeriodMcerDefaultFig.update_xaxes(
                    title_text = 'Period (s)',
                    range = [0,3.5],
                    showgrid = True,
                    showline = True,
                )

twoPeriodMcerDefaultFig.update_yaxes(
                    title_text = 'pSa (g)',
                    showgrid = True,
                    showline = True,
                )

twoPeriodMcerDefaultFig.update_layout(showlegend=False, 
                              plot_bgcolor = "#F0F2F6",
                              title = 'ASCE7-22 Two Period MCEr Design Spectrum', title_x=0.35,
                              height = 500
                        )

# create form
with st.form('inputForm'):
    latitudeCol, longitudeCol, siteCol = st.columns(3)
    with latitudeCol:
        latitude = st.number_input("Latitude", value = locationData[0])
    with longitudeCol:
        longitude = st.number_input("Longitude", value = locationData[1])
    with siteCol:
        site = st.selectbox("Site Category", ["A", "B", "C", "D", "E"], 2)

    responseButton = st.form_submit_button("Create Response Spectrums")

# execute response spectrum functions
multiPeriodSpectrum = getAsceDataMulti(latitude, longitude, 'III', site, 'Call')
multiPeriodMcerSpectrum = getAsceDataMultiMCEr(latitude, longitude, 'III', site, 'Call')
twoPeriodSpectrum = getAsceDataTwo(latitude, longitude, 'III', site, 'Call')
twoPeriodMcerSpectrum = getAsceDataTwoMCEr(latitude, longitude, 'III', site, 'Call')

if responseButton:
    # push data to the figures
    multiDefaultFig.add_trace(go.Scatter(
        x = multiPeriodSpectrum['multiPeriodDesignSpectrumPeriods'],
        y = multiPeriodSpectrum['multiPeriodDesignSpectrumOrdinates']
    ))

    multiMcerDefaultFig.add_trace(go.Scatter(
        x = multiPeriodMcerSpectrum['multiPeriodMCErSpectrumPeriods'],
        y = multiPeriodMcerSpectrum['multiPeriodMCErSpectrumOrdinates']
    ))

    twoPeriodDefaultFig.add_trace(go.Scatter(
        x = twoPeriodSpectrum['twoPeriodDesignSpectrumPeriods'],
        y = twoPeriodSpectrum['twoPeriodDesignSpectrumOrdinates']
    ))

    twoPeriodMcerDefaultFig.add_trace(go.Scatter(
        x = twoPeriodMcerSpectrum['twoPeriodMCErSpectrumPeriods'],
        y = twoPeriodMcerSpectrum['twoPeriodMCErSpectrumOrdinates']
    ))

# create csv files for download
@st.cache
def convert_df(df):
    return df.to_csv().encode('utf-8')
    
multiSpectrumCSV = convert_df(multiPeriodSpectrum)
multiMcerCSV = convert_df(multiPeriodMcerSpectrum)
twoPeriodCSV = convert_df(twoPeriodSpectrum)
twoPeriodMcerCSV = convert_df(twoPeriodMcerSpectrum)

# create two columns for layout
firstCol, secondCol = st.columns(2)
with firstCol:
    st.plotly_chart(multiDefaultFig, use_container_width=True)
    st.download_button("Download Multi Period Spectrum", 
                       data=multiSpectrumCSV, 
                       file_name='multiPeriodDesignSpectrum.csv', 
                       mime='text/csv')

    st.plotly_chart(twoPeriodDefaultFig, use_container_width=True)
    st.download_button("Download Two Period Spectrum", 
                       data=twoPeriodCSV, file_name='twoPeriodDesignSpectrum.csv', mime='text/csv')

with secondCol:
    st.plotly_chart(multiMcerDefaultFig, use_container_width=True)
    st.download_button("Download Multi Period MCEr Spectrum", 
                       data=multiMcerCSV, file_name='multiPeriodMCErSpectrum.csv', mime='text/csv')
    st.plotly_chart(twoPeriodMcerDefaultFig, use_container_width=True)
    st.download_button("Download Two Period MCEr Spectrum", 
                       data=twoPeriodMcerCSV, file_name='twoPeriodMCErSpectrum.csv', mime='text/csv')