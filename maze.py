import random
from graphics import Line, Point


class Cell:
    def __init__(self, window=None):
        self._x1 = None
        self._y1 = None
        self._x2 = None
        self._y2 = None
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._win = window
        self.visited = False

    def draw(self, x1, y1, x2, y2):
        if self._win is None:
            return
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        if self.has_left_wall:
            self._win.draw_line(Line(Point(x1, y1), Point(x1, y2)), "black")
        else:
            self._win.draw_line(Line(Point(x1, y1), Point(x1, y2)), "white")
        if self.has_right_wall:
            self._win.draw_line(Line(Point(x2, y1), Point(x2, y2)), "black")
        else:
            self._win.draw_line(Line(Point(x2, y1), Point(x2, y2)), "white")
        if self.has_top_wall:
            self._win.draw_line(Line(Point(x1, y1), Point(x2, y1)), "black")
        else:
            self._win.draw_line(Line(Point(x1, y1), Point(x2, y1)), "white")
        if self.has_bottom_wall:
            self._win.draw_line(Line(Point(x1, y2), Point(x2, y2)), "black")
        else:
            self._win.draw_line(Line(Point(x1, y2), Point(x2, y2)), "white")

    def draw_move(self, to_cell, undo=False):
        ### draw a path between self and to_cell. The line will go from the center of self to the center of to_cell. if undo is True, the line is colored gray, if False, the line is colored red.
        if self._win is None:
            return
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
        window=None,
        seed=None,
    ):
        if seed is not None:
            self._seed = random.seed(seed)
        else:
            self._seed = random.seed()
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = window
        self._cells = []
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()
        self.solve()

    def _create_cells(self):
        for i in range(self._num_cols):
            col_cells = []
            for j in range(self._num_rows):
                col_cells.append(Cell(self._win))
            self._cells.append(col_cells)
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        if self._win is None:
            return
        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()

    # The entrance to the maze will always be at the top of the top-left cell, the exit always at the bottom of the bottom-right cell.
    # Add a _break_entrance_and_exit() method that removes the walls from those cells, and calls _draw_cell() after each removal.
    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[self._num_cols - 1][self._num_rows - 1].has_bottom_wall = False
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)
        self._animate()

    # The recursive break_walls_r method is a depth-first traversal through the cells, breaking down walls as it goes. I'll describe the algorithm I used, but feel free to write your own from scratch if you're up to it!
    # Mark the current cell as visited
    # In an infinite loop:
    # Create a new empty list to hold the i and j values you will need to visit
    # Check the cells that are directly adjacent to the current cell. Keep track of any that have not been visited as "possible directions" to move to
    # If there are zero directions you can go from the current cell, then draw the current cell and return to break out of the loop
    # Otherwise, pick a random direction.
    # Knock down the walls between the current cell and the chosen cell.
    # Move to the chosen cell by recursively calling _break_walls_r
    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            directions = []
            if i > 0 and not self._cells[i - 1][j].visited:
                directions.append((i - 1, j))
            if i < self._num_cols - 1 and not self._cells[i + 1][j].visited:
                directions.append((i + 1, j))
            if j > 0 and not self._cells[i][j - 1].visited:
                directions.append((i, j - 1))
            if j < self._num_rows - 1 and not self._cells[i][j + 1].visited:
                directions.append((i, j + 1))
            if len(directions) == 0:
                self._draw_cell(i, j)
                return
            else:
                next_i, next_j = random.choice(directions)
                if next_i < i:
                    self._cells[i][j].has_left_wall = False
                    self._cells[next_i][next_j].has_right_wall = False
                elif next_i > i:
                    self._cells[i][j].has_right_wall = False
                    self._cells[next_i][next_j].has_left_wall = False
                elif next_j < j:
                    self._cells[i][j].has_top_wall = False
                    self._cells[next_i][next_j].has_bottom_wall = False
                elif next_j > j:
                    self._cells[i][j].has_bottom_wall = False
                    self._cells[next_i][next_j].has_top_wall = False
                self._draw_cell(i, j)
                self._draw_cell(next_i, next_j)
                self._animate()
                self._break_walls_r(next_i, next_j)

    def _reset_cells_visited(self):
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._cells[i][j].visited = False

    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, i=0, j=0):
        self._animate()
        current_cell = self._cells[i][j]
        current_cell.visited = True
        end_cell = self._cells[self._num_cols - 1][self._num_rows - 1]
        if current_cell == end_cell:
            return True

        if (
            i > 0
            and not self._cells[i - 1][j].visited
            and not self._cells[i][j].has_left_wall
        ):
            self._cells[i][j].draw_move(self._cells[i - 1][j])
            res = self._solve_r(i - 1, j)
            if res:
                return True
            self._cells[i][j].draw_move(self._cells[i - 1][j], True)
        if (
            i < self._num_cols - 1
            and not self._cells[i + 1][j].visited
            and not self._cells[i][j].has_right_wall
        ):
            self._cells[i][j].draw_move(self._cells[i + 1][j])
            res = self._solve_r(i + 1, j)
            if res:
                return True
            self._cells[i][j].draw_move(self._cells[i + 1][j], True)
        if (
            j > 0
            and not self._cells[i][j - 1].visited
            and not self._cells[i][j].has_top_wall
        ):
            self._cells[i][j].draw_move(self._cells[i][j - 1])
            res = self._solve_r(i, j - 1)
            if res:
                return True
            self._cells[i][j].draw_move(self._cells[i][j - 1], True)
        if (
            j < self._num_rows - 1
            and not self._cells[i][j + 1].visited
            and not self._cells[i][j].has_bottom_wall
        ):
            self._cells[i][j].draw_move(self._cells[i][j + 1])
            res = self._solve_r(i, j + 1)
            if res:
                return True
            self._cells[i][j].draw_move(self._cells[i][j + 1], True)
        return False

        # draw a move from current_cell to next_cell
