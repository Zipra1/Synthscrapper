import pymunk #Physics
import pyglet #Rendering
import threading # Please get me 60FPS when I have more than 3 enemies spawned
import player #Import the player script
import worldLoader #Import the SVG World Loader
from random import randrange
import joints
import menus
import math
import weapons
import time
import enemies

from pyglet.gl import *
#import pathfinding
from pymunk.pyglet_util import DrawOptions
## HOW TO USE PYPY? Makes pymunk like 10x faster. Supposedly.
## It made it slower. guh.


#   Pymunk objects note:
# Kinematic objects are controlled by code (Probably wont use)
# Dyanmic objects are physics controlled (Physics objects)
# Static bodies don't move (Map)

# NIGHT TIME:
# At night, visibility is reduced to only a small area around the player.
# Enemies will become incredibly dangerous, knowing that you can't see them
# Blinking lights on tracking spears can be covered by another enemy if there are multiple around
# Forces the player to go back to town.
# For some players, this could be the ideal hunting time if they have a very aggressive & pro-human build

# FAMINE EVENT
# At some point, robots attack your town: destroying town food source.
# You must go out and forage food in the wilderness. Some NPC's may go with you if I can program that.
# If you have a good relationship with both pro-human robots, they will help and make this very easy.
# Timed by the day/night cycle, and a meter of NPC's that are starving.

# "WRESTLING"
# If you can pin down a robot for long enough, you can open the head and kill it like that or talk to it.
# Talking to it: Threaten it so it makes other enemies leave. This will not change its views on you.
# OR Spare it and tell it to get out of the area. Changes political views and builds relationship.
# Sparing it could be done just by pinning it down until it begins pleading, at which point you release it and it flees.

#IDEA: Draw your own map as you go through spaces instead of the game automatically updating it for you. I think this could add a lot to the game. Maybe stickers to customize your map?
# I think that would just be a really fun idea to implement. Also might be easier than an automatically updating minimap.

#ECENTI BABYSITTING: definetly not gonna have enough time to do this but it'd be cool for after the class
# When an ecentis relationship with you is the highest relationship it has, has a child, and is about to die, it will ask you to protect its kid.
# Whether you do this or not, is up to you.
# It will eventually leave you (with dialogue to let you know)
# This ecenti will have a relationship building debuff with others, but any other robots it interacts will have it's political score set nearer to being pro-human

#PROLOGUE:
# Life is death
# Death hates life
# Even though they're exactly the same

#LORE SILLIES:
# Death message :
#   Self-Simulator
#   Critical failure . . . Rolling back to present . . . Resuming simulation
# Saving messages :
#   Commit to actions? Y/N
#   Executing instructions . . .
#   Present is now.
# Exit message:
#   Are you sure? Unexecuted actions remain. Y/N
#   Y: Rolling back to present . . . Setting clock speed to: INF

#NOTES
# Woulda been cool if I could have implemented... literally anything from this list ^^

# SHAPE FILTERS:
# (1) : For enemies
# (2) : Player and player head


screens = pyglet.canvas.Display.get_screens
resolution = [1280,720]
window = pyglet.window.Window(resolution[0],resolution[1],"Pymunk Test",fullscreen=False)
pyglet.gl.glClearColor(0.2,0.2,0.2,1) # Background colour

options = DrawOptions()
space = pymunk.Space()
#frame = pyglet.gui.Frame(window,order=4)
space.gravity = 0,-750 # Not physically accurate, but most satisfying movement.
staticbodies=[]
dynamicbodies=[]
kinematicbodies=[]

###World setup
worldTextures = worldLoader.load_world(space,window) # Load the map in space and pull images from world loader
playerV = player.Player(9,1200,15,150,False,False,False,False,False,False,pyglet.math.Vec2(0,0),0,False,False,False,pyglet.sprite.Sprite(img=pyglet.image.load_animation('Sprites/player/idleR.gif')),False,False)
playerBody = pymunk.Body(playerV.playerMass,playerV.playerMoment,pymunk.Body.DYNAMIC)
playerHeadBody = pymunk.Body(2,1000,pymunk.Body.DYNAMIC)
playerBody.position = 1100, -700#+1300 # -700
playerHeadBody.position = 1100, -675#+1300 # -675
playerPoly = pymunk.Poly.create_box(playerBody, size=(15,25)) #Attach a box to the body
playerHead = pymunk.Poly.create_box(playerHeadBody,size=(15,30)) #For crouching, be able to have the head separated.
joints.rigidJoint(playerBody,playerHeadBody,space,0,25)
playerPoly.friction = 4
playerHead.friction = 0
space.add(playerBody, playerPoly)
space.add(playerHeadBody,playerHead)

