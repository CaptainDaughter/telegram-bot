import random, time, pygame, sys
from pygame.locals import *

fps = 20
window_w = 450
window_h = 480
cellsize = 20
playarea_w = 10
playarea_h = 20
blank = '.'

movetoside = 0.15
movedown = 0.1

templatew = 5
templateh = 5


location_outline = int((window_w - playarea_w * cellsize) / 5)
location_outline_2 = window_h - (playarea_h * cellsize) - 10

white = (255, 255, 255)
outline_col = (9, 85, 131)
black = (0, 0, 0)

red = (255, 51, 51)
lightr = (255, 0, 0)
green = (0, 153, 0)
lightg = (0, 204, 0)
blue = (0, 66, 133)
lightb = (0, 92, 184)
yellow = (255, 220, 51)
lighty = (255, 213, 0)

colour_outline = outline_col
colour_bg = black
text_color = white
COLORS = (blue, green, red, yellow)
LIGHTCOLORS = (lightb, lightg, lightr, lighty)
assert len(COLORS) == len(LIGHTCOLORS)

S_piece = [['.....',
            '.....',
            '..OO.',
            '.OO..',
            '.....'],
           ['.....',
            '..O..',
            '..OO.',
            '...O.',
            '.....']]

Z_piece = [['.....',
            '.....',
            '.OO..',
            '..OO.',
            '.....'],
           ['.....',
            '..O..',
            '.OO..',
            '.O...',
            '.....']]

I_piece = [['..O..',
            '..O..',
            '..O..',
            '..O..',
            '.....'],
           ['.....',
            '.....',
            'OOOO.',
            '.....',
            '.....']]

O_piece = [['.....',
            '.....',
            '.OO..',
            '.OO..',
            '.....']]

J_piece = [['.....',
            '.O...',
            '.OOO.',
            '.....',
            '.....'],
           ['.....',
            '..OO.',
            '..O..',
            '..O..',
            '.....'],
           ['.....',
            '.....',
            '.OOO.',
            '...O.',
            '.....'],
           ['.....',
            '..O..',
            '..O..',
            '.OO..',
            '.....']]

L_piece = [['.....',
            '...O.',
            '.OOO.',
            '.....',
            '.....'],
           ['.....',
            '..O..',
            '..O..',
            '..OO.',
            '.....'],
           ['.....',
            '.....',
            '.OOO.',
            '.O...',
            '.....'],
           ['.....',
            '.OO..',
            '..O..',
            '..O..',
            '.....']]

T_piece = [['.....',
            '..O..',
            '.OOO.',
            '.....',
            '.....'],
           ['.....',
            '..O..',
            '..OO.',
            '..O..',
            '.....'],
           ['.....',
            '.....',
            '.OOO.',
            '..O..',
            '.....'],
           ['.....',
            '..O..',
            '.OO..',
            '..O..',
            '.....']]

PIECES = {'S': S_piece, 'Z': Z_piece, 'J': J_piece, 'L': L_piece, 'I': I_piece, 'O': O_piece, 'T': T_piece}


def main():
    global clock, window, font_basic, font_big
    pygame.init()
    clock = pygame.time.Clock()
    window = pygame.display.set_mode((window_w, window_h))
    font_basic = pygame.font.Font('freesansbold.ttf', 18)
    font_big = pygame.font.Font('freesansbold.ttf', 80)
    pygame.display.set_caption('Тетрис')

    showTextScreen('Тетрис')
    while True:
        runGame()
        window.fill(colour_bg)
        showTextScreen('Game Over')


