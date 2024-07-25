import os

class Config:
    MYSQL_HOST = 'ovh6.mirohost.net'
    MYSQL_USER = 'u_aptashenko'
    MYSQL_PASSWORD = 'Aptashenko93'
    MYSQL_DB = 'utprozorro_db'
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False