playerEars = pyglet.media.Player
###End of world setup

psscreen = menus.pauseScreen(window,playerBody)
wallImage = pyglet.image.load('Sprites/textures/testWall2.bmp')
wallTile = pyglet.image.TileableTexture.create_for_image(wallImage)

enemyList = set()
estims = set()
#enemyList.append(enemies.Ecenti(space, 20, 300, -300, 1, 0, [3,0], 0, 0.5, [])) # Test enemy

spearTest = weapons.Spear(space, 20)
#spearTest.createSpear(playerBody.position.x-20,playerBody.position.y+5,playerBody)
playerPoly.filter = pymunk.ShapeFilter(2)
playerHead.filter = pymunk.ShapeFilter(2)

fpsDisplay = pyglet.window.FPSDisplay(window=window)
#fpsDisplay.label.color=(255,255,255,255)
vignette = pyglet.image.load('Sprites/player/lighting/vignette.png') # Vignette
vignette.opacity = 10
vignette = vignette.get_texture()
vignette.width = 1920*2
vignette.height = 1080*2
#vignette = pyglet.image.load('vignette.png') # An example lighting texture

#global tick  # sorry. but it had to be done. its for the sake of the gaming running at a reasonable speed. actually no its not it made things way worse.
#tick = 0

@window.event
def on_draw(): # Called by pyglet every frame
    #global tick # aaaaaaaaaaaaaaaaaaaa
    window.clear() # Turns out this actually isn't a requirement, it only makes pure transparency and OpenGL background smear. Sprites and images stay fine, which is all that's being drawn.
                   # How could disabling this lead to less code being run? Feels like it could be.
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST) ## Prevents blurring when upscaling : Magnification filter is set to the "Nearest" algorithim
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST) ## Prevents blurring when downscaling : Minimizing filter is set to the "Nearest" algorithim
    #wallTile.blit_tiled(x=0, y=0, z=0, width=500, height=500) ##I CANT BELIEVE THIS TOOK ME 2 DAYS TO FIGURE OUT OH MY GOD and i DIDNT EVEN USE IT. but alas, such is the way of life.
    #wallImage.blit(50,50)
    #space.debug_draw(options) # debug draw, actually stupid?? nothing going on up there? knocks FPS in half, only use when really needed.

    for image in worldTextures: #MAP : BACKGROUND
        bg = image[0].get_texture() # Draws all textures everywhere all the time. Possible optimization.
        bg.width = 1280
        bg.height = 720
        bg.blit(0,-720)
         
    #                   # PLAYER
    playerV.sprite.position=(playerBody.position.x-playerV.sprite.width*0.5,playerBody.position.y-12.5,0)
    playerV.sprite.draw()

    for spear in spearTest.total: # SPEARS
        spear[1].position = (spear[0].position.x,spear[0].position.y,0)
        spear[1].rotation=-spear[0].angle*57.2958
        spear[1].draw()
        

    # ENEMIES
    for enemy in enemyList: # definetly ask mr.park if there's any optimizations to be done here, this is a lot to iterate through. OPTIMIZATION: Use batches! Slightly faster than a for loop: See pyglet docs.
        for seg in enemy.segments:
            enemy.segmentSprite.position=(seg.position.x,seg.position.y,0)
            enemy.segmentSprite.rotation=-seg.angle*57.2958
            enemy.segmentSprite.draw()
        enemy.headSprite.position=(enemy.head.position.x,enemy.head.position.y,0)
        enemy.headSprite.rotation=-enemy.head.angle*57.2958
        enemy.headSprite.draw()
        for shape in enemy.debugShapes:
            shape.draw()


    for image in worldTextures: #MAP : FOREGROUND
        bg = image[1].get_texture() # Draws all textures everywhere all the time. Possible optimization.
        bg.width = 1280
        bg.height = 720
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA) # GL_ONE_MINUS_DST_COLOR for overlay
        bg.blit(image[2]*1280,(image[3]*720)-720)


    # LIGHTING
    glEnable(GL_BLEND)
    glBlendFunc(GL_DST_COLOR, GL_ZERO)
    vignette.blit(playerBody.position.x-2000,playerBody.position.y-1100) # Example lighting


    # FPS DISPLAY
    fpsDisplay.label.x = playerBody.position.x -60
    fpsDisplay.label.y = playerBody.position.y + 70
    fpsDisplay.draw()
    if(playerV.pauseButton==False): # An if statement every frame? Vile. Please fix this.
        if(fpsDisplay.label.text):
            #print(float(str(fpsDisplay.label.text)))
            space.step(1/float(fpsDisplay.label.text)) # Need to make all applied velocities match this, player moves faster at slower FPS even though pymunk is still running "full speed"
    else:
        for elem in menus.pauseScreen(window,playerBody):
            elem.draw()

    '''tick+=1 ## Because pyglet's clocks don't actually help with optimization, there has to be a different way of executing every x seconds for high cost code (like observe)
    if tick >= 10: # randVal spreads out load over time.
        tick = 0
        print(tick)''' # Actually, it's faster to use pyglet clocks. Even though they dont really work? Likely they use threading/multiprocessing. is there truly nothing to be done about this?
    #End of draw


