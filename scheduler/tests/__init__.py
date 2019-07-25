from flask import Flask
from app import app
# from flask_restful import Api

# app_instance = Flask(__name__)
# api = Api(app_instance)
# configure_routes(api, scheduler, logging)
client = app.test_client()