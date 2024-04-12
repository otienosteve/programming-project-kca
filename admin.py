from flask import Blueprint, render_template,request, flash, redirect, url_for
from forms import BursaryForm, BursaryUpdateForm
from models import Bursary, db
from flask_login import login_required


admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin')

@admin_bp.route('/main')
def home():
    return render_template('admin/main.html')

@admin_bp.route('/add_bursary', methods=['GET','POST'])
def add_bursary():
    form = BursaryForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_bursary = Bursary(title= form.data.get('title'), 
                                  description =form.data.get('description'),
                                  fund_amount= form.data.get('fund_amount'),
                                   contact_person= form.data.get('contact_person'), 
                                    contact_person_contact= form.data.get('contact_person_contact') )
            db.session.add(new_bursary)
            db.session.commit()
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'Error in field "{getattr(form, field).label.text}": {error}', 'error')


    return render_template('admin/add-bursary.html', form = form)

@admin_bp.route('/view_bursaries')
def view_bursaries():
    bursaries = Bursary.query.all()
    return render_template('admin/view-bursaries.html', bursaries=bursaries)


@admin_bp.route('/bursary_by_id/<string:id>', methods=['GET','POST'])
@login_required
def delete_bursary(id):
    bursary = Bursary.query.filter_by(id=id).first()
    if bursary:
        db.session.delete(bursary)
        db.session.commit()
        return redirect(url_for('admin_bp.view_bursaries'))
    else: 
        flash('Bursary Does not Exist')
        return redirect(url_for('student_bp.view_bursaries'))
    
@admin_bp.route('/update_bursary<string:id>',methods=['GET','POST'])
def update_bursary(id):
    bursary = Bursary.query.filter_by(id=id).first()
    form = BursaryUpdateForm()
    if request.method=='POST':
         for key, value in form.data.items():
            if value is not None:
                setattr(bursary, key, value)
            db.session.add(bursary)
            db.session.commit()
    return render_template('admin/update-bursary.html', bursary=bursary, form=form)