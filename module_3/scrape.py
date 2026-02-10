from urllib import request,error
from bs4 import BeautifulSoup
import json
import re
import psycopg

# Configuration
base_url = "https://www.thegradcafe.com/survey/index.php?page="
output_file = "applicant_data.json"
# Number of entries to scrape
target = 50
# HTTP Headers - to mimic a browser request
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}

# Function to get HTML content from a URL
# Try/Except block to handle HTTP errors
def get_html(url):
    try:
        req =request.Request(url, headers=HEADERS)
        with request.urlopen(req) as response:
            html = response.read()
            return html
    
    except error.HTTPError as err:
        # Handle different HTTP error codes
        if err.code == 400:
            print(f"Bad Request for URL: {url}")
        elif err.code == 404:
            print(f"Not Found for URL: {url}")
        else:
            print(f"HTTP Error {err.code} for URL: {url}")
        return None
# Function to extract GPA/GRE data using regex    
def regex_extract(pattern, grade_text):
    # GRE ### or GPA #.##
    match = re.search(pattern, grade_text)
    return match.group(1) if match else None
# Function to save scraped data (list of dictionaries) to a JSON file
def save_data(data):
    # Indent = 4 for readability
    with open("applicant_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# Function to clean and extract relevant data from HTML rows
def clean_data(main_row, secondary_row=None, comment_row=None):
    # Parsed main row content: application information
    col = main_row.find_all('td')
    # University name
    university = col[0].find('div', class_='tw-font-medium').get_text(strip=True)
    # Program details
    program = col[1].find('div', class_='tw-text-gray-900')
    program_details = program.find_all('span')
    program_name = program_details[0].get_text(strip=True) if len(program_details) > 0 else None
    program_type = program_details[1].get_text(strip=True) if len(program_details) > 1 else None
    # Date added to the site
    date_added = col[2].get_text(strip=True)
    # Application status
    status = col[3].get_text(strip=True)
    # Entry URL
    link_tag = col[4].find('a', href=True)
    entry_url = f"https://www.thegradcafe.com{link_tag['href']}"

    # Secondary row content: additional details
    tag = secondary_row.find_all('div', class_='tw-inline-flex')
    tag_texts = [t.get_text(strip=True) for t in tag]
    # Extract term, location, grades
    term = tag_texts[1] if len(tag_texts) > 1 else None
    location = tag_texts[2] if len(tag_texts) > 2 else None
    grades = " ".join(tag_texts[3:]) if len(tag_texts) > 3 else ""
    # Extract GPA and GRE using regex
    gpa = regex_extract(r'GPA\s*([\d\.]+)', grades)
    gre = regex_extract(r'GRE\s*([\d/]+)', grades)
    # Extract comments from the optional row
    comment = comment_row.find('p').get_text(strip=True) if comment_row else None
    # Return cleaned data as a dictionary
    return{
        'university': university,
        'program': program_name,
        'program_type': program_type,
        'date_added': date_added,
        'status': status,
        'entry_url': entry_url,
        'term': term,
        'location': location,
        'gpa': gpa,
        'gre': gre,
        'comments': comment
    }
# Iteratively scrape pages until target number of entries is reached
def scrape_page():
    # List to hold all scraped results(dictionaries)
    reults = []
    # Start from page 1
    page = 1 
    while len(reults) < target:
        # Construct URL for the current page
        url = f'{base_url}{page}'
        # Get HTML content
        html_response = get_html(url)
        # Parse HTML using BeautifulSoup
        soup = BeautifulSoup(html_response, 'html.parser')
        # Locate the table body containing entries
        table_body = soup.find('tbody')
        rows = table_body.find_all('tr', recursive=False)
        # i = tracker for current row in the page
        i = 0 
        while i < len(rows):
            # Check if the row has 5 columns (main entry row)
            if len(rows[i].find_all('td')) == 5:
                main_row = rows[i]
                # Secondary row and optional comment row if exist
                secondary_row = rows[i+1] if i + 1 < len(rows) else None
                comment_row = rows[i+2] if i + 2 < len(rows) and rows[i+2].find('p') else None
                # Clean and extract data
                entry = clean_data(main_row, secondary_row, comment_row)
                reults.append(entry)
                # Increment i based on presence of comment row
                i += 3 if comment_row else 2
            else: # Skip rows that do not match expected format
                i += 1
        # Move to the next page
        page += 1
    return reults

def save_to_db(data_list):
    """Inserts scraped data directly into PostgreSQL."""
    conn_info = "dbname=postgres user=harryma"
    with psycopg.connect(conn_info) as conn:
        with conn.cursor() as cur:
            print(f"Connecting to DB to insert {len(data_list)} records...")
            
            # We use ON CONFLICT DO NOTHING so that clicking 'Pull Data' 
            # twice doesn't cause errors or duplicate rows.
            query = """
                INSERT INTO applicants (
                    program, comments, date_added, url, status, term, 
                    us_or_international, gpa, gre, degree
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (url) DO NOTHING;
            """
            
            for entry in data_list:
                # Mapping scraper dictionary to DB columns
                # Note: We combine university + program name for the DB 'program' column
                prog_full = f"{entry['university']} - {entry['program']}"
                
                values = (
                    prog_full,
                    entry['comments'],
                    entry['date_added'],
                    entry['entry_url'],
                    entry['status'],
                    entry['term'],
                    entry['location'],
                    float(entry['gpa']) if entry['gpa'] else None,
                    float(entry['gre']) if entry['gre'] else None,
                    entry['program_type']
                )
                cur.execute(query, values)
            
            conn.commit()

# Main execution
if __name__ == "__main__":
    results = scrape_page()
    save_data(results, output_file)
    save_to_db(results)
