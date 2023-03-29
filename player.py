from pyglet.window import key
import pyglet
class Player: #Not sure why I made this a class, but I don't feel like changing it now.
    def __init__(self, playerMass,playerMoment, playerSpeed, playerMaxSpeed, jump, left, right, down, canJump, jumpDir, lastJump, onGround, pauseButton):
        self.playerMass = playerMass
        self.playerMoment = playerMoment
        self.playerSpeed = playerSpeed
        self.playerMaxSpeed = playerMaxSpeed
        self.jump = jump
        self.left = left
        self.right = right
        self.down = down
        self.canJump = canJump # Don't jump in the air
        self.jumpDir = jumpDir # For wall jumping
        self.lastJump = lastJump # Anti instantaneous double jump
        self.onGround = onGround
        self.pauseButton = pauseButton
    def onkeypress(self, symbol, modifiers): # Add a menu for controls if extra time (Not essential for project)
        if symbol == key.W:
            self.jump = True
        if symbol == key.A:
            self.left = True
        if symbol == key.S:
            self.down = True
        if symbol == key.D:
            self.right = True
        if symbol == key.P and self.pauseButton==False:
            self.pauseButton = True
        elif symbol == key.P and self.pauseButton==True:
            self.pauseButton = False
    def onkeyrelease(self, symbol, modifiers):
        if symbol == key.W:
            self.jump = False
        if symbol == key.A:
            self.left = False
        if symbol == key.S:
            self.down = False
        if symbol == key.D:
            self.right = False
    def anim(position):
        return pyglet.sprite.Sprite(img=pyglet.resource.image('Resources/sprite.png'))
        