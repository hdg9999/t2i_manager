import os
import pprint

import streamlit as st
from DB.DB_Chroma import DB_CLIENT
from PIL import Image

#로컬 이미지뷰어로 파일 열기
def open_image(file_path):
    Image.open(file_path).show()   

# 이미지 검색 결과 데이터 session_state에 저장
def find_images():
    try:    
        search_result = DB_CLIENT.search('img', st.session_state.query_text)
        st.session_state.search_result = search_result
        pprint.pp(search_result)
    except ValueError as VE:
        if 'Collection img does not exist.' in VE.args:
            st.error("DB 생성이 되어있지 않습니다. 폴더 등록 페이지에서 폴더를 지정하여 업로드해보세요!")
        else:
            raise VE

#이미지 클릭 시 나타나는 팝업창
@st.experimental_dialog("이미지 상세", width='large')
def show_detail(file_path, metadata):    
    with st.form(key="update_form"):
        st.image(file_path)
        st.write(metadata)
        st.form_submit_button('변경사항 저장')    
    
    if st.button('파일 열기'):
        open_image(file_path)
        

#검색 결과 썸네일 표시하는 함수
def show_thumnail(state_key:str, file_path:str, metadata:dict):    
    with st.container(border=None):
        st.image(file_path)
        if st.button(metadata['file_name']):
            show_detail(state_key)      