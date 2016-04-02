from flask import Flask, request, session, g, redirect, url_for, render_template, jsonify

import requests
import json
import os
json_data = {}


app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/api/<user>/get_data")
def store(user):
    try:
        return jsonify(json_data[user])
    except Exception as e:
        return jsonify({'status':'Error','msg':'user not present in database'})


if __name__ == "__main__":
    global json_data

    # json_data=open('data/database.json').read()
    with open("data/database.json") as json_file:
        json_data = json.load(json_file)
        print type(json_data)
        print '-------------'
        print json_data['user1']['post1']

    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True,host='0.0.0.0',port=port)
