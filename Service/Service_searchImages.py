import os
import pprint

import streamlit as st
from streamlit.runtime.media_file_storage import MediaFileStorageError
from DB.DB_Chroma import DB_CLIENT
from PIL import Image

from Service.Service_tags import *

#로컬 이미지뷰어로 파일 열기
def open_image(file_path):
    Image.open(file_path).show()   

# 이미지 검색 결과 데이터 session_state에 저장
def find_images():
    try:    
        search_result = DB_CLIENT.search('img', query_texts=st.session_state.query_text, where=st.session_state.selected_tags, top_k=st.session_state.top_K)
        st.session_state.search_result = search_result
        pprint.pp(search_result)
    except ValueError as VE:
        if 'Collection img does not exist.' in VE.args:
            st.error("DB 생성이 되어있지 않습니다. 폴더 등록 페이지에서 폴더를 지정하여 업로드해보세요!")
        else:
            raise VE

def show_img_or_delete(img_path, metadata):
    try:
        st.image(img_path)
        if st.button(metadata['file_name']):
            show_detail(file_path=img_path, metadata=metadata) 
    except MediaFileStorageError as ME:
        DB_CLIENT.delete('img', img_path)
        st.error(f'삭제된 파일입니다. {img_path}')

# metadata를 multiselect출력용으로 변환
def metadata_to_tags(metadata:dict):
    return [ {key:{'$eq':True}} for key in iter(metadata) if key!='file_name' ]

#이미지 클릭 시 나타나는 팝업창
@st.experimental_dialog("이미지 상세", width='large')
def show_detail(file_path, metadata):    
    with st.form(key="update_form"):
        st.image(file_path)
        st.write('파일명:', metadata['file_name'])
        tags_to_update = st.multiselect(label='태그', options=st.session_state.tag_list, format_func=selected_tags_formatter, default=metadata_to_tags(metadata))
        print('tags_to_update:',tags_to_update)      
        if st.form_submit_button('변경사항 저장'):
            print('update...')
            metadata_to_update = {}
            for key in [next(iter(tag)) for tag in tags_to_update]:
                print('key:',key)
                metadata_to_update[key] = True
            print('metadata to update:',metadata_to_update)
            DB_CLIENT.update('img', id=file_path, file_path=file_path, metadata=metadata_to_update)
            st.toast('변경사항이 저장되었습니다.',icon='✅')
            find_images()
            st.rerun()            

    if st.button('파일 열기'):
        open_image(file_path)
        

#검색 결과 썸네일 표시하는 함수
def show_thumnail(state_key:str, file_path:str, metadata:dict):    
    with st.container(border=None):
        st.image(file_path)
        if st.button(metadata['file_name']):
            show_detail(state_key)      