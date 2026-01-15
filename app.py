from flask import Flask, render_template, request, redirect, url_for, session
import json
import os
from datetime import datetime
import psycopg2
from psycopg2 import extras
import uuid
import random
from dotenv import load_dotenv
from collections import deque

# Load environment variables from .env file
load_dotenv('credentials.env')
from pydoc import render_doc

from flask import Flask, redirect, render_template, request, url_for, make_response

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'developmentsupersecretkey')

# Database connection
def get_db_connection():
    # Supports both a full DATABASE_URL or individual components
    db_url = os.environ.get('DATABASE_URL')
    if db_url:
        return psycopg2.connect(db_url)
    
    return psycopg2.connect(
        dbname=os.environ.get('DB_NAME', 'hoppera2'),
        user=os.environ.get('DB_USER', 'hoppera2'),
        password=os.environ.get('DB_PASS', 'supersecretpassword'),
        host=os.environ.get('DB_HOST', 'localhost'),
    )

def init_db():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        # Create participants table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS participants (
                participant_id TEXT PRIMARY KEY,
                name TEXT,
                prompted BOOLEAN,
                consent BOOLEAN,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        # Create wide responses table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS responses (
                participant_id TEXT PRIMARY KEY REFERENCES participants(participant_id),
                task1_id TEXT,
                task1_r1 TEXT,
                task1_r2 TEXT,
                task1_r3 TEXT,
                task2_id TEXT,
                task2_r1 TEXT,
                task2_r2 TEXT,
                task2_r3 TEXT,
                task3_id TEXT,
                task3_r1 TEXT,
                task3_r2 TEXT,
                task3_r3 TEXT,
                task4_id TEXT,
                task4_r1 TEXT,
                task4_r2 TEXT,
                task4_r3 TEXT,
                expert_id INT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Database initialization failed: {e}")

# Initialize DB on start
init_db()

@app.route("/")
def index():
    return render_template("homepage.html")

@app.route("/homepage_final")
def homepage_final():
    return render_template("homepage_final_thing.html")

@app.route("/form_prompted")
def form_p():
    return render_template("form_prompted.html")

@app.route("/form_unprompted")
def form_u():
    return render_template("form_unprompted.html")

@app.route('/form_gateway')
def form_gateway():
    if session.get('prompted'):
        return redirect(url_for('form_p'))
    else:
        return redirect(url_for('form_u'))

@app.route('/tasks/<task_id>')
def show_task(task_id):
    return render_template(f'tasks/task{task_id}.html')

@app.route('/start_experiment')
def start_experiment():
    if 'task_order' not in session:
        return redirect(url_for('consent_form'))
    
    # Rotate task order
    d = deque(session['task_order'])
    d.rotate(random.randint(0, 3))
    session['task_order'] = list(d)
    
    # current_task_index must be an integer index into the task_order list (0-based).
    # Previously this was incorrectly set to a task id string which caused list indexing
    # with a string later in `submit()` and triggered:
    # "TypeError: list indices must be integers or slices, not str."
    session['current_task_index'] = 0
    
    session['all_responses'] = {}
    first_task = session['task_order'][0]
    return redirect(url_for('show_task', task_id=first_task))

@app.route("/purgatory")
def purgatory():
    return render_template("purgatory.html")

@app.route("/begin")
def begin():
    return render_template("begin_experiment.html")

@app.route("/consent_form")
def consent_form():
    return render_template("consent_form.html")

@app.route("/consent_declined")
def consent_declined():
    return render_template("consent_declined.html")

@app.route("/consent_success")
def consent_success():
    return render_template("consent_success.html")

@app.route("/submit", methods=["POST"])
def submit():
    participant_id = session.get('participant_id')
    task_order = session.get('task_order')
    current_index = session.get('current_task_index', 0)
    all_responses = session.get('all_responses', {})
    
    if not participant_id or not task_order:
        return redirect(url_for('index'))

    task_id = task_order[current_index]
    
    # Collect form data for current task
    if session.get('prompted'):
        current_data = {
            'r1': request.form.get('goal', ''),
            'r2': request.form.get('steps_taken', ''),
            'r3': request.form.get('cause_hypothesis', '')
        }
    else:
        current_data = {
            'r1': request.form.get('problem_description', ''),
            'r2': '',
            'r3': ''
        }
    
    # Buffer in session
    # We use the task_id itself as the key to ensure Task 2 always goes to Task 2 columns
    task_num = int(task_id.replace('task', ''))
    all_responses[str(task_num)] = {
        'id': task_num,
        'data': current_data
    }
    session['all_responses'] = all_responses
    
    # Increment task index
    session['current_task_index'] = current_index + 1
    
    if session['current_task_index'] < len(task_order):
        next_task = task_order[session['current_task_index']]
        return render_template('success_intermediate.html', next_task=next_task)
    else:
        # Final task complete, insert entire row
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            
            # Prepare query with all columns
            query = """
                INSERT INTO responses (
                    participant_id, 
                    task1_id, task1_r1, task1_r2, task1_r3,
                    task2_id, task2_r1, task2_r2, task2_r3,
                    task3_id, task3_r1, task3_r2, task3_r3,
                    task4_id, task4_r1, task4_r2, task4_r3,
                    expert_id
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            data_tuple = (participant_id,)
            for i in range(1, 5):
                t_data = all_responses.get(str(i), {})
                data_tuple += (
                    t_data.get('id', i), # task ID (1, 2, 3, or 4)
                    t_data.get('data', {}).get('r1', ''),
                    t_data.get('data', {}).get('r2', ''),
                    t_data.get('data', {}).get('r3', '')
                )
            data_tuple += (session.get('expert_id', -1),) # expert_id (default -1)
            
            cur.execute(query, data_tuple)
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            print(f"Error saving final responses: {e}")
            
        return render_template('success.html')

@app.route("/submit_consent_form", methods=["POST"])
def consent_data():
    name = request.form.get('name')
    preferences = request.form.getlist('preferences')
    consent = 'Consent' in preferences

    participant_id = None
    prompted = random.choice([True, False])
    
    # Set initial task order
    tasks = ['task1', 'task2', 'task3', 'task4']
    
    # Save to DB and generate a unique 3-digit ID
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        while True:
            candidate_id = random.randint(0, 999)
            # Check if this ID already exists
            cur.execute("SELECT 1 FROM participants WHERE participant_id = %s", (candidate_id,))
            if not cur.fetchone():
                participant_id = candidate_id
                break
        
        cur.execute(
            "INSERT INTO participants (participant_id, name, prompted, consent) VALUES (%s, %s, %s, %s)",
            (participant_id, name, prompted, consent)
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error saving participant: {e}")
        return "Internal Server Error", 500

    session['participant_id'] = participant_id
    session['prompted'] = prompted
    session['task_order'] = tasks
    session['consent'] = consent
    return render_template('consent_success.html')


@app.route("/next_task")
def next_task():
    current_task = int(request.cookies.get("currentTask", "1"))
    next_task = current_task + 1
    if next_task > 4:
        return render_template("thankyou.html")
    resp = make_response(render_template("tasks/task" + str(next_task) + ".html"))
    resp.set_cookie("currentTask", str(next_task))
    return resp


@app.route("/thankyou")
def thankyou():
    return render_template("thankyou.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5132)
