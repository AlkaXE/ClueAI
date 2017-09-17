##AI Players Skeleton
# AI was inspired by Douglas Selent, all code is original or taken from class notes
# http://www.rivier.edu/journal/roaj-fall-2011/j550-clue-selent.pdf

from print2dList import *
import random

class AIPlayer(object):
    #taken from notes http://www.cs.cmu.edu/~112/schedule.html
    @staticmethod
    def make2dList(rows, cols):
        a=[]
        for row in range(rows): a += [[None]*cols]
        return a
    
    def __init__(self, data, n):
        #initially has no information, just things to keep track of it
        self.cards = []
        self.checklist = AIPlayer.make2dList(data.numOfCards, data.numOfPlayers)
        self.othersSuggestions = dict()
        self.num = n #which number of player it is in checklist
        self.suggestions = dict() #all suggestions + who made + who disproved
        self.disproves = dict() #what each person has disproved
        self.solution = [None, None, None] #character, weapon, room 
        self.unknownRoom = set() #cards it has no information on
        self.unknownCharac = set()
        self.unknownWeapon = set()
        self.inEnvelope = set()
        self.notInEnvelope = set()
        self.currentRoom = None 
        self.location = None #each piece starts in a different location
        self.shown = dict()
        self.roomsInfo = {13:[(17,0),(14,3)], 14:[(13,3),(16,6)], 15:[(20,0),(16,6)],
                16:[(17,3),(18,5),(15,6),(14,6)], 17:[(13,0),(16,3),(18,6)],
                18:[(19,3),(16,5),(17,6)], 19:[(18,3),(20,6),(12,6)], 
                20:[(15,0),(12,3),(19,6)], 12:[(20,3),(19,6)]}
     
    def setInitialLocation(self, data, row, col):
        self.location = (row, col)
        
    def inputInitialInfo(self, data, cards):
        #called at the start to put the first cards in
        self.cards = cards
        for card in range(data.numOfCards):
            self.checklist[card][self.num] = data.cardNot + self.num
        for card in cards:
            for otherPlayer in range(data.numOfPlayers):
                self.checklist[card][otherPlayer] = data.cardNot + otherPlayer
            self.checklist[card][self.num] = self.num
            
        self.shown = {self.cards[0]:[], self.cards[1]:[], self.cards[2]:[]}

    def memory(self, data, suggestion, personMade, personDisproved):
        #tracks who made and who disproved suggestions
        if (personMade, personDisproved) in self.suggestions:
            self.suggestions[(personMade, personDisproved)].add(suggestion)
        else: self.suggestions[(personMade, personDisproved)] = {suggestion}
        
        #tracks what each person disproved
        if personDisproved in self.disproves:
            self.disproves[personDisproved].add(suggestion)
        else: self.disproves[personDisproved] = {suggestion}
        
        return (self.suggestions, self.disproves)
        
    def analyseMemory(self, data):
        #what cards some people don't have
        self.foundAll(data)
        self.checkKnown(data)
        for pair in self.suggestions:
            peopleBetween = [] #the people that didn't disprove it
            personMade, personDisproved = pair[0], pair[1]
            start = (data.playerOrder.index(personMade)+1)%data.numOfPlayers
            end = data.playerOrder.index(personDisproved)
            while start != end:
                peopleBetween += [data.playerOrder[start]]
                start = (start+1)%data.numOfPlayers
            for suggestion in self.suggestions[pair]:
                if len(peopleBetween) > 0:
                    for person in peopleBetween:
                        if person != None:
                            self.inputNewInfo(data, suggestion, person, False)
        
        if len(self.disproves) != 0: 
            #print(self.disproves)
            #what cards some people must have:
            for person in self.disproves:
                for suggestion in self.disproves[person]:
                    notCounter = 0 #cards they dont have
                    for card in suggestion:
                        if (isinstance(person.num, int) and
                            isinstance(card, int) and
                            self.checklist[card][person.num] != None and
                            self.checklist[card][person.num] >= data.cardNot):
                            notCounter += 1
                    if notCounter == 2: 
                    #doesn't have two of those cards, must have third
                        for card in suggestion:
                            if self.checklist[card][person.num] == None:
                                self.inputNewInfo(data, suggestion, person, True, card)
        self.foundAll(data)
        return self.checklist
        
    def foundAll(self, data):
        #we know all of one players cards
        for player in range(data.numOfPlayers):
            cardCount = 0
            for card in range(data.numOfCards):
                if (isinstance(self.checklist[card][player], int) and
                self.checklist[card][player] < data.cardNot):
                    #the player has the card
                    cardCount += 1

            if cardCount == data.numOfCards//data.numOfPlayers: #cardsperplayer
                #we already know all the cards it has
                for card in range(data.numOfCards):
                    if self.checklist[card][player] == None:
                        self.checklist[card][player] = data.cardNot + player
                        
        return self.checklist
                
    def inputNewInfo(self, data, suggestion, other, disproved, card = None):
        #called mutliple times after suggestions are made
        if disproved: 
            #which was disproved?
            for player in range(data.numOfPlayers):
                if self.checklist[card][player] == None:
                    self.checklist[card][player] = data.cardNot + player
                self.checklist[card][other.num] = other.num
            
        if not disproved:
            #the other player doesn't have it 
            for card in suggestion:
                if card != None and self.checklist[card][other.num] == None:
                    self.checklist[card][other.num] = data.cardNot + other.num
                
        return self.checklist
        
    def checkKnown(self, data):
        #checks what cards we know about 
        for card in range(data.numOfCards):
            if None in self.checklist[card]: #we don't have all the information
                if card in data.characRange: self.unknownCharac.add(card)
                elif card in data.weaponsRange: self.unknownWeapon.add(card)
                else: self.unknownRoom.add(card)
                
            counter = 0 #counts how many don't have the card
            for person in range(data.numOfPlayers):
                if (isinstance(self.checklist[card][person], int) and
                    self.checklist[card][person] == person): 
                    #someone has the card
                    self.notInEnvelope.add(card)
                    #we now know about the card
                    if card in self.unknownCharac:
                        self.unknownCharac.remove(card)
                    elif card in self.unknownWeapon:
                        self.unknownWeapon.remove(card)
                    elif card in self.unknownRoom:
                        self.unknownRoom.remove(card)
                elif (isinstance(self.checklist[card][person], int) and
                    self.checklist[card][person] >= data.cardNot):
                    counter += 1
    
            if counter == data.numOfPlayers: #no one has it
                self.inEnvelope.add(card)
                if card in self.unknownCharac:
                    self.unknownCharac.remove(card)
                elif card in self.unknownWeapon:
                    self.unknownWeapon.remove(card)
                elif card in self.unknownRoom:
                    self.unknownRoom.remove(card) #todo
                    
        for card in self.unknownRoom: #double check we've removed everything
            if card in self.inEnvelope:
                self.unknownRoom.remove(card)
        for card in self.unknownCharac: 
            if card in self.inEnvelope:
                self.unknownCharac.remove(card)
        for card in self.unknownWeapon: 
            if card in self.inEnvelope:
                self.unknownWeapon.remove(card)
                        
    def checkForSolution(self, data):
        self.checkKnown(data)
        #fill in solution
        for card in self.inEnvelope:
            if card in data.characRange: self.solution[0] = card
            elif card in data.weaponsRange: self.solution[1] = card
            else: self.solution[2] = card
            
        #if it is the only one we don't know about it must be the solution
        if len(self.unknownCharac) == 1 and self.solution[0] == None:
            self.solution[0] = list(self.unknownCharac)[0]
        elif len(self.unknownWeapon) == 1 and self.solution[1] == None:
            self.solution[1] = list(self.unknownWeapon)[0]
        elif len(self.unknownRoom) == 1 and self.solution[2] == None:
            self.solution[2] = list(self.unknownRoom)[0]
            
        return self.solution #todo
     
    #priority cards idea taken from Selent 
    def getPriorityGroups(self, data, unknownList):
        #puts things in repective priority list
        g5 = []
        g3 = []
        g2 = []
        for card in unknownList:
            noneCounter = 0
            for player in range(data.numOfPlayers):
                if self.checklist[card][player] == None:
                    noneCounter += 1
            if noneCounter == data.numOfPlayers-1:
                g2 += [card]
            elif noneCounter == 1: #only one person could have it 
                g5 += [card]
            else: g3 += [card]
            
        return (g5, g3, g2)
        
    def setDeckWithPriority(self, data, g5, g3, g2):
        #setting up deck to pick from, will be biased toward g5
        deck = []
        for card in g5:
            deck += [card]*5 
        #the fixed priority numbers, dont cahnge regardless of num of players
        for card in g3:
            deck += [card]*3
        for card in g2:
            deck += [card]*2
        
        return deck
    
    def characterKnown(self, data):
        # if we've already found the winning character
        groups = self.getPriorityGroups(data, list(self.unknownWeapon))
        priorityGroup5 = groups[0]
        priorityGroup3 = groups[1]
        priorityGroup2 = groups[2]
        #setting up deck to pick from 
        deck = self.setDeckWithPriority(data, priorityGroup5, priorityGroup3,
            priorityGroup2)
        if len(deck) > 0: #precaution
            chosenWeaponCard = random.choice(deck)
        else: chosenWeaponCard = random.randint (6,11)
        #now it needs to pick a character to force the weapon:
        ownPeople = []
        for card in data.characRange:
            if card in self.cards:
                ownPeople += [card]
        if ownPeople != []: #we have a person card
            chosenCharacCard = random.choice(ownPeople)
        else:
            chosenCharacCard = self.solution[0] #the winning card must be chosen
            
        return (chosenCharacCard, chosenWeaponCard)
        
    def weaponKnown(self, data):
        # if we've already found the winning weapon, follows same pattern
        groups = self.getPriorityGroups(data, list(self.unknownCharac))
        priorityGroup5 = groups[0]
        priorityGroup3 = groups[1]
        priorityGroup2 = groups[2]
        #setting up deck to pick from 
        deck = self.setDeckWithPriority(data, priorityGroup5, priorityGroup3,
            priorityGroup2)
        if len(deck) > 0: #precaution
            chosenCharacCard = random.choice(deck)
        else: chosenCharacCard = random.randint(0,5)
        #now it needs to pick a weapon to force the character:
        ownWeapons = []
        for card in data.weaponsRange:
            if card in self.cards:
                ownWeapons += [card]
        if ownWeapons != []: #we have a weapon card
            chosenWeaponCard = random.choice(ownWeapons)
        else:
            chosenWeaponCard = self.solution[0] #the winning card must be chosen
            
        return (chosenCharacCard, chosenWeaponCard)
    
    def characterWeaponNotKnown(self, data):
        #we don't know either the person or the weapon
        characGroups = self.getPriorityGroups(data, list(self.unknownCharac))
        characG5 = characGroups[0]
        characG3 = characGroups[1]
        characG2 = characGroups[2] #same process
        characDeck = self.setDeckWithPriority(data, characG5, characG3, characG2)
        if len(characDeck) > 0: #precaution
            chosenCharacCard = random.choice(characDeck)
        else: chosenCharacCard = random.randint(0,5)
        #we need to do the same for the weapons
        weaponGroups = self.getPriorityGroups(data, list(self.unknownWeapon))
        weaponG5 = weaponGroups[0]
        weaponG3 = weaponGroups[1]
        weaponG2 = weaponGroups[2]
        weaponDeck = self.setDeckWithPriority(data, weaponG5, weaponG3, weaponG2)
        if len(weaponDeck) > 0:
            chosenWeaponCard = random.choice(weaponDeck)
        else: chosenWeaponCard = random.randint(6,11)

        return (chosenCharacCard, chosenWeaponCard)
    
    #idea taken from Selent   
    def calculateIsolatePercentage(self, data):
        #number of rooms is fixed, so each number below never changes
        numOfRooms = 9
        roomsKnown = numOfRooms - len(self.unknownRoom) 
        if roomsKnown <= 2:
            isolatePercentage = 25
        elif roomsKnown == 3:
            isolatePercentage = 50
        elif roomsKnown == 4:
            isolatePercentage = 75
        else: isolatePercentage = 100
        return isolatePercentage
        
    def findDistanceToFurthestUnknown(self, data, card):
        #find out how far we must go without being disproved
        furthestUnknown = None
        playerIndex = data.playerOrder.index(self)
        i = (playerIndex+1)%data.numOfPlayers #i is its position in player order
        
        while i != playerIndex:
            if self.checklist[card][data.playerOrder[i].num] == None:
                furthestUnknown = i 
                #furthestUnknown will be the index in the order of furthestUnkwnPlyr
            i = (i+1)%data.numOfPlayers
            
        if furthestUnknown != None:
            distance = furthestUnknown - playerIndex
            if distance < 0: distance += data.numOfPlayers 
        else: distance = 0
        return distance
        
    def findDistanceToFirstUnknown(self, data, card):
        distance = 0
        playerIndex = data.playerOrder.index(self)
        i = (playerIndex+1)%data.numOfPlayers #i is its position in player order
        
        while (self.checklist[card][data.playerOrder[i].num] != None and
                i != playerIndex): #we haven't found a none yet
                    distance += 1
                    i = (i+1)%data.numOfPlayers
        return distance
        
    def pickingCardToIsolateWith(self, data, roomDistance, cards, ownList, unknowns):
        if ownList != []: #we have a card to isolate with
            chosenCard = random.choice(ownList)
        else: #we have to find the furthest with no nones
            furthestCard = [] #initalize
            furthestDist = -1
            for card in cards:
                dist = self.findDistanceToFirstUnknown(data, card)
                if dist > furthestDist:
                    furthestCard = [card]
                    furthestDist = dist
                elif dist == furthestDist:
                    furthestCard += [card]

            if furthestDist <= roomDistance: #we can't assure that we've isolated it 
                #we have to chose from the ones we don't know about
                for card in furthestCard:
                    if card not in unknowns:
                        furthestCard.remove(card)
           
                        
            if furthestCard != []: #precaution
                chosenCard = random.choice(furthestCard)
            else: #assured to pick something valid
                if len(unknowns) != 0:
                    chosenCard = random.choice(list(unknowns))
                else: chosenCard = random.choice(list(cards))
                    
        return chosenCard       
     
    #idea taken from Selent 
    def isolateRoom(self, data):
        roomDistance = self.findDistanceToFurthestUnknown(data, self.currentRoom)
        #isolate with own cards
        ownCharac = []
        ownWeapons = []
        for card in data.characRange:
            if card in self.cards:
                ownCharac += [card]
        for card in data.weaponsRange:
            if card in self.cards:
                ownWeapons += [card]

        chosenCharacCard = self.pickingCardToIsolateWith(data, roomDistance,
                    data.characRange, ownCharac, self.unknownCharac)
        chosenWeaponCard = self.pickingCardToIsolateWith(data, roomDistance,
                    data.weaponsRange, ownWeapons, self.unknownWeapon)
            
        return (chosenCharacCard, chosenWeaponCard)
        
    def makeSuggestion(self, data):
        self.checkKnown(data)
        self.analyseMemory(data)
        self.checkForSolution(data)
        room = self.currentRoom #can only suggest current room
        if room in self.unknownRoom:
            num = random.randint(1,100) 
            probabilityIsolateRoom = self.calculateIsolatePercentage(data)/num
        else: probabilityIsolateRoom = 0 #we would make a useless suggestion otherwise
            
        if probabilityIsolateRoom >= 1:
            charac = self.isolateRoom(data)[0]
            weapon = self.isolateRoom(data)[1]
        elif self.solution[0] != None: #we've found the character
            charac = self.characterKnown(data)[0]
            weapon = self.characterKnown(data)[1]
        elif self.solution[1] != None: #we've found the weapon
            charac = self.weaponKnown(data)[0]
            weapon = self.weaponKnown(data)[1]
        else:
            charac = self.characterWeaponNotKnown(data)[0]
            weapon = self.characterWeaponNotKnown(data)[1]
        
        if charac == None:
            charac = random.choice(data.characRange)
        if weapon == None:
            weapon = random.choice(data.weaponsRange)
        if room == None:
            room = random.choice(data.roomsRange)
        
        return (charac, weapon, room)
        
    def disprove(self, data):
        currPlayer = data.playerOrder[data.current] #actual player object
        canShow = []
        for card in data.currentSuggestion:
            if card in self.cards:
                canShow += [card] #cards that would disprove it
        if len(canShow) == 0: return None #can't disprove
        elif len(canShow) == 1: #only has one option to disprove
            data.shown = canShow[0]
            self.shown[canShow[0]] += [currPlayer.num]
            return canShow[0]
        else:
            for card in canShow: #if it has already been shown show again
                if currPlayer.num in self.shown[card]:
                    data.shown = card
                    self.shown[data.shown] += [currPlayer.num]
                    return card
            #if it has shown it to more than half, show 
            mostShown = None
            minShownNum = data.numOfPlayers//2
            for card in canShow:
                numShown = len(self.shown[card])
                if numShown >= minShownNum:
                    data.shown = card
                    self.shown[data.shown] += [currPlayer.num]
                    return card
                    
            showDeck = []
            for card in canShow:
                if card in data.roomsRange:
                    showDeck += [card]*2 #creating a biased deck
                else: showDeck += [card]*8
            data.shown = random.choice(showDeck)
            self.shown[data.shown] += [currPlayer.num]
            return card
            
    def makeAccusation(self, data):
        for card in self.solution:
            if card == None:
                return False
        else:
            return True
    
    def setLocation(self, data): 
        i = data.playerOrder.index(self)
        self.location = data.locations[i]
        pass
        
        
    def findPathThroughRooms(self, data, room = None):
        #we only need rooms two edges away if already in a room
        pathsThroughRooms = dict()
        if self.currentRoom != None:
            node1 = self.currentRoom
        elif room == None:
            return
        for roomPair1 in self.roomsInfo[node1]:
            node2 = roomPair1[0]
            dist2 = roomPair1[1]
            for roomPair2 in self.roomsInfo[node2]:
                node3 = roomPair2[0]
                dist3 = roomPair2[1]
                pathsThroughRooms[dist2+dist3] = [node1, node2, node3]
                #all paths of leng 2
        
        viablePaths = dict ()
        for path in pathsThroughRooms:
            node2 = pathsThroughRooms[path][1]
            if node2 in data.boardMap.possibleRooms:
                viablePaths[path] = pathsThroughRooms[path]
                #paths it could actually follow
        
        wantedPaths = dict()
        for path in viablePaths:
            node3 = viablePaths[path][2]
            if node3 in self.unknownRoom:
                wantedPaths[path] = viablePaths[path]
        return (viablePaths, wantedPaths)
            
        
    def movement(self, data):
        #we never want to waste a turn
        choices = []
        rooms = []
        betterRooms = [] #rooms it can go to that it needs
        pick = None
        if len(data.boardMap.possibleRooms) >= 1: #it can go to a room
            for room in data.boardMap.possibleRooms: #can't stay in same room
                if room != self.currentRoom:
                    rooms += [room]
            for room in rooms:
                if room in self.unknownRoom:
                    betterRooms += [room]
                    
            if betterRooms != []:
                room = random.choice(betterRooms) #move to room it needs info on
            else:
                if self.currentRoom != None:
                    wantedPaths = self.findPathThroughRooms(data)[1]
                    viablePaths = self.findPathThroughRooms(data)[0]
                    shortestDist = 100 #sentinel value
                    if wantedPaths != dict():
                        for dist in wantedPaths: #keys in the path
                            if dist < shortestDist:
                                shortestDist = dist
                    elif viablePaths != dict():
                        for dist in viablePaths:
                            if dist < shortestDist:
                                shortestDist = dist
                    if shortestDist != 100: #we do have a valid key
                        room = viablePaths[shortestDist][1]
                else: #just go to a room to get weapons or characters
                    room = random.choice(rooms)
                    
            #now we send it to the room
            self.currentRoom = room
            pick = data.boardMap.locationsInRooms[room][data.current]
            
        else: #it can't go to a room
            shortestDist = 100 #sentinel value
            if len(self.unknownRoom) != 0:
                for spot in data.boardMap.allPaths:
                    x0, y0 = spot
                    for room in self.unknownRoom:
                        for door in data.boardMap.doorsCoords[room]:
                            x1, y1 = door
                            dist = abs(x0-x1)+abs(y0-y1)
                            if dist < shortestDist:
                                shortestDist = dist
                                pick = spot
            else: #we know all rooms, unlikely
                for spot in data.boardMap.allPaths:
                    x0, y0 = spot
                    for room in self.doorsCoords:
                        for door in data.boardMap.doorsCoords[room]:
                            x1, y1 = data.boardMap.doorsCoords[room][door]
                            dist = abs(x0-x1)+abs(y0-y1)
                            if dist < shortestDist:
                                shortestDist = dist
                                pick = spot
                
        if pick == None: #precaution
            row, col = data.locations[data.current][0], data.locations[data.current][1]
            data.boardMap.getSpots(data, data.roll, row, col)
            for choice in data.boardMap.allPaths:
                choices += [choice]
            pick = random.choice(choices)
            self.currentRoom = None
             
        data.locations[data.current] = pick
            
    def __repr__(self):
        print2dList(self.checklist)
        return str((self.num, self.cards))