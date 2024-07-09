import streamlit as st
import os

from Service.Service_searchImages import *
from Navigation.sidebar_menu import sidebar_menu

def init():
    if 'init' not in st.session_state:
        print('initialize...')
        st.session_state.images = []    
        st.session_state.query_text = ''
        st.session_state.tag_list = ['test1','test2','test3']
        st.session_state.init = True    
        print('initialize complete')    

def main():
    init()    
    sidebar_menu()
    st.title("갖고있는 로컬 파일 이미지 검색")

    st.text_input("검색어", on_change=find_images, key='query_text')
    selected = st.multiselect('선택', options=st.session_state.tag_list)
    print(selected)

    if "search_result" in st.session_state:
        search_result = st.session_state.search_result
        col1, col2, col3 = st.columns(3)
        for idx, file_info in enumerate(zip(search_result['ids'][0],search_result['metadatas'][0])):
            file_path, metadata = file_info            
            if idx%3==0:            
                with col1:
                    show_img_or_delete(file_path, metadata)
                    # if st.button(metadata['file_name']):
                    #     show_detail(file_path=file_path, metadata=metadata) 
            elif idx%3==1:            
                with col2:
                    show_img_or_delete(file_path, metadata)
                    # if st.button(metadata['file_name']):
                    #     show_detail(file_path=file_path, metadata=metadata) 
            elif idx%3==2:
                with col3:
                    show_img_or_delete(file_path, metadata)
                    # if st.button(metadata['file_name']):
                    #     show_detail(file_path=file_path, metadata=metadata)     

if __name__ == "__main__":
    main()

