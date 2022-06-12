from multiprocessing.sharedctypes import Value
import pandas as pd
from datetime import datetime
from flask import Flask, request, jsonify
import json

app = Flask(__name__)
df = pd.read_csv("data/csvdata.csv", sep = ",")

# Constantes obtenidas del entrenamiento
mean = 72.00158769425943
std = 61.382440401330285

def get_input(fechas):
    resp = []
    for row in fechas.index:
        aux = []
        mini_resp = []
        mini_resp.append(df.loc[row, "price"])
        mini_resp.append(df.loc[row, "day_sin"])
        mini_resp.append(df.loc[row, "day_cos"])
        mini_resp.append(df.loc[row, "year_sin"])
        mini_resp.append(df.loc[row, "year_cos"])
        mini_resp.append(df.loc[row, "week_sin"])
        mini_resp.append(df.loc[row, "week_cos"])
        aux.append(mini_resp)
        resp.append(aux)
    
    data = {}
    data['instances'] = resp
    str_data = json.dumps(data)
    json_data = json.loads(str_data)
    return json_data 

#Metodo al que le pasamos una fecha, y nos devuelve un timestamp
def fecha_parse(fecha):
    fecha_str = fecha + " 00:00:00"
    fecha = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M:%S")
    res = fecha.timestamp()
    return res

def normalize(val):
    norm_val = (val * std) + mean
    return norm_val

def get_real_value_hour(fecha):
    fecha_timestamp = fecha_parse(fecha)
    row_value = df.loc[df['date'] == fecha_timestamp]
    row_value_index = row_value.index[0]
    value = df.loc[row_value_index, "price"]
    value = normalize(value)
    return value

def get_real_values_day(fecha):
    fecha_timestamp = fecha_parse(fecha)
    row_value = df.loc[df['date'] == fecha_timestamp]
    row_value_index = row_value.index[0]
    fechas = df.iloc[row_value_index - 24:row_value_index]
    res = []

    for row in fechas.index:
        value = df.loc[row, "price"]
        res.append(normalize(value))

    return res

def get_hour_data(fecha):
    fecha_timestamp = fecha_parse(fecha)
    fecha_find = df.loc[df['date'] == fecha_timestamp]
    fecha_find_index = fecha_find.index[0]
    print(fecha_find_index)
    fechas_input = df.iloc[fecha_find_index - 3:fecha_find_index]
    #Montamos la entrada
    response = get_input(fechas_input) 
    # Tengo que obtener la predicción 
    return response

def get_day_data(fecha):
    fecha_timestamp = fecha_parse(fecha)
    fecha_find = df.loc[df['date'] == fecha_timestamp]
    fecha_find_index = fecha_find.index[0]
    fechas_input = df.iloc[(fecha_find_index - 24 * 7):fecha_find_index]
    
    #Montamos la entrada
    response = get_input(fechas_input) 
    # Tengo que obtener la predicción 
    return response

def get_week_day():
    fecha = request.json['fecha']
    fecha_timestamp = fecha_parse(fecha)
    fecha_find = df.loc[df['date'] == fecha_timestamp]
    fecha_find_index = fecha_find.index[0]
    fechas_input = df.iloc[(fecha_find_index - 24 * 7 * 3):fecha_find_index]
    
    #Montamos la entrada
    response = get_input(fechas_input) 
    # Tengo que obtener la predicción 
    return response

if __name__ == "__main__":
    app.run(port=5000)