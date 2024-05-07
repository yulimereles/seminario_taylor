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

st.set_page_config(page_title="Collaborators")

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

credits = {
    'writer': '#6D466B',
    'producer': '#58A4B0',
    'artist': '#FF6B6C'}

rcParams, custom_params = toolkit.chart_params(rcParams)

# Creating several temporary tables to be used throughout
temp_tables = toolkit.sql_to_string('collab_temp_tables.sql')
cursor.executescript(temp_tables)

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
        <p style="text-align: center;">Los datos fueron actualizados por última vez el <b>{}</b>.</p>
        
        """.format(today_format), unsafe_allow_html=True)

@st.cache_data
def content():
    st.markdown("""
    ## Eras más colaborativas
    
    A lo largo de su carrera, Taylor Swift ha trabajado con numerosos escritores, productores y artistas para crear su catálogo musical, como se demuestra en los créditos de los músicos en cada canción. Sin embargo, algunos de sus álbumes y eras musicales en general son más colaborativos que otros; aunque un álbum puede no tener muchos artistas destacados, aún puede ser muy colaborativo en términos de escritura o producción. Para ver qué eras tuvieron en general más colaboradores que otras, utilizo dos enfoques:
    
    1. Cuento el número de escritores, productores y artistas *únicos* por canción y resumo por era. Luego calculo las medias para cada tipo de músico en todas las eras. Finalmente, comparo los totales por era con las medias para determinar cuáles son las eras más y menos colaborativas.
    2. Cuento el número *total* de escritores, productores y artistas por canción antes de resumir por era. Luego calculo la cantidad promedio de escritores, productores y artistas por canción para cada era, así como las medias generales para cada tipo de músico por canción. Finalmente, comparo los promedios de las eras con las medias generales para determinar cuáles son las eras más y menos colaborativas.
    """)
    
    unique_credit_per_era = toolkit.sql_to_string('unique_credit_per_era.sql')
    
    unique_credit = pd.read_sql(unique_credit_per_era, connection)
    toolkit.abbreviate_ttpd(unique_credit['era'])
    toolkit.sort_cat_column(unique_credit, 'era', eras)
    
    # Pivoting dataframe for chart table
    unique_credit_pivot = unique_credit.pivot(columns='era', index='type', values='unique_count')
    unique_credit_pivot.sort_values('type', ascending=False, inplace=True)
    
    # Calculating overall means for type
    avg_per_type_unique = unique_credit.groupby('type')['unique_count'].mean().sort_values(ascending=False)
    
    credits_total_fig, credits_total_ax = charts.credit_chart(credits, custom_params, 'bar', unique_credit, 'era', 'unique_count', 'type', 
                        avg_per_type_unique, 'Total Unique Musicial Credits per Era',
                        'Album/Song Era', '# per Era (Count)', 'Credit Type', True,
                        True, 'unique_credits_per_era.png', True, unique_credit_pivot)
    st.pyplot(credits_total_fig)
    
    with st.expander("Ver discusión"):
        st.write("""
            Al observar las barras, podemos ver claramente qué eras tuvieron más colaboradores únicos. Más que cualquier álbum o regrabación, Taylor trabaja con músicos más únicos cuando colabora en canciones de otros artistas o cuando crea canciones que no son parte de un álbum, ya que los totales de productores y artistas para lo primero y el total de escritores para lo segundo son más altos que cualquier otra era. Después de esos dos, está "Red (Versión de Taylor)", que tiene el segundo total más alto para cada artista y el tercero más alto tanto para productores como para escritores. Para los totales más bajos, "Speak Now (Versión de Taylor)" solo tiene 1 escritor único para la era, "Fearless" solo tiene 2 productores únicos y el álbum debut "Taylor Swift" solo tiene 1 artista único.
            
            Para determinar sus eras más y menos colaborativas, analizaremos dónde se encuentran los totales en relación con las medias generales por tipo (representadas por líneas horizontales punteadas). Para sus eras más colaborativas, tanto sus colaboraciones en canciones de otros artistas como sus trabajos no pertenecientes a álbumes están por encima de las medias para los tres tipos de músicos; "Red (Versión de Taylor)" también tiene totales por encima de las tres medias, siendo su único álbum de estudio o regrabación en lograrlo. Para las menos colaborativas, varias eras están por debajo de las medias generales para los tres tipos: el álbum homónimo "Taylor Swift", "Fearless", "Speak Now", "folklore", "evermore", "Speak Now (Versión de Taylor)", "1989 (Versión de Taylor)" y "The Tortured Poets Department". Esto dificulta determinar qué álbumes podrían considerarse los menos colaborativos.
            
            También tengo otros problemas al determinar la colaboración a través de este enfoque: uno de ellos es que no tiene en cuenta la duración de los álbumes y cómo eso puede afectar los recuentos de músicos únicos. Por ejemplo, "Red (Versión de Taylor)" tiene más de 30 canciones asociadas con la era, mientras que "folklore" y "evermore" solo tienen 17 cada uno; incluso si "folklore" y "evermore" presentaran escritores, productores y/o artistas únicos para cada canción, aún es posible que queden por debajo de "Red (Versión de Taylor)" en totales debido a tener menos canciones en general. Además, este método no tiene en cuenta la variabilidad entre canciones individuales en cuanto a escritores, productores o artistas. Por ejemplo, "Midnights" presenta una pista, "Lavender Haze", que tiene solo 6 escritores únicos, mientras que también presenta una pista, "Bigger Than the Whole Sky", que es escrita únicamente por Taylor. Esa variación no se tiene en cuenta al sumar los escritores únicos entre las dos pistas, lo cual seguiría siendo un total de 6.nicos entre las dos pistas, lo cual seguiría siendo un total de 6.a total of 6.
            
            Teniendo en cuenta estos problemas, llegué a mi segundo enfoque: calcular el promedio de cada tipo de músico por canción individual y comparar los promedios generales por era.
        """)
    
    avg_credit_per_song = toolkit.sql_to_string('avg_credit_per_song.sql')
    
    avg_credit = pd.read_sql(avg_credit_per_song, connection)
    toolkit.abbreviate_ttpd(avg_credit['era'])
    toolkit.sort_cat_column(avg_credit, 'era', eras)
    
    # Pivoting dataframe for chart table
    avg_credit_pivot = avg_credit.pivot(columns='era', index='type', values='avg_per_song')
    avg_credit_pivot.sort_values('type', ascending=False, inplace=True)
    
    # Calculating overall means for type-per-song
    avg_per_type = avg_credit.groupby('type')['avg_per_song'].mean().sort_values(ascending=False)
    
    avg_credits_fig, avg_credits_ax = charts.credit_chart(credits, custom_params, 'line', avg_credit, 'era', 'avg_per_song', 'type', 
                        avg_per_type, 'Average Number of Musicial Credits per Song by Era',
                        'Album/Song Era', '# per Song (Average)', 'Credit Type', True,
                        True, 'avg_credits_per_song.png', True, avg_credit_pivot)
    st.pyplot(avg_credits_fig)
    
    with st.expander("See discussion"):
        st.write("""
            Este enfoque analítico nos brinda una forma más matizada de ver qué eras fueron más colaborativas en términos de tipos de músicos individuales. Por ejemplo, tanto "reputation" como "Midnights" fueron eras altamente colaborativas, siendo la primera la que tiene el promedio más alto de escritores por canción (3.13 escritores) y la segunda la que tiene el promedio más alto de productores por canción (2.46 productores). Mientras tanto, tanto "Speak Now" como "Speak Now (Taylor's Version)" tienen el promedio más bajo de 1.1 y 1.0 escritores por canción respectivamente, siendo la regrabación escrita únicamente por Taylor, y el álbum autotitulado "Taylor Swift" tiene el promedio más bajo de 1.14 productores por canción, seguido de "evermore" con 1.41 productores. Sus colaboraciones con otros artistas tienden a ser más constantes, muchos álbumes tienen pocas colaboraciones vocales, pero "Red (Taylor's Version)" tiene el promedio más alto de sus álbumes de estudio y regrabaciones, con 1.22 artistas por canción. No sorprendentemente, esto es superado por sus canciones de colaboración en álbumes de otros artistas, que tienen un promedio de 1.87 artistas por canción y generalmente cuentan con otro artista junto a Taylor Swift., which have an average artist-per-song of 1.87 and usually feature another artist alongside Taylor Swift.

            Para determinar sus eras más y menos colaborativas, una vez más veremos dónde se encuentran los valores promedio en relación con las medias generales (representadas por líneas horizontales punteadas). Tres eras están por debajo de las tres medias: "Speak Now", "Red" y "folklore". Esto significa que, según este enfoque y el enfoque anterior, "Speak Now" y "folklore" se consideran las eras menos colaborativas de Taylor. Para la más colaborativa, "Lover" y "Midnights" tienen todos los valores por encima de las medias generales, lo que las convierte en las eras más colaborativas según este enfoque. Esto es especialmente interesante ya que ninguno de los dos álbumes se consideraba especialmente colaborativo en el enfoque anterior.

            Cualquier método que se utilice para determinar las eras más y menos colaborativas depende en última instancia de cada persona. Si bien ambos enfoques determinan la colaboración de diferentes maneras, solo puedo concluir que las eras menos colaborativas de Taylor Swift son "Speak Now" y "folklore" según los resultados de estos dos enfoques.
            """)
    
    st.markdown("""
    ## Colaboradores más frecuentes
    
    Incluso en algunas de sus eras menos colaborativas, Taylor Swift tiene varios músicos con los que trabaja regularmente para crear su música. Quiero ver con qué músicos colabora más Taylor, pero mi metodología necesita ser ajustada. Muchos de sus coescritores habituales también ayudan a producir sus canciones, lo que significa que si solo contáramos sus créditos musicales, podríamos contar accidentalmente dos veces a un músico por una canción. En cambio, cuento cuántas canciones trabajaron por era, sin importar si escribieron la canción, la produjeron, la cantaron o alguna combinación de las tres.
    
    Por brevedad, clasifico a cada colaborador de Taylor según el número total de canciones en las que trabajaron en toda su discografía, siendo el #1 el que más canciones trabajó, y selecciono a los doce músicos con los rangos más altos (habría seleccionado diez, pero hay un empate de cuatro vías y quiero incluirlos a todos).
    """)
    
    most_frequent_collabs = toolkit.sql_to_string('most_frequent_collaborators.sql')
    
    freq_collabs = pd.read_sql(most_frequent_collabs, connection)
    toolkit.abbreviate_ttpd(freq_collabs['era'])
    toolkit.sort_cat_column(freq_collabs, 'era', eras)
    
    collab_totals = freq_collabs.loc[:,('collaborator', 'total_songs')]
    collab_totals.drop_duplicates('collaborator', inplace=True)
    collab_totals.sort_values('collaborator', inplace=True)
    collab_totals.set_index('collaborator', inplace=True)
    
    freq_collabs_fig, freq_collabs_ax = charts.collab_heatmap(custom_params, freq_collabs, 'era', 'collaborator', 'songs', 'sum', 
                   'Most Frequent Collaborators per Era', 'Album/Song Era', 'Collaborator Name', 
                   True, True, 'most_frequent_collabs_per_era.png', table_bool=True, table_df=collab_totals)
    st.pyplot(freq_collabs_fig)
    
    with st.expander("See discussion"):
        st.write("""
            A partir de este mapa de calor, podemos ver en qué eras los colaboradores más frecuentes de Taylor trabajaron en la mayoría de las canciones. Jack Antonoff tiene una clara ventaja, colaborando en un total de 87 canciones en toda la discografía de Taylor, con 21 canciones solo en "Midnights". También podemos ver en qué momento Jack comenzó a trabajar con Taylor; sus primeras colaboraciones fueron durante "1989" y desde entonces ha sido un colaborador habitual en cada álbum de estudio y regrabación.
            
            Mientras tanto, el colaborador número 2, Nathan Chapman, deja de trabajar con Taylor poco después de que ella haga la transición de la música country al pop, solo trabajando en 1 canción durante "1989" a pesar de ser acreditado varias veces en sus álbumes anteriores. Curiosamente, no regresa para producir las canciones en las versiones regrabadas de "Fearless", "Speak Now" y "Red". Esto a pesar de que varios colaboradores de los álbumes originales regresan para las versiones regrabadas, como Liz Rose para "Fearless (Taylor's Version)" y Max Martin y Shellback para "1989 (Taylor's Version)". En cambio, Christopher Rowe, el colaborador número 3 de Taylor, parece intervenir para hacer la mayor parte de las colaboraciones en las versiones regrabadas, a pesar de no haber trabajado con Taylor antes de "Fearless (Taylor's Version)".
            """)

if __name__ == '__main__':
    main()

connection.close()