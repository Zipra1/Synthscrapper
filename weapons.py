import pyglet
import pymunk

class Spear:
    def __init__(self,space,damage,numSpears):
        self.space = space
        self.damage = damage
        self.numSpears = numSpears

    def createSpear(self,x,y,holdBody):
        self.hitbox = [(-30, 0), (0, 3), (10, 0), (0, -3)]
        self.spearBody = pymunk.Body(3,1200,pymunk.Body.DYNAMIC)
        self.spearBody.position = x,y
        self.spearPoly = pymunk.Poly(self.spearBody, self.hitbox)
        self.spearPoly.friction = 0.4
        self.space.add(self.spearBody,self.spearPoly)

    def throwSpear(self,angx,angy,power):
        self.spearBody.velocity = self.spearBody.velocity + pyglet.math.Vec2(power*angx,power*angy)
    
    #def collBegin(self,arbiter):


