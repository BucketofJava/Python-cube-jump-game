 
import pygame as pg
import time
import random
import math

from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
GREEN = (0, 255, 0)
def indicasdf(index):
  return (index-1)*2
class Cube():
  zpos=0
  xpos=0
  ypos=0
  speed=0
  def __init__(self, zpos, xpos, ypos, speed):
    self.zpos=zpos
    self.ypos=ypos
    self.xpos=xpos
    self.speed=speed
class platform():
  xindex=0
  yshift=0
  shift=False
  zposition=0
  render=True
  def __init__(self, yshift, shift, zposition, xindex):
    self.yshift=(yshift-1)/2
    self.render=(yshift!=0)
    self.shift=shift
    self.zposition=zposition
    self.xindex=xindex
#5.497787143782138
def genplatformarray():
    position = random.randint(0, 2)
    shift = False
    if position == 2:
        shift = (random.randint(0, 1) == 1)
    return position, shift


def convertcolor(color):
    return (color[0] / 255, color[1] / 255, color[2] / 255)


verticies = ((0.5, -0.5, -0.5), (0.5, 0.5, -0.5), (-0.5, 0.5, -0.5), (-0.5, -0.5, -0.5), (0.5, -0.5, 0.5),
             (0.5, 0.5, 0.5), (-0.5, -0.5, 0.5), (-0.5, 0.5, 0.5))
rectverts = ((1, -1, -1), (1, -0.5, -1), (-1, -0.5, -1), (-1, -1, -1),
             (1, -1, 1), (1, -0.5, 1), (-1, -1, 1), (-1, -0.5, 1))
edges = ((0, 1), (0, 3), (0, 4), (2, 1), (2, 3), (2, 7), (6, 3), (6, 4),
         (6, 7), (5, 1), (5, 4), (5, 7))
surfaces = ((0, 1, 2, 3), (3, 2, 7, 6), (6, 7, 5, 4), (4, 5, 1, 0),
            (1, 5, 7, 2), (4, 0, 3, 6))


def draw_cube(verts, color):
    glBegin(GL_QUADS)
    for surface in surfaces:
        glColor3fv((0, 0, 0))
        for vertex in surface:
            glColor3fv(color)
            glVertex3fv(verts[vertex])
    glEnd()
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glColor3fv((0, 0, 0))
            glVertex3fv(verts[vertex])
    glEnd()


