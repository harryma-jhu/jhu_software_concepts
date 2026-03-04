Name: Harry Ma (hm41)

Module Info: Module 3 - Database Queries Assignment Experiment (Due: 02/08/26 11:59PM ET)

Approach: 
1.Database Initization: A PostgreSQL database was established using Homebrew to manage the applicant data. The table applicants was designed with a specific schema to support both historical JSON data and live 
scraped data. Key columns include a url field with a UNIQUE constraint to serve as a primary identifier and prevent duplicate entries, and a degree field to separate the program level from the department name. 
create_table() in load_data.py ensures the structure is consistent across environments.

2.Data Alignment: A PostgreSQL database was established using Homebrew to manage the applicant data. The table applicants was designed with a specific schema to support both historical JSON data and live scraped 
data. Key columns include a url field with a UNIQUE constraint to serve as a primary identifier and prevent duplicate entries, and a degree field to separate the program level from the department name. 
create_table() in load_data.py ensures the structure is consistent across environments.

3.Dynamic Scraper Integration: The scraper.py from Module 2 was updated to interface directly with the database via psycopg. The save_to_db() function was added to map the scraper's dictionary keys (like location)
to the database's specific columns (like us_or_international). 

4.Backend/Analytics: query_data.py contains the analytical "brain" of the project. Case-insensitive pattern matching using ILIKE was utilized for all university and program searches (e.g., %Johns Hopkins%) to ensure 
accuracy regardless of user typos or casing. The Flask app.py coordinates the flow:
1)The @app.route('/') gathers 11 distinct metrics, ranging from Fall 2026 applicant counts to JHU-specific admission rates.
2)The /pull_data route uses subprocess.Popen to launch the scraper in the background, allowing the user to continue browsing the dashboard while new data is being fetched.
3)Flask flash messages provide real-time feedback on the success or failure of database operations.

5.UI Design: User Interface Design The dashboard was built with a clean, grid-based CSS layout. Key metrics are highlighted in "cards" for scannability. A dedicated "Data Management" section was added at the bottom 
to house the "Pull Data" button, while the "Update Analysis" button was positioned in the top-right to allow for quick refreshes of the analytical metrics without a full page reload. The layout was polished by
the assistance of an AI agent. 

How to Run: 
With Repo cloned:
1. Initialize postgreSQL locally 
2. Install necessary libraries in requirements.txt
3. Run loat_data.py to initialize SQL database 
4. Launch app
5. Navigate to localhost or http://127.0.0.1:8080

Known Bugs: 
Integration Issues: 
In Section 4 of the Approach- I had difficulty implementing the communication between the web interface and scrape.py. I believe that there is a data scheme discrepancy between what is being generated in scrape.py vs 
what the SQL table is looking for. I've read that it may also be due to the date format that GradCafe(ex: 'Februrary 25, 2026') uses is not compatable with postgreSQL's date formatting. 
