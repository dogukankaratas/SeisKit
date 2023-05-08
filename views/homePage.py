import streamlit as st
import base64
from injections.cssInjection import injectCSS

def load_view():
    # import bootstrap 5
    st.markdown("""
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-KK94CHFLLe+nY2dmCWGMq91rCGa5gtU4mk92HdvYe+M/SXH301p5ILy+dN9+nJOZ" crossorigin="anonymous">
    """, unsafe_allow_html=True)

    # read animation file
    file_ = open("style/assets/animation.gif", "rb") 
    contents = file_.read() 
    data_url = base64.b64encode(contents).decode("utf-8") 
    file_.close() 

    # hero section
    st.markdown(f"""
        <section id="title">
            <div class="container col-xxl-8 px-4">
                <div class="row flex-lg-row-reverse align-items-center g-5 py-2">
                    <div class="col-10 col-sm-8 col-lg-6">
                        <div id="logoPlot">
                            <img src="data:image/gif;base64,{data_url}" alt="heroGif" style="height: 400px; margin-top: 0px;">
                        </div>
                    </div>
                    <div class="col-lg-6">
                        <h1 class="display-6 fw-bold lh-1 mb-3">Earthquake Engineering Web Applications</h1>
                        <p class="lead"> Quickly access web applications for earthquake engineering developed by open source community.</p>
                        <p class="lead"> For free.</p>
                        <div class="d-grid gap-2 d-md-flex justify-content-md-start">
                            <a href="https://github.com/dogukankaratas/SeisKit" class="btn btn-outline-primary btn-sm px-4 me-md-2" role="button" aria-pressed="true">Source Code</a>
                            <a href="" class="btn btn-outline-primary btn-sm px-4 me-md-2" role="button" aria-pressed="true">Join Slack</a>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    """, unsafe_allow_html=True)

    # features section
    st.markdown("""
        <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-1 border-bottom" style="margin-right: 200px; margin-left: 200px;"></div>
        <div class="row g-5 py-4 row-cols-1 row-cols-lg-3 col-md-8 offset-md-2">
            <div class="feature col">
                <h2 class="display-8 fw-bold lh-1 mb-3">Web Applications</h2>
                <p>Easy access to the web applications developed by the earthquake and structural engineering community.</p>
                <a href="/?nav=appsPage" target="_self" class="icon-link">
                Go to Applications
                </a>
            </div>
            <div class="feature col">
                <h2 class="display-8 fw-bold lh-1 mb-3">Event Reports</h2>
                <p> Case studies for data analysis and visualization of selected earthquake events.</p>
                <a href="/?nav=reportsPage" target="_self" class="icon-link">
                Go to Reports
                </a>
            </div>
            <div class="feature col">
                <h2 class="display-8 fw-bold lh-1 mb-3">Open-Source</h2>
                <p>Transparent and well-documented theory for the application.Open to contribution in public GitHub.</p>
                <a href="https://github.com/dogukankaratas/SeisKit" class="icon-link">
                Go To GitHub
                </a>
            </div>
        </div>
        <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-1 border-bottom" style="margin-right: 200px; margin-left: 200px;"></div>
    """, unsafe_allow_html=True)

    injectCSS()
    
