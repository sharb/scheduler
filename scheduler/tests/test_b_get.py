from tests import client 
import json

header = {'mock': 'True'}


def test_get_a():
    response = client.get("/jobs/unittest-job-a/", 
        headers=header)
    assert b'"image":"nginx",' in response.get_data()
    assert 200 == response.status_code


def test_get_c():
    response = client.get("/jobs/unittest-job-c/", 
        headers=header)
    assert b'"image":"jenkins",' in response.get_data()
    assert 200 == response.status_code


def test_get_all():
    response = client.get("/jobs/", headers=header)
    assert b'{"unittest-job-a":{"image":"nginx",' in response.get_data()
    assert b',"unittest-job-c":{"image":"jenkins",' in response.get_data()
    assert 200 == response.status_code


def test_get_none():
    response = client.get("/jobs/none/", headers=header)
    assert b'"error":"Job name does not exists"' in response.get_data()
    assert 400 == response.status_code