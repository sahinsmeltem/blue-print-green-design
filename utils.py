# Some helper functions and auxilary implementations, such as unit conversion,
# data validation/formatting, Buttons, Gallery etc

from cmu_graphics import *

########################################################
#################### DATA VALIDATION ###################
########################################################

def isValidDimension(app, dimension):
    if not dimension.isdigit() or dimension == None or int(dimension) < 100 or int(dimension) > 500:
        app.showMessage('Invalid dimension. Please enter a value between 100-500.')
        return False
    return True

def isValidHeight(app, dimension):
    if not dimension.isdigit() or dimension == None or int(dimension) < 6 or int(dimension) > 35:
        app.showMessage('Invalid dimension. Please enter a value between 0-10!')
        return False
    return True

def hasAllParametersSet(app):
    if isValidDimension(app.building.length) and isValidDimension(app.building.width):
        return app.building.name and app.building.location and app.buidling.height
    return False

def castCmToMeter(app, dimension):
    return dimension * 100

########################################################
################ HEAT LOSS CALCULATIONS ################
########################################################

def calculateSharedWallArea(room, otherRoom): # WRONG!
        sharedWallArea = 0
        for wall in room.walls:
            if wall in otherRoom.walls:
                sharedWallArea += wall.calculateArea()
        return sharedWallArea


########################################################
##################### UI COMPONENTS ####################
########################################################

class Button:
    def __init__(self, top, buttonNum, buttonStep, buttonHeight, text):
        self.buttonNum = buttonNum
        self.buttonStep = buttonStep
        self.buttonHeight = buttonHeight
        self.text = text
        self.top = top

    def draw(self):
        for i in range(self.buttonNum):
            drawRect(i*self.buttonStep,self.top, self.buttonStep,
                    self.buttonHeight , border = 'white', borderWidth = 1, fill = 'white', opacity = 40)
            drawLabel(self.text[i], (i+0.5)*self.buttonStep, self.top + self.buttonHeight/2,
                        font = 'monospace', fill='white', bold = True, size = 16)
        
    def mouseOver(self,i):
        if app.cx != None and app.cy != None:
            if (app.cx > i*self.buttonStep and app.cx < (i+1)*self.buttonStep and
                        app.cy > self.top and app.cy < self.top + self.buttonHeight):
                app.mouseOverButton = True
                return True
        return False

class Gallery:
    def __init__(self):
        self.items = []
        self.padding = 50
        self.width = 200
        self.length = 200
        self.top = 700
    
    def updateProjectCount(self):
        self.projectCount = len(self.items) # num
        self.galleryStep = (app.width - self.padding*2) / self.projectCount if self.projectCount > 0 else 0 # step

    def draw(self):
        self.updateProjectCount()
        for i in range(self.projectCount):
            drawRect(i*(self.galleryStep) + self.padding, self.top, self.width, self.length, fill = None, border = 'white', borderWidth = 1)
            
            currBuilding = self.items[i]
            newBuilding = currBuilding.createScaledBuildingIcon()

            center = (i*self.galleryStep + self.padding + self.width/2, self.top + self.length/2)
            newBuilding.drawToPlace(center)
            
            cx, cy = center
            drawLabel(currBuilding.name, cx, cy+120, fill = 'white', bold = True, size = 16)
            drawLabel(currBuilding.location, cx, cy+140, fill = 'white', size = 12)
            drawLabel(f'{currBuilding.annualHeatLoss} MMBTU', cx, cy+155, fill = 'white', size = 12)
    
    def mouseOver(self,i):
        self.updateProjectCount()
        if app.cx != None and app.cy != None:
            return (app.cx > i*self.galleryStep and app.cx < (i+1)*self.galleryStep and
                        app.cy > self.top and app.cy < self.top + self.length)
    

def navigateBack(app):
    if len(app.pageHistory) > 1:
        app.pageHistory.pop()
        app.screen = app.pageHistory[-1]

def navigateForward(app):
    pass


