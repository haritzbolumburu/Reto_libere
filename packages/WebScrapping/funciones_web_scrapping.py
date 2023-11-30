# librerias

import time
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import pandas as pd

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk import FreqDist
from sklearn.feature_extraction.text import TfidfVectorizer

import matplotlib.pyplot as plt
import numpy as np
import nltk
from sklearn.feature_extraction.text import CountVectorizer
import datetime as dt

def paginacion(url:str)-> list:
    """Dada una url coge las urls del boton siguiente

    Args:
        url (str): Url inicial

    Returns:
        list: Lista con todas las urls
    """

    urls = [url]
    respuesta = requests.get(url)
    while True:
        soup = BeautifulSoup(respuesta.text, 'lxml')
        next_page = soup.find('a', class_='next')
        if next_page:
            next_url = next_page.get('href') 
            urls.append(next_url)
        else:
            break
        respuesta = requests.get(next_url)
    return urls


#WEB SCRAPPING DE LAS ATRACCIONES / QUE VER
#funcion para coger el link inicial
def que_ver_link(url:str)-> str:
    """Sacar de la pagina principal el link donde se encuentran las atracciones y que ver en cada ciudad

    Args:
        url (str): Url de la pagina principal de la ciudad

    Returns:
        str: Url de las atracciones y que ver en la ciudad
    """

    response = requests.get(url)
    soup= BeautifulSoup(response.text, 'html.parser')
    enlaces = soup.find("a", {"class":"link"})
    links = []
    links.append(enlaces.get('href'))
    link_string=''.join(links)
    return link_string
#funcion para coger los links de cada atraccion
def links_paginas_atraccion(lista: list) -> list:
    """Dado una lista con todos los urls, saca de cada uno los links, 250 como máximo, que te llevan a la información de cada atraccion

    Args:
        lista (list): Lista con los urls de las paginas de previsualización de las atracciones

    Returns:
        list: Lista con los urls de cada atracción
    """

    enlaces_paginas=[]
    for i in lista[0:250]:
        response = requests.get(i)
        soup= BeautifulSoup(response.text, 'html.parser')
        enlaces = soup.find_all(target='_self')
        enlaces_paginas.append(enlaces)
    enlaces_paginas_limpios=[]
    for i in enlaces_paginas:
        for a in i:
            enlaces_paginas_limpios.append(a.get('href'))
    return enlaces_paginas_limpios 
#funcion para sacar las reseñas de cada atraccion
def reseñas(lista_urls: list)-> list:
    """Cada las reseñas de cada atracción

    Returns:
        list: Lista con las reseñas de las atracciones
    """

    reseñas_1=[]
    for i in lista_urls[0:250]:
        response = requests.get(i)
        soup= BeautifulSoup(response.text, 'html.parser')
        reseñas=soup.find_all('div',{"class":"experiencesContainer"})
        reseñas_1.append(reseñas)
    reseñas_limpias=[]
    for i in reseñas_1:
        for a in i:
            reseñas_limpias.append(a.text.replace('\n', ''))
            reseñas_limpias
    return reseñas_limpias

#WEB SCRAPPING DE LOS HOTELES / DONDE DORMIR
def hoteles_principal(ciudad: str, url: str):
    """Dado el link de donde dormir en la ciudad, saca las opiniones principales, de los 15 hoteles prioritarios, con más opiniones y más puntuación

    Args:
        ciudad (str): Nombre de la ciudad
        url (str): Url de donde dormir en esa ciudad

    Returns:
        _type_: Dataframe con las tres opiniones más destacadas
    """
 
    
    driver = webdriver.Firefox('/home/bdata2/Descargas/geckodriver-v0.32.0-linux64')
    driver.maximize_window()
    time.sleep(8)
    driver.get(url)
    time.sleep(10)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    hoteles = soup.find_all("div", class_="hotelQuotes")
    opiniones = []
    for hotel in hoteles:
        opiniones.append(hotel.text.replace('\n', '')[3:].split('" "'))
    df_opiniones = pd.DataFrame()
    df_opiniones = df_opiniones.append(opiniones)
    df_opiniones['ciudades'] = ciudad
    df_opiniones.columns = ['opinion1', 'opinion2', 'opinion3', 'ciudad']
    return df_opiniones

#WEB SCRAPPING DE LAS ATRACCIONES / QUE VER
#función que coge los links de los restaurantes
def links_restaurantes(url:str) -> list:
    """Dado el link de donde se encuentra la previsualización de los restaurantes saca los links de los restaurantes

    Args:
        url (str): Url con los restaurantes

    Returns:
        list: Lista con los urls de los restaurantes
    """

    respuesta = requests.get(url)
    soup = BeautifulSoup(respuesta.text, 'lxml')
    enlaces = []
    for enlace in soup.find_all('a', class_ = "titleItem"):
        enlaces.append(enlace.get('href'))
    enlaces_restaurante=[]
    for restaurante in enlaces:
        if 'rincon' in restaurante:
            enlaces_restaurante.append(restaurante) 
    return enlaces_restaurante
