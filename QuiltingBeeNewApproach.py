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
# 14 April version
# ensure scale factor is within reasonable range - test different ranges.
# if squares are smaller than 1 pixel then dont draw 

# 16 April version 
# successfully scaling up but not scaling down. For small inputs, it scales it up well. 
# But for large inputs, it doesn’t scale it down, its just a huge zoomed in quilt. 
# new scaling function 

# 17 April version 

import tkinter as tk 
import sys 

# Function to calculate the scale factor based on dimensions quilt will occupy for fixed canvas size 
def CalculateScaleFactor(inputTuples, canvasWidth, canvasHeight):

    totalHeight = 25
    totalWidth = 25
    # storing largest scale number 

    # divide each scale by max scale 
    for scale,_,_,_ in inputTuples[1:]:
        scaledSize = scale * 100
        totalWidth += scaledSize * 2
        totalHeight += scaledSize * 2


    widthScale = canvasWidth / totalWidth 
    heightScale = canvasHeight / totalHeight 
    scaleFactor = min(widthScale, heightScale)

    # make sure scale factor is within reasonable range 
    minScale = 0.00001 
    maxScale = 10000.0 
    scaleFactor = max(minScale, min(maxScale, scaleFactor))
    return scaleFactor 

# Scale 
def CalculateProportionalScaleFactor(inputTuples, canvasWidth, canvasHeight):

    initialSize = 100
    maxDimension = initialSize * inputTuples[0][0]
    
    additiveDimension = maxDimension

    for scale, _, _, _ in inputTuples[1:]:
        additiveDimension += initialSize * scale 
    
    scaleFactor = min(canvasWidth / additiveDimension, canvasHeight / additiveDimension)
    return scaleFactor

def DrawSquare(canvas, XCenter, YCenter, size, colour): 

    topLeftX = XCenter - size /2
    topLeftY = YCenter - size /2

    bottomRightX = XCenter + size /2
    bottomRightY = YCenter + size /2
    
    # only draw if greater than 1 pixel
    if size > 1:
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

    newScale = CalculateProportionalScaleFactor(inputTuples, canvasWidth, canvasHeight)

    # draw first square 
    XCenter = canvasWidth/2
    YCenter = canvasHeight/2

    firstScale, r, g, b = inputTuples[0]
    firstSize = firstScale * newScale * 100 
    firstColour = f'#{r:02x}{g:02x}{b:02x}'

    lastCorners = [DrawSquare(canvas, XCenter, YCenter, firstSize, firstColour)]

    #loop over input lines starting from second as first will be drawn above 
    for scale, r, g, b in inputTuples[1:]:

        currentCorners = [] 

        for corners in lastCorners:
            for (XCenter, YCenter) in corners:

                size = scale * newScale * 100
                colour = f'#{r:02x}{g:02x}{b:02x}'
                corners = DrawSquare(canvas, XCenter, YCenter, size, colour)
                currentCorners.append(corners)

        lastCorners = currentCorners

    root.mainloop()
    

if __name__ == "__main__":
    inputText = sys.stdin.read()
    main(inputText)




