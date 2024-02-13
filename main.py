from graphics import Cell, Line, Point, Window

def main():
  window = Window(800, 600)
  # Draw the maze here

  cell1 = Cell(window)
  cell1.draw(0, 0, 100, 100)

  cell2 = Cell(window)
  cell2.draw(100, 0, 200, 100)

  cell3 = Cell(window)
  cell3.draw(200, 0, 300, 100)

  cell4 = Cell(window)
  cell4.draw(300, 0, 400, 100)


  window.wait_for_close()

if __name__ == "__main__":
  main()

