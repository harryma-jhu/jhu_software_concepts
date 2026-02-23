import pytest
import psycopg
import json 
from src import app as flask_app
import src.scrape as sc
from urllib import error
import src.load_data as ld 
@pytest.mark.extras

# app.py exceptions 
def test_pull_data_exception(client, monkeypatch):
    # Triggers the 'except Exception' block in /pull_data (Lines 54-55)
    def mock_fail():
        raise Exception("Simulated Scraper Failure")
    
    monkeypatch.setattr("src.app.scrape_page", mock_fail)
    
    response = client.post('/pull_data')
    assert response.status_code == 500
    assert response.json['ok'] is False

def test_pull_data_busy_conflict(client):
    # Triggers the 'if is_busy' block in /pull_data
    flask_app.is_busy = True
    try:
        response = client.post('/pull_data')
        assert response.status_code == 409
        assert response.json['busy'] is True
    finally:
        # Reset global state for other tests
        flask_app.is_busy = False 

# load_data.py 
def test_load_data_full_coverage(monkeypatch):
    # Targets src/load_data.py to hit line 91 and 96-117.
    # Force the connection logic (Line 91) to run by resetting global state
    monkeypatch.setattr(ld, "conn", None)
    # Needed help with this one and did some reading/research
    # Set up to verify syntax in SQL create table query (line 96-117)
    # Mimics the psycogp connection and cursor - does nothing but is needed for testing
    class StubCursor:
        def execute(self, query, vars=None): 
            return None
        def __enter__(self): 
            return self
        def __exit__(self, *args): 
            pass
    class StubConn:
        def cursor(self): 
            return StubCursor()
        def commit(self): 
            pass
        def __enter__(self): 
            return self
        def __exit__(self, *args): 
            pass
    monkeypatch.setattr("psycopg.connect", lambda *args, **kwargs: StubConn())

    # Trigger get_connection() -> This hits Line 91
    conn = ld.get_connection()
    assert conn is not None

    # Trigger create_table() -> This hits SQL schema 
    ld.create_table()
    

def test_load_data_loop_coverage(monkeypatch):
    # Targets loop logic coverage 
    # Create a simple stub for the active connection
    # Sim to above 
    class SimpleStub:
        def cursor(self):
            class InternalStub:
                def execute(self, *args): pass
                def __enter__(self): return self
                def __exit__(self, *args): pass
            return InternalStub()
        def commit(self): pass
    
    monkeypatch.setattr(ld, "conn", SimpleStub())

    # Mock the built-in 'open' function to return a fake JSON string
    # This ensures the 'for record in data' loop actually executes
    class FakeFile:
        def read(self, *args):
            return json.dumps([{
                "program": "Computer Science MS",
                "university": "JHU",
                "comments": "test",
                "date_added": "2026-01-01",
                "overview_url": "http://test.com/1",
                "applicant_status": "Accepted",
                "start_term": "Fall 2026",
                "citizenship": "US",
                "gpa": "4.0",
                "degree_level": "MS"
            }])
        def __enter__(self): return self
        def __exit__(self, *args): pass

    monkeypatch.setattr("builtins.open", lambda *args, **kwargs: FakeFile())
    # Run the function to hit the internal loop and string parsing
    ld.load_data()


# scrape.py 
def test_get_html_http_errors(monkeypatch):
    # Targets the except blocks in get_html for specific status codes
    
    def mock_urlopen_error(req):
        # 404 error
        raise error.HTTPError("http://test.com", 404, "Not Found", {}, None)

    monkeypatch.setattr("urllib.request.urlopen", mock_urlopen_error)
    
    # This hits the 404 branch and prints the message
    result = sc.get_html("http://test.com")
    assert result is None

def test_get_html_bad_request(monkeypatch):
   # 400 error
    
    def mock_urlopen_400(req):
        raise error.HTTPError("http://test.com", 400, "Bad Request", {}, None)

    monkeypatch.setattr("urllib.request.urlopen", mock_urlopen_400)
    
    result = sc.get_html("http://test.com")
    assert result is None

# Targets save_to_db 
def test_save_to_db_coverage(monkeypatch):
    # Mimics connection and cursor - does nothing but needed     
    class StubCursor:
        def execute(self, query, values=None): pass
        def __enter__(self): return self
        def __exit__(self, *args): pass

    class StubConn:
        def cursor(self): return StubCursor()
        def commit(self): pass
        def __enter__(self): return self
        def __exit__(self, *args): pass

    # Patch psycopg.connect to avoid real DB calls
    monkeypatch.setattr("psycopg.connect", lambda x: StubConn())

    # Mock data that includes a GPA to hit the float conversion line
    fake_data = [{
        "university": "JHU",
        "program": "CS",
        "comments": "Nice",
        "date_added": "Feb 16",
        "overview_url": "http://link.com",
        "applicant_status": "Accepted",
        "start_term": "Fall",
        "citizenship": "US",
        "gpa": "3.9",
        "gre_general": "330",
        "degree_level": "MS",
        "llm-generated-program": None,
        "llm-generated-university": None
    }]

    # This executes the entire save_to_db function
    sc.save_to_db(fake_data)

# Target regex_extract
def test_regex_extract_none():
    # Else none
    assert sc.regex_extract(r'GPA\s*([\d\.]+)', "No grades here") is None

# Target save_data
def test_save_data_file(monkeypatch):
    class FakeFile:
        def write(self, string): pass
        def __enter__(self): return self
        def __exit__(self, *args): pass

    monkeypatch.setattr("builtins.open", lambda *a, **k: FakeFile())
    sc.save_data([{"test": "data"}])

def test_get_html_generic_http_error(monkeypatch):
    # Target error code thats not 400/404
    
    def mock_urlopen_500(req):
        # Trigger an error code that is NOT 400 or 404
        raise error.HTTPError("http://test.com", 500, "Internal Server Error", {}, None)

    monkeypatch.setattr("urllib.request.urlopen", mock_urlopen_500)
    
    # This will trigger: print(f"HTTP Error 500 for URL: http://test.com")
    result = sc.get_html("http://test.com")
    assert result is None