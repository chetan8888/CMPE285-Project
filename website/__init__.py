from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
import os
basedir = os.path.abspath(os.path.dirname(__file__))



db = SQLAlchemy()
DB_NAME = "database.db"

# engine = create_engine(
#     "sqlite://", 
#     connect_args={"check_same_thread": False}, 
#     poolclass=StaticPool
# )

def create_app():
    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'omeopwqpondv5ryt6uhgfhd'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # app.config['SQLALCHEMY_DATABASE_URI'] =\
    # 'sqlite:///' + os.path.join(basedir, 'data.sqlite')

    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, portfolio
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    # if not path.exists('website/' + DB_NAME):
    db.create_all(app=app)
    print('Created Database!')