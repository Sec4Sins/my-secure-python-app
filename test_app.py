import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_hello_world(client):
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Hello, World!'

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'

def test_user_endpoint(client):
    # Test the vulnerable SQL injection endpoint
    response = client.get('/user/1')
    assert response.status_code == 200

def test_ping_endpoint(client):
    # Test the vulnerable command injection endpoint
    response = client.get('/ping?host=localhost')
    assert response.status_code == 200

def test_hash_endpoint(client):
    # Test the weak crypto endpoint
    response = client.get('/hash/testpassword')
    assert response.status_code == 200
    data = response.get_json()
    assert 'hash' in data