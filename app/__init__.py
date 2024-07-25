from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    CORS(app)
    MYSQL_HOST = 'ovh6.mirohost.net'
    MYSQL_USER = 'u_aptashenko'
    MYSQL_PASSWORD = 'Aptashenko93'
    MYSQL_DB = 'utprozorro_db'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}'

    db.init_app(app)
    migrate.init_app(app, db)

    return app