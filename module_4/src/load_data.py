import psycopg
import json 

conn = None

def get_connection():
    global conn
    # Verify connection 
    if conn is None:
        conn = psycopg.connect("host=localhost dbname=postgres user=harryma")
    return conn

def create_table():
    '''Create SQL table in localhost'''
    connection = get_connection()
    # Orginal framework
    with connection.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS applicants (
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
        """)
    connection.commit()

# Read in json data file and insert into database, 
# Ignoring duplicates based on unique url constraint
def load_data():
    '''# Read in json data file and insert into database, 
     Ignoring duplicates based on unique url constraint'''
    connection = get_connection()
    with connection.cursor() as cur:
        # Update to current path
        with open('src/llm_extend_applicant_data_liv.json', 'r') as f:
            data = json.load(f)
            for record in data:
                # Needed to clean up to align with assignment requirements 
                # (University and Department)
                prgm_name = ' '.join(record.get('program').split(' ')[:-1])
                prgm = f'{record.get("university")} {prgm_name}'
                # SQL insert
                cur.execute("""
                    INSERT INTO applicants (
                        program, comments, date_added, url, status, term, 
                        us_or_international, gpa, gre, gre_v, gre_aw, 
                        degree, llm_generated_program, llm_generated_university
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
                    ON CONFLICT (url) DO NOTHING
                """, (
                    prgm, record.get('comments'), record.get('date_added'),
                    record.get('overview_url'), record.get('applicant_status'),
                    record.get('start_term'), record.get('citizenship'),
                    float(record['gpa']) if record.get('gpa') else None,
                    float(record['gre_general']) if record.get('gre_general') else None,
                    float(record['gre_verbal']) if record.get('gre_verbal') else None,
                    float(record['gre_aw']) if record.get('gre_aw') else None,
                    record.get('degree_level'), record.get('llm-generated-program'),
                    record.get('llm-generated-university')
                ))
    connection.commit()