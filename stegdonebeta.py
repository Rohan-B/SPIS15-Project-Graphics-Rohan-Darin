from PIL import Image

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

    for bigw in range(width2):
        for bigh in range(height2):
            #sets last two bits of the picture to be hidden to zero
            (bigR,bigG,bigB)=hider.getpixel((bigw,bigh))
            bigR = (bigR >> 2)<<2
            bigG = (bigG >> 2)<<2
            bigB = (bigB >> 2)<<2
            hider.putpixel((bigw,bigh),(bigR,bigG,bigB))

    for w in range(width1):
        for h in range(height1):
            #shifts first two bits to become the last two bits
            (red,green,blue)=hid.getpixel((w,h))
            red = red >> 6
            green = green >> 6
            blue = blue >> 6
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
        for h in range(height1):
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
            colors.append([red2,green2,blue2])
            colors2.append([red4,green4,blue4])
    for w in range(0,width1):
        for h in range(0,height1,2):
            (bigR,bigG,bigB)=hider.getpixel((w,h))
            red = bigR | colors[w*h][0]
            green = bigG | colors[w*h][1]
            blue = bigB | colors[w*h][2]
            hider.putpixel((w,h),(red,green,blue))
            (bigR,bigG,bigB)=hider.getpixel((w,h+1))
            red = bigR | colors2[w*h][0]
            green = bigG | colors2[w*h][1]
            blue = bigB | colors2[w*h][2]
            hider.putpixel((w,h+1),(red,green,blue))
    hider.show()
    hider.save('hidden2.png')


def debed(uncode):
    #decodes the degraded version of the hidden picture
    hider2 = Image.open(uncode)
    (width2,height2) = hider2.size
    revealed = Image.new("RGB",(width2,height2),'white')

    for w in range(width2):
        for h in range(height2):
            #shifts last two bits to become the fisrt of the extracted 8 bits
            (r,g,b)=hider2.getpixel((w,h))
            r = (r <<6)&0xFF
            g = (g <<6)&0xFF
            b = (b <<6)&0xFF
            revealed.putpixel((w,h),(r,g,b))
    revealed.show()


def debed2(uncode):
    hider2 = Image.open(uncode)
    (width2,height2) = hider2.size
    revealed = Image.new("RGB",(width2,height2),'white')
    colors = []
    for w in range(0,width2,2):
        for h in range(0,height2,2):
            (r,g,b)=hider2.getpixel((w,h))
            r = (r <<6)&0xFF
            g = (g <<6)&0xFF
            b = (b <<6)&0xFF
            #print('r:',bin(r))
            (r2,g2,b2)=hider2.getpixel((w+1,h+1))
            r2 = (r2 <<6)&0xFF
            g2 = (g2 <<6)&0xFF
            b2 = (b2 <<6)&0xFF

            r2 = r2 >> 2
            g2 = g2 >> 2
            b2 = b2 >> 2
            #print('r2:',bin(r2))
            rf = r | r2
            gf = g | g2
            bf = b | b2
            #print('rf:',bin(rf))
            colors.append((rf,gf,bf))
    x = 0
    for w in range(0,width2/2):
        for h in range(0,height2/2):
            revealed.putpixel((w,h),colors[x])
            x = x+1
    revealed.show()
