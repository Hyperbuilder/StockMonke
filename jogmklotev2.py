import CalcLegalMoves
import engine
import Functions
import time

FEN = input("FEN: ")
if FEN == "def":
        FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'

BoardConfig = [list(map(int, i)) for i in Functions.ConvertFENString(FEN)[0]]

WhiteToMove = Functions.ConvertFENString(FEN)[1]


#CalcLegalMoves.FinalLegalMoves(BoardConfig, WhiteToMove)




#Perft

def perft(depth, BoardConfig, WhiteToMove):

	legalmoves = CalcLegalMoves.FinalLegalMoves(BoardConfig, WhiteToMove)[0]
	
	if depth == 1:    
		return len(legalmoves[0])

	elif depth > 1:
		count = 0

		for move in range(len(legalmoves[0])):
			Functions.MakeMove(legalmoves[0][move], legalmoves[1][move], BoardConfig, legalmoves)
			count += perft(depth - 1, BoardConfig, not WhiteToMove)

		return count


start = time.perf_counter()
print(perft(3, BoardConfig, WhiteToMove))
end = time.perf_counter()
print(str((end - start) * 1000) + " ms" )

