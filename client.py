import pandas as pd
from datetime import datetime
from flask import Flask, redirect, render_template, request
import server
import requests

app = Flask(__name__)

df = pd.read_csv("data/csvdata.csv", sep = ",")

# Constantes obtenidas del entrenamiento
mean = 72.00158769425943
std = 61.382440401330285

@app.route('/')
def init():
    return render_template("inicio.html")

@app.route('/hour', methods=['GET','POST'])
def get_hour():
    fecha = request.form.get("fecha")
    resp = server.get_hour_data(fecha)
    realvalue = server.get_real_value_hour(fecha)
    pred = requests.post('http://localhost:8601/v1/models/prueba_model/versions/1:predict', json=resp)
    pred_json = pred.json().get("predictions")
    predvalue =server.normalize(pred_json[0][0])
    return render_template("hora.html", realvalue = realvalue, predvalue = predvalue, error = "Fecha incorrecta")

@app.route('/day', methods=['GET','POST'])
def get_day():
    fecha = request.form.get("fecha")
    resp = server.get_day_data(fecha)
    realvalues = server.get_real_values_day(fecha)
    pred = requests.post('http://localhost:8601/v1/models/prueba_model/versions/2:predict', json=resp)
    pred_json = pred.json().get("predictions")
    
    predvalues = []
    for i in range(0, len(pred_json[0])):
        predvalue = server.normalize(pred_json[0][i])
        predvalues.append(predvalue)
    
    return render_template("dia.html", realvalues = list(realvalues), predvalues = list(predvalues), error = "Fecha incorrecta", len = len(list(realvalues)))

@app.route('/week', methods=['GET','POST'])
def get_week():
    return render_template("inicio.html")

@app.errorhandler(500)
def internal_server_error(e):
    # note that we set the 500 status explicitly
    return render_template('inicio.html', error = "Fecha invalida")

if __name__ == "__main__":
    app.run(port=5001)