import pygame as pygame


#Standaard waarden voor venster en schaakbord
width = 1024
height = 1024
xDimension = 8
yDimension = 8
squareWidth = width / xDimension
squareHeight = height / yDimension
maxFramesPerSecond = 30


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
    screen = pygame.display.set_mode((width,height), #pygame.NOFRAME
    );
    clock = pygame.time.Clock()
    gameRunning = True
    
    sysfont = pygame.font.get_default_font()
    fontSize = int(squareHeight//3)
    font = pygame.font.SysFont(sysfont, fontSize)

    imageLoader()

    while gameRunning:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameRunning = False
                print("Window closed")
                    

        drawScreen(screen, font)
        clock.tick(maxFramesPerSecond)
        pygame.display.flip()

def drawScreen(screen, font):
    drawChessBoard(screen, font)

def drawChessBoard(screen, font):
    colorThemes = [
        [pygame.Color("white"), pygame.Color("darkgray")],
        [pygame.Color("white"), pygame.Color("purple")],
    ]

    for row in range(8):
        for column in range(8):
            color = colorThemes[0][((row+column) % 2)]
            pygame.draw.rect(screen, color, pygame.Rect(column*squareWidth, row*squareHeight, squareWidth, squareHeight))
            if row == 7:
                coordinateText = font.render(xBoardCoordinates[column], False, (200, 200, 200))
                screen.blit(coordinateText, (column*squareWidth + squareWidth - 21, row*squareHeight + squareHeight - 30))
            elif column == 0:
                coordinateText = font.render(yBoardCoordinates[row], False, (200, 200, 200))
                screen.blit(coordinateText, (column*squareWidth + 3, row*squareHeight + 3))



def drawChessPieces(screen, board):
    for row in range(yDimension):
        for column in range(xDimension):
            piece = board[row][column]
            if piece != "--":
                screen.blit(images[piece], pygame.Rect(column*squareWidth, row*squareHeight, squareWidth, squareHeight))


if __name__ == "__main__":
    main()
