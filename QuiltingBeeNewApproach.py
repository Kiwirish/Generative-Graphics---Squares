# Author : Blake Leahy 
#
#
# scaling issue to be fixed - other scales based off first layers scale, 
# first layers scale doesn't necessarily have to be largest scale. 
# 1.0 255 0 0 \n 1.2 0 255 0 \n 0.1 0 0 255 should display correctly 

# new approach:
#   
#  still use tkinter window for quilt drawing but take from stdin 
#  - issues encountered with GUI and scaling 
#  input is put into tuple list containing 'scale r g b' to store 
#  Before drawing, calculate what total size of quilt will need to be from scales in tuple list 
#  
#  Draw first square at canvas center then draw next layers squares at corners of previously drawn square(s). Repeats for all input lines 
#  Once all layers drawn, quilt displayed in tkinter window. 
# 
#  DrawSquare function gets all points of last square to draw new square off and draws that, returning coords/positions of the corners of that new square 
#  
# read input with 'with open(input.txt',r')' 
# EstimateDimensions function to calculate total widthxheight to fit the final quilt using 'scale' in squares tuple list 
#  -starting w a base size, for each layer after the first (squares[1:]), calculate how much more space is needed bc of that layers scale 
#  -that extra space from each layers 'scale' parameter is added to the width and height of the canvas 
#  -ensure canvas is sized well from start 
# 
# so, once input is stored into a tuple list, dimensions are calculated and canvas fitted to that calculation, then 
# the first square is drawn, with the coordinates for the corners of it being returned and stored so we know where to center 
# the next layer of squares. Then we loop over the square tuples holding scale r g b and 
# for each corner of the first square and for each coordinate in each corner, draw a new square at that current corner,
# append that to some storage for the current corners

import tkinter as tk 
import sys 

# function to calculate the dimensions of the canvas from the scale inputs prior to drawing 
def CalculateDimensions(inputTuples):

    totalHeight = 10 
    totalWidth = 10

    for scale,_,_,_ in inputTuples[1:]:
        scaledSize = scale * 100 
        totalWidth += scaledSize * 2 
        totalHeight += scaledSize * 2

    return totalWidth, totalHeight 

def DrawSquare(canvas, XCenter, YCenter, size, colour): 

    topLeftX = XCenter - size /2
    topLeftY = YCenter - size /2

    bottomRightX = XCenter + size /2
    bottomRightY = YCenter + size /2

    canvas.create_rectangle(topLeftX, topLeftY, bottomRightX, bottomRightY, fill=colour, outline=colour)

    corners = [(topLeftX, topLeftY), (bottomRightX, topLeftY), (topLeftX, bottomRightY), (bottomRightX, bottomRightY)]
    return corners


def main(): 

    #setup 
    root = tk.Tk()
    root.title("Quilting Bee")

    with open('input.txt', 'r') as f:
        inputText = f.read()

    lines = inputText.strip().split('\n')

    inputTuples = [(float(scale), int(r), int(g), int(b)) for scale, r, g, b in (line.split() for line in lines)]

    # calculate dinmensions 
    totalWidth, totalHeight = CalculateDimensions(inputTuples)
    canvas = tk.Canvas(root, width = totalWidth, height = totalHeight, bg='white')
    canvas.pack()

    # draw first square 
    XCenter = totalWidth/2
    YCenter = totalHeight/2
    lastCorners = [DrawSquare(canvas, XCenter, YCenter, 100 * inputTuples[0][0], f'#{inputTuples[0][1]:02x}{inputTuples[0][2]:02x}{inputTuples[0][3]:02x}')]

    #loop over input lines starting from second as first will be drawn above 
    for scale, r, g, b in inputTuples[1:]:

        size = scale * 100 
        colour = f'#{int(r):02x}{int(g):02x}{int(b):02x}'
        currentCorners = [] 

        for corner in lastCorners:
            for coordinate in corner: 

                XCenter, YCenter = coordinate
                corners = DrawSquare(canvas, XCenter, YCenter, size, colour)
                currentCorners.append(corners)

        lastCorners = currentCorners 
    
    root.mainloop()

if __name__ == "__main__":
    main()




