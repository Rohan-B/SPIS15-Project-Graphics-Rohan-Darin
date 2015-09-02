import os
from flask import Flask, render_template, request, redirect, url_for
from flask import send_from_directory
from werkzeug import secure_filename
from flask import jsonify
from flask import session
from PIL import Image, ImageDraw
import tempfile

app = Flask(__name__)


# Route that will process the file upload
@app.route('/uploadboth', methods=['POST'])
def uploadboth():
    # Get the name of the uploaded file
    file1 = request.files['file1']
    if file1 != '':
        pass
    else:
        print "result was blank"
        # Make the filename safe, remove unsupported chars
        filename1 = secure_filename(file1.filename)

        fullFilename1 = (os.path.join(app.config['UPLOAD_FOLDER'], filename1))
        session['file1'] = fullFilename1
        print "session['file1'] =" ,session['file1']
        # Move the file form the temporal folder to
        # the upload folder we setup
        file1.save(fullFilename1)
        # Redirect the user to the uploaded_file route, which
        # will basicaly show on the browser the uploaded file
    # Get the name of the uploaded file
    file2 = request.files['file2']
    if file2 != '':
        pass
    else:
        print "result was blank"
        # Make the filename safe, remove unsupported chars
        filename2 = secure_filename(file2.filename)

        fullFilename2 = (os.path.join(app.config['UPLOAD_FOLDER'], filename2))
        session['file2'] = fullFilename2
        print "session['file2'] =" ,session['file2']
        # Move the file form the temporal folder to
        # the upload folder we setup
        file2.save(fullFilename2)
        # Redirect the user to the uploaded_file route, which
        # will basicaly show on the browser the uploaded file
    session["encodedimage"] = embedhighres(session['file1'], session['file2'])
    return render_template('websiteOutput1.html', filename = fixFileName(session['encodedimage']))

def fixFileName(badfilename):
    goodfilename = "/" + app.config['UPLOAD_FOLDER'] + os.path.basename(badfilename)
    return goodfilename
    
# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
def getTempFileName(myPrefix):
    f = tempfile.NamedTemporaryFile(suffix = ".bmp", prefix = myPrefix, delete=False, dir=app.config['UPLOAD_FOLDER'])
    f.close()
    return f.name
    
def embedhighres(toHide,toDo):
    #embeds picture, when debeded it becomes a full picture 
    hid = Image.open(toHide)
    hider = Image.open(toDo)
    
    width1 = hid.size[0]
    height1 = hid.size[1]

    width2 = hider.size[0]
    height2 = hider.size[1]

    for bigw in range(width2):
        for bigh in range(height2):
            #sets last two bits of the picture to be hidden to zero
            (bigR,bigG,bigB)=hider.getpixel((bigw,bigh))
            bigR = (bigR >> 2)<<2
            bigG = (bigG >> 2)<<2
            bigB = (bigB >> 2)<<2
            hider.putpixel((bigw,bigh),(bigR,bigG,bigB))
    colors = []
    colors2 = []

    for w in range(width1):
        for h in range(0,height1):
            #shifts first two bits to become the last two bits
            (red,green,blue)=hid.getpixel((w,h))
            red2 = red >> 6
            green2 = green >> 6
            blue2 = blue >> 6
            #preserves the third and fourth bits
            red4 = (red >> 4)<<2
            green4 = (green >> 4)<<2
            blue4 = (blue >> 4)<<2
            red4 = (red4&0x0F)>>2
            green4 = (green4&0x0F)>>2
            blue4 = (blue4&0x0F)>>2
            (bigR,bigG,bigB)=hider.getpixel((w,h*2))
            red = bigR | red2
            green = bigG | green2
            blue = bigB | blue2
            hider.putpixel((w,h*2),(red,green,blue))
            (bigR,bigG,bigB)=hider.getpixel((w,h*2+1))
            red = bigR | red4
            green = bigG | green4
            blue = bigB | blue4
            hider.putpixel((w,h*2+1),(red,green,blue))
            #########
    name = getTempFileName("encodedimage")
    hider.save(name)
    return name

@app.route('/hidepicture')
def hidePicturePage():
    return render_template('websiteEncodePicture.html')

@app.route('/decodemessage')
def decodeMessagePage():
    return render_template('websiteDecodeMessage.html')

@app.route('/recoverpicture')
def recoverPicturePage():
    return render_template('websiteDecodePicture.html')

@app.route('/')
def mainPage():
    return render_template('websiteHome.html')

@app.route('/encodemessage')
def encodeMessagePage():
    return render_template('websiteEncodeMessage.html')
    
if __name__=="__main__":
    app.run(debug=False,host="0.0.0.0",port=54321)
