import streamlit as st
import os

from Service.Service_searchImages import *
from Navigation.sidebar_menu import sidebar_menu


def main():
    # print('initialize...')
    st.session_state.images = []    
    st.session_state.query_text = ''
    st.session_state.search_result = ''
    # print('initialize complete')
    
    sidebar_menu()
    st.title("Hello World!")

    st.text_input("검색어", on_change=find_images, key='query_text')



if __name__ == "__main__":
    main()
