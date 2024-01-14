import os

from flask import Flask, make_response, jsonify, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_bcrypt import Bcrypt

from models import db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

bcrypt = Bcrypt(app)

class CheckSession(Resource):

    def get(self):
        user = User.query.filter(User.id == session.get('user_id')).first()
        if user:
            return user.to_dict()
        else: 
            return {}, 401
        
class ClearSession(Resource):

    def delete(self):
        
        session['user_id'] = None

        return {}, 204

class Login(Resource):

    def post(self):
        username = request.get_json().get('username')
        user = User.query.filter(User.username == username).first()
        password = request.get_json().get('password')

        if user.authenticate(password):
            session['user_id'] = user.id
            return user.to_dict(), 200
        
        return {}, 401


api.add_resource(CheckSession, '/check_session')
api.add_resource(ClearSession, '/clear_session')
api.add_resource(Login, '/login')

if __name__ == "__main__":
    app.run(debug=False)