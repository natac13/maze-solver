import time
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
  def __init__(self, window):
    self._x1 = None
    self._y1 = None
    self._x2 = None
    self._y2 = None
    self.has_left_wall = True
    self.has_right_wall = True
    self.has_top_wall = True
    self.has_bottom_wall = True
    self._win = window
  
  def draw(self, x1, y1, x2, y2):
    self._x1 = x1
    self._y1 = y1
    self._x2 = x2
    self._y2 = y2
    if self.has_left_wall:
      self._win.draw_line(Line(Point(x1, y1), Point(x1, y2)), "black")
    if self.has_right_wall:
      self._win.draw_line(Line(Point(x2, y1), Point(x2, y2)), "black")
    if self.has_top_wall:
      self._win.draw_line(Line(Point(x1, y1), Point(x2, y1)), "black")
    if self.has_bottom_wall:
      self._win.draw_line(Line(Point(x1, y2), Point(x2, y2)), "black")
  
  def draw_move(self, to_cell, undo=False):
    ### draw a path between self and to_cell. The line will go from the center of self to the center of to_cell. if undo is True, the line is colored gray, if False, the line is colored red.
    x1 = (self._x1 + self._x2) // 2
    y1 = (self._y1 + self._y2) // 2
    x2 = (to_cell._x1 + to_cell._x2) // 2
    y2 = (to_cell._y1 + to_cell._y2) // 2
    if undo:
      self._win.draw_line(Line(Point(x1, y1), Point(x2, y2)), "gray")
    else:
      self._win.draw_line(Line(Point(x1, y1), Point(x2, y2)), "red")

class Maze:
  def __init__(
      self,
      x1,
      y1,
      num_rows,
      num_cols,
      cell_size_x,
      cell_size_y,
      window
  ):
    self._x1 = x1
    self._y1 = y1
    self._num_rows = num_rows
    self._num_cols = num_cols
    self._cell_size_x = cell_size_x
    self._cell_size_y = cell_size_y
    self._win = window
    self._cells = []
    self._create_cells()

  def _create_cells(self):
    for i in range(self._num_rows):
      for j in range(self._num_cols):
        self._draw_cell(i, j)
  
  def _draw_cell(self, i, j):
    cell = Cell(self._win)
    cell.draw(
      self._x1 + i * self._cell_size_x,
      self._y1 + j * self._cell_size_y,
      self._x1 + (i + 1) * self._cell_size_x,
      self._y1 + (j + 1) * self._cell_size_y
    )
    self._cells.append(cell)
    self._animate()

  def _animate(self):
    self._win.redraw()
    time.sleep(0.05)

