from flask import Flask
from app import configure_routes, scheduler, logging
from flask_restful import Api

app_instance = Flask(__name__)
api = Api(app_instance)
configure_routes(api, scheduler, logging)
client = app_instance.test_client()