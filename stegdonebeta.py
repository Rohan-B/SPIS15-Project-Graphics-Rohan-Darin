from PIL import Image
from random import*

hid = Image.open('rohan.png')
hider = Image.open('blue.png')

width1 = hid.size[0]
height1 = hid.size[1]

width2 = hider.size[0]
height2 = hider.size[1]

def embedD(toHide,toDo):
    #embeds picture, when debeded it becomes degraded
    hid = Image.open(toHide)
    hider = Image.open(toDo)

    width1 = hid.size[0]
    height1 = hid.size[1]

    width2 = hider.size[0]
    height2 = hider.size[1]

    hid = scrambler(toHide)

    for bigw in range(width2):
        for bigh in range(height2):
            #sets last two bits of the picture to be hidden to zero
            (bigR,bigG,bigB)=hider.getpixel((bigw,bigh))
            bigR = (bigR >> 3)<<3
            bigG = (bigG >> 3)<<3
            bigB = (bigB >> 3)<<3
            hider.putpixel((bigw,bigh),(bigR,bigG,bigB))

    for w in range(width1):
        for h in range(height1):
            #shifts first two bits to become the last two bits
            (red,green,blue)=hid.getpixel((w,h))
            red = red >> 5
            green = green >> 5
            blue = blue >> 5
            (bigR,bigG,bigB)=hider.getpixel((w,h))
            red = bigR | red
            green = bigG | green
            blue = bigB | blue
            hider.putpixel((w,h),(red,green,blue))
    hider.show()
    hider.save('hidden.png')


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


def debed(uncode,key):
    #decodes the degraded version of the hidden picture
    hider2 = Image.open(uncode)
    (width2,height2) = hider2.size
    revealed = Image.new("RGB",(width2,height2),'white')
    a = int(key[0:2])
    b1 = int(key[2:4])
    c = int(key[4:6])
    
    for w in range(width2):
        for h in range(height2):
            #shifts last two bits to become the fisrt of the extracted 8 bits
            (r,g,b)=hider2.getpixel((w,h))
            r = (r <<5)&0xFF
            g = (g <<5)&0xFF
            b = (b <<5)&0xFF
            ##
            r = r - a
            g= g + a
            b = b - a
            for x in [r,g,b]:
                if x>255:
                    x = x - 255
                if x<0:
                    x = x + 255
            revealed.putpixel((w,h),(r,g,b))
     
    revealed.show()


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


def scrambler(tohide):
    hide = Image.open(tohide)
    (width,height) = hide.size
    alphabet = ['f']               
    a = randint(10,99)
    b1 = randint(10,99)
    c = randint(10,99)
    d = randint(10,99)
    for w in range(width):
        for h in range(height):
            (r,g,b)= hide.getpixel((w,h))
            r = r + a
            g= g - b1
            b = b + c
            for x in [r,g,b]:
                if x>255:
                    x = x - 255
                if x<0:
                    x = x + 255
            hide.putpixel((w,h),(r,g,b))
    
    hide.show()
    code = str(a) + str(b1) + str(c)
    print code
    return hide
