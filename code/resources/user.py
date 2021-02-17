from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    get_jwt
)
from models.user import UserModel
from datetime import timedelta

_user_parser = reqparse.RequestParser()
_user_parser.add_argument(
    'username',
    type=str,
    required=True,
    help="Username is Required!"
)
_user_parser.add_argument(
    'password',
    type=str,
    required=True,
    help="Password is Required!"
)

blacklist = set()


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        return user.json()

    @classmethod
    @jwt_required()
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        user.delete_from_db()
        return {'message': 'User Deleted!'}, 200


class UserRegister(Resource):
    def post(self):
        _user_parser.add_argument(
            'name',
            type=str,
            required=False,
            help="Name is Required!"
        )
        data = _user_parser.parse_args()

        if UserModel.find_by_username(data["username"]):
            return {"message": "Username is already exist"}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User Created Successfully!"}, 201


class UserLogin(Resource):
    @classmethod
    def post(cls):
        data = _user_parser.parse_args()
        user = UserModel.find_by_username(data['username'])

        if user:
            if user.active_status:
                if safe_str_cmp(user.password, data['password']):
                    access_token = create_access_token(
                        identity=user.id, fresh=True)
                    refresh_token = create_refresh_token(user.id)

                    return {
                        'access_token': access_token,
                        'refresh_token': refresh_token
                    }, 200

                return {'message': 'Invalid Password'}, 401
            return {'message': 'User is Currently not Activate'}, 401
        return {'message': 'Inavalid Username'}, 401


class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        blacklist.add(jti)
        return {"message": "Successfully Logged Out"}, 200


class UserStatus(Resource):
    @classmethod
    @jwt_required()
    def put(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404

        if user.active_status:
            user.active_status = False
        else:
            user.active_status = True

        user.save_to_db()
        return {'message': 'User Status Changed'}, 200


class UsersList(Resource):
    @jwt_required()
    def get(self):
        return {'users': [user.json() for user in UserModel.all_users()]}, 200
