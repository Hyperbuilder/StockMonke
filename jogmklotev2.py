import CalcLegalMoves
import engine
import Functions

BoardConfig = engine.BoardConfig

SquareFrom = Functions.SquareNumb(input("Square From:"))

print(SquareFrom)

WhiteToMove = True

CalcLegalMoves.legalKingMoves(BoardConfig, SquareFrom, WhiteToMove)