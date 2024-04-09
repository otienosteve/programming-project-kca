from flask import Blueprint, render_template
from flask_login import current_user, login_required
from forms import StudentDetailsForm

student_bp = Blueprint('student_bp',__name__,url_prefix='/student')

@student_bp.route('/home')
@login_required
def student_home():
    # user = current_user
    # print(user.name)
    return render_template('student/student-dashboard.html')


@student_bp.route('/details')
def add_details():
    form = StudentDetailsForm()
    return render_template('student/details.html', form=form)
