from flask import Flask, request, send_file, session, render_template, jsonify, flash
import os
import json
import firebase_admin
import string
import random
import re

app = Flask(__name__)
app.secret_key = "asdfasfdasfdsafasddfsadfasdfsadfdas"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
base = os.getcwd()
f_credential = json.loads(os.environ['GOOGLE_APPLICATION_CREDS'])
f_credentials = firebase_admin.credentials.Certificate(f_credential)
fb = firebase_admin.initialize_app(f_credentials, {'databaseURL': 'https://clovr-26eba-default-rtdb.firebaseio.com/'})
regex_email = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.](\w+[.]?)\w+$"

from collections import defaultdict
form = defaultdict(list)
form["singles"] = ["first", "last", "email", "major", "linkedin", "instagram"]
form["gender"] = ["man", "woman", "nonbinary"]
form["year"] = ["freshman", "sophomore", "junior", "senior"]
form["csinterest[]"] = ["ai", "arc", "bio", "cpsda", "dbms", "educ", "gr", "hci", "osnt", "ps", "sci", "sec"]
form["hobbies[]"] = ["art", "fitness", "outdoor", "lit", "bgames", "vgames", "music", "bandorch", "sports", "netflix", "digitalart", "tiktok", "activism", "movies", "content", "coding", "writing", "fashion"]
form["terms"] = ["on"]
list_items = ["csinterest[]", "hobbies[]"]

from firebase_admin import db as database

current_db_items = {}
for i in database.reference('/users').get().keys():
    current_db_items[i] = 1

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/questionnaire')
def questionnaire():
    return render_template('questionnaire.html')
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/formsubmit', methods=['POST'])
def submit():
    if request.method == 'POST':
        print(list(request.form.keys()))
        print(request.form.getlist('csinterest[]'))

        result, message = validateForm()
        if result == 0:
            vals = {}
            for i in request.form.keys():
                if '[]' not in i:
                    vals[i] = request.form[i]
            vals['csinterest'] = list(set(request.form.getlist('csinterest[]')))
            vals['hobbies'] = list(set(request.form.getlist('hobbies[]')))
            uploadSurveyContent(vals)
            return 'success?'
        else:
            return message
#Takes in a dictionary for vals
def uploadSurveyContent(vals):
    user_key = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(10))
    #Collision key detection
    while user_key in current_db_items:
        user_key = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(10))
    path = '/users/' + user_key
    ref_path = database.reference(path)
    current_db_items[user_key] = 1
    for i in vals:
        value = vals[i]
        key = i
        ref_path.update({key : value})

def validateForm():
    for i in form.keys():
        if i != 'singles' and i not in request.form.keys():
            return (-1, "Missing attribute: " + i)
        else:
            if i=='singles':
                for j in form[i]:
                    if j not in request.form.keys():
                        return -1, "Missing attribute: " + j
                    else:
                        if len(request.form[j]) == 0:
                            return -1, "Cannot have empty value for \"" + j + "\" input"
            elif i in request.form.keys() and request.form[i] in form[i]:
                if i == 'terms':
                    if request.form[i] == "on": continue
                    else:
                        return -1, "You must accept the terms and condition before we can collect your survey"
                elif i in list_items:
                    for k in request.form.getlist(i):
                        if k not in form[i]:
                            return -1, "Invalid value for attribute \"" + i + "\": " + k
                else:
                    if request.form[i] not in form[i]:
                        return -1, "Invalid value for attribute \"" + i + "\": " + request.form[i]
            else:
                return -1, "Unknown form data: " + i

    if not re.search(regex_email, request.form['email']):
        return -1, "Invalid email format"
    return 0, "Valid form"




if __name__ == '__main__':
    app.run(debug=True) #debug=True so that caching doesn't occur