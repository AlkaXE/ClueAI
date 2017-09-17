##Game loop and all
#Images from https://es.pinterest.com/pin/177118197818054122/
#https://www.flickr.com/photos/rosered/69786244
#https://c1.staticflickr.com/1/35/69786243_d59ab36b7d_z.jpg?zz=1
#http://www.clipartkid.com/images/66/clue-board-driverlayer-search-engine-uaWs8A-clipart.jpg
#https://es.pinterest.com/pin/371828512965881630/


import random
from AIPlayer import *
from Human import *
from print2dList import *
from GameBoard import *
from Checklist import *
from BoardMap import *
from Buttons import *
from AccusationScreen import *
from RulesScreen import *



# Took FullScreenApp from 
# http://stackoverflow.com/questions/7966119/display-fullscreen-mode-on-tkinter
class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master=master
        pad=3
        self._geom='200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
        master.bind('<Escape>',self.toggle_geom)            
    def toggle_geom(self,event):
        geom=self.master.winfo_geometry()
        print(geom,self._geom)
        self.master.geometry(self._geom)
        self._geom=geom

#taken from notes
def rgbString(red, green, blue):
    return "#%02x%02x%02x" % (red, green, blue)
    
##starting game
        
def init(data, canvas):
    data.numOfCards = 21
    data.cardNot = 10 #doesn't have the card
    data.characterPicked = None
    
    #row index each card maps to in player's checklist
    data.characters = {0:'Ms. Scarlet', 1:'Colonel Mustard', 2:'Mrs. White',
                3:'Mr. Green', 4:'Mrs. Peacock', 5:'Professor Plum'}
    data.weapons = {6:'Knife', 7:'Candlestick', 8:'Revolver', 9:'Rope', 
                10:'Lead Pipe', 11:'Wrench'}
    data.rooms = {12:'Hall', 13:'Lounge', 14:'Dining Room', 15:'Kitchen', 
                16:'Ballroom', 17:'Conservatory', 18:'Billiard Room', 19:'Library',
                20:'Study'}
    data.allCards = {**data.characters, **data.weapons, **data.rooms}
                
    data.characRange = range(0, 6)
    data.weaponsRange = range(6, 12)
    data.roomsRange = range(12, 21)
    
    data.playerOrder = [] #order in which they play
    data.gameOver = False
    
    w, h, cx, cy = 600, 120, data.width/2, data.height/2 #dimensions and center
    margin = 20
    #locations on screen
    (x0, y0, x1, y1) = (cx-w, cy-h, cx+w, cy+h)
    data.characterSelectionBox = (x0, y0, x1, y1)
    data.scarletSelectionBox = (x0+margin, y0, x0+w/3-margin, y1)
    data.mustardSelectionBox = (x0+w/3+margin, y0, x0+2*w/3-margin, y1)
    data.whiteSelectionBox = (x0+2*w/3+margin, y0, cx-margin, y1)
    data.greenSelectionBox = (cx+margin, y0, cx+w/3-margin, y1)
    data.peacockSelectionBox = (cx+w/3+margin, y0, cx+2*w/3-margin, y1)
    data.plumSelectionBox = (cx+2*w/3+margin, y0, x1-margin, y1)
    
    data.scarlet = PhotoImage(file = "imagesGIF\%d.gif" %0)
    data.mustard = PhotoImage(file = "imagesGIF\%d.gif" %1) 
    data.white = PhotoImage(file = "imagesGIF\%d.gif" %2)
    data.green = PhotoImage(file = "imagesGIF\%d.gif" %3)
    data.peacock = PhotoImage(file = "imagesGIF\%d.gif" %4)  
    data.plum = PhotoImage(file = "imagesGIF\%d.gif" %5)
    
    #location to character map
    data.initialCharac = {0:data.scarletSelectionBox, 1:data.mustardSelectionBox,
            2:data.whiteSelectionBox, 3:data.greenSelectionBox, 
            4:data.peacockSelectionBox, 5:data.plumSelectionBox}
    data.characImgs = {0:data.scarlet, 1:data.mustard, 2:data.white, 
            3:data.green, 4:data.peacock, 5:data.plum}


