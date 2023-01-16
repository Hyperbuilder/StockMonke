
#Bord om te kijken of het stuk op het speelbord blijft, was sneller volgens gekke website
Board120x = [
     -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
     -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
     -1,  0,  1,  2,  3,  4,  5,  6,  7, -1,
     -1,  8,  9, 10, 11, 12, 13, 14, 15, -1,
     -1, 16, 17, 18, 19, 20, 21, 22, 23, -1,
     -1, 24, 25, 26, 27, 28, 29, 30, 31, -1,
     -1, 32, 33, 34, 35, 36, 37, 38, 39, -1,
     -1, 40, 41, 42, 43, 44, 45, 46, 47, -1,
     -1, 48, 49, 50, 51, 52, 53, 54, 55, -1,
     -1, 56, 57, 58, 59, 60, 61, 62, 63, -1,
     -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
     -1, -1, -1, -1, -1, -1, -1, -1, -1, -1
]

#Bord met offsets voor move generatie, waarom bij 21 beginnen? idk
Board64x = [
    21, 22, 23, 24, 25, 26, 27, 28,
    31, 32, 33, 34, 35, 36, 37, 38,
    41, 42, 43, 44, 45, 46, 47, 48,
    51, 52, 53, 54, 55, 56, 57, 58,
    61, 62, 63, 64, 65, 66, 67, 68,
    71, 72, 73, 74, 75, 76, 77, 78,
    81, 82, 83, 84, 85, 86, 87, 88,
    91, 92, 93, 94, 95, 96, 97, 98
]

# 0 = Empty, 1 = Pawn, 2 = Queen, 3 = King, 4 = Bishop, 5 = Knight, 6 = Rook
PieceList = [
    6, 5, 4, 2, 3, 4, 5, 6, 
    1, 1, 1, 1, 1, 1, 1, 1,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    1, 1, 1, 1, 1, 1, 1, 1, 
    6, 5, 4, 2, 3, 4, 5, 6,   
]

# 0 = Blank, 1 = White, 2 = Black
ColorList = [
    2, 2, 2, 2, 2, 2, 2, 2, 
    2, 2, 2, 2, 2, 2, 2, 2, 
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    1, 1, 1, 1, 1, 1, 1, 1, 
    1, 1, 1, 1, 1, 1, 1, 1, 
]




BeforePiece = input("Before ")
BeforePiece = int(BeforePiece)
AfterPiece = input("After ")
AfterPiece = int(AfterPiece)


#gekloot
PieceList.pop(BeforePiece)
ColorList.pop(BeforePiece)

PieceDict = {
    0 : " ",
    1 : "P",
    2 : "Q",
    3 : "K",
    4 : "B", 
    5 : "N",
    6 : "R"
}
ColorDict = {
    0 : " ",
    1 : "W",
    2 : "B"
}

for i in range(8):
    for j in range(8):
        Piece = PieceList[i * 8 + j]
        Color = ColorList[i * 8 + j]

        print(PieceDict[Piece], ColorDict[Color], sep='', end= " ")
    print()



