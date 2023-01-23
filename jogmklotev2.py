import CalcLegalMoves
import engine
import Functions

FEN = input("FEN: ")
if FEN == "def":
        FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'

BoardConfig = [list(map(int, i)) for i in Functions.ConvertFENString(FEN)[0]]

WhiteToMove = Functions.ConvertFENString(FEN)[1]


CalcLegalMoves.FinalLegalMoves(BoardConfig, WhiteToMove)
