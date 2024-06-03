import os, sys
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
from flask_socketio import SocketIO
from werkzeug.utils import secure_filename
import threading
import json
import sqlite3
import ffmpeg

# Import our processing functions
# import OCRFunction
import STTFunction

UPLOAD_FOLDER = "static/video"
ALLOWED_EXTENSIONS = {"mp4", "avi", "webm"}
FFMPEG_PATH = os.path.abspath("BackendEnv/ffmpeg/bin/ffmpeg.exe")
SQL_PATH = os.path.abspath("sql.db")

app = Flask(__name__, static_folder="static")
app.config["UPLOAD_FOLDER"] = os.path.abspath(UPLOAD_FOLDER)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

socketio = SocketIO(app, cors_allowed_origins="*")

CORS(app)

# Make sure the db exists
sqliteConnection = sqlite3.connect(SQL_PATH)
cursor = sqliteConnection.cursor()
cursor.execute(
    """CREATE TABLE IF NOT EXISTS files
    (id INTEGER PRIMARY KEY, filename TEXT, extension TEXT, processed BOOLEAN DEFAULT 0, processed_data TEXT NULL)"""
)
sqliteConnection.commit()
sqliteConnection.close()

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def autogenerate_thumbnail(video_path, thumbnail_id):
    if os.path.exists(video_path):
        outputFilename = os.path.join(app.config["UPLOAD_FOLDER"], str(thumbnail_id))+".jpg"
        ffmpeg.input(video_path, ss="00:00:00").output(outputFilename, vframes=1).run(quiet=False, cmd=FFMPEG_PATH, overwrite_output=True)

# converts any video in the DB to webm format for standardization reasons
def autoconvert_video(current_path, final_path):
    ffmpeg.input(current_path).output(final_path, vcodec="libvpx", acodec="libvorbis").run(quiet=False, cmd=FFMPEG_PATH, overwrite_output=True)
    os.remove(current_path)


def get_extension(video_id):
    sqliteConnection = sqlite3.connect(SQL_PATH)
    cursor = sqliteConnection.cursor()
    cursor.execute("SELECT extension FROM files WHERE id = ?", [video_id])
    result = cursor.fetchone()
    sqliteConnection.close()

    if result:
        filename = result[0]
        return filename
    else:
        return ""


#handle file upload and delete (and also host barebones test page)
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
            currentFilename = secure_filename(file.filename)
            currentExtension = "." + currentFilename.split(".")[-1]
            sqliteConnection = sqlite3.connect(SQL_PATH)
            cursor = sqliteConnection.cursor()
            file_info = (currentFilename, currentExtension, False, None)
            cursor.execute(
                "INSERT INTO files (filename, extension, processed, processed_data) VALUES (?, ?, ?, ?)",
                file_info,
            )
            sqliteConnection.commit()

            tempName = str(cursor.lastrowid) + currentExtension
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], tempName))
            autogenerate_thumbnail(os.path.join(app.config["UPLOAD_FOLDER"], tempName), cursor.lastrowid) # create the thumbnail before starting the conversion/processing of the video since that can take time
            
            #Spin off a new thread so multiple videos can be converted at the same time
            #newConversionThread = threading.Thread(target=lambda: convert_video_task(os.path.join(app.config["UPLOAD_FOLDER"], tempName), os.path.join(app.config["UPLOAD_FOLDER"], finalName), cursor.lastrowid))
            #newConversionThread.start()
            newSTTThread = threading.Thread(target=lambda: generate_stt_task(os.path.join(app.config["UPLOAD_FOLDER"], tempName), cursor.lastrowid))
            newSTTThread.start()

            #if thread_event.is_set() == False:
            #    try:
            #        thread_event.set()
            #        thread = threading.Thread(target=backgroundTask)
            #        thread.start()
            #    except Exception as error:
            #        print("Error starting processing task")

            # return redirect(url_for('download_file', name=filename))
            
            sqliteConnection.close()
            socketio.emit('list-change', json_list_of_videos())
            #return redirect(url_for("server_url", id=str(cursor.lastrowid)))
            #return url_for("download_file",id=str(cursor.lastrowid))
            return "Upload Started", 200

    return app.send_static_file("index.html")


