from flask import Flask
from flask_cors import CORS
from os import getenv
from dotenv import load_dotenv
#Blueprint for session
from src.routes.auth import auth
from src.routes.student import student 
from src.routes.classroom import classroom
from src.routes.activity import activity
from src.routes.catalogs import catalogs
#Blueprint for profile operations

#Blueprint for activities operations

#Blueprint for student operations

server_api = Flask(__name__)
CORS(server_api)

#Register blueprint to session
server_api.register_blueprint(auth, url_prefix='/auth')
server_api.register_blueprint(student, url_prefix='/student')
server_api.register_blueprint(classroom, url_prefix='/classroom')
server_api.register_blueprint(activity, url_prefix='/activity')
server_api.register_blueprint(catalogs, url_prefix='/catalogs')


if __name__ == '__main__':
    load_dotenv()
    server_api.run(host=getenv('host'), port=getenv('port'), debug=True)
