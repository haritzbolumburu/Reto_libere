def bienvenida():
    """Dar la bienvenida al usuario
    """
    import emoji
    name = input('Hola,¿Cual es tu nombre?')
    print(f'Bienvenido {name.capitalize()}'+ emoji.emojize(':grinning_face:')+'  !! ' + f'\n En este apartado se procedera a hacer un preprocesamiento del dataset proporcionado.')


def retraso()->int:
    """pide al usuario el numero de segundos que quiere que pase entre comando y comando

    Returns:
        int: EL numero de segundos que pasaran entre comando y comando
    """
    retraso=float(input('Especifica el retraso entre codigos.(En segundos):'))
    print(f'El retraso seleccionado han sido {retraso} segundos.')
    return retraso


def read_data(CARPETA:str,FICHERO:str):
    """leer fihcero csv

    Args:
        CARPETA (dir): Directorio donde se almacena el csv con los datos originales
        FICHERO (dir): CSV que contiene  la informacion proporcionada por el cliente

    Returns:
        Dataframe: CSV en dataset
    """
    import pandas as pd
    import os
    return pd.read_csv(os.path.join(CARPETA,FICHERO),sep=',')





def resumen_preprocesamiento(delay:int)->str:
    """ Da la oportunidad de ver los pasos que se van a llevar en el preprocesamiento de los datos

    Args:
        delay (int): retraso seleccionado

    Returns:
        str:Los puntos llevados a cabo en la parte de preprocesamiento
    """
    from time import sleep
    resumen=input('¿Quieres ver un resumen de los puntos que se van a realizar? (Si/No)')
    if resumen.lower() == 'si':
     print(
         'Preprocesamiento \n ')
     sleep(delay)
     print(
     '1- Data Discovering \n ' )
     sleep(delay)
     print(
     '2- Formateo de datos \n')
     sleep(delay)
     print(
     '3- Duplicados \n')
     sleep(delay)
     print(
     '4- Missings \n')
     sleep(delay)
     print('5- Tratamiento de missings \n' )
     sleep(delay)
     print('6- Outliers \n')
     sleep(delay)
     print('7- Creación de nuevas variables \n')
    elif resumen.lower() == 'no':
     print('Perfecto se pasara a la parte de preprocesamiento')
    else:
     print('No te he podido entender teclea si o no')
     print('Por defecto pasare  a la parte de preprocesamiento')



def data_discovering(datos,delay):
    """Esta funcion nos proporciona un resumen del dataset para tener un primer vistazo,numero de observaciones y variables,el tipo de esas variables etc..

     Args:
        datos (dataframe): Datos proporcionados por el cliente
        delay (int): Retraso seleccionado

        Returns:
        str:Breve resumen del dataset
    """
    from time import sleep
    print('En este apartado el primer paso es hacer un apropiado data discoverase recibido, con el objetivo de familiarizarse con la información de este  fichero y entender la información que contiene.')
    sleep(delay)
    print(f'EL  dataset  inicial tiene una forma de {datos.shape[0]} observaciones y {datos.shape[1]} variables')
    sleep(delay)
    print('-------------------------------------------------------------------------------------------')
    print(f'Con el objetivo de conocer el nombre  y el tipo de las columnas ademas  del numero de observaciones en cada columnas se muestra la siguiente tabla')
    print({datos.info()})
    sleep(delay)
    print('Una vez conociendo las dimensiones y las columnas del dataaset proporcionado se pasara a mostrar diversas filas para conocer de que valores tratan')
    sleep(delay)
    print(f'Primeras cinco instancias del dataset {datos.head(5)}')
    sleep(delay)
    print(f'Ultimas cinco instancias del dataset {datos.tail(5)}')
    sleep(delay)
    print(f'5 filas aleatorias de todo el dataset {datos.sample(5)}')
    sleep(delay)
    print('Para finalizar con este paso de  haremos un analisis brevee estadistico para conocer')
    sleep(delay)
    print(datos.describe(include=float))
    sleep(delay)
    print(datos.describe(include=object))


def formateo(dataset,delay):
    import pandas as pd
    from time import sleep
    """Adecuar  el formato de las variables para posteriormente poder trabajar  posterioemtente sin porblemas sin problemas

    Args:
        dataset (dataframe): Dataset inicial  proporcionado por el cliente  Libere
    
    Returns:
        dataset:Dataframe con las columnas formateadas
    """
    print('Se realizara una copia del dataset  por si posteriormente se quiere recuperar los datos originales')
    from time import sleep
    print('Por una parte se propone pasar la variable cancllation a booleana (0-1)')
    dataset=dataset.astype({'cancellation':'bool'})
    dataset['checkin_time']= pd.to_datetime(dataset['checkin_time'] )
    print(f'Fecha aleatoria de cheking  time '+ str(dataset['checkin_time'].sample()))
    sleep(delay)
    dataset['booking_time']= pd.to_datetime(dataset['booking_time'] )
    print(f'Fecha aleatoria de booking  time '+ str(dataset['booking_time'].sample()))
    sleep(delay)
    dataset['checkout_time']= pd.to_datetime(dataset['checkout_time'] )
    print(f'Fecha aleatoria de checkout time '+ str(dataset['checkout_time'].sample()))
    sleep(delay)
    print(f'Se pasan las variables checkin, booking y chekout time a datetime formato %Y-%m-%d y la variable cancellation a booleana')
    return(dataset)