# serve the /static directory
@app.route("/<path:path>")
def static_file(path):
    return app.send_static_file(path)

# serve the videos
# is this one being used?
@app.route("/uploads/<id>")
def download_file(id):
    return send_from_directory(app.config["UPLOAD_FOLDER"], str(id) + get_extension(id))


@app.route("/delete/<id>", methods=["DELETE"])
def delete_file(id):
    try:
        extension = get_extension(id)

        if extension != "":
            try:
                path = os.path.join(app.config["UPLOAD_FOLDER"], id)
                os.remove(path + extension)
                os.remove(path + ".jpg")
                os.remove(path + ".vtt")
            except:
                pass
        
        sqliteConnection = sqlite3.connect(SQL_PATH)
        cursor = sqliteConnection.cursor()
        cursor.execute("DELETE FROM files WHERE id = ?", [id])
        sqliteConnection.commit()
        sqliteConnection.close()

        socketio.emit('list-change',json_list_of_videos())

        return "Succes", 200
    except:
        return "File already deleted", 204

    
@app.route("/uploads/<id>/stt")
def download_file_stt(id):
    return send_from_directory(app.config["UPLOAD_FOLDER"], id + ".vtt")

@app.route("/uploads/<id>/ocr")
def download_file_ocr(id):
    return send_from_directory(app.config["UPLOAD_FOLDER"], id + "OCR.vtt")

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

    sqliteConnection = sqlite3.connect(SQL_PATH)
    cursor = sqliteConnection.cursor()
    cursor.execute("SELECT * FROM files")
    entries = cursor.fetchall()
    sqliteConnection.close()

    # Convert entries to a list of dictionaries
    entry_list = []
    for entry in entries:
        entry_dict = {"id": entry[0], "filename": entry[1], "processed": entry[3]}
        entry_list.append(entry_dict)

    return entry_list


# Handle the background processing
# https://tiagohorta1995.medium.com/python-flask-api-background-task-96bf1120a855
thread_event = threading.Event()

#def convert_video_task(current_path, final_path, video_id):
#    autoconvert_video(current_path, final_path)
#    generate_stt_task(final_path, video_id)

def generate_stt_task(video_path, video_id):

    STTFunction.STTFunction(video_path, video_id, FFMPEG_PATH)
    sqliteConnection = sqlite3.connect(SQL_PATH)
    cursor = sqliteConnection.cursor()
    cursor.execute("UPDATE files SET processed = 1 WHERE id = ?",[video_id])
    sqliteConnection.commit()
    sqliteConnection.close()
    socketio.emit('list-change', json_list_of_videos())

def backgroundTask():
    while (True):
        # find all entries in db not processed
        sqliteConnection = sqlite3.connect(SQL_PATH)
        cursor = sqliteConnection.cursor()
        cursor.execute("SELECT * FROM files WHERE processed = 0")
        entries = cursor.fetchall()

        if len(entries) < 1:
            break
        # process them

        for entry in entries:
            print(entry)

            id = entry[0]

            STTFunction.STTFunction(os.path.join(app.config["UPLOAD_FOLDER"],str(id) + get_extension(id)), id)

            #Call this when ocr function made
            #OCRFunction.OCRFunction(os.path.join(app.config["UPLOAD_FOLDER"],str(id) + get_extension(id)), id)

            #set processed to true
            cursor.execute("UPDATE files SET processed = 1 WHERE id = ?",[entry[0]])
            sqliteConnection.commit()
            sqliteConnection.close()

            socketio.emit('list-change',json_list_of_videos())

    thread_event.clear()
    print("Background Thread Stop")


# start the server
if __name__ == "__main__":
    app.debug = True
    socketio.run(app, port=8000)
    #app.run()
