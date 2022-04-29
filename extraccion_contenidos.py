import streamlit as st
import pytesseract
import json

@st.cache()
def saca_texto_pdf_img(pdf_imagen, name):
	texto = []
	aux = {}
	for page_number, page_data in enumerate(pdf_imagen, start=1):
		contenido = str(pytesseract.image_to_string(page_data))
		texto.append((page_number, contenido))
	for pagina, contenido in texto:
		aux['Pagina_' + str(pagina)] = contenido
	json_object = json.dumps(aux, indent=4, ensure_ascii=False)
	with open('salidas_aplicacion/' + name + '.json', 'w') as outfile:
		outfile.write(json_object)
	return name + '.json'

@st.cache()
def saca_texto_pdf_creado(pdf_creado, name):
	pdf_json = {}
	for i, pagina in enumerate(pdf_creado.pages, start=1):
		pdf_json['Pagina_' + str(i)] = pagina.extract_text()
	convert = json.dumps(pdf_json, indent=4, ensure_ascii=False)
	with open('salidas_aplicacion/' + name + '.json', 'w') as salida:
		salida.write(convert)
	return name + '.json'

