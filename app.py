from flask import Flask, request, send_file, session, render_template, jsonify
import os
import json
import firebase_admin
import string
import random

app = Flask(__name__)
app.secret_key = "asdfasfdasfdsafasddfsadfasdfsadfdas"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
base = os.getcwd()
f_credentials = firebase_admin.credentials.Certificate(json.loads(os.environ['GOOGLE_APPLICATION_CREDS']))
fb = firebase_admin.initialize_app(f_credentials)

from firebase_admin import db as database

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/questionnaire')
def questionnaire():
    return render_template('questionnaire.html')
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/formsubmit', methods=['POST'])
def submit():
    if request.method == 'POST':
        print(list(request.form.keys()))
        print(request.form.getlist('csinterest[]'))

        #TODO validation of form before creating vals dictionary

        vals = {}
        for i in request.form.keys():
            if '[]' not in i:
                vals[i] = request.form[i]
        vals['csinterest'] = request.form.getlist('csinterest[]')
        vals['hobbies'] = request.form.getlist('hobbies[]')
        uploadSurveyContent(vals)
        return 'success?'


#Takes in a dictionary for vals
def uploadSurveyContent(vals):
    user_key = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(10))
    path = '/users/' + user_key
    ref_path = database.reference(path)
    for i in vals:
        ref_path.child(i).push(json.dumps(vals[i]))



if __name__ == '__main__':
    app.run(debug=True) #debug=True so that caching doesn't occur