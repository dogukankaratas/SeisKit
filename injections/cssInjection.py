import streamlit as st
import sys

sys.path.append('./.')

def injectCSS():
    # read css file
    with open('style/styles.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)