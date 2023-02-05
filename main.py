import pygame as pygame
import engine
import Functions

# Invullen van FEN string
FEN = input("Insert FEN (Type: (def) for standard position; Type: (PERFT) for PERFT Debug): ")

if FEN == "def":
        FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq'
# elif FEN == "cas":
#     FEN = "rnbqk1nr/ppp2ppp/3p4/4p3/1bB1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 0 0"
elif FEN == "PERFT":
    exec(open("PERFT.py").read())


BoardConfig = [list(map(int, i)) for i in Functions.ConvertFENString(FEN)[0]]
KQkqcanCastle = Functions.ConvertFENString(FEN)[2]

# Standaard waarden voor venster en schaakbord
width = 512 * 2
height = 512 * 2
xDimension = 8
yDimension = 8
squareWidth = width / xDimension
squareHeight = height / yDimension
maxFramesPerSecond = 15

#Dict voor Piece Name naar int
PieceDict = {
    # Stukken
    0 : ' ',
    1 : 'P',
    2 : 'N',
    3 : 'B',
    4 : 'R', 
    5 : 'Q',
    6 : 'K',

    # Kleuren
    7 : ' ',
    8 : 'W',
    9 : 'B'
}

# Colorthemes (Not in use!)
colorThemes = [
    [pygame.Color("white"), pygame.Color("darkgray")],
    [pygame.Color("white"), pygame.Color("purple")],
]

selectedBoardTheme = colorThemes[0]

xBoardCoordinates = ["a", "b", "c", "d", "e", "f", "g", "h"]
yBoardCoordinates = ["1", "2", "3", "4", "5", "6", "7", "8"]

# Load all images into this dict to store them in cache to reduce rendertime.
images = {}

def main():
    # initiate Pygame
    pygame.init()
    screen = pygame.display.set_mode((width,height));
    clock = pygame.time.Clock()

    gameRunning = True

    # Load Font and images
    sysfont = pygame.font.get_default_font()
    fontSize = int(squareHeight//3)
    font = pygame.font.SysFont(sysfont, fontSize)
    images = Functions.imageLoader(squareWidth, squareHeight)

    HasSelectedPiece = [False, None, None]
    CapturedPieces = []
    WhiteToMove = Functions.ConvertFENString(FEN)[1]

    # Main loop
    while gameRunning:
        Side, notSide = Functions.WhiteToMoveTONumber(WhiteToMove)

        # Check Pygame Events
        for event in pygame.event.get():
            # Window closed by X in topbar
            if event.type == pygame.QUIT:
                gameRunning = False
                print("Window closed")
            # Mouseclick event
            elif event.type == pygame.MOUSEBUTTONDOWN:

                # get Mouselocation
                mouseBoardLocation = Functions.SquareNumb(Functions.getBoardLocationCoords(xBoardCoordinates, yBoardCoordinates, width, height))
                
                # Select Piece
                if HasSelectedPiece == [False, None, None]:
                    if BoardConfig[0][mouseBoardLocation] != 0:
                        if BoardConfig[1][mouseBoardLocation] == Side:
                            HasSelectedPiece = engine.SelectPiece(mouseBoardLocation, BoardConfig, WhiteToMove, KQkqcanCastle)
                # Check if 2nd click isnt the same piece, If yes: unselect piece
                elif mouseBoardLocation == HasSelectedPiece[2]:
                    HasSelectedPiece = [False, None, None]
                # Move Piece
                elif HasSelectedPiece[0] == True and mouseBoardLocation != HasSelectedPiece[2]:
                    moveresult = engine.SelectMoveTo(HasSelectedPiece[2], mouseBoardLocation, BoardConfig, HasSelectedPiece[1], KQkqcanCastle)
                    if moveresult[0] == True:
                        CapturedPieces.append(moveresult[1])
                        WhiteToMove = not WhiteToMove
                        HasSelectedPiece = [False, None, None]
                    else: 
                        print("Move not Legal! ♜  Try again!")

        # Draw move etc.
        drawScreen(screen, font, selectedBoardTheme, BoardConfig, images, HasSelectedPiece)

        clock.tick(maxFramesPerSecond)
        pygame.display.flip()




def drawScreen(screen, font, selectedBoardTheme, BoardConfig, images, HasSelectedPiece):
    drawChessBoard(screen, font, selectedBoardTheme)
    drawChessPieces(screen, BoardConfig, images)
    if HasSelectedPiece[0] == True:
        # Draw legalmoves & Selected piece
        drawHighlight(screen, HasSelectedPiece)

# Draw Chessboard grid and coordinates
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

# Blit Images to location corresponding with Bitboard.
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
# Draw legalmoves
def drawHighlight(screen, HasSelectedPiece):
    for i in range(len(HasSelectedPiece[1][1])):
        row, column = Functions.brdnumtorowcol(HasSelectedPiece[1][1][i])
        pygame.draw.circle(screen, (109, 113, 46), (row*squareHeight + squareHeight / 2, column*squareWidth + squareWidth / 2), squareWidth // 8)
    Sqrow, Sqcolumn = Functions.brdnumtorowcol(HasSelectedPiece[2])
    pygame.draw.circle(screen, (200, 70, 46), (Sqrow*squareHeight + squareHeight / 2, Sqcolumn*squareWidth + squareWidth / 2), squareWidth // 2, 5)


if __name__ == "__main__":
    main()
    

