from time import time
from tkinter import *
from PIL import ImageTk
from copy import deepcopy

from ai.minimax import AI
from ai.moves import is_valid_move
from utils.utils import starting_array

moves = 0
boardStartX = 50
boardEndX = 450
boardCellLen = 50
CircleStartX = 55
CircleEndX = 95
ValidCircleX = 65
ValidCircleY = 35
ScoreCircleStartY = 540
StartRecX = 180
StartRecY = 300
root = Tk()
screen = Canvas(root, width=500, height=600, background="#3b2611", highlightthickness=0)
image = ImageTk.PhotoImage(file="../assets/bg.jpg")
screen.create_image(0, 0, image=image, anchor=NW)
screen.pack()
ai: AI

class OthelloBoard:
    def __init__(self):
        self.player = 1
        self.last_player_NO_valid_move = False
        self.EndGame = False
        self.Cells = starting_array()

    def refreshScreen(self):
        screen.delete("ValidCells")
        screen.delete("FilledCells")
        for x in range(8):
            for y in range(8):
                if self.Cells[x][y] == "w":
                    screen.create_oval(CircleStartX + boardCellLen * x, CircleStartX + boardCellLen * y,
                                       CircleEndX + boardCellLen * x, CircleEndX + boardCellLen * y,
                                       tags="FilledCells", fill="white", outline="white")
                elif self.Cells[x][y] == "b":
                    screen.create_oval(CircleStartX + boardCellLen * x, CircleStartX + boardCellLen * y,
                                       CircleEndX + boardCellLen * x, CircleEndX + boardCellLen * y,
                                       tags="FilledCells", fill="black", outline="black")
        screen.update()

        # show valid cells
        if board.player == 1 or board.player == 0:
            for x in range(8):
                for y in range(8):
                    if is_valid_move(self.Cells, self.player, x, y):
                        screen.create_oval(ValidCircleX + boardCellLen * x, ValidCircleX + boardCellLen * y,
                                           ValidCircleY + boardCellLen * (x + 1), ValidCircleY + boardCellLen * (y + 1),
                                           tags="ValidCells", fill="yellow", outline="yellow")

        if not self.EndGame:
            self.ScoreBoard()
            screen.update()
            if self.player == 0:
                startTime = time()
                alphaBetaResult = ai.minimax(board.Cells, board.player)
                self.Cells = alphaBetaResult.board
                self.player = 1 - self.player
                self.refreshScreen()
                deltaTime = round((time() - startTime) * 100) / 100
                print('the minimax took ' + str(deltaTime))
                self.skip_turn()
        else:
            screen.create_text(250, 550, font=("Arial", 20), fill="yellow", text="End :) ")

    def Move(self, x, y):
        array = deepcopy(self.Cells)
        if board.player == 0:
            color = "w"

        else:
            color = "b"
        array[x][y] = color
        changeColor = []
        surroundingCells = []
        xmin = max(0, x - 1)
        xmax = min(x + 2, 8)
        ymin = max(0, y - 1)
        ymax = min(y + 2, 8)
        for i in range(xmin, xmax):
            for j in range(ymin, ymax):
                if array[i][j] is not None:
                    surroundingCells.append([i, j])

        for cell in surroundingCells:
            cell_X = cell[0]
            cell_Y = cell[1]
            if array[cell_X][cell_Y] != color:
                path = []
                delta_x = cell_X - x
                delta_y = cell_Y - y
                temp_x = cell_X
                temp_y = cell_Y

                while 0 <= temp_x <= 7 and 0 <= temp_y <= 7:
                    path.append([temp_x, temp_y])
                    CellColor = array[temp_x][temp_y]
                    if CellColor == None:
                        break

                    if CellColor == color:
                        # age be khuneE resid ke rangesh ba range player yeki bud masir peyda shode va tamame cell haye masir bayad barax shavand
                        for eachCell in path:
                            changeColor.append(eachCell)
                        break
                    # temp khuneye badi tooye masir hast
                    temp_x += delta_x
                    temp_y += delta_y

        for eachCell in changeColor:
            array[eachCell[0]][eachCell[1]] = color
        self.Cells = array
        # switch player
        self.player = 1 - self.player
        self.skip_turn()
        self.refreshScreen()
        self.skip_turn()

    def skip_turn(self):
        next_player_NO_valid_move = True
        for x in range(8):
            for y in range(8):
                if is_valid_move(self.Cells, self.player, x, y):
                    next_player_NO_valid_move = False

        # age nafare badi harekate mojazi nadasht bazi be nafare ghabli bar migarde
        if next_player_NO_valid_move:
            self.player = 1 - self.player
            if self.last_player_NO_valid_move:
                self.EndGame = True


            else:
                self.last_player_NO_valid_move = True

            self.refreshScreen()
        else:
            self.last_player_NO_valid_move = False

    def ScoreBoard(self):
        global moves
        screen.delete("score")
        Black_Score = 0
        White_Score = 0
        for x in range(8):
            for y in range(8):
                if self.Cells[x][y] == "b":
                    Black_Score += 1
                elif self.Cells[x][y] == "w":
                    White_Score += 1

        if self.player == 0:
            WhitePalyerColor = "yellow"
            BlackPlayerColor = "black"
        else:
            WhitePalyerColor = "white"
            BlackPlayerColor = "yellow"

        screen.create_oval(boardStartX, ScoreCircleStartY, boardStartX + 25, ScoreCircleStartY + 20,
                           fill=BlackPlayerColor, outline=BlackPlayerColor)
        screen.create_text(boardStartX + 25, ScoreCircleStartY + 10, anchor="w", tags="score", font=("Arial", 50),
                           fill="black",
                           text=Black_Score)

        screen.create_oval(boardEndX - 40 - 25, ScoreCircleStartY, boardEndX - 40, ScoreCircleStartY + 20,
                           fill=WhitePalyerColor,
                           outline=WhitePalyerColor)
        screen.create_text(boardEndX - 40, ScoreCircleStartY + 10, anchor="w", tags="score", font=("Arial", 50),
                           fill="white",
                           text=White_Score)

        moves = Black_Score + White_Score



