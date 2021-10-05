from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

if __name__ == '__main__':
    app.run()


from app import create_app, db
from app.models import *
from flask import Flask

app = create_app()

@app.shell_context_processor
def make_shell_context():

    return {
        'db': db,
        'Users': Users,
        'Artists': artists,
        'Albums': albums,
        'Tracks': tracks,
        'Genres': genres,
        'Media_types': media_types,
        'InvalidToken': InvalidToken
    }


if __name__ == '__main__':
    app.run(debug=True)