import os

import streamlit as st
from Navigation.sidebar_menu import sidebar_menu
from Service.Service_folderPicker import select_folder, upload

sidebar_menu()

st.title('폴더 등록')

selected_folder_path = st.session_state.get("folder_path", None)
folder_select_button = st.button("폴더 선택")
if folder_select_button:
  selected_folder_path = select_folder()
  st.session_state.folder_path = selected_folder_path

st.divider()
st.write('선택된 폴더')
if selected_folder_path:
  st.info(selected_folder_path)
  st.button('폴더 등록', on_click=upload)



