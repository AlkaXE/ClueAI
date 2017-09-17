## BoardMap for AI
from GameBoard import *
import copy

#taken from notes
def make2dList(rows, cols):
    a=[]
    for row in range(rows): a += [[None]*cols]
    return a

def rgbString(red, green, blue):
    return "#%02x%02x%02x" % (red, green, blue)

class BoardMap(GameBoard):
    def __init__(self, data):
        super().__init__(data)
        #self.locations = [(23,7), (17,0), (0,9), (0,14), (6,23), (19,23)]
        #locations follow player order
        red = rgbString(255, 26, 0)
        yellow = rgbString(221, 175, 39)
        self.colors = [red, yellow, 'white', 'green', 'blue', 'purple']
        self.rMinus = 3
        self.allPaths = dict()
        self.possibleRooms = dict()
        #fixed coordinates on board of where they would be in rooms
        self.locationsInRooms = {12:[(20,11),(20,12),(21,11),(21,12),(22,11),(22,12)],
            13:[(20,2),(20,3),(21,2),(21,3),(21,4),(22,3)],
            14:[(12,1),(12,2),(12,3),(12,4),(12,5),(12,6)],
            15:[(2,3),(3,3),(3,2),(4,2),(4,3),(5,2)],
            16:[(3,11),(3,12),(4,11),(4,12),(5,11),(5,12)],
            17:[(2,20),(2,21),(3,20),(3,21),(4,20),(4,21)],
            18:[(9,20),(9,21),(10,20),(10,21),(11,20),(11,21)],
            19:[(16,18),(16,19),(16,20),(16,21),(16,22),(16,23)],
            20:[(22,18),(22,19),(22,20),(22,21),(22,22),(22,23)]}
                            
    
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
        
    def isValid(self, data, row, col, visited):
        if visited == []: return True
        if (row, col) in self.center: return False
        if (row >= self.rows or col >= self.cols
            or row < 0 or col < 0):
            return False #off board
        if (row, col) in self.outOfBounds:
            return False
        if (row, col) in visited:
            return False
        for i in data.roomsRange:
            if (row, col) in self.roomsCoords[i]:
                return False #we tried to cross a wall
        for loc in data.locations:
            if (row, col) in data.locations:
                return False #it's occupied 
        return True
        
    def getSpots(self, data, roll, row, col, visited = None, count=0):
        #visted is 1 if we had to leave a room
        currPlayer = data.playerOrder[data.current]
        if currPlayer.currentRoom != None and count == 0: #in a room
            for door in self.doorsCoords[currPlayer.currentRoom]:
                row, col = door
                self.getSpots(data, data.roll-1, row, col, 1, count+1)
        else:
            if visited == None or visited == 1:
                visited = []
            #base case
            if roll == 0 and self.isValid(data, row, col, visited):
                visited += [(row, col)] 
                self.allPaths[(row, col)] = visited
                return True
            
            if self.isValid(data, row, col, visited):
                visited += [(row, col)]
                self.getSpots(data, roll-1, row-1, col, copy.copy(visited), count+1)
                self.getSpots(data, roll-1, row+1, col, copy.copy(visited), count+1)
                self.getSpots(data, roll-1, row, col-1, copy.copy(visited), count+1)
                self.getSpots(data, roll-1, row, col+1, copy.copy(visited), count+1)
            
    def getPossibleRooms(self, data):
        currPlayer = data.playerOrder[data.current] #actual player object
        if currPlayer.currentRoom == 20:
            self.possibleRooms[15] = []
        elif currPlayer.currentRoom == 15:
            self.possibleRooms[20] = []
        elif currPlayer.currentRoom == 17:
            self.possibleRooms[13] = []
        elif currPlayer.currentRoom == 13:
            self.possibleRooms[17] = []
        
        for dest in self.allPaths:
            for spot in self.allPaths[dest]:
                for room in self.doorsCoords:
                    for door in self.doorsCoords[room]:
                        if door == spot and room != currPlayer.currentRoom: #todo
                            self.possibleRooms[room] = self.allPaths[dest]
            

    def drawPossibleSpots(self, data, canvas):
        row, col = data.locations[data.current][0], data.locations[data.current][1]
        #self.getSpots(data, data.roll, row, col)
        #self.getPossibleRooms(data)
        if data.rolled == True: 
            self.allPaths = dict() 
            self.possibleRooms = dict()
            self.getSpots(data, data.roll, row, col) 
            self.getPossibleRooms(data) 
        if data.nextTurn:
            self.allPaths = dict() 
            self.possibleRooms = dict()
            self.getSpots(data, data.roll, row, col) 
            self.getPossibleRooms(data) 
        #print(self.allPaths)
        #mark the places the player could go
        #print(data.locations[data.current])
        for room in self.possibleRooms:
            self.drawRoom(canvas, self.roomsCoords[room], self.possibleSpotColor)
        for dest in self.allPaths:
            #print(dest)
            (x0, y0, x1, y1) = self.getCellBounds(dest[0], dest[1])
            canvas.create_rectangle(x0, y0, x1, y1, fill = self.possibleSpotColor)
        
    #modified from notes
    def pointInGrid(self, x, y, data, colWidth, rowHeight):
        # return True if (x, y) is inside the grid defined by data.
        return ((self.margin <= x <= colWidth*self.cols+self.margin) and
                (self.margin <= y <= self.margin+self.rows*rowHeight))
    
    def getCell(self, x, y, data, colWidth, rowHeight):
        # return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.
        if (not self.pointInGrid(x, y, data, colWidth, rowHeight)):
            return (-1, -1)
        cellWidth  = colWidth
        cellHeight = rowHeight
        row = (y-self.margin) // cellHeight
        col = (x-self.margin) // cellWidth
        # triple-check that we are in bounds
        row = min(self.rows-1, max(0, row))
        col = min(self.cols-1, max(0, col))
        return (row, col)
            
    def mousePressedMove(self, x, y, data):
        colWidth = 32
        rowHeight = 32
        if data.current == data.characterPicked:
            row, col = self.getCell(x, y, data, colWidth, rowHeight)
            if (row, col) in self.allPaths:
                data.humanMoved = True #todo
                self.movePlayer(data, data.current, row, col)
            for room in self.possibleRooms:
                if (row, col) in self.roomsCoords[room]:
                    data.humanMoved = True
                    row1, col1 = self.locationsInRooms[room][data.current]
                    self.movePlayer(data, data.current, row1, col1)
        
    def movePlayer(self, data, player, row, col):
        #moves players about the board
        self.allPaths = dict()
        self.possibleRooms = dict()
        data.locations[player] = (row, col)
        currPlayer = data.playerOrder[data.current] #actual player object
        currPlayer.currentRoom = None
        for room in self.locationsInRooms:
            if (row, col) in self.locationsInRooms[room]:
                currPlayer.currentRoom = room #todo
                
    def moveSuggestedPlayer(self, data):
        beingMoved = data.playerOrder[data.pBeingMoved]
        roomMoved = data.currentSuggestion[2] #room to move to
        loc = self.locationsInRooms[roomMoved][data.pBeingMoved]
        beingMoved.location = loc
        beingMoved.currentRoom = roomMoved
        data.locations[data.pBeingMoved] = loc
        
    def drawPlayers(self, canvas, data):
        for i in range(6): #there are always six pieces
            player = data.locations[i]
            color = self.colors[i]
            if color =='white': out = 'black'
            else: out = 'white'
            (x0, y0, x1, y1) = self.getCellBounds(player[0], player[1])
            canvas.create_oval(x0+self.rMinus, y0+self.rMinus, x1-self.rMinus,
                    y1-self.rMinus, fill = color, width=2, outline = out)
                    
    def findDistanceToRooms(self, data):
        pass
        
        
            