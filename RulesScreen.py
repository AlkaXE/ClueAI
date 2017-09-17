##EVERUTHING FOR THE RULES
#Rules taken from http://www.cs.nmsu.edu/~kcrumpto/TAClasses/ClueRules.html 

def drawRulesScreen(canvas, data):
    w, h, cx, cy = 500, 300, data.width/2, data.height/2 #dimensions and center
    bottomMargin = 20
    topMargin = 30
    sideMargin = 20
    (x0, y0, x1, y1) = (cx-w, cy-h, cx+w, cy+h)
    data.rulesScreen = (x0, y0, x1, y1)
    canvas.create_rectangle(data.rulesScreen, fill='white', width=0)
    retMsg = 'Press SPACE to return or RIGHT and LEFT to see more'
    canvas.create_text(cx, y1-bottomMargin, text = retMsg, font = 'Helvetica 13')
    title = 'How to Play Clue'
    canvas.create_text(cx, y0+topMargin, text = title, fill = 'DeepPink4',
            font = 'Helvetica 20 bold')
    
    if data.currentRulesScreen == 0: #first screen
        retMsg = 'RIGHT'
        canvas.create_text(x1-2*sideMargin, y1-bottomMargin, text = retMsg, 
                font = 'Helvetica 13')
        msg1 = 'Welcome to Tudor Mansion.'
        msg2 = '''
        Your host, Mr. John Boddy, has met an untimely end-he is the 
          victim of foul play. To win this game, you must determine
                    the answer to these three questions:'''
        q1 = 'Who done it?'
        q2 = 'Where?'
        q3 = 'With what weapon?'
                    
        canvas.create_text(cx, y0+3*topMargin, text = msg1, fill = 'black',
            font = 'Helvetica 18 bold')
        canvas.create_text(cx, y0+5*topMargin, text = msg2, fill = 'black',
            font = 'Helvetica 18')
        canvas.create_text(cx, y0+8*topMargin, text = q1, fill = 'turquoise4',
            font = 'Helvetica 18 bold')
        canvas.create_text(cx, y0+9*topMargin, text = q2, fill = 'turquoise4',
            font = 'Helvetica 18 bold')
        canvas.create_text(cx, y0+10*topMargin, text = q3, fill = 'turquoise4',
            font = 'Helvetica 18 bold')
        msg3 = '''
          To do this pick your character and move about the board 
        asking questions to find out which cards are in the Case File'''
        canvas.create_text(cx, y0+12*topMargin, text = msg3, fill = 'black',
            font = 'Helvetica 18')
            
    elif data.currentRulesScreen == 1: #second screen
        margin= 20
        rMsg = 'RIGHT'
        canvas.create_text(x1-2*sideMargin, y1-bottomMargin, text = rMsg, 
                font = 'Helvetica 13')
        lMsg = 'LEFT'
        canvas.create_text(x0+2*sideMargin, y1-bottomMargin, text = lMsg, 
                font = 'Helvetica 13')
        msg1 = 'The game has six characters'
        c1, c2, c3 = 'Miss Scarlet', 'Colonel Mustard', 'Mrs. White'
        c4, c5, c6 = 'Mr. Green', 'Mrs. Peacock', 'Professor Plum '
        #all numbers are fixed locations on screen
        canvas.create_text(cx, y0+3*margin, text = msg1, fill = 'black',
            font = 'Helvetica 15')
        canvas.create_text(cx-margin*8, y0+4*margin+5, text = c1, fill = 'red3',
            font = 'Helvetica 15 ')
        canvas.create_text(cx, y0+4*margin+5, text = c2, fill = 'gold2',
            font = 'Helvetica 15 ')
        canvas.create_text(cx+margin*8, y0+4*margin+5, text = c3, fill = 'black',
            font = 'Helvetica 15 ')
        canvas.create_text(cx-margin*8, y0+5*margin+5, text = c4, fill = 'green4',
            font = 'Helvetica 15 ')
        canvas.create_text(cx, y0+5*margin+5, text = c5, fill = 'blue',
            font = 'Helvetica 15 ')
        canvas.create_text(cx+margin*8, y0+5*margin+5, text = c6, fill = 'purple4',
            font = 'Helvetica 15 ')
        msg2 = '''
        As well as six weapon cards: Knife, Revolver, Rope, Candlestick, Lead Pipe, and
        Wrench, and nine room cards. The rooms are (in counterclockwise order starting 
        from the top left corner) Kitchen, Ballroom, Conservatory, Billiard Room,
        Library, Study, Hall, Lounge, and Dining Room. There is a die and a checklist
        for you to go marking your information. At the start of the game one weapon,
        one character, and one room are chosen at random and are the facts of the
        case. The remaining cards are distributed amongst the players. The first player
        to move is Miss Scarlet and it goes in counterclockwise order (so Colonel
        Mustard is next)'''
        canvas.create_text(cx, y0+13*margin, text = msg2, fill = 'black',
            font = 'Helvetica 15 ')
            
    elif data.currentRulesScreen == 2:
        rMsg = 'RIGHT'
        canvas.create_text(x1-2*sideMargin, y1-bottomMargin, text = rMsg, 
                font = 'Helvetica 13')
        lMsg = 'LEFT'
        canvas.create_text(x0+2*sideMargin, y1-bottomMargin, text = lMsg, 
                font = 'Helvetica 13')
        msg1 = '''
On each turn, try to reach a different room of the mansion. To start your turn roll 
the dice and move that many squares or use a Secret Passages in the corner rooms 
which take you  the opposite corner (all possible spots are marked on the board).
There are three ways of entering a room: 
 (1) Moving your token along the squares entering through a doorway 
 (2) Via the Secret Passages by leaping across the board, corner to corner
 (3) A player's token may be placed in a room by another player in the feature 
 play known as "The Suggestion." 

 On the throw of the die, you may enter a Room by the doors only, but you cannot 
 leave a room on the same turn.  Entering a Room ends your move. It is not 
 necessary to throw the exact number to enter a Room. That is, if you need 4 to get
 into a room and you have thrown a 6, ignore the last two units after entering 
 the Room.'''
        canvas.create_text(cx, cy, text = msg1, fill = 'black',
            font = 'Helvetica 13 ')
            
    elif data.currentRulesScreen == 3:
        rMsg = 'RIGHT'
        canvas.create_text(x1-2*sideMargin, y1-bottomMargin, text = rMsg, 
                font = 'Helvetica 13')
        lMsg = 'LEFT'
        canvas.create_text(x0+2*sideMargin, y1-bottomMargin, text = lMsg, 
                font = 'Helvetica 13')
        msg1 = '''
As soon as you enter a room, make a Suggestion. By making Suggestions, you try to
determine - by process of elimination -- which three cards are in the confidential
Case File envelope.  To make a Suggestion, move a Suspect into the Room that you just
entered.  Then suggest that the crime was committed in that Room, by that Suspect, 
with some Weapon.

Example:  Let's say that you're Miss Scarlet and you enter the Lounge. First move
another Suspect -- Mr. Green, for instance --  into the Lounge and say "I suggest 
that the crime was committed in the Lounge, by Mr. Green with the Wrench."

Remember two things: 
   1.  You must be in the Room that you mention in your Suggestion. 
   2.  Be sure to consider all tokens -- including spare Suspects and yourself! -- 
   as falling under equal suspicion.

As soon as you make a Suggestion, your opponents, in turn, try to prove it false. 
The first to try is the player to your immediate left.  This player looks at his or
her cards to see if one of the three cards you just named is there.  If the player 
has one or more of these cards, he or she must show it to you and no one else.  If 
the player has more than one of the cards named, he or she select just one to show you.

If that opponent does not have any of the three cards, then the next player at his 
left examines his cards and must show one of the three if he has it. 

The opportunity to prove the Suggestion false passes to the left until some player 
has shown ONE card to the suggesting player or none show any, whose turn then ends, 
and play passes to the next player. (press OK to go to next player)'''
        canvas.create_text(cx, cy, text = msg1, fill = 'black',
            font = 'Helvetica 13 ') 
    
    elif data.currentRulesScreen == 4:
        lMsg = 'LEFT'
        canvas.create_text(x0+2*sideMargin, y1-bottomMargin, text = lMsg, 
                font = 'Helvetica 13')
        msg1 = '''
When you think you've figured out which three cards are in the envelope, you may, 
on your turn, make an Accusation by pressing the accuse button. 

In a Suggestion, the Room you name must be the Room where your token is located. 
But in an Accusation, you may name any Room. 
If the Accusation is completely correct, that is, if you find in the envelope, all
3 cards that you just named, you are the winner. Otherwise you lose the game.'''
        canvas.create_text(cx, cy, text = msg1, fill = 'black',
            font = 'Helvetica 13 ')
    
def keyPressedRules(event, data):
    if event.keysym == 'space': 
        data.gameMode = 'start'
    elif event.keysym == 'Right':
        if data.currentRulesScreen < 4:
            data.currentRulesScreen += 1
    elif event.keysym == 'Left':
        if data.currentRulesScreen > 0:
            data.currentRulesScreen -= 1
        
    