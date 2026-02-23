Name: Harry Ma (hm41)

Module Info: Module 4 - Testing and Documentation (Due: 02/15/26 11:59PM ET)

Approach: 
Test Suite Architecture: A comprehensive Pytest suite was established within the /tests directory to validate the stability of the Grad-Café system. The suite is organized into six specialized files: test_flask_page.py 
for UI rendering, test_buttons.py for endpoint logic, test_analysis_format.py for output precision, test_db_insert.py for data integrity, test_integration_end_to_end.py for full-flow validation, and test_extra_coverage
to capture missed tests. Markers were implemented in pytest.ini to allow for targeted execution of web, buttons, analysis, db, or integration tests.
CI/CD Hygiene: A GitHub Actions pipeline was configured in .github/workflows/tests.yml to automate the testing lifecycle on every push. To support database testing in a headless environment, a PostgreSQL 15 service 
container is orchestrated within the workflow. The pipeline utilizes a DATABASE_URL environment variable to connect the runner to the service, ensuring that the psycopg[binary] dependency correctly interfaces with 
the temporary database for schema verification and idempotency checks.
Coverage & Quality Control: To ensure no logic was left unverified, pytest-cov was integrated into the workflow. The pytest.ini configuration was set to enforce a 100% coverage requirement across all modules in 
the src/ directory. This forced the development of additional edge-case tests, such as verifying busy-gating behavior (returning a 409 status when a pull is already in progress) and ensuring that percentages are
strictly formatted to two decimal places in the Flask output.
Automated Documentation: Technical documentation was transitioned to Sphinx to provide a professional API reference and setup guide. The conf.py was updated with autodoc_mock_imports for psycopg and flask to allow
documentation builds on Read the Docs without a live database. The documentation includes an architecture overview, a detailed Testing Guide explaining the custom Pytest markers, and an API reference that 
automatically pulls docstrings from scrape.py, load_data.py, query_data, and app.py.

How to Run: 
1. Initialize postgreSQL locally 
2. Install requirements.test 
3. Run python3 -m pytest for coverage 
4. Access documentation via Read the Doc- https://jhu-software-concepts-hma41.readthedocs.io/en/latest/

Known Bugs: 
CI actions pipeline does not prove to be successful. I believe this is because I expose a flask factory correctly. This may be a fix that affect multiple documents. 
There seemed to be a missing piece between the localhost database and something called a unix socket. 
For some reason, the connection was not linked and kept raising errors in GitHub's workflow. Read online that I needed to change my connection and import 'os' to resolve 
this problem, but was hesitant (not sure if that was the correct path). Fixing flask factory first should be priority. 