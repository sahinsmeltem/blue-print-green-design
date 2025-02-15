from cmu_graphics import *
from building_components import *
from web_scraping import *
import webbrowser
from screens import *
from utils import *

def onAppStart(app):
    initializeHomeScreen(app)
    app.gallery = Gallery()

    app.textSizeHead = 24
    app.textSize = 16
    app.textSizeSmall = 12
    app.scaleFactor = 0.1

    app.currentComponent = None
    app.thermalData = fetchFilteredThermalData()
    app.materialRValueDict = dict()
    for dictionary in app.thermalData:
        app.materialRValueDict[dictionary['Material']] = float(dictionary['Conductivity (W/m·K)'])

    reset(app)

def reset(app):
    initilaizeBuilding(app)

    app.cx = None 
    app.cy = None
    app.pageHistory = []

    dropdownWidth = 200
    dropdownHeight = 200
    app.dropdownMenu = dropdownMenu(app.thermalData, (app.width/2 + 150), (app.height/2 + 50), dropdownWidth, dropdownHeight, 200, 50)

    app.hx = None
    app.hy = None
    
def initilaizeBuilding(app):
    stdWallHeight = 250
    app.building = Building(2000,2000,stdWallHeight) # default building
    app.heatingDegreeDays65F = 1500 # default HDD

    app.addWindow = False
    app.addDoor = False
    app.addRoom = False
    app.roomX = None
    app.roomY = None

    stdWallWidth = 25
    stdWallUValue = 1.0
    w0 = Wall(app.building.width, app.building.height, stdWallWidth, stdWallUValue, app.width/2-app.building.width/2, app.height/2-app.building.height/2) # top wall, left point
    w1 = Wall(app.building.length, app.building.height, stdWallWidth, stdWallUValue, app.width/2+app.building.width/2, app.height/2-app.building.height/2) # right wall, top point
    w2 = Wall(app.building.width, app.building.height, stdWallWidth, stdWallUValue, app.width/2-app.building.width/2, app.height/2+app.building.height/2) # bottom wall, left point
    w3 = Wall(app.building.length, app.building.height, stdWallWidth, stdWallUValue, app.width/2-app.building.width/2, app.height/2-app.building.height/2) # left wall, top point
    app.building.walls = [w0,w1,w2,w3]

    stdFloorHeigth = 15
    stdFloorUValue = 1.5
    stdRoofHeigth = 20
    stdRoofUValue = 0.15
    floor = Floor(app.building.length, stdFloorHeigth, app.building.width, stdFloorUValue)
    roof = Roof(app.building.length, stdRoofHeigth, app.building.width, stdRoofUValue)
    app.building.floors = [floor]
    app.building.roofs = [roof]
    

def initializeHomeScreen(app):
    app.screen= 'home'
    app.fill = 'mediumblue'
    app.secondFill = 'white'
    app.font = 'monospace'
    app.instruction = ('''WHAT
BLUE PRINT GREEN DESIGN is an interactive app for anyone who wants to create and
visualize simple building plans in 2D, calculate and visualize their heat loss,
and get energy analysis for each component to make informed decisions to improve energy efficiency.

                       
HOW
ALWAYS FOLLOW THE LABEL SHORTCUTS! (e.g. 0,1,2,3,w,g,f,r)
- Click on the screen to recalculate and print heat loss of the building.
- Use the keys 0, 1, 2, 3 to navigate between the screens.
- 0. HOME: Choose to draw, detail, or calculate a new building or continue from the saved projects in Gallery.
- 1. DRAW: Create a building plan by adding walls, windows, doors, and rooms.
- 2. DETAIL: Input U-values or enter layers of each building component.
- 3. CALCULATE: Get heat loss calculations, retrofit suggestions, energy report.
''')


########################################################
# DRAWING 
########################################################

def redrawAll(app):
    drawBg(app)
    if app.screen == 'home':
        draw0HomeScreen(app)
        app.gallery.draw()
    elif app.screen == 'draw':
        draw1DrawScreen(app)
        if app.building != None:
            app.building.drawBuilding()
            app.building.drawMeasureLines()
        if len(app.building.rooms) > 0:
            drawRooms(app)
        if len(app.building.windows) > 0:
            drawWindows(app)
        if len(app.building.doors) > 0:
            drawDoors(app)
        
    elif app.screen == 'detail':
        draw2DetailScreen(app)
    elif app.screen == 'calculate':
        draw3CalculateScreen(app)
    elif app.screen == 'detailWalls':
        drawDetailWallsScreen(app)
    elif app.screen == 'detailWindows':
        drawDetailWindowsScreen(app)
    elif app.screen == 'detailDoors':
        drawDetailDoorsScreen(app)
    elif app.screen == 'detailFloor':
        drawDetailFloorsScreen(app)
    elif app.screen == 'detailRoof':
        drawDetailRoofsScreen(app)
    
