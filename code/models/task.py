from db import db
import datetime
from sqlalchemy import DateTime
from models.user import UserModel

################################################
# Class     : TaskModel
# Table     : sharedproject
# Fields    : id, task,
#             description,
#             project_id
# ForeignKey: ProjectModel,
# Methods   : 1. json(self)
#             2. find_by_name(cls, name)
#             3. find_by_project_id(cls, id)
#             4. all_tasks(cls)
#             5. save_to_db(self)
#             6. delete_from_db(self)
#################################################


class TaskModel(db.Model):

    __tablename__ = 'task'

    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(250), unique=False)
    description = db.Column(db.Text)
    # Proposed, Active, On Hold, Completed, Canceled, and Archived
    status = db.Column(db.String(120), unique=False)
    created_at = db.Column(DateTime, default=datetime.datetime.now)

    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    project = db.relationship('ProjectModel')

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), default=None)
    user = db.relationship('UserModel')

    isDeleted = db.Column(db.Integer, default=1)
    deletedDate = db.Column(DateTime, nullable=True)

    def __init__(self, task_name, description, project_id, status, user_id):
        self.task_name = task_name
        self.description = description
        self.status = status
        self.project_id = project_id
        self.user_id = user_id

    def json(self):
        return {
            "task_name": self.task_name,
            "description": self.description,
            "project_name": self.project.name,
            "created_at": str(self.created_at).split('.')[0],
            "status": self.status,
            "assigned_to": self.user.name,
            "isDeleted": self.isDeleted,
            "deletedDate": str(self.deletedDate).split('.')[0]
        }

    @classmethod
    def find_by_name(cls, name, project_id):
        return TaskModel.query.filter_by(task_name=name, project_id=project_id).first()

    @classmethod
    def find_by_project_id(cls, project_id):
        return TaskModel.query.filter_by(project_id=project_id, isDeleted=1).all()

    @classmethod
    def all_tasks(cls):
        return cls.query.order_by(cls.created_at.desc()).filter_by(isDeleted=1)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