@window.event
def on_key_press(symbol, modifiers):
    playerV.onkeypress(symbol,modifiers) # Send the keyboard inputs to the player object
    if(symbol==pyglet.window.key.E): # Throwing and grabbing spears with the same key
        if not playerV.pauseButton:
            i=-1
            throw = True
            for spear in spearTest.stuckSpears: # Check if a spear is within grabbing distance
                i+=1
                x1 = playerBody.position.x
                x2 = spear.position.x
                y1 = playerBody.position.y
                y2 = spear.position.y
                if(math.dist([x1,y1],[x2,y2]) < 40): 
                    throw=False
                    spearTest.grabSpear(spear,spearTest.stuckSpearsPoly[i],spear.constraints)
            if(throw):
                spearTest.throwSpear(playerBody.position.x,playerBody.position.y,-playerV.lleft + playerV.lright,randrange(0,20)/400,1300,playerBody)
        

@window.event 
def on_key_release(symbol, modifiers):
    playerV.onkeyrelease(symbol,modifiers) #Simplifies code. In player.py

@window.event # https://www.youtube.com/watch?v=AR_GB5GoL2k
def on_mouse_press(x, y, button, modifiers):
    print('click')
    x=x*(1280/resolution[0])
    y=y*(1280/resolution[0])
    segment_q = space.segment_query_first(playerBody.position,(x,y),1,pymunk.ShapeFilter())
    if segment_q:
        #print(segment_q.shape, segment_q.shape.body)
        contact_point = segment_q.point
        print(contact_point)
        #line = pymunk.Segment(space.static_body, playerBody.position,contact_point,1) # For some reason, this is incredibly laggy. Figure that out maybe? Could lead to other optimizations.
        #line.sensor = True
        #space.add(line)
    else:
        print('no hit')
    prevEne=enemies.Ecenti(space, 20, x, y-720, 1, 0, [3,0], 0, 0.5, [])
    enemyList.add(prevEne)
    estims.add(prevEne.estimPoly)
    estims.add(prevEne.estimPolyNG)


    