def runGame():
    board = BlankBoard()
    lastMoveDownTime = time.time()
    lastMoveSideTime = time.time()
    lastFallTime = time.time()
    movingDown = False
    moveLeft = False
    moveRight = False
    score = 0
    level, Frequencyfall = calculate(score)

    fallingPiece = NewPiece()
    nextPiece = NewPiece()

    while True:
        if fallingPiece == None:
            fallingPiece = nextPiece
            nextPiece = NewPiece()
            lastFallTime = time.time()

            if not ValidPosition(board, fallingPiece):
                return

        checkForQuit()
        for event in pygame.event.get():
            if event.type == KEYUP:
                if event.key == K_p:
                    showTextScreen('Paused')
                    lastFallTime = time.time()
                    lastMoveDownTime = time.time()
                    lastMoveSideTime = time.time()
                elif event.key == K_LEFT:
                    moveLeft = False
                elif event.key == K_RIGHT:
                    moveRight = False
                elif event.key == K_DOWN:
                    movingDown = False

            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and ValidPosition(board, fallingPiece, adjX=-1):
                    fallingPiece['x'] -= 1
                    moveLeft = True
                    moveRight = False
                    lastMoveSideTime = time.time()

                elif (event.key == K_RIGHT or event.key == K_d) and ValidPosition(board, fallingPiece, adjX=1):
                    fallingPiece['x'] += 1
                    moveRight = True
                    moveLeft = False
                    lastMoveSideTime = time.time()

                elif event.key == K_UP or event.key == K_w:
                    fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(PIECES[fallingPiece['shape']])
                    if not ValidPosition(board, fallingPiece):
                        fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(PIECES[fallingPiece['shape']])
                elif event.key == K_q:
                    fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(PIECES[fallingPiece['shape']])
                    if not ValidPosition(board, fallingPiece):
                        fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(PIECES[fallingPiece['shape']])

                elif event.key == K_DOWN or event.key == K_s:
                    movingDown = True
                    if ValidPosition(board, fallingPiece, adjY=1):
                        fallingPiece['y'] += 1
                    lastMoveDownTime = time.time()

                elif event.key == K_SPACE:
                    movingDown = False
                    moveLeft = False
                    moveRight = False
                    for i in range(1, playarea_h):
                        if not ValidPosition(board, fallingPiece, adjY=i):
                            break
                    fallingPiece['y'] += i - 1

        if (moveLeft or moveRight) and time.time() - lastMoveSideTime > movetoside:
            if moveLeft and ValidPosition(board, fallingPiece, adjX=-1):
                fallingPiece['x'] -= 1
            elif moveRight and ValidPosition(board, fallingPiece, adjX=1):
                fallingPiece['x'] += 1
            lastMoveSideTime = time.time()

        if movingDown and time.time() - lastMoveDownTime > movedown and ValidPosition(board, fallingPiece, adjY=1):
            fallingPiece['y'] += 1
            lastMoveDownTime = time.time()

        if time.time() - lastFallTime > Frequencyfall:
            if not ValidPosition(board, fallingPiece, adjY=1):
                addPieceToBoard(board, fallingPiece)
                score += removeCompleteLines(board)
                level, Frequencyfall = calculate(score)
                fallingPiece = None
            else:
                fallingPiece['y'] += 1
                lastFallTime = time.time()

        window.fill(colour_bg)
        drawBoard(board)
        Status(score, level)
        TextNext(nextPiece)
        if fallingPiece != None:
            drawPiece(fallingPiece)

        pygame.display.update()
        clock.tick(fps)


