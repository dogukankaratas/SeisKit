import streamlit as st
import plotly.graph_objects as go
from functions.eqDataProcess.asciiProcessor import asciiReader
from functions.eqDataProcess.responseCreator import ResponseSpectra
from functions.eqDataProcess.tbecTargetCreator import tbecTargetSpectrum
from functions.eqDataProcess.ariasCreator import ariasIntensityCreator

# set the title of the page and layout
st.markdown("# 🌐Earthquake Data Processor")
firstCol, secondCol = st.columns(2)

# create file uploader
with firstCol:
    uploadedFile = st.file_uploader("Upload File", ['asc'])

# create default figure for filtered acceleration visualization
filteredAccFig = go.Figure()
filteredAccFig.update_xaxes(
    title_text = 'Time (s)',
    showgrid = True,
    showline = False)

filteredAccFig.update_yaxes(
    title_text = 'Acceleration (g)',
    showgrid = True,
    showline = False)

filteredAccFig.update_layout(title = 'Processed Acceleration Data', title_x=0.4)

# create default figure for response spectrum visualization
responseFig = go.Figure()
responseFig.update_xaxes(
                        title_text = 'Period (s)',
                        range = [0,3],
                        showgrid = True,
                        showline = True,
                    )

responseFig.update_yaxes(
                        title_text = 'pSa (g)',
                        showgrid = True,
                        showline = True
                    )

responseFig.update_layout(showlegend=True, 
                          title = 'Response Spectrum', title_x=0.4,
                          legend = dict(
                            yanchor="top",
                            xanchor="right"
                        ))

# create default figure for arias intensity visualization
ariasFig = go.Figure()
ariasFig.update_xaxes(
    title_text = 'Time (s)',
    showgrid = True,
    showline = True,
)

ariasFig.update_yaxes(
    title_text = 'Arias Intensity',
    showgrid = True,
    showline = True,
)    

ariasFig.update_layout(showlegend = True,
                       title = 'Arias Intensity', title_x = 0.4,
                       legend = dict(
                            yanchor="top",
                            y=0.99,
                            xanchor="left",
                            x=0.01
                        ))

# read the uploaded file
rawFile = []
if uploadedFile:
    for data in uploadedFile:
        rawFile.append(data)

    # decide if the uploaded ascii file is for vertical or horizontal
    if uploadedFile.name[-5] == 'E' or uploadedFile.name[-5] == 'N':
        orientation = 'horizontal'
    else:
        orientation = 'vertical'

    # create the response spectrum from uploaded file
    returnedDict = asciiReader(rawFile)
    responseTime, responseAcc = ResponseSpectra(returnedDict['filteredAccList'], returnedDict['sampling'])

    # create target spectrums for DD1 and DD2 from uploaded file
    targetValuesDD1 = tbecTargetSpectrum(returnedDict['latitude'], returnedDict['longitude'], returnedDict['vs30'], "DD1")
    targetValuesDD2 = tbecTargetSpectrum(returnedDict['latitude'], returnedDict['longitude'], returnedDict['vs30'], "DD2")

    # create arias intesity values
    ariasValues = ariasIntensityCreator(returnedDict['filteredAccList'], returnedDict['sampling'])

    # push filtered acceleration to the graphic
    filteredAccFig.add_trace(go.Scatter(
        x = returnedDict['accTime'],
        y = returnedDict['filteredAccList']
    ))

    # push response spectrum to the graphic
    responseFig.add_trace(go.Scatter(
        name = 'Response Spectrum',
        x = responseTime,
        y = responseAcc,
        line=dict(color='gray')
    ))

    # push DD1 target spectrum to the graphic
    responseFig.add_trace(go.Scatter(
        name='DD1 Target Spectrum',
        x = targetValuesDD1['T'],
        y = targetValuesDD1['Sa'],
        line=dict(color='red')
    ))

    # push DD2 target spectrum to the graphic
    responseFig.add_trace(go.Scatter(
        name='DD2 Target Spectrum',
        x = targetValuesDD2['T'],
        y = targetValuesDD2['Sa'],
        line=dict(color='green')
    ))
    
    # push arias intensity values to the 
    ariasFig.add_trace(go.Scatter(
        name = 'Arias Intensity',
        x = ariasValues['ariasTime'][1:-1],
        y = ariasValues['ariasIntesity']
    ))

    ariasFig.add_trace(go.Scatter(
        name = 'Significant Duration',
        x = ariasValues['ariasTime'][ariasValues['timeAriasList']],
        y = ariasValues['ariasIntesity'][ariasValues['timeAriasList']],
        line=dict(color = 'red', width = 2)
    ))

    ariasFig.add_annotation(
        text= f"Earthquake Duration: {round(ariasValues['durationAriasIntensity'][-1],2)} sec.",
        xref="paper", yref="paper",
        y=0.80,
        x=0.01,
        showarrow=False,
         font=dict(
                color="black",
                size=12)
    )

with firstCol:
    st.plotly_chart(responseFig)
with secondCol:
    st.plotly_chart(filteredAccFig)
    st.plotly_chart(ariasFig)