# Author: Blake Leahy 

# Quilting Bee with display fitted nicely to quilt. 

# Done by tracking the co-ords where each square is drawn, then the full canvas is redrawn at the total 
# size of those coordinates. Each layer that's drawn, return coordinates of the size of that layer 

import tkinter as tk 

# Function to recursively draw layers after the first 
def DrawLayer(canvas, center, size, colour, lines, numLayers=0, minX=float('inf'), minY=float('inf'), maxX=float('-inf'), maxY=float('-inf')):

    # base case 
    if numLayers >= len(lines):
        return minX, minY, maxX, maxY

    #calculate square position
    topLeftX = center[0] - size //2 
    topLeftY = center[1] - size //2 
    canvas.create_rectangle(topLeftX, topLeftY, topLeftX + size, topLeftY + size, fill=colour, outline=colour)

    # update min/max co-ords for canvas fitting to new squares drawn 
    minX = min(minX, topLeftX)
    minY = min(minY, topLeftY)
    maxX = max(maxX, topLeftX + size)
    maxY = max(maxY, topLeftY + size)
    # new calculations to feed as input parameters to recursive call to DrawLayer
    if numLayers + 1 < len(lines):

        scale, r, g, b = map(float, lines[numLayers + 1].split())
        newColour = f'#{int(r):02x}{int(g):02x}{int(b):02x}'
        newSize = size * scale   

        cornerCenters = [
            (topLeftX, topLeftY), 
            (topLeftX + size, topLeftY),  
            (topLeftX, topLeftY + size), 
            (topLeftX + size, topLeftY + size), 
        ]

        for x,y in cornerCenters: 
            newCenter = (x,y)
            minX, minY, maxX, maxY = DrawLayer(canvas, newCenter, newSize, newColour, lines, numLayers+1, minX, minY, maxX, maxY)
    
    return minX, minY, maxX, maxY

# Function to draw first square to base next line recursive calls off 
def DrawSquares(inputText):

    lines = inputText.strip().split('\n')
    if not lines:
        print("Input must be provided")
        return 
    
    # setup canvas 
    canvasSize = 800 
    #baseScale = 0.2 #first square small relative to canvas 
    canvas = tk.Canvas(root, width=canvasSize, height = canvasSize, bg = 'white')
    canvas.pack() 

    #draw first line and call recursive function
    scale, r, g, b = map(float, lines[0].split())
    colour = f'#{int(r):02x}{int(g):02x}{int(b):02x}'
    initialSize = canvasSize*scale  

   # DrawLayer(canvas, (canvasSize//2, canvasSize//2), initialSize, colour, lines)
    minX, minY, maxX, maxY = DrawLayer(canvas, (canvasSize // 2, canvasSize // 2), initialSize, colour, lines)

    # scaling factor to fit quilt nicely to canvas 
    quiltWidth = maxX - minX 
    quiltHeight = maxY - minY
    scaleFactor = min(canvasSize / quiltWidth, canvasSize / quiltHeight)

    # redraw quiilt with new scale factor 
    canvas.delete("all")
    DrawLayer(canvas, (canvasSize // 2, canvasSize // 2), initialSize * scaleFactor, colour, lines)


# Function to get input from text field then start drawing
#def Draw():
   # inputText = inputField.get("1.0", tk.END).strip()
    # clear canvas before drawing 
   # for widget in root.winfo_children():
     #   if isinstance(widget, tk.Canvas):
     #       widget.destroy()
   # DrawSquares(inputText)

# GUI setup 
root = tk.Tk()
root.title("Quilting Bee")

# text input field
inputField = tk.Text(root, height = 5, width = 30)
inputField.insert('1.0', "1.0 255 0 0\n0.8 0 255 0\n0.1 0 0 255")  # Default example input.

inputField.pack()

# submit button to draw 
submitButton = tk.Button(root, text= "Draw", command=lambda: DrawSquares(inputField.get("1.0", tk.END).strip()))
submitButton.pack()

# Tkinter loop 
root.mainloop()