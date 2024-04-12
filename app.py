import os

from flask import Flask, render_template
from flask_migrate import Migrate
from dotenv import load_dotenv

from auth import auth_bp, login_manager
from students import student_bp
from admin import admin_bp

from models import db


load_dotenv()

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def create_app():
    app = Flask(__name__,static_folder='static')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://supersteve:super1234@127.0.0.1:3306/bursary'
    app.config['SECRET_KEY'] = '4f334c6c66230ebc0857bcde98b7f05d'
    app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
    app.config['MAIL_PORT'] = os.environ.get('MAIL_PORT')
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS')
    app.config['MAIL_USE_SSL'] = os.environ.get('MAIL_USE_SSL')
    app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER','static')

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    migrate = Migrate(app, db)
    db.init_app(app)
    login_manager.init_app(app)
    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(admin_bp)


    return app


app = create_app()