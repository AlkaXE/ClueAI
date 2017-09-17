##buttons and other things displayed that human can use
from tkinter import *
import random

#taken from notes
def rgbString(red, green, blue):
    return "#%02x%02x%02x" % (red, green, blue)

class Buttons(object):
    def __init__(self, data):
        self.margin = 15
        boardCell = 32
        checkLabel = 100
        checkCell = 25
        checkRows = data.numOfCards
        checkCols = 6 #todo #keep dimensions consistent
        self.buttonColor = rgbString(255, 239, 213)
        
        #so others moves displayed aligned with checklist 
        othersHeight = 215
        x0, y0 = self.margin+boardCell*checkCell, self.margin+checkCell*(checkRows+1)
        x1, y1 = x0+checkLabel+checkCell*checkCols, y0 + othersHeight
        self.othersMovesCoords = (x0,y0,x1,y1) 
        #coordinates for OK button in othersMoves
        okMargin = 10
        okHeight = 40
        self.OkCoords = (x0+okMargin, y1-okMargin-okHeight,x1-okMargin,y1-okMargin)
        #coordinates for hooman cards box
        topmargin = 15
        sidemargin = 25
        hCH = 250 #height of card box
        x0, y0 = self.OkCoords[2] + sidemargin, topmargin
        x1, y1 = data.width-sidemargin, y0 + hCH
        #coordinates for suggestion box: aligned below hooman's cards
        topmargin = 15
        self.bottommargin = 25
        self.humanCardsCoords = (x0, y0, x1, y1)
        x0, y0 = self.humanCardsCoords[0],self.humanCardsCoords[3]+topmargin
        x1, y1 = (self.humanCardsCoords[2],
                self.othersMovesCoords[1]-self.bottommargin)
        self.suggestionBoxCoords = (x0, y0, x1, y1)
        #coordinates for suggestion button
        margin = 10
        w, h = 150, 30 #width and height
        cx = (self.suggestionBoxCoords[2] + self.suggestionBoxCoords[0])/2 #x center
        x1, y1 = cx + w/2,self.suggestionBoxCoords[3]-margin
        x0, y0 = cx - w/2, y1-h 
        self.suggestButtonCoords = (x0, y0, x1, y1)
        #Human shit box coordinates
        x0, x1 = self.suggestionBoxCoords[0], self.suggestionBoxCoords[2]
        y0, y1 = self.othersMovesCoords[1], self.othersMovesCoords[3]
        self.humanBoxCoords = (x0, y0, x1, y1)
        #die coordinates
        x = self.humanBoxCoords[0]
        (cx,cy)=((self.humanBoxCoords[2]-x)/5 + x,
                (self.humanBoxCoords[1]+self.humanBoxCoords[3])/2)
        r = 40 #die 'radius'
        self.dotR = 5
        self.dieCoords = (cx-r, cy-r, cx+r, cy+r)
        #dots distribution on die
        x0, y0, x1, y1 = self.dieCoords
        d = 15 #distance between pips
        self.dot1 = [(cx,cy)] #dot centered in the middle
        self.dot2 = [(cx-d, cy-d),(cx+d, cy+d)]
        self.dot3 = [(cx,cy),(cx-d, cy-d),(cx+d, cy+d)]
        self.dot4 = [(cx-d, cy-d),(cx+d, cy+d),(cx-d, cy+d),(cx+d, cy-d)]
        self.dot5 = [(cx,cy),(cx-d, cy-d),(cx+d, cy+d),(cx-d, cy+d),(cx+d, cy-d)]
        self.dot6 = [(cx-d,cy),(cx-d,cy-d),(cx-d,cy+d),(cx+d,cy),(cx+d,cy-d),
                     (cx+d,cy+d)]
        self.dotsDict = {1:self.dot1, 2:self.dot2, 3:self.dot3, 4:self.dot4,
                5:self.dot5, 6:self.dot6}
        #accusation button coordinates: about 2/3 of the hooman box
        prop, w, h= 2/3, 70, 20 #half the width and height
        x = self.humanBoxCoords[0]+2*(self.humanBoxCoords[2]-self.humanBoxCoords[0])/3
        y = self.humanBoxCoords[1]+(self.humanBoxCoords[3]-self.humanBoxCoords[1])/2
        x0, x1 = x-w, x+w
        y0 ,y1 = y-h, y+h
        self.accuseButtonCoords = (x0, y0, x1, y1)
        #disproveScreenCoordinates
        self.disproveScreenCoords = (data.width/4, data.height/4, data.width*3/4,
                3*data.height/4)
        (x0, y0, x1, y1) = self.disproveScreenCoords
        cardW, cardH = 135/2, 214/2 #fixed sizes
        x, y = (x1-x0)/4, (y0+y1)/2
        self.humanCard1Coords = (x0+x-cardW, y-cardH, x0+x+cardW, y+cardH)
        self.humanCard2Coords = (x0+2*x-cardW, y-cardH, x0+2*x+cardW, y+cardH)
        self.humanCard3Coords = (x0+3*x-cardW, y-cardH, x0+3*x+cardW, y+cardH)
        self.cardBoxes ={0:self.humanCard1Coords, 1:self.humanCard2Coords,
            2:self.humanCard3Coords}
            
        red = rgbString(255, 26, 0)
        yellow = rgbString(221, 175, 39)
        self.colors = [red, yellow, 'black', 'green', 'blue', 'purple']
        #the ones the hooman has selected
        self.selectedCharac = None
        self.selectedWeapon = None
        self.selectedRoom = None
        
    def drawOthersMoves(self, data, canvas):
        canvas.create_rectangle(self.othersMovesCoords, fill = self.buttonColor, 
                width = 0)
        self.drawOkButton(data, canvas)
        (x0,y0,x1,y1) = self.othersMovesCoords 
        margin = 15
        okHeight = 40 #keep consitent
        
        if data.gameStarted == False: #game has not begun
            canvas.create_text((x0+x1)/2, (y0+y1)/2-okHeight, 
                    text = 'PRESS OK TO START', font = 'Helvetica 10')
         
        elif data.current == data.characterPicked: #it is human's turn
            if data.human.currentRoom != None and data.shown != None:
                per = data.characters[data.disproveCount]
                msg1 = "%s has shown you" %per
                msg2 = "%s" %data.allCards[data.shown]
                canvas.create_text((x0+x1)/2, (y0+y1)/2-okHeight, text = msg1, 
                        font = 'Helvetica 10')
                canvas.create_text((x0+x1)/2, (y0+y1)/2-okHeight+self.margin, 
                        text = msg2, font = 'Helvetica 10')
                        
            elif data.humanMoved == False and data.current == data.characterPicked:
                hText1 = "It is your turn"
                hText2 = "Accuse or roll and move"
                canvas.create_text((x0+x1)/2, (y0+y1)/2-okHeight, text = hText1, 
                        font = 'Helvetica, 10')
                canvas.create_text((x0+x1)/2, (y0+y1)/2-okHeight+margin, 
                        text = hText2, font = 'Helvetica 10')
                        
            elif (data.human.currentRoom != None and data.shown == None and 
                data.disproved == False):
                msg = "No one could disprove it"
                canvas.create_text((x0+x1)/2, (y0+y1)/2-okHeight, text = msg, 
                        font = 'Helvetica 10')
                        
            elif (data.human.currentRoom != None and data.shown == None and 
                data.disproveCount != (data.characterPicked+1)%data.numOfPlayers
                and data.rolled == True):
                msg = "Make a suggestion"
                canvas.create_text((x0+x1)/2, (y0+y1)/2-okHeight, text = msg, 
                        font = 'Helvetica 10')
                        
            else:
                hText1 = "Your turn is over"
                canvas.create_text((x0+x1)/2, (y0+y1)/2-okHeight+margin, 
                        text = hText1, font = 'Helvetica 10')
                    
        elif data.currentSuggestion == None: #no suggestion was made
            msg = "%s moved with roll %d" %(data.characters[data.current], data.roll)
            canvas.create_text((x0+x1)/2, (y0+y1)/2-okHeight+margin, text = msg,
                    font = 'Helvetica 10')
                    
        else:
            addMargin = 10 #small additional margin to adjust
            #movement text
            msg = "%s moved with roll %d" %(data.characters[data.current], 
                    data.roll)
            canvas.create_text((x0+x1)/2, y0+margin, text = msg,
                    font = 'Helvetica 10')
            #suggestions text 
            perText = "%s suggests:" %data.characters[data.current]
            (s0, s1, s2) = data.currentSuggestion
            suggestionText = "%s  %s  %s" %(data.characters[s0], data.weapons[s1],
                    data.rooms[s2])
            canvas.create_text((x0+x1)/2, y0+(y1-y0)/2-okHeight, text = suggestionText,
                    font = 'Helvetica 10')
            canvas.create_text((x0+x1)/2, y0+(y1-y0)/2-okHeight*2+addMargin, 
                    text = perText, font = 'Helvetica, 10')
            if data.disproveCount == None: #no one disproved it
                disText = 'No one could disprove it'
            else:
                per = data.characters[data.disproveCount]
                disText = 'it was disproved by %s' %(per) 
            canvas.create_text((x0+x1)/2, (y0+y1)/2+okHeight/3-addMargin, 
                    text = disText, font = 'Helvetica 10')

        
    def inOkButtonBounds(self, x, y, data):
        #check if we've pressed the ok button
        (x0,y0,x1,y1) = self.OkCoords
        return ((x0 <= x <= x) and (y0 <= y <= y1))

    def drawOkButton(self, data, canvas):
        (x0,y0,x1,y1) = self.OkCoords 
        canvas.create_rectangle(self.OkCoords, fill = 'orange', width = 0)
        canvas.create_text((x0+x1)/2, (y0+y1)/2, text = 'OK', fill = 'yellow',
                font = 'Helvetica 13 bold')
        
    def drawHumanCards(self, canvas, data): #todo #get all cards
        #cards are 135x214
        topmargin = 15
        sidemargin = 25
        (x0, y0, x1, y1) = self.humanCardsCoords 
        #note: all coordinates for bounding boxes are given this way
        cardLocations = (1/6, 1/2, 5/6)
        cardsPerPlayer = data.numOfCards//data.numOfPlayers
            
        currPlayer = data.playerOrder[data.current] #actual player object
        for i in range(cardsPerPlayer):
            fac = cardLocations[i] #position factor
            canvas.create_image(x0+(x1-x0)*fac, (y0+y1)/2+topmargin, 
                image = data.cardImgs[i])
        canvas.create_text((x0+x1)/2, y0+topmargin ,text = 'Your Cards', 
                fill = 'white', font ='Helvetica 12 bold')
                
    def drawDisproveScreen(self, canvas, data):
        margin = 30
        canvas.create_rectangle(self.disproveScreenCoords, fill = 'white', width=0)
        perText = "%s suggests:" %data.characters[data.current]
        (s0, s1, s2) = data.currentSuggestion
        suggestionText = "%s  %s  %s" %(data.characters[s0], data.weapons[s1],
                data.rooms[s2])
        bottomText = 'pick a card to disprove with'
        (x0, y0, x1, y1) = self.disproveScreenCoords
        canvas.create_text((x0+x1)/2, y0+margin, text = perText, 
            font = 'Helvetica 15')
        canvas.create_text((x0+x1)/2, y0+2*margin, text = suggestionText, 
            font = 'Helvetica 15')
        canvas.create_text((x0+x1)/2, y1-2*margin, text = bottomText, 
            font = 'Helvetica 13')
            
        cardsPerPlayer = data.numOfCards//data.numOfPlayers
        for i in range(cardsPerPlayer):
            (x0, y0, x1, y1) = self.cardBoxes[i]
            canvas.create_image((x0+x1)/2, (y0+y1)/2, image = data.cardImgs[i])
        
        if (data.selectedToShow == None or 
            data.selectedToShow not in data.currentSuggestion):
            (x0, y0, x1, y1) = self.disproveScreenCoords
            msg = "Pick a valid card."
            color = rgbString(165, 42, 42)
            canvas.create_text((x0+x1)/2, y1-margin, text = msg, fill = color,
                font = 'Helvetica 13')
                
    def mousePressedOwnCards(self, x, y, data):
        #if hooman has selected own card
        (x10, y10, x11, y11) = self.humanCard1Coords
        (x20, y20, x21, y21) = self.humanCard2Coords
        (x30, y30, x31, y31) = self.humanCard3Coords
        if (x10 <= x <= x11) and (y10 <= y <= y11):
            data.selectedToShow = data.human.cards[0]
        if (x20 <= x <= x21) and (y20 <= y <= y21):
            data.selectedToShow = data.human.cards[1] 
        if (x30 <= x <= x31) and (y30 <= y <= y31):
            data.selectedToShow = data.human.cards[2]
                
    def drawSuggestButton(self, canvas, data):
        (x0, y0, x1, y1) = self.suggestButtonCoords 
        canvas.create_rectangle(self.suggestButtonCoords, fill='orange', width=0)
        canvas.create_text((x0+x1)/2, (y0+y1)/2, text = 'SUGGEST', fill = 'yellow',
                font = 'Helvetica 13 bold')
        
    def pointInGrid(self, x, y, data, buttonH1, buttonH2, buttonW):
        #first get area covered by suggestion button boxes
        #all magic nums are constants throughout game
        (x0, y0, a, b) = self.getCellBounds(0, 0, buttonW, buttonH1) #a, b irrelevant
        (a, b, x1, y1) = self.getCellBounds(5, 0, buttonW, buttonH1)
        self.characBox = (x0, y0, x1, y1)

        (x0, y0, a, b) = self.getCellBounds(0, 1, buttonW, buttonH1) #a, b irrelevant
        (a, b, x1, y1) = self.getCellBounds(5, 1, buttonW, buttonH1)
        self.weaponsBox = (x0, y0, x1, y1)

        (x0, y0, a, b) = self.getCellBounds(0, 2, buttonW, buttonH2) #a, b irrelevant
        (a, b, x1, y1) = self.getCellBounds(8, 2, buttonW, buttonH2)
        self.roomsBox = (x0, y0, x1, y1)

        # return True if (x, y) is inside the grid 
        bool1 = ((self.characBox[0] <= x <= self.characBox[2]) and 
                (self.characBox[1] <= y <= self.characBox[3]))
        bool2 = ((self.weaponsBox[0] <= x <= self.weaponsBox[2]) and 
                (self.weaponsBox[1] <= y <= self.weaponsBox[3]))
        bool3 = ((self.roomsBox[0] <= x <= self.roomsBox[2]) and 
                (self.roomsBox[1] <= y <= self.roomsBox[3]))
        return (bool1 or bool2 or bool3)
    
    #modified from notes
    def getCell(self, x, y, data, buttonH1, buttonH2, buttonW):
        # return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.
        if (not self.pointInGrid(x, y, data, buttonH1, buttonH2, buttonW)):
            return (-1, -1)
        cellWidth  = buttonW
        if ((self.roomsBox[0] <= x <= self.roomsBox[2]) and 
            (self.roomsBox[1] <= y <= self.roomsBox[3])): 
            cellHeight = buttonH2 #room button size
        else: cellHeight = buttonH1
        row = (y-self.characBox[1]) // cellHeight
        col = (x-self.characBox[0]) // cellWidth

        return (row, col)
        
    def getCellBounds(self, row, col, colWidth, rowHeight):
        # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
        columnWidth = colWidth
        rowHeight = rowHeight
        m = 3 #small margin around buttons
        x0 = self.margin + col * columnWidth + self.suggestionBoxCoords[0]+m
        x1 = self.margin + (col+1) * columnWidth + self.suggestionBoxCoords[0]-m
        y0 = self.margin + row * rowHeight + self.suggestionBoxCoords[1]
        y1 = self.margin + (row+1) * rowHeight + self.suggestionBoxCoords[1]
        return (x0, y0, x1, y1)
                
    def drawSuggestionBox(self, canvas, data):
        (x0, y0, x1, y1) = self.suggestionBoxCoords 
        canvas.create_rectangle(self.suggestionBoxCoords, fill = self.buttonColor,
                width = 0)
        #submit suggestion button
        self.drawSuggestButton(canvas, data)
        
        self.selectedColor = 'red'
        
        locations = (1/6, 1/2, 5/6)
        w, h = x1-x0, y1-y0 #width and height of box
        rows1, rows2 = 6, 9 #rows for character, weapons and rooms 
        cardButtonW = (w-self.margin*2)//3
        cardButtonH1 = (h-self.bottommargin*2-self.margin)//rows1 
        #for persons and weapons
        cardButtonH2 = (h-self.bottommargin*2-self.margin)//rows2 #for rooms
        
        for row in range(rows1): #draw character suggestion boxes
            (x2, y2, x3, y3) = self.getCellBounds(row, 0, cardButtonW, cardButtonH1)
            if row == self.selectedCharac:
                canvas.create_rectangle(x2, y2, x3, y3, fill=self.selectedColor, 
                        width =0 )
            text = data.characters[row]
            canvas.create_text((x2+x3)/2, (y2+y3)/2, text = text)
        for row in range(rows1): #draw weapons suggestion boxes
            (x2, y2, x3, y3) = self.getCellBounds(row, 1, cardButtonW, cardButtonH1)
            if row + rows1 == self.selectedWeapon:
                canvas.create_rectangle(x2, y2, x3, y3, fill=self.selectedColor, 
                        width =0 )
            text = data.weapons[row+rows1]
            canvas.create_text((x2+x3)/2, (y2+y3)/2, text = text)
        for row in range(rows2): #draw rooms suggestion boxes
            (x2, y2, x3, y3) = self.getCellBounds(row, 2, cardButtonW, cardButtonH2)
            if data.human.currentRoom != None: 
                self.selectedRoom = data.human.currentRoom - 12 #todo
            if row == self.selectedRoom:
                canvas.create_rectangle(x2, y2, x3, y3, fill=self.selectedColor, 
                        width =0 )
            text = data.rooms[row+rows1*2]
            canvas.create_text((x2+x3)/2, (y2+y3)/2, text = text)
            
    def mousePressedSuggestion(self, x, y, data):
        (x0, y0, x1, y1) = self.suggestionBoxCoords
        w, h = x1-x0, y1-y0 #width and height of box
        rows1, rows2 = 6, 9
        buttonW = (w-self.margin*2)//3
        buttonH1 = (h-self.bottommargin*2-self.margin)//rows1 
        #for persons and weapons
        buttonH2 = (h-self.bottommargin*2-self.margin)//rows2 #for rooms
        
        (row, col) = self.getCell(x, y, data, buttonH1, buttonH2, buttonW)
        if col == 0: #charac
            if self.selectedCharac == row:
                self.selectedCharac = None
            else: self.selectedCharac = row
        elif col == 1: #weapon
            if self.selectedWeapon == row:
                self.selectedWeapon = None
            else: self.selectedWeapon = row+rows1
        
        if data.human.currentRoom == None:
            self.selectedRoom = None
        else: self.selectedRoom = data.human.currentRoom
        return (self.selectedCharac , self.selectedWeapon, self.selectedRoom) 
        
    def mousePressedSuggestionButton(self, x, y, data):
        (x0, y0, x1, y1 ) = self.suggestButtonCoords
        return ((x0 <= x <= x1) and (y0 <= y <= y1)) 
        
    def drawDie(self, canvas, data):
        m = 20
        x0, y0, x1, y1 = self.dieCoords
        canvas.create_rectangle(self.dieCoords, fill = 'white', width = 0)
        for dot in self.dotsDict[data.roll]:
            x, y = dot[0], dot[1]
            canvas.create_oval(x-self.dotR, y-self.dotR, x+self.dotR, y+self.dotR,
                    fill = 'black')
        #draw name under die
        name = data.characters[data.characterPicked]
        color = self.colors[data.characterPicked]
        canvas.create_text((x0+x1)/2, y1+m, text = name, fill = color, font = 'Helvetica 13')
                    
    def mousePressedDie(self, x, y, data):
        x0, y0, x1, y1 = self.dieCoords
        if (x0 <= x <= x1) and (y0 <= y <= y1): #in die bounds
            if data.current == data.characterPicked: #hooman 
                data.roll = data.human.rollDie(data)
        
    def drawHumanBox(self, canvas, data):
        #aligns with other boxes
        x0, x1 = self.suggestionBoxCoords[0], self.suggestionBoxCoords[2]
        y0, y1 = self.othersMovesCoords[1], self.othersMovesCoords[3]
        self.humanBoxCoords = (x0, y0, x1, y1)
        canvas.create_rectangle(self.humanBoxCoords, fill = self.buttonColor,
                width=0)
        if data.current != data.characterPicked and data.gameStarted:        
            currPlayerText = "It is %s's turn" %data.characters[data.current] 
            #get the name of the player, currplayer is order index
            canvas.create_text(2*(x1-x0)/3+x0, (y0+y1)/2 , text = currPlayerText,
                font = 'Helvetica 13')
                
    def drawAccuseButton(self, canvas, data):
        (x0, y0, x1, y1) = self.accuseButtonCoords
        canvas.create_rectangle(self.accuseButtonCoords, fill = 'orange', width=0)                     
        canvas.create_text((x0+x1)/2, (y0+y1)/2, text = 'ACCUSE', fill = 'yellow',
                font = 'Helvetica 13 bold')
                
    def mousePressedAccuse(self, x, y, data):
        x0, y0, x1, y1 = self.accuseButtonCoords
        if (x0 <= x <= x1) and (y0 <= y <= y1):
            data.gameMode = 'accuse' 
                
    def mousePressedButtons(self, data, event):
        data.buttons.mousePressedSuggestion(event.x, event.y, data)
        data.buttons.mousePressedOwnCards(event.x, event.y, data)
        if data.current == data.characterPicked and data.gameStarted == True:
            self.mousePressedAccuse(event.x, event.y, data)
            data.buttons.mousePressedDie(event.x, event.y, data)
            
    def drawAllButtons(self, canvas, data):
        self.drawOthersMoves(data, canvas)
        self.drawOkButton(data, canvas)
        self.drawHumanCards(canvas, data)
        self.drawSuggestionBox(canvas, data)
        self.drawHumanBox(canvas, data)
        self.drawDie(canvas, data)
        if data.current == data.characterPicked and data.gameStarted:
            self.drawAccuseButton(canvas, data)
                
            