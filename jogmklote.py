import sys
import os
import csv

python = sys.executable

#Bord om te kijken of het stuk op het speelbord blijft, was sneller volgens gekke website
Board120xFile = list(csv.reader(open('Board120x.csv', 'r')))
Board120xList = [list(map(int, i)) for i in Board120xFile]

#Bord met offsets voor move generatie, waarom bij 21 beginnen? idk
Board64xFile = list(csv.reader(open('Board64x.csv', 'r')))
Board64xList = [list(map(int, i)) for i in Board64xFile]

#Importen van startpositie
#Eerste is Pieces, 2de is kleuren
# 0 = Empty, 1 = Pawn, 2 = Knight, 3 = Bishop, 4 = Rook, 5 = Queen, 6 = King
# 0 = Empty, 1 = White, 2 = Black
PiecesListFile = list(csv.reader(open('StartPos.csv', 'r')))
PiecesList = [list(map(int, i)) for i in PiecesListFile]

while True:

    

    #input player
    InputFrom = input("from: ")
    InputTo = input("to: ")

    #Van vakje naar de array zodat je f1 in kan voeren enzo
    def SquareNumb(Square):
        file = ord(Square[0]) - ord('a')
        rank = 8 - int(Square[1])
        return rank * 8 + file

    

    #Legal move berekenen

    #kijken of move op bord is
    #wiens beurt het is, begint natuurlijk bij wit
    side = 1

    IsSlidingPiece = [False, False, False, True, True, True, False]
    OffsetAmount = [0, 0, 8, 4, 4, 8, 8]
    OffsetValues = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [-21, -19,-12, -8, 8, 12, 19, 21], [-11, -9, 9, 11, 0, 0, 0, 0], [-10, -1, 1, 10, 0, 0, 0, 0], [-11, -10, -9, -1, 1, 9, 10, 11], [-11, -10, -9, -1, 1, 9, 10, 11]]
    
    
    
    
    #move maak klote
    def MakeMove(InputFromSquare, InputToSquare):
        From = SquareNumb(InputFromSquare)
        To = SquareNumb(InputToSquare)

        PiecesList[0][To] = PiecesList[0][From]
        PiecesList[1][To] = PiecesList[1][From]

        PiecesList[0][From] = 0
        PiecesList[1][From] = 0

    MakeMove(InputFrom, InputTo)

    #printen in consoleS
    PiecesDict = {
        #stukken
        0 : ' ',
        1 : 'P',
        2 : 'N',
        3 : 'B',
        4 : 'R', 
        5 : 'Q',
        6 : 'K',

        #kleuren
        7 : ' ',
        8 : 'W',
        9 : 'B'
    }

    for i in range(8):
        for j in range(8):
            Piece = PiecesList[0][i * 8 + j]
            Color = PiecesList[1][i * 8 + j] + 7
            
            print(PiecesDict[Piece], PiecesDict[Color], sep='', end= ' ')
            
        print()
