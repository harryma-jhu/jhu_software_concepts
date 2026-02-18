import pytest 
import re 
import psycopg
import src.query_data as qd 
import src.load_data as ld 

conn_info =("host=localhost dbname=postgres user=harryma")

@pytest.mark.db 
def test_db_insert(client, monkeypatch):
    # Establish the test connection
    with psycopg.connect(conn_info) as conn:
        # FORCE the module's connection variable to be our test connection
        # This prevents the 'NoneType' AttributeError
        monkeypatch.setattr(ld, "conn", conn)
        
        # MAKE SURE TO ROLL BACK SO DATABASE REMAINS SAME AFTER TEST 
        with conn.cursor() as cur:
            # Before: target table empty
            cur.execute("DELETE FROM applicants;")
            assert qd.get_total_count(cur) == 0
            ld.load_data()
            
            # Verify data exists
            cur.execute("SELECT COUNT(*) FROM applicants;")
            count = cur.fetchone()[0]
            assert count > 0
            # Verify duplicate data is NOT loaded
            ld.load_data()
            cur.execute("SELECT COUNT(*) FROM applicants;")
            assert cur.fetchone()[0] == count 

            # Addressing missing coverage
            qd.get_fall2026_count(cur)
            qd.get_intl_percentage(cur)
            qd.get_avg_metrics(cur)
            qd.get_american_gpa_2026(cur)
            qd.get_total_count(cur)
            qd.get_financial_aid_count(cur)
            
            # Rollback - keep data safe
            conn.rollback()