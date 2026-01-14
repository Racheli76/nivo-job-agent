from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_upload_file_too_large():
    # create a dummy large file > 5MB
    large = b'a' * (5 * 1024 * 1024 + 10)
    files = {'file': ('big.txt', large, 'text/plain')}
    res = client.post('/upload-cv-file', files=files)
    assert res.status_code == 200
    data = res.json()
    assert data.get('error') == 'file_too_large'
    assert 'max_size' in data
