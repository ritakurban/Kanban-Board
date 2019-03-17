# Kanban-Board 📋

This project is an implementation of a Kanban Board with three sections "To do", "Doing", and "Done" created in Flask. 
<img width="1280" alt="Screen Shot 2019-03-17 at 15 00 34" src="https://user-images.githubusercontent.com/29481335/54495832-66630280-48c6-11e9-8b5c-27e52b927f53.png">

# Functionality
1. Register new users. The password should contain at least 8 symbols.
2. Log in with user's credentials.
3. Add tasks to any of the categories.
4. Delete tasks.
5. Transfer tasks from "To Do" to "Doing" and from "Doing" to "Done".
6. Logout from the app.

Each user can maintain their own Kanban board that is not visible to other users.

To run it on your computer, clone the repository and do the set up from the `'.../Kanban-Board-master/'`  directory. 


 ## Set Up Virtual Environment and Requirements
```python
python3.6 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

## Set Up the Database
```python
#run from the Python shell (by typing python3 in the terminal)
from kanban import db
db.create_all()
exit()
```
 

## Run the App 
```python

python app.py
 
#Then go to --> http://127.0.0.1:5000/ <--
 ```
 
 ## Run the Unit Tests 
 
 ```python
 
 #from the directory '.../tests/'
 
 python tests.py
 ```

