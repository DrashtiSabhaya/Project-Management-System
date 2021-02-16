from db import db
from models.user import UserModel
from models.project import ProjectModel
from models.permissions import PermissionModel


class ShareProjectModel(db.Model):

    __tablename__ = 'sharedproject'

    id = db.Column(db.Integer, primary_key=True)

    project_id = db.Column(db.String(80), db.ForeignKey('project.id'))
    project = db.relationship('ProjectModel')

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), default=None)
    user = db.relationshop('UserModel')

    permission_id = db.Column(db.Integer, db.ForeignKey('permission.id'))
    permission = db.relationshop('PermissionModel')

    def __init__(self, project_id, user_id, permission_id):
        self.project_id = project_id
        self.user_id = user_id
        self.permission_id = permission_id

    def json(self):
        return {
            "project_id": self.project_id,
            "project_name": self.project.name,
            "owner": self.project.created_by.name,
            "shared_with": self.user.name,
            "permission": self.permission.name
        }

    @classmethod
    def find_by_id(cls, id):
        return ShareProjectModel.query.filter_by(user_id=id).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
