import pygame as pygame
import sys
import os
import csv
import math
import engine
import Functions


FEN = input("Insert FEN: ")

if FEN == "def":
        FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq'

BoardConfig = [list(map(int, i)) for i in Functions.ConvertFENString(FEN)[0]]

WhiteToMove = Functions.ConvertFENString(FEN)[1]

KQkqcanCastle = [True, True, True, True]

#Standaard waarden voor venster en schaakbord
width = 512 *2
height = 512 *2
xDimension = 8
yDimension = 8
squareWidth = width / xDimension
squareHeight = height / yDimension
maxFramesPerSecond = 60

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

images = {}

def main():
    pygame.init()
    screen = pygame.display.set_mode((width,height));
    clock = pygame.time.Clock()
    gameRunning = True
    sysfont = pygame.font.get_default_font()
    fontSize = int(squareHeight//3)
    font = pygame.font.SysFont(sysfont, fontSize)

    images = Functions.imageLoader(squareWidth, squareHeight)
    HasSelectedPiece = [False, None, None]
    WhiteToMove = True
    CapturedPieces = []

    while gameRunning:
        Side, notSide = Functions.WhiteToMoveTONumber(WhiteToMove)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameRunning = False
                print("Window closed")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouseBoardLocation = Functions.SquareNumb(Functions.getBoardLocationCoords(xBoardCoordinates, yBoardCoordinates, width, height))
                
                if HasSelectedPiece == [False, None, None]:
                    if BoardConfig[0][mouseBoardLocation] != 0:
                        if BoardConfig[1][mouseBoardLocation] == Side:
                            HasSelectedPiece = engine.SelectPiece(mouseBoardLocation, BoardConfig, WhiteToMove)
                            if HasSelectedPiece[1] == None:
                                gameRunning = False
                                break
                elif mouseBoardLocation == HasSelectedPiece[2]:
                    HasSelectedPiece = [False, None, None]
                elif HasSelectedPiece[0] == True and mouseBoardLocation != HasSelectedPiece[2]:
                    moveresult = engine.SelectMoveTo(HasSelectedPiece[2], mouseBoardLocation, BoardConfig, HasSelectedPiece[1])
                    if moveresult[0] == True:
                        CapturedPieces.append(moveresult[1])
                        WhiteToMove = not WhiteToMove
                        #print(CapturedPieces)
                        HasSelectedPiece = [False, None, None]
                    else: 
                        print("not a possible move")

        drawScreen(screen, font, selectedBoardTheme, BoardConfig, images, HasSelectedPiece)

        clock.tick(maxFramesPerSecond)
        pygame.display.flip()




def drawScreen(screen, font, selectedBoardTheme, BoardConfig, images, HasSelectedPiece):
    drawChessBoard(screen, font, selectedBoardTheme)
    drawChessPieces(screen, BoardConfig, images)
    if HasSelectedPiece[0] == True:
        drawHighlight(screen, HasSelectedPiece)


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

def drawChessPieces(screen, BoardConfig, images):
    for row in range(yDimension):
        for column in range(xDimension):
            #CSV data omzetten naar letters
            Piece = BoardConfig[0][row * 8 + column]
            Color = BoardConfig[1][row * 8 + column] + 7
            #Letters mergen waardoor images[] het kan gebruiken
            piece = str(PieceDict[Piece]) + str(PieceDict[Color])
            if piece != '  ':
                screen.blit(images[piece], pygame.Rect(column*squareWidth, row*squareHeight, squareWidth, squareHeight))

def drawHighlight(screen, HasSelectedPiece):
    for i in range(len(HasSelectedPiece[1][1])):
        row, column = Functions.brdnumtorowcol(HasSelectedPiece[1][1][i])
        pygame.draw.circle(screen, (109, 113, 46), (row*squareHeight + squareHeight / 2, column*squareWidth + squareWidth / 2), squareWidth // 8)
    Sqrow, Sqcolumn = Functions.brdnumtorowcol(HasSelectedPiece[2])
    pygame.draw.circle(screen, (200, 70, 46), (Sqrow*squareHeight + squareHeight / 2, Sqcolumn*squareWidth + squareWidth / 2), squareWidth // 2, 5)


if __name__ == "__main__":
    main()
    

