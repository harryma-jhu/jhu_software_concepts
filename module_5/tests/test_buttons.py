import pytest 
from src import app

@pytest.mark.buttons
def test_pull_data_button(client, monkeypatch):
    # Mock subprocess.Popen to prevent actual execution
    monkeypatch.setattr("subprocess.Popen", lambda *args, **kwargs: None) 
    # Ensure is_busy is False for the test
    monkeypatch.setattr(app, 'is_busy', False) 
    # Setting redirects = True because button redirects to homepage -> Code 302 not 200
    response = client.post('/pull_data', follow_redirects=True)
    assert response.status_code == 200

@pytest.mark.buttons
@pytest.mark.parametrize("endpoint", ['/pull_data', '/update_analysis'])
def test_busy_state(client, monkeypatch, endpoint):
    monkeypatch.setattr(app, 'is_busy', True) # Set is_busy to True to simulate busy state
    response = client.post(endpoint)
    # Busy state test 
    assert response.status_code == 409
    # Verify Json returns expected values
    assert response.get_json() == {'busy': True}