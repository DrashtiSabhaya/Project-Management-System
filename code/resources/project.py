from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)

from models.project import ProjectModel


class Project(Resource):
    @jwt_required
    def get(self, name):
        project = ProjectModel.find_by_name(name)
        if project:
            return {"project": project.json()}, 200

        return {"message": "Project with Given Name is not Found"}, 404
    
