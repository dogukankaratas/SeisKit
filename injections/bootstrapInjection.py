import streamlit as st
import base64
from streamlit.components.v1 import html

def navigationBar():
    # import bootstrap 5
    st.markdown("""
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-KK94CHFLLe+nY2dmCWGMq91rCGa5gtU4mk92HdvYe+M/SXH301p5ILy+dN9+nJOZ" crossorigin="anonymous">
    """, unsafe_allow_html=True)

    # navigation bar
    st.markdown("""
        <nav class="navbar navbar-expand-md navbar-light bg-light" id="navbar">
            <a class="navbar-brand" href="/?nav=homePage" target="_self" style="margin-left: 100px; color: black;">SeisKit</a>
            <ul class="navbar-nav" style="margin-left: 50px;">
                <li class="nav-item">
                    <a class="nav-link" href="/?nav=homePage" target="_self" style="color: black;">🏛️Home</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="/?nav=appsPage" target="_self" style="color: black;">🔗Applications</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="/?nav=reportsPage" target="_self" style="color: black;">📜Reports</a>
                </li>
            </ul>
            <ul class="navbar-nav ms-auto me-5">
                <li class="nav-item">
                    <a class="nav-link" href="https://github.com/dogukankaratas/SeisKit" target="_blank" style="margin-right: 20px; color: black;">✍️Source Code</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="https://www.linkedin.com/in/dogukankaratas/" target="_blank"  style="margin-right: 50px; color: black;">✉️Contact</a>
                </li>
            </ul>
        </nav>
    """, unsafe_allow_html=True)