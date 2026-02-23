import pytest 
import re 
from bs4 import BeautifulSoup
from src import app

@pytest.mark.analysis
def test_analysis_format(client,monkeypatch):
    # Test Data
    fake_results = {
        'q1': 100,
        'q2': 50.02,
        'q3': (3.52, 280.53, 160.13, 4.18),
        'q4': 3.8,
        'q5': 20.0,
        'q6': 3.79,
        'q7': 10,
        'q8': 5,
        'q9': 2,
        'b1': 500,
        'b2': 200
    }
    # Monkeypatch the database query functions to return fake results
    monkeypatch.setattr('src.query_data', lambda:fake_results)
    response = client.get('/')
    # Testing GET request to index 
    assert response.status_code == 200
    # Beautiful Soup setup to parse HTML responses
    soup = BeautifulSoup(response.data, 'html.parser')
    # Modified all Answer paragraphs with added 'answer' id for easier search 
    answers = soup.find_all('p', id='answer')
    for answer in answers:
        text = answer.get_text()
        # Check that the answer follows the format "Answer: <value>"
        assert 'Answer: ' in text
        # Checking Percentage and decimal outputs having 2 decimal points 
        # GPA, GRE, GRE_subjects, etc
        if 'GPA' in text:
            assert re.search(r'GPA: \d+\.\d{2}+', text)
            assert re.search(r'GRE: \d+\.\d{2}+', text)
            assert re.search(r'GRE V: \d+\.\d{2}+', text)
            assert re.search(r'GRE AW: \d+\.\d{2}+', text)
        if '%' in text:
            assert re.search(r'Answer: \d+\.\d{2}%', text)

