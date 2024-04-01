
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



# 2 layers of input read version   -   need recursive version next to read any number of input lines / square layers  



import tkinter as tk 

# Function to just draw one square on canvas 
def DrawOneLayer(inputText):

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

# Extended to draw 2 layers 
# Function to draw just two input lines layers of squares next
def DrawTwoLayers(inputText):
    lines = inputText.strip().split('\n') 
    # stop drawing once second line gone 
    if len(lines) < 2:
        print("Enter input for two layers of squares in this test")
        return 
    
    # set scale for canvas so that it can be zoomed out and squares dont fill entire thing 
    canvasScale = 0.2 
    canvasSize = 800 

    # Turn first line into right requirements for central square 
    scale1,r1,g1,b1 = map(float, lines[0].split())
    colour1 = f'#{int(r1):02x}{int(g1):02x}{int(b1):02x}'
    squareSize1 = canvasSize * scale1 * canvasScale
    # Turn second line into right requirements for corner squares 
    scale2,r2,g2,b2 = map(float, lines[1].split())
    colour2 = f'#{int(r2):02x}{int(g2):02x}{int(b2):02x}'
    squareSize2 = squareSize1 * scale2

    # canvas setup 
    canvas = tk.Canvas(root, width=canvasSize, height=canvasSize, bg='white')
    canvas.pack()

    # Draw first layer square in center 
    offset1 = (canvasSize - squareSize1) // 2
    canvas.create_rectangle(offset1, offset1, offset1 + squareSize1, offset1 + squareSize1, fill=colour1, outline=colour1)

    # calculate and store corners for second layer squares 
    cornerCenters = [
        (offset1, offset1), #Top Left
        (offset1 + squareSize1, offset1), #top Right
        (offset1, offset1 + squareSize1), #Bottom Left
        (offset1 + squareSize1, offset1 + squareSize1), #Bottom Right
    ]
    # draw second layer squares with recent calculations
    for centerX, centerY in cornerCenters:
        topLeftX = centerX - squareSize2 // 2
        topLeftY = centerY - squareSize2 // 2
        canvas.create_rectangle(topLeftX, topLeftY, topLeftX + squareSize2, topLeftY + squareSize2, fill=colour2, outline=colour2)

# Function to get input from text field then call DrawOneSquare with it
def Draw():
    inputText = inputField.get("1.0", tk.END).strip()
    # clear canvas before drawing 
    for widget in root.winfo_children():
        if isinstance(widget, tk.Canvas):
            widget.destroy()
    DrawTwoLayers(inputText)
# GUI setup 
root = tk.Tk()
root.title("Quilting Bee - Two layers")

# text input field
inputField = tk.Text(root, height = 2, width = 20)
inputField.pack()

# submit button to draw 
submitButton = tk.Button(root, text= "Draw", command = Draw)
submitButton.pack()

# Tkinter loop 
root.mainloop()