import pyglet
import pymunk

class Spear: # Tracking spear. Most complicated weapon (tool?) in the game. What is even happening in here.
    def __init__(self,space,damage):
        self.space = space
        self.damage = damage
        self.spears = [] # Don't remove this. It breaks the game. Its like the coconut in tf2. (fix this later lol)
        self.stuckSpears = []
        self.stuckSpearsShapes = []
        self.canThrow = True
        self.numSpears = 7 # The number of spears the player currently has

    #def createSpear(self,x,y,holdBody): ## Dont create spear, just spawn when you throw it and display it purely visually when on the player.
        
    def throwSpear(self,x,y,angx,angy,power,playerBody):
        if(self.canThrow):
            if(self.numSpears > 0):
                #self.hitbox = pymunk.Poly.create_box(self.spearBody,(2,15))
                self.spearBody = pymunk.Body(3,3000,pymunk.Body.DYNAMIC)
                self.spearBody.position = x,y
                self.spearPoly = pymunk.Poly.create_box(self.spearBody,(55,3))
                self.spearPoly.friction = 0.4
                self.space.add(self.spearBody,self.spearPoly)
                self.spearBody.velocity = self.spearBody.velocity + pyglet.math.Vec2(power*angx,power*angy) + playerBody.velocity/2
                self.spears.append(self.spearBody.shapes)
                self.numSpears -=1

    def stickSpear(self,spear,worldBody,jposition):
        print(jposition)
        jpivot = pymunk.PivotJoint(spear, worldBody, jposition)
        phase = worldBody.angle - spear.angle
        jgear = pymunk.GearJoint(spear, worldBody, phase, 1) ## A pivot joint and a gear joint make a fairly solid joint.
        self.space.add(jpivot)
        self.space.add(jgear)
        #self.spearBodiesFlying.remove(self.spearBody)
        self.spears.remove(self.spearBody.shapes)
        self.stuckSpears.append(self.spearBody)
        self.stuckSpearsShapes.append(self.spearBody.shapes)

    def grabSpear(self,spear,poly):
        self.numSpears+=1
        print(f'grabbed spear{spear.shapes}')
        print(spear,poly)
        self.space.remove(spear,poly)
        self.stuckSpears.remove(spear)
        #self.stuckSpears.remove(spear)
        pass