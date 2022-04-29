import streamlit as st
from PIL import Image
import json
import re
from analisis import *

def select_text_feature(nombre):

	file = open('salidas_aplicacion/' + nombre)
	data = json.load(file)

	text_col = st.selectbox('Select the text column',(list(data.keys())))

	contenido = data[text_col]
	contenido = re.sub('-{2,}', ' ', contenido)

	return contenido, text_col

# Configuración de la aplicación

try:

	from funciones_aux import *

	# Diseño de la aplicación
	app_saxsa(":file_folder:")
	set_bg_hack('36837-claros.jpg')

	logo = Image.open('saxsa.png')
	st.sidebar.image(logo, use_column_width=True)

	# # Configuración del panel principal
	display_app_header(main_txt='Análisis de archivos de textos',
					   sub_txt='Extrae el contenido de un archivo, para analizar con NLP')

	st.markdown("""---""")

	# Side panel setup
	# Step 1 includes Uploading and Preprocessing data (optional)
	display_app_header(main_txt="Paso 1",
					   sub_txt="Cargar datos",
					   is_sidebar=True)

	data_input_mthd = st.sidebar.radio("Seleccione el método de entrada de datos",
									   ('PDF Escaneado', 
									   	'PDF Generado',
									   	'Archivo WORD'))

	st.subheader('Elija los datos que desea analizar :alembic:')
	data, txt = check_input_method(data_input_mthd)

	data, text_column = select_text_feature(data)
	st.write(data)

	st.subheader('Using Raw data :cut_of_meat:')  #Raw data header
	display_app_header(main_txt = "Paso 2",
					   sub_txt= "Analizar los datos",
					   is_sidebar=True)

	selected_plot = st.sidebar.radio(
	"Escoje un analisis", ('Word count',
					  	   'N-grams',
					  	   'Wordcloud',
					  	   'POS')
	)

	analisis_eleccion(selected_plot, data)

except KeyError:
    st.error("Please select a key value from the dropdown to continue.")

except ValueError:
    st.error("Oops, something went wrong. Please check previous steps for inconsistent input.")

except TypeError:
    st.error("Oops, something went wrong. Please check previous steps for inconsistent input.")
