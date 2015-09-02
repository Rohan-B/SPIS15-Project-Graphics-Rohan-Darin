from PIL import Image
from random import*

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
    hider.show()
    hider.save('hidden2.png')

def debed2(uncode):
    hider2 = Image.open(uncode)
    (width2,height2) = hider2.size
    revealed = Image.new("RGB",(width2,height2),'white')
    colors = []
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
    for w in range(0,width2):
        for h in range(0,height2/2):
            revealed.putpixel((w,h),colors[x])
            x = x+1
    revealed.save('prefinal.png')
    finalpic('prefinal.png')

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
    final.show()


######Words#########
def embed_message(string, picture):
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
