
# Notes:
# Recursively generate squares of different colours depending on input
# in all corners of the parent square. 

# Input decides how much smaller/larger the next generated square is relative to the starting square scale
# Input is in the form: 
#  scale r g b 
#  where scale is a size/scale parameter for the current squares layer 
#  
# My approach:  
#   - setup GUI: create main window, add text input widget, add submit button 
#   - Parse GUI's input: Retrieve input from text area, split input into lines where each line represents a layer of the quilt 
#                        with its own scale and RGB, parse each line to extract scale + color 
#   - Drawing the quilt: Find size of canvas based on first square.
#
# Tech used: 
#   - TKinter library for GUI 
#   - 'Canvas' widget for drawing 
#   - 'create_rectangle' method of the 'Canvas' widget for drawing squares 
#   - 

import tkinter as tk 

# Function to just draw one square on canvas 
def DrawOneSquare(inputText):

    # parse first line of input, getting scale + rgb 
    scale,r,g,b = map(float, inputText.split())

    #canvas parameters 
    canvasSize = 500 
    squareSize = int(canvasSize * scale)
    colour = f'#{int(r):02x}{int(g):02x}{int(b):02x}'  # rgb to hex 

    # create canvas
    canvas = tk.Canvas(root, width=canvasSize, height=canvasSize, bg = 'white')
    canvas.pack()

    # position to center square on canvas 
    offset = (canvasSize - squareSize) // 2 

    # create rectangle on canvas 
    canvas.create_rectangle(offset, offset, offset + squareSize, offset + squareSize , fill = colour, outline = colour)

# Function to get input from text field then call DrawOneSquare with it
def Draw():
    inputText = inputField.get("1.0", tk.END).strip()
    DrawOneSquare(inputText)

# GUI setup 
root = tk.Tk()
root.title("Quilting Bee - Just one square")

# text input field
inputField = tk.Text(root, height = 2, width = 20)
inputField.pack()

# submit button to draw 
submitButton = tk.Button(root, text= "Draw", command = Draw)
submitButton.pack()

# Tkinter loop 
root.mainloop()