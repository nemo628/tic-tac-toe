import os
import sys
import random
# from random import random

human = "O"
ai = "X"
draw = "D"
blank = " "
INF = 2


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

    def minimax(self, depth, alpha, beta, isMaximizing):
        # self.showBoard()
        checkScore = self.isGameOver()
        if checkScore:
            # self.showBoard()
            # print(checkScore)
            return 1 if checkScore == ai else 0 if checkScore == draw else -1

        if isMaximizing:
            bestScore = -INF
            for i in range(3):
                for j in range(3):
                    if(self.board[i][j] == blank):
                        self.board[i][j] = ai
                        score = self.minimax(depth + 1, alpha, beta, False)
                        self.board[i][j] = blank
                        bestScore = max(score, bestScore)
                        alpha = max(alpha, bestScore)
                        if alpha >= beta:
                            break
            return bestScore

        else:
            bestScore = INF
            for i in range(3):
                for j in range(3):
                    if(self.board[i][j] == blank):
                        self.board[i][j] = human
                        score = self.minimax(depth + 1, alpha, beta, True)
                        self.board[i][j] = blank
                        bestScore = min(score, bestScore)
                        beta = min(beta, bestScore)
                        if beta <= alpha:
                            break
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
        score = 0
        bestScore = -INF
        bestx, besty = -1, -1
        for i in range(3):
            for j in range(3):
                if(self.board[i][j] == blank):
                    self.board[i][j] = ai
                    score = self.minimax(depth, -INF, INF, False)
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
        returns: human if human wins
                 ai if ai wins
                 draw if draw

        '''
        winner = None
        # winner in row
        for i in range(3):
            if (self.board[i][1] == self.board[i][0] and self.board[i][1] == self.board[i][2]):
                winner = self.board[i][0]
                if winner != blank:
                    return winner

        #winner in col
        for i in range(3):
            if (self.board[1][i] == self.board[0][i] and self.board[1][i] == self.board[2][i]):
                winner = self.board[0][i]
                if winner != blank:
                    return winner

        # diagonal winner
        if (self.board[0][0] == self.board[1][1] and self.board[0][0] == self.board[2][2]) or (self.board[0][2] == self.board[1][1] and self.board[0][2] == self.board[2][0]):
            winner = self.board[1][1]
            if winner != blank:
                return winner

        countEmpty = 0
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == blank:
                    countEmpty += 1

        if countEmpty == 0:  # draw
            return draw
        else:
            return None


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
        if gameValue == ai:
            print("Game over!! AI Wins!")
            return

        elif gameValue == human:
            print("Congrats! You won!")
            return

        elif gameValue == draw:
            print("It's a draw!")
            return

        turns += 1

    if turns == 9:
        print("It's a Draw!")


if __name__ == '__main__':
    main()
    # print(type(-INF))
