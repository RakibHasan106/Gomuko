WIDTH = 800
HEIGHT = 800
ROWS,COLS = 15, 15
SQUARE_SIZE = WIDTH//COLS

WHITE = (255,255,255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

BackGroundColor = (202,228,241)

# EVALUATION SCORES

SCORE_4_UNBLOCKED_PIECES = 50_007
SCORE_3_UNBLOCKED_PIECES = 5_005
SCORE_2_UNBLOCKED_PIECES = 103
SCORE_1_UNBLOCKED_PIECES = 11

SCORE_5_BLOCKED_PIECES = 1_000_009 # WIN
SCORE_4_BLOCKED_PIECES = 6_007
SCORE_3_BLOCKED_PIECES = 185

End_Game_Pattern_AI = ['AI', 'AI', 'AI', 'AI', 'AI']
End_Game_Pattern_Human = ['human', 'human', 'human', 'human', 'human']



# EVALUATION PATTERNS
AI_6_PATTERNS = [[None, 'AI', 'AI', 'AI', 'AI', None],
                [None, 'AI', 'AI', 'AI', None, None],
                [None, None, 'AI', 'AI', 'AI', None],
                [None, 'AI', 'AI', None, 'AI', None],
                [None, 'AI', None, 'AI', 'AI', None],
                [None, None, 'AI', 'AI', None, None],
                [None, None, 'AI', None, 'AI', None],
                [None, 'AI', None, 'AI', None, None],
                [None, 'AI', None, None, 'AI', None],
                [None, None, 'AI', None, None, None],
                [None, None, None, 'AI', None, None]]

AI_6_PATTERNS_SCORES = [
    SCORE_4_UNBLOCKED_PIECES, 
    SCORE_3_UNBLOCKED_PIECES, 
    SCORE_3_UNBLOCKED_PIECES, 
    SCORE_3_UNBLOCKED_PIECES, 
    SCORE_3_UNBLOCKED_PIECES, 
    SCORE_2_UNBLOCKED_PIECES, 
    SCORE_2_UNBLOCKED_PIECES, 
    SCORE_2_UNBLOCKED_PIECES, 
    SCORE_2_UNBLOCKED_PIECES, 
    SCORE_1_UNBLOCKED_PIECES, 
    SCORE_1_UNBLOCKED_PIECES]

AI_5_PATTERNS = [['AI', 'AI', 'AI', 'AI', 'AI'],
                ['AI', 'AI', 'AI', 'AI', None],
                [None, 'AI', 'AI', 'AI', 'AI'],
                ['AI', 'AI', None, 'AI', 'AI'],
                ['AI', None, 'AI', 'AI', 'AI'],
                ['AI', 'AI', 'AI', None, 'AI'],
                ['AI', None, 'AI', None, 'AI'],
                ['AI', 'AI', None, None, 'AI'],
                ['AI', None, None, 'AI', 'AI'],
                [None, 'AI', 'AI', None, 'AI'],
                ['AI', None, 'AI', 'AI', None],
                [None, 'AI', 'AI', 'AI', None],
                ['AI', 'AI', 'AI', None, None],
                [None, None, 'AI', 'AI', 'AI']]

AI_5_PATTERNS_SCORES = [
    SCORE_5_BLOCKED_PIECES, 
    SCORE_4_BLOCKED_PIECES, 
    SCORE_4_BLOCKED_PIECES, 
    SCORE_4_BLOCKED_PIECES,
    SCORE_4_BLOCKED_PIECES, 
    SCORE_4_BLOCKED_PIECES, 
    SCORE_3_BLOCKED_PIECES, 
    SCORE_3_BLOCKED_PIECES, 
    SCORE_3_BLOCKED_PIECES, 
    SCORE_3_BLOCKED_PIECES, 
    SCORE_3_BLOCKED_PIECES, 
    SCORE_3_BLOCKED_PIECES, 
    SCORE_3_BLOCKED_PIECES, 
    SCORE_3_BLOCKED_PIECES]

AI_END_GAME_PATTERN = ['AI', 'AI', 'AI', 'AI', 'AI']

human_6_PATTERNS = [[None, 'human', 'human', 'human', 'human', None],
                [None, 'human', 'human', 'human', None, None],
                [None, None, 'human', 'human', 'human', None],
                [None, 'human', 'human', None, 'human', None],
                [None, 'human', None, 'human', 'human', None],
                [None, None, 'human', 'human', None, None],
                [None, None, 'human', None, 'human', None],
                [None, 'human', None, 'human', None, None],
                [None, 'human', None, None, 'human', None],
                [None, None, 'human', None, None, None],
                [None, None, None, 'human', None, None]]

human_6_PATTERNS_SCORES = [
    SCORE_4_UNBLOCKED_PIECES, 
    SCORE_3_UNBLOCKED_PIECES, 
    SCORE_3_UNBLOCKED_PIECES, 
    SCORE_3_UNBLOCKED_PIECES, 
    SCORE_3_UNBLOCKED_PIECES, 
    SCORE_2_UNBLOCKED_PIECES, 
    SCORE_2_UNBLOCKED_PIECES, 
    SCORE_2_UNBLOCKED_PIECES, 
    SCORE_2_UNBLOCKED_PIECES, 
    SCORE_1_UNBLOCKED_PIECES, 
    SCORE_1_UNBLOCKED_PIECES]

human_5_PATTERNS = [['human', 'human', 'human', 'human', 'human'],
                ['human', 'human', 'human', 'human', None],
                [None, 'human', 'human', 'human', 'human'],
                ['human', 'human', None, 'human', 'human'],
                ['human', None, 'human', 'human', 'human'],
                ['human', 'human', 'human', None, 'human'],
                ['human', None, 'human', None, 'human'],
                ['human', 'human', None, None, 'human'],
                ['human', None, None, 'human', 'human'],
                [None, 'human', 'human', None, 'human'],
                ['human', None, 'human', 'human', None],
                [None, 'human', 'human', 'human', None],
                ['human', 'human', 'human', None, None],
                [None, None, 'human', 'human', 'human']]

human_5_PATTERNS_SCORES = [
    SCORE_5_BLOCKED_PIECES, 
    SCORE_4_BLOCKED_PIECES, 
    SCORE_4_BLOCKED_PIECES, 
    SCORE_4_BLOCKED_PIECES,
    SCORE_4_BLOCKED_PIECES, 
    SCORE_4_BLOCKED_PIECES, 
    SCORE_3_BLOCKED_PIECES, 
    SCORE_3_BLOCKED_PIECES, 
    SCORE_3_BLOCKED_PIECES, 
    SCORE_3_BLOCKED_PIECES, 
    SCORE_3_BLOCKED_PIECES, 
    SCORE_3_BLOCKED_PIECES, 
    SCORE_3_BLOCKED_PIECES, 
    SCORE_3_BLOCKED_PIECES]


# CHECK BEFORE ALPHA BETA PRUNING
ENABLE_HIGH_IMPACT_MOVE = True 
# lower this setting value could reduce time AI thinking but also reduce move quality
HIGH_IMPACT_MOVE_THRESHOLD = 15440 #15440
# a high impact move is a move which could lead to a win or great advantage
