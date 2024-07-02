import streamlit as st
import folium as fl
import math
import pandas as pd
from streamlit_folium import st_folium
import plotly.graph_objects as go
from PIL import Image
import io, base64
import os
import sys
baseName = os.path.basename(__file__)
dirName = os.path.dirname(__file__)
sys.path.append(dirName + r'./')
from functions.tbecResponse.tbecResponseSpectrum import tbecTargetSpectrum

def load_view():

    # set title and logo
    st.markdown("# 🔸TBEC-2018 Response Spectrum Creator")

    # create a function for get position from map
    def get_pos(lat,lng):
        return lat,lng

    # create folium map and zoom in turkey
    m = fl.Map(location=[39, 48], zoom_start=5)
    m.add_child(fl.LatLngPopup())

    # add contour
    img = Image.open('style/assets/afadContour.png')
    b = io.BytesIO()
    img.save(b, format='PNG')
    b64 = base64.b64encode(b.getvalue())
    fl.raster_layers.ImageOverlay(
            image=f'data:image/png;base64,{ b64.decode("utf-8") }',
            bounds=[[35.65, 24.45], [42.65, 45.15]],
            opacity=0.5,
            interactive=False,
            cross_origin=False,
            zindex=1
        ).add_to(m)

    fl.LayerControl().add_to(m)

    # render map
    map = st_folium(m, height=250, width=2000, center=[39, 44], zoom=5)

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

    horizotanlResponseFig.update_layout(showlegend=False, 
                            plot_bgcolor = "#F0F2F6",
                            title = 'TBEC-2018 Horizontal Response Spectrum', title_x=0.4,
                            height = 500
                            )

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

    verticalResponseFig.update_layout(showlegend=False, 
                            plot_bgcolor = "#F0F2F6",
                            title = 'TBEC-2018 Vertical Response Spectrum', title_x=0.4,
                            height = 500
                            )

    # create default table
    spectralTable = pd.DataFrame()
    spectralTable['Spectral Parameters'] = ['SS', 'S1', 'PGA', 'PGV', 'Fs', 'F1', 
                                            'SDs', 'SD1', 'TA', 'TB', 'TL', 'DTS']

    spectralTable['Values'] = ['No Value'] * 12

    # create two columns for layout
    inputCol, graphCol = st.columns([1,2])

    # create input form
    with inputCol:
        st.write("##")
        with st.form('inputForm'):
            latitude = st.number_input("Latitude", 34.25, 42.95, locationData[0], 0.5 , format="%0.6f")
            longitude = st.number_input("Longitude", 24.55, 45.95, locationData[1], 0.5 , format="%0.6f")
            soil = st.selectbox("Soil Type", ('ZA', 'ZB', 'ZC', 'ZD', 'ZE'), 2)
            intensityLevel = st.selectbox("Intensity Level", ["DD1", "DD2", "DD3", "DD4"], 1)
            createButton = st.form_submit_button("Create Response Spectrum")

    if createButton:
        # execute the function for tbec response spectrum
        returnedSpectrumDict = tbecTargetSpectrum(latitude, longitude, soil, intensityLevel)
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
        try:
            horizontalSpectrum = pd.DataFrame()
            horizontalSpectrum['T'] = returnedSpectrumDict['T']
            horizontalSpectrum['Sa'] = returnedSpectrumDict['Sa']

            verticalSpectrum = pd.DataFrame()
            verticalSpectrum['T'] = returnedSpectrumDict['T']
            verticalSpectrum['Sad'] = returnedSpectrumDict['Sad']

            @st.cache_data
            def convert_df(df):
                    return df.to_csv().encode('utf-8')

            horizontalCSV = convert_df(horizontalSpectrum)
            verticalCSV = convert_df(verticalSpectrum)
        except:
            horizontalSpectrum = pd.DataFrame()
            verticalSpectrum = pd.DataFrame()
            @st.cache_data
            def convert_df(df):
                    return df.to_csv().encode('utf-8')

            horizontalCSV = convert_df(horizontalSpectrum)
            verticalCSV = convert_df(verticalSpectrum)

        horizontalTab, verticalTab, tableTab = st.tabs(["Horizontal Spectrum", "Vertical Spectrum", "Spectral Values"])

        with horizontalTab:
            st.plotly_chart(horizotanlResponseFig, use_container_width=True)
            st.download_button("Download Horizontal Response Spectrum", 
                                    data=horizontalCSV, file_name='horizontalSpectrum.csv', mime='text/csv')
        
        with verticalTab:
            st.plotly_chart(verticalResponseFig, use_container_width=True)
            st.download_button("Download Vertical Response Spectrum", 
                                    data=verticalCSV, file_name='verticalSpectrum.csv', mime='text/csv')
        with tableTab:
            st.write('### Spectral Values')
            # inject CSS with markdown
            st.markdown("""
                    <style>
                    thead tr th:first-child {display:none}
                    tbody th {display:none}
                    </style>
                    """, unsafe_allow_html=True)
            st.table(spectralTable)
