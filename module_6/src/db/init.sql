-- 1. Create Applicants first
CREATE TABLE IF NOT EXISTS applicants (
    p_id SERIAL PRIMARY KEY,
    program TEXT,
    university TEXT,
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
);

-- 2. Create watermarks
CREATE TABLE IF NOT EXISTS ingestion_watermarks (
    source      TEXT PRIMARY KEY,
    last_seen   TEXT,
    updated_at  TIMESTAMPTZ DEFAULT now()
);

-- Materialized View for consumer.py
CREATE MATERIALIZED VIEW IF NOT EXISTS application_summaries AS 
SELECT 
    COUNT(*) FILTER (WHERE term ILIKE '%Fall 2026%') as q1,
    ROUND((COUNT(*) FILTER (WHERE us_or_international = 'International')::numeric / NULLIF(COUNT(*), 0)) * 100, 2) as q2,
    COALESCE(ROUND(AVG(gpa)::numeric, 2), 0) as q3_gpa,
    COALESCE(ROUND(AVG(gre)::numeric, 2), 0) as q3_gre,
    COALESCE(ROUND(AVG(gre_v)::numeric, 2), 0) as q3_v,
    COALESCE(ROUND(AVG(gre_aw)::numeric, 2), 0) as q3_aw,
    ROUND(AVG(gpa) FILTER (WHERE us_or_international = 'American' AND term ILIKE '%Fall 2026%')::numeric, 2) as q4,
    ROUND((COUNT(*) FILTER (WHERE status = 'Accepted' AND term ILIKE '%Fall 2025%')::numeric / NULLIF(COUNT(*) FILTER (WHERE term ILIKE '%Fall 2025%'), 0)) * 100, 2) as q5,
    ROUND(AVG(gpa) FILTER (WHERE term ILIKE '%Fall 2026%' AND status = 'Accepted')::numeric, 2) as q6,
    COUNT(*) FILTER (WHERE program ILIKE '%Johns Hopkins%' AND degree ILIKE '%MS%' AND program ILIKE '%Computer Science%') as q7,
    COUNT(*) FILTER (WHERE term ILIKE '%2026%' AND status = 'Accepted' AND degree ILIKE '%PhD%' AND program ILIKE '%Computer Science%' AND (university ILIKE ANY(ARRAY['%Georgetown%', '%MIT%', '%Stanford%', '%Carnegie Mellon%']))) as q8,
    COUNT(*) FILTER (WHERE term ILIKE '%2026%' AND status = 'Accepted' AND degree ILIKE '%PhD%' AND llm_generated_program ILIKE '%Computer Science%' AND (llm_generated_university ILIKE ANY(ARRAY['%Georgetown%', '%MIT%', '%Stanford%', '%Carnegie Mellon%']))) as q9,
    COUNT(*) as b1,
    COUNT(*) FILTER (WHERE comments ILIKE '%financial aid%') as b2
FROM applicants;

-- 3. Permissions
GRANT ALL PRIVILEGES ON TABLE applicants TO postgres;
GRANT ALL PRIVILEGES ON TABLE ingestion_watermarks TO postgres;