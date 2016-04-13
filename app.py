from flask import Flask, request, session, g, redirect, url_for, render_template, jsonify
from flask.ext.login import LoginManager, UserMixin, login_required, current_user
import requests
import json
import os
from flask.ext.cors import CORS
from pymongo import MongoClient
from OpenSSL import SSL
from flask.ext.bcrypt import Bcrypt


def connect():
    # Temporary !!
    connection = MongoClient("ds023118.mlab.com",23118)
    handle = connection["users"]
    handle.authenticate("admin","1234")# .......
    return handle

app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
db = connect()

app.config.update(
    DEBUG=True,
    SECRET_KEY='SuperDuperSecretKey!',
    BCRYPT_LOG_ROUNDS = 12
)

# user class
#----------------------------------------------------------------------------------------------------
class User(UserMixin):
    def __init__(self, username):
        data = db.collection.find({"user": username})[0]
        self.user = data['user']
        self.password_hash = data['password']
        self.data = data['data']

    def update(self,tempdata):
        #add each item in new list to orignal list, ignore duplicates
        db.collection.update(
            {"user": self.user},
            {
                "$addToSet":
                {
                    "data":
                    {
                        "$each": tempdata['data']
                    }
                }
            }
        )
        self.data = db.collection.find({"user": self.user})[0]['data']

    @classmethod
    def get(cls,uid):
        if db.collection.find({"user": uid}).limit(1).count() != 0:
            return db.collection.find({"user": uid})[0]
#----------------------------------------------------------------------------------------------------


# authenticates requests
#----------------------------------------------------------------------------------------------------
@login_manager.request_loader
def load_user(request):
    token = request.headers.get('Authorization')
    if token is None:
        token = request.args.get('token')

    if token is not None:
        username,password = token.split(":") #edit this
        user_entry = User.get(username)
        if (user_entry is not None):
            user = User(user_entry['user'])
            if bcrypt.check_password_hash(user.password_hash, password) == True:
                return user
    return None
#----------------------------------------------------------------------------------------------------

# basic endpoints
#----------------------------------------------------------------------------------------------------
@app.route("/")
def hello():
    #can be used to check connection status with api
    return jsonify({'status':'success'})

@app.route("/api/")
@login_required
def status():
    #can be used to check login status
    return jsonify({'status':'success','msg':'Currently logged in as '+ current_user.user})
#----------------------------------------------------------------------------------------------------



# endpoint for retriving user data from db
#----------------------------------------------------------------------------------------------------
@app.route("/api/get-user-data/" , methods=['GET','POST'])
@login_required
def recieve():
    #retrive specific user data from cloud db
    if current_user.is_anonymous == True:
        return jsonify({'status':'Error','msg':'Authentication failed !!'})
    try:
        if request.method == 'GET':
            return jsonify({
                'user' : current_user.user,
                'data' : current_user.data
            })
        else:
            return jsonify({'status':'Error','msg':'That method is not allowed !!'})
    except Exception as e:
        return jsonify({'status':'Error','msg':'An exception has occured !! - ' + e.message})

    @app.after_request
    def after_request(response):
      response.headers.add('Access-Control-Allow-Origin', '*')
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
      response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
      return response
#----------------------------------------------------------------------------------------------------



# endpoint for storing user data in db
#----------------------------------------------------------------------------------------------------
@app.route('/api/post-user-data/', methods=['GET','POST'])
@login_required
def send():
    #send data to cloud db for storage
    if current_user.is_anonymous == True:
        return jsonify({'status':'Error','msg':'Authentication failed !!'})
    try:
        if request.method == 'POST':
            tempdata = json.loads(request.data)
            current_user.update(tempdata)
            return jsonify({'status':'success','msg':'updated-user'})
        else:
            return jsonify({'status':'Error','msg':'That method is not allowed !!'})

    except Exception as e:
        return jsonify({'status':'Error','msg':'An exception has occured !! - ' + e.message})

    @app.after_request
    def after_request(response):
      response.headers.add('Access-Control-Allow-Origin', '*')
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
      response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
      return response
#----------------------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------------------
@app.route('/api/create-user/', methods=['GET','POST'])
def create():
    try:
        if request.method == 'POST':
            tempdata = json.loads(request.data)
            if db.collection.find({"user": tempdata['user']}).limit(1).count() != 0:
                #user already exists
                return jsonify({'status':'Error','msg':'That user already exists !!'})
            else:
                db.collection.insert(
                    {
                        'user':tempdata['user'],
                        'password': bcrypt.generate_password_hash(tempdata['password'],12),
                        'data':[]
                    }
                )
                return jsonify({'status':'success','msg':'created-user'})

        else:
            return jsonify({'status':'Error','msg':'That method is not allowed !!'})
    except Exception as e:
        return jsonify({'status':'Error','msg':'An exception has occured !! - ' + e.message})

    @app.after_request
    def after_request(response):
      response.headers.add('Access-Control-Allow-Origin', '*')
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
      response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
      return response
#----------------------------------------------------------------------------------------------------




#main function
#----------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    # app.config["SECRET_KEY"] = "SuperDuperSecretKey!"
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True,port=port,host='0.0.0.0',ssl_context=('key.crt','key.key'))
