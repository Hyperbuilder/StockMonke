import CalcLegalMoves
import engine
import Functions
import time

FEN = input("FEN: ")
if FEN == "def":
        FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'

ConvertedFEN = Functions.ConvertFENString(FEN)

BoardConfig = [list(map(int, i)) for i in ConvertedFEN[0]]

WhiteToMove = ConvertedFEN[1]

KQkqCanCastle = ConvertedFEN[2]

depth = int(input("Depth: "))


#CalcLegalMoves.FinalLegalMoves(BoardConfig, WhiteToMove)




#Perft

def perft(depth, BoardConfig, WhiteToMove, KQkqCanCastle):

	legalmoves = CalcLegalMoves.FinalLegalMoves(BoardConfig, WhiteToMove, KQkqCanCastle)[0]

	Side = bool 

	if depth % 2 != 0 and depth > 0:
		Side = WhiteToMove
	elif depth % 2 == 0 and depth > 0:
		Side = not WhiteToMove
	

	if depth == 1:    
		return len(legalmoves[0])

	elif depth > 1:
		count = 0

		for move in range(len(legalmoves[0])):
			
			BoardConfigReset = [x[:] for x in BoardConfig]

			BoardConfigReset = Functions.MakeMove(legalmoves[0][move], legalmoves[1][move], BoardConfigReset, legalmoves)
			result = perft(depth - 1, BoardConfigReset, Side)
			count += result
		return count


start = time.perf_counter()
perftresult = perft(depth, BoardConfig, WhiteToMove, KQkqCanCastle)
end = time.perf_counter()
print(perftresult, str((end - start) * 1000) + " ms")
if FEN == "def": 
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

#27-1-2023 17:43 Intel Core i7-8565U: 
# Depth 1: 20			te verwaarlozen				Correct
# Depth 2: 400			te verwaarlozen				Correct
# Depth 3: 8864  		691.5813000014168 ms		38 missing, expected 8902 recieved: 8864
# Depth 4: 197217		16530.18570000131 ms		64 missing, expected 197281 recieved: 197217
# Depth 5: 4844186		371445.6950999993 ms 		21423 missing, expected 4865609 recieved: 4844186
# Depth 6: 