def drawWindows(app):
    for window in app.building.windows:
        if window.type != None:
            window.draw()
                
def drawDoors(app):
    for door in app.building.doors:
        if door.type != None:
            door.draw()

def drawRooms(app):
    for room in app.building.rooms:
        room.draw()

########################################################
# MOUSE AND KEY EVENTS 
########################################################

def onKeyPress(app, key):
    if key == '0':
        app.screen = 'home'
    elif key == '1':
        app.screen = 'draw'
    elif key == '2':
        app.screen = 'detail'
    elif key == '3':
        app.screen = 'calculate'

    if app.screen == 'detail':
        if key == 'w':
            app.screen = 'detailWalls'
        elif key == 'g':
            app.screen = 'detailWindows'
        elif key == 'd':
            app.screen = 'detailDoors'
        elif key == 'f':
            app.screen = 'detailFloor'
        elif key == 'r':
            app.screen = 'detailRoof'

        
def onMouseMove(app, mouseX, mouseY):
    app.hx = mouseX
    app.hy = mouseY

def onMousePress(app, mouseX, mouseY):
    updateAppHeatLossCalculations(app)
    app.cx = mouseX
    app.cy = mouseY

    if app.pageHistory == []:
        app.pageHistory.append(app.screen)
    elif app.pageHistory[-1] != app.screen:
        app.pageHistory.append(app.screen)

    if app.screen == 'home':
        handleClickHomeScreen(app, mouseX, mouseY)
    elif app.screen == 'draw':
        handleClickDrawScreen(app, mouseX, mouseY)
    elif app.screen == 'detail':
        handleClickDetailScreen(app, mouseX, mouseY)
    elif app.screen == 'calculate':
        handleClickCalculateScreen(app, mouseX, mouseY)
    elif app.screen == 'detailWalls':
        app.currentComponent = app.building.walls
        handleClickDetailWallsScreen(app, mouseX, mouseY)
        app.dropdownMenu.handleClick(mouseX, mouseY)
    elif app.screen == 'detailWindows':
        handleClickDetailWindowsScreen(app, mouseX, mouseY)
        app.dropdownMenu.handleClick(mouseX, mouseY)
    elif app.screen == 'detailDoors':
        handleClickDetailDoorsScreen(app, mouseX, mouseY)
        app.dropdownMenu.handleClick(mouseX, mouseY)
    elif app.screen == 'detailFloor':
        handleClickDetailFloorScreen(app, mouseX, mouseY)
        app.dropdownMenu.handleClick(mouseX, mouseY)
    elif app.screen == 'detailRoof':
        handleClickDetailRoofScreen(app, mouseX, mouseY)
        app.dropdownMenu.handleClick(mouseX, mouseY)

def handleClickHomeScreen(app, mouseX, mouseY):
    if mouseY > app.height/2 and mouseY < app.height/2 + 50:
            if mouseX > 0 and mouseX < app.width/3 :
                app.screen = 'draw'
            elif mouseX > app.width/3 and mouseX < 2*app.width/3:
                app.screen = 'detail'
            elif mouseX > 2*app.width/3:
                app.screen = 'calculate'

    if mouseY > 750 and mouseY < 950:
        for i in range(len(app.gallery.items)):
            if mouseX > 50 + i*app.gallery.galleryStep and mouseX < 50 + (i+1)*app.gallery.galleryStep:
                app.building = app.gallery.items[i]
                app.screen = 'draw'
    
    if mouseY > (app.height/1.6)+20 and mouseY < app.height/1.6 + 30:
            app.gallery.items = []

