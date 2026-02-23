import pytest
from bs4 import BeautifulSoup
@pytest.fixture
def mock_scraper_data():
    # Fake Data inputs - not used?? 
    return [
        {
            "university": "Johns Hopkins University",
            "degree": "MS",
            "season": "Fall",
            "year": 2026,
            "status": "Accepted",
            "gpa": 3.95,
            "is_intl": False,
            "decision_date": "2026-02-15"
        },
        {
            "university": "Stanford",
            "degree": "PhD",
            "season": "Fall",
            "year": 2026,
            "status": "Rejected",
            "gpa": 3.80,
            "is_intl": True,
            "decision_date": "2026-02-10"
        }
    ]
@pytest.mark.integration
def test_end_to_end_pipeline(client, mock_scraper_data):
 
    # Requirement: End-to-end (pull -> update -> Render)
   
    # Pull 
    pull_res = client.post('/pull_data')
    assert pull_res.status_code == 200
    assert pull_res.json['ok'] is True

    # Update
    update_res = client.post('/update_analysis')
    assert update_res.status_code == 302 # Redirects to '/'

    # Render
    response = client.get('/')
    assert response.status_code == 200
    
    soup = BeautifulSoup(response.data, 'html.parser')
    
    # Verify that the "Answer:" labels exist for the new data
    answers = soup.find_all(string=lambda text: "Answer:" in text)
    assert len(answers) > 0
    
    # Verify is_internation -> 2 decimal place output %
    page_text = soup.get_text()
    assert "50.00%" in page_text 

@pytest.mark.integration
def test_multiple_pulls_idempotency(client):
    # Verifying no duplicates
    from src.query_data import get_total_count
    from src.load_data import get_connection
    
    # Manually manage the connection for the test
    conn = get_connection()
    with conn.cursor() as cur:
        # First PUll
        client.post('/pull_data')
        count_1 = get_total_count(cur)
        # Second PULL 
        client.post('/pull_data')
        count_2 = get_total_count(cur)
        
        assert count_1 == count_2
    conn.close()