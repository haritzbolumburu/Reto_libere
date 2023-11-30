# librerias
from sklearn.feature_extraction.text import CountVectorizer
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#funcion que crea un unico wordcloud para todos los contenido
def nube_de_palabras_global(df,stop_words=[]):
    total = df['Contenido'].cumsum()[len(df['Contenido'])-1]
  

    wc = WordCloud(stopwords=stop_words, background_color="white", colormap="Dark2",
               max_font_size=150, random_state=42)
    wc.generate(total)
    plt.imshow(wc, interpolation="bilinear")
    return plt.show()

#funcion que crea wordclouds
def nube_de_palabras(df,stop_words=[]):

    wc = WordCloud(stopwords=stop_words, background_color="white", colormap="Dark2",
               max_font_size=150, random_state=42)

    plt.rcParams['figure.figsize'] = [14,16]

    for index in np.arange(0,6):    
        wc.generate(df.Contenido[index])
        plt.subplot(4, 3, index+1)
        plt.imshow(wc, interpolation="bilinear")
        plt.axis("off")
    return plt.show()


def grafico_palabras_general(df, stopwords = []):
    vectorizer = CountVectorizer(stop_words=stopwords)
    X = vectorizer.fit_transform(df.Contenido)
    data_dtm = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names()) 
    data_dtm.index = df.index
    data_dtm
    counts = data_dtm.sum(axis=0).sort_values(ascending=False)[0:30]
    counts = pd.DataFrame(counts)
    counts.columns = ['Counts']
    f = plt.figure()
    f.set_figwidth(10)
    f.set_figheight(5)
    counts.set_index(counts.index).Counts.plot(kind='bar')