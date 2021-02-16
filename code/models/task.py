from db import db


class TaskModel(db.Model):

    __tablename__ = 'task'

    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(250), unique=True)
    description = db.Column(db.Text)

    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    project = db.relationship('ProjectModel')

    def __init__(self, task_name, description, project_id):
        self.task_name = task_name
        self.description = description
        self.project_id = project_id

    def json(self):
        return {
            "task_name": self.task_name,
            "description": self.description,
            "project_name": self.project.name
        }

    @classmethod
    def find_by_name(cls, name):
        return TaskModel.query.filter_by(task_name=name).first()

    @classmethod
    def all_tasks(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
