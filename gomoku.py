
import sys
from typing import List, Tuple
import pygame
from board import BoardState


pygame.init()

PLAYERTYPE1 = 'human'
PLAYERTYPE2 = 'computer'

white = (255, 255, 255)
black = (0, 0, 0)
red = (175, 0, 0)
green = (0, 120, 0)
lightgreen = (0, 175, 0)
bg = (32, 32, 32, 255)



class GomokuUI(object):
    PLAYER_COUNT = 2

    def __init__(self, display_width: int = 900, display_height: int = 650):
        self.current_player = 1
        N = 15
        # 1 is user
        self.current_player = 1
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
        self.board_width = self.line_width * N + self.cell_side * (N - 1)
        res = './res'
        self.background = pygame.image.load(f'{res}/board.png')
        self.panel = pygame.image.load(f'{res}/panel.png')
        self.pieces: List[pygame.Surface] = []
        for i in range(GomokuUI.PLAYER_COUNT):
            self.pieces.append(pygame.image.load(f'{res}/p{i}.png'))

        self.scores = {
            str(i): 0 for i in range(1, GomokuUI.PLAYER_COUNT + 1)
        }
        self.startx = 0
        self.starty = 0
        self.infox = 3 * self.margin + self.board_width
        self.info1_y = 100
        self.info2_y = 263
        self.info_width = 165
        self.info_height = 125
        self.bg_width = (display_width - self.infox) - 1
        self.piece_size = 29
        self.box_line_width = 4

    def side_panel(self, screen: pygame.Surface):
        screen.blit(self.panel, (self.board_width + 2 * self.margin))

    # def hexa_rgb(self, pixel_value):
    #     v = pixel_value / 256
    #     b = pixel_value - v * 256
    #     pixel_value = v
    #     v = pixel_value / 256
    #     g = pixel_value - v * 256
    #     pixel_value = v
    #     v = pixel_value / 256
    #     r = pixel_value - v * 256
    #     return r, g, b

    # def darkBackground(self, screen, display_width, display_height, hexa_rgb):
    #     # pygame.draw.rect(screen,bg,(0,0,display_width,display_height))
    #     pixels = pygame.PixelArray(screen)
    #     for x in range(display_width):
    #         for y in range(display_height):
    #             r, g, b = hexa_rgb(pixels[x][y])
    #             pixels[x][y] = pygame.Color(4, 4, 4)

    def update_info(self, screen: pygame.Surface):
        screen.blit(self.panel, (self.board_width + 3 * self.margin, 0))

        for player in self.scores.keys():
            self.player_info(screen, int(player))

    def text_field(self, text: str,
                   pos: Tuple[int, int],
                   font: pygame.font.SysFont,
                   color: Tuple[int, int, int]) -> Tuple[pygame.Surface, pygame.Rect]:
        field_surface: pygame.Surface = font.render(text, True, color)
        field_rect: pygame.Rect = field_surface.get_rect()
        field_rect.center = pos
        return field_surface, field_rect

    def player_info(self, screen: pygame.Surface, player_no: int):
        base_y = self.info1_y + (player_no - 1) * 163
        if player_no == self.current_player:
            pygame.draw.rect(screen, lightgreen,
                             (self.infox + 2,
                              base_y + 2,
                              self.info_width - 1,
                              self.info_height - 1),
                             self.box_line_width)

        title_field = self.text_field(f'Player {player_no}',
                                      (self.infox + self.info_width // 2,
                                       base_y + self.info_height // 2 - 30),
                                      self.title_font,
                                      red)
        screen.blit(*title_field)

        score_field = self.text_field(f'Score {self.scores[str(player_no)]}',
                                      (self.infox + self.info_width // 2,
                                       base_y + self.info_height // 2),
                                      self.score_font,
                                      green)
        screen.blit(*score_field)

    def main(self):
        screen: pygame.Surface = pygame.display.set_mode((self.display_width, self.display_height),
                                                         pygame.HWSURFACE |
                                                         pygame.DOUBLEBUF)
        pygame.display.set_caption('Gomoku')
        screen.blit(self.background, (0, 0))
        self.update_info(screen)
        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    x,y = pygame.mouse.get_pos()
                    print(x,y)
                    if 36<= x < 609 and 36<= y < 609:
                        self.current_player = 1 if self.current_player == 2 else 2
                        self.update_info(screen)
                pygame.display.update()





if __name__ == '__main__':
    ui = GomokuUI()
    ui.main()
