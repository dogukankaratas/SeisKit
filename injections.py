import streamlit as st

def addLogo():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"]::before {
                content: "SeisKit";
                margin-left: 120px;
                margin-top: 10px;
                font-size: 20px;
                font-family: "Verdana";
                color: #2F86B1;
                position: absolute;
                top: 30px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

def addBootstrap():
    st.markdown("""
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">

    """, unsafe_allow_html = True)

def zeroPadding():
    hide_streamlit_style = """
    <style>
        #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 0rem;}
    </style>

    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
