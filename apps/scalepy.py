import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import os
import sys
baseName = os.path.basename(__file__)
dirName = os.path.dirname(__file__)
sys.path.append(dirName + r'./')
from functions.scalepy import scalepyBack
from functions.scalepy import accesAsce

st.markdown("# 🚀ScalePy")

# default empty figure
defaultFig = go.Figure()
defaultFig.update_xaxes(
    title_text = 'Period (sec)',
    range=[0,4],
    tickvals=np.arange(0,4.5,0.5),
    dtick = 1,
    showgrid = True,
    zeroline=True,
    zerolinewidth=1
)

defaultFig.update_yaxes(
    title_text = 'pSa (g)',
    range=[0,3],
    showgrid = True,
    zeroline=True,
    zerolinewidth=1
)

defaultFig.update_layout(showlegend=False, template=None, plot_bgcolor = "#F0F2F6", width=1100,height=600, title_text='No Data', title_x=0.5, legend=dict(
    yanchor="top",
    x = 1,
    xanchor="right"
    ))
    
inputCol, graphCol = st.columns([1, 2.7])


with inputCol:
    responseTab, selectionTab, scalingTab = st.tabs(["Response Spectrum", "Record Filtering", "Scaling"])
    with responseTab:
        responseDefinitionType = st.selectbox("Spectrum Definition", ['TBEC-2018', 'ASCE7-22', 'User-Defined'])
        if responseDefinitionType == 'TBEC-2018':
            with st.form("tbecForm"):
                Ss = st.number_input('Spectral Acceleration at Short Periods (Ss)', value=1.2)
                S1 = st.number_input('Spectral Acceleration at 1 sec (S1)', value=0.25)
                soil = st.selectbox('Soil Type', ('ZA', 'ZB', 'ZC', 'ZD', 'ZE'), 2)
                responseButton = st.form_submit_button('Create Response Spectrum')
        if responseDefinitionType == 'ASCE7-22':
            with st.form("asceForm"):
                responseType = st.selectbox("Spectrum Type", ('Multi Period Design Spectrum', 'Multi Period MCEr Design Spectrum', 'Two Period Design Spectrum', 'Two Period MCEr Design Spectrum'))
                latitude = st.number_input('Latitude of Location', 26.0, 50.0, 32.0, 1.0)
                longitude = st.number_input('Longitude of Location', -125.0, -65.0, -94.0, 1.0)
                asceSoil = st.selectbox("Soil Type", ('A', 'B', 'C', 'D', 'E'), 2)
                asceResponseButton = st.form_submit_button('Create Response Spectrum')
        if responseDefinitionType == 'User-Defined':
            st.info('Please consider the format in the example file.', icon="ℹ️")
            targetDf = scalepyBack.targetSpectrum(0.8, 0.4, "ZC")
            @st.cache
            def convert_df(df):
                return df.to_csv().encode('utf-8')
            exampleCSV = convert_df(targetDf)
            st.download_button("Example CSV file", data=exampleCSV, file_name='exampleSpectrum.csv', mime='text/csv')
            with st.form("userDefinedForm"):
                userDefinedSpectrum = st.file_uploader('Upload Response Spectrum Data', type='csv', accept_multiple_files=False)
                st.set_option('deprecation.showfileUploaderEncoding', False)
                userDefinedSpectrumButton = st.form_submit_button('Create Response Spectrum')

    with selectionTab:
        with st.form("selectionForm"):
            period = st.number_input("Structure Period", 0.0, 10.0, 1.0, 0.1)
            magnitudeRange = st.slider('Magnitude Range', 0.0, 12.0, (3.0, 10.0), step=0.2)
            vs30Range = st.slider('Vs30 Range', 0, 1500, (360, 760), step=10)
            rjbRange = st.slider('RJB Range', 0, 3000, (0, 3000), step=10)
            faultMechanism = st.selectbox('Fault Mechanism', ["Strike - Slip", "Normal", "Reverse", "Oblique", "Reverse - Oblique", "Normal - Oblique"])
            duration575Range = st.slider('%5-%75 Duration Range', 0, 500, (0, 500), step=5)
            duration595Range = st.slider('%5-%95 Duration Range', 0, 500, (0, 500), step=5)
            ariasIntensity = st.slider('Arias Intensity Range', 0, 10, (0, 10), step=1)
            filterButton = st.form_submit_button("Filter Ground Motions")
            numberRecords = st.number_input("Number of Ground Motions to be Scaled", 1, value=11, step=1)
            selectButton = st.form_submit_button("Find Optimum Selected Ground Motions")

    with scalingTab:
        with st.form("scalingForm"):
            spectralOrdinate = st.selectbox("Spectral Ordinate", ["SRSS", "RotD50", "RotD100"])
            targetShift = st.number_input("Target Spectrum Shift", 0.1, value=1.3, step=0.1)
            periodRange = st.slider("Period Range of Interest Coefficients", 0.1, 3.0, (0.2, 1.5), 0.1)
            scaleButton = st.form_submit_button("Perform Amplitude Scaling")

