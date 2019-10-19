from flask import Flask, request, redirect, render_template, abort
from werkzeug.utils import secure_filename
from pydub import AudioSegment
from flask_login import LoginManager, login_user, login_required, UserMixin, logout_user
from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, SubmitField, validators
from flask_wtf.file import FileField, FileRequired, FileAllowed


import json
import os


# set -x FLASK_APP src/main.py
# set -x FLASK_EsNV development
# flask run

class LoginForm(FlaskForm):
    username = TextField('Username', [validators.DataRequired(), validators.Length(min=4, max=25)])
    password = PasswordField('Password', [validators.DataRequired(), validators.Length(min=6, max=200)])
    submit = SubmitField('Login')

class UploadForm(FlaskForm):
    mp3 = FileField('mp3', validators=[FileRequired(),FileAllowed(['mp3'], 'mp3 only!')])
    submit = SubmitField('Upload')

class User(UserMixin):
    def __init__(self, id, name, password):
        self.id = id
        self.name = name
        self.password = password

#    def get(self):
#        return self.id

users = {
    1: User(1,'admin', os.environ['ADMIN_PASS'])
}

class G3uploader():

    app = Flask(__name__)
    app.secret_key = 'jrnfuiwenfiqniqwnfoiwqjfoieqwjfwiogjqwe'
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return users.get(int(user_id))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if request.method == 'POST':
            if form.validate_on_submit():
                if request.form['username'] == 'admin' and request.form['password'] == os.environ['ADMIN_PASS']:
                    login_user(User('1', 'admin', request.form['password']))
                    return redirect('/upload')
                else:
                    return abort(401)
            else:
                return abort(401)
        else: 
            return render_template('login.html', form=form) 

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        form = LoginForm()
        return render_template('login.html', form=form)

    @app.route('/upload', methods=['GET', 'POST'])
    @login_required
    def send():
        form = UploadForm()
        if request.method == 'POST':
            if form.validate_on_submit():
                f = form.mp3.data
                filename = secure_filename(f.filename)
                musicbot_dir = ''

                if not os.path.isdir(musicbot_dir + 'audio_cache/'):
                    os.makedirs(musicbot_dir + 'audio_cache/')

                dir = musicbot_dir + 'audio_cache/' + filename
                f.save(dir)

                # convert
                song = AudioSegment.from_mp3(
                    dir)
                duration = int('{:.0f}'.format(len(song) / 1000))
                song.export(dir + '.webm', format='webm')

                # output json
                dir = dir + '.webm'
                filename = filename + '.webm'
                entry = URLPlaylistEntry(filename=filename, title=filename,
                                        duration=duration, download_folder=dir, musicbot_dir=musicbot_dir)

                with open('g3uploader/queue.json.temp', mode='r', encoding='utf8') as f:
                    queue_json = json.loads(f.read())

                queue_json['data']['entries']['data']['entries'].append(
                    entry.__json__())

                with open(musicbot_dir + 'data/server_names.txt', mode='r', encoding='utf8') as f:
                    guildid = f.read().split()[0]
                output_json_dir = musicbot_dir + 'data/%s/queue.json' % guildid
                with open(output_json_dir, mode='w', encoding='utf8') as f:
                    f.write(json.dumps(queue_json))

                return redirect(request.url)
        return render_template('upload.html', form=form)

    def run(self, debug, host):
        self.app.run(debug=debug, host=host)

# Musicbot.entry


class URLPlaylistEntry():
    def __init__(self, filename, title, duration, download_folder, musicbot_dir):
        self.filename = filename
        self.title = title
        self.duration = duration
        self.download_folder = download_folder
        self.musicbot_dir = musicbot_dir

    def _enclose_json(self, data):
        return {
            '__class__': self.__class__.__qualname__,
            '__module__': 'musicbot.entry',
            'data': data
        }

    def __json__(self):
        return self._enclose_json({
            'version': 1,
            'url': 'g3uploader',
            'title': self.title,
            'duration': self.duration,
            'downloaded': True,
            'expected_filename': None,
            'filename': 'audio_cache/' + self.filename,
            'full_filename': os.path.abspath(self.musicbot_dir + 'audio_chache/' + self.filename) + self.filename,
            'meta': {
                "author": {
                    "id": 0000,
                    "name": "g3uploader",
                    "type": "Member"
                },
                "channel": {
                    "id": 0000,
                    "name": "g3musicbot",
                    "type": "TextChannel"
                }
            },
            'aoptions': '-vn'
        })

if __name__ == '__main__':
    web = G3uploader()
    web.run(debug=True, host='0.0.0.0')
