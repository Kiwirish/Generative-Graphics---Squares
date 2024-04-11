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
# so, once input is stored into a tuple list, dimensions are calculated and canvas fitted to that calculation, then 
# the first square is drawn, with the coordinates for the corners of it being returned and stored so we know where to center 
# the next layer of squares. Then we loop over the square tuples holding scale r g b and 
# for each corner of the first square and for each coordinate in each corner, draw a new square at that current corner,
# append that to some storage for the current corners

# 10 april version 

# Pick a display / canvas size FIXED and then scale the quilt to fit the display size 
# scale the quilt with CalculateScaleFactor method rather than 
# CalculateDimensions which calculated the canvas size dependant on the quilt scales. 
# CalculateScaleFactor will scale each square drawn in the quilt to the FIXED CANVAS size instead 

# ACTUALLY read from stdin, not just 'open' the input file 


import tkinter as tk 
import sys 

# Function to calculate the scale factor based on dimensions quilt will occupy for fixed canvas size 
def CalculateScaleFactor(inputTuples, canvasWidth, canvasHeight):

    totalHeight = 25
    totalWidth = 25

    for scale,_,_,_ in inputTuples[1:]:
        scaledSize = scale * 100
        totalWidth += scaledSize * 2
        totalHeight += scaledSize * 2
    
    widthScale = canvasWidth / totalWidth 
    heightScale = canvasHeight / totalHeight 
    
    return min(widthScale, heightScale) 

def DrawSquare(canvas, XCenter, YCenter, size, colour): 

    topLeftX = XCenter - size /2
    topLeftY = YCenter - size /2

    bottomRightX = XCenter + size /2
    bottomRightY = YCenter + size /2

    canvas.create_rectangle(topLeftX, topLeftY, bottomRightX, bottomRightY, fill=colour, outline=colour)

    corners = [(topLeftX, topLeftY), (bottomRightX, topLeftY), (topLeftX, bottomRightY), (bottomRightX, bottomRightY)]
    return corners


def main(inputText): 

    #setup 
    root = tk.Tk()
    root.title("Quilting Bee")

    # fixed canvas size rather than calculated based off quilt layers scales
    canvasWidth = 800
    canvasHeight = 800

    canvas = tk.Canvas(root, width = canvasWidth, height = canvasHeight, bg='white')
    canvas.pack()

    lines = inputText.strip().split('\n')
    inputTuples = [(float(scale), int(r), int(g), int(b)) for scale, r, g, b in (line.split() for line in lines)]

    newScale = CalculateScaleFactor(inputTuples, canvasWidth, canvasHeight)

    # draw first square 
    XCenter = canvasWidth/2
    YCenter = canvasHeight/2
    lastCorners = DrawSquare(canvas, XCenter, YCenter, 100 * inputTuples[0][0] * newScale, f'#{inputTuples[0][1]:02x}{inputTuples[0][2]:02x}{inputTuples[0][3]:02x}')

    #loop over input lines starting from second as first will be drawn above 
    for scale, r, g, b in inputTuples[1:]:

        currentCorners = [] 

        for corner in lastCorners:

            XCenter, YCenter = corner
            colour = f'#{r:02x}{g:02x}{b:02x}'
            size = scale * newScale * 100
            corners = DrawSquare(canvas, XCenter, YCenter, size, colour)
            currentCorners.extend(corners)

        lastCorners = currentCorners

    root.mainloop()
    

if __name__ == "__main__":
    inputText = sys.stdin.read()
    main(inputText)




