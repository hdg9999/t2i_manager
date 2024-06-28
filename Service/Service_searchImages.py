import os
import pprint

import streamlit as st
from DB.DB_Chroma import *
from PIL import Image

db = DB_chroma()

def open_image(file_path):
    Image.open(file_path).show()   

def show_thumnail(state_key:str, file_path:str, metadata:dict):    
    with st.container(border=None):
        st.image(file_path)
        if st.button(metadata['file_name']):
            show_detail(state_key)        

@st.experimental_dialog("이미지 상세")
def show_detail(file_path, metadata):
    with st.container(border=None):
        st.image(file_path)
        st.write(metadata)

def find_images():
    col1, col2, col3 = st.columns(3)
    search_result = db.search('img', st.session_state.query_text)

    st.session_state.search_result = search_result
    pprint.pp(search_result)

    for idx, file_info in enumerate(zip(search_result['ids'][0],search_result['metadatas'][0])):

        file_path, metadata = file_info
        if idx%3==0:            
            with col1:
                st.image(file_path)
                if st.button(metadata['file_name']):
                    show_detail(file_path=file_path, metadata=metadata) 
        elif idx%3==1:            
            with col2:
                st.image(file_path)
                if st.button(metadata['file_name']):
                    show_detail(file_path=file_path, metadata=metadata) 
        elif idx%3==2:
            with col3:
                st.image(file_path)
                if st.button(metadata['file_name']):
                    show_detail(file_path=file_path, metadata=metadata) 