import pygame
from network import Network
from PIL import Image


pygame.font.init()

WIDTH = 600
HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (100, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Client")


class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 50

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.text, 1, WHITE)
        win.blit(text, (self.x + round(self.width / 2) - round(text.get_width()/2),
                        self.y + round(self.height/2) - round(text.get_height()/2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


def redraw_window(win, game, player):
    bg = pygame.image.load("rock_paper_scissors.png")
    win.blit(bg, (0, 0))

    if not game.connected():
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Waiting for player...", 1, BLACK)
        win.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
    else:
        font = pygame.font.SysFont("comicsans", 50)
        text = font.render("Your move", 1, CYAN)
        win.blit(text, (20, 200))

        text = font.render("Opponents", 1, CYAN)
        win.blit(text, (320, 200))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)

        if game.both_went():
            text1 = font.render(move1, 1, MAGENTA)
            text2 = font.render(move2, 1, MAGENTA)
        else:
            if game.p1went:
                if player == 0:
                    text1 = font.render(move1, 1, MAGENTA)
                else:
                    text1 = font.render("Locked in", 1, MAGENTA)
            else:
                text1 = font.render("Waiting...", 1, MAGENTA)

            if game.p2went:
                if player == 1:
                    text2 = font.render(move2, 1, MAGENTA)
                else:
                    text2 = font.render("Locked in", 1, MAGENTA)
            else:
                text2 = font.render("Waiting...", 1, MAGENTA)

        if player == 0:
            win.blit(text1, (50, 350))
            win.blit(text2, (350, 350))
        else:
            win.blit(text1, (350, 350))
            win.blit(text2, (50, 350))

        for btn in btns:
            btn.draw(win)

        font = pygame.font.SysFont("comicsans", 25)
        text = font.render(f"Wins: {game.wins[player]}", 1, GREEN)
        win.blit(text, (WIDTH/6 - text.get_width()/2, 10))
        text = font.render(f"Loses: {game.wins[1] if player == 0 else game.wins[0]}", 1, RED)
        win.blit(text, (WIDTH/2 - text.get_width()/2, 10))
        text = font.render(f"Ties: {game.ties}", 1, BLACK)
        win.blit(text, (WIDTH/6*5 - text.get_width()/2, 10))

    pygame.display.update()


btns = [Button("Rock", 25, 500, RED),
        Button("Paper", 225, 500, GREEN), Button("Scissors", 425, 500, BLUE)]


def main():
    run = True
    pygame.font.init()
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    print("You are player ", player)

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except Exception as e:
            run = False
            print("couldn't get game")
            break

        if game.both_went():
            redraw_window(win, game, player)
            pygame.time.delay(500)
            try:
                game = n.send("reset")
            except:
                run = False
                print("Couldn't get game")
                break

            font = pygame.font.SysFont("comicsans", 80)
            if game.winner() == player:
                text = font.render("You won!", 1, GREEN)
            elif game.winner() == 2:
                text = font.render("Tie game", 1, BLACK)
            else:
                text = font.render("You lost", 1, RED)

            win.blit(text, (WIDTH/2 - text.get_width()/2, text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                n.send("quit")
                pygame.quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1went:
                                n.send(btn.text)
                        else:
                            if not game.p2went:
                                n.send(btn.text)

        if run:
            redraw_window(win, game, player)


def start_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        bg = pygame.image.load("rock_paper_scissors.png")
        win.blit(bg, (0, 0))
        font = pygame.font.SysFont("comicsans", 90)
        text = font.render("Click to play", 1, BLUE)
        win.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                run = False

                main()


while True:
    start_screen()
