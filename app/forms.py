from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, DateField, BooleanField, DateTimeField
from wtforms.validators import DataRequired, Email, Length

class SignupForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField("Sign Up")

class ProjectForm(FlaskForm):
    title = StringField('Project Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Create Project')

class MilestoneForm(FlaskForm):
    name = StringField('Milestone Name', validators=[DataRequired()])
    deadline = DateTimeField("Deadline (YYYY-MM-DD HH:MM:SS)", format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()])
    completed = BooleanField('Completed')
    submit = SubmitField('Add Milestone')