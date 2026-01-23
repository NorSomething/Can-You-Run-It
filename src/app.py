from flask import Flask, render_template, request
import requests
import json 

import data_parsing

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def index():
    
    if request.method == 'GET':
        return render_template('index.html')

    elif request.method == 'POST':

        game = request.form["game_name"]
        cpu = request.form["cpu"]
        ram = int(request.form["ram"])
        gpu = request.form["gpu"]

        if ram > 20:
            return "nirmal kumar"
        else:
            return ""
    return None

@app.route('/check', methods = ['POST'])
def check():

    game = request.form["game_name"]




if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)