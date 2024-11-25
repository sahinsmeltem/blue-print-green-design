# all screens here. draw funcs.
from cmu_graphics import *
from components import *
from utils import *


def drawBg(app):
    drawRect(0,0,app.width, app.height, fill = app.fill)

def draw0HomeScreen(app):    
    buttons = Button(app.height/2, 3, app.width/3, 50,['1."DRAW"', '2."DETAIL"', '3. "CALCULATE"'])
    buttons.draw()
    
    drawLabel('BLUE PRINT GREEN DESIGN', app.width/2, app.height/11, size=24, fill='white', bold=True, font=app.font)
    
    margin = 100
    for i in range(len(app.instruction.splitlines())):
        lines = app.instruction.splitlines()
        margin = 20
        drawLabel(lines[i], app.width/2, app.height/7 + margin*i, size=16, fill='white', bold=True, font=app.font)

    drawLabel('Press (1, 2, 3) or click on buttons to navigate.', app.width/2, app.height/2+75, size=16, fill='white', font=app.font, italic=True)
    drawLabel('GALLERY', app.width/2, app.height/1.6, size=24, fill='white', bold=True, font=app.font)

def draw1DrawScreen(app):
    buttonsTop = Button(0, 4, app.width/4, 50,['1.PROJECT NAME', '2.LOCATION', '3.HEIGHT', '4.DIMENSIONS'])
    buttonsTop2 = Button(50, 2, app.width/2, 50,['+ADD WINDOW', '+ADD DOOR'])
    buttonsBottom2 = Button(app.height-100, 4, app.width/4, 50,['UNDO WINDOW', 'UNDO DOOR', '← BACK', 'FORWARD →'])
    buttonsBottom = Button(app.height-50, 3, app.width/3, 50,['RESET', 'TOGGLE VIEW', '?'])
    buttonsTop.draw()
    buttonsTop2.draw()
    buttonsBottom.draw()
    buttonsBottom2.draw()

    
    drawLabel(f'PROJECT NAME: {app.building.name}', 25, 125, size=app.textSize, fill='white', bold=True, font=app.font, align='left')

    drawLabel(f'LOCATION: {app.building.location}', 25, 150, size=app.textSize, fill='white', bold=True, font=app.font, align='left')

    drawLabel(app.building, 25, app.height-125, size=app.textSize, fill='white', font=app.font, align='left')
    drawLabel(f'Current screen: {app.screen}', app.width-25, app.height-125, size=app.textSize, fill='white', font=app.font, align='right')


def draw2DetailScreen(app):
    buttonsTop = Button(app.height/2, 5, app.width/5, 50,['A. WALLS (W)', 'B. WINDOWS (G)', 'C. DOORS (D)', 'D. FLOOR (F)', 'E. ROOF (R)'])
    buttonsBottom2 = Button(app.height-100, 2, app.width/2, 50,['← BACK', 'FORWARD →'])
    buttonsBottom = Button(app.height-50, 3, app.width/3, 50,['RESET', 'SAVE', '?'])
    buttonsTop.draw()
    buttonsBottom.draw()
    buttonsBottom2.draw()
    
    drawLabel('Press (W, G, D, F, R) or click on buttons to navigate.', app.width/2, app.height/2 + 100, size=16, fill='white', font=app.font, italic=True)
    drawLabel(f'Current screen: {app.screen}', app.width-25, app.height-125, size=app.textSize, fill='white', font=app.font, align='right')
    

def drawDetailWallsScreen(app):
    buttonsTop = Button(0, 2, app.width/2, 50,['← BACK', 'FORWARD →'])
    buttonsTop.draw()

    drawLabel('WALLS (W)', app.width/2, app.height/10, size=24, fill='white', bold=True, font=app.font)
    drawLabel(f'Current screen: {app.screen}', app.width-25, app.height-125, size=app.textSize, fill='white', font=app.font, align='right')

def drawDetailWindowsScreen(app):
    buttonsTop = Button(0, 2, app.width/2, 50,['← BACK', 'FORWARD →'])
    buttonsTop.draw()

    drawLabel('WINDOWS (G)', app.width/2, app.height/10, size=24, fill='white', bold=True, font=app.font)

def drawDetailDoorsScreen(app):
    buttonsTop = Button(0, 2, app.width/2, 50,['← BACK', 'FORWARD →'])
    buttonsTop.draw()

    drawLabel('DOORS (D)', app.width/2, app.height/10, size=24, fill='white', bold=True, font=app.font)


def drawDetailFloorsScreen(app):
    buttonsTop = Button(0, 2, app.width/2, 50,['← BACK', 'FORWARD →'])
    buttonsTop.draw()
    
    drawLabel('FLOORS (F)', app.width/2, app.height/10, size=24, fill='white', bold=True, font=app.font)


def drawDetailRoofsScreen(app):
    buttonsTop = Button(0, 2, app.width/2, 50,['← BACK', 'FORWARD →'])
    buttonsTop.draw()

    drawLabel('ROOFS (R)', app.width/2, app.height/10, size=24, fill='white', bold=True, font=app.font)



def draw3CalculateScreen(app):
    drawLabel('TRANSMISSION LOSSES', app.width/2, app.height/8, size=24, fill='white', bold=True, font=app.font)
    buttonsBottom2 = Button(app.height-100, 2, app.width/2, 50,['← BACK', 'SAVE AND CLOSE'])
    buttonsBottom = Button(app.height-50, 3, app.width/3, 50,['RESET', 'SAVE', '?'])
    drawLabel('RETROFIT SUGGESTIONS', app.width/2, app.height-250, size=24, fill='white', bold=True, font=app.font)
    buttonsBottom.draw()
    buttonsBottom2.draw()

    drawLabel(f'Current screen: {app.screen}', app.width-25, app.height-125, size=app.textSize, fill='white', font=app.font, align='right')