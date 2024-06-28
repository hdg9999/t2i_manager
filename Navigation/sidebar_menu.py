import os
import streamlit as st

def sidebar_menu():
    with st.sidebar:
        st.page_link(page='app.py', label='Home')
        st.page_link(page='Pages/register_folder.py', label='폴더 등록')