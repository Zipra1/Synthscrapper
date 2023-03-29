import pymunk #Physics
import pyglet #Rendering
import player #Import the player script
import worldLoader #Import the SVG World Loader
import menus
import time
from pymunk.pyglet_util import DrawOptions
#   Pymunk objects note:
# Kinematic objects are controlled by code (Player and enemies)
# Dyanmic objects are physics controlled (Physics objects)
# Static bodies don't move (Map)
screens = pyglet.canvas.Display.get_screens
resolution = [1280,720]
window = pyglet.window.Window(resolution[0],resolution[1],"Pymunk Test")
options = DrawOptions()

space = pymunk.Space()
frame = pyglet.gui.Frame(window,order=4)
space.gravity = 0,-981
staticbodies=[]
dynamicbodies=[]
kinematicbodies=[]

###Spawning the world & player
worldLoader.load_world(space) # Load the map in space

playerV = player.Player(10,3000,20,200,False,False,False,False,False,pyglet.math.Vec2(0,0),0,False,False) # Mass, Moment, Speed, Key,Key,Key,Key,CanJump,JumpDir,onGround
playerBody = pymunk.Body(playerV.playerMass,playerV.playerMoment,pymunk.Body.DYNAMIC)
playerBody.position = 640, 700
playerPoly = pymunk.Poly.create_box(playerBody, size=(30,30)) #Attach a box to the body
playerPoly.friction = 1
#print(playerPoly.center_of_gravity)
space.add(playerBody, playerPoly)
###End spawning the world


@window.event
def on_draw(): # Called by pyglet every frame
    window.clear()
    space.debug_draw(options)
    for elem in menus.pauseScreen(window,playerBody):
        if(playerV.pauseButton==True):
            elem.draw()
            
    # Player animations

    image = pyglet.resource.image('sprite.png')
    texture = image.get_texture()   ## Resizing image without blurring using OpenGL
    pyglet.gl.glTexParameteri(pyglet.gl.GL_TEXTURE_2D, pyglet.gl.GL_TEXTURE_MAG_FILTER, pyglet.gl.GL_NEAREST)
    texture.width = 30
    texture.height = 90
    playerSprite = pyglet.sprite.Sprite(texture,x=playerBody.position.x-15,y=playerBody.position.y-15)
    playerSprite.draw()
        

@window.event
def on_key_press(symbol, modifiers):
    playerV.onkeypress(symbol,modifiers)

@window.event 
def on_key_release(symbol, modifiers):
    playerV.onkeyrelease(symbol,modifiers) #Simplifies code. In player.py
    
screenZoom = [1280,720] ## May want to make this adjust with monitor for different aspect ratios. Currently only for 16:9 monitors.
#1280x720 is default
def update(dt):
    #window.view = window.view.from_rotation(-playerBody.angle/8,pyglet.math.Vec3(0,0,1))
    window.view = window.view.from_translation(pyglet.math.Vec3(-playerBody.position.x*(resolution[0]/screenZoom[0]) + window.width//2, -playerBody.position.y*(resolution[1]/screenZoom[1]) + window.height//2, 0)) # Change the camera position
    window.view = window.view.scale(pyglet.math.Vec3(resolution[0]/screenZoom[0],resolution[1]/screenZoom[1],1))

    

def limit_velocity(body,gravity,damping,dt): #Pymunk velocity function magic?
    max_velocity = 600-((600-playerV.playerMaxSpeed)*playerV.onGround)
    pymunk.Body.update_velocity(body,gravity,damping,dt)
    scalarVel = body.velocity.length # Get the scalar quantity of the velocity
    if scalarVel > max_velocity: # Harsh dampen speed if over max velocity
        scale = max_velocity / scalarVel
        body.velocity = body.velocity * scale
    body.velcoity = body.velocity * 0.98 # Constant slight dampen

def coll_begin(arbiter, space, data): # Start collision calculator
    return True

def coll_pre(arbiter, space, data): # Pre collision calculation
    #if({arbiter.shapes[0]} == playerBody.shapes or {arbiter.shapes[1]} == playerBody.shapes):
    #    arbiter.surface_velocity = 400,0
    return True

def coll_post(arbiter, space, data): # Post collision calculation
    if({arbiter.shapes[0]} == playerBody.shapes or {arbiter.shapes[1]} == playerBody.shapes):
        playerV.jumpDir = pyglet.math.Vec2(arbiter.normal.x,arbiter.normal.y+1) # Set jump direction to the normal of the last collided body, with additional y force.
        playerV.onGround = True
        if(playerV.lastJump+0.1 < time.time()): # Stops instantaneous double jumps
            playerV.canJump=True
        
def coll_separate(arbiter, space, data): # When collission separates
    if({arbiter.shapes[0]} == playerBody.shapes or {arbiter.shapes[1]} == playerBody.shapes):
        playerV.canJump=False
        playerV.onGround=False

handler = space.add_default_collision_handler() # Collision handler, to check when objects are colliding.
handler.begin = coll_begin
handler.pre_solve = coll_pre
handler.post_solve = coll_post
handler.separate = coll_separate

def physupdate(dt): ### Updating physics
    #[> If adding moving platforms, change playerBody.velocity to a local velocity.
    #[> Calculate by saving the body previously collided with and make a local velocity based off that. I think this is how Titanfall does it.
    #if(playerBody.velocity.length < 200):
    #playerBody.angle = sorted((-0.4, playerBody.angle, 0.4))[1] # Lock rotation to a fixed amount
    #playerBody.angle = 0 # "Lock" rotation to 0
    rotLockBody = pymunk.Body(body_type=pymunk.Body.STATIC)
    rotLockBody.position = 0,0
    rotLock = pymunk.RotaryLimitJoint(playerBody,rotLockBody,0,0)
    space.add(rotLock)
    if(playerV.canJump and playerV.jump):
        playerBody.velocity = playerBody.velocity + pyglet.math.Vec2(playerV.jumpDir.x*250,200*playerV.jumpDir.y)
        playerV.canJump = False
        playerV.lastJump = time.time()
    if(playerV.pauseButton==False):
        playerBody.velocity = playerBody.velocity + pyglet.math.Vec2(-playerV.playerSpeed*playerV.left,0)
        playerBody.velocity = playerBody.velocity + pyglet.math.Vec2(playerV.playerSpeed*playerV.right,0)
        playerBody.velocity_func = limit_velocity
    #playerPoly.friction = pow(1.002,playerBody.velocity.length)/3
    #print(playerBody.velocity[0])
    # Soft cap movement speed
    playerPoly.friction = 4
    if(playerV.left==True):
        playerV.playerSpeed = -sorted((0, pow(1.015,-playerBody.velocity[0]*1.2), 30))[1]+30
        playerPoly.friction = 0.1 ## This might break wall climbing. Test later when the world loader is built up enough.
    if(playerV.right==True):
        playerV.playerSpeed = -sorted((0, pow(1.015,playerBody.velocity[0]*1.2), 30))[1]+30
        playerPoly.friction = 0.1
    #print(playerPoly.friction)
    
    #print(playerV.playerSpeed ) # sorted((0, pow(1.015,playerBody.velocity.length*1.2), 5))[1]
    if(playerV.pauseButton==False):
        space.step(1/60) #Physics step of 1/60th of a second. Means lag will slow down physics as well as rendering (If this doesn't happen, this start to clip through each other.)


if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1/60) # Call function "update" every 1/60th of a second (60fps)
    pyglet.clock.schedule_interval(physupdate,1/60) # Update physics at 60FPS. This value will never change.
    pyglet.app.run()
