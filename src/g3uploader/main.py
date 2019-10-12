from flask import Flask, request, redirect, render_template
from werkzeug.utils import secure_filename

import os

# set -x FLASK_APP src/main.py
# flask run
# set -x FLASK_ENV development

app = Flask(__name__)
@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/upload', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        f = request.files['uploadFile']
        f.save('./upload_data/' + secure_filename(f.filename))
        app.logger.info('upload file saved')
        return redirect(request.url)

    return render_template('upload.html')
