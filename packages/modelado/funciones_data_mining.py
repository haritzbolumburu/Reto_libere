
# librerias
import pandas as pd
import datetime as dt
from sklearn.model_selection import GridSearchCV
from time import time
from sklearn.metrics import classification_report, confusion_matrix, plot_confusion_matrix, roc_auc_score


def ciudades(df:pd.DataFrame, variable:str)->pd.DataFrame:
    ciudad=[]
    vitoria=["Líbere Vitoria"]
    bilbao=["Líbere Bilbao Museo","Líbere Bilbao La Vieja"]
    madrid=["Líbere Madrid Palacio Real"]
    malaga=["Naitly Málaga Teatro Romano"]
    valencia=["Líbere Valencia Abastos","Líbere Valencia Jardín Botánico"]

    for i in range(0,len(df)):
        if df[variable][i] in vitoria:
           ciudad.append("vitoria-gasteiz")
           i+=1
        elif df[variable][i] in bilbao:
           ciudad.append("bilbao")
           i+=1
        elif df[variable][i] in madrid:
           ciudad.append("madrid")
           i+=1
        elif df[variable][i] in malaga:
           ciudad.append("malaga")
           i+=1
        elif df[variable][i] in valencia:
           ciudad.append("valencia")
           i+=1
        else:
            ciudad.append("otro")
    
    df['ciudad']=ciudad
    return df



def estado_clima(df:pd.DataFrame, variable:str) -> pd.DataFrame:

    lluvia=['Aguanieve fuerte o moderada', 'Ligeras lluvias', 'Ligeras precipitaciones', 'Ligeras precipitaciones de aguanieve', 'Llovizna', 'Llovizna a intervalos','Lluvia moderada','Lluvia moderada a intervalos','Lluvias ligeras a intervalos']
    nieve=['Chubascos de nieve fuertes o moderados', 'Fuertes nevadas']
    soleado=['Soleado']
    lluvias_fuertes=['Fuertes lluvias','Lluvias fuertes o moderadas','Periodos de fuertes lluvias' ]
    tormenta=['Cielos tormentosos en las aproximaciones ', 'Intervalos de lluvias ligeras con tomenta en la región', 'Lluvias con tormenta fuertes o moderadas en la región']
    niebla=['Neblina','Niebla moderada']
    nublado=['Cielo cubierto','Nublado','Parcialmente nublado']

    estado=[]
    i=0
    for i in range(0,len(df)):

       if df[variable][i] in lluvia:
           estado.append('lluvia')
           i+=1

       elif df[variable][i] in nieve:
           estado.append('nieve')
           i+=1

       elif df[variable][i] in soleado:
           estado.append('soleado')
           i+=1

       elif df[variable][i] in lluvias_fuertes:
           estado.append('lluvias_fuertes')
           i+=1

       elif df[variable][i] in tormenta:
           estado.append('tormenta')
           i+=1

       elif df[variable][i] in niebla:
           estado.append('niebla')
           i+=1

       elif df[variable][i] in nublado:
           estado.append('nublado')
           i+=1

       else:
            estado.append('otro') 
            i+=1

    df['estado']=estado
    
    return df


def dummys(df:pd.DataFrame,variable:str):
    dfin=df
    dummy=pd.get_dummies(dfin[variable])
    df_out=dfin.join(dummy, how='outer')
    return df_out



def modelo_sin_balanceo(xtr:pd.DataFrame, ytr:pd.DataFrame, models_list:list, model_hyperparameters:dict)-> pd.DataFrame:
    start_time = time()
    model_keys=list(model_hyperparameters.keys())
  
    print('DATOS DESBALANCEADOS')
    print(ytr.value_counts())


    result = []
    i=0

    for model in models_list:
       key=model_keys[i]
       i+=1
       params = model_hyperparameters[key]

       classifier=GridSearchCV(model,params,cv=5,scoring='accuracy',refit=False)

       classifier.fit(xtr,ytr)
       elapsed_time = time() - start_time
       result.append({
        'model_used':model,
        'highest_score':classifier.best_score_,
        'best hyperparameters':classifier.best_params_,
        'balanceo':"sin_balanceo",
        'segundos': elapsed_time,
        'hora_subida':dt.datetime.now()

       })
       print(result[i-1])

    

    return pd.DataFrame(result)


