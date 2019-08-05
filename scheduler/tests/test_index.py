from tests import client


def test_index_html():
    response = client.get("/")
    assert "<h1>Welcome To Scheduler API</h1>" in response.get_data().decode()


def test_index_status():
    response = client.get("/")
    assert response.status_code == 200


def test_index_html2():
    response = client.get("/index")
    assert "<h1>Welcome To Scheduler API</h1>" in response.get_data().decode()


def test_index_status2():
    response = client.get("/index")
    assert response.status_code == 200
