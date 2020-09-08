import pygame as pg 
import time
import openglstuff
pg.init()
display = pg.display.set_mode((800, 800))
pg.display.set_caption("Stuff")
RED=(255, 0, 0)
GREEN=(0, 255, 0)
currentcubecolorindex=-1
def ToggleColor(color):
    if color==RED:
      color=GREEN
    elif color==GREEN:
      color=RED
    return color
def ChangeLightness(rgb, percent):
    return (rgb[0] * percent, rgb[1] * percent, rgb[2] * percent)
def getTextObjects(textt, texttype, color):
    tsurface = texttype.render(textt, True, color)
    return tsurface, tsurface.get_rect()
def shift_pos(pos, axis, amound):
  pos=list(pos)
  pos[ord(axis.lower())-120]=pos[ord(axis.lower())-120]+amound
  return tuple(pos)
# Shows message on screen
def show_message(text, center, color, text_type, dsplay):
    tsurface, trect = getTextObjects(text, text_type, color)
    trect.center = center
    dsplay.blit(tsurface, trect)
    pg.display.update()
def get_cube_color():
  if(currentcubecolorindex==-1):
    return None
  elif currentcubecolorindex==0:
    return GREEN
  elif currentcubecolorindex==1:
    return (0, 0, 255)
  elif currentcubecolorindex==2:
    return RED
  elif currentcubecolorindex==3:
    return (255, 255, 0)
  elif currentcubecolorindex==4:
    return (255, 150, 0)
  elif currentcubecolorindex==5:
    return (200, 0, 200)
def runGUI():
  import main
  global currentcubecolorindex
  clk = pg.time.Clock()
  text_type_button = pg.font.Font("COMIC.TTF", 50)
  text_type_title = pg.font.Font("COMIC.TTF", 150)
  display.fill((0, 0, 0))
  class button:
      ulpos = []
      brpos = []
      color1 = (0, 0, 0)
      text = ""

      def __init__(self, ulpos, brpos, color1, text):
          self.ulpos = ulpos
          self.brpos = brpos
          self.color1 = color1
          self.text = text

      def Draw(self):
          Rect = pg.draw.rect(
              display, self.color1,
              (self.ulpos[0], self.ulpos[1], self.brpos[0] - self.ulpos[0],
              self.brpos[1] - self.ulpos[1]))
          pg.display.update()
          show_message(self.text, Rect.center, (0, 0, 0), text_type_button, display)

      def draw(self, color, text):
          self.color1=color
          self.text=text
          Rect = pg.draw.rect(
              display, color,
              (self.ulpos[0], self.ulpos[1], self.brpos[0] - self.ulpos[0],
              self.brpos[1] - self.ulpos[1]))
          pg.display.update()
          show_message(text, Rect.center, (0, 0, 0), text_type_button, display)

      def getText(self):
          return self.text

      def isOver(self, mousepos):
          mousepos = pg.mouse.get_pos()
          if (self.ulpos[0] <= mousepos[0] <= self.brpos[0]
                  and self.ulpos[1] <= mousepos[1] <= self.brpos[1]):
              Rect = pg.draw.rect(
                  display, ChangeLightness(self.color1, 0.75),
                  (self.ulpos[0], self.ulpos[1], self.brpos[0] - self.ulpos[0],
                  self.brpos[1] - self.ulpos[1]))
              pg.display.update()
              show_message(self.text, Rect.center, (0, 0, 0), text_type_button, display)
              return True
          else:
              Rect = pg.draw.rect(
                  display, self.color1,
                  (self.ulpos[0], self.ulpos[1], self.brpos[0] - self.ulpos[0],
                  self.brpos[1] - self.ulpos[1]))
              pg.display.update()
              show_message(self.text, Rect.center, (0, 0, 0), text_type_button, display)
              return False
  buttonstart = button(
      (display.get_rect().center[0] - 100, display.get_rect().center[0] + 150),
      (display.get_rect().center[0] + 100, display.get_rect().center[0] + 250),
      RED, "Start")

  colorbystring={"Purple":RED, "Green":RED, "Blue":RED, "Yellow":RED, "Red":RED, "Orange":RED}
  StartGamebutton=button((500, 700), (800, 800), (0, 255, 0), "Start Game") 
  buttoncolorarray=[]        
  for i in range(6):
    if (i>2):
      newbutton=button((400, 125+150*(i-2)), (650, 75+150*(i-1)), RED, "")
    else:
      newbutton=button((50, 125+150*(i+1)), (250, 75+150*(i+2)), RED, "")
    buttoncolorarray.append(newbutton)
  stage=1
  while main.getfeefifo():
    event=pg.event.poll()
    if event.type==pg.QUIT:
        quit()
        pg.quit()
    elif stage==1:
      buttonstart.Draw()
      show_message("Cube Jump", shift_pos(display.get_rect().center, 'x', -5), (255, 255, 255), text_type_title, display)
      if event.type==pg.MOUSEMOTION:
        buttonstart.isOver(pg.mouse.get_pos())
      elif event.type==pg.MOUSEBUTTONUP and buttonstart.isOver(pg.mouse.get_pos()):
        stage=2
        display.fill((0, 0, 0))
        pg.display.flip()
    elif stage==2:
      show_message("Choose a color", shift_pos(display.get_rect().center, 'y', -175), (255, 255, 255), text_type_button, display)
      StartGamebutton.Draw()
      buttoncolorarray[0].draw(colorbystring.get("Green"), "Green")
      buttoncolorarray[1].draw(colorbystring.get("Blue"), "Blue")
      buttoncolorarray[2].draw(colorbystring.get("Red"), "Red")
      buttoncolorarray[3].draw(colorbystring.get("Yellow"), "Yellow")
      buttoncolorarray[4].draw(colorbystring.get("Orange"), "Orange")
      buttoncolorarray[5].draw(colorbystring.get("Purple"), "Purple")
      if event.type==pg.MOUSEMOTION:
        for i in range(6):
          buttoncolorarray[i].isOver(pg.mouse.get_pos())
        StartGamebutton.isOver(pg.mouse.get_pos())
      elif event.type==pg.MOUSEBUTTONUP:
        indexclicked=-1
        for i in range(6):
          if (buttoncolorarray[i].isOver(pg.mouse.get_pos())): 
            indexclicked=i
        if indexclicked!=-1:
          colorbystring[buttoncolorarray[currentcubecolorindex*int(currentcubecolorindex!=-1)].getText()]=RED
          colorbystring[buttoncolorarray[indexclicked].getText()]=GREEN
          currentcubecolorindex=indexclicked
        elif StartGamebutton.isOver(pg.mouse.get_pos()) and currentcubecolorindex !=-1:
          stage=3
          main.setfeefifo(False)
          display.fill((0, 0, 0))
          pg.display.flip()
          pg.quit()
          openglstuff.game()
        elif StartGamebutton.isOver(pg.mouse.get_pos()):
          print("You need to select a color")
    time.sleep(0.2)  
