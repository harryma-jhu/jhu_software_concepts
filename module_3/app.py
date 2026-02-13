# Import necessary libraries and modules
from flask import Flask, render_template, url_for, redirect, flash
import psycopg
import query_data
import subprocess

app = Flask(__name__)
# Connection info 
CONN_INFO = "dbname=postgres user=harryma"
# Secret key needed for Flask Flash messages
app.secret_key = 'secret'

@app.route('/')
def index():
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
@app.route('/pull_data', methods=['POST'])
def pull_data():
    try:
        subprocess.Popen(["python3", "module_3/scrape.py"])
        # Fun popup that allows the user to know that the button worked
        # And scraper is running in the background
        flash("Background Data Pull Started! Check back in a few minutes.")
    except Exception as e:
        flash(f"Error starting scraper: {e}")
    # Keeps user on homepage
    return redirect(url_for('index'))

# Function to update the analysis dashboard with the latest database entries
# Triggered by the 'Update Analysis' button on the dashboard
@app.route('/update_analysis', methods=['POST'])
def update_analysis():
    flash("Analysis Updated with latest database entries!")
    # Keeps user on homepage
    return redirect(url_for('index'))


if __name__ == '__main__':
    # Running on localhost:8080 with debug mode on for easier development 
    app.run(debug=True, port=8080)