import os
from flask import (
    Flask,
    flash,
    request,
    redirect,
    url_for,
    jsonify,
    send_from_directory,
    after_this_request,
)
from flask_cors import CORS
from werkzeug.utils import secure_filename
import threading
import json
import sqlite3
import imageio.v3 as ffmpeg

# Import our processing functions
import OCRFunction
import STTFunction

UPLOAD_FOLDER = "static/video"
ALLOWED_EXTENSIONS = {"mp4", "avi", "webm"}

app = Flask(__name__, static_folder="static")
app.config["UPLOAD_FOLDER"] = os.path.abspath(UPLOAD_FOLDER)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
CORS(app)

# Make sure the db exists
sqliteConnection = sqlite3.connect("sql.db")
cursor = sqliteConnection.cursor()
cursor.execute(
    """CREATE TABLE IF NOT EXISTS files
    (id INTEGER PRIMARY KEY, filename TEXT, processed BOOLEAN DEFAULT 0, processed_data TEXT NULL)"""
)
sqliteConnection.commit()
sqliteConnection.close()

# part to handle the file uploads

# file upload bit

# call captioning funciton in a new thread

# call ocr'ing function in a new thread

# use sqlite database to store response from the functions once done


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def autogenerate_thumbnail(video_id):
    sqliteConnection = sqlite3.connect("sql.db")
    cursor = sqliteConnection.cursor()
    cursor.execute("SELECT filename FROM files WHERE id = ?", [video_id])
    result = cursor.fetchone()

    if result:
        filename = os.path.join(app.config["UPLOAD_FOLDER"], str(video_id)+ result[0])
        for frame_count, first_frame in enumerate(ffmpeg.imiter(filename)):
            ffmpeg.imwrite(os.path.join(app.config["UPLOAD_FOLDER"], str(video_id))+".jpg", first_frame)
            break
        



#handle file upload (and also host barebones test page)
@app.route("/", methods=["GET", "POST"])
def root():
    if request.method == "POST":
        # check if the post request has the file part
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            sqliteConnection = sqlite3.connect("sql.db")
            cursor = sqliteConnection.cursor()
            file_info = (filename, False, None)
            cursor.execute(
                "INSERT INTO files (filename, processed, processed_data) VALUES (?, ?, ?)",
                file_info,
            )
            sqliteConnection.commit()

            newName = str(cursor.lastrowid) + filename
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], newName))
            autogenerate_thumbnail(cursor.lastrowid)

            if thread_event.is_set() == False:
                try:
                    thread_event.set()
                    thread = threading.Thread(target=backgroundTask)
                    thread.start()
                except Exception as error:
                    print("Error starting processing task")

            # return redirect(url_for('download_file', name=filename))

            #return redirect(url_for("server_url", id=str(cursor.lastrowid)))
            return url_for("download_file",id=str(cursor.lastrowid))

    return app.send_static_file("index.html")


# serve the /static directory
@app.route("/<path:path>")
def static_file(path):
    return app.send_static_file(path)


# serve the video player page
@app.route("/watch")
def serve_player_page():
    return app.send_static_file("player.html")


# serve the videos
# is this one being used?
@app.route("/uploads/<id>")
def download_file(id):
    sqliteConnection = sqlite3.connect("sql.db")
    cursor = sqliteConnection.cursor()
    # https://stackoverflow.com/questions/16856647/sqlite3-programmingerror-incorrect-number-of-bindings-supplied-the-current-sta
    # id input MUST be cast to tuple otherwise sql treats each digit as a seperate binding
    cursor.execute("SELECT filename FROM files WHERE id = ?", [id])
    result = cursor.fetchone()

    if result:
        filename = result[0]
        return send_from_directory(app.config["UPLOAD_FOLDER"], id + filename)
    else:
        return "not found", 404
    
@app.route("/uploads/<id>/vtt")
def download_file_vtt(id):
    return send_from_directory(app.config["UPLOAD_FOLDER"], id + ".vtt")

@app.route("/uploads/<id>/thumb")
def download_file_thumb(id):
    return send_from_directory(app.config["UPLOAD_FOLDER"], id + ".jpg")

# get the video metadata
# @app.route("/uploads/<id>/data")
# def download_file_data(id):
#     sqliteConnection = sqlite3.connect("sql.db")
#     cursor = sqliteConnection.cursor()
#     cursor.execute("SELECT * FROM files WHERE id = ?", [id])
#     entries = cursor.fetchall()
#     entry = entries[0]

#     entry_dict = {
#         "id": entry[0],
#         "filename": entry[1],
#         "processed": bool(entry[2]),
#         "json_data": json.loads(entry[3]) if entry[3] else None,
#     }

#     return entry_dict


# Serve video as url
# @app.route("/uploads/url/<id>")
# def server_url(id):
#     sqliteConnection = sqlite3.connect("sql.db")
#     cursor = sqliteConnection.cursor()
#     print(id)
#     cursor.execute("SELECT filename FROM files WHERE id = ?", [id])
#     result = cursor.fetchone()

#     if result:
#         filename = result[0]
#         return url_for("static", filename=("video/" + str(id) + filename))
#     else:
#         return "not found", 404

# serve list of videos for the index page
@app.route("/list")
def json_list_of_videos():

    sqliteConnection = sqlite3.connect("sql.db")
    cursor = sqliteConnection.cursor()
    cursor.execute("SELECT * FROM files")
    entries = cursor.fetchall()

    # Convert entries to a list of dictionaries
    entry_list = []
    for entry in entries:
        entry_dict = {"id": entry[0], "filename": entry[1], "processed": bool(entry[2])}
        entry_list.append(entry_dict)

    return entry_list


# Handle the background processing
# https://tiagohorta1995.medium.com/python-flask-api-background-task-96bf1120a855
thread_event = threading.Event()


def backgroundTask():
    while (True):
        # find all entries in db not processed
        # process them

        # add data to their json_data

        # set processed to true

        break

    thread_event.clear()


# start the server
if __name__ == "__main__":
    app.debug = True
    app.run()
