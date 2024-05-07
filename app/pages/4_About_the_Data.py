import os
import sys
from datetime import date

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Acerca de los Datos")

st.markdown(
    """
    <style>
        section.main > div {max-width:65rem}
    </style>
    """,
    unsafe_allow_html=True
)

today = date(2024, 5, 5)
today_format = today.strftime("%B %d, %Y")

def main():
    sidebar()
    content()

def sidebar():
    with st.sidebar:
        st.image('assets/img/TheTorturedPoetsDepartment.jpg')
        st.markdown("""
        <h3 style="text-align: center;">Discografía de Taylor Swift - Canciones</h3>

        <p style="text-align: center;">Este es un proyecto en curso y de código abierto. ¡Sigue el progreso en <a href='https://github.com/madroscla/taylor-swift-discography'>Github</a>!</p>

        <p style="text-align: center;">Los datos fueron actualizados por última vez el <b>{}</b>.</p>
        
        """.format(today_format), unsafe_allow_html=True)

@st.cache_data
def content():
    st.markdown("""
    ## Acerca de los Datos

    Todos los datos para este proyecto han sido extraídos de Genius utilizando el paquete de Python [parsel](https://parsel.readthedocs.io/en/latest/). Los datos se formatean en una base de datos SQLite, desde la cual se consultan todos los datos en esta aplicación. La base de datos tiene el siguiente formato:
    """)

    st.image('figures/db_schema.png')

    st.markdown("""    
    Por favor, revisa [este cuaderno en el Github del proyecto](https://github.com/madroscla/taylor-swift-discography/blob/main/notebooks/data_collection.ipynb) para obtener más detalles sobre cómo se obtuvieron los datos. 
    """)

    st.markdown("""
    ## Vista previa de los datos

    La base de datos utilizada en esta aplicación, así como las versiones en pickle de los datos, se pueden encontrar en el [repositorio de Github del proyecto](https://github.com/madroscla/taylor-swift-discography/tree/main/data). Los datos también están disponibles en formato CSV en [Kaggle](https://www.kaggle.com/datasets/madroscla/taylor-swift-released-song-discography-genius) para uso público bajo la licencia CC BY-SA 4.0.
    """)

    df = pd.read_pickle('data/taylor_swift_clean.pkl')

    st.dataframe(df.sample(100))
    st.markdown("""
    ## Restricciones y Limitaciones de la Discografía
    
    Esta discografía prioriza la cobertura de *canciones* sobre la cobertura de *álbumes*; esto significa que se prefieren las versiones de lujo de los álbumes con más canciones sobre las versiones estándar, y que se prefieren los lanzamientos de álbumes sobre los lanzamientos de sencillos/EP. Si bien no se cubrirán todas las versiones de lanzamiento de una canción en este conjunto de datos, contiene cada canción única. Las canciones regrabadas se cuentan como entradas separadas de sus versiones originales.
    
    Consulta la tabla a continuación para obtener más información sobre lo que está incluido y lo que no está incluido en la discografía:
    
    | Incluido en la Discografía | No incluido en la Discografía |
    | -- | -- |
    | Canciones lanzadas en los álbumes de estudio de Taylor Swift | Entradas duplicadas de canciones (por ejemplo, para lanzamiento como sencillo, lanzamiento de álbum, lanzamiento de álbum de lujo, etc.) |
    | Canciones lanzadas en los álbumes regrabados de Taylor Swift "Taylor's Version" | Canciones no lanzadas/filtradas y demos |
    | Canciones de Taylor Swift para bandas sonoras o lanzadas como sencillos no incluidos en álbumes | Covers de canciones de Taylor Swift realizados por otros artistas |
    | Remixes de canciones de Taylor Swift con nuevos artistas intérpretes o ejecutantes | Remixes/versiones acústicas de canciones que no cuentan con nuevos artistas intérpretes o ejecutantes |
    | Canciones escritas por Taylor Swift para otros artistas, incluso si no cuenta con la participación de Taylor | Versiones en vivo de canciones/mashups de canciones ya contabilizadas |
    | Canciones de otros artistas con la participación de Taylor Swift | Canciones que muestren/superpongan fragmentos de canciones de Taylor Swift, incluso si la lista como escritora o con su participación |
    | Covers de canciones realizados por Taylor Swift o con su participación que hayan sido grabados y lanzados oficialmente | Canciones que solo existen en formato de video (DVD, grabación de espectáculo en vivo, etc.) |
    """)

if __name__ == '__main__':
    main()