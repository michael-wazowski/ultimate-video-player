from flask import Flask

import OCRFunction

import STTFunction

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

#part to handle the file uploads

    #file upload bit

    #call captioning funciton in a new thread

    #call ocr'ing function in a new thread

    #use sqlite database to store response from the functions once done

#part to serve the index.html / css / javascript UI

#part to serve json of given timestamps from the database for given file