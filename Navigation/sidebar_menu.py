import os
import pickle
import streamlit as st

from Service.Service_tags import *

def sidebar_menu():
    with st.sidebar:
        st.title('🏷️T2I Manager')
        st.divider()
        page_menu()
        tag_manager()
        search_options()

def page_menu():    
    st.subheader('메뉴', divider=True)    
    st.page_link(page='app.py', label='Home')
    st.page_link(page='Pages/register_folder.py', label='폴더 등록')
    # st.page_link(page='Pages/clear_db.py', label='초기화(데이터 전체 삭제)')  //백신이 막아서.. 일단 보류
    st.write('\n') #여백

def tag_manager():
    st.subheader('태그 관리', divider=True)  
    tag_input = st.text_input(label='태그 추가',placeholder='새로 추가할 태그 작성...')
    # print('tag_list:',st.session_state.tag_list)
    # print('tag_input:',tag_input)
    tag_to_add ={tag_input:{'$eq':True}}
    # print('tag_to_add:',tag_to_add)
    if tag_input:
        add_tags = st.button(label='태그추가')
        if add_tags:
            if tag_to_add in st.session_state.tag_list:
                st.toast(body="이미 존재하는 태그입니다.", icon='⚠️')
            else:
                st.session_state.tag_list.append(tag_to_add)
                # st.session_state.tag_list=list(set(st.session_state.tag_list))
                with open('tags.p', 'wb') as tag_config_file:
                    pickle.dump(st.session_state.tag_list, tag_config_file)
                st.toast(body="태그가 추가되었습니다.", icon='✅')    

    tags = st.multiselect('등록된 태그', options=st.session_state.tag_list, placeholder='태그 선택...', default=st.session_state.tag_list, format_func=selected_tags_formatter)
    # delete_tags = st.button(label='선택된 태그 삭제')

def search_options():
    st.divider()
    with st.expander(label='검색 옵션'):    
        st.session_state.top_K = st.slider(label='검색 갯수', min_value=1, max_value=1000, value=10)