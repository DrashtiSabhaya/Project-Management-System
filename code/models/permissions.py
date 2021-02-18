from db import db

########################################
# Class     : PermissionModel         
# Table     : permission               
# Fields    : id, name, description    
# Methods   : 1. json(self)
#             2. find_by_name(cls, name)  
#             3. all_permissions(cls)
#             4. save_to_db(self)
#             4. delete_from_db(self)
#########################################

class PermissionModel(db.Model):

    __tablename__ = 'permission'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.Text)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    ## Return : Json Represent of Calling Object
    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }

    ## Parameter(name) : Permission name 
    ## Return : Permission Matched with Given Name 
    @classmethod
    def find_by_name(cls, name):
        return PermissionModel.query.filter_by(name=name).first()

    ## Return : All Permissions 
    @classmethod
    def all_permissions(cls):
        return cls.query.all()

    ## Save or Update Permission in Database
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        
    ## Delete Permission in Database
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