class dropdownMenu:
    def __init__(self, items, x, y, width, height, buttonWidth, buttonHeight):
        self.items = items
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.buttonWidth = buttonWidth
        self.buttonHeight = buttonHeight

        self.currStartIdx = 0
        self.elementsPerPage = 6

    def draw(self):
        currPageItems = self.items[self.currStartIdx:self.currStartIdx+self.elementsPerPage]
        for i in range(len(currPageItems)):
            item = currPageItems[i]
            drawRect(self.x, self.y + i*self.buttonHeight, self.buttonWidth, self.buttonHeight, fill='white', border='white', borderWidth=1, opacity = 20)
            drawLabel(item['Material'], self.x + self.buttonWidth/2, self.y + i*self.buttonHeight + self.buttonHeight/2, fill='white', size=app.textSizeSmall, font=app.font, align='center', bold = True)
        
        # navi buttons
        buttonSize = self.buttonHeight
        drawRect(self.x + self.width, self.y, buttonSize, buttonSize, fill='white', border='white', borderWidth=1, opacity = 20)
        drawLabel('↑', self.x + self.width + buttonSize/2, self.y + buttonSize/2, fill='white', size=app.textSizeHead, align='center', bold = True)
        drawRect(self.x + self.width, self.y + buttonSize, buttonSize, buttonSize, fill='white', border='white', borderWidth=1, opacity = 20)
        drawLabel('↓', self.x + self.width + buttonSize/2, self.y + buttonSize + buttonSize/2, fill='white', size=app.textSizeHead, align='center', bold = True)

    
    def handleClick(self, mouseX, mouseY):
        if mouseX > self.x + self.width and mouseX < self.x + self.width + self.buttonWidth:
            if mouseY > self.y and mouseY < self.y + self.buttonHeight:
                if self.currStartIdx > 0:
                    self.currStartIdx -= 1
            elif mouseY > self.y + self.buttonHeight and mouseY < self.y + self.buttonHeight*2:
                if self.currStartIdx < len(self.items) - self.elementsPerPage:
                    self.currStartIdx += 1

        if mouseX > self.x and mouseX < self.x + self.buttonWidth:
            currPageItems = self.items[self.currStartIdx:self.currStartIdx+self.elementsPerPage]
            for i in range(len(currPageItems)):
                if mouseY > self.y + i*self.buttonHeight and mouseY < self.y + (i+1)*self.buttonHeight:
                    itemRValue = pythonRound(1/(float(currPageItems[i]['Conductivity (W/m·K)'])), 2) # isDigit?
                    if app.screen == 'detailWalls':
                        if isinstance(app.building.wallsRValue, list):
                            app.building.wallsLayers.append(currPageItems[i]['Material'])
                            app.building.wallsRValue.append(itemRValue) # append the selected item conductivity
                    elif app.screen == 'detailWindows':
                        if isinstance(app.building.windowsRValue, list):
                            app.building.windowsLayers.append(currPageItems[i]['Material'])
                            app.building.windowsRValue.append(itemRValue)
                    elif app.screen == 'detailDoors':
                        if isinstance(app.building.doorsRValue, list):
                            app.building.doorsLayers.append(currPageItems[i]['Material'])
                            app.building.doorsRValue.append(itemRValue)
                    elif app.screen == 'detailFloor':
                        if isinstance(app.building.floorsRValue, list):
                            app.building.floorsLayers.append(currPageItems[i]['Material'])
                            app.building.floorsRValue.append(itemRValue)
                    elif app.screen == 'detailRoof':
                        if isinstance(app.building.roofsRValue, list):
                            app.building.roofsLayers.append(currPageItems[i]['Material'])
                            app.building.roofsRValue.append(itemRValue)

class TableCol:
    def __init__(self, items, x, y, width, height, rowWidth, rowHeight):
        self.items = items
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rowWidth = rowWidth
        self.rowHeight = rowHeight

        self.currStartIdx = 0
        self.elementsPerPage = 8

    def draw(self):
        for i in range(len(self.items)):
            item = self.items[i]
            drawRect(self.x, self.y + i*self.rowHeight, self.rowWidth, self.rowHeight, fill=None, border='white', borderWidth=1)
            drawLabel(item, self.x + self.rowWidth/2, self.y + i*self.rowHeight + self.rowHeight/2, fill='white', size=app.textSize, font=app.font, align='center', bold = True)

# class Icon:
#     def __init__(self, r, origin, name=None, lineColor='white', lineWidth=1):
#         self.r = r
#         self.origin = origin
#         self.name = name
#         self.lineColor = lineColor
#         self.lineWidth = lineWidth
    
#     def draw(self, app):
#         lineColor, fillColor = 'white'
#         cx, cy = self.origin
#         r = self.r
#         if self.name == 'Forward Arrow':
#             drawLabel(cx,cy-r, text='→', fill=lineColor, 
#                                         font=app.font)
#             drawLabel(cx,cy+r, text='F', fill=lineColor, 
#                                         font=app.font)
#         elif self.name == 'Backward Arrow':
#             drawLabel(cx,cy-r, text='←', fill=lineColor, 
#                                         font=app.font)
#             drawLabel(cx,cy+r, text='B', fill=lineColor, 
#                                         font=app.font)
        
#         elif self.name == 'Help':
#             drawLabel(cx,cy, text='?', fill=lineColor, 
#                                         font=app.font)
#             drawCircle(cx,cy,r, fill=fillColor, border=lineColor, borderWidth=self.lineWidth)
#         elif self.name == 'Save':
#             pass
