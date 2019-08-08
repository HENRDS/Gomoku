import sys
from typing import List, Tuple
import pygame
from board import BoardState, WinnerException
from jorge import Jorge


pygame.init()

# Colors in the interface
white = (255, 255, 255)
black = (0, 0, 0)
medium_blue = (0, 0, 205)
green = (0, 120, 0)
dodger_blue = (30, 144, 255)
bg = (32, 32, 32, 255)


class GomokuUI(object):
    """
    This class represents the Gomuku interface
    """
    PLAYER_COUNT = 2

    def __init__(self, display_width: int = 900, display_height: int = 650):
        """
        Defines the sizes, fonts and images in the game Surface

        :param display_width:
        :param display_height:
        """
        N = 15
        # 1 is user
        self.jorge = Jorge(2, GomokuUI.PLAYER_COUNT)
        self.jorges = []
        self.board: BoardState = BoardState()
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
        self.has_winner = False
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

    def update_info(self, screen: pygame.Surface):
        """
        Updates the screen
        :param screen:
        :return:
        """
        screen.blit(self.panel, (self.board_width + 3 * self.margin, 0))

        for player in self.scores.keys():
            self.player_info(screen, int(player))

    def text_field(self, text: str,
                   pos: Tuple[int, int],
                   font: pygame.font.SysFont,
                   color: Tuple[int, int, int]) -> Tuple[pygame.Surface, pygame.Rect]:
        """
        Show the text field in the Surface
        :param text:
        :param pos:
        :param font:
        :param color:
        :return:
        """
        field_surface: pygame.Surface = font.render(text, True, color)
        field_rect: pygame.Rect = field_surface.get_rect()
        field_rect.center = pos
        return field_surface, field_rect

    def player_info(self, screen: pygame.Surface, player_no: int):
        """
        Show the currently player information
        :param screen:
        :param player_no:
        :return:
        """
        base_y = self.info1_y + (player_no - 1) * 163
        if player_no == self.current_player:
            pygame.draw.rect(screen, dodger_blue,
                             (self.infox + 2,
                              base_y + 2,
                              self.info_width - 1,
                              self.info_height - 1),
                             self.box_line_width)

        title_field = self.text_field(f'Player {player_no}',
                                      (self.infox + self.info_width // 2,
                                       base_y + self.info_height // 2 - 30),
                                      self.title_font,
                                      medium_blue)
        screen.blit(*title_field)

        score_field = self.text_field(f'Score {self.scores[str(player_no)]}',
                                      (self.infox + self.info_width // 2,
                                       base_y + self.info_height // 2),
                                      self.score_font,
                                      green)
        screen.blit(*score_field)

    def get_position_piece(self, x: int, y: int):
        """
        Get the position at the right spot on the Surface
        :param x:
        :param y:
        :return:
        """
        step = self.cell_side + self.line_width
        size_x = (x - 36) / step
        size_y = (y - 36) / step
        return round(size_x), round(size_y)

    def win_screen(self, screen: pygame.Surface):
        if self.current_player == 1:
            txt = 'You won mothafucker!'
            img = pygame.image.load('./res/youwon.png')
            pos = (200, 300)
        else:
            img = pygame.image.load('./res/youlost.png')
            txt = 'You lost mothafucker!'
            pos = (0, 300)

        leaf = pygame.image.load('./res/med.png')
        font = pygame.font.SysFont('Calibri', 84)
        field = self.text_field(txt, (500, 250), font, green)
        screen.blit(*field)
        screen.blit(img, pos)
        screen.blit(leaf, (0, 350))
        screen.blit(leaf, (600, 350))

    def next_player(self):
        score = self.board.score(self.current_player, self.PLAYER_COUNT)
        self.scores[str(self.current_player)] = score
        if score == BoardState.MAX_SCORE:
            raise WinnerException(self.current_player)
        if self.current_player == GomokuUI.PLAYER_COUNT:
            self.current_player = 1
        else:
            self.current_player += 1

    def play_piece(self, col: int, row: int, screen: pygame.Surface):
        """
        Select the piece and put on the Surface
        :param col:
        :param row:
        :param screen:
        :return:
        """
        step = self.cell_side + self.line_width
        d = 23 // 2
        x = ((col * step) + 36) - d
        y = ((row * step) + 36) - d
        piece = self.pieces[self.current_player - 1]
        screen.blit(piece, (x, y))
        self.board = self.board.after_play(row, col, self.current_player)
        try:
            self.next_player()
        except WinnerException:
            self.win_screen(screen)
            self.has_winner = True
            return
        self.update_info(screen)
        pygame.display.update()

    def user_turn(self, screen: pygame.Surface):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    if (not (36 <= x < 609)) or (not (36 <= y < 609)):
                        print('invalid pos')
                        continue
                    col, row = self.get_position_piece(x, y)
                    if self.board.is_valid(row, col):
                        self.play_piece(col, row, screen)
                        return
                pygame.display.update()

    def jorge_turn(self, screen: pygame.Surface):
        row, col = self.jorge.play(self.board)
        if not self.board.is_valid(row, col):
            raise Exception()
        self.play_piece(col, row, screen)

    def main(self):
        screen: pygame.Surface = pygame.display.set_mode((self.display_width, self.display_height),
                                                         pygame.HWSURFACE |
                                                         pygame.DOUBLEBUF)
        pygame.display.set_caption('Gomoku')
        screen.blit(self.background, (0, 0))
        self.update_info(screen)
        while True:
            if not self.has_winner:
                if self.current_player == 1:
                    self.user_turn(screen)
                else:
                    self.jorge_turn(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                pygame.display.update()


if __name__ == '__main__':
    ui = GomokuUI()
    ui.main()
