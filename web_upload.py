from flask import Flask, render_template, redirect, url_for, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FileField
from wtforms.validators import InputRequired
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import secrets
import os
import json
import hashlib

template_dir = os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'templates'))
static_dir = os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'static'))

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.config['SECRET_KEY'] = secrets.token_hex(16)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    def get_id(self):
        return self.id


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def load_users():
    with open('users.json', 'r') as file:
        data = json.load(file)
        return [User(user['id'], user['username'], user['password'])
                for user in data['users']]


users = load_users()


@login_manager.user_loader
def load_user(user_id):
    user = next((user for user in users if user.id == int(user_id)), None)
    return user


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])


class UploadForm(FlaskForm):
    file = FileField('File', validators=[InputRequired()])


@app.route('/')
def index():
    return 'Welcome to the home page!'


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = next((user for user in users if user.username ==
                    form.username.data and user.password == hash_password(form.password.data)), None)
        if user:
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('upload'))
        else:
            flash('Invalid username or password!', 'error')

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadForm()

    if form.is_submitted():
        album_dir = os.path.join(
            'audio', current_user.username, request.form['album_title'].lower())
        cover = request.files['cover']
        cover_path = os.path.join(
            album_dir, f'cover.{cover.filename.split(".")[-1]}')

        os.makedirs(os.path.dirname(cover_path), exist_ok=True)

        with open(cover_path, 'wb') as file:
            file.write(cover.read())

        songs = request.files.getlist('songs')
        for i, song in enumerate(songs):
            title = request.form[f'title-{i}']
            track = request.form[f'track-{i}']
            release_date_str = request.form[f'release_date-{i}']
            print(release_date_str)
            authors = request.form[f'authors-{i}']

            song_path = os.path.join(album_dir, title.lower())

            # Save the song file
            with open(song_path, 'wb') as file:
                file.write(song.read())

            # Save the metadata
            json_metadata = {
                title: {
                    'file_path': song_path,
                    'cover_path': cover_path,
                    'artist': authors,
                    'album': request.form['album_title'],
                    'date': release_date_str,
                    'track': track
                }
            }
            metadata_path = os.path.join(
                song_path + '.json')
            with open(metadata_path, 'w') as file:
                json.dump(json_metadata, file, indent=4)

        flash('Files uploaded successfully!', 'success')

        # Launch python script
        os.system('python3 main.py')

    return render_template('upload.html', form=form)


if __name__ == '__main__':
    app.run(
        port=8080,
        debug=True)