def analisis_descriptivo(df,delay):
    import pandas as pd
    import numpy as np
    from scipy import stats
    from time import sleep
    """Analisis descriptivo de los datos proporcionados por el cliente.Creamos una
    tabla por variable numerica.
    """
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    for column in numeric_columns:
        print(f'Análisis estadístico para la columna {column}:')
        print(f'Media: {df[column].mean()}')
        print(f'Mediana: {df[column].median()}')
        print(f'Moda: {stats.mode(df[column])[0][0]}')
        print(f'Desviación estándar: {df[column].std()}')
        print(f'Varianza: {df[column].var()}')
        print(f'Mínimo: {df[column].min()}')
        print(f'Máximo: {df[column].max()}')
        print(f'Rango: {df[column].max() - df[column].min()}')
        print(f'Curtosis: {stats.kurtosis(df[column])}')
        print('\n')
        sleep(delay)


def data_duplicados(dataset):
    import pandas as pd
    """Analizar los datos duplicados y borrarlos en caso necesario

    Args:
        dataset (dataframe): Dataset formateado en la funcion 'formateo'
    """
    df_duplicados= dataset.copy()
    dataset=dataset[dataset.duplicated()]
    print(dataset)
    if len(dataset)==0:
        print('No hay duplicados y por lo tanto se pasara a analizar los missing values.')
    else:
        dataset.drop_duplicates()
        print('Hay duplicados y se  deciden eliminar ya que se supone que hay un error y hay una reserva duplicadada en el dataset ')
    return(dataset)


def missing_exploratorio(datos,delay):
    """Analizar los datos ausentes del dataser

    Args:
        datos (dataframe): datos proporcionados por el cliente
        delay (int): retraso seleccionado
    """
    from time import sleep
    print('Una vez  habiendo formateado y habiendo quitado los duplicados en caso necesario se pasara a analizar los datos ausentes')
    sleep(delay)
    print(f' En este dataser nos encontramos con un total de {sum(datos.isna().sum())} observaciones ausentes')
    sleep(delay)
    print(f' Este total de valores ausentes se reparte de la siguiente manera:')
    print(datos.isna().sum())
    sleep(delay)


#Outliers errores 
def errores_informaticos(df,variable):
    """Borramos las instancias fuera de comun

    Args:
        df (dataframe): Datos proporcionados por el cliente
        variable (age): edad de los usuarios que han hecho la reserva
    """
    df = df[df[variable]<90]
    df = df[df[variable]>=16]
    print('Se  eliminan todas las reservas hechas por personas menores de 16 y mayores de 90')
    return(df)

def age_nan(df,variable): 
    age_na=[]
    """Variable que nos indica si el usuario ha rellenado la edad o no

    Returns:
        age: edad de los usuarios que han hecho la reserva
    """
    for i in df[variable].isnull():
        if i == True:
            age_na.append(1)
        else:
            age_na.append(0)
    df['age_nan']=age_na
    return df

def quita_na_1(variable:str, df, poner):
    """Sustuir los missings de una variable

    Args:
        variable (_type_): Nombre de la variable que se va a esciger
        df (_type_, optional): DataFrame de donde es la variable. Defaults to df.
        poner (str): Con que texto se quiere imputar los valores ausentes de la columna

    Returns:
        _type_: Columna sin missings
    """
    transformado = df[variable].fillna(poner)
    return transformado


def quita_na_2(variable,df):
    """Sustuir los missings de una variable

    Args:
        variable (age): Edad del usuario que ha reservado
        df (dataframe): Datos proporcionados por el cliente

    Returns:
        age: nos devuelve la edad media de los usuarios que han hecho la reserva para el mismo numero de niños y adultos
    """
    df[variable]= df.groupby([df['child_count'],df['adult_count']])['age'].transform(lambda x: x.fillna(x.mean()).round())
    print(f' Se han cambiado los missing values de la variable {variable} dependiendo de la nacionalidad y la cantidad de hijos con los que habia reservado')
    return df





#Construccion variables
#1 variables ccategoricas y numericas


def extras(df):
    """NOs devuelve cuanto dinero extra se ha dejado el usuario en la reserva

    Args:
        df (dataframe): datos proporcionados por el cliente

    Returns:
        int: Diferencia entre las variables reservation net value y nights net value
    """
    import datetime
    import pandas
    df['extras_net_value'] = df['reservation_net_value'] - df['reservation_nights_net_value']
    return df['extras_net_value']

def rangos_edad(df):
    """_summary_

    Args:
        df (dataframe): datos proporcionados por el cliente

    Returns:
        categorical: El rango de edad que es el usuario
    """
    import pandas as pd
    bins = [16, 18, 25, 35, 50, 65, 80, 90]
    names = ["16-18", "18-24", "25-35", "35-50", "50-65", "65-80", "+80"]
    df['rangos_age'] = pd.cut(df['age'], bins, labels = names)
    return df['rangos_age']



