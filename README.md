# Project_Management_System

This Repo contains all required Flask APIs for Project Management System.

Requirements
------------ 
- pip install python
- pip install flask_restful
- pip install falsk_jwt_extended
- pip install SQLAlchemy

Steps to run Apis
-----------------
1. Set up a virtual environment to use for our application ($ python3 -m venv env)
2. Install all libraries using requirements.txt file
3. Switch into /code dir
4. Run command : python app.py in console

# APIs
------
url = http://127.0.0.1:5000

| Name | URL | Request Type | Body | Response | Description |
|------|-----|--------------|-------|---------|-------------|
| Registration | {{url}}/register | POST |  {<br>  "name": "XXXX",<br>  "username": "XXXX",<br>  "password": "XXXX" <br> } | { <br>  "message": "User Created Successfully!" <br> } | User Registration |
| Login | {{url}}/login | POST |   {<br>    "username": "XXXX",<br>  "password": "XXXX" <br> } | {<br> "access_token": XXXX, <br> "refresh_token": XXXX <br> } | User Authentication |
| Logout | {{url}}/logout | POST | | {<br> "message": "Successfully Logged Out" <br>} | User Logout |
| Create Project | {{url}}/project/<name> | POST | {<br> "name": "XXXX",<br> "description": "XXXX",<br> "project_color_identity": "XXXX" <br>} | {<br> "message": "Project Successfully Created"<br>} | Create New Project |
| Get Project<br> [ Name ] | {{url}}/project/<name> | GET | | {<br>"project": {<br> "id": "XXXX",<br>"name": "XXXX",<br>"description": "XXXX",<br>"created_by": "XXXX",<br>"created_at": "XXXX",<br>"project_color_identity": "XXXX",<br> "tasks": [],<br>"users": []<br>}<br>} | To Get Project Details |
| Edit Project | {{url}}/project/<name> | PUT | {<br>"description":"XXXX"<br>"project_color_identity":<br>"XXXX"<br>} | {<br>    "message": "Project Details Updated" <br>} | Edit Project Details |
| Delete Project | {{url}}/project/<name> | DELETE ||{<br>"message": "Project is Deleted"<br>} | Delete Project |
| All Project List | {{url}}/projects | GET | |{<br> "projects": [ XXXX ] <br>} | It will List All Projects |
| My Project List<br> [Logged in User's] | {{url}}/myproject | GET | | {<br> "projects": [ XXXX ] <br>"shared_with_me": []<br>} | Project List of Logged in User | 
| Project Users | {{url}}/shared_project/<name> | GET | | {<br>"project_users": [] <br> } | List User of particular Project |
| Create Task | {{url}}/task/<name> | POST | {<br>"task_name": "XXXX",<br>"description": "XXXX",<br>"project_name": "XXXX"<br>} | {<br>"message": "Project Task Successfully Created"<br>} | Create New Task in Project |
| Get Task<br> [ Name ] | {{url}}/task/<name> | GET ||{<br>"task_name": "XXXX",<br>"description": "XXXX",<br>"project_name": "XXXX"<br>} | Get Task By Name |
| Edit Task | {{url}}/task/<name> | PUT | {<br>"task_name": "XXXX",<br>"description": "XXXX",<br>"project_name": "XXXX" <br>} | {<br>"message": "Task Details Updated"<br>} | Edit Task Details |
| Delete Task | {{url}}/task/<name> | DELETE | | {<br>Task is Deleted<br>}| Delete Task From Project |
| Task List <br> [ Project Name] | {{url}}/project/tasks/<name> | GET | | {<br>"project": "XXXX",<br>"total_task": XXXX,<br>"tasks": [ XXXX ]<br>} | Project Task List With Number Of Tasks |
| Share Project | {{url}}/project/share | POST | {<br>"project_name": "XXXX",<br>"user_id": "XXXX",<br> "permission": "XXXX"<br>} | {<br>"message": "Project is Shared Successfully"<br>} | Share Project With other User with View, Edit, Delete Permission |
| User List | {{url}}/users | GET | | {<br> "users": [ XXXX ]<br>} | List of all Users |
| Get User <br> [ Name ] | {{url}}/user/<userid> | GET | | {<br>"id": XXXX,<br>"name": "XXXX",<br>"username": "XXXX",<br> "active_status": XXXX <br>} | Get user Details with name |
| Change Active <br> Status | {{url}}/changestatus/<userid> | PUT | | {<br>"message": "User Status Changed"<br>} | Used To Active/Deactive User |
| Delete User | {{url}}/user/<userid> | DELETE | | {<br>"message": "User Deleted!"<br>} | Delete User From System |
| Create Permission | {{url}}/permission/<name> | POST | {<br>"description": "XXXX" <br>} | {<br>"message": "Permission is Saved"<br>} | Add Permission |
| Delete Permission | {{url}}/permission/<name> | DELETE | | {<br>"message": "Permission is Deleted!"<br>} | Delete Permission |
| Permission List | {{url}}/permissions | GET | | {<br>"permission": [ XXXX ]<br>} | Lists all Available Permissions |
| Task List | {{url}}/tasks | GET | | {<br>"tasks": [ XXXX ]<br>} | List All the Tasks |
