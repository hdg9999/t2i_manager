import tkinter
import os
import pprint
import traceback
import streamlit as st

from tkinter import filedialog
from DB.DB_Chroma import DB_chroma

def select_folder():
   root = tkinter.Tk()
   root.withdraw()
   folder_path = filedialog.askdirectory(master=root)
   root.destroy()
   return folder_path

def upload():
   client = DB_chroma()

   ids = [file.path for file in os.scandir(st.session_state.folder_path)]
   image_files = [file.path for file in os.scandir(st.session_state.folder_path)]
   metadatas = [{'file_name':file.name} for file in os.scandir(st.session_state.folder_path)]

   # pprint.pp(metadatas)
   
   try:      
      client.add('img',ids=ids, image_files=image_files, file_info=metadatas)
   except ValueError as VE:
      if 'Collection img already exists' in VE.args:
         client.create('img')
         client.add('img',ids=ids, image_files=image_files, file_info=metadatas)
      else:
         print(traceback.format_exc())
         raise Exception('뭔가 잘못되었습니다! 에러 로그를 확인하세요.')