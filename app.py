from flask import Flask, request, send_file, session, render_template
import os
import json

app = Flask(__name__)
app.secret_key = "asdfasfdasfdsafasddfsadfasdfsadfdas"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
base = os.getcwd()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/questionnaire')
def questionnaire():
    return render_template('questionnaire.html')
@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run()