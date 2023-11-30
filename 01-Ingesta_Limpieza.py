# INGESTA
# In: Datos originales
# Out: Datos limpios y transfromados

import packages.Preprocesamiento as PPS #desde donde vamos a llamar las funciones






#INTRODUCCION
PPS.bienvenida()
from time import sleep
delay=PPS.retraso()



#INDICE
print('A continuación tendras la opcion de analizar el proceso general que se ha llevado a cabo en este preprocesamiento. \n ')
PPS.resumen_preprocesamiento(delay)




#Carga de datos
CARPETA=('./Datos/Originales')
FICHERO='booking_data_for_cancellation_proyecto.csv'
datos = PPS.read_data(CARPETA,FICHERO)
datos.head()
#primer acercamiento a los datos


#1-DATA DISCOVERING
PPS.data_discovering(datos,delay)

#2. FORMATEO DE LOS DATOS
print('2. FORMATEO DE LOS DATOS')
sleep(delay)
print(f'Una vez habiendo hecho un analis exploratorio del dataset inicial el siguiente paso es hacer un formateo de las variables')
datos=PPS.formateo(datos,delay)
sleep(delay)

#2.2-ANALISIS DESCRIPTIVO
PPS.analisis_descriptivo(datos,delay)


#3- DUPLICADOS
print('3- Duplicados')
print('En este tercer paso se pasar a analizar si hay duplicados en el dataset proporcionado')
PPS.data_duplicados(datos)
sleep(delay)

#4-VALORES AUSENTE
print('4- Missings')
print('Antes de quitar os valores ausentes creamos una nueva variable de las instancias que tienen NA en la columa "age"')
sleep(delay)
datos=PPS.age_nan(datos, 'age')
PPS.missing_exploratorio(datos,delay)
sleep(delay)



print('Trartamiento de valores ausentes')
datos['cancelled_at'] = PPS.quita_na('cancelled_at', datos, 'No cancelado')
sleep(delay)
datos['travel_agency_name'] = PPS.quita_na('travel_agency_name', datos, 'No determinado')
sleep(delay)
datos['nationality'] = PPS.quita_na('nationality', datos, 'No determinado')
sleep(delay)
PPS.quita_na_2('age',datos)
sleep(delay)
PPS.missing_exploratorio(datos,delay)
sleep(delay)


#5-OUTLIERS
print('5-OUTLIERS')
datos=PPS.errores_informaticos(datos,'age')



#6-CONSTRUCCION DE VARIABLES
#Construccion variables categoricas
sleep(delay)
datos['extras']=PPS.extras(datos)
datos['rangos_edad']=PPS.rangos_edad(datos)
datos['total_personas']=PPS.total_personas(datos)
datos['rango_de_numero_adutlos']=PPS.rango_de_numero_adutlos(datos)
datos['rango_de_numero_niños']=PPS.rango_de_numero_niños(datos)


#Construccion de variables de fecha
datos['dif_checkin_cancelacion']=PPS.dif_checkin_canc(datos)
datos['dif_fecha_cancelacion_booking']=PPS.dif_fecha_cancelacion_booking(datos)
datos['dif_reserva_entrada']=PPS.dif_reserva_entrada(datos)
datos['duracion_reserva']=PPS.duracion_reserva(datos)
#diferencia fecha reserva y entrada

##Data discovering del nuevo dataset
#7-DATA DISCOVERING DEL DATAFRAME TRANSFORMADO
print('7-DATA DISCOVERING DEL DATAFRAME TRANSFORMADO')
sleep(delay)
PPS.data_discovering(datos,delay)



#Crear carpeta de transformados en datos y creamos tambien la de graficos
PPS.crear_carpeta('Graficos')

#Pasar a csv
PPS.write_csv(datos,'./Datos/Transformados/','df_transformado')

#Final
PPS.despedida()