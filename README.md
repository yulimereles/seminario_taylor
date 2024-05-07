# taylor-swift-discography
Este repositorio contiene un proyecto en curso para compilar y analizar la discografía de Taylor Swift, incluyendo todas las canciones que ha escrito para otros artistas. Todos los datos, incluyendo las letras, se obtienen inicialmente de [Genius](https://genius.com/) a través de [parsel](https://parsel.readthedocs.io/) y se colocan en una base de datos SQLite. Las consultas SQL transforman los datos a través de [pandas](https://pandas.pydata.org/) y [sqlite3](https://docs.python.org/3/library/sqlite3.html) antes de ser visualizados mediante [matplotlib](https://matplotlib.org/) y [seaborn](http://seaborn.pydata.org/index.html).

**Ten en cuenta que este proyecto está en desarrollo y aún no está completo.**

## Este proyecto está actualmente desplegado en [Streamlit](https://taylor-swift-discography.streamlit.app/)!

![streamlit gif](./figures/streamlit_demo.gif)

## Directorio
* **[app](./app)**: contiene archivos de aplicación para la aplicación Streamlit
* **[assets](./assets)**: contiene activos de terceros
  * **[fonts](./assets/fonts)**: contiene archivos de fuente `ttf` utilizados en gráficos (cortesía de [Google Fonts](https://fonts.google.com/))
  * **[img](./assets/img)**: contiene archivos de imagen utilizados en la aplicación
* **[data](./data)**: contiene versiones en pickle de los datos de web scraping, tanto en bruto como limpios, así como el archivo de base de datos SQLite
  * **[csv](./data/csv)**: contiene archivos CSV utilizados para agregar/eliminar datos del dataframe
  * **[kaggle](./data/kaggle)**: contiene archivo CSV utilizado para el [conjunto de datos de Kaggle](https://www.kaggle.com/datasets/madroscla/taylor-swift-released-song-discography-genius)
* **[figures](./figures)**: contiene imágenes del proyecto, incluyendo el esquema de la base de datos (cortesía de [dbdiagram.io](https://dbdiagram.io))
  * **[charts](./figures/charts)**: contiene todos los gráficos de matplotlib/seaborn creados
* **[notebooks](./notebooks)**: contiene todos los cuadernos de Jupyter
  * **[data_collection.ipynb](./notebooks/data_collection.ipynb)**: web scraping inicial desde Genius utilizando parsel, creando dataframes y base de datos de canciones y letras de Taylor Swift
* **[sql](./sql)**: contiene todas las consultas SQL utilizadas en el proyecto (nota: están escritas en SQL de SQLite)
* **[src](./src)**: contiene todos los módulos de Python utilizados en el proyecto

## Restricciones y Limitaciones de la Discografía
Esta discografía prioriza la cobertura de *canciones* sobre la cobertura de *álbumes*; esto significa que se prefieren las versiones de lujo de los álbumes con más canciones sobre las versiones estándar, y que se prefieren los lanzamientos de álbumes sobre los lanzamientos de sencillos/EP. Si bien no se cubrirán todas las versiones de lanzamiento de una canción en este conjunto de datos, se incluye cada canción única. Las canciones regrabadas se cuentan como entradas separadas de sus versiones originales.

Consulta la tabla a continuación para obtener más información sobre lo que se incluye y lo que no se incluye en la discografía:

| Incluido en la Discografía | No incluido en la Discografía |
| -- | -- |
| Canciones lanzadas en los álbumes de estudio de Taylor Swift | Entradas duplicadas de canciones (por ejemplo, para lanzamiento como sencillo, lanzamiento de álbum, lanzamiento de álbum de lujo, etc.) |
| Canciones lanzadas en los álbumes regrabados "Taylor's Version" de Taylor Swift | Canciones no lanzadas/filtradas y demos |
| Canciones de Taylor Swift para bandas sonoras o lanzadas como sencillos/EP no pertenecientes a un álbum | Versiones de canciones de Taylor Swift interpretadas por otros artistas |
| Remixes de canciones de Taylor Swift con nuevos artistas intérpretes | Remixes/versiones acústicas de canciones que no incluyen nuevos artistas intérpretes |
| Canciones escritas por Taylor Swift para otros artistas, incluso si no la incluyen como intérprete | Versiones en vivo de canciones/mashups de canciones ya contabilizadas |
| Canciones de otros artistas con la participación de Taylor Swift | Canciones que muestren/interpolen canciones de Taylor Swift, incluso si la incluyen como escritora o colaboradora |
| Covers de canciones de Taylor Swift interpretadas por ella o con su participación que hayan sido grabadas y lanzadas oficialmente | Canciones que solo existen en formato de video (DVD, grabación de espectáculo en vivo, etc.) |
#   s e m i n a r i o _ t a y l o r  
 