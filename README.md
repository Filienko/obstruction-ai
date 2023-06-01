# obstruction-ai
A MiniMax with AB pruning implementation of an AI for an obstruction game with a variable, increasing depth look-up. 

To change the initial depth lookup, change the STEP value in Solver

To play with the AI, input [ai_player_turn] [AB or MM] [row * column size]

Where MM = default MiniMax, no pruning, and AB = MiniMax with full AlphaBeta pruning.
e.g.  1 AB 7 * 8

For more examples, look at input.txt file. 