def handleClickDrawScreen(app, mouseX, mouseY):   
    # top buttons 
    if mouseY > 0 and mouseY < 50:
        if mouseX > 0 and mouseX < app.width/5:
             app.building.name = app.getTextInput('Enter project name: ')

        elif mouseX > app.width/5 and mouseX < 2*app.width/5:
            app.building.location = app.getTextInput('Enter location: ')

        elif mouseX > 2*app.width/5 and mouseX < 3*app.width/5:
            inputConsent = app.getTextInput('Do you want to be directed to degreedays.net? (y/n)')
            if inputConsent.lower() == 'y':
                    webbrowser.open("https://www.degreedays.net/")
            inputHDD = app.getTextInput('Enter the heating degree days of the location: ')
            if inputHDD != '' and inputHDD.isdigit():
                app.heatingDegreeDays65F = int(inputHDD)
            else:
                app.showMessage('Invalid input. Try again with digits or the default value will be used.')
            
        elif mouseX > 3*app.width/5 and mouseX < 4*app.width/5:
            inputHeight = app.getTextInput('Enter building height (Between 100-1000cm): ')
            if isValidHeight(app, inputHeight):
                app.building.height = int(inputHeight)                
        elif mouseX > 4*app.width/5:
            inputLength = app.getTextInput('Enter building length (Between 500-6000cm): ')
            if isValidDimension(app, inputLength):
                app.building.length= int(inputLength)
                app.building.scaledLength = app.building.length * app.scaleFactor

            inputWidth = app.getTextInput('Enter building width (Between 500-6000cm): ')
            if isValidDimension(app, inputWidth):
                app.building.width = int(inputWidth)
                app.building.scaledWidth = app.building.width * app.scaleFactor
            if isValidDimension(app, inputLength) and isValidDimension(app, inputWidth):
                stdWallWidth = 25
                stdWallUValue = 0.2
                w0 = Wall(app.building.width, app.building.height, stdWallWidth, stdWallUValue, app.width/2-app.building.width/2, app.height/2-app.building.height/2) # top wall, left point
                w1 = Wall(app.building.length, app.building.height, stdWallWidth, stdWallUValue, app.width/2+app.building.width/2, app.height/2-app.building.height/2) # right wall, top point
                w2 = Wall(app.building.width, app.building.height, stdWallWidth, stdWallUValue, app.width/2-app.building.width/2, app.height/2+app.building.height/2) # bottom wall, left point
                w3 = Wall(app.building.length, app.building.height, stdWallWidth, stdWallUValue, app.width/2-app.building.width/2, app.height/2-app.building.height/2) # left wall, top point
                app.building.walls = [w0,w1,w2,w3]

                stdFloorHeigth = 15 # thickness
                stdFloorUValue = 0.2

                stdRoofHeigth = 20
                stdRoofUValue = 1.0
                floor = Floor(app.building.length, stdFloorHeigth, app.building.width, stdFloorUValue)
                roof = Roof(app.building.length, stdRoofHeigth, app.building.width, stdRoofUValue)
                app.building.floors = [floor]
                app.building.roofs = [roof]

                app.building.rooms = []
                app.building.windows = []
                app.building.doors = []
 
    # +add window,door,room buttons
    if mouseY > 50 and mouseY < 100:
        if mouseX > 0 and mouseX < app.width/3:
            app.addWindow = True
            app.addDoor = False
        elif mouseX > app.width/3 and mouseX < 2*app.width/3:
            app.addDoor = True
            app.addWindow = False
        elif mouseX > 2*app.width/3:
            app.addRoom = True
            app.addDoor = False
            app.addWindow = False
            app.showMessage('To draw the room, click on the top-left corner and then on the bottom-right corner of the room.')
    
    if isMouseClickOnTheWall(app):
        snappedX, snappedY = snapToWall(app, mouseX, mouseY)
        if app.addWindow:
            stdWindowLenght = 150
            stdWindowHeight = 180
            stdWindowUValue = 5.8
            newWindow = Window(stdWindowLenght,stdWindowHeight,stdWindowUValue, snappedX, snappedY)
            app.building.windows.append(newWindow)
            newWindow.type = classifyComponentAllignment(app)

        if app.addDoor:
            stdDoorLength = 180
            stdDoorHeight = 210
            stdDoorUValue = 4.0
            newDoor = Door(stdDoorLength,stdDoorHeight,stdDoorUValue, snappedX, snappedY)
            app.building.doors.append(newDoor)
            newDoor.type = classifyComponentAllignment(app)


    if isMouseClickNearWall(app): # within a rectangle of border + margin
        if app.addRoom:
            if app.roomX == None: # first click - left-top
                app.roomX, app.roomY = mouseX, mouseY
                app.roomX, app.roomY = snapToWall(app, app.roomX, app.roomY)
    
            elif app.roomX != None: # second click - right-bottom
                roomWidth = abs(mouseX - app.roomX)
                roomHeight = abs(mouseY - app.roomY)

                inputRoomName = app.getTextInput('Enter room name: ')
                roomName = f'Room {len(app.building.rooms) + 1}' if inputRoomName == '' else inputRoomName

                inputHeated = app.getTextInput('Is the room heated? (y/n)')
                if inputHeated.lower() == 'y':
                    isHeated = True
                elif inputHeated.lower() == 'n':
                    isHeated = False
                else:
                    isHeated = False
                    app.showMessage('Invalid input. Room is not heated by default.')

                left = min(app.roomX, mouseX)
                top = min(app.roomY, mouseY)

                newRoom = Room(left, top, roomWidth, roomHeight, roomName, isHeated)
                app.building.rooms.append(newRoom)

                w1 = Wall(newRoom.width, app.building.height, 25, 0.2, newRoom.x, newRoom.y) # top wall
                w2 = Wall(newRoom.height, app.building.height, 25, 0.2, newRoom.x + newRoom.width, newRoom.y) # right wall
                w3 = Wall(newRoom.width, app.building.height, 25, 0.2, newRoom.x, newRoom.y + newRoom.height) # bottom wall
                w4 = Wall(newRoom.height, app.building.height, 25, 0.2, newRoom.x, newRoom.y) # left wall
                app.building.interiorWalls += w1,w2,w3,w4

                app.roomX = None
                app.roomY = None
                app.addRoom = False
            
    # bottom2 buttons:
    if mouseY > app.height-100:
        if mouseX > 0 and mouseX < app.width/5:
            if len(app.building.windows) > 0:
                app.building.windows.pop()
        elif mouseX > app.width/5 and mouseX < 2*app.width/5:
            if len(app.building.doors) > 0:
                app.building.doors.pop()
        elif mouseX > 2*app.width/5 and mouseX < 3*app.width/5:
            if len(app.building.rooms) > 0:
                app.building.rooms.pop()
        elif mouseX > 3*app.width/5 and mouseX < 4*app.width/5:
            navigateBack(app)
        elif mouseX > 4*app.width/5:
            app.screen = 'detail'
            
    # bottom buttons
    if mouseY > app.height-50:
        if mouseX > 0 and mouseX < app.width/3:
            reset(app)
        elif mouseX > app.width/3 and mouseX < 2*app.width/3:
            app.building.save()
            app.screen = 'home'
            reset(app)
        elif mouseX > 2*app.width/3:
            app.screen = 'home' # or go to screen "home"?