if responseDefinitionType == 'TBEC-2018':
    if responseButton:
        defaultTarget = scalepyBack.targetSpectrum(Ss, S1, soil)
        defaultTarget = defaultTarget.rename(columns={'T': 'Period (sec)', 'Sa': 'pSa (g)'})
        defaultFig = go.Figure()
        defaultFig.add_trace(go.Scatter(x = defaultTarget['Period (sec)'],
                                        y=defaultTarget['pSa (g)'],
                                        name='Response Spectrum', line=dict(color='red')))

        defaultFig.update_xaxes(
            title_text = 'Period (sec)',
            range=[0,4],
            tickvals=np.arange(0,4.5,0.5),
            dtick = 1,
            showgrid = True,
            zeroline=True,
            zerolinewidth=1
        )

        defaultFig.update_yaxes(
            title_text = 'pSa (g)',
            range=[0,3],
            showgrid = True,
            zeroline=True,
            zerolinewidth=1
        )

        defaultFig.update_layout(showlegend=True, template=None, plot_bgcolor = "#F0F2F6", width=1100,height=600, 
                                title_text='Response Spectrum', title_x=0.5, legend=dict(
                                                                yanchor="top",
                                                                x = 1,
                                                                xanchor="right")
                                )

if responseDefinitionType == 'ASCE7-22':
    if asceResponseButton:
        initialResponse = scalepyBack.targetSpectrum(0.8, 0.4, "ZC")
        t = initialResponse['T']

        if responseType == 'Multi Period Design Spectrum':
            asceInit = accesAsce.getAsceDataMulti(latitude, longitude, 'III', asceSoil, 'Call')
            targetAsce = pd.DataFrame()
            targetAsce['multiPeriodDesignSpectrumPeriods'] = t
            targetAsce['multiPeriodDesignSpectrumOrdinates'] = [x*9.81 for x in np.interp(t, asceInit['multiPeriodDesignSpectrumPeriods'], asceInit['multiPeriodDesignSpectrumOrdinates'])]
            targetAsce = targetAsce.rename(columns={'multiPeriodDesignSpectrumPeriods': 'T', 'multiPeriodDesignSpectrumOrdinates': 'Sa'})

        elif responseType == 'Multi Period MCEr Design Spectrum':
            asceInit = accesAsce.getAsceDataMultiMCEr(latitude, longitude, 'III', asceSoil, 'Call')
            targetAsce = pd.DataFrame()
            targetAsce['multiPeriodMCErSpectrumPeriods'] = t
            targetAsce['multiPeriodMCErSpectrumOrdinates'] = [x*9.81 for x in np.interp(t, asceInit['multiPeriodMCErSpectrumPeriods'], asceInit['multiPeriodMCErSpectrumOrdinates'])]
            targetAsce = targetAsce.rename(columns={'multiPeriodMCErSpectrumPeriods': 'T', 'multiPeriodMCErSpectrumOrdinates': 'Sa'})

        elif responseType == 'Two Period Design Spectrum':
            asceInit = accesAsce.getAsceDataTwo(latitude, longitude, 'III', asceSoil, 'Call')
            targetAsce = pd.DataFrame()
            targetAsce['twoPeriodDesignSpectrumPeriods'] = t
            targetAsce['twoPeriodDesignSpectrumOrdinates'] = [x*9.81 for x in np.interp(t, asceInit['twoPeriodDesignSpectrumPeriods'], asceInit['twoPeriodDesignSpectrumOrdinates'])]
            targetAsce = targetAsce.rename(columns={'twoPeriodDesignSpectrumPeriods': 'T', 'twoPeriodDesignSpectrumOrdinates': 'Sa'})

        elif responseType == 'Two Period MCEr Design Spectrum':
            asceInit = accesAsce.getAsceDataTwoMCEr(latitude, longitude, 'III', asceSoil, 'Call')
            targetAsce = pd.DataFrame()
            targetAsce['twoPeriodMCErSpectrumPeriods'] = t
            targetAsce['twoPeriodMCErSpectrumOrdinates'] = [x*9.81 for x in np.interp(t, asceInit['twoPeriodMCErSpectrumPeriods'], asceInit['twoPeriodMCErSpectrumOrdinates'])]
            targetAsce = targetAsce.rename(columns={'twoPeriodMCErSpectrumPeriods': 'T', 'twoPeriodMCErSpectrumOrdinates': 'Sa'})

        defaultTarget = targetAsce

        defaultTarget = defaultTarget.rename(columns={'T': 'Period (sec)', 'Sa': 'pSa (g)'})
        defaultFig = go.Figure()
        defaultFig.add_trace(go.Scatter(x = defaultTarget['Period (sec)'],
                                        y=defaultTarget['pSa (g)'],
                                        name='Response Spectrum', line=dict(color='red')))

        defaultFig.update_xaxes(
            title_text = 'Period (sec)',
            range=[0,4],
            tickvals=np.arange(0,4.5,0.5),
            dtick = 1,
            showgrid = True,
            zeroline=True,
            zerolinewidth=1
        )

        defaultFig.update_yaxes(
            title_text = 'pSa (g)',
            range=[0,3],
            showgrid = True,
            zeroline=True,
            zerolinewidth=1
        )

        defaultFig.update_layout(showlegend=True, template=None, plot_bgcolor = "#F0F2F6", width=1100,height=600, 
                                title_text='Response Spectrum', title_x=0.5, legend=dict(
                                                                yanchor="top",
                                                                x = 1,
                                                                xanchor="right")
                                )
