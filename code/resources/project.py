from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from models.project import ProjectModel
from models.shareproject import ShareProjectModel


class Project(Resource):
    @jwt_required()
    def get(self, name):
        project = ProjectModel.find_by_name(name)
        if project:
            return {"project": project.json()}, 200

        return {"message": "Project with Given Name Doesn't Exist"}, 404

    @jwt_required()
    def post(self, name):
        project_parse = reqparse.RequestParser()
        project_parse.add_argument(
            'description',
            type=str,
            required=True,
            help="Project Description is required"
        )
        project_parse.add_argument(
            'project_color_identity',
            type=str,
            required=True,
            help="Project color identity is required"
        )

        project = ProjectModel.find_by_name(name)
        if project:
            return {"message": "Project with given Name Already Exists"}, 400

        data = project_parse.parse_args()
        project = ProjectModel(
            name,
            data['description'],
            get_jwt_identity(),
            data['project_color_identity']
        )
        project.save_to_db()
        return {"message": "Project Successfully Created"}, 200

    @jwt_required()
    def put(self, name):
        project_parse = reqparse.RequestParser()
        project_parse.add_argument(
            'name',
            type=str,
            required=False,
            help="Project Description is required"
        )
        project_parse.add_argument(
            'description',
            type=str,
            required=False,
            help="Project Description is required"
        )
        project_parse.add_argument(
            'project_color_identity',
            type=str,
            required=False,
            help="Project color identity is required"
        )

        data = project_parse.parse_args()
        project = ProjectModel.find_by_name(name)

        if project:
            if project.created_by_id == get_jwt_identity():
                if data['name'] != None:
                    project.name = data['name']

                if data['description'] != None:
                    project.description = data['description']

                if data['project_color_identity'] != None:
                    project.project_color_identity = data['project_color_identity']

                project.save_to_db()
                return {"message": "Project Details Updated"}, 200

            else:
                user = ShareProjectModel.get_user_permissions(
                    get_jwt_identity(), project.id)
                if user:
                    if user.permission.name == 'Edit' or user.permission.name == 'Delete':
                        if data['project_color_identity'] != None:
                            project.project_color_identity = data['project_color_identity']

                        project.save_to_db()
                        return {"message": "Project Details Updated"}, 200

                    return {"message": "You Don't have enough permissions to Update the Project"}, 401

                return {"message": "You are not part of this Project"}, 401

        return {"message": "Project With Given Name Doesn't Exist"}, 404

    @jwt_required()
    def delete(self, name):
        project = ProjectModel.find_by_name(name)

        if project:
            if project.created_by_id == get_jwt_identity():
                project.delete_from_db()
                return {"message": "Project is Deleted"}, 200

            else:
                user = ShareProjectModel.get_user_permissions(
                    get_jwt_identity(), project.id)
                if user:
                    if user.permission.name == 'Delete':
                        project.delete_from_db()
                        return {"message": "Project is Deleted"}, 200

                    return {"message": "You Don't have enough permissions to Delete the Project"}, 401

                return {"message": "You are not part of this Project"}, 401

        return {"message": "Project With Given Name Doesn't Exist"}, 404


class ProjectsList(Resource):
    @classmethod
    def get(cls):
        return {"projects": [project.json() for project in ProjectModel.all_projects()]}, 200


class UserProjectList(Resource):
    @classmethod
    @jwt_required()
    def get(cls):
        my_projects = [
            project.json() for project in ProjectModel.all_projects(
            ) if project.created_by_id == get_jwt_identity()
        ]
        shared_with_me = [
            project.json()
            for project in ShareProjectModel.find_by_user_id(get_jwt_identity())
        ]

        return {"my_projects": my_projects, "shared_with_me": shared_with_me}, 200


class SharedProjects(Resource):
    @classmethod
    @jwt_required()
    def get(cls, name):
        project = ProjectModel.find_by_name(name)
        if project:
            shared_projects = [
                project.json() for project in ShareProjectModel.find_by_project_id(project.id)
            ]
            return {"project_users": shared_projects}, 200

        return {"message": "Project with Given Name Doesn't Exist"}, 404
