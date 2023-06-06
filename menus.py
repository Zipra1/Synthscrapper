import pyglet

pyglet.font.add_file('FFFFORWA.TTF')
pyglet.font.load('FFF Forward')

def pauseScreen(window,playerBody):
    output=[] # (playerBody.position.x//1280)*(-window.width),-(playerBody.position.y//720)*(window.height)
    label = pyglet.text.Label('Quit game',
                          font_name='FFF Forward',
                          font_size=24,
                          x=(playerBody.position.x//1280)*(window.width) + 140, 
                          y=(playerBody.position.y//720)*(window.height)+window.height - 30,
                          anchor_x='center', anchor_y='center')
    output.append(label)
    return output

def dialogueBox(window,playerBody,text,image):
    output=[]
    label = pyglet.text.Label(text,
                          font_name='Arial',
                          font_size=36,
                          x=(playerBody.position.x//1280)*(window.width) + 140, 
                          y=(playerBody.position.y//720)*(window.height)+window.height - 30,
                          anchor_x='center', anchor_y='center')