import streamlit as st
import pandas as pd
import base64
import io
import pdfplumber
from extraccion_contenidos import *
from pdf2image import convert_from_bytes

def app_saxsa(icon):

	# Set website details
	st.set_page_config(page_title="Análisis de textos", 
					   page_icon=icon, 
					   layout='centered')

	# set sidebar width
	st.markdown(
	"""
	<style>
	[data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
		width: 300px;
	}
	[data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
		width: 300px;
		margin-left: -300px;
	}
	</style>
	""",
    unsafe_allow_html=True
    )

def set_bg_hack(main_bg):
	'''
	A function to unpack an image from root folder and set as bg.
	The bg will be static and won't take resolution of device into account.
	Returns
	-------
	The background.
	'''
	# set bg name
	main_bg_ext = "jpg"

	st.markdown(
		f"""
		<style>
			.stApp {{
				background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
				background-size: cover
         	}}
        </style>
        """,
        unsafe_allow_html=True
    )


# mostrar la cabecera de la aplicación y la barra lateral
# utilizar el código HTML para establecer el div
def display_app_header(main_txt, sub_txt, is_sidebar=False):
	"""
	function to display major headers at user interface
	----------
	main_txt: str -> the major text to be displayed
	sub_txt: str -> the minor text to be displayed 
	is_sidebar: bool -> check if its side panel or major panel
	"""

	html_temp = f"""
	<h2 style="color: #F74369; text-align: center; font-weight: bold;"> {main_txt} </h2>
	<p style="color: #BB1D3F; text-align: center;"> {sub_txt} </p>
	</div>
	"""
	if is_sidebar:
		st.sidebar.markdown(html_temp, unsafe_allow_html=True)
	else: 
		st.markdown(html_temp, unsafe_allow_html=True)


def get_input(data_input_mthd,ss_text,is_batch=False,text_column = "text"):
    """
    function get input from user either by uploading a csv file, pasting text
    or importing json files
    ----------
    ss_text: string
    is_batch: bool 
    text_column: str -> the columnn name for creating pd.DataFrame is _is_batch is False
    """
    if 'Escaneado' in data_input_mthd:
        uploaded_file = st.file_uploader("Elija un archivo pdf escaneado para analizar", type="pdf")

        if uploaded_file is not None:
            st.success('Archivo cargado con éxito')
            nombre = uploaded_file.name.split('.')[0]
            str_data = uploaded_file.getvalue()
            pdf_escaneado = convert_from_bytes(str_data)
            with st.spinner('Espera mientras termina de procesar ...'):
            	nombre = saca_texto_pdf_img(pdf_escaneado, nombre)
            st.success('Tu archivo se proceso con éxito')
            return nombre, ss_text
        else:
            st.info('Cargue un archivo pdf escaneado')
            return 'Hola.json',ss_text

    elif 'Generado' in data_input_mthd: 
        uploaded_file = st.file_uploader("Elija un archivo pdf procesado para analizar", type="pdf")

        if uploaded_file is not None:
            st.success('Archivo cargado con éxito')
            nombre = uploaded_file.name.split('.')[0]
            str_data = uploaded_file.getvalue()
            content = io.BytesIO(str_data)
            entrada = pdfplumber.open(content)
            with st.spinner('Espera mientras termina de procesar ...'):
            	nombre = saca_texto_pdf_creado(entrada, nombre)
            st.success('Tu archivo se proceso con éxito')
            return nombre, ss_text
        else:
            st.info('Cargue un archivo pdf procesado')
            return 'Hola.json', ss_text
    
    elif 'WORD' in data_input_mthd:
        uploaded_file = st.file_uploader("Elija un archivo word para analizar", type = "docx")

        if uploaded_file is not None:
            st.success('Archivo cargado con éxito')
            #data = json.load(uploaded_file)
            #df = pd.json_normalize(data)
            #df = pd.read_json(uploaded_file)
            saludo = "Hola"
            return saludo, ss_text
        else:
            st.info('Cargue un archivo word')
            return pd.DataFrame(), ss_text

def check_input_method(data_input_mthd):
	"""
	function check user input method if uploading or pasting or using
	a json file
	Parameters
	----------
	data_input_mthd: str -> the default displayed text for decision making
	"""
	# ----------------------------------------------
	# session state init
	st.session_state['is_file_uploaded'] = False
	st.session_state['is_batch_process'] = False
	st.session_state['txt'] = 'Paste the text to analyze here'

	if 'Escaneado' in data_input_mthd:
		contenido, st.session_state.txt = get_input(data_input_mthd,
													ss_text= st.session_state.txt,
													is_batch=True)
		if len(contenido)>0:
			st.session_state.is_batch_process = True
			st.session_state.is_file_uploaded = True			

	elif 'Generado' in data_input_mthd:
		contenido, st.session_state.txt = get_input(data_input_mthd,
												    ss_text= st.session_state.txt,
												    is_batch=True)
		if len(contenido)>0:
			st.session_state.is_batch_process = True
			st.session_state.is_file_uploaded = True

	elif 'WORD' in data_input_mthd:
		contenido, st.session_state.txt = get_input(data_input_mthd,
												    ss_text= st.session_state.txt,
												    is_batch=True)
		if contenido>0:
			st.session_state.is_batch_process = True
			st.session_state.is_file_uploaded = True

	return contenido, st.session_state.txt