if responseDefinitionType == 'User-Defined':
    if userDefinedSpectrumButton:
        if userDefinedSpectrum is None:
            st.error('No file has uploaded.', icon="🚨")
        else:
            spectrumData = pd.read_csv(userDefinedSpectrum)
            spectrumData = spectrumData.loc[:, ~spectrumData.columns.str.contains('^Unnamed')]
            defaultTarget = spectrumData
            defaultTarget = defaultTarget.rename(columns={'T': 'Period (sec)', 'Sa': 'pSa (g)'})
            defaultFig = go.Figure()
            defaultFig.add_trace(go.Scatter(x = defaultTarget['Period (sec)'],
                                            y=defaultTarget['pSa (g)'],
                                            name='Response Spectrum', line=dict(color='red')))

            defaultFig.update_xaxes(
                title_text = 'Period (sec)',
                range=[0,4],
                tickvals=np.arange(0,4.5,0.5),
                dtick = 1,
                showgrid = True,
                zeroline=True,
                zerolinewidth=1
            )

            defaultFig.update_yaxes(
                title_text = 'pSa (g)',
                range=[0,3],
                showgrid = True,
                zeroline=True,
                zerolinewidth=1
            )

            defaultFig.update_layout(showlegend=True, template=None, plot_bgcolor = "#F0F2F6", width=1100,height=600, 
                                    title_text='Response Spectrum', title_x=0.5, legend=dict(
                                                                    yanchor="top",
                                                                    x = 1,
                                                                    xanchor="right")
                                    )