def total_personas(df):
    """Calcula  de personas total 

    Args:
        df (dataframe): Datos proporcionado por el cliente

    Returns:
        _type_: Suma de las variables adult county child count
    """
    import pandas as pd
    df['total_personas'] = df['adult_count'] + df['child_count']
    return df['total_personas']

def rango_de_numero_adutlos(df):
    """Cantidad de adultos en cada reserva dividida en tres rangos.

    Args:
        df (dataframe): Datos proporcionados por el cliente

    Returns:
        _type_: _persona sola, pareja y grupo de adultos_
    """
    import pandas as pd
    bins = [0, 1, 2, 8]
    names = ["persona sola", "pareja", "grupo de adultos"]
    df['rangos_adultos'] = pd.cut(df['adult_count'], bins, labels = names)
    return df['rangos_adultos']


def rango_de_numero_niños(df):
    """Cantidad de niños en cada reserva dividida en cuatro rangos.
    Args:
        df (dataframe): Datos proporcionados por el cliente

    Returns:
        _type_: [sin niños, niño único, dos niños y familia numerosa]
    """
    import pandas as pd
    bins = [-1,0, 1, 2, 5]
    names = ["sin niños", "niño unico", "dos niños", "familia numerosa"]
    df['rangos_niños'] = pd.cut(df['child_count'], bins, labels = names)
    return df['rangos_niños']

#Variables de fecha


def fecha_sol(x):
    from datetime import datetime
    import pandas
    x = x.strftime("%Y-%m-%d %H:%M:%S")
    return x
def redondear_dias(x):
     x = x.ceil('1440 min').days
     return x


def dif_checkin_canc(df):
    """_summary_

    Args:
        df (_type_): _description_

    Returns:
        _type_: _description_
    """
    import pandas as pd
    df['cancelled_imp']=df['cancelled_at']
    df.loc[df['cancelled_at']=='No cancelado', 'cancelled_imp'] = '2000-01-01T00:00:00.000Z'
    df['cancelled_imp']=pd.to_datetime(df['cancelled_imp'])
    df['dif_can_in'] = df['checkin_time'] - df['cancelled_imp'] 
    df.loc[df['cancelled_at']=='No cancelado', 'dif_can_in'] = 0
    
    df.loc[df['cancelled_at']!='No cancelado', 'dif_can_in'] = df.loc[df['cancelled_at']!='No cancelado', 'dif_can_in'].apply(redondear_dias)
    return df['dif_can_in'] 



def dif_fecha_cancelacion_booking(df):
    """_summary_

    Args:
        df (_type_): _description_

    Returns:
        _type_: _description_
    """
    import pandas as pd 
    df['booking_time'] = df['booking_time']
    df['booking_time'] = pd.to_datetime(df['booking_time'])
    df['dif_can_res'] = df['cancelled_imp'] - df['booking_time']
    df.loc[df['cancelled_at']=='No cancelado', 'dif_can_res'] = 0
    df.loc[df['cancelled_at']!='No cancelado', 'dif_can_res']  = df.loc[df['cancelled_at']!='No cancelado', 'dif_can_res'].apply(redondear_dias)
    df.loc[df['cancelled_at']!='No cancelado', 'dif_can_res']
    return df['dif_can_res']


def dif_reserva_entrada(df):
    """_summary_

    Args:
        df (_type_): _description_

    Returns:
        _type_: _description_
    """
    df['dif_ent_res'] = df['checkin_time'] - df['booking_time']
    df['dif_ent_res'] = df['dif_ent_res'].apply(redondear_dias)
    return df['dif_ent_res']



def duracion_reserva(df):
    """_summary_

    Args:
        df (_type_): _description_

    Returns:
        _type_: _description_
    """
    import pandas as pd
    df['checkout_time'] = df['checkout_time']
    df['checkout_time'] = pd.to_datetime(df['checkout_time'])
    df['duracion_reserva'] = df['checkout_time'] - df['checkin_time']
    df['duracion_reserva'] = df['duracion_reserva'].apply(redondear_dias)
    return df['duracion_reserva']




#Crear carpeta
def crear_carpeta(carpeta):
    import os
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)
        print(f"La carpeta '{carpeta}' ha sido creada.")
    else:
        print(f"La carpeta '{carpeta}' ya existe.")



#Guardar dataframe en un csv 
def write_csv(dataframe,ruta,nombre):
    """gurada un dataframe en un csv

    Args:
        dataframe (df): dataframe que queremos exportar a csv
        ruta (dict): tura del direcotio
        nombre (string): nombre del documento

    Returns:
        _type_: _description_
    """
    X=(ruta+ nombre +'.csv')
    dataframe.to_csv(X,index=False)
    return X

#Despedida

def despedida():
    """Imprime un mensaje de despedida y notifica que el proceso ha finalizado.
    
    """
    print("¡El proceso  de Preprocesamiento ha finalizado con exito!")
    print('¡Espero haber sido de ayuda!')
    print('Tienes el csv limpio en la carpeta de datos transformados')


  