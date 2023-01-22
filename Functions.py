import math
import pygame

def ConvertFENString(FEN):
    
    Board = [[],[]]
    for row in FEN.split('/'):
        for c in row:
            FENDict = {
                'n' : '2',
                'b' : '3',
                'r' : '4',
                'q' : '5',
                'k' : '6'
            }

            if c == ' ':
                break
            elif c in '12345678':
                Board[0].append(['0'] * int(c))
                Board[1].append(['0'] * int(c))
            elif c == 'p':
                Board[0].append('1')
                Board[1].append('2')
            elif c == 'P':
                Board[0].append('1')
                Board[1].append('1')
            elif c > 'Z':
                Board[0].append(FENDict[c])
                Board[1].append('2')
            else:
                Board[0].append(FENDict[c.lower()])
                Board[1].append('1')

    FinalBoard = [[],[]]
    FinalBoard[0] = [i for j in Board[0] for i in j]
    FinalBoard[1] = [i for j in Board[1] for i in j]
    
    WhiteToMove = True
    for Turn in FEN.split(' '):
        if Turn.lower() == 'w':
            WhiteToMove = True
        elif Turn.lower() == 'b':
            WhiteToMove = False
    
    return FinalBoard, WhiteToMove



def SquareNumb(Square):
    File = ord(Square[0]) - ord('a')
    Rank = 8 - int(Square[1])
    return Rank * 8 + File


def InvSquareNumb(Square):
    FileNum= Square % 8
    RankNum = 8 - math.floor(Square / 8)
    File = chr((ord('a') + FileNum))
    Rank = str(RankNum)
    return File + Rank

       



#functies voor debuggen zoals printen'
def PrintChessBoard(BoardConfig, PieceDict):
    for i in range(8):
        for j in range(8):
            Piece = BoardConfig[0][i * 8 + j]
            Color = BoardConfig[1][i * 8 + j] + 7

            print(PieceDict[Piece], PieceDict[Color], sep='', end= ' ')

        print()

def PrintChessBoardLegalMovesForPiece(LegalMoves):
    PrintGrid = ["."] * 64
    for i in range(len(LegalMoves[1])):
            LegalMovesPrint = LegalMoves[1]
            if LegalMoves[2][i] == False:
                PrintGrid[LegalMovesPrint[i]] = 'x'
            else:
                PrintGrid[LegalMovesPrint[i]] = 'o'

    for i in range(0, 64, 8):
            print(' '.join(PrintGrid[i:i+8]))

    PrintGrid = ["."] * 64


def PrintLegalMoveList(LegalMoves):
    for j in range(len(LegalMoves[0])):
        ConvertLegalMoves = [[],[],[]]
        ConvertLegalMoves[0] = InvSquareNumb(int(LegalMoves[0][j]))
        ConvertLegalMoves[1] = InvSquareNumb(int(LegalMoves[1][j]))
        ConvertLegalMoves[2] = LegalMoves[2][j]
        print(ConvertLegalMoves)

def WhiteToMoveTONumber(whiteToMove):
    if whiteToMove:
        Side = 1
        NotSide = 2
    else: 
        Side = 2
        NotSide = 1
    return Side, NotSide

def imageLoader(squareWidth, squareHeight):
    images = {}
    pieces = ['PW', 'RW', 'NW', 'BW', 'QW', 'KW', 'PB', 'RB', 'NB', 'BB', 'QB', 'KB']
    for piece in pieces:
        images[piece] = pygame.transform.scale(pygame.image.load("images/" + piece + ".png"), (squareWidth, squareHeight))
    return images

def getChessPieceOnLocation(BoardConfig, PieceDict, mouseBoardCoordinate):
    x64BoardindexNumber = SquareNumb(mouseBoardCoordinate)
    PieceIndexNumber = BoardConfig[0][x64BoardindexNumber]
    return PieceDict[PieceIndexNumber]

def getBoardLocationCoords(xBoardCoordinates, yBoardCoordinates, width, height):
    mouseLocationCoords = pygame.mouse.get_pos()
    mouseXAxisLocation = mouseLocationCoords[0]
    mouseYAxisLocation = mouseLocationCoords[1]
    mouseBoardLocation = str(xBoardCoordinates[mouseXAxisLocation // (width//8)]) + str(yBoardCoordinates[7 - mouseYAxisLocation // (height//8)])
    return mouseBoardLocation
