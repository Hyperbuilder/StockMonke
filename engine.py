import sys
import csv
import Functions

python = sys.executable


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
CheckPawnPromotion = [0, 1, 2, 3, 4, 5, 6, 7, 56, 57, 58, 59, 60, 61, 62, 63]
CheckWhiteCastleSquares = [57, 58, 59, 61, 62]
CheckBlackCastleSquares = [1, 2, 3, 5, 6]

EnPassantTotal = []
EnPassantStored = []

#Calc pseudo legal moves (alle moves zonder dat er met schaak, en passant of rokeren te maken heeft), moves voor specific pieces komt in andere functie
def CalcPseudoLegalMoves(BoardConfig, WhiteToMove, KQkqCanCastle):


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

                                if Piece == 6:
                                    if Side == 1:
                                        if KQkqCanCastle[0] == True:
                                            if BoardConfig[1][5] == 0 and BoardConfig[1][6] == 0:
                                                print("K Castle")
                                                LegalMoves[0].append(PieceIndex)
                                                LegalMoves[1].append(5)
                                                LegalMoves[2].append(False)    
                                        if KQkqCanCastle[1] == True:
                                            
                                            if BoardConfig[1][1] == 0 and BoardConfig[1][2] == 0 and BoardConfig[1][3] == 0:
                                                print("Q Castle")
                                                LegalMoves[0].append(PieceIndex)
                                                LegalMoves[1].append(2)
                                                LegalMoves[2].append(False)       
                                    elif Side == 2:
                                        if KQkqCanCastle[2] == True:
                                            if BoardConfig[1][61] == 0 and BoardConfig[1][62] == 0:
                                                print("K Castle")
                                                LegalMoves[0].append(PieceIndex)
                                                LegalMoves[1].append(62)
                                                LegalMoves[2].append(False)    
                                        if KQkqCanCastle[3] == True:
                                            if BoardConfig[1][57] == 0 and BoardConfig[1][58] == 0 and BoardConfig[1][59] == 0:
                                                print("Q Castle")
                                                LegalMoves[0].append(PieceIndex)
                                                LegalMoves[1].append(58)
                                                LegalMoves[2].append(False)

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
                        
                        #passanten terrein
                        if len(EnPassantStored) == 1 and (PieceIndex + 1 == EnPassantStored[0] or PieceIndex -1 == EnPassantStored[0]):
                            print(PieceIndex)
                            if Side == 1:
                                print(EnPassantStored, "w", Board120x[0][Board64x[0][PieceIndex]])
                                
                                IndexNumber120xEnPassant = EnPassantStored[0] - 8
                                
                            else:
                                print(EnPassantStored, "b", PieceIndex)
                               
                                IndexNumber120xEnPassant = EnPassantStored[0] + 8
                                
                            LegalMoves[0].append(PieceIndex)
                            LegalMoves[1].append(IndexNumber120xEnPassant)
                            LegalMoves[2].append(True)
                            EnPassantStored.clear()
                            
                        


                        if BoardConfig[1][PieceIndex] == 1:
                            IndexNumber120xSingle = Board120x[0][Board64x[0][PieceIndex] - 10]
                            IndexNumber120xDouble = Board120x[0][Board64x[0][PieceIndex] - 20]
                        else:
                            IndexNumber120xSingle = Board120x[0][Board64x[0][PieceIndex] + 10]
                            IndexNumber120xDouble = Board120x[0][Board64x[0][PieceIndex] + 20]

                        if IndexNumber120xDouble == -1 and IndexNumber120xSingle == -1: break

                        if BoardConfig[1][IndexNumber120xSingle] == 0 and BoardConfig[1][IndexNumber120xDouble] == 0 and Board64x[0][PieceIndex] in CheckPawnOnFirstRow and IndexNumber120xDouble != -1:
                            LegalMoves[0].append(PieceIndex)
                            LegalMoves[1].append(IndexNumber120xDouble)
                            LegalMoves[2].append(False)
                            if IndexNumber120xDouble not in EnPassantTotal:
                                EnPassantTotal.append(IndexNumber120xDouble)
                        
                        if BoardConfig[1][IndexNumber120xSingle] == 0 and IndexNumber120xSingle != -1: 
                            LegalMoves[0].append(PieceIndex)
                            LegalMoves[1].append(IndexNumber120xSingle)
                            LegalMoves[2].append(False)
         
    return LegalMoves



def PieceSpecificMoves(SelectedPiece, LegalMoves):
    PieceSpecificLegalMoves = [[], [], []]
    for selectedPieceIndexPos, selectedPiece in enumerate(LegalMoves[0]):
        if (selectedPiece == SelectedPiece):
            PieceSpecificLegalMoves[0].append(LegalMoves[0][selectedPieceIndexPos])
            PieceSpecificLegalMoves[1].append(LegalMoves[1][selectedPieceIndexPos])
            PieceSpecificLegalMoves[2].append(LegalMoves[2][selectedPieceIndexPos])
    return PieceSpecificLegalMoves


