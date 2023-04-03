import pymunk
class rigidJoint:
    def __init__(self,b1,b2,space,x,y):
        #joint = pymunk.PinJoint(b1,b2,(0,0),(0,0)) ## didnt finish cause realized i dont need it yet
        joint2 = pymunk.GrooveJoint(b1,b2,(x,y),(x,y+0.1),(0,0))
        #space.add(joint)
        space.add(joint2)