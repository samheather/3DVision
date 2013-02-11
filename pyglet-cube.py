import pyglet

cubeWindow = pyglet.window.Window(width = 400, height = 400)

@cubeWindow.event
def on_draw():
    cubeWindow.clear()
    
    pyglet.gl.glColor4f(1.0,0,0,1.0)

    pyglet.graphics.draw_indexed(8, pyglet.gl.GL_LINES, [0,1,2,3,4,5,6,7],
        ('v3f', (100, 100, -10, 300, 100, 0, #as soon as I change a Z variable, part of the line goes black.
                 100, 100, 0, 100, 300, 0,
                 300, 300, 0, 100, 300, 0,
                 300, 300, 0, 300, 100, 0)))

pyglet.app.run()
