import os
from flask import Flask, render_template, request, redirect, url_for, send_file
from flask import send_from_directory
from werkzeug import secure_filename
from flask import jsonify
from flask import session
from PIL import Image, ImageDraw
import tempfile

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploadedimg/'
app.secret_key='rohandarinsecretkeyisthebest234568dskfd24525sdf';

# Route that will process the file upload
@app.route('/uploadboth', methods=['POST'])
def uploadboth():
    print('5')
    # Get the name of the uploaded file
    file = request.files['file1']
    if file == '5':
        pass
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
    # Get the name of the uploaded file
    file2 = request.files['file2']
    if file2 == '5':
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
    print 6109
   # session["encodedimage"] = embedhighres(session['file'], session['file2'])
    #print 2930
    filename= embedhighres(session['file'], session['file2'])
    filename = os.path.basename(filename)
    #print filename

    return render_template('websiteOutput2.html', filename=filename )

@app.route('/converted/<filename>', methods=['GET'])
def getconvertedimage(filename):
     print filename
     print fixFileName(filename)
     return send_file(fixFileName(filename), mimetype='image/png')
     
@app.route('/uploadtext', methods=['POST'])
def gettextimg():
    print 56
    file = request.files['file']
    if file == '5':
        pass
    else:
        print "test"
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
    # Get the name of the uploaded file
    session['string'] = request.form['message']
    print session['string'] 
    filename= embed_message(session['file'], session['string'])
    filename = os.path.basename(filename)
    #print filename

    return render_template('websiteOutput3.html', filename=filename )

@app.route('/decodetext',methods=['POST'])
def decodetext():
	print 56
	file = request.files['file']
	print "test"
	filename = secure_filename(file.filename)
	fullFilename = (os.path.join(app.config['UPLOAD_FOLDER'],filename))
	session['file'] = fullFilename
        print "session['file'] =" ,session['file']
        # Move the file form the temporal folder to
        # the upload folder we setup
        file.save(fullFilename)
        # Redirect the user to the uploaded_file route, which
        # will basicaly show on the browser the uploaded file
    # Get the name of the uploaded file
	return render_template('websiteOutput1.html',message = debed_message(session['file']))
	
@app.route('/decodeimage',methods=['POST'])
def decodeimage():
	print 56
	file = request.files['file']
	print "test"
	filename = secure_filename(file.filename)
	fullFilename = (os.path.join(app.config['UPLOAD_FOLDER'],filename))
	session['file'] = fullFilename
        print "session['file'] =" ,session['file']
        # Move the file form the temporal folder to
        # the upload folder we setup
        file.save(fullFilename) 
	print 2454
        # Redirect the user to the uploaded_file route, which
        # will basicaly show on the browser the uploaded file
    # Get the name of the uploaded file
        print session['file']
	decodedimage = debed2(session['file'])
	print decodedimage
	finalimage = finalpic(decodedimage)
        f = fixFileName(finalimage)
        return send_file(f, mimetype ='image/png')

def fixFileName(badfilename):
    print 'badfilename =', badfilename 
    goodfilename = app.config['UPLOAD_FOLDER'] + os.path.basename(badfilename)
    print 'goodfilename=',goodfilename
    return goodfilename
    
# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
def getTempFileName(myPrefix):
    f = tempfile.NamedTemporaryFile(suffix = ".png", prefix = myPrefix, delete=False, dir=app.config['UPLOAD_FOLDER'])
    f.close()
    return f.name

def getTemptext(myPrefix):
    f = tempfile.NamedTemporaryFile(suffix = ".txt", prefix = myPrefix, delete=False, dir=app.config['UPLOAD_FOLDER'])
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

def embed_message(picture,string):
    hider = Image.open(picture)
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
    name = getTempFileName("encodedimage")
    hider.save(name)
    return name

def debed_message(picture):
    hider = Image.open(picture)
    width1 = hider.size[0]
    height1 = hider.size[1]
    shortnums = []
    string_output  = ''
    for bigw in range(width1):
        for bigh in range(height1):
            (r,g,b)=hider.getpixel((bigw,bigh))
            r = r & 0x03
            shortnums.append(r)
    for r in range(0,len(shortnums),4):
        x1 = shortnums[r]
        x2 = shortnums[r+1]
        x3 = shortnums[r+2]
        x4 = shortnums[r+3]
        x1 = x1 << 6
        x2 = x2 << 4
        x3 = x3 << 2
        final = x1+x2+x3+x4
        if x1+x2+x3+x4 != 0:
            final = chr(final)
            string_output = string_output + final
    return string_output

def debed2(uncode):
    print 213134
    hider2 = Image.open(uncode)
    print 564
    (width2,height2) = hider2.size
    revealed = Image.new("RGB",(width2,height2),'white')
    colors = []
    print 1
    for w in range(0,width2):
        for h in range(0,height2,2):
            (r,g,b)=hider2.getpixel((w,h))
            r = (r <<6)&0xFF
            g = (g <<6)&0xFF
            b = (b <<6)&0xFF
            #print('r:',bin(r))
            (r2,g2,b2)=hider2.getpixel((w,h+1))
            r2 = (r2 <<6)&0xFF
            g2 = (g2 <<6)&0xFF
            b2 = (b2 <<6)&0xFF

            r2 = r2 >> 2
            g2 = g2 >> 2
            b2 = b2 >> 2
            #print('r2:',bin(r2))
            rf = r + r2
            gf = g + g2
            bf = b + b2
            #print('rf:',bin(rf))
            colors.append((rf,gf,bf))
    x = 0
    print 5
    for w in range(0,width2):
        for h in range(0,height2/2):
            revealed.putpixel((w,h),colors[x])
            x = x+1
    name = getTempFileName("debed")
    revealed.save(name)
    return name

def finalpic(uncoded):
    uncd = Image.open(uncoded)
    (width2,height2) = uncd.size
    picwidth = []
    piclength = []
    for w in range(width2):
        (r,g,b)= uncd.getpixel((w,0))
        if (r,g,b) != (0,0,0):
            picwidth.append((r))
    for h in range(height2):
        (r,g,b)= uncd.getpixel((0,h))
        if (r,g,b) != (0,0,0) and (r,g,b) != (255,255,255):
            piclength.append((r))
    hlen = len(piclength)
    wlen = len(picwidth)
    final = Image.new("RGB",(wlen,hlen))
    for w in range(wlen):
        for h in range(hlen):
            (r,g,b)= uncd.getpixel((w,h))
            final.putpixel((w,h),(r,g,b))
    name = getTempFileName("debed")
    final.save(name)
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
