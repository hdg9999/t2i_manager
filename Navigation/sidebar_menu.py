import os
import streamlit as st

def sidebar_menu():
    with st.sidebar:
        st.page_link(page='app.py', label='Home')
        st.page_link(page='Pages/register_folder.py', label='폴더 등록')
        tag_manager()

def tag_manager():
    st.divider()
    tag_input = st.text_input(label='태그 추가',placeholder='새로 추가할 태그 작성...')
    add_tags = st.button(label='태그추가')
    if add_tags:
        st.session_state.tag_list.append(tag_input)
        st.session_state.tag_list=list(set(st.session_state.tag_list))

    tags = st.multiselect('등록된 태그', options=st.session_state.tag_list, placeholder='태그 선택...', default=st.session_state.tag_list)


    print(tags)