x = 5
jumptime = 0
canJump = True
isJumping=False
isJumpingvalue=0
timeness=0
didsomething=False
sd=False
def game():
    global sd
    global didsomething
    global timeness
    global x
    global canJump
    global isJumping
    global isJumpingvalue
    platformarray=[]
    for i in range(5):
      platformarray1=genplatformarray()
      print(platformarray1[0])
      Platform=platform(platformarray1[0], False, -(5+3*i), indicasdf(0))
      platformarray2=genplatformarray()
      Platform2=platform(platformarray2[0], False, -(5+3*i), indicasdf(1))
      platformarray3=genplatformarray()
      Platform3=platform(platformarray3[0], False, -(5+3*i), indicasdf(2))
      if(Platform.render==False and Platform2.render==False and Platform3.render==False):
              Platform2.render=True
      platformarray.append(Platform)
      platformarray.append(Platform2)
      platformarray.append(Platform3)
    from GUI import get_cube_color
    from GUI import show_message, shift_pos
    pg.init()
    text_type_title = pg.font.Font("COMIC.TTF", 150)
    display = pg.display.set_mode((800, 800), DOUBLEBUF | OPENGL)
    glEnable(GL_DEPTH_TEST)
    gluPerspective(55, 1, 0.1, 50)
    glTranslatef(0, -1, -5)
    cube=Cube(0, 0, 0, 0)
    while True:
        didsomething=False
        falla=True;
        event = pg.event.poll()
        pg.event.pump()
        keys=pg.key.get_pressed()
        if isJumping:
          cube.ypos+=isJumpingvalue
        if event.type == pg.QUIT:
            quit()
            pg.quit()
        if keys[pg.K_UP] and canJump:
            cube.ypos+=0.4
            canJump=False
            isJumping=True
            isJumpingvalue=0.4+int(sd)/5
            didsomething=False
            sd=False
        elif keys[pg.K_LEFT] and cube.xpos>-2:
            cube.xpos-=0.5
        elif keys[pg.K_RIGHT] and cube.xpos<2:
            cube.xpos+=0.5
        
        platformys=[x.yshift for x in platformarray]
        for i in range(len(platformys)):
          if((platformys[i]+0.5>cube.ypos>platformys[i]-0.5) and platformarray[i].zposition+6>cube.zpos>platformarray[i].zposition+4 and platformarray[i].xindex+1>cube.xpos>platformarray[i].xindex-1):
            canJump=True
            isJumping=False
            didsomething=True
        if timeness>50:
          print(str(didsomething))
        if didsomething==False and timeness>50:
          isJumping=True
          canJump=False
        if isJumping:
          isJumpingvalue-=0.05
        
        if cube.ypos<-5:
         pg.quit()
         quit()
        elif cube.ypos<-2.5:
          platformzs=[x.zposition for x in platformarray]
          platformxs=[y.xindex for y in platformarray]
          if round(cube.zpos-1.5, 1) in platformzs:
            canJump=True
            sd=True
          elif round(cube.xpos-1.5, 1) in platformxs or round(cube.xpos+1.5, 1) in platformxs:
            canJump=True
            sd=True


        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        glRotatef(5, 90, 0, 0)
        glTranslatef(cube.xpos, cube.ypos, cube.zpos)
        draw_cube(verticies,convertcolor(get_cube_color()))
        glPopMatrix()
        for i in range(5): 
          shiftie=True
          glPushMatrix()
          glRotatef(10, 90, 0, 0)
          glTranslatef(platformarray[i*3].xindex,  platformarray[i*3].yshift, platformarray[i*3].zposition+5)
          platformarray[i*3].zposition+=0.1
          if platformarray[i*3].render==True:
            draw_cube(rectverts, GREEN)
          glPopMatrix()
          glPushMatrix()
          glRotatef(10, 90, 0, 0)
          glTranslatef(platformarray[(i*3)+1].xindex,  platformarray[(i*3)+1].yshift, platformarray[(i*3)+1].zposition+5)
          platformarray[(i*3)+1].zposition+=0.1
          if platformarray[(i*3)+1].render==True:
            draw_cube(rectverts, GREEN)
          glPopMatrix()
          glPushMatrix()
          glRotatef(10, 90, 0, 0)
          glTranslatef(platformarray[(i*3)+2].xindex,  platformarray[(i*3)+2].yshift, platformarray[(i*3)+2].zposition+5)
          platformarray[(i*3)+2].zposition+=0.1
          if platformarray[(i*3)+2].render==True:
            draw_cube(rectverts, GREEN)
          glPopMatrix()
          if platformarray[0].zposition>=cube.zpos and i==0:
            platformarray.remove(platformarray[0])
            platformarray.remove(platformarray[1])
            platformarray.remove(platformarray[2])
            platformarray1=genplatformarray()
            print(platformarray1[0])
            Platform=platform(platformarray1[0], False, -(5+3*4), indicasdf(0))
            platformarray2=genplatformarray()
            Platform2=platform(platformarray2[0], False, -(5+3*4), indicasdf(1))
            platformarray3=genplatformarray()
            Platform3=platform(platformarray3[0], False, -(5+3*4), indicasdf(2))
            if(Platform.render==False and Platform2.render==False and Platform3.render==False):
              Platform2.render=True
            platformarray.append(Platform)
            platformarray.append(Platform2)
            platformarray.append(Platform3)
            print(platformarray.index(Platform))
          

        pg.display.flip()
        time.sleep(0.1)
        timeness += 1
        print("Timenesscoutn")
        print(str(timeness))
        x += 0.1
