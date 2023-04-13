import pyglet
import pymunk

class Spear: # Tracking spear. Most complicated weapon (tool?) in the game. What is even happening in here.
    def __init__(self,space,damage):
        self.space = space
        self.damage = damage
        self.spears = []
        self.spearsPoly = []
        self.stuckSpears = []
        self.stuckSpearsShapes = []
        self.stuckSpearsPoly = []
        self.canThrow = True
        self.numSpears = 2 # The number of spears the player currently has

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
                self.spearsPoly.append(self.spearPoly)
                self.numSpears -=1

    def stickSpear(self,spear,worldBody,jposition):
        print(jposition)
        jpivot = pymunk.PivotJoint(spear, worldBody, jposition)
        phase = worldBody.angle - spear.angle
        jgear = pymunk.GearJoint(spear, worldBody, phase, 1) ## A pivot joint and a gear joint make a fairly solid joint.
        self.space.add(jpivot)
        self.space.add(jgear)
        #self.spearBodiesFlying.remove(self.spearBody)
        self.spearsPoly = []
        self.spears=[]
        self.stuckSpears.append(self.spearBody)
        self.stuckSpearsPoly.append(self.spearPoly)
        self.stuckSpearsShapes.append(self.spearBody.shapes)

    def grabSpear(self,spear,poly,constraints):
        self.numSpears+=1
        self.space.remove(spear,poly)
        for joint in constraints: # Remove all joints attatched to the spear, leaving them behind might cause performance issues after playing for a while
            self.space.remove(joint)
        self.stuckSpears.remove(spear)
        self.stuckSpearsPoly.remove(poly)
        self.stuckSpearsShapes.remove(spear.shapes)
        pass