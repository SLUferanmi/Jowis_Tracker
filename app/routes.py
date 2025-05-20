from flask import render_template, redirect, url_for
from flask import flash, request, Blueprint
from flask_login import login_user, logout_user, login_required, current_user
from .dbmodels import User, db, Project, Milestone, Task
from app import db
from .forms import SignupForm, ProjectForm, MilestoneForm
from werkzeug.security import generate_password_hash, check_password_hash

# Create a blueprint for the main routes
main = Blueprint("main", __name__)

# Route for the home page
@main.route("/")
def index(): 
    return render_template("index.html")

# Route for dashboard page
@main.route("/dashboard")
@login_required
def dashboard():
    if current_user.role == "manager":
        # Fetch all users for manager
        users = User.query.all()
    else:
        projects = current_user.projects
        # Fetch projects for employee
    return render_template("dashboard.html", projects=projects)

# Route for login page
@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method== "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for("main.dashboard"))
        else:
            flash("Invalid username or password", "danger")
    return render_template("login.html")
    
@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))


# Route for signup page
@main.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        existing_mail = User.query.filter_by(email= form.email.data).first()
        existing_username = User.query.filter_by(username= form.username.data).first()

        if existing_mail:
            flash("Email already registered. Please use a different email.", "danger")
            return redirect(url_for("main.signup"))
        
        if existing_username:
            flash("Username already taken. Please choose a different username.", "danger")
            return redirect(url_for("main.signup"))
        
        # Create a new user instance
        new_user = User(
            username = form.username.data, 
            email= form.email.data
        )
        new_user.set_password(form.password.data)
        
        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()
        flash("Account created successfully! You can now log in.", "success")
        return redirect(url_for("main.login"))
    
    return render_template("signup.html", form=form)

# Route for creating a new project


@main.route('/add_project', methods=['GET', 'POST'])
@login_required
def add_project():
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(
            title=form.title.data,
            description=form.description.data,
            user_id=current_user.id
        )
        db.session.add(project)
        db.session.commit()
        flash('Project added successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('add_project.html', form=form)

@main.route('/project/<int:project_id>/add_milestone', methods=['GET', 'POST'])
@login_required
def add_milestone(project_id):
    form = MilestoneForm()
    project = Project.query.get_or_404(project_id)
    if form.validate_on_submit():
        milestone = Milestone(
            name=form.name.data,
            deadline=form.deadline.data,
            completed=form.completed.data,
            project_id=project_id
        )
        db.session.add(milestone)
        db.session.commit()
        flash('Milestone added successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('add_milestone.html', form=form, project_id=project_id)
