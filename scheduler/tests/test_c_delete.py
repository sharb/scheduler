from tests import client 
import json

header = {'mock': 'True'}


def test_delete_a():
    response = client.delete("/jobs/unittest-job-a/", 
        headers=header)
    assert b'"message":"removed a scheduled job"' in response.get_data()
    assert 200 == response.status_code


def test_delete_c():
    response = client.delete("/jobs/unittest-job-c/", 
        headers=header)
    assert b'"message":"removed a scheduled job"' in response.get_data()
    assert 200 == response.status_code
    

def test_delete_all():
    response = client.delete("/jobs/", headers=header)
    assert b'"message":"all job removed"' in response.get_data()
    assert 200 == response.status_code


def test_delete_none():
    response = client.delete("/jobs/none/", headers=header)
    assert b'"error":"job not found"' in response.get_data()
    assert 400 == response.status_code