from flask import Flask, request, session, g, redirect, url_for, render_template, jsonify

import requests
import json
import os

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True,host='0.0.0.0',port=port)
