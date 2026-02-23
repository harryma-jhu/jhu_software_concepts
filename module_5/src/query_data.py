'''
This module handles database queries and provides 
analysis based on applicant data entries 
Safe limit is set to 1 for each query
'''
from psycopg import sql 
def get_fall2026_count(cur):
    '''# Q1 - Fall 2026 Count Function'''
    term_pattern = '%Fall 2026%'

    query = sql.SQL("SELECT COUNT(*) FROM applicants WHERE term ILIKE %s LIMIT 1;")
    cur.execute(query, (term_pattern,))
    return cur.fetchone()[0]

def get_intl_percentage(cur):
    '''Q2 - International Percentage Function'''
    query = sql.SQL("""
        SELECT ROUND((COUNT(*) FILTER (WHERE us_or_international = %s)::numeric / 
        NULLIF(COUNT(*), 0)::numeric) * 100, 2) FROM applicants LIMIT 1;
    """)
    cur.execute(query, ("International",))
    return cur.fetchone()[0]


def get_avg_metrics(cur):
    '''Q3 - Average Grade Metrics Function'''
    query = sql.SQL("""
        SELECT 
            ROUND(AVG(gpa)::numeric, 2), 
            ROUND(AVG(gre)::numeric, 2), 
            ROUND(AVG(gre_v)::numeric, 2), 
            ROUND(AVG(gre_aw)::numeric, 2) 
        FROM applicants LIMIT 1;
    """)
    cur.execute(query)
    return cur.fetchone()

def get_american_gpa_2026(cur):
    '''Q4 - Average GPA for American Applicants Fall 2026 Function'''
    query = sql.SQL("""
        SELECT ROUND(AVG(gpa)::numeric, 2) FROM applicants 
        WHERE us_or_international = %s AND term ILIKE %s LIMIT 1;
    """)
    cur.execute(query, ("American", "%Fall 2026%"))
    return cur.fetchone()[0]

def get_fall2025_acc_rate(cur):
    '''Q5 - Acceptance Rate for Fall 2025 Function'''
    query = sql.SQL("""
        SELECT ROUND((COUNT(*) FILTER (WHERE status = %s AND term ILIKE %s)::numeric / 
        NULLIF(COUNT(*) FILTER (WHERE term ILIKE %s), 0)::numeric) * 100, 2) FROM applicants LIMIT 1;
    """)
    cur.execute(query, ("Accepted", "%Fall 2025%", "%Fall 2025%"))
    return cur.fetchone()[0]

def get_gpa_2026_acceptances(cur):
    '''# Q6 - GPA of Accepted Applicants Fall 2026 Function'''
    query = sql.SQL("""
        SELECT ROUND(AVG(gpa)::numeric, 2) FROM applicants 
        WHERE term ILIKE %s AND status = %s LIMIT 1;
    """)
    cur.execute(query, ("%Fall 2026%", "Accepted"))
    return cur.fetchone()[0]

def get_jhu_cs_masters(cur):
    '''# Q7 - JHU MS CS Applicants Function'''
    query = sql.SQL("""
        SELECT COUNT(*) FROM applicants 
        WHERE program ILIKE %s AND degree ILIKE %s AND program ILIKE %s LIMIT 1;
    """)
    cur.execute(query, ("%Johns Hopkins%", "%MS%", "%Computer Science%"))
    return cur.fetchone()[0]

def get_elite_phd(cur):
    '''# Q8 - Elite Schools PhD Programs (Raw) Function'''
    query = sql.SQL("""
        SELECT COUNT(*) FROM applicants 
        WHERE term ILIKE %s AND status = %s AND degree ILIKE %s 
        AND program ILIKE %s
        AND (program ILIKE ANY(%s)) LIMIT 1;
    """)
    schools = ['%Georgetown%', '%MIT%', '%Stanford%', '%Carnegie Mellon%']
    cur.execute(query, ("%2026%", "Accepted", "%PhD%", "%Computer Science%", schools))
    return cur.fetchone()[0]

def get_elite_phd_llm(cur):
    '''# Q9 - Elite Schools PhD Programs (LLM-Generated) Function'''
    query = sql.SQL("""
        SELECT COUNT(*) FROM applicants 
        WHERE term ILIKE %s AND status = %s AND degree ILIKE %s 
        AND llm_generated_program ILIKE %s
        AND (llm_generated_university ILIKE ANY(%s)) LIMIT 1;
    """)
    schools = ['%Georgetown%', '%MIT%', '%Stanford%', '%Carnegie Mellon%']
    cur.execute(query, ("%2026%", "Accepted", "%PhD%", "%Computer Science%", schools))
    return cur.fetchone()[0]

# ADDING BONUS QUERIES BELOW

def get_total_count(cur):
    '''# Bonus1 - Total Applicants Function'''
    query = sql.SQL("SELECT COUNT(*) FROM applicants LIMIT 1;")
    cur.execute(query)
    result = cur.fetchone()
    return result[0] if result else 0

def get_financial_aid_count(cur):
    '''# Bonus2 - Count of Mentions of 'Financial Aid' in Comments Function'''
    query = sql.SQL("SELECT COUNT(*) FROM applicants WHERE comments ILIKE %s LIMIT 1;")
    cur.execute(query, ("%financial aid%",))
    return cur.fetchone()[0]
