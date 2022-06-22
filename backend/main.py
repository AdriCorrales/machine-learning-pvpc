import pandas as pd
from datetime import datetime
from flask import Flask, redirect, render_template, request
import server
import requests

app = Flask(__name__)

df = pd.read_csv("data/csvdata.csv", sep = ",")

@app.route('/')
def init():
    return render_template("inicio.html")

@app.route('/hour', methods=['GET','POST'])
def get_hour():
    fecha = request.form.get("fecha")
    hora = request.form.get("hora")
    resp = server.get_hour_data(fecha, hora)
    realvalue = server.get_real_value_hour(fecha, hora)
    pred = requests.post('http://pvpc-serving:8501/v1/models/modelhour/versions/1:predict', json=resp)
    pred_json = pred.json().get("predictions")
    predvalue =server.normalize(pred_json[0][0])
    fechashow = fecha + " " + hora
    return render_template("hora.html", realvalue = realvalue, predvalue = predvalue, fechashow = fechashow, error = "Fecha incorrecta")

@app.route('/day', methods=['GET','POST'])
def get_day():
    fecha = request.form.get("fecha")
    hora = request.form.get("hora")
    resp = server.get_day_data(fecha, hora)
    realvalues = server.get_real_values_day(fecha, hora)
    pred = requests.post('http://pvpc-serving:8501/v1/models/modelday/versions/1:predict', json=resp)
    pred_json = pred.json().get("predictions")
    
    predvalues = []
    for i in range(0, len(pred_json[0])):
        predvalue = server.normalize(pred_json[0][i])
        predvalues.append(predvalue)
    
    fechashow = fecha + " " + hora
    return render_template("dia.html", realvalues = list(realvalues), predvalues = list(predvalues), fechashow = fechashow, error = "Fecha incorrecta", len = len(list(realvalues)))

@app.route('/week', methods=['GET','POST'])
def get_week():
    fecha = request.form.get("fecha")
    hora = request.form.get("hora")
    resp = server.get_week_data(fecha, hora)
    realvalues = server.get_real_values_week(fecha, hora)
    pred = requests.post('http://pvpc-serving:8501/v1/models/modelweek/versions/1:predict', json=resp)
    pred_json = pred.json().get("predictions")
    
    predvalues = []
    for i in range(0, len(pred_json[0])):
        predvalue = server.normalize(pred_json[0][i])
        predvalues.append(predvalue)
    
    fechashow = fecha + " " + hora
    return render_template("semana.html", realvalues = list(realvalues), predvalues = list(predvalues), fechashow = fechashow, error = "Fecha incorrecta", len = len(list(realvalues)))

@app.errorhandler(500)
def internal_server_error(e):
    # note that we set the 500 status explicitly
    return render_template('inicio.html', error = "Fecha invalida")

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5001)