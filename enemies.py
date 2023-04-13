import pymunk

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
        self.relationship = []
        self.inventory = inventory

        self.head = pymunk.Body(50, 1500, pymunk.Body.DYNAMIC) #Create the head/center of the enemy.
        self.head.position = posx,posy
        #testPolyP = [(0,0),(0,20),(20,20)]
        headPoly = pymunk.Poly.create_box(self.head,(20,20))
        headPoly.friction = 3
        #testPoly = pymunk.Poly(testBody,testPolyP)
        space.add(self.head,headPoly)

    def infoUpdate(self): # Global communications.
        pass

def zero_gravity(body, damping, dt): # Velocity function to remove gravity from an object
        pymunk.Body.update_velocity(body, (0,0), damping, dt)

def zero_gravity_dampen(body, damping, dt): # Velocity function to remove gravity from an object
        #pymunk.Body.update_velocity(body, (0,0), damping, dt)
        body.velocity = body.velocity*0.1
        pass

class Ecenti(Enemy):
    def __init__(self, space, health, posx, posy, anger, fear, goal, adrenaline, politics, inventory):
        super().__init__(space, health, posx, posy, anger, fear, goal, adrenaline, politics, inventory) 
        self.head.velocity_func = zero_gravity

        prevSegment = self.head

        for i in range(12): # Creating segments
             segment = pymunk.Body(5,1500,pymunk.Body.DYNAMIC)
             segment.position = posx+(25*i)+25,posy
             segmentPoly = pymunk.Circle(segment,12.5)
             segmentPoly.friction = 3
             space.add(segment,segmentPoly)
             segment.velocity_func = zero_gravity_dampen
             jpivot = pymunk.PivotJoint(segment, prevSegment, (posx+(25*i)+25,posy))
             jrotlim = pymunk.RotaryLimitJoint(segment,prevSegment,-0.8,0.8)
             space.add(jrotlim)
             space.add(jpivot)
             prevSegment = segment
    
    def act(playerBody):
         pass
        
    
