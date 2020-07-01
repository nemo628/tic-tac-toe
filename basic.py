import os
import sys
import random
# from random import random

human = "X"
ai = "O"
blank = " "
INF = 10


class Board:
    def __init__(self):
        self.board = [[blank for i in range(3)]
                      for j in range(3)]

    def showBoard(self):
        for i in range(7):
            if i % 2:
                print(" _", end=" ")
            else:
                print("", end=" ")
        print()
        for i in range(6):
            print("|", end=" ")
            for j in range(3):
                if i % 2 == 0:
                    k = int(i / 2)
                    print(f"{self.board[k][j]} |", end=" ")
                else:
                    print("_ |", end=" ")
            print()

        print()

    def minimax(self, depth, isMaximizing):
        if self.isGameOver():
            return self.isGameOver()

        if isMaximizing:
            score = 0
            bestScore = -INF
            for i in range(3):
                for j in range(3):
                    if(self.board[i][j] == blank):
                        self.board[i][j] = ai
                        score = self.minimax(depth + 1, False)
                        self.board[i][j] = blank
                        bestScore = max(score, bestScore)

            return bestScore

        else:
            score = 0
            bestScore = INF
            for i in range(3):
                for j in range(3):
                    if(self.board[i][j] == blank):
                        self.board[i][j] = human
                        score = self.minimax(depth + 1, True)
                        self.board[i][j] = blank
                        bestScore = min(score, bestScore)

            return bestScore

    def findEmpty(self):
        emptyList = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == blank:
                    emptyList.append((i, j))

        if not len(emptyList) == 0:
            return random.choice(emptyList)
        else:
            return (-1, -1)

    def findBest(self, depth):
        score = INF
        bestScore = -INF
        bestx, besty = self.findEmpty()
        for i in range(3):
            for j in range(3):
                if(self.board[i][j] == blank):
                    self.board[i][j] = ai
                    score = self.minimax(depth, False)
                    self.board[i][j] = blank
                    if score > bestScore:
                        bestScore = score
                        bestx, besty = i, j

        return (bestx, besty)

    def aiTurn(self):
        # (x, y) = self.findEmpty()
        (x, y) = self.findBest(0)
        # if (x,y) != (-1,-1):
        self.board[x][y] = ai

    def humanTurn(self):
        (x, y) = askHuman()
        if(self.board[x][y] == blank):
            self.board[x][y] = human
        else:
            print("Oops! It is already occupied. Please select again!")
            self.humanTurn()

    def isGameOver(self):
        '''
        returns: -1 if human wins
                  1 if ai wins
                  0 if draw
        '''
        # winner in row
        for i in range(3):
            if (self.board[i][1] != blank and self.board[i][1] == self.board[i][0] and self.board[i][1] == self.board[i][2]):
                return -1 if self.board[i][0] == human else 1

        #winner in col
        for i in range(3):
            if (self.board[1][i] != blank and self.board[1][i] == self.board[0][i] and self.board[1][i] == self.board[2][i]):
                return -1 if self.board[0][i] == human else 1

        # diagonal winner
        if (self.board[1][1] != blank and self.board[0][0] == self.board[1][1] and self.board[0][0] == self.board[2][2]) or (self.board[1][1] != blank and self.board[0][2] == self.board[1][1] and self.board[0][2] == self.board[2][0]):
            return -1 if self.board[1][1] == human else 1

        return 0

# could be a static method


def askHuman():
    x = input("enter x co-ordinate: ")
    y = input("enter y co-ordinate: ")
    x = int(x)
    y = int(y)
    return (x, y)


def main():
    board = Board()
    turns = 0
    board.showBoard()
    gameValue = 0
    while(turns < 9):
        if turns % 2 == 0:
            board.aiTurn()
        else:
            board.humanTurn()

        board.showBoard()
        gameValue = board.isGameOver()
        if gameValue == 1:
            print("Game over!! AI Wins!")
            break

        elif gameValue == -1:
            print("Congrats! You won!")
            break

        turns += 1

    if gameValue == 0 and turns == 9:
        print("It's a Draw!")


if __name__ == '__main__':
    main()
    # print(type(-INF))
