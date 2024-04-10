from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import LoginManager, login_required, login_user, logout_user

from forms import RegisterForm, LoginForm
from models import User, db

auth_bp = Blueprint('auth_bp', __name__, template_folder='templates')
login_manager = LoginManager()
login_manager.login_view = "auth_bp.login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        print(form.data)
        if form.validate_on_submit():
            hashed_password = generate_password_hash(
                form.data['password'], method='pbkdf2')
            new_user = User(email=form.data.get('email'), password_hash=hashed_password,id_no=form.data.get('id_no'), name=form.data.get('name'), phone=form.data.get('phone'), role='student')
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('auth_bp.login'))
        else:
            flash("Error, Check data submitted and try again!")
            return render_template('auth/registeru.html', form=form)
        
    return render_template('auth/registeru.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            payload = form.data
            user = User.query.filter_by(email=payload['email']).first()
            if not user:
                flash('User Does not Exist')
                return render_template('auth/loginu.html', form=form)
            if check_password_hash(user.password_hash, payload['password']):
                login_user(user)
                if user.role =='admin':
                    return redirect(url_for('admin_bp.home'))
                if user.role == 'examiner':
                    return redirect(url_for('examiner_bp.home'))
                return redirect(url_for('student_bp.student_home'))
            else:
                flash('Incorrect Password Entered')
                return render_template('auth/loginu.html', form=form)

    return render_template('auth/loginu.html', form=form)


@auth_bp.route('/test')
@login_required
def test():
    return "logged in"


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("student_bp.student_home"))



@auth_bp.route('/access_denied')
def forbidden():

    return render_template('503.html')
