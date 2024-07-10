import os
import time
import pickle

import streamlit as st
from Navigation.sidebar_menu import sidebar_menu
from DB.DB_Chroma import *

sidebar_menu()

st.title('데이터 초기화')

st.warning('정말로 초기화 하시겠습니까? 기록했던 태그 정보, 등록된 임베딩 등이 모두 사라집니다.\n\n *이미지 파일 원본이 사라지는 것은 아닙니다.')
if st.button('초기화'):
    DB_CLIENT.drop('img')
    print('db 초기화 완료.')
    with open('tags.p', 'wb') as tag_config_file:
        pickle.dump([], tag_config_file)
    print('저장된 태그 데이터 제거 완료.')
    st.session_state.tag_list=[]
    st.info('저장된 데이터가 모두 초기화 되었습니다. 3초 후 새로고침 됩니다.')
    time.sleep(3)
    st.rerun()
