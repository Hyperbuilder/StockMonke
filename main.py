import pygame as pygame
import sys
import os
import csv
import math
import jogmklote

Board120xFile = list(csv.reader(open('Board120x.csv', 'r')))
Board120x = [list(map(int, i)) for i in Board120xFile]

Board64xFile = list(csv.reader(open('Board64x.csv', 'r')))
Board64x = [list(map(int, i)) for i in Board64xFile]

BoardConfigFile = list(csv.reader(open('StartPos.csv', 'r')))
BoardConfig = [list(map(int, i)) for i in BoardConfigFile]


#Standaard waarden voor venster en schaakbord
width = 1024
height = 1024
xDimension = 8
yDimension = 8
squareWidth = width / xDimension
squareHeight = height / yDimension
maxFramesPerSecond = 30

PieceDict = {
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

colorThemes = [
    [pygame.Color("white"), pygame.Color("darkgray")],
    [pygame.Color("white"), pygame.Color("purple")],
]
selectedBoardTheme = colorThemes[0]

xBoardCoordinates = ["a", "b", "c", "d", "e", "f", "g", "h"]
yBoardCoordinates = ["1", "2", "3", "4", "5", "6", "7", "8"]

#Load image with "images['piece']"
images = {}
#Functie laad images 1x in.
def imageLoader():
    pieces = ['PW', 'RW', 'NW', 'BW', 'QW', 'KW', 'PB', 'RB', 'NB', 'BB', 'QB', 'KB']
    for piece in pieces:
        images[piece] = pygame.transform.scale(pygame.image.load("images/" + piece + ".png"), (squareWidth,squareHeight))

def main():
    pygame.init()
    screen = pygame.display.set_mode((width,height));
    clock = pygame.time.Clock()
    gameRunning = True
    sysfont = pygame.font.get_default_font()
    fontSize = int(squareHeight//3)
    font = pygame.font.SysFont(sysfont, fontSize)

    imageLoader()

    SelectedSquareLocation = ''
    playerSelectedSquares = []
    pieceOnSelectedSquare = ''


    while gameRunning:

        PiecesListFile = list(csv.reader(open('StartPos.csv', 'r')))
        PiecesList = [list(map(int, i)) for i in PiecesListFile]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameRunning = False
                print("Window closed")
            elif event.type == pygame.MOUSEBUTTONDOWN:

                mouseBoardLocation = getBoardLocationCoords()
                if mouseBoardLocation == SelectedSquareLocation:
                    SelectedSquareLocation = ''
                    playerSelectedSquares = []
                    pieceOnSelectedSquare = ''
                elif len(playerSelectedSquares) == 0:
                    SelectedSquareLocation = mouseBoardLocation
                    playerSelectedSquares.append(mouseBoardLocation)
                    pieceOnSelectedSquare = getChessPieceOnLocation(PiecesList)
                elif len(playerSelectedSquares) == 1:
                    SelectedSquareLocation = ''
                    playerSelectedSquares.append(mouseBoardLocation)
                    print("moved " + pieceOnSelectedSquare + playerSelectedSquares[0] + " to " + playerSelectedSquares[1])
                    jogmklote.PlayGame(playerSelectedSquares[0], playerSelectedSquares[1])
                    playerSelectedSquares = []
                    pieceOnSelectedSquare = ''



        drawScreen(screen, font, selectedBoardTheme, PiecesList)
        clock.tick(maxFramesPerSecond)
        pygame.display.flip()

def drawScreen(screen, font, selectedBoardTheme, PiecesList):
    drawChessBoard(screen, font, selectedBoardTheme)
    drawChessPieces(screen, PiecesList)

def drawChessBoard(screen, font, BoardTheme):
    for row in range(8):
        for column in range(8):
            color = BoardTheme[((row+column) % 2)]
            pygame.draw.rect(screen, color, pygame.Rect(column*squareWidth, row*squareHeight, squareWidth, squareHeight))
            if row == 7:
                coordinateText = font.render(xBoardCoordinates[column], False, (200, 200, 200)).convert()
                #change -21 and -30 to relative to screensize values
                screen.blit(coordinateText, (column*squareWidth + squareWidth - 21, row*squareHeight + squareHeight - 30))
            elif column == 0:
                coordinateText = font.render(yBoardCoordinates[7 - row], False, (200, 200, 200))
                screen.blit(coordinateText, (column*squareWidth + 3, row*squareHeight + 3))

def drawChessPieces(screen, PiecesList):
    for row in range(yDimension):
        for column in range(xDimension):
            #CSV data omzetten naar letters
            Piece = PiecesList[0][row * 8 + column]
            Color = PiecesList[1][row * 8 + column] + 7
            #Letters mergen waardoor images[] het kan gebruiken
            piece = str(PieceDict[Piece]) + str(PieceDict[Color])
            if piece != '  ':
                screen.blit(images[piece], pygame.Rect(column*squareWidth, row*squareHeight, squareWidth, squareHeight))

def getBoardLocationCoords():
    mouseLocationCoords = pygame.mouse.get_pos()
    mouseXAxisLocation = mouseLocationCoords[0]
    mouseYAxisLocation = mouseLocationCoords[1]
    mouseBoardLocation = str(xBoardCoordinates[mouseXAxisLocation // (width//8)]) + str(yBoardCoordinates[7 - mouseYAxisLocation // (height//8)])
    return mouseBoardLocation

def SquareIndexNumber(Square):
    File = ord(Square[0]) - ord('a')
    Rank = 8 - int(Square[1])
    return Rank * 8 + File

def getChessPieceOnLocation(PiecesList):
    mouseBoardCoordinate = getBoardLocationCoords()
    x64BoardindexNumber = SquareIndexNumber(mouseBoardCoordinate)
    PieceIndexNumber = PiecesList[0][x64BoardindexNumber]
    return PieceDict[PieceIndexNumber]






if __name__ == "__main__":
    main()
    

