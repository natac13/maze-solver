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

class Cell:
  def __init__(self, x1, y1, x2, y2, window):
    self._x1 = x1
    self._y1 = y1
    self._x2 = x2
    self._y2 = y2
    self.has_left_wall = True
    self.has_right_wall = True
    self.has_top_wall = True
    self.has_bottom_wall = True
    self._win = window
  
  def draw(self, x1, y1, x2, y2):
    if self.has_left_wall:
      self._win.draw_line(Line(Point(x1, y1), Point(x1, y2)), "black")
    if self.has_right_wall:
      self._win.draw_line(Line(Point(x2, y1), Point(x2, y2)), "black")
    if self.has_top_wall:
      self._win.draw_line(Line(Point(x1, y1), Point(x2, y1)), "black")
    if self.has_bottom_wall:
      self._win.draw_line(Line(Point(x1, y2), Point(x2, y2)), "black")
