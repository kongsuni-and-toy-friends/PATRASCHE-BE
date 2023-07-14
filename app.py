from flask import Flask, jsonify
from flask_restx import Api,cors
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
from resources import create_api, create_socketio
import os
import xml.etree.ElementTree as elemTree
from datetime import timedelta
from db import db

#SECRET_KEY = config['DEFAULT']['SECRET_KEY']
#db_name = config['DEFAULT']['DB_NAME']+'.db'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./config/swm-pat.json"

host = "0.0.0.0"
port = 5000
expire_duration = 1

tree = elemTree.parse('config/keys.xml')
secretkey = tree.find('string[@name="secret_key"]').text

app = Flask(__name__)

app.secret_key = secretkey
db_info = {
    "user": tree.find('string[@name="DB_USER"]').text,
    "password": tree.find('string[@name="DB_PASS"]').text,
    "host": tree.find('string[@name="DB_HOST"]').text,
    "port": tree.find('string[@name="DB_PORT"]').text,
    "database": tree.find('string[@name="DB_DBNAME"]').text
}


app.config['JWT_SECRET_KEY'] = secretkey
app.config[
     'SQLALCHEMY_DATABASE_URI'] = f"mysql://{db_info['user']}:{db_info['password']}@{db_info['host']}:{db_info['port']}/{db_info['database']}"
#app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_POOL_RECYCLE'] = 499
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 20

app.config['PROPAGATE_EXCEPTIONS'] = True
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=expire_duration)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=180)

CORS(app)
api = Api(app) #API FLASK SERVER

sock = SocketIO(app,cors_allowed_origins="*")

#this will be used for login(authenticate users)
jwt = JWTManager(app) #this will make endpoint named '/auth' (username,password)
#JWT will be made based on what authenticate returns(user) and JWT will be sent to identity to identify which user has Vaild JWT

#API works with resouce
#200 ok
#201 created
#202 accepted
#400 Bad request
#404 NotFounded
#
# @jwt.user_claims_loader
# def add_claims_to_jwt(identity):  # Remember identity is what we define when creating the access token
#     if identity == 1:   # instead of hard-coding, we should read from a config file or database to get a list of admins instead
#         return {'is_admin': True}
#     return {'is_admin': False}
#
# @jwt.invalid_token_loa
#
# der
# def invalid_token_callback(error):  # we have to keep the argument here, since it's passed in by the caller internally
#     return jsonify({
#         'message': 'Signature verification failed.',
#         'error': 'invalid_token'
#     }), 401
#
# @jwt.unauthorized_loader
# def missing_token_callback(error):
#     return jsonify({
#         "description": "Request does not contain an access token.",
#         'error': 'authorization_required'
#     }), 401
#
# @jwt.revoked_token_loader
# def revoked_token_callback():
#     return jsonify({
#         "description": "The token has been revoked.",
#         'error': 'token_revoked'
#     }), 401
@app.route('/health')
def health():
    return "OK"

@app.before_request
def create_tables():
    db.create_all()

create_api(api)
#create_socketio(sock)


if __name__ == "__main__":
    print("Now we Run...")
    db.init_app(app)
    app.run(host=host,port=port,debug=False)
    #sock.run(app,host=host,port=port,debug=False)