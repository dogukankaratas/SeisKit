import streamlit as st
from injections.bootstrapInjection import navigationBar
from injections.cssInjection import injectCSS
from views import appsPage, reportsPage, homePage, seisScale, processorPage, tbec2018Page, asce22Page

# set page configuration to wide
st.set_page_config(page_title='SeisKit',layout='wide', page_icon="🏛️")

# apply injections
navigationBar()
injectCSS()

def get_current_route():
    try:
        return st.experimental_get_query_params()['nav'][0]
    except:
        return "homePage"
    
def navigation():
    route = get_current_route()
    if route == "homePage":
        homePage.load_view()
    elif route == "appsPage":
        appsPage.load_view()
    elif route == "reportsPage":
        reportsPage.load_view()
    elif route == "seisScale":
        seisScale.load_view()
    elif route == "processorPage":
        processorPage.load_view()
    elif route == "tbec2018Page":
        tbec2018Page.load_view()
    elif route == "asce22Page":
        asce22Page.load_view()

navigation()