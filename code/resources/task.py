from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)

from models.task import TaskModel
from models.project import ProjectModel
from models.shareproject import ShareProjectModel


class Task(Resource):
    @jwt_required()
    def get(self, name):
        task = TaskModel.find_by_name(name)
        if task:
            return task.json()
        return {"message": "Task with given name Doesn't Exists"}, 404

    @jwt_required()
    def post(self, name):
        task_parse = reqparse.RequestParser()
        task_parse.add_argument(
            'task_name',
            type=str,
            required=True,
            help="Task Name is required"
        )
        task_parse.add_argument(
            'description',
            type=str,
            required=True,
            help="Task description is required"
        )
        task_parse.add_argument(
            'project_name',
            type=str,
            required=True,
            help="Project Name is required"
        )

        data = task_parse.parse_args()

        project = ProjectModel.find_by_name(data['project_name'])
        if project:
            if project.created_by_id == get_jwt_identity():
                task = TaskModel.find_by_name(name)
                if task and task.project_id == project.id:
                    return {"message": "Task with Given Name is Already exist in Same Project"}, 401

                task = TaskModel(
                    data['task_name'],
                    data['description'],
                    project.id
                )
                task.save_to_db()

                return {"message": "Project Task Successfully Created"}, 200

            return {"message": "You Don't have enough permissions to Add Task in the Project"}, 401

        return {"message": "Project with Given Name Doesn't Exist"}, 404

    @jwt_required()
    def put(self, name):
        task_parse = reqparse.RequestParser()
        task_parse.add_argument(
            'task_name',
            type=str,
            required=False,
            help="Task Name is required"
        )
        task_parse.add_argument(
            'description',
            required=False,
            help="Task description is required"
        )
        task_parse.add_argument(
            'project_name',
            type=str,
            required=True,
            help="Project Name is required"
        )
        data = task_parse.parse_args()

        project = ProjectModel.find_by_name(data['project_name'])
        if project:
            task = TaskModel.find_by_name(name)
            if task and project.id == task.project_id:
                if project.created_by_id == get_jwt_identity():
                    if data['task_name'] is not None:
                        task.task_name = data['task_name']

                    if data['description'] is not None:
                        task.description = data['description']
                    task.project_id = project.id
                    task.save_to_db()
                    return {"message": "Task Details Updated"}, 200

                else:
                    user = ShareProjectModel.get_user_permissions(
                        get_jwt_identity(), project.id)
                    if user:
                        if user.permission.name == 'Edit' or user.permission.name == 'Delete':
                            if data['task_name'] is not None:
                                task.task_name = data['task_name']

                            if data['description'] is not None:
                                task.description = data['description']

                            task.project_id = project.id

                            task.save_to_db()
                            return {"message": "Task Details Updated"}, 200

                    return {"message": "You Don't have enough permissions to Add Task in the Project"}, 401

            return {"message": "Task Doesn't Exist in this Project"}, 401

        return {"message": "Project with Given Name Doesn't Exist"}, 404

    @jwt_required()
    def delete(self, name):
        task_parse = reqparse.RequestParser()
        task_parse.add_argument(
            'project_name',
            type=str,
            required=True,
            help="Project Name is required"
        )
        data = task_parse.parse_args()

        project = ProjectModel.find_by_name(data['project_name'])
        if project:
            task = TaskModel.find_by_name(name)
            if task and project.id == task.project_id:
                if project.created_by_id == get_jwt_identity():
                    task.delete_from_db()
                    return {"message": "Task is Deleted"}, 200

                return {"message": "You Don't have enough permissions to Add Task in the Project"}, 401

            return {"message": "Task Doesn't Exist in this Project"}, 401

        return {"message": "Project with Given Name Doesn't Exist"}, 404


class ProjectTaskList(Resource):
    @classmethod
    @jwt_required()
    def get(cls, name):
        project = ProjectModel.find_by_name(name)
        if project:
            return {
                "project": project.name,
                "total_task": len(TaskModel.find_by_project_id(project.id)),
                "tasks": [task.json() for task in TaskModel.find_by_project_id(project.id)]
            }, 200
        return {"message": "Project with Given Name Doesn't Exist"}, 404


class TaskList(Resource):
    @classmethod
    def get(cls):
        return {"tasks": [task.json() for task in TaskModel.all_tasks()]}, 200