def isMouseClickOnTheWall(app): # T/F
    wallWidth = 15

    halfLength = (app.building.scaledLength)/2
    halfWidth = (app.building.scaledWidth)/2

    outerLeft = app.width/2 - halfWidth
    outerRight = app.width/2 + halfWidth
    outerTop = app.height/2 - halfLength
    outerBottom = app.height/2 + halfLength

    innerLeft = app.width/2 - halfWidth + wallWidth
    innerRight = app.width/2 + halfWidth - wallWidth
    innerTop = app.height/2 - halfLength + wallWidth
    innerBottom = app.height/2 + halfLength - wallWidth

    return ((outerLeft <= app.cx <= outerRight and outerTop <= app.cy <= outerBottom) and 
        not (innerLeft <= app.cx <= innerRight and innerTop <= app.cy <= innerBottom))

def snapToWall(app, xCoor, yCoor):
    buildingLeft = app.width/2 - app.building.scaledWidth/2 + 15/2
    buildingTop = app.height/2 - app.building.scaledLength/2 + 15/2
    buildingRight = app.width/2 + app.building.scaledWidth/2 - 15/2
    buildingBottom = app.height/2 + app.building.scaledLength/2 - 15/2

    margin = 10
    if abs(xCoor - buildingLeft) < margin:
        xCoor = buildingLeft
    elif abs(xCoor - buildingRight) < margin:
        xCoor = buildingRight
    if abs(yCoor - buildingTop) < margin:
        yCoor = buildingTop
    elif abs(yCoor - buildingBottom) < margin:
        yCoor = buildingBottom
    return xCoor, yCoor


def isMouseClickNearWall(app):
    margin = 10
    
    offsetLeft = app.width/2 - (app.building.scaledWidth)/2 - margin
    offsetRight = app.width/2 + (app.building.scaledWidth)/2 + margin
    offsetTop = app.height/2 - (app.building.scaledLength)/2 - margin
    offsetBottom = app.height/2 + (app.building.scaledLength)/2 + margin

    return (offsetLeft <= app.cx <= offsetRight and offsetTop <= app.cy <= offsetBottom)

