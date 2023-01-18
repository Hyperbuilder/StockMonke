import sys
import os
import csv
import math
import time
import CalcLegalMoves

python = sys.executable
clear = lambda: os.system('cls')

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
PiecesListFile = list(csv.reader(open('StartPos.csv', 'r')))
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

        if Side == 1:
            print("White")
        else:
            print("Black")

        print()

        #printen van bord
        for i in range(8):
            for j in range(8):
                Piece = PiecesList[0][i * 8 + j]
                Color = PiecesList[1][i * 8 + j] + 7
                
                print(PiecesDict[Piece], PiecesDict[Color], sep='', end= ' ')
                
            print()

        print()
    
        InputFrom = SquareNumb(input("From: "))

        print()


        #Pseudo legal move generenen
        LegalMoves = CalcLegalMoves.PieceSpecificMoves(InputFrom, CalcLegalMoves.CalcPseudoLegalMoves(PiecesList, Side, NotSide))
        

        #for j in range(len(LegalMoves[0])):
         #   ConvertLegalMoves = [[],[],[]]
         #   ConvertLegalMoves[0] = InvSquareNumb(int(LegalMoves[0][j]))
          #  ConvertLegalMoves[1] = InvSquareNumb(int(LegalMoves[1][j]))
          #  ConvertLegalMoves[2] = LegalMoves[2][j]
           # print(ConvertLegalMoves)


        #printen legalmoves & capture
        for i in range(len(LegalMoves[1])):
            LegalMovesPrint = LegalMoves[1]
            if LegalMoves[2][i] == False:
                PrintGrid[LegalMovesPrint[i]] = 'x'
            else:
                PrintGrid[LegalMovesPrint[i]] = 'o'
        
        print()
            
        for i in range(0, 64, 8):
            print(' '.join(PrintGrid[i:i+8]))
                
        PrintGrid = ["."] * 64
        
        print()

        SelectPiece = True
        
    ChooseMove = False
    while ChooseMove == False:
        print()

        InputTo = SquareNumb(input("to: "))

        print()

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
    print()
    clear()
    

    
 