from flask_wtf import FlaskForm
from flask import current_app as app
from wtforms import (StringField, PasswordField,
                     SubmitField, SelectField,
                     TextAreaField, IntegerField,
                     FileField,DateField)
from wtforms.validators import DataRequired, Email, EqualTo, Length,Regexp
from flask_wtf.file import FileField, FileAllowed, FileRequired

class RegisterForm(FlaskForm):
    email = StringField(label='Email:', validators=[DataRequired(), Email()])
    name = StringField(label='Name', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[
                              DataRequired(), EqualTo('password')])
    id_no = StringField('Id No (Parent/Student)', validators=[DataRequired(),Length(min=6, max=8),Regexp(r'^([\s\d]+)$')])
    phone = StringField('Phone Number',validators=[DataRequired(),Length(min=10, max=12),Regexp(r'^([\s\d]+)$')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):

    email = StringField(label='Email:', validators=[DataRequired(), Email()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField('Login')

gender_choices = [('Male', 'Male'), ('Female','Female')]

class StudentDetailsForm(FlaskForm):
    firstname = StringField(validators=[DataRequired(), Length(min=3, max=25)])
    lastname = StringField(validators=[DataRequired(), Length(min=3, max=25)])
    contact_phone_number = StringField('Phone Number',validators=[DataRequired(),Length(min=10, max=12),Regexp(r'^([\s\d]+)$')])
    photo_url = FileField('Image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
    gender = SelectField(choices=gender_choices)
    dob = DateField()
    place_of_birth = StringField(validators=[DataRequired(), Length(min=3, max=25)])
    village = StringField(validators=[DataRequired(), Length(min=3, max=25)])
    ward = StringField(validators=[DataRequired(), Length(min=3, max=25)])
    constituency = StringField(validators=[DataRequired(), Length(min=3, max=25)])
    institution_name = StringField(validators=[DataRequired(), Length(min=3, max=25)])
    institution_code = StringField(validators=[DataRequired(), Length(min=3, max=25)])
    campus = StringField(validators=[DataRequired(), Length(min=3, max=25)])
    level = StringField(validators=[DataRequired(), Length(min=3, max=25)])
    course = StringField(validators=[DataRequired(), Length(min=3, max=25)])
    mode_of_study = StringField(validators=[DataRequired(), Length(min=3, max=25)])
    expected_completion_year = DateField('Start Date', format='%m/%d/%Y', validators=[DataRequired()])