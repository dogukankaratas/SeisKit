import streamlit as st
from st_pages import show_pages, Page
from injections import addLogo, addBootstrap, zeroPadding

# set page config and logo
st.set_page_config(layout="wide", page_icon="🪁")
# add injections
addLogo()
addBootstrap()
zeroPadding()

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
            <div class="card-body ">
                <h5 class="card-title justify-content-center">🚀ScalePy</h5>
                <p class="card-text">Ground Motion Selection and Scaling Tool</p>
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
            </div>
            <div class="card-footer">
                <small class="text-muted">Updated at 01/03/2023</small>
            </div>
        </div>
    </div>
""", unsafe_allow_html = True)