def mousePressed(event, data):
    if data.gameMode == 'start':
        data.characterPicked = None
        mousePressedStart(data, event.x, event.y)
        mousePressedRules(data, event.x, event.y)
    elif data.gameMode == 'select':
        data.characterPicked = None
        #data.characterPicked = 
        mousePressedInitialSelection(data, event.x, event.y)
        if data.characterPicked != None:
            setupGame(data.characterPicked, data)
    elif data.gameMode == 'play':
        data.checklist.mousePressed(event.x, event.y, data)
        if data.current == data.characterPicked and data.human.currentRoom != None:
            if data.buttons.inOkButtonBounds(event.x, event.y, data):
                data.nextTurn = True
                if data.gameStarted == False:
                    data.gameStarted = True
                playGame(data)
            
            data.checklist.mousePressed(event.x, event.y, data)
            data.buttons.mousePressedButtons(data, event)
            data.boardMap.mousePressedMove(event.x, event.y, data) #moving
            if data.humanMoved == True and data.human.currentRoom == None:
                playGame(data)
            data.buttons.mousePressedSuggestion(event.x, event.y, data)
            data.checklist.mousePressed(event.x, event.y, data)
            if (data.buttons.mousePressedSuggestionButton(event.x, event.y,data)
                and data.rolled == True): 
                if (data.buttons.selectedCharac == None or 
                        data.buttons.selectedWeapon == None 
                        or data.buttons.selectedRoom == None):
                    print('notValid')
                else:
                    data.currentSuggestion = (data.buttons.selectedCharac,
                    data.buttons.selectedWeapon, data.buttons.selectedRoom)
                    humanTurn(data)
                    data.pBeingMoved = data.currentSuggestion[0]
                    data.boardMap.moveSuggestedPlayer(data) 
    
        if not data.tellHumanToShow:
            data.checklist.mousePressed(event.x, event.y, data)
            data.buttons.mousePressedButtons(data, event)
            data.boardMap.mousePressedMove(event.x, event.y, data)
            if data.buttons.inOkButtonBounds(event.x, event.y, data):
                data.nextTurn = True
                if data.gameStarted == False:
                    data.gameStarted = True
                playGame(data)
        else:
            data.buttons.mousePressedOwnCards(event.x, event.y, data)
            if (data.selectedToShow != None and 
                data.selectedToShow in data.currentSuggestion):
                data.shown = data.selectedToShow
                data.tellHumanToShow = False
                humanJustDisproved(data)
                
    elif data.gameMode == 'accuse':
        mousePressedAccusation(event.x, event.y, data)

def keyPressed(event, data, canvas):
    if data.gameMode == 'rules':
        keyPressedRules(event, data)
    if data.gameMode == 'accuse':
        if event.keysym == 'space': 
            data.gameMode = 'play'
        if event.keysym == 's':
            #we submit and check if we are correct
            if data.selectedCharac != data.solution[0]:
               data.gameMode = 'lost'
            if data.selectedWeapon+6 != data.solution[1]:
               data.gameMode = 'lost'
            if data.selectedRoom+12 != data.solution[2]:
               data.gameMode = 'lost'
            else:
                data.gameMode = 'won'
    if data.gameMode == 'lost' or data.gameMode == 'won':
        if event.keysym == 'space':
            data.gameMode = 'start'
            init(data, canvas)
            
    if data.gameMode == 'AIaccusing': #AI messes up
        if event.keysym == 'space':
            data.gameMode = 'play'
            playGame(data)
        
            
def timerFired(data):
    pass

