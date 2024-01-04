# main.py
import sys
sys.path.append(r'C:\Users\Darek\Desktop\Studia\TO\PacBraun')
from game.game import Game

if __name__ == "__main__":
    # Wczytanie mapy z pliku
    maze = []
    with open("saved_maze.csv", 'r') as file:
        for line in file:
            row = [int(cell) for cell in line.strip().split(',')]
            maze.append(row)

    game = Game(maze)
    game.run()