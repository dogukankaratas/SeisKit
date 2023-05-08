import streamlit as st
from injections.cssInjection import injectCSS

def load_view():

    injectCSS()

    st.markdown("""
    <h2 class="display-6 fw-bold lh-1 mb-3">Application Library</h2>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="row">
        <div class="col-sm-3">
            <div class="card text-center">
                <img class="card-img-top" src="https://i.ibb.co/XCNVKXG/scalePy.png" alt="Card image cap" style="height: 200px;">
                <div class="card-body">
                    <h5 class="card-title">🚀SeisScale</h5>
                    <p class="card-text">Ground Motion Selection and Scaling Tool</p>
                    <a href="/?nav=seisScale" target="_self" class="btn btn-outline-primary btn-sm px-4 me-md-2" role="button" aria-pressed="true">Go To App</a>
                </div>
            </div>
        </div>
        <div class="col-sm-3">
            <div class="card text-center">
                <img class="card-img-top" src="https://i.ibb.co/MZ2bDxS/data-Process.png" alt="Card image cap" style="height: 200px;">
                <div class="card-body">
                    <h5 class="card-title">🌐Earthquake Data Processor</h5>
                    <p class="card-text">Process and Visualize Earthquake Data</p>
                    <a href="/?nav=processorPage" target="_self" class="btn btn-outline-primary btn-sm px-4 me-md-2" role="button" aria-pressed="true">Go To App</a>
                </div>
            </div>
        </div>
        <div class="col-sm-3">
            <div class="card text-center">
                <img class="card-img-top" src="https://i.ibb.co/0qYksZ3/turkey-Map.png" alt="Card image cap" style="height: 200px;">
                <div class="card-body">
                    <h5 class="card-title">🔸TBEC-2018 Response Spectrum Creator</h5>
                    <p class="card-text">Create TBEC-2018 Response Spectrums</p>
                    <a href="/?nav=tbec2018Page" target="_self" class="btn btn-outline-primary btn-sm px-4 me-md-2" role="button" aria-pressed="true">Go To App</a>
                </div>
            </div>
        </div>
        <div class="col-sm-3">
            <div class="card text-center">
                <img class="card-img-top" src="https://i.ibb.co/VHmfkCm/usaMap.png" alt="Card image cap" style="height: 200px;">
                <div class="card-body">
                    <h5 class="card-title">🔹ASCE7-22 Response Spectrum Creator</h5>
                    <p class="card-text">Create ASCE7-22 Response Spectrums</p>
                    <a href="/?nav=asce22Page" target="_self" class="btn btn-outline-primary btn-sm px-4 me-md-2" role="button" aria-pressed="true">Go To App</a>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html = True)
    
    
    