def CalcFinalLegalMoves(InputInitBoardConfig, WhiteToMove, KQkqCanCastle):
    LegalMoves = InitPseudoLegalMoves = CalcPseudoLegalMoves(InputInitBoardConfig, WhiteToMove, KQkqCanCastle)
    IllegalMoves = []


    # if WhiteToMove == True:
    #     KingSideCastle = KQkqCanCastle[0]
    #     QueenSideCastle = KQkqCanCastle[1]
    # else:
    #     KingSideCastle = KQkqCanCastle[2]
    #     QueenSideCastle = KQkqCanCastle[3]

    
      
    for PossibleMove in range(len(InitPseudoLegalMoves[0])):
        InitBoardConfig  = [x[:] for x in InputInitBoardConfig]
        FirstItBoardConfig = MakeMoveCalculations(InitPseudoLegalMoves[0][PossibleMove], InitPseudoLegalMoves[1][PossibleMove], InitBoardConfig, InitPseudoLegalMoves)[:]
        
        SecondItPseudoLegalMoves = CalcPseudoLegalMoves(FirstItBoardConfig, not WhiteToMove, KQkqCanCastle)
        
        for Index in range(len(SecondItPseudoLegalMoves[1])):
            if SecondItPseudoLegalMoves[2][Index] == True:
                if FirstItBoardConfig[0][SecondItPseudoLegalMoves[1][Index]] == 6:
                    if PossibleMove not in IllegalMoves:
                        IllegalMoves.append(PossibleMove)
                    
                    
        FirstItBoardConfig.clear()
        
    for RemoveMove in reversed(range(len(IllegalMoves))):
        LegalMoves[0].pop(IllegalMoves[RemoveMove])
        LegalMoves[1].pop(IllegalMoves[RemoveMove])
        LegalMoves[2].pop(IllegalMoves[RemoveMove])
    
    AmountOfMoves = len(LegalMoves[0])

    isCheckmate = False

    if len(LegalMoves[0]) == 0:
        isCheckmate = True
        print(LegalMoves)

    return LegalMoves, isCheckmate, AmountOfMoves
  

def SelectPiece(SquareFrom, BoardConfig, WhiteToMove, KQkqCanCastle):
    FinalLegalMoves = CalcFinalLegalMoves(BoardConfig, WhiteToMove, KQkqCanCastle)


    if FinalLegalMoves[1] == True:
        print('Game Over')
        return False, None, None
    else:
        LegalMovesForPiece = PieceSpecificMoves(SquareFrom, FinalLegalMoves[0])
        return True, LegalMovesForPiece, SquareFrom



def SelectMoveTo(InputFromSquare, InputToSquare, BoardConfig, LegalMoves):
    Capture = ()
    if InputToSquare in LegalMoves[1]:
        
        PieceIndex = LegalMoves[1].index(InputToSquare)

        #Promotion system
        if BoardConfig[0][InputFromSquare] == 1 and InputToSquare in CheckPawnPromotion:
            PromoteToPiece = input("Promote to (NBRQ): ")
            if PromoteToPiece.lower() == 'n':
                BoardConfig[0][InputToSquare] = 2
                BoardConfig[1][InputToSquare] = BoardConfig[1][InputFromSquare]
            elif PromoteToPiece.lower() == 'b':
                BoardConfig[0][InputToSquare] = 3
                BoardConfig[1][InputToSquare] = BoardConfig[1][InputFromSquare]
            elif PromoteToPiece.lower() == 'r':
                BoardConfig[0][InputToSquare] = 4
                BoardConfig[1][InputToSquare] = BoardConfig[1][InputFromSquare]
            elif PromoteToPiece.lower() == 'q':
                BoardConfig[0][InputToSquare] = 5
                BoardConfig[1][InputToSquare] = BoardConfig[1][InputFromSquare]
        else: 
            BoardConfig[0][InputToSquare] = BoardConfig[0][InputFromSquare]
            BoardConfig[1][InputToSquare] = BoardConfig[1][InputFromSquare]

        #Reset Square piece came from
        BoardConfig[0][InputFromSquare] = 0
        BoardConfig[1][InputFromSquare] = 0

        #logic voor enpassant
        if InputToSquare in EnPassantTotal:
            
            EnPassantStored.append(InputToSquare)
        EnPassantTotal.clear()
            
        if LegalMoves[2][PieceIndex] == True:
            Capture = ((BoardConfig[0][InputToSquare], BoardConfig[1][InputToSquare]))

        return True, Capture
    else:
        return False, Capture

#zelfde functie maar dan voor berekenen bij perft of checks

def MakeMoveCalculations(InputFromSquare, InputToSquare, InitBoardConfig, LegalMoves):
    BoardConfig = InitBoardConfig[:]
    if InputToSquare in LegalMoves[1]:
        BoardConfig[0][InputToSquare] = BoardConfig[0][InputFromSquare]
        BoardConfig[1][InputToSquare] = BoardConfig[1][InputFromSquare]

        BoardConfig[0][InputFromSquare] = 0
        BoardConfig[1][InputFromSquare] = 0
    
    return list(BoardConfig)
  

