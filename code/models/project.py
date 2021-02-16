from db import db
from sqlalchemy.dialects.postgresql import UUID
import uuid
import datetime
from sqlalchemy import DateTime


class ProjectModel:

    __tablename__ = 'project'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.Text)

    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.relationship('UserModel')

    created_at = db.Column(DateTime, default=datetime.datetime.now)
    project_color_identity = db.Column(db.String(20), unique=True)

    tasks = db.relationship('taskModel', lazy='dynamic')

    def __init__(self, name, description, created_by_id, project_color_identity):
        self.name = name
        self.description = description
        self.created_by_id = created_by_id
        self.project_color_identity = project_color_identity

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_by": self.created_by.name,
            "created_at": str(self.created_at).split('.')[0],
            "project_color_identity": self.project_color_identity,
            "tasks": [task.json() for task in self.tasks.all()]
        }

    @classmethod
    def find_by_name(cls, name):
        return ProjectModel.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, id):
        return ProjectModel.query.filter_by(id=id).first()

    @classmethod
    def all_projects(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
