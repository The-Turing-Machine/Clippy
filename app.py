from flask import Flask, request, session, g, redirect, url_for, render_template, jsonify
from flask.ext.login import LoginManager, UserMixin, login_required
import requests
import json
import os
from flask.ext.cors import CORS


from pymongo import MongoClient

from OpenSSL import SSL

# from werkzeug.serving import make_ssl_devcert
# make_ssl_devcert('key', host='localhost')

# context = SSL.Context(SSL.SSLv23_METHOD)
# context.use_privatekey_file('key.key')
# context.use_certificate_file('key.crt')




def connect():
    # Temporary !!
    connection = MongoClient("ds023118.mlab.com",23118)
    handle = connection["users"]
    handle.authenticate("admin","1234")# .......
    return handle



app = Flask(__name__)
CORS(app)
login_manager = LoginManager()
login_manager.init_app(app)
db = connect()



class User(UserMixin):
    #edit this
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
    #can be used to check connection status with api
    return jsonify({'status':'ok'})

@app.route("/api/")
@login_required
def status():
    #can be used to check login status
    return jsonify({'status':'ok'})

#----------------------------------------------------------------------------------------------------



# endpoint for retriving user data from db
#----------------------------------------------------------------------------------------------------
@app.route("/api/get/<user>/" , methods=['GET'])
def recieve(user):
    #retrive specific user data from cloud db

    try:

        if db.collection.find({"user": user}).limit(1).count() == 0:
            #user does not exist
            return jsonify({'status':'Error','msg':'That username does not exist !!'})

        else:
            #return user's data
            return jsonify({
                'user' : db.collection.find({"user": user})[0]['user'],
                'data' : db.collection.find({"user": user})[0]['data']
            })

    except Exception as e:
        return jsonify({'status':'Error','msg':'An exception has occured !! - ' + e.message})
#----------------------------------------------------------------------------------------------------



# endpoint for storing user data in db
#----------------------------------------------------------------------------------------------------
@app.route('/api/post/', methods=['POST'])
def send():
    #send data to cloud db for storage
    try:
        if request.method == 'POST':
            tempdata = json.loads(request.data)

            #check if user exist in database
            if db.collection.find({"user": tempdata['user']}).limit(1).count() == 0:
                #user does not exist, create one
                db.collection.insert(tempdata)
                return jsonify({'status':'success','msg':'created-user'})

            else:
                #user exists , add each item in new list to orignal list, ignore duplicates
                db.collection.update(
                    {"user": tempdata['user']},
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
if __name__ == "__main__":
    global json_data
    app.config["SECRET_KEY"] = "SuperDuperSecretKey!"
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True,port=port,host='0.0.0.0',ssl_context=('key.crt','key.key'))
