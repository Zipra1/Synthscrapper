import pymunk #Physics
import pyglet #Rendering
import player #Import the player script
import worldLoader #Import the SVG World Loader
import joints
import menus
import weapons
import time
from pymunk.pyglet_util import DrawOptions
#   Pymunk objects note:
# Kinematic objects are controlled by code
# Dyanmic objects are physics controlled (Physics objects)
# Static bodies don't move (Map)
screens = pyglet.canvas.Display.get_screens
resolution = [1920,1080]
window = pyglet.window.Window(resolution[0],resolution[1],"Pymunk Test",fullscreen=True)
pyglet.gl.glClearColor(0.2,0.2,0.2,1)
options = DrawOptions()

wallImage = pyglet.image.load('Sprites/textures/testWall.png')
wallTexture = wallImage.get_texture()


space = pymunk.Space()
frame = pyglet.gui.Frame(window,order=4)
space.gravity = 0,-900
staticbodies=[]
dynamicbodies=[]
kinematicbodies=[]

###Spawning the world & player1
worldTextures = worldLoader.load_world(space,window) # Load the map in space

playerV = player.Player(9,1500,15,150,False,False,False,False,False,False,pyglet.math.Vec2(0,0),0,False,False,False,pyglet.sprite.Sprite(img=pyglet.image.load_animation('Resources/catone.gif')),False,False)
playerBody = pymunk.Body(playerV.playerMass,playerV.playerMoment,pymunk.Body.DYNAMIC)
playerHeadBody = pymunk.Body(2,1000,pymunk.Body.DYNAMIC)
playerBody.position = 640, 700
playerHeadBody.position = 640, 725
playerPoly = pymunk.Poly.create_box(playerBody, size=(20,25)) #Attach a box to the body
playerHead = pymunk.Poly.create_box(playerHeadBody,size=(20,30)) #For crouching, be able to have the head separated.
joints.rigidJoint(playerBody,playerHeadBody,space,0,25)
playerPoly.friction = 4
playerHead.friction = 0
space.add(playerBody, playerPoly)
space.add(playerHeadBody,playerHead)
###End spawning the world

psscreen = menus.pauseScreen(window,playerBody)
wallImage = pyglet.image.load('Sprites/textures/testWall2.bmp')
wallTile = pyglet.image.TileableTexture.create_for_image(wallImage)


spearTest = weapons.Spear(space, 20, 2)
spearTest.createSpear(200,200,playerBody)

@window.event
def on_draw(): # Called by pyglet every frame
    window.clear()
    #wallTile.blit_tiled(x=0, y=0, z=0, width=500, height=500) ##I CANT BELIEVE THIS TOOK ME 2 DAYS TO FIGURE OUT OH MY GOD
    #wallImage.blit(50,50)
    space.debug_draw(options)
    if(playerV.pauseButton==True):
        for elem in psscreen:
                elem.draw()
    # Player animations
    for textparam in worldTextures:
        wallTile.blit_tiled(x=textparam[1]-(textparam[3]/2), y=textparam[2]-(textparam[4]/2), z=0, width=textparam[3], height=textparam[4])
        
    playerV.sprite.position=(playerBody.position.x-playerV.sprite.width*0.5,playerBody.position.y-12.5,0)
    playerV.sprite.draw()
    if(playerV.pauseButton==False):
        space.step(1/60)

@window.event
def on_key_press(symbol, modifiers):
    playerV.onkeypress(symbol,modifiers)
    if(symbol==pyglet.window.key.E):
        spearTest.throwSpear(1,1,100)

@window.event 
def on_key_release(symbol, modifiers):
    playerV.onkeyrelease(symbol,modifiers) #Simplifies code. In player.py
    