def classifyComponentAllignment(app): # vertical, horizontal, None
    wallWidth = 15

    halfLength = (app.building.scaledLength)/2
    halfWidth = (app.building.scaledWidth)/2

    innerLeft = app.width/2 - halfWidth + wallWidth
    innerRight = app.width/2 + halfWidth - wallWidth
    innerTop = app.height/2 - halfLength + wallWidth
    innerBottom = app.height/2 + halfLength - wallWidth

    if app.cx < innerLeft: # vertical or horizontal allignment
        return "verticalLeft" 
    elif app.cx > innerRight:
        return "verticalRight"
    elif app.cy < innerTop:
        return "horizontalTop"
    elif app.cy > innerBottom:
        return "horizontalBottom"
     
    return None

def handleClickDetailScreen(app, mouseX, mouseY):
    # middle component buttons
    if mouseY > app.height/2 and mouseY < app.height/2 + 50:
        if mouseX > 0 and mouseX < app.width/5:
            app.screen = 'detailWalls'
        elif mouseX > app.width/5 and mouseX < 2*app.width/5:
            app.screen = 'detailWindows'
        elif mouseX > 2*app.width/5 and mouseX < 3*app.width/5:
            app.screen = 'detailDoors'
        elif mouseX > 3*app.width/5 and mouseX < 4*app.width/5:
            app.screen = 'detailFloor'
        elif mouseX > 4*app.width/5 and mouseX < app.width:
            app.screen = 'detailRoof'
    
    # bottom buttons
    if mouseY > app.height-50:
        if mouseX > 0 and mouseX < app.width/4:
            reset(app)
        elif mouseX > app.width/4 and mouseX < app.width/2:
            app.screen = 'home'
        elif mouseX > app.width/2 and mouseX < 3*app.width/4:
            navigateBack(app)
        elif mouseX > 3*app.width/4:
            app.screen = 'calculate'

def handleClickDetailWallsScreen(app, mouseX, mouseY):
    # top buttons
    if mouseY > 0 and mouseY < 50:
        if mouseX > 0 and mouseX < app.width/4:
            navigateBack(app)
        elif mouseX > app.width/4 and mouseX < app.width/2:
            app.building.wallsLayers = []
            app.building.wallsRValue = []
        elif mouseX > app.width/2 and mouseX < 3*app.width/4:
            app.building.wallsLayers.pop()
            app.building.wallsRValue.pop()
        elif mouseX > 3*app.width/4:
            app.screen = 'detailWindows'

    # middle buttons
    if mouseY > app.height/2 and mouseY < app.height/2 + 50:
        if mouseX > 0 and mouseX < app.width/2:
            app.building.wallsRValue = pythonRound(1/float(app.getTextInput('Enter the U-Value of the walls: ')),2)
            app.building.calculateTotalHeatLossCoefficient()
            app.building.calculateSiteEUI() 
            app.building.calculateTotalHeatLossCoefficientPerComponent()
        elif mouseX > app.width:
            app.building.calculateTotalHeatLossCoefficient()
            app.building.calculateSiteEUI() 
            app.building.calculateTotalHeatLossCoefficientPerComponent()    

def handleClickDetailWindowsScreen(app, mouseX, mouseY):
    # top buttons   
    if mouseY > 0 and mouseY < 50:
        if mouseX > 0 and mouseX < app.width/4:
            navigateBack(app)
        elif mouseX > app.width/4 and mouseX < app.width/2:
            app.building.windowsLayers = []
            app.building.windowsRValue = []
        elif mouseX > app.width/2 and mouseX < 3*app.width/4:
            app.building.windowsLayers.pop()
            app.building.windowsRValue.pop()
        elif mouseX > 3*app.width/4:
            app.screen = 'detailDoors'
    
    # middle buttons
    if mouseY > app.height/2 and mouseY < app.height/2 + 50:
        if mouseX > 0 and mouseX < app.width/2:
            app.building.windowsRValue = pythonRound(1/float(app.getTextInput('Enter the U-Value of the windows: ')),2)
            app.building.calculateTotalHeatLossCoefficient()
            app.building.calculateSiteEUI() 
            app.building.calculateTotalHeatLossCoefficientPerComponent()
        elif mouseX > app.width:
            app.building.calculateTotalHeatLossCoefficient()
            app.building.calculateSiteEUI() 
            app.building.calculateTotalHeatLossCoefficientPerComponent()     

