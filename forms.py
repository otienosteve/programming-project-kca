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
    firstname = StringField('First Name',validators=[DataRequired(), Length(min=3, max=25)])
    lastname = StringField('Last Name',validators=[DataRequired(), Length(min=3, max=25)])
    contact_phone_number = StringField('Phone Number',validators=[DataRequired(),Length(min=10, max=12),Regexp(r'^([\s\d]+)$')])
    photo_url = FileField('photo', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
    gender = SelectField(choices=gender_choices)
    dob = DateField()
    place_of_birth = StringField(validators=[DataRequired(), Length(min=3, max=25)])
    village = StringField(validators=[DataRequired(), Length(min=3, max=25)])
    ward = StringField(validators=[DataRequired(), Length(min=3, max=25)])
    constituency = StringField(validators=[DataRequired(), Length(min=3, max=25)])
    submit =SubmitField('Add Bio Data')

class StudentDetailsUpdateForm(FlaskForm):
    firstname = StringField('First Name',validators=[ Length(min=3, max=25)])
    lastname = StringField('Last Name',validators=[ Length(min=3, max=25)])
    contact_phone_number = StringField('Phone Number',validators=[Length(min=10, max=12),Regexp(r'^([\s\d]+)$')])
    photo_url = FileField('photo', validators=[
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
    gender = SelectField(choices=gender_choices)
    dob = DateField()
    place_of_birth = StringField(validators=[ Length(min=3, max=25)])
    village = StringField(validators=[ Length(min=3, max=25)])
    ward = StringField(validators=[ Length(min=3, max=25)])
    constituency = StringField(validators=[ Length(min=3, max=25)])
    submit =SubmitField('Add Bio Data')

institution_choices = [('primary','primary'),
                       ('secondary','secondary'),
                       ('tetiary','tetiary')
                      ]

class InstitutionDetailsForm(FlaskForm):
    institution_type = SelectField('Institution Type',choices=institution_choices, validators=[DataRequired()])
    institution_name = StringField('Institution Name',validators=[DataRequired(), Length(min=3, max=25)])
    institution_code = StringField('(Where Applicable) Institution Code',validators=[DataRequired(), Length(min=3, max=25)])
    campus = StringField('(Where Applicable) Campus',validators=[DataRequired(), Length(min=3, max=25)])
    level = StringField('Level/year/class',validators=[DataRequired(), Length(min=3, max=25)])
    course = StringField('(Where Appplicable) Course',validators=[DataRequired(), Length(min=3, max=25)])
    mode_of_study = StringField('(Where Appplicable) Mode Of Study',validators=[DataRequired(), Length(min=3, max=25)])
    start_date = DateField('Start Date', format='%m/%d/%Y', validators=[DataRequired()])
    end_date =  DateField('Start Date', format='%m/%d/%Y', validators=[DataRequired()])
    details = TextAreaField('Funding Details', validators=[DataRequired()])
    funding_source = StringField('Funding Source',validators=[DataRequired()])
    grade = StringField('Grade/Marks', validators=[DataRequired()])
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('Start Date', validators=[DataRequired()])
    submit =SubmitField('Add Education Details')
    

class InstitutionDetailsUpdateForm(FlaskForm):
    institution_type = SelectField('Institution Type',choices=institution_choices, validators=[])
    institution_name = StringField('Institution Name',validators=[Length(min=3, max=25)])
    institution_code = StringField('(Where Applicable) Institution Code',validators=[Length(min=3, max=25)])
    campus = StringField('(Where Applicable) Campus',validators=[Length(min=3, max=25)])
    level = StringField('Level/year/class',validators=[Length(min=3, max=25)])
    course = StringField('(Where Appplicable) Course',validators=[Length(min=3, max=25)])
    mode_of_study = StringField('(Where Appplicable) Mode Of Study',validators=[Length(min=3, max=25)])
    start_date = DateField('Start Date', format='%m/%d/%Y', validators=[])
    end_date =  DateField('Start Date', format='%m/%d/%Y', validators=[])
    details = TextAreaField('Funding Details', validators=[])
    funding_source = StringField('Funding Source',validators=[])
    grade = StringField('Grade/Marks', validators=[])
    start_date = DateField('Start Date', validators=[])
    end_date = DateField('Start Date', validators=[])
    submit =SubmitField('Update Education Details')


class SiblingsForm(FlaskForm):
    name = StringField('Sibling Name',validators=[DataRequired()])
    relationship = StringField('Relationship',validators=[DataRequired()])
    institution = StringField('Institution',validators=[DataRequired()])
    total = StringField('Total Annual Fees', validators=[DataRequired()])
    level = StringField('Education Level', validators=[DataRequired()])
    paid = StringField('Total Paid',validators=[DataRequired()])
    submit =SubmitField('Add Sibling Details')

class SiblingsUpdateForm(FlaskForm):
    name = StringField('Sibling Name')
    relationship = StringField('Relationship')
    institution = StringField('Institution')
    total = StringField('Total Annual Fees')
    paid = StringField('Total Paid')
    submit =SubmitField('Update Sibling Details')