#funciones de limpieza del contenido
def clean_text_round1(text: str) -> str:
    """Limpieza del texto, donde se eliminan signos, saltos de linea, tildes y otros caracteres especiales.

    Args:
        text (str): texto que se desea limpiar

    Returns:
        str: texto limpio
    """
    import re
    import string
    text = text.lower()
    text = re.sub('\[.*?¿\]\%@', ' ', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), ' ', text) 
    text = re.sub('\w*\d\w*', '', text) 
    text = re.sub("ú","u", text)
    text = re.sub("ó","o", text)
    text = re.sub("á","a", text)
    text = re.sub("é","e", text)
    text = re.sub("ñ","n", text)
    return text
def limpieza1(df):
    """Dado el data frame que deseas limpiar, limpia la columna llamada Contenido

    Args:
        df (_type_): Dataframe con columna contenido que se desea limpiar

    Returns:
        _type_: Dataframe limpio
    """
    import pandas as pd
    round1 = lambda x: clean_text_round1(x)
    data_clean = pd.DataFrame(df.Contenido.apply(round1))
    return data_clean
def clean_text_round2(text: str) -> str:
    """Limpieza del texto, donde se eliminan signos y el simbolo '\n'

    Args:
        text (str): texto que se desea limpiar

    Returns:
        str: tetxo limpio
    """
    import re
    import string
    text = re.sub('[‘’“”…«»]', '', text)
    text = re.sub('\n', ' ', text)
    return text

def limpieza2(data_clean):
    """Dado el data frame que deseas limpiar, limpia la columna llamada Contenido

    Args:
        df (_type_): Dataframe con columna contenido que se desea limpiar

    Returns:
        _type_: Dataframe limpio
    """
    import pandas as pd
    round2 = lambda x: clean_text_round2(x)
    data_clean = pd.DataFrame(data_clean.Contenido.apply(round2))
    return data_clean

def limpieza_total(df):
    """Unión de las dos limpiezas en una unica función

    Args:
        df (_type_):  Dataframe con columna contenido que se desea limpiar

    Returns:
        _type_: Dataframe limpio
    """
    data_clean = limpieza1(df)
    data_clean = limpieza2(data_clean)
    return data_clean

def create_frequency_matrix(descripciones) -> dict:
    """Dado el contenido que se quiere analizar, se crea la matriz de frecencia de palabras en cada sentencia/contenido.

    Args:
        descripciones (_type_): Contenido que se desea analizar

    Returns:
        dict: Diccionario en el que cada sentencia es la clave y el valor es cada palabra y su frecuencia
    """
    from nltk.tokenize import sent_tokenize, word_tokenize
    from nltk.corpus import stopwords
    from nltk import FreqDist
    from sklearn.feature_extraction.text import TfidfVectorizer
    import matplotlib.pyplot as plt
    import numpy as np
    from sklearn.feature_extraction.text import CountVectorizer
    frequency_matrix = {}
    stopWords = set(stopwords.words("spanish"))
    indice = 0

    for desc in descripciones:
        freq_table = {}
        words = word_tokenize(desc)
        for word in words:
            word = word.lower()
            if word in stopWords:
                continue

            if word in freq_table:
                freq_table[word] += 1
            else:
                freq_table[word] = 1

        frequency_matrix[str(indice)] = freq_table
        indice += 1
    return frequency_matrix

def create_tf_matrix(freq_matrix:dict)-> dict:
    """Calcula el termino de frecuencia TF, que se calcula dividiendo el numero de veces que aparece el termino en un documento entre el numero total de 
    terminos en el documento.

    Args:
        freq_matrix (dict): Diccionario con la frecuencia de las palabras (frequency_matrix)

    Returns:
        dict: Diccionario en el que cada sentencia es la clave y el valor es cada palabra y su porcentaje de frecuencia
    """
    from nltk.tokenize import sent_tokenize, word_tokenize
    from nltk.corpus import stopwords
    from nltk import FreqDist
    from sklearn.feature_extraction.text import TfidfVectorizer
    import matplotlib.pyplot as plt
    import numpy as np
    import nltk
    from sklearn.feature_extraction.text import CountVectorizer
    tf_matrix = {}

    for desc, f_table in freq_matrix.items(): 
        tf_table = {}
        count_words_in_desc = len(f_table) 
        for word, count in f_table.items():
            tf_table[word] = count / count_words_in_desc 

        tf_matrix[desc] = tf_table
    return tf_matrix

