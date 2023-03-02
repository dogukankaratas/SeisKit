import streamlit as st
from st_pages import show_pages, Page, Section, add_page_title

st.set_page_config(layout="wide", page_icon="🪁")

# add_page_title()

show_pages(
    [
        Page("mainPage.py", "Home", "🏛️"),

        Page("apps/scalepy.py", "ScalePy", "🚀"),

        Page("apps/eqDataProcess.py", "Earthquake Data Processor", "🌐"),

        Page("apps/tbecResponse.py", "TBEC-2018 Response Spectrum", "🔸"),

        Page("apps/asceResponse.py", "ASCE7-22 Response Spectrum", "🔹")

    ]
)

st.title("Welcome to SeisKit 👋")

st.markdown("SeisKit is an open-source project which aims to create free and accesible applications for earthquake engineering.")
st.markdown("## Applications")
st.markdown("""
    <div class="card-deck">
        <div class="card">
            <img class="card-img-top" src="https://i.ibb.co/XCNVKXG/scalePy.png" alt="Card image cap">
            <div class="card-body">
                <h5 class="card-title">🚀ScalePy</h5>
                <p class="card-text">Ground Motion Selection and Scaling Tool</p>
                <a href="http://localhost:8501/ScalePy" class="btn btn-outline-primary" >Go To App</a>
            </div>
            <div class="card-footer">
                <small class="text-muted">Updated at 25/02/2023</small>
            </div>
        </div>
        <div class="card">
            <img class="card-img-top" src="https://i.ibb.co/MZ2bDxS/data-Process.png" alt="Card image cap">
            <div class="card-body">
                <h5 class="card-title">🌐Earthquake Data Processor</h5>
                <p class="card-text">Process and visualize your raw earthquake data.</p>
                <a href="http://localhost:8501/ScalePy" class="btn btn-outline-primary" >Go To App</a>
            </div>
            <div class="card-footer">
                <small class="text-muted">Updated at 01/03/2023</small>
            </div>
        </div>
        <div class="card">
            <img class="card-img-top" src="https://i.ibb.co/0qYksZ3/turkey-Map.png" alt="Card image cap">
            <div class="card-body">
                <h5 class="card-title">🔸TBEC-2018 Response Spectrum Creator</h5>
                <p class="card-text">Create response spectrums based on selected location acc. to TBEC-2018.</p>
                <a href="http://localhost:8501/ScalePy" class="btn btn-outline-primary" >Go To App</a>
            </div>
            <div class="card-footer">
                <small class="text-muted">Updated at 01/03/2023</small>
            </div>
        </div>
        <div class="card">
            <img class="card-img-top" src="https://i.ibb.co/VHmfkCm/usaMap.png" alt="Card image cap">
            <div class="card-body">
                <h5 class="card-title">🔹ASCE7-22 Response Spectrum Creator</h5>
                <p class="card-text">Create response spectrums based on selected location acc. to ASCE7-22.</p>
                <a href="http://localhost:8501/ScalePy" class="btn btn-outline-primary" >Go To App</a>
            </div>
            <div class="card-footer">
                <small class="text-muted">Updated at 01/03/2023</small>
            </div>
        </div>
    </div>
""", unsafe_allow_html = True)

st.markdown("""
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">

""", unsafe_allow_html = True)

