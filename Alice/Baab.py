import random

import AssignmentOne

def findGoodMoves(gameId: int) -> list[tuple[int, int]]:
    p = AssignmentOne.getTurn(gameId)
    o = "x" if p == "o" else "o"

    # move patterns in order of how good they are
    patterns = [['-', p, p, p, p], # make five in a row
                ['-', o, o, o, o], # block five in a row
                ['-', p, p, p], # make four in a row
                #[o, o, '_', o], # block four in a row
                ['-', o, o, o, '*'], # block four in a row away from the edge
                ['-', o, o, p], # make a capture
                ['-', p, p, '*'], # threaten a capture away from the edge
                ['-', p, '-'], # make two in a row with space
                #['-', o, '*'], # get in the way, away from the edge
                ['-']] # any legal move

    for pattern in patterns:
        moves = searchForPattern(gameId, pattern)
        if len(moves) > 0:
            return moves

    raise NotImplementedError

def makeMove(gameId: int) -> tuple:
    moveChoices = findGoodMoves(gameId)
    move = moveChoices[random.randint(0, len(moveChoices)-1)]
    return move[0], move[1]

def searchForPattern(gameId: int, pattern: list[str]) -> list[tuple[int, int]]:
    if "_" in pattern:
        moveIdx = pattern.index("_")
        pattern[moveIdx] = "-"
    else:
        moveIdx = 0
    captures = []
    for r in range(19):
        for c in range(19):
            for dr in range(-1, 2):
                for dc in range(-1, 2):
                    if dr == 0 and dc == 0:
                        continue
                    if AssignmentOne.checkPattern(gameId, (r, c), (dr, dc), pattern):
                        captures.append((r + dr*moveIdx, c+dc*moveIdx))
    return captures