def create_documents_per_words(freq_matrix:dict)->dict:
    """Calculo de en cuantos documentos aparece cada palabra

    Args:
        freq_matrix (dict): Diccionario con la frecuencia de las palabras (frequency_matrix)

    Returns:
        dict: Diccionario en el que cada palabra es la clave y el valor en cuantos documentos aparece
    """
    from nltk.tokenize import sent_tokenize, word_tokenize
    from nltk.corpus import stopwords
    from nltk import FreqDist
    from sklearn.feature_extraction.text import TfidfVectorizer
    import re
    import math
    import matplotlib.pyplot as plt
    import numpy as np
    import nltk
    from sklearn.feature_extraction.text import CountVectorizer
    word_per_doc_table = {}

    for dok, f_table in freq_matrix.items():
        for word, count in f_table.items():
            if word in word_per_doc_table:
                word_per_doc_table[word] += 1
            else:
                word_per_doc_table[word] = 1

    return word_per_doc_table

def create_idf_matrix(freq_matrix: dict, count_doc_per_words: dict, total_documents: int) -> dict:
    """Calculo del término IDF (como de habitual es una palabra en los documentos)

    Args:
        freq_matrix (dict): Diccionario con la frecuencia de las palabras (frequency_matrix)
        count_doc_per_words (dict): Diccionario en el que cada palabra es la clave y el valor en cuantos documentos aparece
        total_documents (int): Número de contenidos

    Returns:
        dict: Diccionario en el que cada sentencia es la clave y el valor es cada palabra y su IDF
    """
    from nltk.tokenize import sent_tokenize, word_tokenize
    from nltk.corpus import stopwords
    from nltk import FreqDist
    from sklearn.feature_extraction.text import TfidfVectorizer
    import re
    import math
    import matplotlib.pyplot as plt
    import numpy as np
    import nltk
    from sklearn.feature_extraction.text import CountVectorizer
    idf_matrix = {}

    for desc, f_table in freq_matrix.items():
        idf_table = {}

        for word in f_table.keys():
            idf_table[word] = math.log10(total_documents / float(count_doc_per_words[word])) 

        idf_matrix[desc] = idf_table

    return idf_matrix

def create_tf_idf_matrix(tf_matrix:dict, idf_matrix:dict) -> dict:
    """Calculo del termino TF-IDF, multiplicando el porcentaje de aparicion de una palabra por el término IDF

    Args:
        tf_matrix (dict): Diccionario en el que cada sentencia es la clave y el valor es cada palabra y su porcentaje de frecuencia
        idf_matrix (dict): Diccionario en el que cada sentencia es la clave y el valor es cada palabra y su IDF

    Returns:
        dict: Diccionario en el que cada sentencia es la clave y el valor es cada palabra y su TF-IDF
    """
    from nltk.tokenize import sent_tokenize, word_tokenize
    from nltk.corpus import stopwords
    from nltk import FreqDist
    from sklearn.feature_extraction.text import TfidfVectorizer
    import re
    import math
    import matplotlib.pyplot as plt
    import numpy as np
    import nltk
    from sklearn.feature_extraction.text import CountVectorizer
    tf_idf_matrix = {}

    for (desc1, f_table1), (desc2, f_table2) in zip(tf_matrix.items(), idf_matrix.items()):

        tf_idf_table = {}

        for (word1, value1), (word2, value2) in zip(f_table1.items(),
                                                    f_table2.items()):  # here, keys are the same in both the table
            tf_idf_table[word1] = float(value1 * value2)

        tf_idf_matrix[desc1] = tf_idf_table

    return tf_idf_matrix