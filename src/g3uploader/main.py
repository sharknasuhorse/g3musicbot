from flask import Flask, request, redirect, render_template
from werkzeug.utils import secure_filename

import os

# set -x FLASK_APP src/main.py
# flask run
# set -x FLASK_ENV development


class G3uploader():

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

    def run(self, debug, host):
        self.app.run(debug=True, host=host)
def debug_json():
    with open('queue.json.temp', mode='r', encoding='utf8') as f:
        raw_json = f.read()
    pprint(raw_json)


if __name__ == '__main__':
    web = G3uploader()
    # debug_json()
    web.run(debug=True, host='0.0.0.0')
