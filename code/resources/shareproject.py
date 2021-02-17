from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from models.shareproject import ShareProjectModel
from models.project import ProjectModel
from models.user import UserModel
from models.permissions import PermissionModel


class ShareProject(Resource):
    project_parse = reqparse.RequestParser()
    project_parse.add_argument(
        'project_name',
        type=str,
        required=True,
        help='Project Name is required'
    )
    project_parse.add_argument(
        'user_id',
        type=int,
        required=True,
        help="User id is required to Share a project"
    )
    project_parse.add_argument(
        'permission',
        type=str,
        required=True,
        help="Permission Name is required"
    )

    @classmethod
    @jwt_required()
    def post(cls):
        data = cls.project_parse.parse_args()

        project = ProjectModel.find_by_name(data['project_name'])
        user = UserModel.find_by_id(data['user_id'])
        permission = PermissionModel.find_by_name(name=data['permission'])

        if project is None:
            return {"message": "Project with Given Name Doesn't Exist"}, 404

        if permission is None:
            return {"message": "Inavlid Permission Name"}, 404

        if user.id == get_jwt_identity():
            return {"message": "You are owner of this Project, Please Select Other User to Share Project"}

        if user:
            if user.active_status:
                if project.created_by_id == get_jwt_identity():
                    share_project = ShareProjectModel(
                        project.id, user.id, permission.id)
                    share_project.save_to_db()
                    return {"message": "Project is Shared Successfully"}, 200

                return {"message": "You don't have Permission to Share this Project"}, 401

            return {"message": "User is Not Active"}, 401

        return {"message": "User with Given Name Doesn't Exist"}, 404

    