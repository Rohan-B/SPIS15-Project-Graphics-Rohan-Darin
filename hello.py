from flask import Flask, url_for, render_template, request
from PIL import Image

app = Flask(__name__)

@app.route('/')
def mainPage():
    return render_template('websiteHome.html')

@app.route('/encodemessage')
def encodeMessagePage():
    return render_template('websiteEncodeMessage.html')

@app.route('/hidepicture')
def hidePicturePage():
    return render_template('websiteEncodePicture.html')

@app.route('/decodemessage')
def decodeMessagePage():
    return render_template('websiteDecodeMessage.html')

@app.route('/recoverpicture')
def recoverPicturePage():
    return render_template('websiteDecodePicture.html')