if filterButton:

    def tupleToStr(tup):
        return'{value1} {value2}'.format(value1= tup[0], value2 = tup[1])

    if responseDefinitionType == 'TBEC-2018':
        selectedTarget = scalepyBack.targetSpectrum(Ss, S1, soil)

    elif responseDefinitionType == 'ASCE7-22':

        initialResponse = scalepyBack.targetSpectrum(0.8, 0.4, "ZC")
        t = initialResponse['T']

        if responseType == 'Multi Period Design Spectrum':
            asceInit = accesAsce.getAsceDataMulti(latitude, longitude, 'III', asceSoil, 'Call')
            targetAsce = pd.DataFrame()
            targetAsce['multiPeriodDesignSpectrumPeriods'] = t
            targetAsce['multiPeriodDesignSpectrumOrdinates'] = [x*9.81 for x in np.interp(t, asceInit['multiPeriodDesignSpectrumPeriods'], asceInit['multiPeriodDesignSpectrumOrdinates'])]
            targetAsce = targetAsce.rename(columns={'multiPeriodDesignSpectrumPeriods': 'T', 'multiPeriodDesignSpectrumOrdinates': 'Sa'})

        elif responseType == 'Multi Period MCEr Design Spectrum':
            asceInit = accesAsce.getAsceDataMultiMCEr(latitude, longitude, 'III', asceSoil, 'Call')
            targetAsce = pd.DataFrame()
            targetAsce['multiPeriodMCErSpectrumPeriods'] = t
            targetAsce['multiPeriodMCErSpectrumOrdinates'] = [x*9.81 for x in np.interp(t, asceInit['multiPeriodMCErSpectrumPeriods'], asceInit['multiPeriodMCErSpectrumOrdinates'])]
            targetAsce = targetAsce.rename(columns={'multiPeriodMCErSpectrumPeriods': 'T', 'multiPeriodMCErSpectrumOrdinates': 'Sa'})

        elif responseType == 'Two Period Design Spectrum':
            asceInit = accesAsce.getAsceDataTwo(latitude, longitude, 'III', asceSoil, 'Call')
            targetAsce = pd.DataFrame()
            targetAsce['twoPeriodDesignSpectrumPeriods'] = t
            targetAsce['twoPeriodDesignSpectrumOrdinates'] = [x*9.81 for x in np.interp(t, asceInit['twoPeriodDesignSpectrumPeriods'], asceInit['twoPeriodDesignSpectrumOrdinates'])]
            targetAsce = targetAsce.rename(columns={'twoPeriodDesignSpectrumPeriods': 'T', 'twoPeriodDesignSpectrumOrdinates': 'Sa'})

        elif responseType == 'Two Period MCEr Design Spectrum':
            asceInit = accesAsce.getAsceDataTwoMCEr(latitude, longitude, 'III', asceSoil, 'Call')
            targetAsce = pd.DataFrame()
            targetAsce['twoPeriodMCErSpectrumPeriods'] = t
            targetAsce['twoPeriodMCErSpectrumOrdinates'] = [x*9.81 for x in np.interp(t, asceInit['twoPeriodMCErSpectrumPeriods'], asceInit['twoPeriodMCErSpectrumOrdinates'])]
            targetAsce = targetAsce.rename(columns={'twoPeriodMCErSpectrumPeriods': 'T', 'twoPeriodMCErSpectrumOrdinates': 'Sa'})

        selectedTarget = targetAsce
    
    elif responseDefinitionType == 'User-Defined':
        if userDefinedSpectrum is None:
            st.error('No file has uploaded.', icon="🚨")
        else:
            spectrumData = pd.read_csv(userDefinedSpectrum)
            spectrumData = spectrumData.loc[:, ~spectrumData.columns.str.contains('^Unnamed')]
        selectedTarget = spectrumData


    selected_keys, eqe_selected_x, eqe_selected_y, rsn_selected, t, eqe_s = scalepyBack.recordSelection(tupleToStr(magnitudeRange), 
                                                                                             tupleToStr(vs30Range), 
                                                                                             tupleToStr(rjbRange), 
                                                                                             faultMechanism, 
                                                                                             tupleToStr(duration575Range), 
                                                                                             tupleToStr(duration595Range), 
                                                                                             tupleToStr(ariasIntensity), 
                                                                                             selectedTarget, 
                                                                                             "Any", 
                                                                                             period,
                                                                                             numberRecords)
    defaultFig = go.Figure()
    for name in rsn_selected:
        defaultFig.add_trace(go.Scatter(x = t,
                                    y=eqe_selected_x[name], line=dict(color='gray'), showlegend=False))
        defaultFig.add_trace(go.Scatter(x = t,
                                        y=eqe_selected_y[name], line=dict(color='gray'), showlegend=False))

    defaultFig.add_trace(go.Scatter(x = selectedTarget['T'],
                                    y=selectedTarget['Sa'],
                                    name='Response Spectrum', line=dict(color='red')))

    defaultFig.update_layout(showlegend=True, template=None, plot_bgcolor = "#F0F2F6", width=1100,height=600, 
                             title_text='Filtered Records', title_x=0.5, legend=dict(
                                                            yanchor="top",
                                                            x = 1,
                                                            xanchor="right")
                            )

    defaultFig.update_xaxes(
            title_text = 'Period (sec)',
            range=[0,4],
            tickvals=np.arange(0,4.5,0.5),
            dtick = 1,
            showgrid = True,
            zeroline=True,
            zerolinewidth=1
    )

    defaultFig.update_yaxes(
        title_text = 'pSa (g)',
        range=[0,3],
        showgrid = True,
        zeroline=True,
        zerolinewidth=1
        )

    defaultFig.add_trace(go.Scatter(
        x = [None],
        y = [None],
        mode = 'lines',
        name = "Filtered Records",
        line=dict(color='gray')
    ))