def redrawAll(canvas, data):
    canvas.create_image(data.width/2, data.height/2, image = data.image)
    #always in the background
    if data.gameMode == 'lost':
        drawLoseScreen(canvas, data)
    if data.gameMode == 'won':
        drawWinScreen(canvas, data)
    if data.gameMode == 'start':
        drawStartScreen(canvas, data)
    if data.gameMode == 'select':
        drawAllCharacters(canvas, data)
    if data.gameMode == 'rules':
        drawRulesScreen(canvas, data)
    if data.gameMode == 'play':
        data.board.draw(canvas)
        data.checklist.draw(canvas, data)
        data.buttons.drawAllButtons(canvas, data)
        if (data.current == data.characterPicked and data.rolled == True 
            and data.humanMoved == False):
            data.boardMap.drawPossibleSpots(data, canvas)
        data.boardMap.drawPlayers(canvas, data)
        if data.tellHumanToShow:
            data.buttons.drawDisproveScreen(canvas, data)
    if data.gameMode == 'accuse':
        data.board.draw(canvas)
        data.checklist.draw(canvas, data)
        data.buttons.drawAllButtons(canvas, data)
        data.boardMap.drawPossibleSpots(data, canvas)
        data.board.drawAllDoors(canvas)
        data.boardMap.drawPlayers(canvas, data)
        drawAccusationScreen(canvas, data)
    if data.gameMode == 'AIaccusing':
        data.board.draw(canvas)
        data.checklist.draw(canvas, data)
        data.buttons.drawAllButtons(canvas, data)
        data.boardMap.drawPlayers(canvas, data)
        if AIAccused(data):
            playGame(data)
        else:
            drawFalseAccusation(data, canvas)
            
################################
##Character Selection
################################

def drawAllCharacters(canvas, data):
    w, h, cx, cy = 600, 120, data.width/2, data.height/2 #dimensions and center
    margin = 20
    (x0, y0, x1, y1) = (cx-w, cy-h, cx+w, cy+h)
    canvas.create_text(cx, y0-2*margin, text='PICK YOUR CHARACTER', fill='cyan',
            font = 'Helvetica 40 bold')
    
    for character in data.initialCharac:
        (x0, y0, x1, y1) = data.initialCharac[character]
        canvas.create_rectangle(x0, y0, x1, y1, fill='white', width=0)
        canvas.create_image((x0+x1)/2, (y1+y0)/2, image=data.characImgs[character])
        
def mousePressedInitialSelection(data, x, y):
    data.characterPicked = None
    (x00, y00, x01, y01) = data.initialCharac[0]
    if (x00 <= x <= x01) and (y00 <= y <= y01):
        data.gameMode = 'play'
        data.characterPicked = 0
    (x10, y10, x11, y11) = data.initialCharac[1]
    if (x10 <= x <= x11) and (y10 <= y <= y11):
        data.gameMode = 'play'
        data.characterPicked = 1
    (x20, y20, x21, y21) = data.initialCharac[2]
    if (x20 <= x <= x21) and (y20 <= y <= y21):
        data.gameMode = 'play'
        data.characterPicked = 2
    (x30, y30, x31, y31) = data.initialCharac[3]
    if (x30 <= x <= x31) and (y30 <= y <= y31):
        data.gameMode = 'play'
        data.characterPicked = 3
    (x40, y40, x41, y41) = data.initialCharac[4]
    if (x40 <= x <= x41) and (y40 <= y <= y41):
        data.gameMode = 'play'
        data.characterPicked = 4
    (x50, y50, x51, y51) = data.initialCharac[5]
    if (x50 <= x <= x51) and (y50 <= y <= y51):
        data.gameMode = 'play'
        data.characterPicked = 5
 
########################
##AI Accusing
########################
def AIAccused(data):
    currPlayer = data.playerOrder[data.current] #actual player object
    if currPlayer.solution[0] != data.solution[0]:
        data.losers += [data.current]
        return False
    if currPlayer.solution[1] != data.solution[1]:
        data.losers += [data.current]
        return False
    if currPlayer.solution[2] != data.solution[2]:
        data.losers += [data.current]
        return False
    else:
        data.winner = data.current
        data.gameMode = 'lost'
        return True
        
def drawFalseAccusation(data, canvas):
    currPlayer = data.playerOrder[data.current] #actual player object
    w, h = 400, 300
    offs = 100 #off set for text
    cx, cy = data.width/2, data.height/2
    canvas.create_rectangle(cx-w, cy-h, cx+w, cy+h, fill = 'white', width = 0)
    msg = '%s wrongly accused' %data.characters[data.current]
    canvas.create_text(cx, cy-offs, text = msg, fill = 'red',
        font = 'Helvetica 25 bold')
    c = data.allCards[currPlayer.solution[0]]
    w = data.allCards[currPlayer.solution[1]]
    r = data.allCards[currPlayer.solution[2]]
    sol = " %s, %s, %s" %(c, w, r)    
    canvas.create_text(cx, cy+offs, text = sol, fill = 'red',
        font = 'Helvetica 20 bold')
    res = 'Press SPACE to keep playing'
    canvas.create_text(cx, cy+h-offs/2, text = res, fill = 'black',
        font = 'Helvetica 15')

