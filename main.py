import pygame as pygame
import engine

width = 512
height = 512
xDimension = 8
yDimension = 8
squareWidth = width / xDimension
squareHeight = height / yDimension
maxFramesPerSecond = 30

#Initialize images once to improve performance
#Load image with "images['piece']"
images = {}

def imageLoader():
    pieces = ['PW', 'RW', 'NW', 'BW', 'QW', 'KW', 'PB', 'RB', 'NB', 'BB', 'QB', 'KB']
    for piece in pieces:
        images[piece] = pygame.transform.scale(pygame.image.load("images/" + piece + ".png"), (squareWidth,squareHeight))

def main():
    pygame.init()
    screen = pygame.display.set_mode((width,height), #pygame.NOFRAME
    );
    clock = pygame.time.Clock()
    gState = engine.GameState()
    gameRunning = True
    imageLoader()

    selectedSquare = ()
    mouseClickEvents = []
    while gameRunning:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameRunning = False
                print("Window closed")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouseLocation = pygame.mouse.get_pos()
                column = mouseLocation[0] // squareWidth
                row = mouseLocation[1] // squareHeight
                if selectedSquare == (row, column):
                    selectedSquare == ()
                    mouseClickEvents == []
                else:
                    selectedSquare = (row, column)
                    mouseClickEvents.append(selectedSquare)
                if len(mouseClickEvents) == 2:
                    

        drawGState(screen, gState)
        clock.tick(maxFramesPerSecond)
        pygame.display.flip()


def drawGState(screen, gState):
    drawChessBoard(screen)
    drawChessPieces(screen, gState.board)

def drawChessBoard(screen):
    colorThemes = [
        [pygame.Color("white"), pygame.Color("darkgray")],
        [pygame.Color("white"), pygame.Color("purple")],
    ]

    for row in range(8):
        for column in range(8):
            color = colorThemes[0][((row+column) % 2)]
            pygame.draw.rect(screen, color, pygame.Rect(column*squareWidth, row*squareHeight, squareWidth, squareHeight))


def drawChessPieces(screen, board):
    for row in range(yDimension):
        for column in range(xDimension):
            piece = board[row][column]
            if piece != "--":
                screen.blit(images[piece], pygame.Rect(column*squareWidth, row*squareHeight, squareWidth, squareHeight))


if __name__ == "__main__":
    main()
