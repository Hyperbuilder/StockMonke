import pygame as pygame
import engine

width = 512
height = 512
xDimension = 8
yDimension = 8
squareWidth = width / xDimension
squareHeight = height / yDimension
maxFramesPerSecond = 5

#Initialize images once to improve performance
#Load image with "images['piece']"
images = {}

def imageLoader():
    pieces = ['wP', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bP', 'bR', 'bN', 'bB', 'bQ', 'bK']
    for piece in pieces:
        images[piece] = pygame.transform.scale(pygame.image.load("images/" + piece + ".png"), (squareWidth,squareHeight))

def main():
    pygame.init()
    screen = pygame.display.set_mode((width,height));
    clock = pygame.time.Clock()
    gState = engine.GameState()

    print(gState)

main()