import csv
import math
import Functions
import engine
import time

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
def CalcPseudoLegalMoves(BoardConfig, WhiteToMove):

    LegalMoves = [[],[],[]]

    Side, NotSide = Functions.WhiteToMoveTONumber(WhiteToMove)
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


def FinalLegalMoves(InputInitBoardConfig, WhiteToMove):
    start = time.perf_counter()
    InitMoveCount = 0
    ResponseMoveCount = 0

    LegalMoves = [[],[],[]]

    InitPseudoLegalMoves = CalcPseudoLegalMoves(InputInitBoardConfig, WhiteToMove)

    IllegalMoves = []
    

    # Functions.PrintChessBoard(InputInitBoardConfig)
    # Functions.PrintLegalMoveList(InitPseudoLegalMoves)

      
    for PossibleMove in range(len(InitPseudoLegalMoves[0])):
        InitBoardConfig  = [x[:] for x in InputInitBoardConfig]
        FirstItBoardConfig = Functions.MakeMove(InitPseudoLegalMoves[0][PossibleMove], InitPseudoLegalMoves[1][PossibleMove], InitBoardConfig, InitPseudoLegalMoves)[:]

        SecondItPseudoLegalMoves = CalcPseudoLegalMoves(FirstItBoardConfig, not WhiteToMove)
        Functions.PrintChessBoardLegalMovesForPiece(SecondItPseudoLegalMoves)

        for Index in range(len(SecondItPseudoLegalMoves[1])):
            if SecondItPseudoLegalMoves[2][Index] == True:
                if FirstItBoardConfig[0][SecondItPseudoLegalMoves[1][Index]] == 6:
                    print(SecondItPseudoLegalMoves[1][Index])
                    IllegalMoves.append(SecondItPseudoLegalMoves[1][Index])



        
        FirstItBoardConfig.clear()
        InitMoveCount += 1

    Functions.PrintLegalMoveList(InitPseudoLegalMoves)
    for Move in IllegalMoves:
        if Move in InitPseudoLegalMoves[1]:
            Index = InitPseudoLegalMoves[1].index(Move)
            if InputInitBoardConfig[0][InitPseudoLegalMoves[0][Index]] == 6:
                InitPseudoLegalMoves[0].pop(Index)
                InitPseudoLegalMoves[1].pop(Index)
                InitPseudoLegalMoves[2].pop(Index)
    Functions.PrintLegalMoveList(InitPseudoLegalMoves)



        
  
    

    end = time.perf_counter()
    print(IllegalMoves)
    print(str((end - start) * 1000) + " ms" )
    print("InitMoveCount", InitMoveCount)
    print("ResponseMoveCount", ResponseMoveCount)
    
    