screenZoom = [1280,720] ## May want to make this adjust with monitor for different aspect ratios. Currently only for 16:9 monitors.
### ALL BACKGROUNDS MUST BE AT A MULTIPLE OF THIS RESOLUTION!
#1280x720 is default
def update(dt):
    #window.view = window.view.from_rotation(-playerBody.angle/8,pyglet.math.Vec3(0,0,1))
    #window.view = window.view.from_translation(pyglet.math.Vec3(-playerBody.position.x*(resolution[0]/screenZoom[0]) + window.width//2, -playerBody.position.y*(resolution[1]/screenZoom[1]) + window.height//2, 0)) # Change the camera position
    if(playerV.canJump and playerV.jump):
        playerBody.velocity = playerBody.velocity + pyglet.math.Vec2(playerV.jumpDir.x*400,250*playerV.jumpDir.y)
        playerV.canJump = False
        playerV.lastJump = time.time()
    if(playerV.pauseButton==False):
        playerBody.velocity = playerBody.velocity + pyglet.math.Vec2(-playerV.playerSpeed*playerV.left,0)
        playerBody.velocity = playerBody.velocity + pyglet.math.Vec2(playerV.playerSpeed*playerV.right,0)
        playerBody.velocity_func = limit_velocity
    # Soft cap movement speed
    playerPoly.friction = 4

    ## Movement
    if(playerV.left==True):
        playerV.playerSpeed = -sorted((0, pow(1.015,-playerBody.velocity[0]*1.2+(playerV.down*100)), 30))[1]+30
        playerPoly.friction = 0.1
    elif(playerV.right==True):
        playerV.playerSpeed = -sorted((0, pow(1.015,playerBody.velocity[0]*1.2+(playerV.down*100)), 30))[1]+30
        playerPoly.friction = 0.1
    #space.step(dt) # Causes slightly choppy because it does not line up perfectly with the frame draw.
    #print(playerBody.position.x//1280,'|',playerBody.position.y//720) # Print map location
    
    

def limit_velocity(body,gravity,damping,dt): #Pymunk velocity function magic?
    maxVelocity = 600-((600-playerV.playerMaxSpeed)*playerV.onGround)
    pymunk.Body.update_velocity(body,gravity,damping,dt)
    scalarVel = body.velocity.length # Get the scalar quantity of the velocity
    if scalarVel > maxVelocity: # Harsh dampen speed if over max velocity
        scale = maxVelocity / scalarVel
        body.velocity = body.velocity * scale
    #body.velocity = body.velocity * 0.98 # Constant slight dampen. Does this even actually do anything?





    # POTENTIAL OPTIMIZATION: Use pymunk's layers instead of checking if something should collide
    # layers are now being used where possible. but they are not as powerful as expected.
    # there are such things as layer groups. check those out if having collission optimization issues.
def coll_begin(arbiter, space, data): # Start collision calculator (All collision functions are pymunk magic)
    # Here, could check if should even consider the rest of the collision logic. Same goes for all other collision events. "Is it a spear, player, or enemy?"
    #for ene in enemyList: # This is probably painfully unoptimized. But I don't see any other way to do it. Possible optimization.
    if({arbiter.shapes[0]} in spearTest.spears or {arbiter.shapes[1]} in spearTest.spears): # If a spear is colliding with something
        worldBody = int( not {arbiter.shapes[1]} in spearTest.spears)
        spearBody = int({arbiter.shapes[1]} in spearTest.spears)
        if arbiter.shapes[worldBody] not in estims: # Spears dont stick if no enemy is spawned. Not really a problem but its a strange reaction to this.
            if(not {arbiter.shapes[0]} == playerBody.shapes and not {arbiter.shapes[1]} == playerBody.shapes): # Spears can stick to the players head still. This only happened once. Worth?
                spearTest.stickSpear(arbiter.shapes[spearBody].body,arbiter.shapes[worldBody].body,arbiter.contact_point_set.points[0].point_a)

    if({arbiter.shapes[0]} == playerHeadBody.shapes or {arbiter.shapes[1]} == playerHeadBody.shapes): #If coll is with player head
        if({arbiter.shapes[0]} == playerBody.shapes or {arbiter.shapes[1]} == playerBody.shapes): # If coll is between the player's head and body
            return False # dont continue this collision
        if(arbiter.shapes[0].friction == 8.4 or arbiter.shapes[1].friction == 8.4): # Nocollide with walls so your big head doesn't get in the way
            return False # dont continue this collision
    return True # continue collision

def coll_pre(arbiter, space, data): # Pre collision calculation
    if({arbiter.shapes[0]} == playerHeadBody.shapes or {arbiter.shapes[1]} == playerHeadBody.shapes): # if PLAYER HEAD
        if(playerV.down):
            playerV.inWall=True
            return False
    elif({arbiter.shapes[0]} in spearTest.stuckSpearsShapes or {arbiter.shapes[1]} in spearTest.stuckSpearsShapes):
        if({arbiter.shapes[0]} == playerBody.shapes or {arbiter.shapes[1]} == playerBody.shapes):
            return True
        else:
            return False
    return True # return true to continue collision