#función que lee la opinion de los restaurantes
def lectura_opiniones(url_restaurante:str) -> list:
    """Saca las reseñas de los restaurantes

    Args:
        url_restaurante (str): Url del restaurante

    Returns:
        list: Lista con las opiniones de los restaurantes
    """

    respuesta = requests.get(url_restaurante)
    soup = BeautifulSoup(respuesta.text, 'lxml')
    opiniones = []
    for i in soup.find_all('div', class_ = 'content'):
            opiniones.append(str(i.p).replace('<p>', '').replace('</p>', '').replace('<br/>', ''))
    return opiniones
#automatización de todo lo anterior
def restaurantes_opinion(url:str):
    """Proceso completo para sacar las opiniones de los restaurantes de una ciudad

    Args:
        url (str): Link principal de donde comer en la ciudad

    Returns:
        _type_: Data Frame con el contenido/opiniones de los restaurantes
    """

    urls = paginacion(url)
    enlaces_restaurante = []
    for url in urls[0:10]:
        enlaces_restaurante.extend(links_restaurantes(url))
    opiniones_restaurantes = []
    for url_restaurante in enlaces_restaurante[0:250]:
        opiniones_restaurantes.extend(lectura_opiniones(url_restaurante))
    opiniones_restaurantes = pd.DataFrame(opiniones_restaurantes)
    opiniones_restaurantes.columns = ['Contenido']
    return opiniones_restaurantes




def crear_tabla(url):
    response = requests.get(url)
    #sacamos el mes
    posicion = url.index('month&month=')+12
    mes = url[posicion:]
    mes = str(mes)
    #sacamos la ciudad
    posicion2 = url.index('?page=month&month')
    posicion1 = url.rfind('/')
    ciudad = url[posicion1+1:posicion2]
    #comenzamos con el scrapping
    soup = BeautifulSoup(response.text, 'html.parser')
    tabla = soup.find_all("table", {"class": "calendar_table"})
    calendario = pd.read_html(str(tabla))
    calendario = pd.concat(calendario)
    calendario = calendario.fillna('---')
    maximas = []
    minimas = []
    dias = []
    for dia in calendario:
        for semana in range(0,5):
            if calendario[dia][semana]!= '---':
                dias.append(calendario[dia][semana].replace('/', '').split()[0])
                maximas.append(calendario[dia][semana].replace('/', '').split()[1])
                minimas.append(calendario[dia][semana].replace('/', '').split()[2])
            else:
                continue
    dias = list(map(int, dias))
    imagenes = soup.find_all("img", {"class": "calendar_day_image"})
    datos = {
        'dia_mes': dias,
        'temp_max': maximas,
        'temp_min': minimas
    }
    df = pd.DataFrame(datos)
    df_bc = df.copy()
    df = df.set_index('dia_mes')
    df = df.sort_index()
    df = df.reset_index()
    imagenes = soup.find_all("img", {"class": "calendar_day_image"})
    clima = []
    for dia in imagenes:
        clima.append(dia.get('alt'))
    df['clima'] = clima
    fechas = []
    for dia_mes in df['dia_mes']:
        dia = str(dia_mes)
        fecha = dia+'/'+mes+'/2022'
        fecha_dt = dt.datetime.strptime(fecha, '%d/%B/%Y')
        fechas.append(fecha_dt)
    df['fecha']=fechas
    df['ciudad']=ciudad
    return df


def review_score(url:str) ->dict:
    response=requests.get(url)
    soup=BeautifulSoup(response.text)
    review=[]
    for i in soup.select("p[class*='review_score_name']"):
        review.append(i.text)
    score=[]
    for i in soup.select("p[class*='review_score_value']"):
        score.append(i.text)
    
    dicc={}
    for i in range(0,len(review)):
        dicc[review[i]]=score[i]
    
    return dicc


def opiniones(url:str) ->list:
    response=requests.get(url)
    soup=BeautifulSoup(response.text)
    lista=[]
    num=1
    while num<4:
        for i in soup.select("p[class*='review_neg']"):
            lista.append(i.text)

        enlace=[]

        for siguente in soup.select("p[class*='page_link review_next_page']"):
            enlace.append(siguente.a.get('href'))
        enlace="https://www.booking.com"+str(enlace[0])
        response=requests.get(enlace)
        soup=BeautifulSoup(response.text)
        num+=1
    return lista