def handleClickDetailDoorsScreen(app, mouseX, mouseY):
    # top buttons
    if mouseY > 0 and mouseY < 50:
        if mouseX > 0 and mouseX < app.width/4:
            navigateBack(app)
        elif mouseX > app.width/4 and mouseX < app.width/2:
            app.building.doorsLayers = []
            app.building.doorsRValue = []
        elif mouseX > app.width/2 and mouseX < 3*app.width/4:
            app.building.doorsLayers.pop()
            app.building.doorsRValue.pop()
        elif mouseX > 3*app.width/4:
            app.screen = 'detailFloor'

    # middle buttons
    if mouseY > app.height/2 and mouseY < app.height/2 + 50:
        if mouseX > 0 and mouseX < app.width/2:
            app.building.doorsRValue = pythonRound(1/float(app.getTextInput('Enter the U-Value of the doors: ')),2)
            app.building.calculateTotalHeatLossCoefficient()
            app.building.calculateSiteEUI() 
            app.building.calculateTotalHeatLossCoefficientPerComponent()
        elif mouseX > app.width:
            app.building.calculateTotalHeatLossCoefficient()
            app.building.calculateSiteEUI() 
            app.building.calculateTotalHeatLossCoefficientPerComponent()    

def handleClickDetailFloorScreen(app, mouseX, mouseY):
    # top buttons
    if mouseY > 0 and mouseY < 50:
        if mouseX > 0 and mouseX < app.width/4:
            navigateBack(app)
        elif mouseX > app.width/4 and mouseX < app.width/2:
            app.building.floorsLayers = []
            app.building.floorsRValue = []
        elif mouseX > app.width/2 and mouseX < 3*app.width/4:
            app.building.floorsLayers.pop()
            app.building.floorsRValue.pop()
        elif mouseX > 3*app.width/4:
            app.screen = 'detailRoof'
    
    # middle buttons
    if mouseY > app.height/2 and mouseY < app.height/2 + 50:
        if mouseX > 0 and mouseX < app.width/2:
            app.building.floorsRValue = pythonRound(1/float(app.getTextInput('Enter the U-Value of the floors: ')),2)
            app.building.calculateTotalHeatLossCoefficient()
            app.building.calculateSiteEUI() 
            app.building.calculateTotalHeatLossCoefficientPerComponent()
        elif mouseX > app.width:
            app.building.calculateTotalHeatLossCoefficient()
            app.building.calculateSiteEUI() 
            app.building.calculateTotalHeatLossCoefficientPerComponent()    

def handleClickDetailRoofScreen(app, mouseX, mouseY):
    # top buttons
    if mouseY > 0 and mouseY < 50:
        if mouseX > 0 and mouseX < app.width/4:
            navigateBack(app)
        elif mouseX > app.width/4 and mouseX < app.width/2:
            app.building.roofsLayers = []
            app.building.roofsRValue = []
        elif mouseX > app.width/2 and mouseX < 3*app.width/4:
            app.building.roofsLayers.pop()
            app.building.roofsRValue.pop()
        elif mouseX > 3*app.width/4:
            app.screen = 'calculate'

    # middle buttons
    if mouseY > app.height/2 and mouseY < app.height/2 + 50:
        if mouseX > 0 and mouseX < app.width/2:
            app.building.roofsRValue = pythonRound(1/float(app.getTextInput('Enter the U-Value of the roofs: ')),2)
            app.building.calculateTotalHeatLossCoefficient()
            app.building.calculateSiteEUI() 
            app.building.calculateTotalHeatLossCoefficientPerComponent()
        elif mouseX > app.width:
            app.building.calculateTotalHeatLossCoefficient()
            app.building.calculateSiteEUI() 
            app.building.calculateTotalHeatLossCoefficientPerComponent()     


def handleClickCalculateScreen(app, mouseX, mouseY):
    # bottom buttons
    if mouseY > app.height-50:
        if mouseX > 0 and mouseX < app.width/4:
            reset(app)
        elif mouseX > app.width/4 and mouseX < app.width/2:
            app.screen = 'home'
        elif mouseX > app.width/2 and mouseX < 3*app.width/4:
            app.screen = 'detail'
        elif mouseX > 3*app.width/4:
            app.building.save()
            app.screen = 'home'
            reset(app)

def main():
    runApp(width=1080, height=1080)
main()

