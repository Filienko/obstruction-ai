# obstruction-ai
A MiniMax with AB pruning implementation of an AI for an obstruction game with a variable, increasing depth look-up. 

To change the initial depth lookup, change the STEP value in Solver

To play with the AI, input [ai_player_turn] [AB or MM] [row * column size]

Where:
MM = default MiniMax, no pruning, and AB = MiniMax with full AlphaBeta pruning.

ai_player_turn set to 1 sets AI to play Max, and 2 means it will attempt optimal Min player moves, limited in optimality due to the depth constraints. 
Increase for STEP results in better overall AI accuracy


MM = default MiniMax, no pruning, and AB = MiniMax with full AlphaBeta pruning.

e.g.  1 AB 7 * 8

For further moves, input your move in row * column coordinate format, utilizing a 1-based input coordinate system. AI will respond with a proper move

e.g. 6 * 8