screenZoom = [1280,720] ## May want to make this adjust with monitor for different aspect ratios. Currently only for 16:9 monitors.
#1280x720 is default
def update(dt):
    atime=time.time()
    #window.view = window.view.from_rotation(-playerBody.angle/8,pyglet.math.Vec3(0,0,1))
    #window.view = window.view.from_translation(pyglet.math.Vec3(-playerBody.position.x*(resolution[0]/screenZoom[0]) + window.width//2, -playerBody.position.y*(resolution[1]/screenZoom[1]) + window.height//2, 0)) # Change the camera position
    window.view = window.view.from_translation(pyglet.math.Vec3((playerBody.position.x//1280)*(-window.width),-(playerBody.position.y//720)*(window.height),0))
    window.view = window.view.scale(pyglet.math.Vec3(resolution[0]/screenZoom[0],resolution[1]/screenZoom[1],1))
    if(playerV.canJump and playerV.jump):
        playerBody.velocity = playerBody.velocity + pyglet.math.Vec2(playerV.jumpDir.x*400,200*playerV.jumpDir.y)
        playerV.canJump = False
        playerV.lastJump = time.time()
    if(playerV.pauseButton==False):
        playerBody.velocity = playerBody.velocity + pyglet.math.Vec2(-playerV.playerSpeed*playerV.left,0)
        playerBody.velocity = playerBody.velocity + pyglet.math.Vec2(playerV.playerSpeed*playerV.right,0)
        playerBody.velocity_func = limit_velocity
    # Soft cap movement speed
    playerPoly.friction = 4
    if(playerV.left==True):
        playerV.playerSpeed = -sorted((0, pow(1.015,-playerBody.velocity[0]*1.2+(playerV.down*100)), 30))[1]+30
        playerPoly.friction = 0.1
    if(playerV.right==True):
        playerV.playerSpeed = -sorted((0, pow(1.015,playerBody.velocity[0]*1.2+(playerV.down*100)), 30))[1]+30
        playerPoly.friction = 0.1
    
    
    fps=((time.time()-atime))
    if(fps>0.016666667):
        ('FT<60FPS!:', fps)
    #print(playerBody.position.x//1280,'|',playerBody.position.y//720)
    
    

def limit_velocity(body,gravity,damping,dt): #Pymunk velocity function magic?
    maxVelocity = 600-((600-playerV.playerMaxSpeed)*playerV.onGround)
    pymunk.Body.update_velocity(body,gravity,damping,dt)
    scalarVel = body.velocity.length # Get the scalar quantity of the velocity
    if scalarVel > maxVelocity: # Harsh dampen speed if over max velocity
        scale = maxVelocity / scalarVel
        body.velocity = body.velocity * scale
    body.velcoity = body.velocity * 0.98 # Constant slight dampen

def coll_begin(arbiter, space, data): # Start collision calculator
    if({arbiter.shapes[0]} == playerHeadBody.shapes or {arbiter.shapes[1]} == playerHeadBody.shapes): #If coll is with player head
        if({arbiter.shapes[0]} == playerBody.shapes or {arbiter.shapes[1]} == playerBody.shapes): # If coll is between the player's head and body
            return False # dont continue this collision
        if(arbiter.shapes[0].friction == 8.4 or arbiter.shapes[1].friction == 8.4): # Nocollide with walls so your big head doesn't get in the way
            return False # dont continue this collision
    return True # continue collision

def coll_pre(arbiter, space, data): # Pre collision calculation
    #if({arbiter.shapes[0]} == playerBody.shapes or {arbiter.shapes[1]} == playerBody.shapes):
    #    arbiter.surface_velocity = 400,0
    if({arbiter.shapes[0]} == playerHeadBody.shapes or {arbiter.shapes[1]} == playerHeadBody.shapes): # if PLAYER HEAD
        if(playerV.down):
            playerV.inWall=True
            return False
    return True # return true to continue collision

def coll_post(arbiter, space, data): # Post collision calculation
    
    if({arbiter.shapes[0]} == playerBody.shapes or {arbiter.shapes[1]} == playerBody.shapes and not {arbiter.shapes[0]} == playerHeadBody.shapes or {arbiter.shapes[1]} == playerHeadBody.shapes):
        worldBody = int(not {arbiter.shapes[1]} == playerBody.shapes)
        playerV.jumpDir = pyglet.math.Vec2(arbiter.normal.x,arbiter.normal.y+0.7) # Set jump direction to the normal of the last collided body, with additional y force.
        playerV.onGround = True
        playerV.onWall = False
        if(playerV.lastJump+0.1 < time.time()): # Stops instantaneous double jumps
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

def slowUpdate(dt):
    playerV.animCheck()
    if(playerV.wantUp and not playerV.inWall):
        playerV.down = False

handler = space.add_default_collision_handler() # Collision handler, to check when objects are colliding.
handler.begin = coll_begin
handler.pre_solve = coll_pre
handler.post_solve = coll_post
handler.separate = coll_separate

rotLockBody = pymunk.Body(body_type=pymunk.Body.STATIC)
rotLockBody.position = 0,0
rotLock = pymunk.RotaryLimitJoint(playerBody,rotLockBody,0,0)
rotLock2 = pymunk.RotaryLimitJoint(playerHeadBody,rotLockBody,0,0)
space.add(rotLock)
space.add(rotLock2)


if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1/60) # Call function "update" every 1/60th of a second (60fps)
    pyglet.clock.schedule_interval(slowUpdate, 1/20) # For near-realtime logic
    pyglet.app.run()
