from flask import Flask, url_for, render_template, request
from PIL import Image

app = Flask(__name__)


def check_file(file):
    # Check if the file is one of the allowed types/extensions
    if not allowed_file(file.filename):
        print "Block 1"
        message = "Sorry. Only files that end with one of these "
        message += "extensions is permitted: " 
        message += str(app.config['ALLOWED_EXTENSIONS'])
        message += "<a href='" + url_for("index") + "'>Try again</a>"
        return message
    elif not file:
        print "block 2"
        message = "Sorry. There was an error with that file.<br>"
        message += "<a href='" + url_for("index") + "'>Try again</a>"
        return message
    return ''

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
    # Get the name of the uploaded file
    file = request.files['file']
    result = check_file(file)
    if result != '':
        print "result was not blank, result =", result
        return result
    else:
        print "result was blank"
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)

        fullFilename = (os.path.join(app.config['UPLOAD_FOLDER'], filename))
        session['file'] = fullFilename
        print "session['file'] =" ,session['file']
        # Move the file form the temporal folder to
        # the upload folder we setup
        file.save(fullFilename)
        # Redirect the user to the uploaded_file route, which
        # will basicaly show on the browser the uploaded file
        session["filter"]=request.form['filters']
        newImage = processimage(session["filter"])
        return render_template('applyfilter.html', newImage = fixupfilename(newImage))

# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/')
def mainPage():
    return render_template('websiteHome.html')

@app.route('/encodemessage')
def encodeMessagePage():
    return render_template('websiteEncodeMessage.html')

@app.route('/encodemessagepython')
def encodeMessageCode():
    hider = request.files['hider']
    hider = Image.open(picture)
    hider.show()
    width1 = hider.size[0]
    height1 = hider.size[1]

    for bigw in range(width1):
        for bigh in range(height1):
            (bigR,bigG,bigB)=hider.getpixel((bigw,bigh))
            bigR = (bigR >> 2)<<2
            bigG = (bigG >> 2)<<2
            bigB = (bigB >> 2)<<2
            hider.putpixel((bigw,bigh),(bigR,bigG,bigB))
    nums = []
    for c in string:
        x = ord(c)
        nums.append(x)
    fnums = []
    for y in nums:
        y1 = bin(y)
        y1 = y1[2:]
        for b in range(8-len(y1)):
            y1 = '0' + y1
        fnums.append(y1)
    shortnums = []
    for x in fnums:
        x1 = x[0:2]
        x2 = x[2:4]
        x3 = x[4:6]
        x4 = x[6:8]
        #print x1,x2,x3,x4
        shortnums.append(x1)
        shortnums.append(x2)
        shortnums.append(x3)
        shortnums.append(x4)
    count = 0
    for bigw in range(width1):
        for bigh in range(height1):
            if count >= len(shortnums):
                pass
            else:
                count = count +1
                x1 = int(shortnums[bigh])
                if x1 == 11:
                    y = 3
                if x1 == 10:
                    y = 2
                if x1 == 0:
                    y = 0
                if x1 == 1:
                    y = 1
                (bigR,bigG,bigB)=hider.getpixel((bigw,bigh))
                bigR = bigR | y
                hider.putpixel((bigw,bigh),(bigR,bigG,bigB))
    hider.save('hiddenwords.png')

@app.route('/hidepicture')
def hidePicturePage():
    return render_template('websiteEncodePicture.html')

@app.route('/decodemessage')
def decodeMessagePage():
    return render_template('websiteDecodeMessage.html')

@app.route('/recoverpicture')
def recoverPicturePage():
    return render_template('websiteDecodePicture.html')


