def make2dList(rows, cols):
    a=[]
    for row in range(rows): a += [[0]*cols]
    return a

class Checklist(object):
    #taken from notes:        
    def getCellBounds(self, row, col, colWidth, rowHeight):
        # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
        columnWidth = colWidth
        rowHeight = rowHeight
        x0 = self.margin + col * columnWidth + self.leftStart
        x1 = self.margin + (col+1) * columnWidth +self.leftStart
        y0 = self.margin + row * rowHeight 
        y1 = self.margin + (row+1) * rowHeight
        return (x0, y0, x1, y1)
        
    def __init__(self, data):
        self.rows = data.numOfCards
        self.cols = 6
        self.width = data.width
        self.height = data.height
        self.margin = 15
        self.labelWidth = 100
        self.labelHeight = 25
        self.cellDim = 25
        self.color = 'white'
        #postion on screen
        boardCellDim = 32
        self.topStart = 0
        self.leftStart = boardCellDim * self.cellDim #todo
        self.selected = make2dList(self.rows, self.cols) #cells that are selected
        self.selectedColor1 = 'red' 
        self.selectedColor2 = 'green'
    
    #modified from notes
    def pointInGrid(self, x, y, data, colWidth, rowHeight):
        # return True if (x, y) is inside the grid defined by data.
        return ((self.leftStart+self.labelWidth+self.margin <= x 
            <= self.leftStart+self.cellDim*self.cols+self.labelWidth+self.margin) and
                (self.margin+self.topStart <= y 
            <= self.margin+self.topStart+self.cellDim*self.rows))
    
    def getCell(self, x, y, data, colWidth, rowHeight):
        # return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.
        if (not self.pointInGrid(x, y, data, colWidth, rowHeight)):
            return (-1, -1)
        cellWidth  = colWidth
        cellHeight = rowHeight
        row = (y-self.margin-self.topStart) // cellHeight
        col = (x-self.leftStart-self.labelWidth-self.margin) // cellWidth
        # triple-check that we are in bounds
        row = min(self.rows-1, max(0, row))
        col = min(self.cols-1, max(0, col))
        return (row, col)
        
    def mousePressed(self, x, y, data):
        numOfColors = 3
        row, col = self.getCell(x, y, data, self.cellDim, self.cellDim)
        if (row, col) != (-1, -1): #on board
            self.selected[row][col] = (self.selected[row][col]+1)%numOfColors
    
    def draw(self, canvas, data):
        for row in range(self.rows):
            col = 0 #only one column
            (x0, y0, x1, y1) = self.getCellBounds(row, col, self.labelWidth, 
                    self.labelHeight)
            canvas.create_rectangle(x0, y0, x1, y1, fill = 'white')
            label = data.allCards[row]
            canvas.create_text((x0+x1)/2, (y0+y1)/2, text = label)
            
        
        for row in range(self.rows):
            for col in range(self.cols):
                if self.selected[row][col] == 0: color = 'white'
                elif self.selected[row][col] == 1: color = self.selectedColor1
                else: color = self.selectedColor2
                (x0, y0, x1, y1) = self.getCellBounds(row, col, self.cellDim,
                    self.cellDim)
                canvas.create_rectangle(x0+self.labelWidth, y0,
                    x1+self.labelWidth, y1, fill = color) #include offset for labels