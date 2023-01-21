import csv
import math
import Functions

#120x board importen
Board120xFile = csv.reader(open('Board120x.csv', 'r'))
Board120x = [list(map(int, i)) for i in Board120xFile]

#64x board importen
Board64xFile = csv.reader(open('Board64x.csv', 'r'))
Board64x = [list(map(int, i)) for i in Board64xFile]

#Constants
IsSlidingPiece = [False, False, False, True, True, True, False]
OffsetDirAmount = [0, 2, 8, 4, 4, 8, 8]
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
def CalcPseudoLegalMoves(BoardConfig, whiteToMove):

    LegalMoves = [[],[],[]]

    Side, NotSide = Functions.WhiteToMoveTONumber(whiteToMove)


    for PieceIndex in range(64):
        if BoardConfig[1][PieceIndex] == Side:
                    Piece = BoardConfig[0][PieceIndex]
                    if Piece != 1:
                        for AmountOffsetDirLoop in range(OffsetDirAmount[Piece]):
                            for RayAttackLoop in range(1, 8):
                                
                                IndexNumber = Board64x[0][PieceIndex] + OffsetValues[Piece][AmountOffsetDirLoop] * RayAttackLoop

                                if IndexNumber <= 120:
                                    IndexNumber120x = Board120x[0][IndexNumber]
                                else:
                                    IndexNumber120x = -1

                                if IndexNumber120x == -1: break

                                if BoardConfig[1][IndexNumber120x] != 0:
                                    if BoardConfig[1][IndexNumber120x] == NotSide:
                                        if IndexNumber120x not in LegalMoves:
                                            LegalMoves[0].append(PieceIndex)
                                            LegalMoves[1].append(IndexNumber120x)
                                            LegalMoves[2].append(True)
                                        break
                                    else:
                                        break
                                        
                                elif BoardConfig[1][IndexNumber120x] == 0:
                                    if IndexNumber120x not in LegalMoves:
                                        LegalMoves[0].append(PieceIndex)
                                        LegalMoves[1].append(IndexNumber120x)
                                        LegalMoves[2].append(False)
                                    breakpoint
                                    
                                if IsSlidingPiece[Piece] == False: break                  
                    else:
                        #Double pawn moves
                        if Board64x[0][PieceIndex] in CheckPawnOnFirstRowW or Board64x[0][PieceIndex] in CheckPawnOnFirstRowB:
                            if BoardConfig[1][PieceIndex] == 1:
                                IndexNumber = Board64x[0][PieceIndex] - 20
                                IndexNumber120x = Board120x[0][IndexNumber]
                            elif BoardConfig[1][PieceIndex] == 2:
                                IndexNumber = Board64x[0][PieceIndex] + 20
                                IndexNumber120x = Board120x[0][IndexNumber]

                            if IndexNumber == -1: break

                            if BoardConfig[1][IndexNumber120x] == 0:
                                LegalMoves[0].append(PieceIndex)
                                LegalMoves[1].append(IndexNumber120x)
                                LegalMoves[2].append(False)
                            else: breakpoint
                        
                        #Normale pawn moves
                        if BoardConfig[1][PieceIndex] == 1:
                            IndexNumber = Board64x[0][PieceIndex] - 10
                            IndexNumber120x = Board120x[0][IndexNumber]   
                        else:
                            IndexNumber = Board64x[0][PieceIndex] + 10
                            IndexNumber120x = Board120x[0][IndexNumber]
                        
                        if BoardConfig[1][IndexNumber120x] == 0:
                            LegalMoves[0].append(PieceIndex)
                            LegalMoves[1].append(IndexNumber120x)
                            LegalMoves[2].append(False)
                        
                        else: breakpoint

                        #Pawn captures
                        for AmountOffsetDirLoop in range(OffsetDirAmount[Piece]):
                            if BoardConfig[1][PieceIndex] == 1:
                                IndexNumber = Board64x[0][PieceIndex] + OffsetValues[Piece][AmountOffsetDirLoop]
                            else:
                                IndexNumber = Board64x[0][PieceIndex] + OffsetValues[Piece][AmountOffsetDirLoop + 2]
                            if IndexNumber <= 120:
                                IndexNumber120x = Board120x[0][IndexNumber]
                            else:
                                IndexNumber120x = -1
                            if IndexNumber120x == -1: break
                            
                            if BoardConfig[1][IndexNumber120x] != 0:
                                if BoardConfig[1][IndexNumber120x] == NotSide:
                                    if IndexNumber120x not in LegalMoves:
                                        LegalMoves[0].append(PieceIndex)
                                        LegalMoves[1].append(IndexNumber120x)
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


# def legalKingMoves(BoardConfig, whiteToMove):
#     return
#     for i in range(64):
#         if i in CalcPseudoLegalMoves(BoardConfig, whiteToMove):

    
    



