import pyglet

def pauseScreen(window,player):
    output=[]
    label = pyglet.text.Label('Quit game',
                          font_name='Arial',
                          font_size=36,
                          x=player.position.x-(1920/2)+300, y=player.position.y+(1080/2)-36,
                          anchor_x='center', anchor_y='center')
    output.append(label)
    return output