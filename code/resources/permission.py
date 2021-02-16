from flask_restful import Resource, reqparse
from models.permissions import PermissionModel


class Permission(Resource):
    def get(self, name):
        permission = PermissionModel.find_by_name(name=name)
        if permission:
            return permission.json()

        return {"message": "Permission Not found"}, 404

    def post(self, name):
        parse = reqparse.RequestParser()
        parse.add_argument(
            'description',
            type=str,
            required=True,
            help='Permission description required'
        )

        data = parse.parse_args()
        permission = PermissionModel.find_by_name(name=name)
        if permission:
            return {"message": "Permission name is already exists"}, 400

        permission = PermissionModel(name, data['description'])
        permission.save_to_db()
        return {"Message": "Permission is Saved"}, 200

    def delete(self, name):
        permission = PermissionModel.find_by_name(name=name)
        if permission:
            permission.delete_from_db()
            return {'message': 'Permission is Deleted!'}, 200

        return {"message": "Permission Not found"}, 404


class PermissionsList(Resource):
    def get(self):
        return {'permission': [per.json() for per in PermissionModel.all_permissions()]}, 200
