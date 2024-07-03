import os
import pprint
import traceback
import streamlit as st

from DB.DB_Chroma import DB_CLIENT

def update_tags(id, tags:list[str]):
   new_metadata = {'file_name':os.path.basename(id)}
   for tag in tags:
      new_metadata[tag]='tag'

   DB_CLIENT.update('img', id, file_path=None, metadata=new_metadata)