from flask import Flask, render_template, request, redirect, url_for
import json
from datetime import datetime
import os

app = Flask(__name__)

# create data directory if there isn't one
DATA_DIR = 'data'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

@app.route('/')
def index():
    return render_template('homepage.html')

@app.route('/form_prompted')
def form_p():
    return render_template('form_prompted.html')

@app.route('/form_unprompted')
def form_u():
    return render_template('form_unprompted.html')

@app.route('/tasks/task1')
def task1():
    return render_template('tasks/task1.html')

@app.route('/taskmanagement.js')
def task_management_js():
    return app.send_static_file('taskmanagement.js')


@app.route('/submit', methods=['POST'])
def submit():
    # get form data
    goal = request.form.get('goal', '')
    steps_taken = request.form.get('steps_taken', '')
    cause_hypothesis = request.form.get('cause_hypothesis', '')
    
    # make submission record
    submission = {
        'timestamp': datetime.now().isoformat(),
        'goal': goal,
        'steps_taken': steps_taken,
        'cause_hypothesis': cause_hypothesis
    }
    
    # save to json
    filename = f"{DATA_DIR}/submission_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump(submission, f, indent=2)
    
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=42069)