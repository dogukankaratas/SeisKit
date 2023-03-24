import streamlit as st

def add_logo():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url(https://i.ibb.co/QrL4kjj/logo5.png);
                background-repeat: no-repeat;
                padding-top: 80px;
                background-position: 65px 20px;
            }
            [data-testid="stSidebarNav"]::before {
                content: "openseiskit";
                margin-left: 90px;
                margin-top: 10px;
                font-size: 20px;
                font-family: "Verdana";
                color: #2F86B1;
                position: relative;
                top: 80px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
