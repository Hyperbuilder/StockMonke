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

def PlayGame(InputFrom, InputTo):
#kant die aan de beurt is toevoegen
    #FEN = input("Insert FEN: ")

    #if FEN == "def":
    #    FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'

    #BoardConfig = [list(map(int, i)) for i in Functions.ConvertFENString(FEN)[0]]




    #Wiens beurt
    whiteToMove = True #Functions.ConvertFENString(FEN)[1]
    whiteKingSquare = 60
    blackKingSquare = 5
    CapturedPieces = []

    while True:
        StartTime = time.process_time()


        #Selec
    #while SelectPiece == False:

        LegalMoves = [[],[],[]]

        if whiteToMove:
            print("White")
        else:
            print("Black")

        #printen van bord
        Functions.PrintChessBoard(BoardConfig, PieceDict)
        

        #Legal moves voor geselecteerde schaakstuk
        LegalMoves = CalcLegalMoves.PieceSpecificMoves(InputFrom, CalcLegalMoves.CalcPseudoLegalMoves(BoardConfig, whiteToMove))
    

        Functions.PrintLegalMoveList(LegalMoves)

        #printen legalmoves & capture
        Functions.PrintChessBoardCaptures(LegalMoves)
        
        print()
        
        time.sleep(5)

        #Stop Whileloop
        #SelectPiece = True
        #End of While Loop


        #ChooseMove = False
        #while ChooseMove == False:

        ChooseMove = Functions.MakeMove(InputFrom, InputTo, BoardConfig, LegalMoves)
        if ChooseMove[1] != ():
            CapturedPieces.append(ChooseMove[1])
        print(CapturedPieces)
    
        if not ChooseMove[0]:
            print("EY DUMDUM kan toch niet he moettie briltje ha?")
        #End of While Loop

        whiteToMove = not whiteToMove

        EndTime = time.process_time()
        print("Process time: ", EndTime - StartTime)
        #End of While Loop


