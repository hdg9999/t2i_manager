import os
import streamlit as st
from DB.DB_Chroma import *

# db = DB_chroma()

def find_images():
    col1, col2, col3 = st.columns(3)
    for idx, file in enumerate(os.scandir('static/samples')):
        
        if idx%3==0:
            with col1:
                with st.container(border=False):
                    st.image(file.path, file.name)
                    # st.markdown(f"![Foo](app/static/samples/{file.name}) {file.name}")
                continue
        elif idx%3==1:
            with col2:
                with st.container(border=False):
                    st.image(file.path, file.name)
                    # st.markdown(f"[![Foo](app/static/samples/{file.name})](http://google.com/) {file.name}")
                continue
        elif idx%3==2:
            with col3:
                with st.container(border=False):
                    st.image(file.path, file.name)
                    # st.markdown(f"[![Foo](app/static/samples/{file.name})](http://google.com/) {file.name}")
                continue