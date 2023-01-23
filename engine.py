import sys
import os
import csv
import math
import time
import CalcLegalMoves
import Functions

python = sys.executable

#Bord om te kijken of het stuk op het speelbord blijft, was sneller volgens gekke website
Board120xFile = csv.reader(open('Board120x.csv', 'r'))
Board120x = [list(map(int, i)) for i in Board120xFile]

#Bord met offsets voor move generatie, waarom bij 21 beginnen? idk
Board64xFile = csv.reader(open('Board64x.csv', 'r'))
Board64x = [list(map(int, i)) for i in Board64xFile]

#Importen van startpositie
#Eerste is Pieces, 2de is kleuren
# 0 = Empty, 1 = Pawn, 2 = Knight, 3 = Bishop, 4 = Rook, 5 = Queen, 6 = King
# 0 = Empty, 1 = White, 2 = Black
BoardConfigFile = list(csv.reader(open('StartPos.csv', 'r')))
BoardConfig = [list(map(int, i)) for i in BoardConfigFile]

PieceDict = {
        #stukken
        0 : '.',
        1 : 'P',
        2 : 'N',
        3 : 'B',
        4 : 'R',
        5 : 'Q',
        6 : 'K',

        #kleuren
        7 : '.',
        8 : 'W',
        9 : 'B'
    }

def SelectPiece(SquareFrom, BoardConfig, WhiteToMove):
    LegalMovesForPiece = CalcLegalMoves.PieceSpecificMoves(SquareFrom, CalcLegalMoves.CalcPseudoLegalMoves(BoardConfig, WhiteToMove))
    print(LegalMovesForPiece)
    Functions.PrintChessBoard(BoardConfig)
    Functions.PrintChessBoardLegalMovesForPiece(LegalMovesForPiece)
    Functions.PrintLegalMoveList(LegalMovesForPiece)

    if len(LegalMovesForPiece) != 0:
        return True, LegalMovesForPiece, SquareFrom
    else:
        return False, LegalMovesForPiece, SquareFrom

def SelectMoveTo(InputFromSquare, InputToSquare, BoardConfig, LegalMoves):
    Capture = ()
    if InputToSquare in LegalMoves[1]:
        PieceIndex = LegalMoves[1].index(InputToSquare)
        BoardConfig[0][InputToSquare] = BoardConfig[0][InputFromSquare]
        BoardConfig[1][InputToSquare] = BoardConfig[1][InputFromSquare]

        BoardConfig[0][InputFromSquare] = 0
        BoardConfig[1][InputFromSquare] = 0

        if LegalMoves[2][PieceIndex] == True:
            Capture = ((BoardConfig[0][InputToSquare], BoardConfig[1][InputToSquare]))
        
        return True, Capture
    else:
        return False, Capture
