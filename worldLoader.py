#######        SVG World Loader        #######
# Every map must have an invisible 1920x1080 box to define the width and height of the level
# Adoble Illustrator > File > Export > Export As
# SELECT: Inline Style, SVG, Preserve, Layer Names, 2 Decimals

# Current formatting rules for map:
# [> Key rectangles are static
#   [> #636466 means climbable
# [> #00aeef (cyan) rectangles are dynamic
# [> #fff (no fill) means do not load
# [> 

# Art rules:
# 640x360
# Stay somewhat consistent
import pymunk
import pyglet
import os

def fFine(haystack,needle,occ): # For extracting specific information from files
    occurs = 0
    indx=0
    for c in haystack:
        indx+=1
        if c == needle:
            occurs+=1
        if occurs == occ:
            return indx
    return(-1)

def load_world(space,window):

    '''
    wallImage = pyglet.image.load('Sprites/textures/testWall2.bmp')
    wallTexture = pyglet.image.TileableTexture(50,50,'Sprites/textures/testWall2.bmp',0)

    testBody = pymunk.Body(50, 1500, pymunk.Body.DYNAMIC) ## This is just to test the effects of spears on dynamic bodies while I work on implementing dynamics to the world editor.
    testBody.position = 640,400
    #testPolyP = [(0,0),(0,20),(20,20)]
    testPoly = pymunk.Poly.create_box(testBody,(20,20))
    testPoly.friction = 0.4
    #testPoly = pymunk.Poly(testBody,testPolyP)
    space.add(testBody,testPoly)
    '''
    #world = open('testmap.svg','r')
    worldStatic = []
    worldStaticPoly=[]
    worldStaticPolyPoints=[]
    #print(os.listdir('levels'))
    i=0
    for lvl in os.listdir('levels'):
        #print(lvl)
        world= open('levels/'+lvl,'r')
        i+=1
        for ln in world:
            if(ln[fFine(ln,'r',1)-1:fFine(ln,'t',1)]=='rect'):
                xpos = ln[fFine(ln,'"',1):fFine(ln,'"',2)-1] # Get x position of rect
                if(xpos=='.5'):xpos=0

                ypos = ln[fFine(ln,'"',3):fFine(ln,'"',4)-1] # Get y position of rect
                if(ypos=='.5'):ypos=0

                width = float(ln[fFine(ln,'"',5):fFine(ln,'"',6)-1]) # Get width rect
                height = float(ln[fFine(ln,'"',7):fFine(ln,'"',8)-1]) # Get height rect
                if('rotate' in ln):
                    rotation = float(ln[fFine(ln,'(',2):fFine(ln,')',2)-1])*-0.0174533
                else:rotation = 0
                #print(lvl[2:3])
                worldOffsetx=(int(lvl[0:1])*1920)
                worldOffsety=(int(lvl[2:3])*1080)
                xpos = (float(xpos)+width/2) + worldOffsetx
                ypos = (-float(ypos)-height/2) + worldOffsety

                colour = ln[fFine(ln,'#',1):fFine(ln,';',1)-1]
                
                wall=False
                doDraw=True
                dynamic=False
                if(colour == '636466'): # Wall check
                    wall=True
                elif(colour == 'fff'):
                    doDraw=False
                elif(colour == '00aeef'):
                    dynamic=True
                #print(doDraw)
                worldStatic.append([xpos*(1280/1920),ypos*(720/1080),width*(1280/1920),height*(720/1080),wall,rotation,doDraw,dynamic])
            if(ln[fFine(ln,'p',1)-1:fFine(ln,'n',1)]=='polygon'):
                pointstr=[]
                run=True
                i=0
                pointstr.append(float(ln[fFine(ln,'"',1):fFine(ln,' ',4)-1]))
                while run:
                    if(fFine(ln,'"',2)) > fFine(ln,' ',5+i):
                        pointstr.append(ln[fFine(ln,' ',4+i):fFine(ln,' ',5+i)-1])
                    else:
                        run=False
                    i+=1
                pointstr.append(ln[fFine(ln,' ',3+i):fFine(ln,'"',2)-1])
                worldStaticPolyPoints.append(pointstr) #Polygons half implemented.
                #print(worldStaticPolyPoints)

    statics = []
    polys = []
    image = []
    for i in range(len(worldStatic)):
        if(worldStatic[i][7]==False):
            statics.append(pymunk.Body(body_type=pymunk.Body.STATIC))
        else:
            statics.append(pymunk.Body((worldStatic[i][2]*worldStatic[i][3])//100, (worldStatic[i][2]*worldStatic[i][3])*2, pymunk.Body.DYNAMIC))
        statics[i].position = worldStatic[i][0],worldStatic[i][1]
        statics[i].angle = worldStatic[i][5]
        polys.append(pymunk.Poly.create_box(statics[i],size=(worldStatic[i][2],worldStatic[i][3])))
        polys[i].friction = (worldStatic[i][4]*8)+0.4
        if(worldStatic[i][6]==True):
            space.add(statics[i],polys[i])
            #wallTexture = wallImage.get_texture()
            #image.append([wallTexture,worldStatic[i][0],worldStatic[i][1],worldStatic[i][2],worldStatic[i][3]])
    #return image
    worldTextures = []
    for lvl in os.listdir('levelsart/background'):
        #worldTextures.append(pyglet.resource.image('levelsart/'+lvl))
        Offsetx=int(lvl[0:1])
        Offsety=int(lvl[2:3])
        background = pyglet.resource.image('levelsart/background/'+lvl)
        foreground = pyglet.resource.image('levelsart/foreground/'+lvl)
        worldTextures.append([background,foreground,Offsetx,Offsety])
    return worldTextures 