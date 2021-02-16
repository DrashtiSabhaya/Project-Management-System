from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)

from models.task import TaskModel


class Task(Resource):
    pass