#########################
## Start Screen
#########################
def drawStartButton(canvas, data):
    w = 150 #width
    h = 75 #height
    (x0, y0, x1, y1) = (data.width/2-w, data.height/2-h, data.width/2+w, 
        data.height/2+h)
    data.startButton = (x0, y0, x1, y1)
    canvas.create_rectangle(data.startButton,fill='red',width=5,outline='yellow')
    canvas.create_text((x0+x1)/2, (y1+y0)/2, text = "PLAY", fill='white', 
        font = 'Helvetica 30 bold')
        
def drawRulesButton(canvas, data):
    w = 200 #width
    h = 50 #height
    (x0, y0, x1, y1) = (data.width/2-w, data.height/2+2*h, data.width/2+w, 
        data.height/2+3*h)
    data.rulesButton = (x0, y0, x1, y1)
    canvas.create_rectangle(data.rulesButton,fill='orange',width=3,outline='blue')
    canvas.create_text((x0+x1)/2, (y1+y0)/2, text = "HOW TO PLAY", fill='white', 
        font = 'Helvetica 15 bold')
        
def mousePressedStart(data, x, y):
    (x0, y0, x1, y1) = data.startButton 
    if (x0 <= x <= x1) and (y0 <= y <= y1):
        data.gameMode = 'select'
        
def mousePressedRules(data, x, y):
    data.currentRulesScreen = 0
    (x0, y0, x1, y1) = data.rulesButton 
    if (x0 <= x <= x1) and (y0 <= y <= y1):
        data.gameMode = 'rules'

def drawStartScreen(canvas, data):
    drawStartButton(canvas, data)
    drawRulesButton(canvas, data)
 
#########################
### Lose Screen
#########################
def drawLoseScreen(canvas, data):
    w, h = 400, 300
    offs = 100 #off set for text
    cx, cy = data.width/2, data.height/2
    canvas.create_rectangle(cx-w, cy-h, cx+w, cy+h, fill = 'white', width = 0)
    canvas.create_text(cx, cy-offs, text = '¡YOU LOST!', fill = 'red',
        font = 'Helvetica 25 bold')
    c = data.allCards[data.solution[0]]
    w = data.allCards[data.solution[1]]
    r = data.allCards[data.solution[2]]
    sol = "The solution was %s, %s, %s" %(c, w, r)    
    canvas.create_text(cx, cy+offs, text = sol, fill = 'red',
        font = 'Helvetica 20 bold')
    res = 'Press SPACE to play again'
    canvas.create_text(cx, cy+h-offs/2, text = res, fill = 'black',
        font = 'Helvetica 15')
        
    if data.winner != None:
        winner = data.characters[data.current]
        msg = "%s won" %winner
        canvas.create_text(cx, cy-2*offs, text = msg, fill = 'red',
            font = 'Helvetica 20 bold')
        
############################
### Win Screen
############################
def drawWinScreen(canvas, data):
    w, h = 400, 300
    offs = 100 #off set for text
    cx, cy = data.width/2, data.height/2
    canvas.create_rectangle(cx-w, cy-h, cx+w, cy+h, fill = 'white', width = 0)
    canvas.create_text(cx, cy-offs, text = '¡YOU WON!', fill = 'blue',
        font = 'Helvetica 25 bold')
    c = data.allCards[data.solution[0]]
    w = data.allCards[data.solution[1]]
    r = data.allCards[data.solution[2]]
    sol = "The solution was %s, %s, %s" %(c, w, r)    
    canvas.create_text(cx, cy+offs, text = sol, fill = 'blue',
        font = 'Helvetica 20 bold')
    res = 'Press SPACE to play again'
    canvas.create_text(cx, cy-offs+h, text = res, fill = 'black',
        font = 'Helvetica 18')

        
