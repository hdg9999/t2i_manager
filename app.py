import streamlit as st
import os

from Service.Service_searchImages import *


def main():
    # print('initialize...')
    st.session_state.images = []    
    st.session_state.query_text = ''
    # print('initialize complete')

    st.title("Hello World!")

    st.text_input("검색어", on_change=find_images, key='query_text')
    



if __name__ == "__main__":
    main()