def modelo_balanceado(balanceo, xtr:pd.DataFrame, ytr:pd.DataFrame, models_list:list, model_hyperparameters:dict)->pd.DataFrame:
    start_time = time()
    model_keys=list(model_hyperparameters.keys())
  
    print('DATOS DESBALANCEADOS')
    print(ytr.value_counts())

    xbal, ybal = balanceo.fit_resample(xtr, ytr)

    print('DATOS BALANCEADOS')
    print(ybal.value_counts())


    result = []
    i=0

    for model in models_list:
       key=model_keys[i]
       i+=1
       params = model_hyperparameters[key]

       classifier=GridSearchCV(model,params,cv=5,scoring='accuracy',refit=False)

       classifier.fit(xbal,ybal)
       elapsed_time = time() - start_time
       result.append({
        'model_used':model,
        'highest_score':classifier.best_score_,
        'best hyperparameters':classifier.best_params_,
        'segundos':elapsed_time,
        'balanceo':balanceo,
        'hora_subida':dt.datetime.now()
       })
       print(result[i-1])

    return pd.DataFrame(result)



def modelo_final(modelo, balanceo, xtr:pd.DataFrame, ytr:pd.DataFrame, xte:pd.DataFrame, yte:pd.DataFrame):

  
    print('DATOS DESBALANCEADOS')
    print(ytr.value_counts())

    xbal, ybal = balanceo.fit_resample(xtr, ytr)

    print('DATOS BALANCEADOS')
    print(ybal.value_counts())
    

     #creacion de modelo
    model=modelo
    model.fit(xbal,ybal)
    prediction=model.predict(xte)

    # scoring modelo
    mean_accuracy = modelo.score(xte, yte)
    auc = roc_auc_score(yte,prediction)
    print('La precision media es de : ' + str(mean_accuracy))
    print('EL area bajo la curva de ROC es de : ' + str(auc))

    # validation
    expected = yte
    predicted = prediction
    print("Classification report for classifier %s:\n%s\n"
      % (modelo, classification_report(expected, predicted, digits=4)))
    print("Confusion matrix:\n%s" % confusion_matrix(expected, predicted))
    plot_confusion_matrix(modelo, xte, yte)


def modelo_final_sin_balanceo(modelo, xtr:pd.DataFrame, ytr:pd.DataFrame, xte:pd.DataFrame, yte:pd.DataFrame):
    

     #creacion de modelo
    model=modelo
    model.fit(xtr,ytr)
    prediction=model.predict(xte)

    # scoring modelo
    mean_accuracy = modelo.score(xte, yte)
    auc = roc_auc_score(yte,prediction)
    print('La precision media es de : ' + str(mean_accuracy))
    print('EL area bajo la curva de ROC es de : ' + str(auc))

    # validation
    expected = yte
    predicted = prediction
    print("Classification report for classifier %s:\n%s\n"
      % (modelo, classification_report(expected, predicted, digits=4)))
    print("Confusion matrix:\n%s" % confusion_matrix(expected, predicted))
    plot_confusion_matrix(modelo, xte, yte)

def coeficientes_logis(modelo, balanceo, xtr:pd.DataFrame, ytr:pd.DataFrame)->pd.DataFrame:

    xbal, ybal = balanceo.fit_resample(xtr, ytr)

    model=modelo
    model.fit(xbal,ybal)

    importance = model.coef_

    columnas=list(xtr.columns)
    valores=importance.flatten().tolist()

    coeficientes={}
    for i in range(0,len(valores)):
        coeficientes[columnas[i]]=valores[i]

    df_coef1=pd.DataFrame()
    df_coef1['columna']=coeficientes.keys()
    df_coef1['coeficiente']=coeficientes.values()

    return df_coef1.sort_values("coeficiente", ascending=True)


def resultados_csv(lista_modelos):

    resultados=pd.DataFrame()
    for df in lista_modelos:
        resultados=resultados.append(df, ignore_index=True)

    resultados.to_csv('./Datos/Transformados/resultados.csv', index=False)