#########################
## Initial Game Setup 
#########################
def placingInEnvelope(data):
    #selects one of each category for the solution
    char = random.randint(0, 5)
    weapon = random.randint(6, 11)
    room = random.randint(12, 20) 
    sol = [char, weapon, room]
    return sol
 
def randomAssignment(used, n, numOfCards):
    #randomly picks n cards, checking they haven't been picked already
    picked = []
    while len(picked) < n:
        a = random.randint(0, numOfCards-1)
        if a not in used:
            picked += [a]
            used += [a]
    return (used, picked)
      
def setupGame(characterPicked, data):
    data.time = 0
    data.numOfPlayers = 6
    data.characterPicked = characterPicked #todo
    data.current = data.numOfPlayers-1 #index in player order of current player
    data.currentSuggestion = None #todo
    data.disproveCount = None #who is disproving
    data.humanCanDisprove = False #if the human can disprove it
    data.shown = None
    data.nextTurn = False #wait before going to next turn 
    data.selectedToShow = None
    data.tellHumanToShow = False
    data.humanMoved = False
    data.pBeingMoved = False #person moved to another room
    data.winner = None
    data.disproved = True
    #initial locations: (by index in player order)   
    data.locations = [(23,7), (17,0), (0,9), (0,14), (6,23), (19,23)]
    data.checklist = Checklist(data)
    data.board = GameBoard(data)
    data.boardMap = BoardMap(data)
    data.buttons = Buttons(data)
    data.roll = 6
    data.rolled = False #hooman hasn't rolled yet
    data.moved = False
    data.gameStarted = False
    data.losers = []
    
    data.selectedCharac = None #for accusations
    data.selectedWeapon = None
    data.selectedRoom = None

    numCardsPerPlayer = data.numOfCards//data.numOfPlayers
    usedCards = [] #cards that have been assigned
    
    #places cards in envelope: 'solution'
    envelope = placingInEnvelope(data)
    data.solution = envelope
    usedCards += envelope
    print(data.solution)
    
    data.human = Human(data, characterPicked)
    #initializing 5 AI players:
    data.p1 = AIPlayer(data, 1)
    data.p2 = AIPlayer(data, 2)
    data.p3 = AIPlayer(data, 3)
    data.p4 = AIPlayer(data, 4)
    data.p5 = AIPlayer(data, 5)
    
    order = [data.p1, data.p2, data.p3, data.p4, data.p5] 
    data.playerOrder = order[:characterPicked] + [data.human] + order[characterPicked:]
    #they go in that order

    for player in data.playerOrder:
        Cards = randomAssignment(usedCards,numCardsPerPlayer,data.numOfCards)
        usedCards += Cards[0]
        player.inputInitialInfo(data, Cards[1])
        i = data.playerOrder.index(player)
        player.setInitialLocation(data, data.locations[i][0], data.locations[i][1])
        #gives different cards to each one

    data.img1 = PhotoImage(file = "imagesGIF\%d.gif" %data.human.cards[0])
    data.img2 = PhotoImage(file = "imagesGIF\%d.gif" %data.human.cards[1]) 
    data.img3 = PhotoImage(file = "imagesGIF\%d.gif" %data.human.cards[2])
    data.cardImgs = [data.img1, data.img2, data.img3]
 
    
###################################
## game loop
###################################

