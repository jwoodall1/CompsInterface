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

@app.route('/tasks/task2')
def task2():
    return render_template('tasks/task2.html')

@app.route('/tasks/task3')
def task3():
    return render_template('tasks/task3.html')

@app.route('/tasks/task4')
def task4():
    return render_template('tasks/task4.html')


@app.route('/purgatory')
def purgatory():
    return render_template('purgatory.html')


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

@app.route('/submit_contact_form', methods = ['Post'])
def contact_data():
    preferences = request.form.getlist('preferences')


    submission = {
        'timestamp': datetime.now().isoformat(),
        'form_type': 'consent',
        'preferences': preferences


    }

    filename = f"{DATA_DIR}/submission_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump(submission, f, indent=2)

    return render_template('Homepage.html')



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=42069)