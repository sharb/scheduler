from flask import Flask
from app import configure_routes
from flask_restful import Api

app_instance = Flask(__name__)
api = Api(app_instance)
configure_routes(api)
client = app_instance.test_client()

def test_index_html():
    response = client.get("/")
    assert "<h1>Welcome To Schedular API</h1>" in response.get_data().decode()

def test_index_status():
    response = client.get("/")
    assert response.status_code == 200

def test_index_html2():
    response = client.get("/index")
    assert "<h1>Welcome To Schedular API</h1>" in response.get_data().decode()

def test_index_status2():
    response = client.get("/index")
    assert response.status_code == 200