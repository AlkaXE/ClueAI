##Human
from AIPlayer import *
from tkinter import *
import random

class Human(AIPlayer):
    #taken from notes
    @staticmethod
    def make2dList(rows, cols):
        a=[]
        for row in range(rows): a += [[None]*cols]
        return a
        
    def __init__(self, data, charac):
        super().__init__(data, 0) 
        cols = 6
        self.checklist = Human.make2dList(data.numOfCards, cols)
        self.character = charac
        self.num = 0
        self.currentRoom = None #TODO
        self.orderNum = None 
        #self.rolled = False
        
    def rollDie(self, data):
        if data.rolled == False:
            data.rolled = True
            return random.randint(1,6)
        else: return data.roll
        

        