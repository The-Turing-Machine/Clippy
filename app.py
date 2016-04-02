from flask import Flask, request, session, g, redirect, url_for, render_template, jsonify
from flask.ext.login import LoginManager, UserMixin, login_required
import requests
import json
import os
json_data = {}


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    # user_database = json_data
    user_database = {"admin": ("admin", "1234"),"user1": ("user1", "abcd")}
    def __init__(self, username, password):
        self.id = username
        self.password = password
    @classmethod
    def get(cls,id):
        return cls.user_database.get(id)


@login_manager.request_loader
def load_user(request):
    token = request.headers.get('Authorization')
    if token is None:
        token = request.args.get('token')

    if token is not None:
        print token
        username,password = token.split(":") #edit this
        user_entry = User.get(username)
        if (user_entry is not None):
            user = User(user_entry[0],user_entry[1])
            if (user.password == password):
                return user
    return None



@app.route("/")
def hello():
    return jsonify({'status':'ok'})

@app.route("/api/")
@login_required
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
    app.config["SECRET_KEY"] = "SuperDuperSecretKey!"
    with open("data/database.json") as json_file:
        json_data = json.load(json_file)

    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True,host='0.0.0.0',port=port)
