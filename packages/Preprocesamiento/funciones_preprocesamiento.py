#analisis de df
def informacion_inicial(df):
    """Dado un dataframe se da la información principal para un primer analisis general

    Args:
        df (_type_): Dataframe que se desa analizar

    Returns:
        _type_: Dataframe de 5 instancias aleatorias del dataframe dado
    """
    print(f'La forma del dataframe es {df.shape}, es decir tiene {len(df.columns)} columnas y {len(df.index)} filas.')
    print(f'A continuación se muestra los nombres de las columnas, junto con el tipo de variable:')
    print(df.dtypes)
    print(f'Además se dispone de un analisis más profundo que nos ayude a conseguir una imagen global de cada una de ella')
    print(f'De las variables numericas recibimos información de su media, mediana, entre otros datos importantes.')
    print(df.describe())
    print(f'De las variables cartegoricas recibimos información de lso diferentes valores, el más repetido, entre otros datos importantes.')
    print(df.describe(include=object))
    print(f'Por ultimo, se muestran 5 instancias aleatorias del dataframe')
    return df.sample(5)

#pasar a datetime
def convertir_en_fecha(variable:str, df ):
    """Convertir una variable con formato "%Y-%m-%dT%H:%M:%SZ" a datetime

    Args:
        variable (_type_): Nombre de la variable
        df (_type_, optional): DataFrame dde donde es la variable. Defaults to df.

    Returns:
        _type_: COlumna transformada
    """
    import pandas as pd
    transformado = pd.to_datetime(df[variable])
    return transformado
#eliminar naS
def quita_na(variable:str, df, poner):
    """Eliminar los missings de una variable

    Args:
        variable (_type_): Nombre de la variable
        df (_type_, optional): DataFrame de donde es la variable. Defaults to df.
        poner (str): Con que texto se quiere imputar

    Returns:
        _type_: Columna sin missings
    """
    transformado = df[variable].fillna(poner)
    return transformado