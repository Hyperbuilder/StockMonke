import csv
import math

#120x board importen
Board120xFile = csv.reader(open('Board120x.csv', 'r'))
Board120x = [list(map(int, i)) for i in Board120xFile]

#64x board importen
Board64xFile = csv.reader(open('Board64x.csv', 'r'))
Board64x = [list(map(int, i)) for i in Board64xFile]

PiecesListFile = list(csv.reader(open('StartPos.csv', 'r')))
PiecesList = [list(map(int, i)) for i in PiecesListFile]

#Constants
IsSlidingPiece = [False, False, False, True, True, True, False]
OffsetAmount = [0, 2, 8, 4, 4, 8, 8]
OffsetValues = [
    [0, 0, 0, 0, 0, 0, 0, 0],           #Empty
    [-11, -9, 9, 11, 0, 0, 0, 0],        #Pawn
    [-21, -19,-12, -8, 8, 12, 19, 21],  #Pferd
    [-11, -9, 9, 11, 0, 0, 0, 0],       #Bishop
    [-10, -1, 1, 10, 0, 0, 0, 0],       #Rook
    [-11, -10, -9, -1, 1, 9, 10, 11],   #Queen
    [-11, -10, -9, -1, 1, 9, 10, 11]]   #King

#kijken of pawn zich op eerste rij bevindt, zo ja double push mogelijk
CheckPawnOnFirstRowW = [81, 82, 83, 84, 85, 86, 87, 88]
CheckPawnOnFirstRowB = [31, 32, 33, 34, 35, 36, 37, 38]

#Calc pseudo legal moves (alle moves zonder dat er met schaak, en passant of rokeren te maken heeft), moves voor specific pieces komt in andere functie
def CalcPseudoLegalMoves(BoardConfig, Side, NotSide):
    LegalMoves = [[],[],[]]
    for i in range(64):
        if BoardConfig[1][i] == Side:
                    Piece = BoardConfig[0][i]
                    if Piece != 1:
                        for j in range(OffsetAmount[Piece]):
                            for m in range(1, 8):
                                
                                IndexNumber = Board64x[0][i] + OffsetValues[Piece][j] * m

                                if IndexNumber <= 120:
                                    n = Board120x[0][IndexNumber]
                                else:
                                    n = -1

                                if n == -1: break

                                if BoardConfig[1][n] != 0:
                                    if BoardConfig[1][n] == NotSide:
                                        if n not in LegalMoves:
                                            LegalMoves[0].append(i)
                                            LegalMoves[1].append(n)
                                            LegalMoves[2].append(True)
                                        break
                                    else:
                                        break
                                        
                                elif BoardConfig[1][n] == 0:
                                    if n not in LegalMoves:
                                        LegalMoves[0].append(i)
                                        LegalMoves[1].append(n)
                                        LegalMoves[2].append(False)
                                    breakpoint
                                    
                                if IsSlidingPiece[Piece] == False: break                  
                    else:
                        #Double pawn moves
                        if Board64x[0][i] in CheckPawnOnFirstRowW or Board64x[0][i] in CheckPawnOnFirstRowB:
                            if BoardConfig[1][i] == 1:
                                IndexNumber = Board64x[0][i] - 20
                                n = Board120x[0][IndexNumber]
                            elif BoardConfig[1][i] == 2:
                                IndexNumber = Board64x[0][i] + 20
                                n = Board120x[0][IndexNumber]

                            if IndexNumber == -1: break

                            if BoardConfig[1][n] == 0:
                                LegalMoves[0].append(i)
                                LegalMoves[1].append(n)
                                LegalMoves[2].append(False)
                            else: breakpoint
                        
                        #Normale pawn moves
                        if BoardConfig[1][i] == 1:
                            IndexNumber = Board64x[0][i] - 10
                            n = Board120x[0][IndexNumber]   
                        else:
                            IndexNumber = Board64x[0][i] + 10
                            n = Board120x[0][IndexNumber]
                        
                        if BoardConfig[1][n] == 0:
                            LegalMoves[0].append(i)
                            LegalMoves[1].append(n)
                            LegalMoves[2].append(False)
                        
                        else: breakpoint

                        #Pawn captures
                        for j in range(OffsetAmount[Piece]):
                            if BoardConfig[1][i] == 1:
                                IndexNumber = Board64x[0][i] + OffsetValues[Piece][j]
                            else:
                                IndexNumber = Board64x[0][i] + OffsetValues[Piece][j + 2]
                            if IndexNumber <= 120:
                                n = Board120x[0][IndexNumber]
                            else:
                                n = -1
                            if n == -1: break
                            
                            if BoardConfig[1][n] != 0:
                                if BoardConfig[1][n] == NotSide:
                                    if n not in LegalMoves:
                                        LegalMoves[0].append(i)
                                        LegalMoves[1].append(n)
                                        LegalMoves[2].append(True)            
    return LegalMoves



def PieceSpecificMoves(SelectedPiece, LegalMoves):
    PieceSpecificLegalMoves = [[], [], []]
    for selectedPieceIndexPos, selectedPiece in enumerate(LegalMoves[0]):
        if (selectedPiece == SelectedPiece):
            PieceSpecificLegalMoves[0].append(LegalMoves[0][selectedPieceIndexPos])
            PieceSpecificLegalMoves[1].append(LegalMoves[1][selectedPieceIndexPos])
            PieceSpecificLegalMoves[2].append(LegalMoves[2][selectedPieceIndexPos])
    return PieceSpecificLegalMoves


def isPlayerInCheck():
    pass



