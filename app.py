from flask import Flask, request, session, g, redirect, url_for, render_template, jsonify
from flask.ext.login import LoginManager, UserMixin, login_required, current_user
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
    def __init__(self, username):
        data = db.collection.find({"user": username})[0]
        self.user = data['user']
        self.password = data['password']
        self.data = data['data']

    @classmethod
    def get(cls,uid):
        if db.collection.find({"user": uid}).limit(1).count() != 0:
            return db.collection.find({"user": uid})[0]


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
            user = User(user_entry['user'])
            # print user.username
            if (user.password == password):
                return user
            # return user_entry
    return None



@app.route("/")
def hello():
    #can be used to check connection status with api
    return jsonify({'status':'ok'})

@app.route("/api/")
@login_required
def status():
    #can be used to check login status
    # return jsonify({'status':user})
    return current_user.user

#----------------------------------------------------------------------------------------------------



# endpoint for retriving user data from db
#----------------------------------------------------------------------------------------------------
@app.route("/api/get-user-data" , methods=['GET'])
@login_required
def recieve():
    #retrive specific user data from cloud db
    return jsonify({
        'user' : current_user.user,
        'data' : current_user.data
    })

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
