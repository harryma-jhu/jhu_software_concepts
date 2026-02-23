'''
This is the main application where the frontend
is loaded and launched for the user to interact with
'''
# Import necessary libraries and modules
# import subprocess
from flask import Flask, jsonify, render_template, redirect, Blueprint
import psycopg
import query_data
from scrape import scrape_page, save_to_db

#app = Flask(__name__)
bp = Blueprint('app', __name__)
# Connection info
CONN_INFO = "host=localhost dbname=postgres user=harryma"
# Secret key needed for Flask Flash messages
#bp.secret_key = 'secret'
# Global is-busy variable to track state
"""
setup
"""
IS_BUSY = False

@bp.route('/')
def index():
    '''Main Page'''
    with psycopg.connect(CONN_INFO) as conn:
        with conn.cursor() as cur:
            # Aggregate all function results into one dictionary
            results = {
                # Q1-Q9
                'q1': query_data.get_fall2026_count(cur),
                'q2': query_data.get_intl_percentage(cur),
                'q3': query_data.get_avg_metrics(cur),
                'q4': query_data.get_american_gpa_2026(cur),
                'q5': query_data.get_fall2025_acc_rate(cur),
                'q6': query_data.get_gpa_2026_acceptances(cur),
                'q7': query_data.get_jhu_cs_masters(cur),
                'q8': query_data.get_elite_phd(cur),
                'q9': query_data.get_elite_phd_llm(cur),
                # Bonus Questions
                'b1': query_data.get_total_count(cur),
                'b2': query_data.get_financial_aid_count(cur)
            }
    return render_template('index.html', results=results)

# Function that pulls new data from scraper.py and launches it in the background
# Triggered by the 'Pull Data Button' on the dashboard
@bp.route('/pull_data', methods=['POST'])
def pull_data():
    ''' Function that pulls new data from scraper.py and launches it in the background
        Triggered by the 'Pull Data Button' on the dashboard'''
    global IS_BUSY
    if IS_BUSY:
        return jsonify({'busy':True}),409
    IS_BUSY = True
    try:
        # subprocess.Popen(["python3", "src/scrape.py"]) # Modified to Module 4 Path
        # REVISIT: Subprocesses does not hit testing - shouldve kept as is and
        # Extended coverage in extras-test
        results = scrape_page()
        save_to_db(results)
        return jsonify({"ok": True}), 200
        # Deleted Flash messages
    # Updating Exeptions to address generalized exception msg
    # except Exception as e:
        # return jsonify({"ok": False}), 500
    except (RuntimeError, ConnectionError) as error:
        print(f"Scraping failed: {error}")
        return jsonify({"ok": False, "error": "Scraping error"}), 500
    finally: # Reset busy state
        IS_BUSY = False

# Function to update the analysis dashboard with the latest database entries
# Triggered by the 'Update Analysis' button on the dashboard
@bp.route('/update_analysis', methods=['POST'])
def update_analysis():
    '''
    Function to update the analysis dashboard with the latest database entries
    Triggered by the 'Update Analysis' button on the dashboard
    '''
    global IS_BUSY
    if IS_BUSY:
        return jsonify({'busy':True}),409
    # Keeps user on homepage
    return redirect('/')


if __name__ == '__main__':
    # Running on localhost:8080 with debug mode on for easier development
    app = Flask(__name__)
    app.register_blueprint(bp)
    app.run(debug=True,port=8080)