def playGame(data):
    if data.gameStarted: #game has started
        data.disproved = True
        data.humanMoved = False
        data.disproveCount = None
        data.selectedToShow = None
        data.tellHumanToShow = False
        data.humanCanDisprove = False
        data.shown = None
        data.current = (data.current+1)%data.numOfPlayers
        while data.current in data.losers: #skip the losers
            data.current = (data.current+1)%data.numOfPlayers
        currPlayer = data.playerOrder[data.current] #actual player object
        currPlayer.analyseMemory(data)
        data.roll = random.randint(1,6)
        data.boardMap.allPaths = dict()
        data.boardMap.possibleRooms = dict()
        row, col = data.locations[data.current][0], data.locations[data.current][1]
        data.boardMap.getSpots(data, data.roll, row, col)
        data.boardMap.getPossibleRooms(data)
        
        if currPlayer != data.human: #AI
            currPlayer.analyseMemory(data) #todo
            if currPlayer.makeAccusation(data):
                data.gameMode = 'AIaccusing'
            currPlayer.findPathThroughRooms(data)
            currPlayer.movement(data)
            #currPlayer.findPathThroughRooms(data)
            
            if data.gameMode != 'AIaccusing': #AI is not accusing
                if currPlayer.currentRoom != None:
                    data.currentSuggestion = currPlayer.makeSuggestion(data) #suggest
                    data.pBeingMoved = data.currentSuggestion[0]
                    data.boardMap.moveSuggestedPlayer(data) 
                    data.disproveCount = (data.current+1)%data.numOfPlayers
                    
                    for card in data.currentSuggestion:
                        if card in data.human.cards: #hooman can disprove
                            data.humanCanDisprove = True
                    
                    if data.humanCanDisprove:
                        while (data.shown == None and 
                            data.disproveCount != data.characterPicked):
                            player = data.playerOrder[data.disproveCount]
                            player.disprove(data)
                            data.disproveCount = (data.disproveCount+1)%data.numOfPlayers
                        if data.shown == None: #no one else disproved it
                            data.tellHumanToShow = True 
    
                    else:
                        while data.shown == None and data.disproveCount != data.current:
                            #disprove cycle
                            player = data.playerOrder[data.disproveCount]
                            player.disprove(data)
                            data.disproveCount = (data.disproveCount+1)%data.numOfPlayers
                            
                    data.disproveCount = (data.disproveCount-1)%data.numOfPlayers 
                    #remove off by one from loop
                    personDisproved=data.playerOrder[data.disproveCount]
                    
                    if data.shown != None: #it was disproved
                        currPlayer.inputNewInfo(data, data.currentSuggestion,
                                personDisproved, True, data.shown)
                        for player in data.playerOrder:
                            #everyone adds it to memory
                            player.memory(data, data.currentSuggestion,
                                    currPlayer, personDisproved)
                    elif data.shown == None and data.humanCanDisprove == False: 
                    #it wasn't disproved and hooman can't disprove
                        for person in data.playerOrder:
                            currPlayer.inputNewInfo(data, data.currentSuggestion,
                                    person, False) #input that no one has it
                    currPlayer.analyseMemory(data)          
                    data.shown = None #resetting for next
                
                else:
                    if data.rolled == True:
                        data.rolled = False
                    data.currentSuggestion = None
        
        if data.nextTurn: #go on to next player
            data.nextTurn = False
            data.rolled = False
            
def humanTurn(data):
    data.disproveCount = (data.current+1)%data.numOfPlayers
    while data.shown == None and data.disproveCount != data.current:
        #disprove cycle
        player = data.playerOrder[data.disproveCount]
        player.disprove(data)
        data.disproveCount = (data.disproveCount+1)%data.numOfPlayers
    #remove offset by one
    if data.shown == None:
        data.disproved = False
    data.disproveCount = (data.disproveCount-1)%data.numOfPlayers
    (data.buttons.selectedCharac, data.buttons.selectedWeapon,
        data.buttons.selectedRoom) = (None, None, None)
    
def humanJustDisproved(data):
    currPlayer = data.playerOrder[data.current] #actual player object
    data.shown = data.selectedToShow
    data.tellHumanToShow = False
    
    currPlayer.inputNewInfo(data, data.currentSuggestion,
            data.human, True, data.shown)
    for player in data.playerOrder:
        #everyone adds it to memory
        player.memory(data, data.currentSuggestion,
                currPlayer, data.human)

    currPlayer.analyseMemory(data) 
    currPlayer.checkForSolution(data)  
    data.shown = None #resetting for next
    playGame(data)
    
####################################
## run function modified from notes
####################################

def runGame(width=900, height=600):
    # Set up data and call init
    root = Toplevel()
    app = FullScreenApp(root)
    class Struct(object): pass
    data = Struct()
    data.image = PhotoImage(file = 'Clue_bg.gif')
    data.width = root.winfo_screenwidth()
    data.height = root.winfo_screenheight()
    data.timerDelay = 100 # milliseconds
    data.gameMode = 'start'
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    init(data, canvas) 
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data, canvas)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    if data.gameMode == 'play':
        playGame(data) 
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

runGame()
