from flask import Flask, request, session, g, redirect, url_for, render_template, jsonify
# from flask_mongoengine import MongoEngine
from pymongo import MongoClient

import requests
import json
import os


def connect():
    # Temporary !!
    connection = MongoClient("ds023118.mlab.com",23118)
    handle = connection["users"]
    handle.authenticate("admin","1234")
    return handle


app = Flask(__name__)
handle = connect()


@app.route("/")
def hello():
    return "Hello World!"

@app.route("/data",methods=['GET'])
def data():
    userinputs = [x for x in handle.mycollection.find()]
    for item in userinputs:
        print item
        # print item.message + ' has database id ' + item._id
    return str(userinputs)

@app.route("/add/<text>", methods=['GET','POST'])
def write(text):
    userinput = text
    oid = handle.mycollection.insert({"message":userinput})
    return redirect ("/data")


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True,host='0.0.0.0',port=port)
