import streamlit as st

def add_logo():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url(https://i.ibb.co/Hgyhdvf/logo2.png);
                background-repeat: no-repeat;
                padding-top: 35px;
                background-position: 100px 20px;
            }
            [data-testid="stSidebarNav"]::before {
                content: "openseiskit";
                margin-left: 100px;
                margin-top: 10px;
                font-size: 18px;
                font-family: "Verdana";
                color: #2F86B1;
                position: relative;
                top: 80px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
