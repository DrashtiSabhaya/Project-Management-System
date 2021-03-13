from db import db
from sqlalchemy.dialects.postgresql import UUID
import uuid
import datetime
from sqlalchemy import DateTime
from models.user import UserModel

###############################################
# Class     : ProjectModel
# Table     : project
# Fields    : id, name, description,
#             created_by_id,
#             created_at
# ForeignKey: UserModel
# Methods   : 1. json(self)
#             2. find_by_name(cls, name)
#             3. find_by_owner_id(cls, owner_id)
#             4. all_projects(cls)
#             5. save_to_db(self)
#             6. delete_from_db(self)
#################################################


class ProjectModel(db.Model):

    __tablename__ = 'project'

    id = db.Column('id', db.Text(length=36), default=lambda: str(
        uuid.uuid4()), primary_key=True)
    name = db.Column(db.String(60))
    description = db.Column(db.Text)

    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.relationship('UserModel')

    isDeleted = db.Column(db.Integer, default=1)
    deletedDate = db.Column(DateTime, nullable=True)

    created_at = db.Column(DateTime, default=datetime.datetime.now)
    project_color_identity = db.Column(db.String(20))

    tasks = db.relationship('TaskModel', cascade="all,delete")
    users = db.relationship('ShareProjectModel', cascade="all,delete")

    def __init__(self, name, description, created_by_id, project_color_identity):
        self.name = name
        self.description = description
        self.created_by_id = created_by_id
        self.project_color_identity = project_color_identity

    # Return : Json Represent of Calling Object

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_by": self.created_by.name,
            "ownerid": self.created_by.username,
            "created_at": str(self.created_at).split('.')[0],
            "project_color_identity": self.project_color_identity,
            "tasks": [task.json() for task in self.tasks],
            "users": [user.json() for user in self.users]
        }

    # Parameter(name) : Project name
    # Return : Project Matched with Given Name
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    # Parameter(owner_id) : Project Owner id
    # Return : All Projects Owned by Given Owner_id
    @classmethod
    def find_by_owner_id(cls, owner_id):
        return cls.query.filter_by(created_by_id=owner_id)

    # Return : All Projects
    @classmethod
    def all_projects(cls):
        return cls.query.order_by(cls.created_at.desc()).filter_by(isDeleted=1)

    # Save or Update Project in Database
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # Delete Project from Database
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
