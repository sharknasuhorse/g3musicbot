from flask import Flask, request, redirect, render_template
from werkzeug.utils import secure_filename
from pydub import AudioSegment
import json
import os

# set -x FLASK_APP src/main.py
# set -x FLASK_EsNV development
# flask run


class G3uploader():

    app = Flask(__name__)
    @app.route('/')
    def hello_world():
        return 'Hello, World!'

    @app.route('/upload', methods=['GET', 'POST'])
    def send():
        if request.method == 'POST':
            f = request.files['uploadFile']
            filename = secure_filename(f.filename)
            musicbot_dir = ''
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

        return render_template('upload.html')

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


# if __name__ == '__main__':
#    web = G3uploader()
#    # debug_json()
#    web.run(debug=True, host='0.0.0.0')
