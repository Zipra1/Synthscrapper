import pyglet
from pyglet.gl import *

import os
working_dir = os.path.dirname(os.path.realpath(__file__)) #Get directory of folder running from
pyglet.resource.path = [os.path.join(working_dir,'Resources')] ## For some reason, pyglet refuses to use local paths (../resources)
pyglet.resource.reindex() #Reindex pyglet resources

 #Note: 0,0 is the lower left corner in the pyglet window.
window = pyglet.window.Window()

#pixel images
label = pyglet.text.Label('Hello, world',font_name='Times New Roman',font_size=36,x=window.width//2, y=window.height//2,anchor_x='center', anchor_y='center')
image = pyglet.resource.image('sprite.png')
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
texture = image.get_texture()
texture.width=256
texture.height=256



@window.event
def on_key_press(symbol,modifiers):
    if(symbol==pyglet.window.key.A):
        pyglet.window.Window.view = pyglet.window.Window.view.from_translation
        

sound = pyglet.resource.media('softdrum.wav',streaming = False) # Store the sound in memory, for short sounds.
music = pyglet.resource.media('20221212_i love coal!!!.wav') # For long tracks
#music.play()

player_char = pyglet.sprite.Sprite(texture, x=400, y=300)

@window.event
def on_mouse_press(x,y,button,modifiers):
    if button == pyglet.window.mouse.LEFT:
        print(x,y)
        sound.play()

@window.event
def on_draw():
    window.clear()
    label.draw()
    texture.blit(0,0)

pyglet.app.run()