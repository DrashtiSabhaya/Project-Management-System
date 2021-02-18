from db import db

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
    def find_by_project_id(cls, project_id):
        return TaskModel.query.filter_by(project_id=project_id).all()

    @classmethod
    def all_tasks(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
