import uuid
import os
from flask import Blueprint, render_template,request, flash, redirect, url_for
from werkzeug.utils import secure_filename
from flask_login import current_user, login_required
from forms import StudentDetailsForm
from models import User, StudentDetails,db

student_bp = Blueprint('student_bp',__name__,url_prefix='/student')

@student_bp.route('/home')
@login_required
def student_home():
    user = current_user
    return render_template('student/student-dashboard.html', user=user)


@student_bp.route('/add_bio_data', methods=['GET','POST'])
def add_details():
    user = current_user
    form = StudentDetailsForm()
    if request.method=='POST':
        test_exist = StudentDetails.query.filter_by(user_id=current_user.id).first()
        if test_exist:
            flash('You cannot create bio twice, Update Bio')
            return redirect(url_for('student_bp.details'))
        if form.validate_on_submit():
            file = form.data.get('photo_url')
            ext = file.filename.split('.')[-1]
            file.filename = str(uuid.uuid4())+'.'+ext
            filename = secure_filename(file.filename)
            file.save(os.path.join(os.environ.get('UPLOAD_FOLDER'), filename))
            new_user_details = StudentDetails(user_id=current_user.id,firstname=form.data.get('firstname'),
                                      lastname=form.data.get('lastname'),contact_phone_number=form.data.get('contact_phone_number'), 
                                      photo_url=filename,gender=form.data.get('gender'),dob=form.data.get('dob'),place_of_birth=form.data.get('place_of_birth'),
                                      village=form.data.get('village'),ward=form.data.get('ward'),
                                      constituency=form.data.get('constituency'))
            db.session.add(new_user_details)
            db.session.commit()
            return redirect(url_for('student_bp.details'))
        else: 
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'Error in field "{getattr(form, field).label.text}": {error}', 'error')
    return render_template('student/student-details.html', form=form, user=user)

@student_bp.route('/details')
def details():
    user = current_user
    form = StudentDetailsForm()
    student_details = StudentDetails.query.filter_by(user_id=current_user.id).first()
    form.photo_url.data = student_details.photo_url
    if request.method=='POST':
        if form.validate_on_submit():
            for key, value in form.data.items():
                if value is not None:
                    setattr(student_details,key,value)
                    db.session.add(student_details)
                    db.session.commit()
    else:
        for field, errors in form.errors.items():
                for error in errors:
                    flash(f'Error in field "{getattr(form, field).label.text}": {error}', 'error')
    return render_template('student/details.html', user=user,student_details=student_details, form=form)