if selectButton:

    def tupleToStr(tup):
        return'{value1} {value2}'.format(value1= tup[0], value2 = tup[1])

    if responseDefinitionType == 'TBEC-2018':
        selectedTarget = scalepyBack.targetSpectrum(Ss, S1, soil)

    if responseDefinitionType == 'ASCE7-22':

        initialResponse = scalepyBack.targetSpectrum(0.8, 0.4, "ZC")
        t = initialResponse['T']

        if responseType == 'Multi Period Design Spectrum':
            asceInit = accesAsce.getAsceDataMulti(latitude, longitude, 'III', asceSoil, 'Call')
            targetAsce = pd.DataFrame()
            targetAsce['multiPeriodDesignSpectrumPeriods'] = t
            targetAsce['multiPeriodDesignSpectrumOrdinates'] = [x*9.81 for x in np.interp(t, asceInit['multiPeriodDesignSpectrumPeriods'], asceInit['multiPeriodDesignSpectrumOrdinates'])]
            targetAsce = targetAsce.rename(columns={'multiPeriodDesignSpectrumPeriods': 'T', 'multiPeriodDesignSpectrumOrdinates': 'Sa'})

        elif responseType == 'Multi Period MCEr Design Spectrum':
            asceInit = accesAsce.getAsceDataMultiMCEr(latitude, longitude, 'III', asceSoil, 'Call')
            targetAsce = pd.DataFrame()
            targetAsce['multiPeriodMCErSpectrumPeriods'] = t
            targetAsce['multiPeriodMCErSpectrumOrdinates'] = [x*9.81 for x in np.interp(t, asceInit['multiPeriodMCErSpectrumPeriods'], asceInit['multiPeriodMCErSpectrumOrdinates'])]
            targetAsce = targetAsce.rename(columns={'multiPeriodMCErSpectrumPeriods': 'T', 'multiPeriodMCErSpectrumOrdinates': 'Sa'})

        elif responseType == 'Two Period Design Spectrum':
            asceInit = accesAsce.getAsceDataTwo(latitude, longitude, 'III', asceSoil, 'Call')
            targetAsce = pd.DataFrame()
            targetAsce['twoPeriodDesignSpectrumPeriods'] = t
            targetAsce['twoPeriodDesignSpectrumOrdinates'] = [x*9.81 for x in np.interp(t, asceInit['twoPeriodDesignSpectrumPeriods'], asceInit['twoPeriodDesignSpectrumOrdinates'])]
            targetAsce = targetAsce.rename(columns={'twoPeriodDesignSpectrumPeriods': 'T', 'twoPeriodDesignSpectrumOrdinates': 'Sa'})

        elif responseType == 'Two Period MCEr Design Spectrum':
            asceInit = accesAsce.getAsceDataTwoMCEr(latitude, longitude, 'III', asceSoil, 'Call')
            targetAsce = pd.DataFrame()
            targetAsce['twoPeriodMCErSpectrumPeriods'] = t
            targetAsce['twoPeriodMCErSpectrumOrdinates'] = [x*9.81 for x in np.interp(t, asceInit['twoPeriodMCErSpectrumPeriods'], asceInit['twoPeriodMCErSpectrumOrdinates'])]
            targetAsce = targetAsce.rename(columns={'twoPeriodMCErSpectrumPeriods': 'T', 'twoPeriodMCErSpectrumOrdinates': 'Sa'})

        selectedTarget = targetAsce

    elif responseDefinitionType == 'User-Defined':
        if userDefinedSpectrum is None:
            st.error('No file has uploaded.', icon="🚨")
        else:
            spectrumData = pd.read_csv(userDefinedSpectrum)
            spectrumData = spectrumData.loc[:, ~spectrumData.columns.str.contains('^Unnamed')]
        selectedTarget = spectrumData

    selected_keys, eqe_selected_x, eqe_selected_y, rsn_selected, t, eqe_s = scalepyBack.recordSelection(tupleToStr(magnitudeRange), 
                                                                                             tupleToStr(vs30Range), 
                                                                                             tupleToStr(rjbRange), 
                                                                                             faultMechanism, 
                                                                                             tupleToStr(duration575Range), 
                                                                                             tupleToStr(duration595Range), 
                                                                                             tupleToStr(ariasIntensity), 
                                                                                             selectedTarget, 
                                                                                             "Any", 
                                                                                             period,
                                                                                             numberRecords)
    defaultFig = go.Figure()
    for name in selected_keys:
        defaultFig.add_trace(go.Scatter(x = t,
                                    y=eqe_selected_x[name], line=dict(color='gray'), showlegend=False))
        defaultFig.add_trace(go.Scatter(x = t,
                                        y=eqe_selected_y[name], line=dict(color='gray'), showlegend=False))

    defaultFig.add_trace(go.Scatter(x = selectedTarget['T'],
                                    y=selectedTarget['Sa'],
                                    name='Response Spectrum', line=dict(color='red')))

    defaultFig.update_layout(showlegend=True, template=None, plot_bgcolor = "#F0F2F6", width=1100,height=600, 
                             title_text='Optimum Selected Records', title_x=0.5, legend=dict(
                                                            yanchor="top",
                                                            x = 1,
                                                            xanchor="right")
                            )

    defaultFig.update_xaxes(
            title_text = 'Period (sec)',
            range=[0,4],
            tickvals=np.arange(0,4.5,0.5),
            dtick = 1,
            showgrid = True,
            zeroline=True,
            zerolinewidth=1
    )

    defaultFig.update_yaxes(
        title_text = 'pSa (g)',
        range=[0,3],
        showgrid = True,
        zeroline=True,
        zerolinewidth=1
        )

    defaultFig.add_trace(go.Scatter(
        x = [None],
        y = [None],
        mode = 'lines',
        name = "Selected Records",
        line=dict(color='gray')
    ))

