Architecture
============
* **Web Layer**: Flask application serving the dashboard and handling "Pull Data" requests.
* **ETL Layer**: Scraper (urllib) and Loader (psycopg) modules.
* **DB Layer**: PostgreSQL storing applicant records with a unique URL constraint.