'''
This module handles database queries and provides 
analysis based on applicant data entries 
'''
def get_fall2026_count(cur):
    '''# Q1 - Fall 2026 Count Function'''
    cur.execute("SELECT COUNT(*) FROM applicants WHERE term ILIKE '%Fall 2026%';")
    return cur.fetchone()[0]

def get_intl_percentage(cur):
    '''Q2 - International Percentage Function'''
    cur.execute("""
        SELECT ROUND((COUNT(*) FILTER (WHERE us_or_international = 'International')::numeric / 
        NULLIF(COUNT(*), 0)::numeric) * 100, 2) FROM applicants;
    """)
    return cur.fetchone()[0]


def get_avg_metrics(cur):
    '''Q3 - Average Grade Metrics Function'''
    cur.execute("""
        SELECT 
            ROUND(AVG(gpa)::numeric, 2), 
            ROUND(AVG(gre)::numeric, 2), 
            ROUND(AVG(gre_v)::numeric, 2), 
            ROUND(AVG(gre_aw)::numeric, 2) 
        FROM applicants;
    """)
    return cur.fetchone()

def get_american_gpa_2026(cur):
    '''Q4 - Average GPA for American Applicants Fall 2026 Function'''
    cur.execute("""
        SELECT ROUND(AVG(gpa)::numeric, 2) FROM applicants 
        WHERE us_or_international = 'American' AND term ILIKE '%Fall 2026%';
    """)
    return cur.fetchone()[0]


def get_fall2025_acc_rate(cur):
    '''Q5 - Acceptance Rate for Fall 2025 Function'''
    cur.execute("""
        SELECT ROUND((COUNT(*) FILTER (WHERE status = 'Accepted' AND term ILIKE '%Fall 2025%')::numeric / 
        NULLIF(COUNT(*) FILTER (WHERE term ILIKE '%Fall 2025%'), 0)::numeric) * 100, 2) FROM applicants;
    """)
    return cur.fetchone()[0]

def get_gpa_2026_acceptances(cur):
    '''# Q6 - GPA of Accepted Applicants Fall 2026 Function'''
    cur.execute("""
        SELECT ROUND(AVG(gpa)::numeric, 2) FROM applicants 
        WHERE term ILIKE '%Fall 2026%' AND status = 'Accepted';
    """)
    return cur.fetchone()[0]

def get_jhu_cs_masters(cur):
    '''# Q7 - JHU MS CS Applicants Function'''
    cur.execute("""
        SELECT COUNT(*) FROM applicants 
        WHERE program ILIKE '%Johns Hopkins%' AND degree ILIKE '%MS%' AND program ILIKE '%Computer Science%';
    """)
    return cur.fetchone()[0]

def get_elite_phd(cur):
    '''# Q8 - Elite Schools PhD Programs (Raw) Function'''
    cur.execute("""
        SELECT COUNT(*) FROM applicants 
        WHERE term ILIKE '%2026%' AND status = 'Accepted' AND degree ILIKE '%PhD%' 
        AND program ILIKE '%Computer Science%'
        AND (program ILIKE '%Georgetown%' OR program ILIKE '%MIT%' 
             OR program ILIKE '%Stanford%' OR program ILIKE '%Carnegie Mellon%');
    """)
    return cur.fetchone()[0]

def get_elite_phd_llm(cur):
    '''# Q9 - Elite Schools PhD Programs (LLM-Generated) Function'''
    cur.execute("""
        SELECT COUNT(*) FROM applicants 
        WHERE term ILIKE '%2026%' AND status = 'Accepted' AND degree ILIKE '%PhD%' 
        AND llm_generated_program ILIKE '%Computer Science%'
        AND (llm_generated_university ILIKE '%Georgetown%' OR llm_generated_university ILIKE '%MIT%' 
             OR llm_generated_university ILIKE '%Stanford%' OR llm_generated_university ILIKE '%Carnegie Mellon%');
    """)
    return cur.fetchone()[0]

# ADDING BONUS QUERIES BELOW

def get_total_count(cur):
    '''# Bonus1 - Total Applicants Function'''
    query = "SELECT COUNT(*) FROM applicants;"
    cur.execute(query)
    result = cur.fetchone()
    return result[0] if result else 0
def get_financial_aid_count(cur):
    '''# Bonus2 - Count of Mentions of 'Financial Aid' in Comments Function'''
    cur.execute("SELECT COUNT(*) FROM applicants WHERE comments ILIKE '%financial aid%';")
    return cur.fetchone()[0]