if scaleButton:

    def tupleToStr(tup):
        return'{value1} {value2}'.format(value1= tup[0], value2 = tup[1])

    if responseDefinitionType == 'TBEC-2018':
        selectedTarget = scalepyBack.targetSpectrum(Ss, S1, soil)

    if responseDefinitionType == 'ASCE7-22':

        initialResponse = scalepyBack.targetSpectrum(0.8, 0.4, "ZC")
        t = initialResponse['T']

        if responseType == 'Multi Period Design Spectrum':
            asceInit = accesAsce.getAsceDataMulti(latitude, longitude, 'III', asceSoil, 'Call')
            targetAsce = pd.DataFrame()
            targetAsce['multiPeriodDesignSpectrumPeriods'] = t
            targetAsce['multiPeriodDesignSpectrumOrdinates'] = [x*9.81 for x in np.interp(t, asceInit['multiPeriodDesignSpectrumPeriods'], asceInit['multiPeriodDesignSpectrumOrdinates'])]
            targetAsce = targetAsce.rename(columns={'multiPeriodDesignSpectrumPeriods': 'T', 'multiPeriodDesignSpectrumOrdinates': 'Sa'})

        elif responseType == 'Multi Period MCEr Design Spectrum':
            asceInit = accesAsce.getAsceDataMultiMCEr(latitude, longitude, 'III', asceSoil, 'Call')
            targetAsce = pd.DataFrame()
            targetAsce['multiPeriodMCErSpectrumPeriods'] = t
            targetAsce['multiPeriodMCErSpectrumOrdinates'] = [x*9.81 for x in np.interp(t, asceInit['multiPeriodMCErSpectrumPeriods'], asceInit['multiPeriodMCErSpectrumOrdinates'])]
            targetAsce = targetAsce.rename(columns={'multiPeriodMCErSpectrumPeriods': 'T', 'multiPeriodMCErSpectrumOrdinates': 'Sa'})

        elif responseType == 'Two Period Design Spectrum':
            asceInit = accesAsce.getAsceDataTwo(latitude, longitude, 'III', asceSoil, 'Call')
            targetAsce = pd.DataFrame()
            targetAsce['twoPeriodDesignSpectrumPeriods'] = t
            targetAsce['twoPeriodDesignSpectrumOrdinates'] = [x*9.81 for x in np.interp(t, asceInit['twoPeriodDesignSpectrumPeriods'], asceInit['twoPeriodDesignSpectrumOrdinates'])]
            targetAsce = targetAsce.rename(columns={'twoPeriodDesignSpectrumPeriods': 'T', 'twoPeriodDesignSpectrumOrdinates': 'Sa'})

        elif responseType == 'Two Period MCEr Design Spectrum':
            asceInit = accesAsce.getAsceDataTwoMCEr(latitude, longitude, 'III', asceSoil, 'Call')
            targetAsce = pd.DataFrame()
            targetAsce['twoPeriodMCErSpectrumPeriods'] = t
            targetAsce['twoPeriodMCErSpectrumOrdinates'] = [x*9.81 for x in np.interp(t, asceInit['twoPeriodMCErSpectrumPeriods'], asceInit['twoPeriodMCErSpectrumOrdinates'])]
            targetAsce = targetAsce.rename(columns={'twoPeriodMCErSpectrumPeriods': 'T', 'twoPeriodMCErSpectrumOrdinates': 'Sa'})

        selectedTarget = targetAsce

    elif responseDefinitionType == 'User-Defined':
        if userDefinedSpectrum is None:
            st.error('No file has uploaded.', icon="🚨")
        else:
            spectrumData = pd.read_csv(userDefinedSpectrum)
            spectrumData = spectrumData.loc[:, ~spectrumData.columns.str.contains('^Unnamed')]
        selectedTarget = spectrumData
    
    selected_keys, eqe_selected_x, eqe_selected_y, rsn_selected, t, eqe_s = scalepyBack.recordSelection(tupleToStr(magnitudeRange), 
                                                                                             tupleToStr(vs30Range), 
                                                                                             tupleToStr(rjbRange), 
                                                                                             faultMechanism, 
                                                                                             tupleToStr(duration575Range), 
                                                                                             tupleToStr(duration595Range), 
                                                                                             tupleToStr(ariasIntensity), 
                                                                                             selectedTarget, 
                                                                                             "Any", 
                                                                                             period,
                                                                                             numberRecords)
    
    if spectralOrdinate == "SRSS":

        sf_dict, multiplied_selected_x, multiplied_selected_y, geo_mean_1st_scaled_df, srss_mean_df, srss_mean_scaled_df = scalepyBack.amplitudeScaling(selected_keys, selectedTarget, period, targetShift, periodRange[0], periodRange[1], 'srss')

        defaultFig = go.Figure()
        for name in selected_keys:
            defaultFig.add_trace(go.Scatter(x = t,
                                        y= eqe_selected_x[name], line=dict(color='gray'), showlegend=False))
            defaultFig.add_trace(go.Scatter(x = t,
                                            y = eqe_selected_y[name], line=dict(color='gray'), showlegend=False))

        defaultFig.add_trace(go.Scatter(x = selectedTarget['T'],
                                        y = selectedTarget['Sa'],
                                        name='Response Spectrum', line=dict(color='red', dash='dash')))

        defaultFig.add_trace(go.Scatter(x = selectedTarget['T'],
                                        y = selectedTarget['Sa']*targetShift,
                                        name='Shifted Response Spectrum', line=dict(color='red')))

        defaultFig.add_trace(go.Scatter(x = t,
                                        y = geo_mean_1st_scaled_df[ "Mean"],
                                        name='Geometric Mean Scaled', line=dict(color='blue')))

        defaultFig.add_trace(go.Scatter(x = t,
                                        y = srss_mean_df[ "Mean"],
                                        name='SRSS Scaled', line=dict(color='black', dash='dash')))

        defaultFig.add_trace(go.Scatter(x = t,
                                        y = srss_mean_scaled_df[ "Mean"],
                                        name='SRSS Mean Scaled', line=dict(color='black')))

        defaultFig.update_layout(showlegend=True, template=None, plot_bgcolor = "#F0F2F6", width=1100,height=600, 
                             title_text='Scaled Ground Motions', title_x=0.5, legend=dict(
                                                            yanchor="top",
                                                            x = 1,
                                                            xanchor="right")
                            )

        defaultFig.update_xaxes(
                title_text = 'Period (sec)',
                range=[0,4],
                tickvals=np.arange(0,4.5,0.5),
                dtick = 1,
                showgrid = True,
                zeroline=True,
                zerolinewidth=1
                )

        defaultFig.update_yaxes(
            title_text = 'pSa (g)',
            range=[0,max(srss_mean_scaled_df[ "Mean"]) + 1],
            showgrid = True,
            zeroline=True,
            zerolinewidth=1
    )

        defaultFig.add_trace(go.Scatter(
            x = [None],
            y = [None],
            mode = 'lines',
            name = "Selected Records",
            line=dict(color='gray')
        ))

        defaultFig.add_vrect(x0=periodRange[0]*period, x1=periodRange[1]*period, 
              fillcolor="yellow", opacity=0.1, line_width=0)

    if spectralOrdinate == "RotD50":
        sf_dict, multiplied_selected_x, multiplied_selected_y, geo_mean_1st_scaled_df, rotd50_mean_df, rotd50_mean_scaled_df = scalepyBack.amplitudeScaling(selected_keys, selectedTarget, period, targetShift, periodRange[0], periodRange[1], 'rotd50')

        defaultFig = go.Figure()
        for name in selected_keys:
            defaultFig.add_trace(go.Scatter(x = t,
                                        y= eqe_selected_x[name], line=dict(color='gray'), showlegend=False))
        defaultFig.add_trace(go.Scatter(x = t,
                                        y = eqe_selected_y[name], line=dict(color='gray'), showlegend=False))

        defaultFig.add_trace(go.Scatter(x = selectedTarget['T'],
                                        y = selectedTarget['Sa'],
                                        name='Response Spectrum', line=dict(color='red', dash='dash')))

        defaultFig.add_trace(go.Scatter(x = selectedTarget['T'],
                                        y = selectedTarget['Sa']*targetShift,
                                        name='Shifted Response Spectrum', line=dict(color='red')))

        defaultFig.add_trace(go.Scatter(x = t,
                                        y = geo_mean_1st_scaled_df[ "Mean"],
                                        name='Geometric Mean Scaled', line=dict(color='blue')))

        defaultFig.add_trace(go.Scatter(x = t,
                                        y = rotd50_mean_df[ "Mean"],
                                        name='RotD50 Scaled', line=dict(color='black', dash='dash')))

        defaultFig.add_trace(go.Scatter(x = t,
                                        y = rotd50_mean_scaled_df[ "Mean"],
                                        name='RotD50 Mean Scaled', line=dict(color='black')))

        defaultFig.update_layout(showlegend=True, template=None, plot_bgcolor = "#F0F2F6", width=1100,height=600, 
                             title_text='Scaled Ground Motions', title_x=0.5, legend=dict(
                                                            yanchor="top",
                                                            x = 1,
                                                            xanchor="right")
                            )

        defaultFig.update_xaxes(
                title_text = 'Period (sec)',
                range=[0,4],
                tickvals=np.arange(0,4.5,0.5),
                dtick = 1,
                showgrid = True,
                zeroline=True,
                zerolinewidth=1
    )

        defaultFig.update_yaxes(
            title_text = 'pSa (g)',
            range=[0,max(rotd50_mean_scaled_df[ "Mean"]) + 1],
            showgrid = True,
            zeroline=True,
            zerolinewidth=1
            )

        defaultFig.add_trace(go.Scatter(
            x = [None],
            y = [None],
            mode = 'lines',
            name = "Selected Records",
            line=dict(color='gray')
        ))

        defaultFig.add_vrect(x0=periodRange[0]*period, x1=periodRange[1]*period, 
              fillcolor="yellow", opacity=0.1, line_width=0)

    if spectralOrdinate == "RotD100":
        sf_dict, multiplied_selected_x, multiplied_selected_y, geo_mean_1st_scaled_df, rotd100_mean_df, rotd100_mean_scaled_df = scalepyBack.amplitudeScaling(selected_keys, selectedTarget, period, targetShift, periodRange[0], periodRange[1], 'rotd100')

        defaultFig = go.Figure()
        for name in selected_keys:
            defaultFig.add_trace(go.Scatter(x = t,
                                        y= eqe_selected_x[name], line=dict(color='gray'), showlegend=False))
        defaultFig.add_trace(go.Scatter(x = t,
                                        y = eqe_selected_y[name], line=dict(color='gray'), showlegend=False))

        defaultFig.add_trace(go.Scatter(x = selectedTarget['T'],
                                        y = selectedTarget['Sa'],
                                        name='Response Spectrum', line=dict(color='red', dash='dash')))

        defaultFig.add_trace(go.Scatter(x = selectedTarget['T'],
                                        y = selectedTarget['Sa']*targetShift,
                                        name='Shifted Response Spectrum', line=dict(color='red')))

        defaultFig.add_trace(go.Scatter(x = t,
                                        y = geo_mean_1st_scaled_df[ "Mean"],
                                        name='Geometric Mean Scaled', line=dict(color='blue')))

        defaultFig.add_trace(go.Scatter(x = t,
                                        y = rotd100_mean_df[ "Mean"],
                                        name='RotD100 Scaled', line=dict(color='black', dash='dash')))

        defaultFig.add_trace(go.Scatter(x = t,
                                        y = rotd100_mean_scaled_df[ "Mean"],
                                        name='RotD100 Mean Scaled', line=dict(color='black')))

        defaultFig.update_layout(showlegend=True, template=None, plot_bgcolor = "#F0F2F6", width=1100,height=600, 
                             title_text='Scaled Ground Motions', title_x=0.5, legend=dict(
                                                            yanchor="top",
                                                            x = 1,
                                                            xanchor="right")
                            )

        defaultFig.update_xaxes(
                title_text = 'Period (sec)',
                range=[0,4],
                tickvals=np.arange(0,4.5,0.5),
                dtick = 1,
                showgrid = True,
                zeroline=True,
                zerolinewidth=1
    )

        defaultFig.update_yaxes(
            title_text = 'pSa (g)',
            range=[0,max(rotd100_mean_scaled_df[ "Mean"]) +1],
            showgrid = True,
            zeroline=True,
            zerolinewidth=1
    )

        defaultFig.add_trace(go.Scatter(
            x = [None],
            y = [None],
            mode = 'lines',
            name = "Selected Records",
            line=dict(color='gray')
        ))
        
        defaultFig.add_vrect(x0=periodRange[0]*period, x1=periodRange[1]*period, 
              fillcolor="yellow", opacity=0.1, line_width=0)

