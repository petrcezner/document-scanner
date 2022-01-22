import streamlit as st
import pandas as pd
import datetime
import argparse
from pathlib import Path

from utils import init_logger

logger = init_logger(__name__, testing_mode=False)
# parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
# path_parser = parser.add_argument('-c', '--config', type=Path, default='config.ini',
#                                   help='Set path to your config.ini file.')
#
# args = parser.parse_args()

st.set_page_config(
    page_title="Document Extractor",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/petrcezner/document-scanner/issues',
        'Report a bug': "https://github.com/petrcezner/document-scanner/issues",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

st.title('Welcome to Document Extractor!!!')

if 'upload_submit' not in st.session_state:
    st.session_state.upload_submit = False


def on_data_upload_submit():
    st.session_state.bucket = st.session_state.u_bucket
    st.session_state.measurement = st.session_state.u_measurement
    st.session_state.data_time = datetime.datetime.combine(st.session_state.u_date,
                                                           st.session_state.u_time,
                                                           tzinfo=datetime.datetime.now().astimezone().tzinfo)
    st.session_state.uploaded_data = pd.read_csv(st.session_state.uploaded_file)
    st.session_state.upload_submit = True
    st.session_state.data_loaded = True


if st.sidebar.button('Upload data'):
    with st.form('upload_form'):
        st.text_input('Warehouse', value='w0000', key='u_bucket')
        st.text_input('Box Number', value='b0000', key='u_measurement')
        st.file_uploader("Choose a file", key='uploaded_file', type=['jpg', 'png'])
        # st.form_submit_button(label='Convert', on_click=on_data_upload_submit)
        st.form_submit_button(label='Convert')
