from tests import client 
import json, pytest

header = {'mock': 'True'}


def test_delete_all():
    response = client.delete("jobs", headers=header)
    assert b'{"message": "all job removed"}\n' in response.get_data()


def test_scheduled_job():
    response = client.post("/jobs/unittest-job-a", 
        json = {"image": "nginx", "time_scheduled": "2019-08-28 06:00:00.00"}, 
        headers=header)
    assert b'{"message": "job scheduled in' in response.get_data()
    assert 201 == response.status_code


def test_now_job():
    response = client.post("/jobs/unittest-job-b", 
        json = {"image": "nginx", "time_scheduled": "now"}, 
        headers=header)
    assert b'{"message": "job mock scheduled"}' in response.get_data()
    assert 201 == response.status_code


def test_scheduled_job_2():
    response = client.post("/jobs/unittest-job-c", 
        json = {"image": "jenkins", "time_scheduled": "2019-08-28 06:00:00.00"}, 
        headers=header)
    assert b'{"message": "job scheduled in' in response.get_data()
    assert 201 == response.status_code


def test_json_validation():
    response = client.post("/jobs/unittest-job-d", 
        json = {"image": "jenkins", "time_scheduled": "2019--08-28 06:00:00.00"}, 
        headers=header)
    assert b'{"error": "datetime format not valid"}' in response.get_data()
    assert 400 == response.status_code


def test_json_validation_b():
    response = client.post("/jobs/unittest-job-d", 
        json = {"image-": "jenkins", "time_scheduled": "2019--08-28 06:00:00.00"}, 
        headers=header)
    assert b'{"error": "please provide a valid job"}' in response.get_data()
    assert 400 == response.status_code


def test_duplicate_job():
    response = client.post("/jobs/unittest-job-c", 
        json = {"image": "jenkins", "time_scheduled": "2019-08-28 06:00:00.00"}, 
        headers=header)
    assert b'{"error": "job already scheduled to run' in response.get_data()
    assert 409 == response.status_code
