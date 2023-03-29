import pyglet
import os
working_dir = os.path.dirname(os.path.realpath(__file__)) #Get directory of folder running from
pyglet.resource.path = [os.path.join(working_dir,'Resources')] ## For some reason, pyglet refuses to use local paths (../resources)
pyglet.resource.reindex() #Reindex pyglet resources

game_window = pyglet.window.Window(800, 600)


playerImage = pyglet.resource.image('cattwo.png')
image = pyglet.resource.image('catone.gif')
image2 = pyglet.resource.image('sprite.png')

def center_image(image):
    image.anchor_x = image.width//2
    image.anchor_y = image.height//2

center_image(playerImage)
center_image(image) 
center_image(image2)

score_label = pyglet.text.Label(text="Score: 0", x=10, y=460)
level_label = pyglet.text.Label(text="My Amazing Game",
                            x=game_window.width//2, y=game_window.height//2, anchor_x='center')

player_char = pyglet.sprite.Sprite(img=playerImage, x=400, y=300)

@game_window.event
def on_draw():
    game_window.clear()
    
    level_label.draw()
    score_label.draw()
    player_char.draw()

if __name__ == '__main__':
    pyglet.app.run()