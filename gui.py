import sys
import pygame
from basic import Board
from pygame.locals import *
from time import sleep
human = "O"
ai = "X"
blank = " "
draw = "D"
INF = 2

white = (255, 255, 255)
black = (0, 0, 0)


class GuiBoard(Board):
    def __init__(self):
        super().__init__()
        pygame.init()
        self.height = 400
        self.width = 400
        self.fps = 30
        self.ai_image = pygame.image.load("images/x.png")     # ai
        self.human_image = pygame.image.load("images/o.png")  # human
        self.ai_image = pygame.transform.scale(self.ai_image, (80, 80))
        self.human_image = pygame.transform.scale(self.human_image, (80, 80))
        self.line_color = black
        self.screen = pygame.display.set_mode(
            (self.width, self.height + 100), 0, 32)
        pygame.display.set_caption("Tic-Tac-Toe!")
        self.CLOCK = pygame.time.Clock()

    def initalize(self):
        self.screen.fill(white)
        # drawing vertical lines
        pygame.draw.line(self.screen, self.line_color, (self.width / 3, 0),
                         (self.width / 3, self.height), 7)
        pygame.draw.line(self.screen, self.line_color, (self.width / 3 * 2, 0),
                         (self.width / 3 * 2, self.height), 7)
        # drawing horizontal lines
        pygame.draw.line(self.screen, self.line_color, (0, self.height / 3),
                         (self.width, self.height / 3), 7)
        pygame.draw.line(self.screen, self.line_color, (0, self.height / 3 * 2),
                         (self.width, self.height / 3 * 2), 7)
        self.drawStatusAndReturnWinner()

    def drawStatusAndReturnWinner(self):
        winner = self.isGameOver()
        if winner == human:
            message = "You won!"
        elif winner == ai:
            message = "AI Won!"
        elif winner == draw:
            message = "It's a draw!"
        else:
            message = "Game in Progress"

        font = pygame.font.Font(None, 30)
        text = font.render(message, 1, white)

        self.screen.fill(black, (0, 400, 500, 100))
        text_rect = text.get_rect(center=(self.width / 2, 500 - 50))
        self.screen.blit(text, text_rect)
        pygame.display.update()
        return winner

    def drawImage(self, row, col):

        posx = [30, self.width / 3 + 30, self.width / 3 * 2 + 30]
        posy = [30, self.height / 3 + 30, self.height / 3 * 2 + 30]

        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ai:
                    self.screen.blit(self.ai_image, (posy[j], posx[i]))
                elif self.board[i][j] == human:
                    self.screen.blit(self.human_image, (posy[j], posx[i]))

        pygame.display.update()

    def humanTurn(self, x, y):
        if(x < self.width / 3):
            col = 0
        elif (x < self.width / 3 * 2):
            col = 1
        elif(x < self.width):
            col = 2
        else:
            col = -1

        if(y < self.height / 3):
            row = 0
        elif (y < self.height / 3 * 2):
            row = 1
        elif(y < self.height):
            row = 2
        else:
            row = -1

        if row != -1 and col != -1 and self.board[row][col] == blank:
            self.board[row][col] = human
            self.drawImage(row, col)
            return True

        else:
            return False

    def aiTurn(self):
        (row, col) = self.findBest(0)
        self.board[row][col] = ai
        self.drawImage(row, col)

    def restart(self):
        self.board = [[blank for i in range(3)] for j in range(3)]
        self.screen.fill(white)
        self.initalize()

    def game(self):
        self.initalize()
        ai_turn_flag = True
        human_turn_flag = False
        run = True
        while(run):
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type is MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if human_turn_flag:
                        if self.humanTurn(x, y):
                            winner = self.drawStatusAndReturnWinner()
                            if winner:
                                sleep(2)
                                print("Game is over")
                            else:
                                ai_turn_flag = True

                            human_turn_flag = False

                elif event.type is KEYDOWN:
                    if event.key == K_SPACE and not human_turn_flag and not ai_turn_flag:
                        self.initalize()
                        self.restart()
                        ai_turn_flag = True
                        human_turn_flag = False

                    if event.key == K_ESCAPE:
                        run = False

                if ai_turn_flag:
                    self.aiTurn()
                    winner = self.drawStatusAndReturnWinner()
                    if winner:
                        sleep(2)
                        print("Game is over")
                        # pygame.quit()
                    else:
                        human_turn_flag = True
                    ai_turn_flag = False

            pygame.display.update()
            self.CLOCK.tick(self.fps)


board = GuiBoard()
board.game()
