from flask import Flask, url_for, render_template, request
from PIL import Image

app = Flask(__name__)

@app.route('/')
def mainPage():
    return render_template('websiteHome.html')

@app.route('/encodemessage')
def encodeMessagePage():
    return render_template('websiteEncodeMessage.html')

@app.route('/encodemessagepython')
def encodeMessagePage():
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


