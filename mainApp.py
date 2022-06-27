
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from os import path
import json


db = SQLAlchemy()
DB_NAME = 'userinfo.db'


def create_app():

    app=Flask(__name__)
    app.config['SECRET_KEY'] = 'adityaf17'
    app.config['SQLALCHEMY_DATABASE_URI']=f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from views import views
    # from models import Contacts,Posts

    app.register_blueprint(views,url_prefix='/')

    create_database(app)

    return app



def create_database(app):
    if not path.exists(DB_NAME):
        db.create_all(app=app)

        print('Database created')


if __name__=='__main__':
    app = create_app()
    app.run(debug=True)