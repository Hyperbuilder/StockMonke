import sys
import os
import csv
import math
import time

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
PiecesListFile = list(csv.reader(open('Test Bord.csv', 'r')))
PiecesList = [list(map(int, i)) for i in PiecesListFile]

#Van bordcoordinaat naar x64index int
def SquareNumb(Square):
    File = ord(Square[0]) - ord('a')
    Rank = 8 - int(Square[1])
    return Rank * 8 + File

#Van x64index int naar bordcoordinaat
def InvSquareNumb(Square):
    FileNum= Square % 8
    RankNum = 8 - math.floor(Square / 8)
    File = chr((ord('a') + FileNum))
    Rank = str(RankNum)
    return File + Rank


def MakeMove(InputFromSquare, InputToSquare):
    From = InputFromSquare
    To = InputToSquare

    PiecesList[0][To] = PiecesList[0][From]
    PiecesList[1][To] = PiecesList[1][From]

    PiecesList[0][From] = 0
    PiecesList[1][From] = 0

IsSlidingPiece = [False, False, False, True, True, True, False]
OffsetAmount = [0, 0, 8, 4, 4, 8, 8]
OffsetValues = [
    [0, 0, 0, 0, 0, 0, 0, 0],           #Empty
    [0, 0, 0, 0, 0, 0, 0, 0],           #Pawwn
    [-21, -19,-12, -8, 8, 12, 19, 21],  #Pferd
    [-11, -9, 9, 11, 0, 0, 0, 0],       #Bishop
    [-10, -1, 1, 10, 0, 0, 0, 0],       #Rook
    [-11, -10, -9, -1, 1, 9, 10, 11],   #Queen
    [-11, -10, -9, -1, 1, 9, 10, 11]]   #King

PiecesDict = {
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

#Wiens beurt
Side = 1
NotSide = 2

while True:
    StartTime = time.process_time()


    PrintGrid = ["."] * 64

    SelectPiece = False
    while SelectPiece == False:     

        LegalMoves = [[],[],[]]

        print(Side)

        #printen van bord
        for i in range(8):
            for j in range(8):
                Piece = PiecesList[0][i * 8 + j]
                Color = PiecesList[1][i * 8 + j] + 7
                
                print(PiecesDict[Piece], PiecesDict[Color], sep='', end= ' ')
                
            print()

        print('\n')
    
        InputFrom = SquareNumb(input("From: "))

        #Pseudo legal move generenen
        if PiecesList[1][InputFrom] == Side:
            Piece = PiecesList[0][InputFrom]
            if Piece != 1:
                for j in range(OffsetAmount[Piece]):
                    for m in range(1, 8):
                        
                        IndexNumber = Board64x[0][InputFrom] + OffsetValues[Piece][j] * m

                        if IndexNumber <= 120:
                            n = Board120x[0][IndexNumber]
                        else:
                            n = -1

                        if n == -1: break

                        if PiecesList[1][n] != 0:
                            if PiecesList[1][n] == NotSide:
                                if n not in LegalMoves:
                                    LegalMoves[0].append(i)
                                    LegalMoves[1].append(n)
                                    LegalMoves[2].append(True)
                                break
                                
                        elif PiecesList[1][n] == 0:
                            if n not in LegalMoves:
                                LegalMoves[0].append(i)
                                LegalMoves[1].append(n)
                                LegalMoves[2].append(False)
                            breakpoint
                            
                        if IsSlidingPiece[Piece] == False: break                  
            else:
                None #pawn moves

        for j in range(len(LegalMoves[0])):
            ConvertLegalMoves = [[],[],[]]
            ConvertLegalMoves[0] = InvSquareNumb(int(LegalMoves[0][j]))
            ConvertLegalMoves[1] = InvSquareNumb(int(LegalMoves[1][j]))
            ConvertLegalMoves[2] = LegalMoves[2][j]
            print(ConvertLegalMoves)


        #printen legalmoves & capture
        for i in range(len(LegalMoves[1])):
            LegalMovesPrint = LegalMoves[1]
            if LegalMoves[2][i] == False:
                PrintGrid[LegalMovesPrint[i]] = 'x'
            else:
                PrintGrid[LegalMovesPrint[i]] = 'o'
            
            
        for i in range(0, 64, 8):
            print(' '.join(PrintGrid[i:i+8]))
                
        PrintGrid = ["."] * 64
        
        InputContinue = input("Move this piece? Y/N ")
        if InputContinue.lower() == 'y':
            SelectPiece = True
        else:
            SelectPiece = False
            LegalMoves[0].clear()
            LegalMoves[1].clear()
            LegalMoves[2].clear()
            
    ChooseMove = False
    while ChooseMove == False:

        InputTo = SquareNumb(input("to: "))

        if InputTo in LegalMoves[1]:
            MakeMove(InputFrom, InputTo)
            ChooseMove = True
        else:
            ChooseMove = False 
            print('\n', "u stupid thats big nono", '\n')

    StoreSide = Side
    Side = NotSide 
    NotSide = StoreSide    

    EndTime = time.process_time()
    print("Process time: ", EndTime - StartTime)

    
