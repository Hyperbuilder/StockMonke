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
CheckPawnOnFirstRow = [81, 82, 83, 84, 85, 86, 87, 88, 31, 32, 33, 34, 35, 36, 37, 38]



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
                    else: #pawn moves
                       
                        for AmountOffsetDirLoop in range(2):
                            if BoardConfig[1][PieceIndex] == 0: break
                            if BoardConfig[1][PieceIndex] == 1:
                                IndexNumber = Board64x[0][PieceIndex] + OffsetValues[Piece][AmountOffsetDirLoop]
                            else:
                                IndexNumber = Board64x[0][PieceIndex] + OffsetValues[Piece][AmountOffsetDirLoop + 2]

                            if IndexNumber < 120:
                                IndexNumber120xCapture = Board120x[0][IndexNumber]
                            else:
                                break

                            if IndexNumber120xCapture == -1: break
                            
                            if BoardConfig[1][IndexNumber120xCapture] != 0:
                                if BoardConfig[1][IndexNumber120xCapture] == NotSide:
                                        LegalMoves[0].append(PieceIndex)
                                        LegalMoves[1].append(IndexNumber120xCapture)
                                        LegalMoves[2].append(True)    
                                        

                        if BoardConfig[1][PieceIndex] == 1:
                            IndexNumber120xSingle = Board120x[0][Board64x[0][PieceIndex] - 10]
                            IndexNumber120xDouble = Board120x[0][Board64x[0][PieceIndex] - 20]
                        else:
                            IndexNumber120xSingle = Board120x[0][Board64x[0][PieceIndex] + 10]
                            IndexNumber120xDouble = Board120x[0][Board64x[0][PieceIndex] + 20]

                        if IndexNumber120xDouble == -1 or IndexNumber120xSingle == -1: break

                        if BoardConfig[1][IndexNumber120xSingle] == 0 and BoardConfig[1][IndexNumber120xDouble] == 0 and Board64x[0][PieceIndex] in CheckPawnOnFirstRow:
                            LegalMoves[0].append(PieceIndex)
                            LegalMoves[1].append(IndexNumber120xDouble)
                            LegalMoves[2].append(False)
                        
                        if BoardConfig[1][IndexNumber120xSingle] == 0: 
                            LegalMoves[0].append(PieceIndex)
                            LegalMoves[1].append(IndexNumber120xSingle)
                            LegalMoves[2].append(False)
                        else: breakpoint


                        
                        
    return LegalMoves



def PieceSpecificMoves(SelectedPiece, LegalMoves):
    PieceSpecificLegalMoves = [[], [], []]
    for selectedPieceIndexPos, selectedPiece in enumerate(LegalMoves[0]):
        if (selectedPiece == SelectedPiece):
            PieceSpecificLegalMoves[0].append(LegalMoves[0][selectedPieceIndexPos])
            PieceSpecificLegalMoves[1].append(LegalMoves[1][selectedPieceIndexPos])
            PieceSpecificLegalMoves[2].append(LegalMoves[2][selectedPieceIndexPos])
    return PieceSpecificLegalMoves


def FinalLegalMoves(InputInitBoardConfig, WhiteToMove, KQkqCanCastle):
    #start = time.perf_counter()
    LegalMoves = InitPseudoLegalMoves = CalcPseudoLegalMoves(InputInitBoardConfig, WhiteToMove)

    IllegalMoves = []

    KQkqCanCastle
    

    # Functions.PrintChessBoard(InputInitBoardConfig)
    # Functions.PrintLegalMoveList(InitPseudoLegalMoves)

      
    for PossibleMove in range(len(InitPseudoLegalMoves[0])):
        InitBoardConfig  = [x[:] for x in InputInitBoardConfig]
        FirstItBoardConfig = Functions.MakeMove(InitPseudoLegalMoves[0][PossibleMove], InitPseudoLegalMoves[1][PossibleMove], InitBoardConfig, InitPseudoLegalMoves)[:]
        
        SecondItPseudoLegalMoves = CalcPseudoLegalMoves(FirstItBoardConfig, not WhiteToMove)
        #Functions.PrintChessBoardLegalMovesForPiece(SecondItPseudoLegalMoves)
        #Functions.PrintLegalMoveList(SecondItPseudoLegalMoves)
        #Functions.PrintChessBoard(FirstItBoardConfig)
    
        
        for Index in range(len(SecondItPseudoLegalMoves[1])):
            if SecondItPseudoLegalMoves[2][Index] == True:
                if FirstItBoardConfig[0][SecondItPseudoLegalMoves[1][Index]] == 6:
                    if PossibleMove not in IllegalMoves:
                        IllegalMoves.append(PossibleMove)
                    
                    
        FirstItBoardConfig.clear()
        

  
    #Functions.PrintLegalMoveList(InitPseudoLegalMoves)
    #print(IllegalMoves)

    for RemoveMove in reversed(range(len(IllegalMoves))):
        LegalMoves[0].pop(IllegalMoves[RemoveMove])
        LegalMoves[1].pop(IllegalMoves[RemoveMove])
        LegalMoves[2].pop(IllegalMoves[RemoveMove])
    

    #Functions.PrintLegalMoveList(LegalMoves)
    #end = time.perf_counter()
    #print(LegalMoves)
    #Functions.PrintLegalMoveList(LegalMoves)
    #Functions.PrintChessBoard(InputInitBoardConfig)
    #print(str((end - start) * 1000) + " ms" )
    #print("InitMoveCount", InitMoveCount)
    #print("ResponseMoveCount", ResponseMoveCount)

    AmountOfMoves = len(LegalMoves[0])

    isCheckmate = False
    #print(len(LegalMoves[0]))
    if len(LegalMoves[0]) == 0:
        isCheckmate = True
        #print(isCheckmate)
  
    return LegalMoves, isCheckmate, AmountOfMoves
  
    
    



