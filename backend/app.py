import os
from flask import Flask, flash, request, redirect, url_for, jsonify, send_from_directory, after_this_request
from flask_cors import CORS
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "../static/video"
ALLOWED_EXTENSIONS = {'mp4','avi'}


app = Flask(__name__, static_folder='static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)

#Stuff for the database
import sqlite3

sqliteConnection = sqlite3.connect('sql.db')
cursor = sqliteConnection.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS files
    (id INTEGER PRIMARY KEY, filename TEXT, processed BOOLEAN DEFAULT 0, processed_data TEXT NULL)''')
sqliteConnection.commit()
sqliteConnection.close()

import json

#Stuff for the processor functions
import OCRFunction

import STTFunction

@app.route("/upload_complete")
def upload_complete():
    return "<h1>File Upload Complete!</h1><a href='/'>Return</a>"

#part to handle the file uploads

    #file upload bit

    #call captioning funciton in a new thread

    #call ocr'ing function in a new thread

    #use sqlite database to store response from the functions once done

#part to serve the index.html / css / javascript UI

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET', 'POST'])
def root():
    if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)

                sqliteConnection = sqlite3.connect('sql.db')
                cursor = sqliteConnection.cursor()
                file_info = (filename, False, None)
                cursor.execute('INSERT INTO files (filename, processed, processed_data) VALUES (?, ?, ?)', file_info)
                sqliteConnection.commit()

                file.save(os.path.join(app.config['UPLOAD_FOLDER'], str(cursor.lastrowid)+filename))
                #return redirect(url_for('download_file', name=filename))
                return redirect(url_for('upload_complete'))

    return app.send_static_file('index.html')
    #return "Kellefef"

#serve the /static directory
@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)

#serve the video player page
@app.route('/watch')
def serve_player_page():
    return app.send_static_file('player.html')

#serve the videos
@app.route('/uploads/<id>')
def download_file(id):
    sqliteConnection = sqlite3.connect('sql.db')
    cursor = sqliteConnection.cursor()
    cursor.execute('SELECT filename FROM files WHERE id = ?', (id))
    result = cursor.fetchone()

    if result:
        filename = result[0]
        return send_from_directory(app.config["UPLOAD_FOLDER"], id+filename)
    else:
        return "not found", 404    

#Serve video as url
@app.route('/uploads/url/<id>')
def server_url(id):
    sqliteConnection = sqlite3.connect('sql.db')
    cursor = sqliteConnection.cursor()
    cursor.execute('SELECT filename FROM files WHERE id = ?', (id))
    result = cursor.fetchone()

    if(result):
        filename = result[0]
        return url_for('static', filename=("video/"+id+filename))
    else:
        return "not found", 404    

#serve list of videos for the index page
@app.route('/list')
def json_list_of_videos():

    sqliteConnection = sqlite3.connect('sql.db')
    cursor = sqliteConnection.cursor()
    cursor.execute('SELECT * FROM files')
    entries = cursor.fetchall()

    # Convert entries to a list of dictionaries
    entry_list = []
    for entry in entries:
        entry_dict = {
            'id': entry[0],
            'filename': entry[1],
            'processed': bool(entry[2]),
            'json_data': json.loads(entry[3]) if entry[3] else None
        }
        entry_list.append(entry_dict)

    return entry_list

#part to serve json of given timestamps from the database for given file
if(__name__ == "__main__"):
    app.debug = true
    app.run()