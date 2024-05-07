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

st.set_page_config(page_title="Release Overview")

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

rcParams, custom_params = toolkit.chart_params(rcParams)

# Creating temporary table to be used throughout
temp_table = toolkit.sql_to_string('release_temp_table.sql')
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
        <h3 style="text-align: center;">Taylor Swift - Discografía de Canciones</h3>

        <p style="text-align: center;">Este es un proyecto en curso y de código abierto. ¡Sigue el progreso en <a href='https://github.com/madroscla/taylor-swift-discography'>Github</a>!</p>

        <p style="text-align: center;">Los datos fueron actualizados por última vez el <b>{}</b>.</p>
        
        """.format(today_format), unsafe_allow_html=True)

@st.cache_data
def content():
    st.markdown("""
    ## Formatos de Lanzamiento de Canciones

    Taylor Swift actualmente tiene más de 350 canciones en su discografía: muchas han sido lanzadas en sus álbumes de estudio, pero una cantidad significativa ha sido lanzada en otros formatos. Para visualizar mejor su discografía, he categorizado sus canciones en cuatro grupos basados en el formato de lanzamiento: canciones en sus álbumes de estudio (incluyendo versiones deluxe), canciones en sus álbumes regrabados, canciones en álbumes de otros artistas (sin incluir bandas sonoras) y cualquier otro formato de lanzamiento misceláneo como EPs, sencillos promocionales o lanzamientos de bandas sonoras.
    """)
    
    release_formats = toolkit.sql_to_string('release_formats.sql')
    
    formats = pd.read_sql(release_formats, connection)
    formats_table = formats.set_index('classification')

    formats_fig, formats_ax = charts.formats_pie(custom_params, formats, 'total_songs', 'classification', 'Song Release Formats', 
                                             ['#f6fff8', '#eaf4f4', '#cce3de', '#a4c3b2'], True, 'release_formats.png', True, formats)
    
    st.pyplot(formats_fig)

    with st.expander("Ver discusión"):
        st.write("""
            A partir de este gráfico circular, podemos ver claramente que las canciones lanzadas en álbumes de estudio constituyen la gran mayoría de la discografía de Taylor, representando más del 59%. Curiosamente, casi un tercio de su discografía incluye las versiones regrabadas de sus canciones anteriores, a pesar de haber comenzado su proceso de regrabación en los últimos cinco años. Las contribuciones en álbumes de otros artistas y los lanzamientos misceláneos solo representan un pequeño porcentaje de su discografía, siendo menos del 13% en total.
            """)

    st.markdown("""
    ## Fechas de Lanzamiento de Canciones

    Con una carrera de casi 18 años, Taylor Swift a menudo lanza música en las mismas épocas del año e incluso en los mismos días que lanzamientos anteriores. Desde el comienzo de la década de 2020 y el inicio de su proceso de regrabación, la cantidad de lanzamientos por año ha sido mucho mayor que en el pasado. Para ver los patrones generales en las fechas de lanzamiento, visualizo dos métricas:

    1. Grafico las distribuciones de frecuencia para los años de lanzamiento, los meses de lanzamiento y los días de lanzamiento de forma independiente, para ver en qué años, meses y días Taylor ha lanzado la mayor parte de su música.
    2. Grafico los meses de lanzamiento en función de los días de lanzamiento para encontrar las fechas más comunes en las que Taylor tiende a lanzar música.
    """)
    release_dates_split = toolkit.sql_to_string('release_dates_split.sql')
    releases = pd.read_sql(release_dates_split, connection)

    releases_fig, releases_ax = charts.release_hist(custom_params, releases, 'year', 'month', 'day', 'Frequency Distributions of Song Release Dates', 
                                             'Release Years', 'Release Months', 'Release Days', 'Year', 'Month', 'Day of Month', 'Song Count', 
                                             ['#d00000', '#e85d04', '#faa307'], ['#6a040f'], True, 'release_dates_distribution.png')
    st.pyplot(releases_fig)

    with st.expander("Ver discusión"):
        st.write("""
            En cuanto a sus años más productivos, Taylor ha lanzado la mayor parte de su música entre 2019 y 2024. Este rango tiene sentido, ya que Taylor no solo lanzó dos álbumes de estudio en 2020, sino que también comenzó su proceso de regrabación, lanzando dos álbumes regrabados tanto en 2021 como en 2023. Fuera de este rango, su año más productivo fue 2012 con el lanzamiento de su álbum de estudio "Red", junto con algunas colaboraciones en la banda sonora de la película "The Hunger Games". Su año menos productivo fue 2015, con solo una canción lanzada, seguido de un empate entre 2013, 2016 y 2018. Estos tres años estuvieron entre los lanzamientos de álbumes de estudio de Taylor, quien generalmente estaba de gira internacionalmente, por lo que no es sorprendente ver que estos años tuvieran lanzamientos limitados. Aún así, es interesante comparar estos años de gira con su constante productividad en 2023 y 2024, a pesar de estar de gira en el Eras Tour.

            En cuanto a los meses más productivos, Taylor tiende a lanzar sus canciones en octubre, con casi un tercio de su catálogo completo lanzado en ese mes. Otros meses de alta actividad son noviembre, abril y julio, con 60, 59 y 41 canciones lanzadas respectivamente. No suele lanzar música en febrero, junio o enero, el primero solo tiene 3 lanzamientos de canciones y los dos últimos tienen 5 lanzamientos de canciones cada uno. Taylor también tiende a lanzar canciones más tarde en el mes, la mayoría se lanzan entre el día 19 y el día 27 del mes. También tiende a lanzar canciones los días 12, 7, 9 y 11 del mes, dentro de las primeras dos semanas del mes.
            """)

    month_day_distribution = toolkit.sql_to_string('month_day_distribution.sql')
    month_day = pd.read_sql(month_day_distribution, connection)
    dates = month_day.sort_values(by=['count'], ascending=False)
    dates = dates[['date', 'count']].head(10)

    freq_dates_fig, freq_dates_ax = charts.date_scatter(custom_params, month_day, 'month', 'day', 'count', 'Most Frequent Release Dates', 
                                                        'Month', 'Day of Month', True, 'most_frequent_dates.png', True, dates)
    st.pyplot(freq_dates_fig)

    with st.expander("See discussion"):
        st.write("""
            El patrón previamente observado de lanzamientos en octubre sigue apareciendo al trazar los meses de lanzamiento contra los días de lanzamiento, con tres fechas diferentes en octubre entre las 10 fechas de lanzamiento más frecuentes: 21/10, 22/10 y 27/10, siendo esta última la que tiene la mayor cantidad de lanzamientos de canciones. Los otros meses que tuvieron distribuciones de lanzamiento altas cuando se trazaron de forma independiente también aparecen en las 10 primeras: 9/4 y 19/4 para abril, 7/7 y 24/7 para julio, y 12/11 para noviembre. Estas fechas de lanzamiento también coinciden con el patrón de Taylor de lanzar música entre los días 19 y 27 del mes o dentro de las primeras dos semanas del mes.
            """)

if __name__ == '__main__':
    main()

connection.close()