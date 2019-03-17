import os

from flask import Flask
from flask import redirect, g
from flask import render_template
from flask import request, session
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from flask_login import LoginManager, UserMixin, current_user, login_user, login_required, logout_user, login_manager

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "taskdb.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.secret_key = "very secret"
login = LoginManager()
login.init_app(app)
login.login_view = 'login'
db = SQLAlchemy(app)

class Task(db.Model):
    '''
    Define task name and status as well as connect it to the user table.
    '''
    __tablename__ = 'Task'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    status = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    def __repr__(self):
        return "<Title: {}>".format(self.title)

class User(UserMixin, db.Model):
    '''
    Define user names, passwords, and their tasks.
    '''
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200))
    password = db.Column(db.String(200))
    task_id = db.relationship('Task', backref='user', lazy='dynamic')
    def __repr__(self):
        return "<Username: {}>".format(self.username)

# Create db
db.create_all()
db.session.commit()


@app.route('/', methods=['GET', 'POST'])
def welcome():
    '''
    Redirect users to the login page.
    '''
    return redirect('login')

@login.user_loader
def load_user(id):
    '''
    Load users using user_loader.
    '''
    return User.query.get(int(id))

@app.route('/register', methods=['GET','POST'])
def register():
    '''
    Register new users.
    '''
    if request.method == 'POST':
        # Check password requirements
        if len(request.form['password']) < 8:
            error = 'Your password should be at least 8 symbols long. Please, try again.'
            return render_template('register.html', error=error)
        if request.form['password'] != request.form['repeat']:
            error = 'Passwords do not match. Please, try again.'
            return render_template('register.html', error=error)

        new_user = User(username=request.form['username'], password=request.form['password'])
        db.session.add(new_user)
        db.session.commit()
        return redirect("/login")
    elif request.method == 'GET':
        return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    ''' Log in existing users.
    '''
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username'], password=request.form['password']).first()
        # Check whether credentials are valid
        if user is None:
            error = 'Invalid credentials. Please, try again.'
            return render_template('login.html', error=error)
        login_user(user)
        return redirect("/main")
    elif request.method == 'GET':
        return render_template('login.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    '''
    Log users out.
    '''
    session.pop('logged_in', None)
    return redirect('login')

@app.route('/main', methods=["GET", "POST"])
# Make sure only authorized users can access the main page
@login_required
def home():
    '''
    Add tasks to the Kanban board
    '''
    g.user = current_user
    tasks = None
    error = None
    if request.form:
        try:
            # Ensure tasks are unique
            if request.form.get("title") in [task.title for task in Task.query.all()]:
                error = "This task already exists."
            else:
                task = Task(id = 1, title=request.form.get("title"), status=request.form.get("status"), user_id = g.user.id)
                tasks = Task.query.all()

                db.session.add(task)
                db.session.commit()
        except Exception as e:
            print("Failed to add task")
            print(e)
    # Sort tasks according to their status
    tasks = Task.query.filter_by(user_id=g.user.id).all()
    todo = Task.query.filter_by(status='todo',user_id=g.user.id).all()
    doing = Task.query.filter_by(status='doing',user_id=g.user.id).all()
    done = Task.query.filter_by(status='done',user_id=g.user.id).all()
    return render_template("home.html", error=error, tasks=tasks, todo=todo, doing=doing, done=done, myuser=current_user)

@app.route("/update", methods=["POST"])
def update():
    '''
    Move tasks to other categories.
    '''
    try:
        newstatus = request.form.get("newstatus")
        name = request.form.get("name")
        task = Task.query.filter_by(title=name).first()
        task.status = newstatus
        db.session.commit()
    except Exception as e:
        print("Couldn't update task status")
        print(e)
    return redirect("/main")

@app.route("/delete", methods=["POST"])
def delete():
    '''
    Delete tasks.
    '''
    title = request.form.get("title")
    task = Task.query.filter_by(title=title).first()
    db.session.delete(task)
    db.session.commit()
    return redirect("/main")

if __name__ == "__main__":
    app.run(debug=True)
