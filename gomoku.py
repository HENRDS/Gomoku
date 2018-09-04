import sys
from typing import List
import pygame
from board import BoardState


pygame.init()


class GomokuUI(object):
    def __init__(self, display_width: int = 900, display_height: int = 650):
        N = 15
        self.game_state: BoardState = BoardState()
        self.display_width: int = display_width
        self.display_height: int = display_height
        self.margin = 23
        self.line_width = 1
        self.cell_side = 40
        self.box_width = (self.line_width + self.cell_side) * 4
        self.box_height = (self.line_width + self.cell_side) * 3
        self.title_font = pygame.font.SysFont('Calibri', 24)
        self.score_font = pygame.font.SysFont('Calibri', 20)
        self.time_font = pygame.font.SysFont('Calibri', 20)
        self.board_width = self.line_width * N + self.cell_side * (N-1)
        self.clock: pygame.time.Clock = pygame.time.Clock()
        res = './res'
        self.background = pygame.image.load(f'{res}/board.png')
        self.panel = pygame.image.load(f'{res}/panel.png')
        self.pieces: List[pygame.Surface] = []
        for i in range(2):
            self.pieces.append(pygame.image.load(f'{res}/p{i}.png'))

    def side_panel(self, screen: pygame.Surface):
        screen.blit(self.panel, (self.board_width + 2 * self.margin))

    def update_info(self, screen: pygame.Surface):
        pass

    def on_click(self):
        pass

    def main(self):
        screen: pygame.Surface = pygame.display.set_mode((self.display_width, self.display_height),
                                                         pygame.HWSURFACE |
                                                         pygame.DOUBLEBUF)
        pygame.display.set_caption('Gomoku')
        screen.blit(self.background, (0, 0))
        screen.blit(self.panel, (self.board_width + 3 * self.margin, 0))
        self.update_info(screen)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                pygame.display.update()
                self.clock.tick(20)





if __name__ == '__main__':
    ui = GomokuUI()
    ui.main()
