import pygame
from checkers.constants import *
import random
from copy import deepcopy

class Gomoku:
    def __init__(self):
        self.board = [[None for _ in range(COLS)] for _ in range(ROWS)]
        self.current_player = 'human'
        self.moves=0
    
    def draw_board(self, win):
        win.fill(WHITE)
        for row in range(ROWS):
            for col in range(COLS):
                pygame.draw.rect(win, BLACK, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 1)
                if self.board[row][col] == 'human':
                    self.draw_cross(win, row, col)
                    # print(f"{row,col}=>{self.board[row][col]}")
                elif self.board[row][col] == 'AI':
                    self.draw_circle(win,row,col)
    
    def draw_cross(self, win, row, col):
        x = col * SQUARE_SIZE
        y = row * SQUARE_SIZE
        pygame.draw.line(win, BLACK, (x, y), (x + SQUARE_SIZE, y + SQUARE_SIZE), 2)
        pygame.draw.line(win, BLACK, (x + SQUARE_SIZE, y), (x, y + SQUARE_SIZE), 2)

    def draw_circle(self,win,row,col):
        x = col * SQUARE_SIZE + SQUARE_SIZE // 2
        y = row * SQUARE_SIZE + SQUARE_SIZE // 2
        pygame.draw.circle(win, BLACK, (x, y), SQUARE_SIZE // 2 - 2, 2)

    
    def make_move(self, row, col):
        if self.board[row][col] is None:
            self.board[row][col] = self.current_player
            self.current_player = 'AI' if self.current_player=='human' else 'human'
            return True
        return False
    
    def ai_move(self):
        if(self.moves<=3):
            row,col = self.random_move(1)
            T = self.make_move(row,col)
            #T is just a place holder as make_move returns true or false
            return

        #check if there is any checkmate moves that AI can take.
        
    def checkmate(self):
        """
        It checks if there's a 
        continuous-five (win condition) in the board
        """
        
        streak = 4
        continous_five_patterns = None
        if(self.current_player == 'AI'): 
            continuous_five_pattern = End_Game_Pattern_AI
        elif(self.current_player == 'human'):
            continuous_five_pattern = End_Game_Pattern_Human
        
        possible_moves = self.generate_possible_moves(1)
        check_mate_moves = []
        
        #the below loop will check if a possible move 
        #can lead to game over situation
        #if it can then the move is added to the checkmate 
        #move
        for move in possible_moves:
            temp_board = deepcopy(self.board)
            temp_board[move[0]][move[1]] = self.current_player
            if self.game_over(temp_board):
                check_mate_moves.append(move)
                
                
        
        
        
        
    def game_over(board):
        """
        It checks if there is a winning pattern in the board
        
        :param board: the current state of the game
        :return: the winner of the game.
        """
        value_lines = State.split_board_to_arrays(board)

        for value_line in value_lines:
            pattern_length = 5
            if(len(value_line) >= pattern_length):
                for i in range(0, len(value_line) - pattern_length + 1):
                    temp_line = [
                        value_line[i],
                        value_line[i+1],
                        value_line[i+2],
                        value_line[i+3],
                        value_line[i+4]
                    ]
                    # HUMAN win
                    if(temp_line == ai_settings.O_END_GAME_PATTERN):
                        return game_settings.O
                    
                    # COM win
                    if(temp_line == ai_settings.X_END_GAME_PATTERN):
                        return game_settings.X
                    
        return game_settings.EMPTY   
    
    def check_winner(self):
        # Implement the logic to check for a winner
        pass

    def alpha_beta_pruning(self):
        # Implement Alpha-Beta pruning logic for AI moves
        pass
    
    # def random_move(self,expansion_range):
    #     possible_moves = self.generate_possible_moves(expansion_range)
    #     return random.choice(possible_moves)

    def random_move(self,expansion_range):
        possible_moves = self.generate_possible_moves(expansion_range)
        return random.choice(possible_moves)

    def generate_possible_moves(self,expansion_range):
        """
        returns 
        all the possible moves that are
        not empty and have a neighbor
        """
        
        possible_moves = []
        for r in range(0, ROWS):
            for c in range(0, COLS):
                temp_move = self.board[r][c]
                if(temp_move != None):
                    continue
                
                neighbor = 0
                valid = 0
                
                for i in range(-expansion_range,expansion_range+1):
                    for j in range(-expansion_range,expansion_range+1):
                        neighbor_r = i+r
                        neighbor_c = j+c
                        
                        if(0 <= neighbor_r < ROWS and 0 <= neighbor_c < COLS):
                            
                            neighbor = self.board[neighbor_r][neighbor_c]
                            
                        if(neighbor != 0):
                            break
                
                        
                
                if neighbor==0:
                    continue
                
                possible_moves.append((r, c))
        
        return possible_moves    
        
    