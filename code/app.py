from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask.json import jsonify

from resources.user import (
    User,
    UserRegister,
    UserLogin,
    UserLogout,
    UserStatus,
    UsersList
)
from resources.permission import Permission, PermissionsList


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']


app.secret_key = 'Project_Management_System'
api = Api(app)

jwt = JWTManager(app)


@app.before_first_request
def create_tables():
    db.create_all()


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'error': 'Token Expired',
        'description': 'The token has expired!'
    }), 401


@jwt.invalid_token_loader
def inavlid_token_callback(error):
    return jsonify({
        'error': 'Invalid Token',
        'description': 'The Signature Verification failed'
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'error': 'Authorization Required',
        'description': 'Request Does not contain access token'
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'error': 'Token Revoked',
        'description': 'The token has been Revoked'
    }), 401


api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserStatus, '/changestatus/<int:user_id>')
api.add_resource(UsersList, '/users')

api.add_resource(Permission, '/permission/<string:name>')
api.add_resource(PermissionsList, '/permissions')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
