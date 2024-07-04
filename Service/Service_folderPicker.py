import tkinter
import os
import pprint
import traceback
import streamlit as st

from tkinter import filedialog
from DB.DB_Chroma import DB_CLIENT

def select_folder():
   root = tkinter.Tk()
   root.withdraw()
   folder_path = filedialog.askdirectory(master=root)
   root.destroy()
   return folder_path

def upload():
   ids = [file.path for file in os.scandir(st.session_state.folder_path)]
   image_files = [file.path for file in os.scandir(st.session_state.folder_path)]
   metadatas = [{'file_name':file.name} for file in os.scandir(st.session_state.folder_path)]

   DB_CLIENT.get_or_create('img')
   DB_CLIENT.add('img',ids=ids, image_files=image_files, file_info=metadatas)
   
   st.info('등록이 완료되었습니다.')

