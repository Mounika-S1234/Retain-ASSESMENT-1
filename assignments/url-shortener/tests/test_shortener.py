import pytest
from app.main import app

@pytest.fixture
def client():
    app.testing = True
    return app.test_client()

def test_shorten_url(client):
    res = client.post('/api/shorten', json={"url": "https://example.com"})
    assert res.status_code == 201
    assert "short_code" in res.get_json()

def test_invalid_url(client):
    res = client.post('/api/shorten', json={"url": "invalid-url"})
    assert res.status_code == 400

def test_redirect_and_stats(client):
    res = client.post('/api/shorten', json={"url": "https://google.com"})
    data = res.get_json()
    code = data["short_code"]

    redirect_res = client.get(f'/{code}', follow_redirects=False)
    assert redirect_res.status_code == 302

    stats_res = client.get(f'/api/stats/{code}')
    stats = stats_res.get_json()
    assert stats["clicks"] >= 1
    assert stats["url"] == "https://google.com"
