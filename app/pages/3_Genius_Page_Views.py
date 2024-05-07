import os
import sys
from datetime import date

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pandas as pd
import streamlit as st
import sqlite3 as sql
from matplotlib import rcParams

from src import charts
from src import toolkit

st.set_page_config(page_title="Vistas de Página en Genius")

st.markdown(
    """
    <style>
        section.main > div {max-width:65rem}
    </style>
    """,
    unsafe_allow_html=True
)

connection = sql.connect('data/taylor_swift.db')
cursor = connection.cursor()

eras = toolkit.eras_order()

rcParams, custom_params = toolkit.chart_params(rcParams)

# Creating temporary table to be used throughout
temp_table = toolkit.sql_to_string('views_temp_table.sql')
cursor.executescript(temp_table)

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
    ## Vistas de páginas en Genius

    Genius es un centro de referencia para letras de canciones y análisis lírico, y con las letras autobiográficas de Taylor Swift que tienen metáforas extendidas y prosa poética, no es sorprendente que muchas de las canciones de Taylor reciban tráfico en Genius. Quiero ver qué álbumes o eras de canciones en general reciben más atención en Genius en función del tráfico que recibe cada canción de cada álbum/era. Utilizo dos enfoques para responder a esta pregunta:

    1. Sumo el número total de vistas de página para cada canción y las comparo entre sí para ver cuál es la más popular, así como trazo la distribución de frecuencia de las vistas de página en la discografía de Taylor.
    2. Represento gráficamente la distribución de las vistas de página mediante un diagrama de caja para comparar las medianas, medias y cualquier valor atípico que potencialmente influya en las conclusiones del enfoque anterior.
    """)
    df_views = pd.read_sql('SELECT * FROM song_views', connection)
    
    views_totals = toolkit.sql_to_string('views_totals.sql')
    era_views = pd.read_sql(views_totals, connection)
    toolkit.abbreviate_ttpd(era_views['era'])
    toolkit.abbreviate_ttpd(df_views['era'])
    toolkit.sort_cat_column(era_views, 'era', eras)
    toolkit.sort_cat_column(df_views, 'era', eras)

    views_fig, views_ax = charts.views_plots(custom_params, era_views, 'total_views', 'era', df_views, 'views', 
                                             'Song Page Views on Genius', 'Total Page Views per Era', 'Frequency Distribution of Page Views',
                                             'Total Page Views', 'Page Views', 'Album/Song Era', 'Song Count', ['#858ae3', '#613dc1'], 
                                             ['#4e148c', '#2c0735'], True, 'total_page_views_distribution.png')
    st.pyplot(views_fig)

    with st.expander("Ver discusión"):
        st.write("""
            A pesar de ser el álbum más recientemente lanzado, "The Tortured Poets Department" ha tomado la delantera con 47 millones de vistas totales de páginas, lo que son 20 millones más de vistas que "folklore" en segundo lugar. "Midnights" está en tercer lugar con 23.6 millones y "Lover" en cuarto lugar con 19.9 millones de vistas. De sus álbumes de estudio, su debut "Taylor Swift" tiene la menor cantidad de vistas con 2.1 millones, y solo sus colaboraciones con otros artistas tienen menos vistas con un total de 1.8 millones. De sus grabaciones nuevamente, "Red (Taylor's Version)" es el más popular con 8.4 millones de vistas, mientras que "Fearless (Taylor's Version)" es el menos popular con 3.3 millones de vistas. Es posible concluir a partir de este gráfico que "The Tortured Poets Department" es el álbum más popular de Taylor Swift en Genius en términos de tráfico a las canciones del álbum.

            Hay algunos problemas con este enfoque, como se ilustra en el histograma adjunto: los datos están sesgados hacia la derecha, con la mayoría de las páginas de canciones teniendo menos de 1 millón de vistas. Debido a esto, es probable que estos totales estén influenciados por valores atípicos, o canciones individuales con una gran cantidad de vistas. Para contrarrestar esto, trazamos las distribuciones y vemos cómo se comparan las medianas entre sí.
            """)

    view_box_fig, view_box_ax = charts.views_box(custom_params, df_views,'views', 'era', 'Genius Song Page View Distribution per Album/Song Category', 
                                                 'Page Views', 'Album/Song Era', '#7D7C78', '#3A3633', True, 'page_view_box_distribution.png')
    st.pyplot(view_box_fig)

    with st.expander("Ver discusión"):
        st.write("""
            Todas las eras de Taylor están influenciadas en cierta medida por valores atípicos en términos de vistas de página; todas sus medias (representadas por puntos blancos) caen a la derecha de sus medianas (representadas por las barras verticales en las cajas). El ejemplo más flagrante es "Red (Taylor's Version)", cuya canción "All Too Well (10 Minute Version) (Taylor’s Version) [From The Vault]" es la canción de Taylor Swift más vista en Genius con 4.7 millones de vistas, lo que representa casi la mitad de sus totales de vistas de página calculados en la visualización anterior.

            Al observar las medianas, "The Tortured Poets Department" tiene la más alta, lo que significa que en promedio las canciones de "The Tortured Poets Department" obtienen más vistas de página que las canciones de otros álbumes o eras, siendo la mediana alrededor de 1.5 millones de vistas por página. Con esta estadística, podemos argumentar que "The Tortured Poets Department" sigue siendo el álbum más popular de Taylor Swift en Genius, lo que coincide con la conclusión del enfoque anterior. Lo mismo podría decirse de "folklore", que es su segundo álbum más popular en Genius, con una mediana de alrededor de 1.4 millones de vistas por página de canción. Sin embargo, "reputation" tiene la tercera mediana más alta, alrededor de 1.1 millones de vistas por página de canción, lo que difiere del primer enfoque en el que "reputation" es el sexto álbum más popular con 17.2 millones de vistas totales de página. Esto significa que las canciones de "reputation" en promedio obtienen más vistas de página que otras páginas de canciones de diferentes álbumes/eras, incluso si el total del álbum es más bajo en general.

            En términos de medianas más bajas, los cuatro álbumes grabados de Taylor tienen vistas por página muy bajas, cada uno con alrededor de 0.1 millones (100,000) por canción, y todos los álbumes regrabados tienen medianas más bajas que sus contrapartes originales. Esto podría deberse a lo recientemente que se lanzaron los álbumes, ya que los álbumes originales han existido en Genius durante mucho más tiempo, pero en mi opinión es más probable que Genius sugiera las páginas de canciones de los álbumes originales con más frecuencia que las de sus contrapartes regrabadas cuando el usuario busca el título de la canción. La única era que es más baja que los álbumes regrabados es la de las canciones no pertenecientes a álbumes de Taylor, como las canciones de bandas sonoras de películas o sencillos promocionales, que tienen las medianas más bajas de vistas por página.
            """)

if __name__ == '__main__':
    main()

connection.close()