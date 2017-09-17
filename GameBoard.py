from tkinter import *

#taken from notes
def rgbString(red, green, blue):
    return "#%02x%02x%02x" % (red, green, blue)

class GameBoard(object):
    def __init__(self, data):
        #fixed board size 
        self.rows = 24
        self.cols = 24
        self.margin = 15 #pixels around board
        self.width = data.width
        self.height = data.height
        self.cellDim = 32
        self.boardColor = rgbString(235, 221, 130)
        
        self.kitchenImg = PhotoImage(file = "boardImgs\kitchenImg.gif")
        self.diningRoomImg = PhotoImage(file = "boardImgs\diningRoomImg.gif")
        self.ballroomImg = PhotoImage(file = "boardImgs\%s.gif" %'bRoomImg')
        self.gameRoomImg = PhotoImage(file = "boardImgs\%s.gif" %'billRoomImg')
        self.hallImg = PhotoImage(file = "boardImgs\%s.gif" %'hImg')
        self.conservatoryImg = PhotoImage(file = "boardImgs\%s.gif" %'conservImg')
        self.studyImg = PhotoImage(file = "boardImgs\%s.gif" %'studyImg')
        self.libraryImg = PhotoImage(file = "boardImgs\%s.gif" %'libImg')
        self.loungeImg = PhotoImage(file = "boardImgs\%s.gif" %'loungImg')
        self.centerImg = PhotoImage(file = "boardImgs\%s.gif" %'center')
        
        self.possibleSpotColor = rgbString(244,164,96)
        self.selected = []
        #all the room coordiantes, they are fixed and there are many of them
        #no point in having a variable for each
        self.center = self.getCoords(10, 10, 15, 17)
        #extra cells we had to fill in due to images
        self.extraCells = []
        self.outOfBounds = self.settingOutOfBounds()
        self.outOfBoundsColor = rgbString(49,79,79) 
        self.kitchen = self.getCoords(1, 0, 6, 7)
        self.kitchenDoors = [(7,4)]
        self.hall = self.getCoords(18, 9, 15, 24)
        self.hallDoors = [(17,11),(17,12),(20,15)] #last one is a right door
        self.diningRoom = self.getCoords(9,0,5,16) + self.getCoords(10,5,8,16)
        self.diningRoomDoors = [(16,6),(12,8)] #up and left
        self.extraCells += [(9,i) for i in range(5,8)] 
        self.lounge = self.getCoords(19, 0, 7, 24)
        self.loungeDoors = [(18, 6)] #down
        self.conservatory = self.getCoords(1,18,24,5) + self.getCoords(5,19,24,6)
        self.extraCells += [(5,18)]
        self.conservatoryDoors = [(5, 18)] #right
        self.gameRoom = self.getCoords(8, 18, 24, 13)
        self.gameRoomDoors = [(9,17), (13,22)] #right, up
        self.ballroom = self.getCoords(2,8,16,8) + self.getCoords(0,10,14,2)
        self.ballroomDoors = [(8,9),(8,14),(5,7),(5,16)] #2up, right, left
        self.extraCells += [(0,8),(0,9),(0,14),(0,15),(1,8),(1,9),(1,14),(1,15)]
        self.library = self.getCoords(15,17,18,18) + self.getCoords(14,18,24,19)
        self.libraryColor = 'black'
        self.libraryDoors = [(13,20),(16,16)] #down, right
        self.extraCells += [(18,17),(14,17)]
        self.study = self.getCoords(21, 17, 24, 24)
        self.studyDoors = [(20,17)] #down
        self.roomsCoords = {12:self.hall, 13:self.lounge, 14:self.diningRoom,
                    15:self.kitchen, 16:self.ballroom, 17:self.conservatory,
                    18:self.gameRoom, 19:self.library, 20:self.study}
        self.doorsCoords = {12:self.hallDoors, 13:self.loungeDoors,
                14:self.diningRoomDoors,15:self.kitchenDoors, 16:self.ballroomDoors, 
                17:self.conservatoryDoors,18:self.gameRoomDoors,  
                19:self.libraryDoors, 20:self.studyDoors} 

    #taken from notes:        
    def getCellBounds(self, row, col):
        # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
        columnWidth = 32
        rowHeight = 32
        x0 = self.margin + col * columnWidth
        x1 = self.margin + (col+1) * columnWidth
        y0 = self.margin + row * rowHeight
        y1 = self.margin + (row+1) * rowHeight
        return (x0, y0, x1, y1)
        
    def settingOutOfBounds(self):
        rows, cols = self.rows, self.cols
        #makes list of out of bounds coordinates (outside of playing area)
        outOfBounds = [(1,6),(1,17)]
        #top-most "grassy" area
        firstStrip, secStrip = 9, 15
        for i in range(firstStrip):
            outOfBounds += [(0,i)]
        for i in range(secStrip, cols):
            outOfBounds += [(0,i)]
        #along left edge 
        for i in [6, 8, 16, 18]:
            outOfBounds += [(i,0)]
        #along bottom edge
        for i in [6, 8, 15, 17]:
            outOfBounds += [(rows-1,i)]
        #right edge
        for i in [5, 7, 13, 14, 18, 20]:
            outOfBounds += [(i,cols-1)]
        return outOfBounds
        
    def getCoords(self, top, left, right, bottom):
        coords = []
        for row in range(top, bottom):
            for col in range(left, right):
                coords += [(row, col)]
        return coords
        
    def drawRoom(self, canvas, room, color):
        #draws each individual room
        for cell in room:
            (x0, y0, x1, y1) = self.getCellBounds(cell[0], cell[1])
            canvas.create_rectangle(x0, y0, x1, y1, fill=color,
                    width=0)
                    
    def drawDoor(self, canvas, row, col, direction):
        #0:up, 1:right, 2:down, 3:left
        up, right, down, left = 0, 1, 2, 3
        (x0, y0, x1, y1) = self.getCellBounds(row, col)
        m = 5 #margin
        if direction%2 == 0:
            #arrow coordinates
            (a,b,c,d) = ((x0+m,(y0+y1)/2),((x0+x1)/2, y0+m),
                    (x1-m,(y0+y1)/2),((x0+x1)/2,y1-m))
            canvas.create_line(b, d, width = 2) #main line
            if direction == up:
                canvas.create_line(a, b, width = 2)
                canvas.create_line(b, c, width = 2)
            else:
                canvas.create_line(a, d, width = 2)
                canvas.create_line(d, c, width = 2)
                
        else:
            (d,a,b,c) = ((x0+m,(y0+y1)/2),((x0+x1)/2, y0+m),
                    (x1-m,(y0+y1)/2),((x0+x1)/2,y1-m))
            canvas.create_line(b, d, width = 2) #main line
            if direction == right:
                canvas.create_line(a, b, width = 2)
                canvas.create_line(b, c, width = 2)
            else:
                canvas.create_line(a, d, width = 2)
                canvas.create_line(d, c, width = 2)
            
    def drawAllDoors(self, canvas):
        #0:up, 1:right, 2:down, 3:left
        up, right, down, left = 0, 1, 2, 3
        UpDoors = (self.kitchenDoors+self.diningRoomDoors[:1]+self.gameRoomDoors[1:]
                +self.ballroomDoors[:2])
        DownDoors = (self.hallDoors[:2]+self.loungeDoors+self.libraryDoors[:1]
                +self.studyDoors)
        RightDoors = (self.conservatoryDoors+self.gameRoomDoors[:1]
                +self.ballroomDoors[2:3]+self.libraryDoors[1:])
        LeftDoors = (self.diningRoomDoors[1:]+self.ballroomDoors[3:]
                +self.hallDoors[2:])
        for door in UpDoors:
            self.drawDoor(canvas, door[0], door[1], up)
        for door in DownDoors:
            self.drawDoor(canvas, door[0], door[1], down)
        for door in RightDoors:
            self.drawDoor(canvas, door[0], door[1], right)
        for door in LeftDoors:
            self.drawDoor(canvas, door[0], door[1], left)
            
    def draw(self, canvas):
        #draw basic board
        for row in range(self.rows):
            for col in range(self.cols):
                (x0, y0, x1, y1) = self.getCellBounds(row, col)
                canvas.create_rectangle(x0, y0, x1, y1, fill=self.boardColor)
        
        #drawing each room 
        #center
        x0, y0, a, b = self.getCellBounds(10,10)
        a, b, x1, y1 = self.getCellBounds(16,14)
        canvas.create_image((x0+x1)/2, (y0+y1)/2, image = self.centerImg)
        #kitchen
        x0, y0, a, b = self.getCellBounds(1,0)
        a, b, x1, y1 = self.getCellBounds(6,5)
        canvas.create_image((x0+x1)/2, (y0+y1)/2, image = self.kitchenImg)
        #diningRoom
        x0, y0, a, b = self.getCellBounds(9,0)
        a, b, x1, y1 = self.getCellBounds(15,7)
        canvas.create_image((x0+x1)/2, (y0+y1)/2, image = self.diningRoomImg)
        #ballroom
        x0, y0, a, b = self.getCellBounds(0,8)
        a, b, x1, y1 = self.getCellBounds(7,15)
        canvas.create_image((x0+x1)/2, (y0+y1)/2, image = self.ballroomImg)
        #hall
        x0, y0, a, b = self.getCellBounds(18,9)
        a, b, x1, y1 = self.getCellBounds(23,14)
        canvas.create_image((x0+x1)/2, (y0+y1)/2, image = self.hallImg)
        #gameRoom
        x0, y0, a, b = self.getCellBounds(8,18)
        a, b, x1, y1 = self.getCellBounds(12,23)
        canvas.create_image((x0+x1)/2, (y0+y1)/2, image = self.gameRoomImg)
        #study
        x0, y0, a, b = self.getCellBounds(21,17)
        a, b, x1, y1 = self.getCellBounds(23,23)
        canvas.create_image((x0+x1)/2, (y0+y1)/2, image = self.studyImg)
        #library
        x0, y0, a, b = self.getCellBounds(14,17)
        a, b, x1, y1 = self.getCellBounds(18,23)
        canvas.create_image((x0+x1)/2, (y0+y1)/2, image = self.libraryImg)
        #conservatory
        x0, y0, a, b = self.getCellBounds(1,18)
        a, b, x1, y1 = self.getCellBounds(5,23)
        canvas.create_image((x0+x1)/2, (y0+y1)/2, image = self.conservatoryImg)
        #lounge
        x0, y0, a, b = self.getCellBounds(19,0)
        a, b, x1, y1 = self.getCellBounds(23,6)
        canvas.create_image((x0+x1)/2, (y0+y1)/2, image = self.loungeImg)
        
        #fill in extra cells:
        for cell in self.extraCells:
            (x0, y0, x1, y1) = self.getCellBounds(cell[0], cell[1])
            canvas.create_rectangle(x0, y0, x1, y1, fill=self.boardColor)
        
        #draw door indicators:
        self.drawAllDoors(canvas)
        #draw out 1of bounds (not usable squares)
        for cell in self.outOfBounds:
            (x0, y0, x1, y1) = self.getCellBounds(cell[0], cell[1])
            canvas.create_rectangle(x0, y0, x1, y1, fill=self.outOfBoundsColor,
                    width=0)

