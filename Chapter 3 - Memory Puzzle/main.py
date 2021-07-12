# Memory Puzzle
# By Al Erislash
# Released under a "Simplified BSD" license
import pygame, random, sys, pprint
from pygame.locals import *  # All the constants


class Icon:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color


FPS = 30

WINDOW_SIZE = {
    'width': 640,
    'height': 480
}

# Speed of the cover and uncover box
ANIMATION_SPEED = 8

BOX_SIZE = 40
GAP = 10
COLUMNS = 4
ROWS = 3
assert ((COLUMNS * ROWS) % 2 == 0), 'The board MUST have an even number of boxes'

# Margins of the board -- (Window's size - Total space filled by boxes) / 2
MARGINS = {
    'x': int((WINDOW_SIZE['width'] - (BOX_SIZE + GAP) * COLUMNS) / 2),
    'y': int((WINDOW_SIZE['height'] - (BOX_SIZE + GAP) * ROWS) / 2)
}

# Colors
GRAY = (100, 100, 100)
NAVYBLUE = (60, 60, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)

# Background color
BACKGROUND = NAVYBLUE
# Light background color
LBACKGROUND = GRAY
BOX_COLOR = WHITE
# Box highlight color
HIGHLIGHT = BLUE

DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'

COLORS = [GRAY, WHITE, RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN]
SHAPES = [DONUT, SQUARE, DIAMOND, LINES, OVAL]
# Making sure there's enough color/shapes combinations to fill the board
assert (len(COLORS) * len(SHAPES) * 2 >= COLUMNS * ROWS), 'Board is too big for the number of possible icons'

pygame.init()

CLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((WINDOW_SIZE['width'], WINDOW_SIZE['height']), 0, 32)
pygame.display.set_caption('Memory Game!')


def main():
    mousePos = {
        'x': 0,
        'y': 0
    }
    SCREEN.fill(BACKGROUND)
    # Gets the structure of the board filled with random icons (shape/color)
    mainBoard: list[list[Icon]] = getRandomBoard()
    revealedBoard: list = generateBoxesData(False)

    firstSelect = None
    # startGameAnimation(mainBoard)
    startGameAnimation(mainBoard)
    # Main game loop
    while True:
        mouseClicked = False
        SCREEN.fill(NAVYBLUE)
        drawBoard(mainBoard, revealedBoard)

        events = pygame.event.get()
        for event in events:
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousePos['x'] = event.pos[0]
                mousePos['y'] = event.pos[1]
            elif event.type == MOUSEBUTTONUP:
                mousePos['x'] = event.pos[0]
                mousePos['y'] = event.pos[1]
                mouseClicked = True

        box_X, box_Y = getBoxAtCoords(mousePos['x'], mousePos['y'])

        if box_X is not None and box_Y is not None:
            if not revealedBoard[box_X][box_Y]:
                highlightBox(box_X, box_Y)

            if not revealedBoard[box_X][box_Y] and mouseClicked:
                revealBoxAnimation(mainBoard, [(box_X, box_Y)])
                revealedBoard[box_X][box_Y] = True

                if firstSelect == None:
                    firstSelect = (box_X, box_Y)
                else:
                    firstIconShape, firstIconColor = getIcon(mainBoard, firstSelect[0], firstSelect[1])
                    secondIconShape, secondIconColor = getIcon(mainBoard, box_X, box_Y)
                    if firstIconColor != secondIconColor or firstIconShape != secondIconShape:
                        pygame.time.wait(1000)
                        coverBoxAnimation(mainBoard, [(firstSelect[0], firstSelect[1]), (box_X, box_Y)])
                        revealedBoard[firstSelect[0]][firstSelect[1]] = False
                        revealedBoard[box_X][box_Y] = False
                    elif hasWon(revealedBoard):
                        gameWonAnimation(mainBoard)
                        pygame.time.wait(2000)

                    firstSelect = None

        pygame.display.update()
        CLOCK.tick(FPS)


def generateBoxesData(val):
    boxes: list = []
    for i in range(COLUMNS):
        boxes += [[val] * ROWS]
    return boxes


def getIcons():
    icons: list[Icon] = []
    for color in COLORS:
        for shape in SHAPES:
            icons.append(Icon(shape, color))
    random.shuffle(icons)
    # How many icons do I need to fill the main board.
    iconsNeeded: int = int((COLUMNS * ROWS) / 2)
    # Double the icons in list the get a couple of each icon
    icons = icons[:iconsNeeded] * 2
    random.shuffle(icons)
    return icons


def getRandomBoard():
    icons = getIcons()

    board: list[list[Icon]] = []
    for x in range(COLUMNS):
        column: list[Icon] = []
        for y in range(ROWS):
            column.append(icons[0])
            del icons[0]
        board.append(column)
    return board


def originBoxCoords(box_X: int, box_Y: int) -> tuple:
    # Get the origin in pixels of a specific box
    left = box_X * (BOX_SIZE + GAP) + MARGINS['x']
    top = box_Y * (BOX_SIZE + GAP) + MARGINS['y']
    return left, top


