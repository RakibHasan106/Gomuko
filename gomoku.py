import pygame
from Minimax import MinimaxNode
from checkers.constants import *
import random
from copy import deepcopy
from math import inf as infinity

class Gomoku:
    def __init__(self):
        self.board = [[None for _ in range(COLS)] for _ in range(ROWS)]
        self.current_player = 'human'
        self.moves = []
    
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
        """
        First Checking if the game has just started
        i.e. there is not enough move so that AI can choose a move
        intelligently.
        """
        if(len(self.moves)<=3):
            row,col = self.random_move(1)
            # T = self.make_move(row,col)
            #T is just a place holder as make_move returns true or false
            return row,col
        
        """
        If there is enough moves,(>3)
        then check if there is any checkmate
        moves that AI can take
        """
        #check if there is any checkmate moves that AI can take.
        chkmate = self.checkmate()
        
        if chkmate:
            print("AI checkmate move")
            return chkmate  
        
        """
        If there is no checkmate moves as well, 
        then check if there is any high impact move
        """
        # =======================================
        # HIGH-IMPACT MOVE
        # if opponent or AI has a high-impact move, 
        # AI will take whether move which has highest score
        
        print("Checking for high-impact move...")
        opponent = 'AI' if self.current_player=='human' else 'human'
        if ENABLE_HIGH_IMPACT_MOVE:
            opponent_high_impact_move, opponent_high_impact_score = self.high_impact_move(opponent)
            com_high_impact_move, com_high_impact_score = self.high_impact_move(self.current_player)
            
            if opponent_high_impact_move and opponent_high_impact_score > com_high_impact_score : 
                
                print("AI may loose as HUMAN has a high-impact move.")
                print("AI has taken this move (a defensive move).")
                
                return opponent_high_impact_move
            # >=: Prioritize playing the move to the advantage of the player
            if com_high_impact_move and com_high_impact_score >= opponent_high_impact_score: 
                # Announcement
                print("AI may win it has a high-impact move.")
                print("AI has taken this move (an offensive move).")
                
                return com_high_impact_move
            
            print("No high impact moves")
        
        
        
        
        """
        If there is no high impact move as well, 
        then check if there is any combo move
        """
        # =======================================
        # COMBO MOVE
        # if opponent or AI has a combo move, AI will take this move
        
        # Announcement
        print("Checking for combo moves...")
        
        opponent_combo_move = self.combo_move(self.board,opponent)
        com_combo_move = self.combo_move(self.board,self.current_player)
        
        if com_combo_move:
            print("AI has a combo move. Take it!")
            
            return com_combo_move

        if opponent_combo_move:
            # Announcement
            print("HUMAN has a combo move. Block it!")
            
            return opponent_combo_move
        
        """
        If there is no combo move as well, 
        AI will use alpha_beta_pruning algorithm to 
        find the best move
        """
        print("There is no combo move.")
        print("---------------------------------")


        # Announcement
        print("will use the Alpha-Beta pruning algorithm. Calculating...")
        
        root_node = MinimaxNode(self.board, self.moves[-1::1], self.current_player, None)
       
        MAX_TREE_DEPTH_LEVEL = 2 #the maximum depth the AI will search 
        
        score = self.alpha_beta(root_node, MAX_TREE_DEPTH_LEVEL, -infinity, +infinity, True)
        # Announcement
        print("Completed calculation with depth = ", MAX_TREE_DEPTH_LEVEL, ".")

        return root_node.planing_next_move
    
    
    def combo_move(self,board,current_turn):
        
        # combo move
        # is a combo which could create
        # a one-end-blocked-four and a unblocked three 
        # or n blocked-four (n>=2)

        # get moves that could create
        # one-end-blocked-four
        
        blocked_four_patterns = []
        blocked_four_pattern_length = 5
        matched_blocked_four_pattern_move_direction_list = []
        move_direction_dictionary = dict()
        
        # add element(s) to blocked_four_patterns
        if(current_turn == 'AI'):
            for pattern in AI_5_PATTERNS:
                if(pattern.count('AI') == 4):
                    blocked_four_patterns.append(pattern)
        elif(current_turn == 'human'):
            for pattern in human_5_PATTERNS:
                if(pattern.count('human') == 4):
                    blocked_four_patterns.append(pattern)
                    
        # scan for blocked-four
        
        possible_moves = self.generate_possible_moves(board,2)
        
        for p_m_move in possible_moves:
            move_direction_set = set()
            matched_direction_count = 0
            
            direction_pattern_tuples = self.get_direction_pattern_tuples(board, p_m_move, 4, current_turn)
            
            if(len(direction_pattern_tuples)>0):
                for tuple in direction_pattern_tuples:
                    direction, pattern = tuple
                    for i in range(0, len(pattern) - blocked_four_pattern_length+1):
                        checking_pattern = [
                            pattern[i],
                            pattern[i+1],
                            pattern[i+2],
                            pattern[i+3],
                            pattern[i+4],
                        ]
                        has_pattern_in_this_direction = False
                        for blocked_four_pattern in blocked_four_patterns:
                            if(checking_pattern == blocked_four_pattern):
                                has_pattern_in_this_direction = True
                                move_direction_dictionary[p_m_move] = (direction,checking_pattern)
                        
                        if has_pattern_in_this_direction:
                            matched_blocked_four_pattern_move_direction_list.append((direction, p_m_move))
                            if (direction, p_m_move) not in move_direction_set:
                                move_direction_set.add((direction, p_m_move))
                                matched_direction_count += 1
                                # this means that move can create at least 2 blocked fours -> a combo move
                                if matched_direction_count > 1:
                                    return p_m_move   
            
        # for each move that could create one-end-blocked-four, 
        # we scan if there is any unblocked-three created by that move
        if len(matched_blocked_four_pattern_move_direction_list) >= 1:
            
            move_pos_in_pattern = 4
            # scan for unblocked-three
            for p_m_move in matched_blocked_four_pattern_move_direction_list:
                blocked_four_direction, blocked_four_move = p_m_move
                direction_pattern_tuples = self.get_direction_pattern_tuples(board, blocked_four_move, move_pos_in_pattern, current_turn)  
                
                if(len(direction_pattern_tuples) > 0) :
                    for tuple in direction_pattern_tuples:
                        direction, pattern = tuple # len(pattern) = 7
                        # make sure that current_turn is counted in pattern
                        if(pattern[move_pos_in_pattern] == current_turn): # center pattern must be the current move
                            M = current_turn
                            E = None
                            opponent = 'AI' if self.current_player=='human' else 'human'
                            check_left_pattern = pattern[1:5].count(current_turn) >= 3 and pattern[0:5].count(opponent) == 0
                            check_right_pattern = pattern[4:].count(current_turn) >= 3 and pattern[4:].count(opponent) == 0
                            check_center_pattern = (
                                pattern[2:7] == [E, M, M, M, E] 
                                or pattern[1:7] == [E, M, E, M, M, E]
                                or pattern[2:-1] == [E, M, M, E, M, E]
                                )

                            has_unblocked_three = check_left_pattern or check_right_pattern or check_center_pattern
                            if(has_unblocked_three and direction != blocked_four_direction):
                                return blocked_four_move            

        return None
                
            
            
            
    def get_direction_pattern_tuples(self,board,move,streak,current_turn):
        """
            It takes a board, a move, 
            a streak, and the current turn, 
            and returns a list of lists of the
            pieces in the directions of the move
        
            :param board: the current board (will not be changed after running this function)
            :param move: the move that is being evaluated
            :param streak: the number of pieces in a row needed to win
            :param current_turn: the current player's turn
            :return: A list of lists of patterns.
        """
            
        if not self.is_valid_move(move, board):
            return []
        # streak = number of unblocked pieces
        move_r, move_c = move
        # r ~ x
        # c ~ y
        direction_patterns = []
        # horizontal
        pattern = []
        for i in range(-streak, streak + 1):
            if(i == 0):
                temp_move = move
                pattern.append(current_turn)
            else:
                temp_move = (move_r + i, move_c)
                if(self.is_valid_move(temp_move, board)):
                    temp_move_r, temp_move_c = temp_move
                    pattern.append(board[temp_move_r][temp_move_c])
        if(len(pattern) > streak + 2):
            direction_patterns.append(('H', pattern))

        # vertical
        pattern = []
        for i in range(-streak, streak + 1):
            if(i == 0):
                temp_move = move
                pattern.append(current_turn)
            else:
                temp_move = (move_r, move_c + i)
                if(self.is_valid_move(temp_move, board)):
                    temp_move_r, temp_move_c = temp_move
                    pattern.append(board[temp_move_r][temp_move_c])
        if(len(pattern) > streak + 2):
            direction_patterns.append(('V', pattern))

        # diagonals
        # lower-left to upper-right
        pattern = []
        for i in range(-streak, streak + 1):
            if(i == 0):
                temp_move = move
                pattern.append(current_turn)
            else:
                temp_move = (move_r + i, move_c + i)
                if(self.is_valid_move(temp_move, board)):
                    temp_move_r, temp_move_c = temp_move
                    pattern.append(board[temp_move_r][temp_move_c])
        if(len(pattern) > streak + 2):
            direction_patterns.append(('D1', pattern))
        # upper-left to lower-right
        pattern = []
        for i in range(-streak, streak + 1):
            if(i == 0):
                temp_move = move
                pattern.append(current_turn)
            else:
                temp_move = (move_r - i, move_c + i)
                if(self.is_valid_move(temp_move, board)):
                    temp_move_r, temp_move_c = temp_move
                    pattern.append(board[temp_move_r][temp_move_c])
        if(len(pattern) > streak + 2):
            direction_patterns.append(('D2', pattern))

        return direction_patterns
            
    def is_valid_move(self,move_position, board):
        """
        It checks if the move is valid.
        
        :param move_position: the position of the move
        :param board: the board that the player is playing on
        :return: The return value is a boolean value.
        """
        move_r, move_c = move_position
        is_r_valid = (0 <= move_r < ROWS)
        is_c_valid = (0 <= move_c < COLS)
        return is_c_valid and is_r_valid  
    
    
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
        
        possible_moves = self.generate_possible_moves(self.board,1)
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

        if(len(check_mate_moves)>0):
            score = -infinity
            best_move = None
            
            for move in check_mate_moves:
                temp_board = deepcopy(self.board)
                temp_board[move[0]][move[1]] = self.current_player
                AI_score, human_score = self.evaluate(temp_board)
                temp_score = 0
                if(self.current_player == 'human'):
                    temp_score = AI_score - human_score
                else:
                    temp_score = human_score - AI_score
                if(temp_score > score):
                    score = temp_score
                    best_move = move
                
                return best_move
        
        else:
            return None
                
    def evaluate(self,board):
        """
        It takes a board and returns a tuple of 
        for each player
        
        """
        AI_score = 0
        human_score = 0
        
        lines = self.split_board_to_arrays(board)
        for line in lines : 
            line_AI_score , line_human_score = self.evaluate_line(line)
            AI_score += line_AI_score
            human_score += line_human_score
            
        return (AI_score, human_score)
    
    def split_board_to_arrays(self,board):
        """
        It takes a 2D array and returns a list of 1D arrays,
        where each 1D array is a row, column, or
        diagonal of the original 2D array
        """
        res_arrays = []
        # diagonals: (SQUARE ONLY)
        # https://stackoverflow.com/questions/6313308/get-all-the-diagonals-in-a-matrix-list-of-lists-in-python

        # convert "upper left - lower right" diagonal lines to list of "straight lines"
        #   0 1 2         list[[]]
        # 0 ⟍ ⟍ ⟍        —
        # 1 ⟍ ⟍ ⟍        — —
        # 2 * ⟍ ⟍    =>  — — —
        #                 — —
        #                 —
        # start at *
        diagonal_count = range(-(ROWS-1),COLS)
        for d in diagonal_count:
            res_arrays.append( [ row[r+d] for r,row in enumerate(board) if 0 <= r+d < len(row)] )
        
        # convert "lower left - upper right" diagonal lines to list of "straight lines"
        #   0 1 2         list[[]]
        # 0 ⟋ ⟋ ⟋        —
        # 1 ⟋ ⟋ ⟋        — —
        # 2 ⟋ ⟋ *    =>  — — —
        #                 — —
        #                 —
        # start at *
        
        for d in diagonal_count:
            res_arrays.append( [ row[~(r+d)] for r,row in enumerate(board) if 0 <= r+d < len(row)] )
    
        #rows
        for row in board:
            res_arrays.append(deepcopy(row))
        
        #columns
        for c in range(0, COLS):
            temp_column = []
            for r in range(0,ROWS):
                temp_column.append(board[r][c])
            res_arrays.append(temp_column)
            
        return res_arrays
            
        
    def evaluate_line(self,line):
        """
        It takes a line of the board
        and returns the score for AI and human
        """
        AI_score = 0
        human_score = 0

        # check 6 patterns
        pattern_length = 6
        if(len(line) >= pattern_length):
            for i in range(0, len(line) - pattern_length + 1):
                temp_line = [
                    line[i],
                    line[i+1],
                    line[i+2],
                    line[i+3],
                    line[i+4],
                    line[i+5]
                ]
                # human score
                for p, pattern in enumerate(human_6_PATTERNS):
                    if(temp_line == pattern):
                        human_score += human_6_PATTERNS_SCORES[p]

                # AI score
                for p, pattern in enumerate(AI_6_PATTERNS):
                    if(temp_line == pattern):
                        AI_score += AI_6_PATTERNS_SCORES[p]

        # check 6 patterns
        pattern_length = 5
        if(len(line) >= pattern_length):
            for i in range(0, len(line) - pattern_length + 1):
                temp_line = [
                    line[i],
                    line[i+1],
                    line[i+2],
                    line[i+3],
                    line[i+4]
                ]
                # human score
                for p, pattern in enumerate(human_5_PATTERNS):
                    if(temp_line == pattern):
                        human_score += human_5_PATTERNS_SCORES[p]

                # X score
                for p, pattern in enumerate(AI_5_PATTERNS):
                    if(temp_line == pattern):
                        AI_score += AI_5_PATTERNS_SCORES[p]
        return(human_score, AI_score)

    def high_impact_move(self, current_turn):
        """
        It takes a board and a player, 
        and returns the move that would have the highest 
        impact on the board, and the score of that move
        
        :return: A tuple of the highest score move and
        the highest score. 
        Return (None, 0) if the highest impact move's score
        do not reach HIGH_IMPACT_MOVE_THRESHOLD.
        """
        
        temp_board = deepcopy(self.board)
        board_AI_score , board_human_score = self.evaluate(temp_board)
        
        highest_score = 0
        highest_score_move = None
        
        for r in range(0, ROWS):
            for c in range(0, COLS):
                if(temp_board[r][c] == None):
                    temp_board[r][c] = current_turn
                    temp_board_AI_score , temp_board_human_score = self.evaluate(temp_board)

                    score = 0
                    
                    if(current_turn == 'AI'):
                        score = temp_board_AI_score - board_AI_score
                    elif(current_turn == 'human'):
                        score = temp_board_human_score - board_human_score
                    
                    if(score > highest_score):
                        highest_score = score 
                        highest_score_move = (r,c)
                    
                    temp_board[r][c] = None
        if(highest_score >= HIGH_IMPACT_MOVE_THRESHOLD):
            return (highest_score_move,highest_score)

        else:
            return (None,0)
        
        
    def game_over(self,board):
        """
        It checks if there is a winning pattern in the board
        
        :param board: the current state of the game
        :return: the winner of the game.
        """
        value_lines = self.split_board_to_arrays(board)

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
                    if(temp_line == End_Game_Pattern_Human):
                        return 'human' #human wins
                    
                    # COM win
                    if(temp_line == End_Game_Pattern_AI):
                        return 'AI' #AI wins
                    
        return None  #meaning game over 
    
    # def check_winner(self):
    #     # Implement the logic to check for a winner
    #     pass

    def alpha_beta(self,current_node: MinimaxNode, depth, alpha, beta, maximizingPlayer):
        #refernce from gfg
        
        # to understand this implementation : https://www.youtube.com/watch?v=l-hh51ncgDI&ab_channel=SebastianLague
        # Here maximizingPlayer variable means whether it's turn of max player or not.
        
        if(depth == 0 or self.game_over(current_node.board)):
            AI_score, human_score = self.evaluate(current_node.board)
            return AI_score - human_score
        
        if maximizingPlayer:
            value = -infinity
            child_nodes = current_node.generate_child_nodes()
            for child_node in child_nodes:
                temp = self.alpha_beta(child_node, depth - 1, alpha, beta, False)
                alpha = max(alpha, value)
            
                if temp > value:
                    value = temp
                    current_node.planing_next_move = child_node.last_move
                if value >= beta:
                    break
            return value
        else:
            value = + infinity
            child_nodes = current_node.generate_child_nodes()
            for child_node in child_nodes:
                temp = self.alpha_beta(child_node, depth - 1, alpha, beta, True)
                if temp < value:
                    value = temp
                    current_node.planing_next_move = child_node.last_move
                beta = min(beta, value)
            return value

    def random_move(self,expansion_range):
        possible_moves = self.generate_possible_moves(self.board,expansion_range)
        return random.choice(possible_moves)

    def generate_possible_moves(self,board,expansion_range):
        """
        returns 
        all the possible moves that are
        not empty and have a neighbor
        """
        
        possible_moves = []
        for r in range(0, ROWS):
            for c in range(0, COLS):
                temp_move = board[r][c]
                if(temp_move != None): 
                    #if the move we are intentended to do is already occupied , 
                    #we will skip that square of the board
                    # (i.e it is not possible to move to that square(invalid) as it is already occupied)
                    continue
                
                neighbor = None
                # valid = 0
                
                #after checking if the square is occupied or not
                #now we will check if there is any occupied neighbour of that square
                #if there is occupied neighbour we will append the square to possible moves.
                
                #This logic implies that the AI will never choose a desserted square from the board. 
                # desserted square = the square which has no neighbour occupied square
                
                
                for i in range(-expansion_range,expansion_range+1):
                    for j in range(-expansion_range,expansion_range+1):
                        neighbor_r = i+r
                        neighbor_c = j+c
                        
                        if(0 <= neighbor_r < ROWS and 0 <= neighbor_c < COLS):
                            
                            neighbor = board[neighbor_r][neighbor_c]
                            
                        if(neighbor != None):
                            break
                
                
                if neighbor == None:
                    continue
                
                possible_moves.append((r, c))
        
        return possible_moves