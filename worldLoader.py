#######        SVG World Loader        #######
# Every map must have an invisible 1920x1080 box to define the width and height of the level.
# Adoble Illustrator > File > Export > Export As
# SELECT: Inline Style, SVG, Preserve, Layer Names, 2 Decimals

# Current formatting rules for map:
# [> All rectangles are solid
# [> Temporary rule: Tall rectangles are climable, flat ones are walkable.
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

def load_world(space):
    #world = open('testmap.svg','r')
    worldStatic = []
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
                xpos = (float(xpos)+width/2) + (int(lvl[0:1])*1920)
                ypos = (-float(ypos)-height/2) + (int(lvl[2:3])*1080)

                colour = ln[fFine(ln,'#',1):fFine(ln,';',1)-1]
                
                wall=False
                doDraw=True
                if(colour == '636466'): # Wall check
                    wall=True
                elif(colour == 'fff'):
                    doDraw=False
                #print(doDraw)
                worldStatic.append([xpos*(1280/1920),ypos*(720/1080),width*(1280/1920),height*(720/1080),wall,rotation,doDraw])


    statics = []
    polys = []
    for i in range(len(worldStatic)):
        statics.append(pymunk.Body(body_type=pymunk.Body.STATIC))
        statics[i].position = worldStatic[i][0],worldStatic[i][1]
        statics[i].angle = worldStatic[i][5]
        polys.append(pymunk.Poly.create_box(statics[i],size=(worldStatic[i][2],worldStatic[i][3])))
        polys[i].friction = (worldStatic[i][4]*8)+0.4
        if(worldStatic[i][6]==True):
            space.add(statics[i],polys[i])