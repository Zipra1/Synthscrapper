from pyglet.window import key
import pyglet
class Player: #Not sure why I made this a class, but I don't feel like changing it now.
    def __init__(self, playerMass,playerMoment, playerSpeed, playerMaxSpeed, jump, left, right, down, up, canJump, jumpDir, lastJump, onGround, onWall, pauseButton, sprite):
        self.playerMass = playerMass
        self.playerMoment = playerMoment
        self.playerSpeed = playerSpeed
        self.playerMaxSpeed = playerMaxSpeed
        self.jump = jump
        self.left = left
        self.right = right
        self.down = down
        self.up = up
        self.canJump = canJump # Don't jump in the air
        self.jumpDir = jumpDir # For wall jumping
        self.lastJump = lastJump # Anti instantaneous double jump
        self.onGround = onGround
        self.onWall = onWall
        self.pauseButton = pauseButton # Don't use ESC
        #Animation setup
        self.sprite = sprite
        self.animLeft = pyglet.image.load_animation('Resources/2053.gif')
        self.animIdle = pyglet.image.load_animation('Resources/catone.gif')
    def onkeypress(self, symbol, modifiers): # Add a menu for controls if extra time (Not essential for project)
        if symbol == key.SPACE:
            self.jump = True
            self.animCheck()
        if symbol == key.A:
            self.left = True
            self.animCheck()
        if symbol == key.S:
            self.down = True
            if(self.onWall):
                self.animCheck()
        if symbol == key.D:
            self.right = True
            self.animCheck()
        if symbol == key.W:
            self.up = True
            if(self.onWall):
                self.animCheck()
        if symbol == key.P and self.pauseButton==False:
            self.pauseButton = True
        elif symbol == key.P and self.pauseButton==True:
            self.pauseButton = False
    def onkeyrelease(self, symbol, modifiers):
        if symbol == key.SPACE:
            self.jump = False
            self.animCheck()
        if symbol == key.A:
            self.left = False
            self.animCheck()
        if symbol == key.S:
            self.down = False
            if(self.onWall):
                self.animCheck()
        if symbol == key.D:
            self.right = False
            self.animCheck()
        if symbol == key.W:
            self.up = False
            if(self.onWall):
                self.animCheck()
    def animCheck(self):
        #print(self.onWall)
        if(self.left and self.onGround):
            print('left')
            self.sprite = pyglet.sprite.Sprite(img=self.animLeft)
            self.sprite.scale_x = 20/self.sprite.width
            self.sprite.scale_y = 55/self.sprite.height
        else:
            print('idle')
            self.sprite = pyglet.sprite.Sprite(img=self.animIdle)
            self.sprite.scale_x = 20/self.sprite.width
            self.sprite.scale_y = 55/self.sprite.height
        
        