import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_hello(client):
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert 'message' in data

def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'

def test_ping(client):
    response = client.get('/ping?host=google.com')
    assert response.status_code == 200

def test_user_endpoint(client):
    # Test the SQL injection endpoint (now with working database)
    response = client.get('/user/1')
    assert response.status_code == 200
    data = response.get_json()
    assert 'result' in data

def test_calc(client):
    response = client.get('/calc/2+2')
    assert response.status_code == 200
    data = response.get_json()
    assert data['result'] == 4