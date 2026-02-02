Name: Harry Ma (hm41)

Module Info: Module 2 - Web Scrapping (Due: 02/01/26 11:59PM ET)

Approach: 
Initial Investigation & Ethics First, thegradcafe.com was investigated to see if web scraping is allowed. This was done through checking the thegradcafe.com/robots.txt. After verifying web scraping was allowed, the data page was located on https://www.thegradcafe.com/survey/index.php?page=, 
where each page contained 20 data entries. Setting this as the base URL allows the script to iterate through the survey results by appending page numbers dynamically. The output file was set to applicant_data.json and the target was set to 50,000 data points to ensure a robust dataset for analysis.
Request Configuration A header was added to the request to mimic a real browser (User-Agent). This helps avoid raising any security flags or being blocked by anti-bot filters when scraping large volumes of data. get_html() was the standard function for reading in data from the URL. A try/except block 
specifically catching urllib.error.HTTPError was used to prevent the code from crashing when common network errors (404/403/500/etc) were reached, allowing the scraper to skip a problematic page and continue.
Data Extraction Utilities regex_extract() was set up to pull GRE and GPA data from raw text strings since they followed a similar pattern. By using capturing groups like r'GPA\s*([\d\.]+)', the utility can ignore text labels and isolate only the numerical values regardless of how much whitespace the user entered.
Row Grouping & Sorting Logic process_row() contained the primary sorting and extraction logic. After inspecting the HTML elements on Grad Cafe, it showed data for each person scattered across multiple <tr> (table row) tags. This was identified as 'row grouping'.
After analysis, the row structure was decoded as follows:
Main Row: Contained 5 <td> (table data) columns holding the University name, Program name, Degree type (extracted via nested <span> tags), Date Added, Decision Status, and the entry's specific URL.
Secondary Row: Contained tags inside div elements representing the Term, Location (American/International), and grades/test scores.
Optional Third Row: Contained the comments in a <p> tag, which only existed if the applicant provided them.
The application finds each specific datapoint within these tags and saves each applicant's data into a structured dictionary.
Scraping Orchestration scrape_pages() contained the main logic of the web scraper. The scraper uses a while loop that continues to run until the target count (50,000) is met or exceeded. All data of interest was contained within the <tbody> block of the results table.
An 'i' counter was used as a pointer to track the current applicant's starting row. Because the number of rows per applicant varies, the pointer moves dynamically:
If comments exist: i + 3
If no comments exist: i + 2
The start of a new applicant was determined by checking if len(<td>) == 5, since the first row of a group always has exactly five columns. The script calls process_row() for each valid group and appends the resulting dictionaries into a master list.
Data Persistence save_data() is the standard function for writing the master list into an output file. It uses json.dump with indent=4 to ensure the resulting JSON is human-readable and ensure_ascii=False to properly preserve non-English characters in university names.

Known Bugs: 
Integration Issues: clean.py does not currently call app.py as a module. The provided JSON output file was built by running the command line interface: python app.py --file applicant_data.json > out.json.
Model Accuracy: The LLM does not provide the best outputs for highly specific academic program names and occasionally struggles to handle typos or non-standard abbreviations correctly.
I noticed sone typos in the original data that the LLM did not catch, especially when 'Graduate School of X' was mentioned, or 'GS'derivatives. 
LLM Latency: clean.py does not work as intended for large datasets because the local LLM takes too long to compile and process 50,000 rows. On consumer hardware, the inference time per row makes processing the full dataset impractical.
