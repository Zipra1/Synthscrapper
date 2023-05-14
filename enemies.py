import pymunk
import pyglet
import math
import random
import time
import asyncio

class Enemy:
    '''
    The enemy class defines the base properties of an enemy.
    Each enemy is fairly complicated, with "emotions" to dictate how
    an enemy acts. High anger will cause it to be more reckless and aggressive,
    with less regard for the future.
    An aggressive enemy does not mean it will attack you aimlessly. Have them try
    to hide, then trick the player into going into a vulnerable position (in front
    of a hiding spot, on dynamic objects, near traps). Extremely high aggression
    may mean the enemy will sacrifice itself to kill you.
    
    Fear will cause it to try and hide, but also panic and be slightly more clumsy.

    Accomplishment is whether or not it considers its life worthwhile. High
    accomplishment will cause an enemy to be more determined on killing you, 
    with little regard for itself.

    Goal determines what the enemy currently wants to do. An array of tasks, can have multiple.
    0: Kill the player
    1: Repair environment
    2: Survive
    3: Track player

    Politics determines how much the enemy agrees with humans and robots. A high political level
    represents an enemy prepared to lose their life to end yours. The lowest political
    level would mean the robot would try to help you, although this should be very rare.
    Somewhere inbetween might be a separate smaller "tribe" of robots, who are neutral to you (like endermen)
    Enemies with drastically different political levels will be aggressive toward each other.

    Relationship is a list of all enemies with a value to represent how close they are. Very
    close enemies will share similar politics, anger, fear, and goals. Having similar feeling values
    will also increase the relationship value. Emotionally close enemies will also communicate
    with each other much more effectively, at times possibly ambushing (or rarely protecting) the player.
    The player is capable of being in the relationship list, though will be at a disadvantage with
    all enemies except for near zero political enemies.

    Inventory is a list of all the items an enemy has. Enemies can use some items, but this will
    mostly be used for item drops.

    Adrenaline increases an enemy's effectiveness in a fight. Causes enemies hunting you to be more powerful than sneaking up on an enemy.

    health: The amount of health the enemy has
    posx: Spawn position(x) of the enemy as well as the position the enemy is currently at
    posy: ^^
    '''


    def __init__(self, space, health, posx, posy, anger, fear, goal, adrenaline, politics, inventory):
        self.space = space
        self.health = health
        self.posx = posx
        self.posy = posy
        self.anger = anger
        self.fear = fear
        self.goal = goal
        self.adrenaline = adrenaline
        self.politics = politics
        self.relationship = {'player':60,'jared':0} # Should probably use ad ictionary for this. ENTITY:RELATIONSHIPVALUE
        self.inventory = inventory
        self.memory = {'lastSeenPlayerPosition':(0,0),'playerPositionConfidence':False,'lastSeenPlayerTime':time.time(),'lastSeenPlayerVelocity':(0,0),'lastSeenPlayerState':'Standing'}
        self.map = []
        self.estimatedPlayerPosition = (0,0)
        
        #Debug variables, comment when done.
        self.debugShapes = []
        self.red = random.randrange(0,255)
        self.green = random.randrange(0,255)
        self.blue = random.randrange(0,255)
        self.debugCircle = pyglet.shapes.Circle(0,0,10,color=(self.red,self.green,self.blue,255))

        self.head = pymunk.Body(50, 1500, pymunk.Body.DYNAMIC) #Create the head/center of the enemy.
        self.head.position = posx,posy
        #testPolyP = [(0,0),(0,20),(20,20)]
        headPoly = pymunk.Circle(self.head,12.5)
        headPoly.friction = 3
        headPoly.filter = pymunk.ShapeFilter(1)
        #testPoly = pymunk.Poly(testBody,testPolyP)
        space.add(self.head,headPoly)

    def infoUpdate(self): # Global communications.
        pass

def zero_gravity(body, gravity, damping, dt): # Velocity function to remove gravity from an object
        pymunk.Body.update_velocity(body, (0,0), damping, dt)

def zero_gravity_dampen(body, gravity, damping, dt): # Velocity function to remove gravity from an object
        #pymunk.Body.update_velocity(body, (0,0), damping, dt)
        body.velocity = body.velocity*0.85

