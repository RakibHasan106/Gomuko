import pygame
from checkers.constants import *
from gomoku import Gomoku

pygame.init()

FPS = 60

window = pygame.display.set_mode((WIDTH,HEIGHT)) 
pygame.display.set_caption('Gomuko')

# button_font = pygame.font.Font(None,74)
# button_text = button_font.render('Play Game',True,WHITE )
# button_rect = button_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

start_img = pygame.image.load('images/start_btn.png').convert_alpha()
exit_img = pygame.image.load('images/exit_btn.png').convert_alpha()

class Button():
    def __init__(self,x,y,image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        
    def draw(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

start_btn = Button(WIDTH//2 - start_img.get_width() // 2 , HEIGHT//2 - start_img.get_height() // 2,start_img)
exit_btn = Button(WIDTH//2 - exit_img.get_width() // 2 , HEIGHT//2 - exit_img.get_height() // 2,exit_img)

def draw_menu():
    window.fill(BackGroundColor)    
    start_btn.draw()
    pygame.display.flip()

def draw_game(game):
    game.draw_board(window)
    pygame.display.flip()
    
def check_winner(board, player):
    for row in range(ROWS):
        for col in range(COLS):
            if check_five_in_a_row(board, player, row, col):
                return True
    return False

def check_five_in_a_row(board, player, row, col):
    # Check horizontally
    if col <= COLS - 5 and all(board[row][c] == player for c in range(col, col + 5)):
        return True
    # Check vertically
    if row <= ROWS - 5 and all(board[r][col] == player for r in range(row, row + 5)):
        return True
    # Check diagonal /
    if row >= 4 and col <= COLS - 5 and all(board[row - i][col + i] == player for i in range(5)):
        return True
    # Check diagonal \
    if row <= ROWS - 5 and col <= COLS - 5 and all(board[row + i][col + i] == player for i in range(5)):
        return True
    return False




def main():
    menu = True
    game = False
    
    gomoku_game = Gomoku()
    
    run = True
    clock = pygame.time.Clock()
        
    while run:
        clock.tick(FPS)
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if menu and start_btn.rect.collidepoint(event.pos):
                    menu = False 
                    game = True
                elif menu and exit_btn.rect.collidepoint(event.pos):
                    """This button will exit the user fronm the game """
                    """There could be some other buttons which will allow user to use different difficulty modes."""
                    pass
                elif game and gomoku_game.current_player == 'human':
                    x,y = event.pos
                    row,col = y // SQUARE_SIZE, x // SQUARE_SIZE
                    if gomoku_game.make_move(row,col):
                        gomoku_game.moves+=1
                        if gomoku_game.check_winner():
                            print(f"{gomoku_game.current_player} wins!")
                            pass
                # pass
        if game and gomoku_game.current_player == 'AI':
            gomoku_game.ai_move()
            gomoku_game.moves+=1
            gomoku_game.current_player = 'human'
            print("Currently AI move")
            if gomoku_game.check_winner():
                print(f"{gomoku_game.current_player} wins!")
                run = False
                
        if menu:
            draw_menu()
        elif game:
            draw_game(gomoku_game)
        # pygame.display.flip()
            
    pygame.quit()
        
main()