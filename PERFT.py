import engine
import Functions
import time

FEN = input("FEN: ")
if FEN == "def":
        FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq'

ConvertedFEN = Functions.ConvertFENString(FEN)

BoardConfig = [list(map(int, i)) for i in ConvertedFEN[0]]

WhiteToMove = ConvertedFEN[1]

KQkqCanCastle = ConvertedFEN[2]

depth = int(input("Depth: "))

# Om te runnen: py PERFT.py

# Perft Debug Fuction
# Om te kijken of de engine alle moves kan vinden
# Waardes kloppen niet met andere engines omdat wij geen En Passant of Rokeren aan de praat hebben gekregen
# https://www.chessprogramming.org/Perft_Results

def perft(depth, BoardConfig, WhiteToMove, KQkqCanCastle):
    legalmoves = engine.CalcFinalLegalMoves(BoardConfig, WhiteToMove, KQkqCanCastle)[0]

    Side = WhiteToMove

    if depth == 1:
        return len(legalmoves[0])
        
    count = 0

    for move in range(len(legalmoves[0])):
        BoardConfigReset = [x[:] for x in BoardConfig]
        BoardConfigReset = engine.MakeMoveCalculations(legalmoves[0][move], legalmoves[1][move], BoardConfigReset, legalmoves)
        Nodes = perft(depth - 1, BoardConfigReset, not Side, KQkqCanCastle)
        count += Nodes
           
    return count



start = time.perf_counter_ns()
perftresult = perft(depth, BoardConfig, WhiteToMove, KQkqCanCastle)
end = time.perf_counter_ns()

print(perftresult, str((end - start) / 1000000) + " ms")



# Resultaten van eerste 5 depths vergelijken met de goede waardes
if FEN == "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq": 
	if depth == 1: 
		print(str(20-perftresult) + " missing, expected 20 recieved: " + str(perftresult))
	elif depth == 2:
		print(str(400-perftresult) + " missing, expected 400 recieved: " + str(perftresult))
	elif depth == 3:
		print(str(8902-perftresult) + " missing, expected 8902 recieved: " + str(perftresult))
	elif depth == 4:
		print(str(197281-perftresult) + " missing, expected 197281 recieved: " + str(perftresult))
	elif depth == 5:
		print(str(4865609-perftresult) + " missing, expected 4865609 recieved: " + str(perftresult))

input()
quit()

