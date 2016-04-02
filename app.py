from flask import Flask, request, session, g, redirect, url_for, render_template, jsonify

import requests
import json
import os
json_data = {}


app = Flask(__name__)

@app.route("/")
def hello():
    return jsonify({'status':'ok'})

@app.route("/api/")
def status():
    return jsonify({'status':'ok'})

@app.route("/api/get/<user>" , methods=['GET'])
def recieve(user):
    global json_data

    try:
        return jsonify(json_data[user])
    except KeyError:
        return jsonify({'status':'Error','msg':'That username does not exist !!'})
    except Exception as e:
        return jsonify({'status':'Error','msg':'An exception has occured !!'})

@app.route('/api/post/<user>', methods=['GET','POST'])
def send(user):
    global json_data

    if request.method == 'POST':
        pass
    else:
        pass

if __name__ == "__main__":
    global json_data

    with open("data/database.json") as json_file:
        json_data = json.load(json_file)

    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True,host='0.0.0.0',port=port)
