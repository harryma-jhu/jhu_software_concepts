import json
import os 
from dotenv import load_dotenv
import psycopg
from psycopg import sql
 

CONN = None
load_dotenv()
def get_connection():
    global CONN
    # Verify connection 
    if CONN is None:
        CONN = psycopg.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER")
            )
    return CONN

def create_table():
    '''Create SQL table in localhost'''
    connection = get_connection()
    table_name = "applicants"
    
    # Using sql.Identifier to safely handle the table name
    query = sql.SQL("""
        CREATE TABLE IF NOT EXISTS {table} (
            p_id SERIAL PRIMARY KEY,
            program TEXT,
            comments TEXT,
            date_added DATE,
            url TEXT UNIQUE,
            status TEXT,
            term TEXT,
            us_or_international TEXT,
            gpa FLOAT,
            gre FLOAT,
            gre_v FLOAT,
            gre_aw FLOAT,
            degree TEXT,
            llm_generated_program TEXT,
            llm_generated_university TEXT
        )
    """).format(table=sql.Identifier(table_name))

    with connection.cursor() as cur:
        cur.execute(query)
    connection.commit()

# Read in json data file and insert into database, 
# Ignoring duplicates based on unique url constraint
def load_data():
    '''# Read in json data file and insert into database, 
     Ignoring duplicates based on unique url constraint'''
    connection = get_connection()
    with connection.cursor() as cur:
        # Update to current path
        with open('src/llm_extend_applicant_data_liv.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            for record in data:
                # Needed to clean up to align with assignment requirements 
                # (University and Department)
                prgm_name = ' '.join(record.get('program').split(' ')[:-1])
                prgm = f'{record.get("university")} {prgm_name}'
                # SQL insert
                # Could add LIMIT 1 at the end to set max
                insert_stmt = """
                    INSERT INTO applicants (
                        program, comments, date_added, url, status, term, 
                        us_or_international, gpa, gre, gre_v, gre_aw, 
                        degree, llm_generated_program, llm_generated_university
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
                    ON CONFLICT (url) DO NOTHING
                """
                params = (           
                    prgm, record.get('comments'), record.get('date_added'),
                    record.get('overview_url'), record.get('applicant_status'),
                    record.get('start_term'), record.get('citizenship'),
                    float(record['gpa']) if record.get('gpa') else None,
                    float(record['gre_general']) if record.get('gre_general') else None,
                    float(record['gre_verbal']) if record.get('gre_verbal') else None,
                    float(record['gre_aw']) if record.get('gre_aw') else None,
                    record.get('degree_level'), record.get('llm-generated-program'),
                    record.get('llm-generated-university')
                )
                # Limit not needed since its 1 record per insert 
                cur.execute(insert_stmt, params)
    connection.commit()

if __name__ == "__main__":
    create_table()
    load_data()