def clickHandle(event):
    X = event.x
    Y = event.y
    if not InStartScreen:
        if X >= boardEndX and Y <= boardStartX:
            # close game
            root.destroy()
        elif X <= boardStartX and Y <= boardStartX:
            # refresh game
            play()
        else:
            # playing
            x = int((event.x - boardStartX) / boardCellLen)
            y = int((event.y - boardStartX) / boardCellLen)
            if 0 <= x <= 7 and 0 <= y <= 7:
                if is_valid_move(board.Cells, board.player, x, y):
                    board.Move(x, y)

    else:
        if StartRecX <= X <= StartRecX + 130 and StartRecY <= Y <= StartRecY + 50:
            play()


def create_Game_Screen():
    # Close Button
    imgRefresh = PhotoImage(file="../assets/close.png")
    screen.create_image(500, 0, anchor=NE, image=imgRefresh)
    screen.close = imgRefresh
    # Refresh Button
    imgRefresh = PhotoImage(file="../assets/refresh.png")
    screen.create_image(50, 0, anchor=NE, image=imgRefresh)
    screen.refresh = imgRefresh
    # Grids
    screen.create_rectangle(boardStartX, boardStartX, boardEndX, boardEndX, outline="#423324", fill='#174f17', width=5)
    for i in range(7):
        screen.create_line(boardStartX, boardStartX + boardCellLen * (i + 1), boardEndX,
                           boardStartX + boardCellLen * (i + 1), fill="black")
        screen.create_line(boardStartX + boardCellLen * (i + 1), boardStartX, boardStartX + boardCellLen * (i + 1),
                           boardEndX, fill="black")
    screen.update()


def StartScreen():
    global InStartScreen
    InStartScreen = True
    screen.create_text(250, 203, anchor="c", text="Othello", font=("Arial", 40), fill="#efefef")
    screen.create_rectangle(StartRecX, StartRecY, StartRecX + 130, StartRecY + 50, fill="black", outline="black")
    screen.create_text(250, 325, anchor="c", text="START", font=("Arial", 20), fill="#e3eb0c")
    screen.update()


def play():
    global InStartScreen
    global board
    InStartScreen = False
    screen.delete(ALL)
    create_Game_Screen()
    board = OthelloBoard()
    board.refreshScreen()


def main(agent: AI = None):
    global ai
    if agent is None:
        ai = AI()
    else:
        ai = agent
    StartScreen()
    screen.bind("<Button-1>", clickHandle)
    root.wm_title("Othello Game")
    root.mainloop()


if __name__ == '__main__':
    main()