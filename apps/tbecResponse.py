import streamlit as st
import folium as fl
import math
import pandas as pd
from streamlit_folium import st_folium
import plotly.graph_objects as go
from functions.tbecResponse.tbecResponseSpectrum import tbecTargetSpectrum
from injections import add_logo

# set title and logo
st.markdown("# 🔸TBEC-2018 Response Spectrum Creator")
add_logo()

# create a function for get position from map
def get_pos(lat,lng):
    return lat,lng

# create folium map and zoom in turkey
m = fl.Map(location=[39, 48], zoom_start=5)
m.add_child(fl.LatLngPopup())
map = st_folium(m, height=250, width=1500, center=[39, 48], zoom=5)

# get location data from click event
locationData = [36.0, 42.0]
if map['last_clicked']:
    clickedData = get_pos(map['last_clicked']['lat'],map['last_clicked']['lng'])
    locationData[0] = clickedData[0]
    locationData[1] = clickedData[1]

# create default figure for horizontal spectrum figure
horizotanlResponseFig = go.Figure()
horizotanlResponseFig.update_xaxes(
                        title_text = 'Period (s)',
                        range = [0,3.5],
                        showgrid = True,
                        showline = True,
                    )

horizotanlResponseFig.update_yaxes(
                        title_text = 'pSa (g)',
                        showgrid = True,
                        showline = True
                    )

horizotanlResponseFig.update_layout(showlegend=True, 
                          plot_bgcolor = "#F0F2F6",
                          title = 'TBEC-2018 Horizontal Response Spectrum', title_x=0.4,
                          height = 500,
                          legend = dict(
                            yanchor="top",
                            xanchor="right"
                        ))

# create default figure for vertical spectrum figure
verticalResponseFig = go.Figure()
verticalResponseFig.update_xaxes(
                        title_text = 'Period (s)',
                        range = [0,3],
                        showgrid = True,
                        showline = True,
                    )

verticalResponseFig.update_yaxes(
                        title_text = 'pSa (g)',
                        showgrid = True,
                        showline = True
                    )

verticalResponseFig.update_layout(showlegend=True, 
                          plot_bgcolor = "#F0F2F6",
                          title = 'TBEC-2018 Vertical Response Spectrum', title_x=0.4,
                          height = 500,
                          legend = dict(
                            yanchor="top",
                            xanchor="right"
                        ))

# create default table
spectralTable = pd.DataFrame()
spectralTable['Spectral Parameters'] = ['SS', 'S1', 'PGA', 'PGV', 'Fs', 'F1', 
                                        'SDs', 'SD1', 'TA', 'TB', 'TL', 'DTS']

spectralTable['Values'] = ['No Value'] * 12

# create two columns for layout
inputCol, graphCol = st.columns([1,2])

# create input form
with inputCol:
    with st.form('inputForm'):
        latitude = st.number_input("Latitude", 34.25, 42.95, locationData[0], 0.5)
        longitude = st.number_input("Longitude", 24.55, 45.95, locationData[1], 0.5)
        soil = st.selectbox("Soil Type", ('ZA', 'ZB', 'ZC', 'ZD', 'ZE'), 2)
        intensityLevel = st.selectbox("Intensity Level", ["DD1", "DD2", "DD3", "DD4"], 1)
        createButton = st.form_submit_button("Create Response Spectrum")

# execute the function for tbec response spectrum
returnedSpectrumDict = tbecTargetSpectrum(latitude, longitude, soil, intensityLevel)

if createButton:
    # push data to the figures
    horizotanlResponseFig.add_trace(go.Scatter(
        x = returnedSpectrumDict['T'],
        y = returnedSpectrumDict['Sa']
    ))

    maxHorizontalAcc = math.ceil(max(returnedSpectrumDict['Sa']))
    horizotanlResponseFig.update_yaxes(
        range = [0, maxHorizontalAcc]
    )

    verticalResponseFig.add_trace(go.Scatter(
        x = returnedSpectrumDict['T'],
        y = returnedSpectrumDict['Sad']
    ))

    maxVerticalAcc = math.ceil(max(returnedSpectrumDict['Sad']))
    verticalResponseFig.update_yaxes(
        range = [0, maxVerticalAcc]
    )

    # read returned spectral values
    returnedValues = []
    returnedValues.append(returnedSpectrumDict['Ss'])
    returnedValues.append(returnedSpectrumDict['S1'])
    returnedValues.append(returnedSpectrumDict['PGA'])
    returnedValues.append(returnedSpectrumDict['PGV'])
    returnedValues.append(returnedSpectrumDict['Fs'])
    returnedValues.append(returnedSpectrumDict['F1'])
    returnedValues.append(returnedSpectrumDict['SDs'])
    returnedValues.append(returnedSpectrumDict['SD1'])
    returnedValues.append(returnedSpectrumDict['TA'])
    returnedValues.append(returnedSpectrumDict['TB'])
    returnedValues.append(returnedSpectrumDict['TL'])
    returnedValues.append(returnedSpectrumDict['DTS'])

    spectralTable['Values'] = returnedValues

# push figures to the layout
with graphCol:
    # add download buttons
    horizontalSpectrum = pd.DataFrame()
    horizontalSpectrum['T'] = returnedSpectrumDict['T']
    horizontalSpectrum['Sa'] = returnedSpectrumDict['Sa']

    verticalSpectrum = pd.DataFrame()
    verticalSpectrum['T'] = returnedSpectrumDict['T']
    verticalSpectrum['Sad'] = returnedSpectrumDict['Sad']

    @st.cache
    def convert_df(df):
        return df.to_csv().encode('utf-8')

    horizontalCSV = convert_df(horizontalSpectrum)
    verticalCSV = convert_df(verticalSpectrum)

    st.plotly_chart(horizotanlResponseFig, use_container_width=True)
    st.download_button("Download Horizontal Response Spectrum", 
                       data=horizontalCSV, file_name='horizontalSpectrum.csv', mime='text/csv')

    st.plotly_chart(verticalResponseFig, use_container_width=True)
    st.download_button("Download Vertical Response Spectrum", 
                       data=verticalCSV, file_name='horizontalSpectrum.csv', mime='text/csv')
    
# push table to the layout
with inputCol:
    # add title
    st.write('###')
    st.write('### Spectral Values')
    # inject CSS with markdown
    st.markdown("""
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """, unsafe_allow_html=True)
    st.table(spectralTable)

