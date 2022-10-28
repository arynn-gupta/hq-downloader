import streamlit as st
import os, shutil, mimetypes
from icons import *

style='''
div.css-1gk2i2l.e17lx80j0 {
  width: 100%;
  height: 250px;
  display: flex;
  align-items: center;
  justify-content: center;
}

h1 span {
  color: #893aff;
}

h3 span {
  color: #06b48b;
}

li path {
  display: none;
}

li {
  padding: none;
}

li span {
  width: 100%;
  margin-right: 1.2rem;
  margin-bottom: 0.5rem;
  padding: 0.5rem 2rem;
  color: #b4b6be;
  border-radius: 0.5rem;
}

li span:before{
    margin-right: 8px; position: relative;  top: 2px; 
}

li span:hover {
  color: white;
  background-color: #313334;
}

a {
  background: none !important;
}

a.css-1m59598.e1fqkh3o6 span{
  color: white;
  background-color: #313334;
}
'''

def styling():
  st.markdown(f"<style>{style}</style>", unsafe_allow_html=True)
  st.markdown('''<style>
      li:nth-child(1) span:before {  content: '''+fire+'''; }
      li:nth-child(2) span:before {  content: '''+folder+'''; }
  </style>''', unsafe_allow_html=True)

def make_zip(download_file_path):
    file_path = st.session_state["current_path"]+"/"+download_file_path
    if(os.path.isfile(file_path)):
        shutil.make_archive(file_path, 'zip', st.session_state["current_path"], download_file_path)
    elif len(os.listdir(file_path)) != 0:
        shutil.make_archive(file_path, 'zip', file_path)

def download_file(download_file_path, ele):
    file_path = st.session_state["current_path"]+"/"+download_file_path
    mimestart = mimetypes.guess_type(download_file_path)[0]
    if mimestart != None:
      file = open(f"{file_path}", "rb")
      ele.download_button(
              label="⬇️",
              data=file,
              file_name=f"{download_file_path}",
              mime=mimestart,
          )
      file.close()