def makeTextObjs(text, font, color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()


def terminate():
    pygame.quit()
    sys.exit()


def checkKeyPress():
    checkForQuit()
    for event in pygame.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue
        return event.key
    return None


def showTextScreen(text):
    titleSurf, titleRect = makeTextObjs(text, font_big, text_color)
    titleRect.center = (int(window_w / 2) - 3, int(window_h / 2) - 3)
    window.blit(titleSurf, titleRect)

    pressKeySurf, pressKeyRect = makeTextObjs('Press a key to play.', font_basic, text_color)
    pressKeyRect.center = (int(window_w / 2), int(window_h / 2) + 100)
    window.blit(pressKeySurf, pressKeyRect)

    while checkKeyPress() == None:
        pygame.display.update()
        clock.tick()


def checkForQuit():
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            terminate()
        pygame.event.post(event)


def calculate(score):
    level = int(score / 10) + 1
    fallFreq = 0.30 - (level * 0.02)
    return level, fallFreq


def NewPiece():
    shape = random.choice(list(PIECES.keys()))
    newPiece_ = {'shape': shape,
                 'rotation': random.randint(0, len(PIECES[shape]) - 1),
                 'x': int(playarea_w / 2) - int(templatew / 2),
                 'y': -2,
                 'color': random.randint(0, len(COLORS) - 1)}
    return newPiece_


def addPieceToBoard(board, piece):
    for x in range(templatew):
        for y in range(templateh):
            if PIECES[piece['shape']][piece['rotation']][y][x] != blank:
                board[x + piece['x']][y + piece['y']] = piece['color']


def BlankBoard():
    board = []
    for i in range(playarea_w):
        board.append([blank] * playarea_h)
    return board


def isOnBoard(x, y):
    return x >= 0 and x < playarea_w and y < playarea_h


def ValidPosition(board, piece, adjX = 0, adjY = 0):
    for x in range(templatew):
        for y in range(templateh):
            AboveBoard = y + piece['y'] + adjY < 0
            if AboveBoard or PIECES[piece['shape']][piece['rotation']][y][x] == blank:
                continue
            if not isOnBoard(x + piece['x'] + adjX, y + piece['y'] + adjY):
                return False
            if board[x + piece['x'] + adjX][y + piece['y'] + adjY] != blank:
                return False
    return True


def CompleteLine(board, y):
    for x in range(playarea_w):
        if board[x][y] == blank:
            return False
    return True


def removeCompleteLines(board):
    numLinesRemoved = 0
    y = playarea_h - 1
    while y >= 0:
        if CompleteLine(board, y):
            for pullDown_y in range(y, 0, -1):
                for x in range(playarea_w):
                    board[x][pullDown_y] = board[x][pullDown_y - 1]
            for x in range(playarea_w):
                board[x][0] = blank
            numLinesRemoved += 1
        else:
            y -= 1
    return numLinesRemoved


def convertToPixCoords(boxx, boxy):
    return (location_outline + (boxx * cellsize)), (location_outline_2 + (boxy * cellsize))


def drawCell(cell_x, cell_y, color, pixel_x=None, pixel_y=None):
    if color == blank:
        return
    if pixel_x == None and pixel_y == None:
        pixel_x, pixel_y = convertToPixCoords(cell_x, cell_y)
    pygame.draw.rect(window, COLORS[color], (pixel_x + 1, pixel_y + 1, cellsize - 1, cellsize - 1))
    pygame.draw.rect(window, LIGHTCOLORS[color], (pixel_x + 1, pixel_y + 1, cellsize - 4, cellsize - 4))


def drawBoard(board):
    pygame.draw.rect(window, colour_outline,
                     (location_outline - 3, location_outline_2 - 7, (playarea_w * cellsize) + 8, (playarea_h * cellsize) + 8), 5)

    pygame.draw.rect(window, colour_bg, (location_outline, location_outline_2, cellsize * playarea_w, cellsize * playarea_h))
    for x in range(playarea_w):
        for y in range(playarea_h):
            drawCell(x, y, board[x][y])


def Status(score, level):
    scoreSurf = font_basic.render('Score: %s' % score, True, text_color)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (window_w - 120, 20)
    window.blit(scoreSurf, scoreRect)

    levelSurf = font_basic.render('Level: %s' % level, True, text_color)
    levelRect = levelSurf.get_rect()
    levelRect.topleft = (window_w - 120, 50)
    window.blit(levelSurf, levelRect)


def drawPiece(piece, pixel_x=None, pixel_y=None):
    shapeDraw = PIECES[piece['shape']][piece['rotation']]
    if pixel_x == None and pixel_y == None:
        pixel_x, pixel_y = convertToPixCoords(piece['x'], piece['y'])

    for x in range(templatew):
        for y in range(templateh):
            if shapeDraw[y][x] != blank:
                drawCell(None, None, piece['color'], pixel_x + (x * cellsize), pixel_y + (y * cellsize))


def TextNext(piece):
    nextSurf = font_basic.render('Next:', True, text_color)
    nextRect = nextSurf.get_rect()
    nextRect.topleft = (window_w - 120, 80)
    window.blit(nextSurf, nextRect)
    drawPiece(piece, pixel_x =window_w - 100, pixel_y = 100)


if __name__ == '__main__':
    main()
