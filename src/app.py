from flask import Flask, render_template, request
import requests
import json 

from data_parsing import final_checker

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def index():
    
    if request.method == 'GET':
        return render_template('index.html')

    elif request.method == 'POST':

        steam_appid = request.form['steam_id']
        result = final_checker(steam_appid)

        can_run = result["can run"]

        if can_run:
            result_text = "You can run this game!"
            result_class = "success"
        else:
            result_text = "You cannot run this game."
            result_class = "fail"

        return render_template(
            "index.html",
            user_specs=result["user_specs"],
            game_specs=result["game_specs"],
            can_run=can_run,
            bottlenecks=result["bottlenecks"],
            result_text=result_text,
            result_class=result_class
        )

    return None





if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)