from pyglet.window import key
import pyglet
# TO ADD:
# S to crouch / slide
class Player: 
    '''This class represents the player.
        wantUp: True if the player is stuck under an object crouching and wants to stand up.
    '''
    def __init__(self, playerMass,playerMoment, playerSpeed, playerMaxSpeed, jump, left, right, down, up, canJump, jumpDir, lastJump, onGround, onWall, pauseButton, sprite, inWall, wantUp):
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
        self.lleft = False
        self.wantUp = False
        self.lright = False
        self.inWall = inWall
        #Animation setup
        self.sprite = sprite
        self.animLeft = pyglet.sprite.Sprite(pyglet.image.load_animation('Sprites/player/walkL.gif'))
        self.animRight = pyglet.sprite.Sprite(pyglet.image.load_animation('Sprites/player/walkR.gif'))
        self.animCrouchLeft = pyglet.sprite.Sprite(pyglet.image.load_animation('Sprites/player/crouchwalkL.gif'))
        self.animCrouchRight = pyglet.sprite.Sprite(pyglet.image.load_animation('Sprites/player/crouchwalkR.gif'))
        self.animCrouchIdleL = pyglet.sprite.Sprite(pyglet.image.load_animation('Sprites/player/crouchidleL.gif'))
        self.animCrouchIdleR = pyglet.sprite.Sprite(pyglet.image.load_animation('Sprites/player/crouchidleR.gif'))
        self.animWallRight = pyglet.sprite.Sprite(pyglet.image.load_animation('Sprites/player/wallR.gif'))
        self.animClimbRight = pyglet.sprite.Sprite(pyglet.image.load_animation('Sprites/player/climbR.gif'))
        self.animClimbLeft = pyglet.sprite.Sprite(pyglet.image.load_animation('Sprites/player/climbL.gif'))
        self.animWallLeft = pyglet.sprite.Sprite(pyglet.image.load_animation('Sprites/player/wallL.gif'))
        self.animIdleR = pyglet.sprite.Sprite(pyglet.image.load_animation('Sprites/player/idleR.gif'))
        self.animIdleL = pyglet.sprite.Sprite(pyglet.image.load_animation('Sprites/player/idleL.gif'))
    def onkeypress(self, symbol, modifiers): # Add a menu for controls if extra time (Not essential for project)
        if symbol == key.SPACE:
            self.jump = True
            self.animCheck()
        if symbol == key.A:
            self.left = True
            self.lleft = True
            self.lright = False
            self.animCheck()
        elif symbol == key.D:
            self.right = True
            self.lright = True #llright and lleft are for the last direction the player was going in. used for idle animation directions.
            self.lleft = False
            self.animCheck()
        if symbol == key.S:
            self.down = True
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
            if(self.inWall):
                self.wantUp=True
            else:
                self.wantUp=False
                self.down=False
            self.animCheck()
        if symbol == key.D:
            self.right = False
            self.animCheck()
        if symbol == key.W:
            self.up = False
            if(self.onWall):
                self.animCheck()
    def animCheck(self): ## DO NOT Make the sprite in this! pyglet.sprite.Sprite creates a NEW sprite. Make any sprites in __init__
        if(self.left and self.onGround and not self.right and not self.onWall): # LEFT
            if(self.down): # CROUCH
                self.sprite = self.animCrouchLeft
            else: # NOCROUCH
                self.sprite = self.animLeft
        elif(self.right and self.onGround and not self.left and not self.onWall): # RIGHT
            if(self.down): # CROUCH
                self.sprite = self.animCrouchRight
            else: # NOCROUCH
                self.sprite = self.animRight
        elif(self.right and not self.left and self.onWall): # RIGHT WALL
            if(self.up and not self.down): # CLIMB
                self.sprite = self.animClimbRight
            else:
                self.sprite = self.animWallRight
        elif(self.left and not self.right and self.onWall): # LEFT WALL
            if(self.up and not self.down): # CLIMB
                self.sprite = self.animClimbLeft
            else:
                self.sprite = self.animWallLeft
        else: # IDLE
            if(self.lleft == True):
                if(self.down):
                    self.sprite = self.animCrouchIdleL
                else:
                    self.sprite = self.animIdleL
            if(self.lright == True):
                if(self.down):
                    self.sprite = self.animCrouchIdleR
                else:
                    self.sprite = self.animIdleR
        