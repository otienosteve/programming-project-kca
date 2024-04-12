import uuid
import os
from flask import Blueprint, render_template,request, flash, redirect, url_for
from werkzeug.utils import secure_filename
from flask_login import current_user, login_required
from forms import (StudentDetailsForm, \
                   StudentDetailsUpdateForm,
                     SiblingsForm,
                       SiblingsUpdateForm,
                       InstitutionDetailsForm,
                       InstitutionDetailsUpdateForm,
                       ParentGuradianFrom,
                       ParentGuradianUpdateFrom,
                       DocumentsForm,
                       DocumentsUpdateForm)
from models import( User, 
                   StudentDetails,
                   db, 
                   EducationDetails,
                     Siblings,
                       ParentGuardian,
                         Documents)

student_bp = Blueprint('student_bp',__name__,url_prefix='/student')

@student_bp.route('/home')
@login_required
def student_home():
    user = current_user
    return render_template('student/student-dashboard.html', user=user)

@student_bp.route('/')
@login_required
def main():
    user = current_user
    return render_template('student/main.html', user=user)


@student_bp.route('/add_bio_data', methods=['GET','POST'])
@login_required
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
@login_required
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
@login_required
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
                                                 grade=form.data.get('grade'),
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
@login_required
def view_education():
    user = current_user
    education_details = EducationDetails.query.filter_by(user_id=user.id).all()
    return render_template('student/view-education.html',user=user,education_details=education_details)

@student_bp.route('/education_by_id/<string:id>', methods=['GET','POST'])
@login_required
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
@login_required
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
@login_required
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
@login_required
def view_siblings():
    user = current_user
    sibling_details = Siblings.query.filter_by(student_id=user.id).all()
    return render_template('student/view-siblings.html',user=user,sibling_details=sibling_details)


@student_bp.route('/sibling_by_id/<string:id>', methods=['GET','POST'])
@login_required
def sibling_by_id(id):
    sibling = Siblings.query.filter_by(id=id).first()
    if sibling:
        db.session.delete(sibling)
        db.session.commit()
        return redirect(url_for('student_bp.view_siblings'))
    else: 
        flash('Education Does not Exist')
        return redirect(url_for('student_bp.view_siblings'))


@student_bp.route('/update_siblings/<string:id>', methods=['GET','POST'])
@login_required
def update_sibling(id):
    sibling_details = Siblings.query.filter_by(id=id).first()
    form = SiblingsUpdateForm()
    user = current_user 
    if request.method == 'POST':
        for key, value in form.data.items():
            if value is not None:
                setattr(sibling_details, key, value)
            db.session.add(sibling_details)
            db.session.commit()
        return redirect(url_for('student_bp.view_siblings'))
    return render_template('student/update-siblings.html', user=user, form=form, sibling_details=sibling_details)



# Add Parents
@student_bp.route('/parent', methods=['GET','POST'])
@login_required
def add_parent():
    user = current_user
    form =ParentGuradianFrom()
    if request.method == 'POST':
        print(form.data)
        if form.validate_on_submit():
            parent_details = ParentGuardian(parent_type=form.data.get('parent_type'),
                                            first_name=form.data.get('first_name'),
                                         last_name=form.data.get('last_name'),
                                         occupation = form.data.get('occupation'),
                                         main_income_source = form.data.get('main_income_source'),
                                         other_income_source = form.data.get('other_income_source'),
                                         employment_status = form.data.get('employment_status'),
                                         average_monthly_income = form.data.get('average_monthly_income'),
                                                 student_id=current_user.id)
            db.session.add(parent_details)
            db.session.commit()
            return redirect(url_for('student_bp.view_parent'))
        else:
             for field, errors in form.errors.items():
                for error in errors:
                    flash(f'Error in field "{getattr(form, field).label.text}": {error}', 'error')
    
    return render_template('student/add-parent.html', user=user, form=form)



@student_bp.route('/view_parent', methods=['GET','POST'])
@login_required
def view_parent():
    user = current_user
    parent_details = ParentGuardian.query.filter_by(student_id=user.id).all()
    return render_template('student/view-parent.html',user=user,parent_details=parent_details)


@student_bp.route('/parent_by_id/<string:id>', methods=['GET','POST'])
@login_required
def parent_by_id(id):
    parent = ParentGuardian.query.filter_by(id=id).first()
    if parent:
        db.session.delete(parent)
        db.session.commit()
        return redirect(url_for('student_bp.view_parent'))
    else: 
        flash('Education Does not Exist')
        return redirect(url_for('student_bp.view_parent'))
    

@student_bp.route('/update_parent/<string:id>', methods=['GET','POST'])
@login_required
def update_parent(id):
    parent_details = ParentGuardian.query.filter_by(id=id).first()
    form = ParentGuradianUpdateFrom()
    user = current_user 
    if request.method == 'POST':
        for key, value in form.data.items():
            if value is not None:
                setattr(parent_details, key, value)
            db.session.add(parent_details)
            db.session.commit()
        return redirect(url_for('student_bp.view_parent'))
    return render_template('student/update-parent.html', user=user, form=form, parent_details=parent_details)



# add documents
@student_bp.route('/add_document', methods=['GET','POST'])
@login_required
def add_document():
    user = current_user
    form = DocumentsForm()
    if request.method=='POST':
        print(form.data)
        if form.validate_on_submit():
            file = form.data.get('document')
            ext = file.filename.split('.')[-1]
            file.filename = str(uuid.uuid4())+'.'+ext
            filename = secure_filename(file.filename)
            file.save(os.path.join(os.environ.get('UPLOAD_FOLDER'), filename))
            new_document= Documents(student_id=current_user.id,
                                         name=form.data.get('name'),
                                        document_type=form.data.get('document_type'),
                                        description= form.data.get('description'),
                                        document=filename)
                                      
                                      
            db.session.add(new_document)
            db.session.commit()
            return redirect(url_for('student_bp.view_document'))
        else: 
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'Error in field "{getattr(form, field).label.text}": {error}', 'error')
    return render_template('student/add-documents.html', form=form, user=user)


@student_bp.route('/view_document', methods=['GET','POST'])
@login_required
def view_document():
    user = current_user
    docuemnt_details = Documents.query.filter_by(student_id=user.id).all()
    return render_template('student/view-documents.html',user=user,docuemnt_details=docuemnt_details)


@student_bp.route('/docuemnt_by_id/<string:id>', methods=['GET','POST'])
@login_required
def document_by_id(id):
    docuemnt = Documents.query.filter_by(id=id).first()
    if docuemnt:
        db.session.delete(docuemnt)
        db.session.commit()
        return redirect(url_for('student_bp.view_docuemnt'))
    else: 
        flash('Education Does not Exist')
        return redirect(url_for('student_bp.view_document'))
    

@student_bp.route('/update_document/<string:id>', methods=['GET','POST'])
@login_required
def update_document(id):
    docuemnt_details = Documents.query.filter_by(id=id).first()
    form = DocumentsUpdateForm()
    user = current_user 
    if request.method == 'POST':
        for key, value in form.data.items():
            if value is not None:
                setattr(docuemnt_details, key, value)
            db.session.add(docuemnt_details)
            db.session.commit()
        return redirect(url_for('student_bp.view_docuemnt'))
    return render_template('student/update-document.html', user=user, form=form, docuemnt_details=docuemnt_details)