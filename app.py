import streamlit as st
import os
import pickle

from Service.Service_searchImages import *
from Service.Service_tags import *
from Navigation.sidebar_menu import sidebar_menu


def init():
    if 'init' not in st.session_state:
        print('initialize...')
        st.session_state.images = []    
        st.session_state.query_text = ''
        st.session_state.selected_tags = []
        st.session_state.top_K = 10
        try:        
            with open('tags.p', 'rb') as tag_config_file:
                st.session_state.tag_list = pickle.load(tag_config_file)
        except:
            st.session_state.tag_list = []
            with open('tags.p', 'wb') as tag_config_file:
                pickle.dump(st.session_state.tag_list, tag_config_file)
        st.session_state.init = True    
        print('initialize complete')    

def main():
    init()    
    sidebar_menu()
    st.title("갖고있는 로컬 파일 이미지 검색")

    st.text_input("검색어", on_change=find_images, key='query_text')
    st.session_state.selected_tags = st.multiselect('검색할 태그', options=st.session_state.tag_list, format_func=selected_tags_formatter)

    if "search_result" in st.session_state:
        search_result = st.session_state.search_result
        col1, col2, col3 = st.columns(3)
        for idx, file_info in enumerate(zip(search_result['ids'][0],search_result['metadatas'][0])):
            file_path, metadata = file_info            
            if idx%3==0:            
                with col1:
                    show_img_or_delete(file_path, metadata)
            elif idx%3==1:            
                with col2:
                    show_img_or_delete(file_path, metadata)
            elif idx%3==2:
                with col3:
                    show_img_or_delete(file_path, metadata)  

if __name__ == "__main__":
    main()

