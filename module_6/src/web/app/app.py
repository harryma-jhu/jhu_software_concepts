'''
This is the main application where the frontend
is loaded and launched for the user to interact with
'''
# Import necessary libraries and modules
# import subprocess
import os 
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, Blueprint, current_app
import psycopg
# removed since worker handles this now 
# from module_6.src.worker.etl.scrape import scrape_page, save_to_db
from src.web.publisher import publish_task

load_dotenv()

#app = Flask(__name__)
bp = Blueprint('app', __name__)
# Connection info

def get_db_connection_info():
    url = os.getenv('DATABASE_URL')
    if url:
        return psycopg.connect(url)
    return psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS")
    )
# Global is-busy variable to track state
# Now handled by rabbit
# IS_BUSY = False

@bp.route('/')
def index():
    '''Main Page'''

    with get_db_connection_info() as conn:
        with conn.cursor() as cur:
            # Aggregate all function results into one dictionary
            cur.execute("SELECT * FROM application_summaries LIMIT 1;")
            row = cur.fetchone()
            if row:
                results = {
                    'q1': row[0], 'q2': row[1],
                    'q3': [row[2], row[3], row[4], row[5]],
                    'q4': row[6], 'q5': row[7],
                    'q6': row[8], 'q7': row[9],
                    'q8': row[10], 'q9': row[11],
                    'b1': row[12], 'b2': row[13] # B2 is now here!
                }
            else:
                results = {k: 0 for k in ['q1','q2','q4','q5','q6','q7','q8','q9','b1','b2']}
                results['q3'] = [0,0,0,0]
    return render_template('index.html', results=results)
    

# Function that pulls new data from scraper.py and launches it in the background
# Triggered by the 'Pull Data Button' on the dashboard
@bp.route('/pull_data', methods=['POST'])
def pull_data():
    ''' Function that pulls new data from scraper.py and launches it in the background
        Triggered by the 'Pull Data Button' on the dashboard'''
    #global IS_BUSY
    #if IS_BUSY:
        #return jsonify({'busy':True}),409
    #IS_BUSY = True
    try:
        # subprocess.Popen(["python3", "src/scrape.py"]) # Modified to Module 4 Path
        # REVISIT: Subprocesses does not hit testing - shouldve kept as is and
        # Extended coverage in extras-test
        ''' HISTORY
        results = scrape_page()
        save_to_db(results)
        return jsonify({"ok": True}), 200
        '''
        publish_task('scrape_new_data',payload = {})
        return jsonify({"ok": True, "status": "request queued"}), 202
        # Deleted Flash messages
    # Updating Exeptions to address generalized exception msg
    # except Exception as e:
        # return jsonify({"ok": False}), 500
    # HISTORY
    #except (RuntimeError, ConnectionError) as error:
        #print(f"Scraping failed: {error}")
        #return jsonify({"ok": False, "error": "Scraping error"}), 500
    except Exception as e:
        current_app.logger.exception("Failed to publish scrape_new_data")
        return jsonify({"ok": False, "error": "Queue unavailable"}), 503
    #finally: # Reset busy state
        #IS_BUSY = False

# Function to update the analysis dashboard with the latest database entries
# Triggered by the 'Update Analysis' button on the dashboard
@bp.route('/update_analysis', methods=['POST'])
def update_analysis():
    '''
    Function to update the analysis dashboard with the latest database entries
    Triggered by the 'Update Analysis' button on the dashboard
    '''
    #global IS_BUSY
    #if IS_BUSY:
        #return jsonify({'busy':True}),409
    # Keeps user on homepage
    #return redirect('/')
    try:
        publish_task("recompute_analytics",payload={})
        return jsonify({"ok": True, "status": "recompute queued"}), 202
    except Exception as e:
        return jsonify({"ok": False, "error": "Queue unavailable"}), 503


if __name__ == '__main__':
    # Running on localhost:8080 with debug mode on for easier development
    app = Flask(__name__)
    app.register_blueprint(bp)
    app.run(debug=True,host="0.0.0.0", port=8080)
