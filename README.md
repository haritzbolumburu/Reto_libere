# Reto_06_Morado
Repositorio en GitHub con el proyecto del equipo morado.
La estructura del repositorio:
En el repositorio, se disponen dos tipos de archivos *.py* y *.ipynb* en ambas empleamos el lenguaje de programación **Python**. El repositorio consta de cuatro apartados:
- En la pantalla principal, se encuentran todos los scripts en los que se realiza el proyecto y el enviromnent empleado, el orden de carga el el siguiente:
    1. Primero desde la terminal hay que hacer la activación del entorno, a traves del comando, *conda env create -f environment_Reto06_Morado.yml* y una vez hecho esto activar el environment. Además, para la carga del webscraping hay que descargarse un driver de Firefox, del siguiente github https://github.com/mozilla/geckodriver/releases.
    2. Segundo desde la misma terminal cargaremos el primer archivo .py, en el que se realiza el procesamiento, la creación de variables y el guardado del nuevo csv, que se empleara en los demas procesos. Esto se hará a traves del comando, *python 01-Ingesta_Limpieza.py*.
    3. Una vez guardado el csv, abrimos la carpeta en VSCode y podemos comenzar con la carga de los notebooks. El primer archivo a cargar es el de *02-elastic_DatosLimpios.ipynb*, donde cada uno deberá poner su contraseña y arrancar elastic en la terminal.
    4. Lo siguiente, será comenzar con la carga de los notebook del webscraping: *03-web_scraping_Atracciones.ipynb*, *07-web_scraping_Clima.ipynb*, *04-web_scraping_Hoteles.ipynb*, *06-web_scraping_Opiniones.ipynb* y *05-web_scraping_Restaurantes.ipynb*.
    5. Despues de esto, los datos sobre el clima se subiran a elastic para su posterior uso en el modelado, para ello se debe seguir el mismo proceso que en el tercer paso, y cargar *08-elastic_DatosClima.ipynb*
    6. Después, hay que hacer las cargas donde se realiza el modelado mediante el notebook *09-modelado_entrenamiento.ipynb*.
    7. Los df train y test se subirán a elasticsearch junto con los modelos, mediante el notebook *10-elastic_Modelado.ipynb*.
    8. A continuación, se sacan los resultados del mejor modelo, filtrando los mejores, mediante la carga del notebook *11-modelo_seleccion.ipynb*
    9. Tras el modelado, se da paso a la segmentacion de clientes mediante la carga de los notebook *12-clustering.ipynb* y *13-perfil_abandonista*
    10. Por lo que se subirán a elasticsearch mediante la carga del notebook *14-elastic_Clustering.ipynb*
    11. Por último, se cargara el notebook de los gráficos en *15-Visualizacion.ipynb*
- En la carpeta packages, hay tres carpetas diferentes, donde se crean las funciones empleadas para cada apartado.
- En la carpeta Datos, hay dos carpetas una con los datos originales y otro con los trasnformados.
- En la carpeta Graficos, se guardan algunos de los graficos que se crean durante el proyecto.
