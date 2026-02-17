import pytest
from src import create_app
from bs4 import BeautifulSoup

from flask import Flask

@pytest.mark.web 
def test_index_page(client):
    # Test that the index page loads successfully and contains key elements
    response = client.get('/')
    assert response.status_code == 200
    # Check for presence of key elements in the HTML
    soup = BeautifulSoup(response.data, 'html.parser')
    # Checks page load = success
    assert "Admissions Data Dashboard" in soup.get_text()
    assert "Answer:" in soup.get_text()  # Check that answer placeholders are present
    # Verifying buttons are there
    pull_data_button = soup.find('button', attrs = {'data-testid': 'pull-data-button'})
    update_data_button = soup.find('button', attrs = {'data-testid': 'update-data-button'})
    # Button exist AND correctly labeled
    assert pull_data_button is not None
    assert 'Pull Data' in pull_data_button.get_text()
    assert update_data_button is not None
    assert 'Update Analysis' in update_data_button.get_text()
    



