from flask import Flask, request, session, g, redirect, url_for, render_template, jsonify

import requests
import json
import os
json_data = {}


app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/api/")
def status():
    pass

@app.route("/api/<user>/get_data" , methods=['GET'])
def store(user):
    try:
        return jsonify(json_data[user])
    except KeyError:
        return jsonify({'status':'Error','msg':'That username does not exist !!'})
    except Exception as e:
        return jsonify({'status':'Error','msg':'An exception has occured !!'})



if __name__ == "__main__":
    global json_data

    with open("data/database.json") as json_file:
        json_data = json.load(json_file)

    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True,host='0.0.0.0',port=port)
