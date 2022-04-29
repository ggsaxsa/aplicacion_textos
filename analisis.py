from collections import Counter
from wordcloud import WordCloud
import streamlit as st

f = open('spanish.txt')
stopwords = set(map(lambda x: x.replace('\n', ''), f.readlines()))

def texto_s_stopwords(texto):
	cuerpo = texto.split()
	new_cuerpo = []
	for palabra in cuerpo:
		if not palabra in stopwords:
			new_cuerpo.append(palabra)
	return new_cuerpo


def analisis_eleccion(seleccion, data):

	if seleccion == 'Word count':
		texto_sin_stop = texto_s_stopwords(data)
		counter = Counter(texto_sin_stop)
		return st.write(counter)

	else:
		st.write('UPSSSSS... no implementado')