def coll_post(arbiter, space, data): # Post collision calculation
    if({arbiter.shapes[0]} == playerBody.shapes or {arbiter.shapes[1]} == playerBody.shapes and not {arbiter.shapes[0]} == playerHeadBody.shapes or {arbiter.shapes[1]} == playerHeadBody.shapes):
        worldBody = int(not {arbiter.shapes[1]} == playerBody.shapes) ### ^^ If not <player body + head>
        playerV.jumpDir = pyglet.math.Vec2(arbiter.normal.x,abs(arbiter.normal.y)+0.7) # Set jump direction to the normal of the last collided body, with additional y force.
        playerV.onGround = True
        playerV.onWall = False
        if(playerV.lastJump+0.3 < time.time()): # Stops instantaneous double jumps
                playerV.canJump=True
        if(arbiter.shapes[worldBody].friction == 8.4):
                playerV.onWall=True
                if(playerV.up):
                    playerBody.velocity = playerBody.velocity + pyglet.math.Vec2(0,43*(playerV.left+playerV.right))
                    playerV.playerMaxSpeed = 40
                else:
                    playerV.playerMaxSpeed = 150
                if(playerV.down):
                    playerBody.velocity = playerBody.velocity + pyglet.math.Vec2(0,-15*(playerV.left+playerV.right))
                    playerV.playerMaxSpeed = 150
                
        
def coll_separate(arbiter, space, data): # When collission separates
    if({arbiter.shapes[0]} == playerBody.shapes or {arbiter.shapes[1]} == playerBody.shapes): # If player separates
        playerV.canJump=False
        playerV.onGround=False
        playerV.playerMaxSpeed = 200
    if({arbiter.shapes[0]} == playerHeadBody.shapes or {arbiter.shapes[1]} == playerHeadBody.shapes): # If head separates
        playerV.inWall=False
        playerV.onGround=False

handler = space.add_default_collision_handler() # Collision handler, to check when objects are colliding.
handler.begin = coll_begin
handler.pre_solve = coll_pre
handler.post_solve = coll_post
handler.separate = coll_separate

threads=[]

def slowUpdate(dt):
    #playerV.animCheck()
    thread = threading.Thread(target=playerV.animCheck)
    thread.start()
    threads.append(thread)
    for hostile in enemyList:
        hostile.act()
    for hostile in enemyList:
        hostile.observe(playerPoly,playerHead,playerBody,playerV)
    if(playerV.wantUp and not playerV.inWall):
        playerV.down = False
    if(not playerV.pauseButton):
        window.view = window.view.from_translation(pyglet.math.Vec3((playerBody.position.x//1280)*(-window.width),-(playerBody.position.y//720)*(window.height),0))
        window.view = window.view.scale(pyglet.math.Vec3(resolution[0]/screenZoom[0],resolution[1]/screenZoom[1],1))
    if playerV.down:
        playerHead.filter = pymunk.ShapeFilter(1) # Enemies won't see player head when crouching, allowing for hiding behind smaller walls. makes crouching actually useful
    else:
        playerHead.filter = pymunk.ShapeFilter(2)
    #playerEars = pyglet.media.Player.position = playerBody.position

def secClock(dt):
    for thread in threads:
        thread.join()
    for ene in enemyList:
        print('\n\n\n\n\nNEWLINE\n\n\n\n')
        for ln in ene.nodeMap:
            print(ln)

rotLockBody = pymunk.Body(body_type=pymunk.Body.STATIC) # Stops the player from falling over.
rotLockBody.position = 0,0 
rotLock = pymunk.RotaryLimitJoint(playerBody,rotLockBody,0,0)
rotLock2 = pymunk.RotaryLimitJoint(playerHeadBody,rotLockBody,0,0)
space.add(rotLock)
space.add(rotLock2)

## These dont actually improve performance when you change how often they are called? What?
## Soft clocks seem to slightly improve performance.
pyglet.clock.schedule_interval_soft(update, 1/60) # Call function "update" every 1/60th of a second (60fps)
pyglet.clock.schedule_interval_soft(slowUpdate, 1/10) # For near-realtime logic
#pyglet.clock.schedule_interval_soft(slowerUpdate, 1/10) # For non-realtime logic. Op count doesn't matter. of course it doesnt! Aaaa
pyglet.clock.schedule_interval_soft(secClock, 1.1)
pyglet.app.run(interval=1/60) # Start the game loop. Max FPS is 60