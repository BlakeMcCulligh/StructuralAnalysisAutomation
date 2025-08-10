import tkinter as tk
from tkinter import ttk
import DrawLine
import SelectTool
import Relations

class SketchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Structural Analysis Automation")

        # creating the toolbars
        self.notebook = None
        self.toolbar = []
        self.toolbarFrame = []
        self.currentTool = tk.StringVar(value="line")
        self.createToolBars()

        # creating the drawing area
        self.canvas = tk.Canvas(root, bg="white", width=800, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        #SketchObjects
        self.listLines = []
        self.listPoints = []
        self.set_tool("select")

        # things that are being watched for on the canvas
        self.canvas.bind("<Button-1>", self.on_click_Left)
        #self.canvas.bind("<Motion>", self.on_motion)

    def createToolBars(self):
        self.notebook = ttk.Notebook()
        self.notebook.pack(side=tk.TOP, fill=tk.X)

        self.toolbar.append(tk.Frame(self.notebook))
        self.toolbar.append(tk.Frame(self.notebook))

        self.notebook.add(self.toolbar[0], text="Draw")
        self.notebook.add(self.toolbar[1], text="Relations")

        self.toolbarFrame.append(tk.Frame(self.toolbar[0], bg="#ddd"))
        self.toolbarFrame[0].pack(side=tk.TOP, fill=tk.X)

        tk.Button(self.toolbarFrame[0], text="select", command=lambda: self.set_tool("select")).pack(side=tk.LEFT)
        tk.Button(self.toolbarFrame[0], text="Line", command=lambda: self.set_tool("line")).pack(side=tk.LEFT)

        self.toolbarFrame.append(tk.Frame(self.toolbar[1], bg="#ddd"))
        self.toolbarFrame[1].pack(side=tk.TOP, fill=tk.X)

        tk.Button(self.toolbarFrame[1], text="Horizontal", command=lambda: self.set_tool("Horizontal")).pack(side=tk.LEFT)
        tk.Button(self.toolbarFrame[1], text="Vertical", command=lambda: self.set_tool("Vertical")).pack(side=tk.LEFT)
        tk.Button(self.toolbarFrame[1], text="Parallel", command=lambda: self.set_tool("Parallel")).pack(side=tk.LEFT)
        tk.Button(self.toolbarFrame[1], text="Perpendicular", command=lambda: self.set_tool("Perpendicular")).pack(side=tk.LEFT)
        tk.Button(self.toolbarFrame[1], text="Equal", command=lambda: self.set_tool("Equal")).pack(side=tk.LEFT)
        tk.Button(self.toolbarFrame[1], text="colinear", command=lambda: self.set_tool("colinear")).pack(side=tk.LEFT)
        tk.Button(self.toolbarFrame[1], text="Coincidence", command=lambda: self.set_tool("Coincidence")).pack(side=tk.LEFT)
        tk.Button(self.toolbarFrame[1], text="Dimentions", command=lambda: self.set_tool("Dimentions")).pack(side=tk.LEFT)
        tk.Button(self.toolbarFrame[1], text="Fixed", command=lambda: self.set_tool("Fixed")).pack(side=tk.LEFT)

    def set_tool(self, newTool):
        self.currentTool.set(newTool)
        DrawLine.exitDrawLine(self.canvas)
        Relations.l1 = None
        Relations.p1 = None

        # may need to be changed

    # when the left mouse button is clicked on the canvas
    def on_click_Left(self, event):
        currentTool = self.currentTool.get()
        window = self
        # needs implemented
        if currentTool == "select":
            SelectTool.click(self.canvas, event.x, event.y)
        elif currentTool == "line":
            DrawLine.draw(window, self.canvas, event.x, event.y)
        elif currentTool == "Horizontal":
            Relations.addHorizontal(self.canvas, event.x, event.y)
        elif currentTool == "Vertical":
            Relations.addVertical(self.canvas, event.x, event.y)
        elif currentTool == "Parallel":
            Relations.addParallel(self.canvas, event.x, event.y)
        elif currentTool == "Perpendicular":
            Relations.addPerpendicualer(self.canvas, event.x, event.y)
        elif currentTool == "Equal":
            Relations.addEqual(self.canvas, event.x, event.y)
        elif currentTool == "colinear":
            Relations.addColinear(self.canvas, event.x, event.y)
        elif currentTool == "Coincidence":
            Relations.addCoincidence(self.canvas, event.x, event.y)
        elif currentTool == "Dimentions":
            Relations.addDimentions(self.canvas, event.x, event.y)
        elif currentTool == "Fixed":
            Relations.addFixed(self.canvas, event.x, event.y)

root = tk.Tk()
app = SketchApp(root)
root.mainloop()