class Ecenti(Enemy):
    '''Same as Enemy class with:
        Specific sprites
        Segmented
        act()
        observe()
    
    '''
    
    def __init__(self, space, health, posx, posy, anger, fear, goal, adrenaline, politics, inventory):
        #def coll_begin(arbiter,space,data): # Another collision handler here with just a begin, to make code easier to read.
        #    return True
        super().__init__(space, health, posx, posy, anger, fear, goal, adrenaline, politics, inventory) 
        self.head.velocity_func = zero_gravity
        prevSegment = self.head
        segmentImg = pyglet.image.load('Sprites/creatures/ecenti/segment.png')
        segmentImg.anchor_x = segmentImg.width//2
        segmentImg.anchor_y = segmentImg.height//2
        headImg = pyglet.image.load('Sprites/creatures/ecenti/head.png')
        headImg.anchor_x = 12
        headImg.anchor_y = headImg.height//2
        self.segmentSprite = pyglet.sprite.Sprite(segmentImg)
        self.headSprite = pyglet.sprite.Sprite(headImg)
        self.segments = []

        self.estimBody = pymunk.Body(7,1500,pymunk.Body.DYNAMIC)
        self.estimPoly = pymunk.Circle(self.estimBody,4)
        self.estimPoly.filter = pymunk.ShapeFilter(2)
        space.add(self.estimBody,self.estimPoly)
        self.estimBodyNG = pymunk.Body(7,1500,pymunk.Body.DYNAMIC)
        self.estimPolyNG = pymunk.Circle(self.estimBodyNG,4)
        self.estimPolyNG.filter = pymunk.ShapeFilter(2)
        space.add(self.estimBodyNG,self.estimPolyNG)
        self.estimBodyNG.velocity_func = zero_gravity

        #debug
        self.estimCircle = pyglet.shapes.Circle(0,0,4,color=(75,125,255,255))
        self.estimCircle2 = pyglet.shapes.Circle(0,0,4,color=(255,125,75,255))
        #handler = space.add_default_collision_handler() # Collision handler, to check when objects are colliding.
        #handler.begin = coll_begin

        for i in range(9): # Creating segments
             segment = pymunk.Body(5,1500,pymunk.Body.DYNAMIC)
             segment.position = posx+(25*i)+25,posy
             segmentPoly = pymunk.Circle(segment,12.5)
             segmentPoly.friction = 0
             #segmentPoly.filter = pymunk.ShapeFilter(3) #this doesn't optimize much i think
             space.add(segment,segmentPoly)
             segment.velocity_func = zero_gravity_dampen
             jpivot = pymunk.PivotJoint(segment, prevSegment, (posx+(25*i)+25,posy))
             jrotlim = pymunk.RotaryLimitJoint(segment,prevSegment,-1.2,1.2)
             space.add(jrotlim)
             space.add(jpivot)
             prevSegment = segment
             self.segments.append(segment)
    
    def act(self): #20 TPS
        '''Low-cost thinking and movement'''
        if(self.memory['playerPositionConfidence']==1):
            self.head.velocity = self.head.velocity + pyglet.math.Vec2((self.estimBody.position.x-self.head.position.x)*0.8,(self.estimBody.position.y-self.head.position.y)*0.8)
        elif(self.memory['playerPositionConfidence']==0.5):
            self.head.velocity = self.head.velocity + pyglet.math.Vec2((self.estimBodyNG.position.x-self.head.position.x)*0.8,(self.estimBodyNG.position.y-self.head.position.y)*0.8)
        self.estimCircle.x = self.estimBody.position.x
        self.estimCircle.y = self.estimBody.position.y
        self.estimCircle2.x = self.estimBodyNG.position.x
        self.estimCircle2.y = self.estimBodyNG.position.y
        pass
        #self.estimBody.velocity = (self.memory['lastSeenPlayerVelocity'][0]/1.5*(self.memory['lastSeenPlayerState']),self.memory['lastSeenPlayerVelocity'][1]/1.5)

    async def observe(self,playerPoly,playerHead,playerBody,playerV): #6 TPS
        '''Take in surroundings and high-cost thinking
        Executes at 6TPS, but still be careful with optimization. it's still fairly heavy with lots of enemies.
        '''
        # print(self.memory['lastSeenPlayerVelocity'])
        #testv = 5
        #for i in range(1000000): # Testing impact
             #testv+=i
             #aa = testv
        self.debugShapes = []
        for i in range(20): # The enemies see in really low resolution raytracing, RTX ON!
            segment_q = self.space.segment_query_first(self.head.position,(self.head.position.x+(math.sin(-self.head.angle-1.571-(i/(10))+1)*1000),self.head.position.y+(math.cos(-self.head.angle-1.571-(i/(10))+1)*1000)),1,pymunk.ShapeFilter(1))
            if segment_q:
                contact_point = segment_q.point
                if segment_q[0] in [playerPoly,playerHead]: # If can see player
                     #self.debugCircle = pyglet.shapes.Circle(0,0,10,color=(255,0,0,255))
                     self.memory['playerPositionConfidence']=1 # Confident of players position
                     self.memory['lastSeenPlayerPosition'] = (contact_point.x,contact_point.y)
                     self.memory['lastSeenPlayerTime'] = time.time()
                     self.estimBody.position = playerBody.position+(0,5)
                     self.estimBodyNG.position = playerBody.position+(0,5)
                     self.estimBody.velocity = playerBody.velocity
                     self.estimBodyNG.velocity = playerBody.velocity
                     self.memory['lastSeenPlayerVelocity'] = playerBody.velocity
                     self.memory['lastSeenPlayerState'] = (playerV.onWall*'onWall')+(playerV.onGround*'onGround')
                elif segment_q[0]==self.estimPoly:
                     self.memory['playerPositionConfidence']=0.5 # Move to second best guess
                elif segment_q[0]==self.estimPolyNG and self.memory['playerPositionConfidence']==0.5:
                     self.memory['playerPositionConfidence']=0 # Dont know where player is
                #self.debugCircle.x = contact_point.x
                #self.debugCircle.y = contact_point.y
                #self.debugShapes.append(self.debugCircle)
                self.debugShapes.append(self.estimCircle)
                self.debugShapes.append(self.estimCircle2)
                #print(self.memory['lastSeenPlayerState'])
                #print(contact_point)
         

        

