from db import db


class PermissionModel(db.Model):

    __tablename__ = 'permission'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.Text)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }

    @classmethod
    def find_by_name(cls, name):
        return PermissionModel.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, id):
        return PermissionModel.query.filter_by(id=id).first()

    @classmethod
    def all_permissions(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.sessoin.delete(self)
        db.session.commit()
