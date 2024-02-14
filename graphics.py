from tkinter import Tk, BOTH, Canvas

class Window:
    def __init__(self, width, height):
      self.width = width
      self.height = height

      self.root = Tk()
      self.root.title("Maze Solver")

      self.canvas = Canvas(self.root, bg="white", width=width, height=height)
      self.canvas.pack(fill=BOTH, expand=1)
      self.running = False
      
      self.root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
      # Draw the maze here
      self.root.update_idletasks()
      self.root.update()
    
    def wait_for_close(self):
      self.running = True
      while self.running:
        self.redraw()
      print("window closed...")
    
    def close(self):
      self.running = False

    def draw_line(self, line, fill_color):
      line.draw(self.canvas, fill_color)

class Point:
  def __init__(self, x, y):
    self.x = x
    self.y = y

class Line:
  def __init__(self, start, end):
    self.start = start
    self.end = end

  def draw(self, canvas, fill_color="black"):
    canvas.create_line(self.start.x, self.start.y, self.end.x, self.end.y, fill=fill_color, width=2)
    canvas.pack(fill=BOTH, expand=1)

