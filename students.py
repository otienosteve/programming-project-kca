import uuid
import os
from flask import Blueprint, render_template,request, flash, redirect, url_for
from werkzeug.utils import secure_filename
from flask_login import current_user, login_required
from forms import StudentDetailsForm, StudentDetailsUpdateForm, SiblingsForm, SiblingsUpdateForm,InstitutionDetailsForm,InstitutionDetailsUpdateForm
from models import User, StudentDetails,db, EducationDetails, Siblings

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

@student_bp.route('/details', methods=['GET', 'POST'])
def details():
    user = current_user
    form = StudentDetailsUpdateForm()
    student_details = StudentDetails.query.filter_by(user_id=current_user.id).first()
    form.photo_url.file = student_details.photo_url
    if request.method=='POST':
        if form.validate_on_submit():
            if form.data.get('photo_url'):
                file = form.data.get('photo_url')
                ext = file.filename.split('.')[-1]
                file.filename = str(uuid.uuid4())+'.'+ext
                filename = secure_filename(file.filename)
                file.save(os.path.join(os.environ.get('UPLOAD_FOLDER'), filename))
                student_details.photo_url= filename
            for key, value in form.data.items():
                if key == 'photo_url':
                    continue
                if value is not None:
                    setattr(student_details,key,value)
                    db.session.add(student_details)
                    db.session.commit()
    else:
        for field, errors in form.errors.items():
                for error in errors:
                    flash(f'Error in field "{getattr(form, field).label.text}": {error}', 'error')

    return render_template('student/details.html', user=user,student_details=student_details, form=form)

@student_bp.route('/education', methods=['GET','POST'])
def add_education():
    user = current_user
    form =InstitutionDetailsForm()
    if request.method == 'POST':
        print(form.data)
        if form.validate_on_submit():
            education_details = EducationDetails(institution_type=form.data.get('institution_type'),
                                                 institution_name=form.data.get('institution_name'),
                                                 institution_code=form.data.get('institution_code'),
                                                 level=form.data.get('level'),
                                                 campus=form.data.get('campus'),
                                                 course=form.data.get('course'),
                                                 mode_of_study=form.data.get('mode_of_study'),
                                                 funding_source=form.data.get('funding_source'),
                                                 details=form.data.get('details'),
                                                 grade='98',
                                                 start_date=form.data.get('start_date'),
                                                 end_date=form.data.get('end_date'),
                                                 user_id=current_user.id)
            db.session.add(education_details)
            db.session.commit()
            return redirect(url_for('student_bp.view_education'))
        else:
             for field, errors in form.errors.items():
                for error in errors:
                    flash(f'Error in field "{getattr(form, field).label.text}": {error}', 'error')
    
    return render_template('student/add-education.html', user=user, form=form)


@student_bp.route('/education_details', methods=['GET','POST'])
def view_education():
    user = current_user
    education_details = EducationDetails.query.filter_by(user_id=user.id).all()
    return render_template('student/view-education.html',user=user,education_details=education_details)

@student_bp.route('/education_by_id/<string:id>', methods=['GET','POST'])
def education_by_id(id):
    education = EducationDetails.query.filter_by(id=id).first()
    if education:
        db.session.delete(education)
        db.session.commit()
        return redirect(url_for('student_bp.view_education'))
    else: 
        flash('Education Does not Exist')
        return redirect(url_for('student_bp.view_education'))
    
@student_bp.route('/update_education/<string:id>', methods=['GET','POST'])
def update_education(id):
    education_details = EducationDetails.query.filter_by(id=id).first()
    form = InstitutionDetailsUpdateForm()
    user = current_user 
    form.details.data = education_details.details
    form.institution_type.data = education_details.institution_type.value 
    if request.method == 'POST':
        for key, value in form.data.items():
            if value is not None:
                setattr(education_details, key, value)
            db.session.add(education_details)
            db.session.commit()
        return redirect(url_for('student_bp.view_education'))
    return render_template('student/update-details.html', user=user, form=form, education_details=education_details)


# 
@student_bp.route('/siblings', methods=['GET','POST'])
def add_siblings():
    user = current_user
    form =SiblingsForm()
    if request.method == 'POST':
        print(form.data)
        if form.validate_on_submit():
            sibling_details = Siblings(name=form.data.get('name'),
                                         relationship=form.data.get('relationship'),
                                         institution = form.data.get('institution'),
                                         level = form.data.get('level'),
                                         total_annual_fees = form.data.get('total'),
                                         paid = form.data.get('paid'),
                                                 student_id=current_user.id)
            db.session.add(sibling_details)
            db.session.commit()
            return redirect(url_for('student_bp.view_siblings'))
        else:
             for field, errors in form.errors.items():
                for error in errors:
                    flash(f'Error in field "{getattr(form, field).label.text}": {error}', 'error')
    
    return render_template('student/add-siblings.html', user=user, form=form)


@student_bp.route('/sibling_details', methods=['GET','POST'])
def view_siblings():
    user = current_user
    sibling_details = Siblings.query.filter_by(student_id=user.id).all()
    return render_template('student/view-siblings.html',user=user,sibling_details=sibling_details)

@student_bp.route('/education_by_id/<string:id>', methods=['GET','POST'])
def sibling_by_id(id):
    education = EducationDetails.query.filter_by(id=id).first()
    if education:
        db.session.delete(education)
        db.session.commit()
        return redirect(url_for('student_bp.view_education'))
    else: 
        flash('Education Does not Exist')
        return redirect(url_for('student_bp.view_education'))
    
@student_bp.route('/update_education/<string:id>', methods=['GET','POST'])
def update_sibling(id):
    education_details = EducationDetails.query.filter_by(id=id).first()
    form = SiblingsUpdateForm()
    user = current_user 
    form.details.data = education_details.details
    form.institution_type.data = education_details.institution_type.value 
    if request.method == 'POST':
        for key, value in form.data.items():
            if value is not None:
                setattr(education_details, key, value)
            db.session.add(education_details)
            db.session.commit()
        return redirect(url_for('student_bp.view_education'))
    return render_template('student/update-details.html', user=user, form=form, education_details=education_details)
