import numpy as np
import pygame as pg
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import ProjectileMotion as pm

def hex_to_colour(hex):
    return [float(int(hex[i:i+2],16))/255 for i in range(1, len(hex), 2)]

def polygon(coords, r, colour, verticies=100):
    x, y = coords
    theta = 0
    theta_step = 2*np.pi / 100
    glBegin(GL_POLYGON)
    glColor3f(colour[0], colour[1], colour[2])
    for _ in range(verticies):
        x_, y_ = x+(r*np.cos(theta)), y+(r*np.sin(theta))
        theta += theta_step
        glVertex2f(int(x_),int(y_))
    glEnd()

def callback():
    for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
    global tstep_no
    if tstep_no % speed == 0:
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        frametime = clk.tick()           
        if frametime>=1/framerate:
            for i in range(env.num_bodies):
                body = env.bodies[i]
                colour = hex_to_colour(colours[i])
                radius = radiuses[i]
                x = (body.pos[0]/scale) + (display[0]*0.5)
                y = (body.pos[1]/scale) + (display[1]*0.5)
                polygon((x,y), radius, colour, 100)
            glFlush()
            pg.display.flip()
        else:
            pg.time.wait((1/framerate) - frametime)
    tstep_no += 1

pg.init()
pg.display.set_caption("Physics Simulation")
display = (1920, 1080)

pg.display.set_mode(display, pg.OPENGL|pg.DOUBLEBUF)
glClearColor(0.0, 0.0, 0.0, 1.0)
gluOrtho2D(0, display[0], 0, display[1])

framerate = 30
timestep = 60*60
scale = 5e+9
speed = 10
tstep_no = 0
clk = pg.time.Clock()
colours = ["#fdb813","#d5d2d1","#8B7D82","#0077be","#a1251b","#c88b3a","#ab604a","#65868b","#73acac", "#9ca6b7"]
radiuses = np.array([20, 7.01, 17.39, 18.30, 9.74, 200.9, 167.4, 72.87, 70.76, 3.4])*0.2
env = pm.Environment.from_json("planets.json")
_ = env.run(timestep=timestep, timestep_callback=callback, loop=True)