import cv2
import numpy as np
import streamlit as st
import pandas as pd
import datetime
import argparse
from pathlib import Path
from numbers_detector import convert_image
from utils import init_logger
from PIL import Image

logger = init_logger(__name__, testing_mode=False)
# parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
# path_parser = parser.add_argument('-c', '--config', type=Path, default='config.ini',
#                                   help='Set path to your config.ini file.')
#
# args = parser.parse_args()

st.set_page_config(
    page_title="Document Extractor",
    page_icon="🧊",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/petrcezner/document-scanner/issues',
        'Report a bug': "https://github.com/petrcezner/document-scanner/issues",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

st.title('Welcome to Document Extractor!!!')

if 'current_time' not in st.session_state:
    st.session_state.current_time = datetime.datetime.now()

if 'image_loaded' not in st.session_state:
    st.session_state.image_loaded = False

if 'converted' not in st.session_state:
    st.session_state.converted = False

if 'document_language' not in st.session_state:
    st.session_state.document_language = 'eng'


def on_image_convert_submit():
    st.session_state.current_time = datetime.datetime.now()
    file_bytes = np.asarray(bytearray(st.session_state.image_path.read()), dtype=np.uint8)
    st.session_state.loaded_image = cv2.imdecode(file_bytes, 1)
    st.session_state.document_language = st.session_state.doc_language
    st.session_state.image_loaded = True
    logger.info('Image is uploaded.')


if st.button('Upload Image'):
    with st.form('upload_form'):
        st.text_input('Warehouse', value='w0000', key='warehouse')
        st.text_input('Box Number', value='b0000', key='box_number')
        st.selectbox('Select document language',
                     ['eng', 'deu', 'fra', 'ces', 'rus', 'pol'],
                     key='doc_language')
        st.file_uploader("Choose a file", key='image_path', type=['jpg', 'png'])
        st.form_submit_button(label='Upload', on_click=on_image_convert_submit)

if st.session_state.image_loaded:
    st.image(st.session_state.loaded_image, channels="BGR")
    if st.button('Convert'):
        st.session_state.result_path = convert_image(st.session_state.loaded_image,
                                                     language=st.session_state.document_language)
        st.session_state.converted = True

    if st.session_state.converted:
        with open(st.session_state.result_path, 'r') as f:
            uploaded_file = f.read()
            st.markdown('## Found numbers in image:')
            st.write(uploaded_file)

        st.download_button(label='Download converted image',
                           data=uploaded_file,
                           file_name=f'converted_image_{st.session_state.current_time.strftime("%Y%m%d-%H%M%S")}.txt',
                           mime='text/txt')
        logger.info('The output file is downloaded and saved.')

if st.button('Close'):
    st.session_state.image_loaded = False
    st.session_state.converted = False
