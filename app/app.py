from flask import  Flask, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./testdb.db'
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/yourdatabase'
    app.config['UPLOAD_FOLDER'] = 'uploads'
    
    db.init_app(app)
    app.secret_key = 'your_secret_key_here'

    # User Login
    login_manager = LoginManager()
    login_manager.init_app(app)

    from models import User

    @login_manager.user_loader
    def load_user(uid):
        return User.query.get(uid)
    
    @login_manager.unauthorized_handler
    def unauthorized_callback():
        flash('Please Login')
        return redirect(url_for('login'))
       # return redirect(url_for('unauthorized_callback'))

    bcrypt = Bcrypt(app)

   # register_routes(app, db, bcrypt)
    from routes import register_routes
    register_routes(app, db, bcrypt)

    migrate = Migrate(app, db)

    return app