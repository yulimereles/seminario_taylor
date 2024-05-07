import os
import sys
from datetime import date

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import streamlit as st

st.markdown(
    """
    <style>
        section.main > div {max-width:65rem}
    </style>
    """,
    unsafe_allow_html=True
)

today = date(2024, 5, 7)
today_format = today.strftime("%B %D, %Y")



def main():
    sidebar()
    content()

def sidebar():
    with st.sidebar:
        st.image('assets/img/TheTorturedPoetsDepartment.jpg')
        st.markdown("""
        <h3 style="text-align: center;">Discografía de canciones de Taylor Swift</h3>

        <p style="text-align: center;">Este es un proyecto en curso y de código abierto. ¡Sigue el progreso en <a href='https://github.com/madroscla/taylor-swift-discography'>Github</a>!</p>

        <p style="text-align: center;">Los datos se actualizaron por última vez el <b>{}</b>.</p>
        
        """.format(today_format), unsafe_allow_html=True)

def content():
    st.image('assets/img/TTPDLogo.png')
    st.markdown(
        """
   ¡Bienvenido!
    Esta aplicación representa un proyecto en curso para compilar y analizar la discografía de canciones de Taylor Swift. Aquí encontrarás varios análisis exploratorios de datos de diferentes aspectos de las canciones de Taylor Swift, incluyendo cómo y cuándo se lanzan, con quién crea su música, y el tráfico de cada canción en Genius. A medida que Taylor lance más música, esta aplicación crecerá, con planes inmediatos para el análisis de sus letras usando NLP.
    """
    )

if __name__ == '__main__':
    main()
