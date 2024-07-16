import tkinter
import os
import pprint
import traceback
from pathlib import Path
import streamlit as st

from tkinter import filedialog
from DB.DB_Chroma import DB_CLIENT

def select_folder():
   tk = tkinter.Tk()
   tk.wm_attributes("-topmost",1)
   tk.withdraw()
   folder_path = filedialog.askdirectory(master=tk)
   tk.destroy()
   return folder_path

def upload():
   allowed_exts = ['.jpg','.jpeg','.png','.gif','.webp']
   target_files = [ file for file in os.scandir(st.session_state.folder_path) if Path(file.name).suffix in allowed_exts ]
   ids = [ file.path for file in target_files ]
   image_files = [ file.path for file in target_files ]
   metadatas = [ {'file_name':file.name} for file in target_files ]

   DB_CLIENT.get_or_create('img')
   DB_CLIENT.add('img',ids=ids, image_files=image_files, file_info=metadatas)
   
   st.info('등록이 완료되었습니다.')