with graphCol:
    st.plotly_chart(defaultFig, use_container_width=True)

if selectButton:
    defaultFrame = pd.DataFrame(columns=["Record Sequence Number", "Earthquake Name", "Station Name", "Scale Factor"], index=pd.RangeIndex(start=1, stop = numberRecords + 1, name='index'))
    eqe_s_filtered = eqe_s[ eqe_s["RecordSequenceNumber"].isin(selected_keys)]
    defaultFrame["Earthquake Name"] = eqe_s_filtered["EarthquakeName"].to_list()
    defaultFrame["Station Name"] = eqe_s_filtered["StationName"].to_list()
    defaultFrame["Record Sequence Number"] = selected_keys
    del defaultFrame['Scale Factor']
    with graphCol:
        st.table(defaultFrame)

if scaleButton:

    defaultFrame = pd.DataFrame(columns=["Record Sequence Number", "Earthquake Name", "Station Name", "Scale Factor"], index=pd.RangeIndex(start=1, stop = numberRecords + 1, name='index'))
    eqe_s_filtered = eqe_s[ eqe_s["RecordSequenceNumber"].isin(selected_keys)]
    defaultFrame["Earthquake Name"] = eqe_s_filtered["EarthquakeName"].to_list()
    defaultFrame["Station Name"] = eqe_s_filtered["StationName"].to_list()
    defaultFrame["Record Sequence Number"] = selected_keys

    if spectralOrdinate == "SRSS":

        sf_dict, multiplied_selected_x, multiplied_selected_y, geo_mean_1st_scaled_df, srss_mean_df, srss_mean_scaled_df = scalepyBack.amplitudeScaling(selected_keys, selectedTarget, period, targetShift, periodRange[0], periodRange[1], 'srss')
        defaultFrame["Scale Factor"] = list(sf_dict.values())
        with graphCol:
            st.table(defaultFrame)

    if spectralOrdinate == "RotD50":

        sf_dict, multiplied_selected_x, multiplied_selected_y, geo_mean_1st_scaled_df, rotd50_mean_df, rotd50_mean_scaled_df = scalepyBack.amplitudeScaling(selected_keys, selectedTarget, period, targetShift, periodRange[0], periodRange[1], 'rotd50')
        defaultFrame["Scale Factor"] = list(sf_dict.values())
        with graphCol:
            st.table(defaultFrame)

    if spectralOrdinate == "RotD100":
        sf_dict, multiplied_selected_x, multiplied_selected_y, geo_mean_1st_scaled_df, rotd100_mean_df, rotd100_mean_scaled_df = scalepyBack.amplitudeScaling(selected_keys, selectedTarget, period, targetShift, periodRange[0], periodRange[1], 'rotd100')
        defaultFrame["Scale Factor"] = list(sf_dict.values())
        with graphCol:
            st.table(defaultFrame)