def getIcon(mainBoard: list[list[Icon]], box_X: int, box_Y: int) -> tuple:
    icon = mainBoard[box_X][box_Y]
    return icon.shape, icon.color


def splitIntoGroups(groupSize, list):
    result = []
    for i in range(0, len(list), groupSize):
        result.append(list[i:i + groupSize])
    return result


def drawIcon(shape, color, box_X, box_Y):
    quarter = int(BOX_SIZE / 4)
    half = int(BOX_SIZE / 2)

    left, top = originBoxCoords(box_X, box_Y)

    if shape == DONUT:
        pygame.draw.circle(SCREEN, color, (left + half, top + half), half - 5)
        pygame.draw.circle(SCREEN, BACKGROUND, (left + half, top + half), quarter - 5)
    elif shape == SQUARE:
        pygame.draw.rect(SCREEN, color, (left + quarter, top + quarter, BOX_SIZE - half, BOX_SIZE - half))
    elif shape == DIAMOND:
        pygame.draw.polygon(SCREEN, color, ((left + half, top), (left + BOX_SIZE - 1, top + half),
                                            (left + half, top + BOX_SIZE - 1), (left, top + half)))
    elif shape == LINES:
        for i in range(0, BOX_SIZE, 4):
            pygame.draw.line(SCREEN, color, (left, top + 1), (left + i, top))
            pygame.draw.line(SCREEN, color, (left + i, top + BOX_SIZE - 1), (left + BOX_SIZE - 1, top + i))
    elif shape == OVAL:
        pygame.draw.ellipse(SCREEN, color, (left, top + quarter, BOX_SIZE, half))


def drawBoard(mainBoard: list[list[Icon]], revealedBoard: list[list[bool]]):
    for box_X in range(COLUMNS):
        for box_Y in range(ROWS):
            left, top = originBoxCoords(box_X, box_Y)
            if not revealedBoard[box_X][box_Y]:
                pygame.draw.rect(SCREEN, BOX_COLOR, (left, top, BOX_SIZE, BOX_SIZE))
            else:
                shape, color = getIcon(mainBoard, box_X, box_Y)
                drawIcon(shape, color, box_X, box_Y)


def getBoxAtCoords(x, y):
    for box_X in range(COLUMNS):
        for box_Y in range(ROWS):
            left, top = originBoxCoords(box_X, box_Y)
            if (left < x < left + BOX_SIZE) and (top < y < top + BOX_SIZE):
                return box_X, box_Y

    return None, None


def highlightBox(box_X, box_Y):
    left, top = originBoxCoords(box_X, box_Y)
    pygame.draw.rect(SCREEN, HIGHLIGHT, (left - 5, top - 5, BOX_SIZE + 10, BOX_SIZE + 10))


def drawBoxCover(mainBoard, boxes, coverage):
    for box in boxes:
        left, top = originBoxCoords(box[0], box[1])
        pygame.draw.rect(SCREEN, BACKGROUND, (left, top, BOX_SIZE, BOX_SIZE))
        shape, color = getIcon(mainBoard, box[0], box[1])
        drawIcon(shape, color, box[0], box[1])
        if coverage > 0:
            pygame.draw.rect(SCREEN, BOX_COLOR, (left, top, coverage, BOX_SIZE))

    pygame.display.update()
    CLOCK.tick(FPS)


def revealBoxAnimation(mainBoard: list[list[Icon]], boxes):
    for coverage in range(BOX_SIZE, (-ANIMATION_SPEED) - 1, -ANIMATION_SPEED):
        drawBoxCover(mainBoard, boxes, coverage)


def coverBoxAnimation(mainBoard, boxesToCover):
    for coverage in range(0, BOX_SIZE + ANIMATION_SPEED, ANIMATION_SPEED):
        drawBoxCover(mainBoard, boxesToCover, coverage)


def startGameAnimation(mainBoard):
    coverBoxes = generateBoxesData(False)
    boxes = []
    for x in range(COLUMNS):
        for y in range(ROWS):
            boxes.append((x, y))
    random.shuffle(boxes)
    boxGroups = splitIntoGroups(8, boxes)

    drawBoard(mainBoard, coverBoxes)
    for boxGroup in boxGroups:
        revealBoxAnimation(mainBoard, boxGroup)
        coverBoxAnimation(mainBoard, boxGroup)


def gameWonAnimation(mainBoard):
    coveredBoxes = generateBoxesData(True)
    color1 = LBACKGROUND
    color2 = BACKGROUND

    for i in range(13):
        color1, color2 = color2, color1
        SCREEN.fill(color1)
        drawBoard(mainBoard, coveredBoxes)
        pygame.display.update()
        pygame.time.wait(300)


def hasWon(revealedBoxes):
    for i in revealedBoxes:
        if False in i:
            return False
    return True


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
