from fastapi.testclient import TestClient
from slowapi import Limiter
from slowapi.util import get_remote_address


def test_rate_limit_exceeded(monkeypatch):
    # import app after monkeypatching settings if needed
    from app import app
    # set a low limit for testing
    app.state.limiter = Limiter(key_func=get_remote_address, default_limits=['2/minute'])

    client = TestClient(app)
    res1 = client.get('/health')
    assert res1.status_code == 200
    res2 = client.get('/health')
    assert res2.status_code == 200
    res3 = client.get('/health')
    assert res3.status_code == 429
    # slowapi may return a human message or our handler's JSON; accept either
    try:
        body = res3.json()
        assert body.get('error') == 'rate_limit_exceeded' or 'Rate limit' in str(body)
    except Exception:
        assert 'Rate limit' in res3.text
