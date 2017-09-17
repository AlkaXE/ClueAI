##################################
### accusing Screen
##################################
#graphics recycled from buttons class
def pointInGrid(x, y, data, buttonH1, buttonH2, buttonW):
    #first get area covered by accusation button boxes
    #all magic nums are constants throughout game
    (x0, y0, a, b) = getCellBounds(data, 0, 0, buttonW, buttonH1) #a, b irrelevant
    (a, b, x1, y1) = getCellBounds(data, 5, 0, buttonW, buttonH1)
    characBox = (x0, y0, x1, y1)

    (x0, y0, a, b) = getCellBounds(data, 0, 1, buttonW, buttonH1) #a, b irrelevant
    (a, b, x1, y1) = getCellBounds(data, 5, 1, buttonW, buttonH1)
    weaponsBox = (x0, y0, x1, y1)

    (x0, y0, a, b) = getCellBounds(data, 0, 2, buttonW, buttonH2) 
    (a, b, x1, y1) = getCellBounds(data, 8, 2, buttonW, buttonH2)
    roomsBox = (x0, y0, x1, y1)

    # return True if (x, y) is inside the grid 
    bool1 = ((characBox[0] <= x <= characBox[2]) and 
            (characBox[1] <= y <= characBox[3]))
    bool2 = ((weaponsBox[0] <= x <= weaponsBox[2]) and 
            (weaponsBox[1] <= y <= weaponsBox[3]))
    bool3 = ((roomsBox[0] <= x <= roomsBox[2]) and 
            (roomsBox[1] <= y <= roomsBox[3]))
    return (bool1 or bool2 or bool3)

def getCell(x, y, data, buttonH1, buttonH2, buttonW):
    (x0, y0, a, b) = getCellBounds(data, 0, 0, buttonW, buttonH1) #a, b irrelevant
    (a, b, x1, y1) = getCellBounds(data, 5, 0, buttonW, buttonH1)
    characBox = (x0, y0, x1, y1)

    (x0, y0, a, b) = getCellBounds(data, 0, 1, buttonW, buttonH1) #a, b irrelevant
    (a, b, x1, y1) = getCellBounds(data, 5, 1, buttonW, buttonH1)
    weaponsBox = (x0, y0, x1, y1)

    (x0, y0, a, b) = getCellBounds(data, 0, 2, buttonW, buttonH2) 
    (a, b, x1, y1) = getCellBounds(data, 8, 2, buttonW, buttonH2)
    roomsBox = (x0, y0, x1, y1)
    # return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.
    if (not pointInGrid(x, y, data, buttonH1, buttonH2, buttonW)):
        return (-1, -1)
    cellWidth  = buttonW
    if ((roomsBox[0] <= x <= roomsBox[2]) and 
        (roomsBox[1] <= y <= roomsBox[3])): 
        cellHeight = buttonH2 #room button size
    else: cellHeight = buttonH1
    row = (y-characBox[1]) // cellHeight
    col = (x-characBox[0]) // cellWidth
    return (row, col)
    
def mousePressedAccusation(x, y, data):
    (x0, y0, x1, y1) = (data.width/4, data.height/4, data.width*3/4,
        3*data.height/4)
    coords = (x0, y0, x1, y1)
    margin = 20
    bottommargin = 30
    rows1, rows2 = 6, 9
    w, h = x1-x0, y1-y0 #width and height of box
    buttonW = (w-margin*2)//3
    buttonH1 = (h-bottommargin*2-margin)//rows1 
    #for persons and weapons
    buttonH2 = (h-bottommargin*2-margin)//rows2 #for rooms
    
    (row, col) = getCell(x, y, data, buttonH1, buttonH2, buttonW)
    if col == 0: #charac
        if data.selectedCharac == row:
            data.selectedCharac = None
        else: data.selectedCharac = row
    elif col == 1: #weapon
        if data.selectedWeapon == row:
            data.selectedWeapon = None
        else: data.selectedWeapon = row
    elif col == 2: #room
        if data.selectedRoom == row:
            data.selectedRoom = None
        else: data.selectedRoom = row
    return (data.selectedCharac , data.selectedWeapon, data.selectedRoom) 

def getCellBounds(data, row, col, colWidth, rowHeight):
    (x0, y0, x1, y1) = (data.width/4, data.height/4, data.width*3/4,
        3*data.height/4)
    coords = (x0, y0, x1, y1)
    margin = 20
    bottommargin = 30
    rows1, rows2 = 6, 9
    w, h = x1-x0, y1-y0 #width and height of box
    buttonW = (w-margin*2)//3
    buttonH1 = (h-bottommargin*2-margin)//rows1 
    columnWidth = colWidth
    rowHeight = rowHeight
    m = 3 #small margin around buttons
    margin = 20
    x0 = margin + col * columnWidth + coords[0]+m
    x1 = margin + (col+1) * columnWidth + coords[0]-m
    y0 = margin + row * rowHeight + coords[1]
    y1 = margin + (row+1) * rowHeight + coords[1]
    return (x0, y0, x1, y1)

def drawAccusationScreen(canvas, data):
    (x0, y0, x1, y1) = (data.width/4, data.height/4, data.width*3/4,
        3*data.height/4)
    coords = (x0, y0, x1, y1)
    canvas.create_rectangle(x0, y0, x1, y1, fill = 'white', width = 0)
    
    margin = 20
    bottommargin = 30
    selectedColor = 'red'
    locations = (1/6, 1/2, 5/6)
    w, h = x1-x0, y1-y0 #width and height of box
    rows1, rows2 = 6, 9 #rows for character, weapons and rooms 
    cardButtonW = (w-margin*2)//3
    cardButtonH1 = (h-bottommargin*2-margin)//rows1 
    #for persons and weapons
    cardButtonH2 = (h-bottommargin*2-margin)//rows2 #for rooms
    msg = 'Press \'s\' to submit or SPACE to exit'
    canvas.create_text((x0+x1)/2, y1-bottommargin, text = msg, fill = 'black',
            font = 'Helvetica 14')
    
    for row in range(rows1): #draw character suggestion boxes
        (x2, y2, x3, y3) = getCellBounds(data, row, 0, cardButtonW, cardButtonH1)
        if row == data.selectedCharac:
            canvas.create_rectangle(x2, y2, x3, y3, fill=selectedColor, 
                    width =0 )
        text = data.characters[row]
        canvas.create_text((x2+x3)/2, (y2+y3)/2, text = text)
    for row in range(rows1): #draw weapons suggestion boxes
        (x2, y2, x3, y3) = getCellBounds(data, row, 1, cardButtonW, cardButtonH1)
        if row == data.selectedWeapon:
            canvas.create_rectangle(x2, y2, x3, y3, fill=selectedColor, 
                    width =0 )
        text = data.weapons[row+rows1]
        canvas.create_text((x2+x3)/2, (y2+y3)/2, text = text)
    for row in range(rows2): #draw rooms suggestion boxes
        (x2, y2, x3, y3) = getCellBounds(data, row, 2, cardButtonW, cardButtonH2)
        if row == data.selectedRoom:
            canvas.create_rectangle(x2, y2, x3, y3, fill=selectedColor, 
                    width =0)
        text = data.rooms[row+rows1*2]
        canvas.create_text((x2+x3)/2, (y2+y3)/2, text = text)