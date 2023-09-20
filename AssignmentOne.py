
import flask
import json
import random
app = flask.Flask(__name__)

boards = {}
gameId = 0

@app.route("/newgame")
def newGameHelp() -> str:
    return "Usage: http://localhost:5000/newgame/player, where player is x or o"

@app.route("/newgame/<player>")
def newgame(player: str) -> str:
    player = player.lower()
    if player not in ['x', 'o']:
        return newGameHelp()
    global boards
    global gameId
    newBoard = '-' * 19 * 19
    boards[gameId] = f"x#{newBoard}#0#0"
    if player == 'o':
        doComputerMove(gameId)
    output = {'ID': gameId, 'state': boards[gameId]}
    gameId += 1

    return json.dumps(output) + "<br>" + getFormattedBoard(gameId-1)

@app.route("/nextmove/")
def nextmoveHelp():
    return "Usage: http://localhost:5000/nextmove/gameID/row/col, where:<br>-gameID is a previously created game<br>-row and column are a legal move space"

def getSquare(gameId: int, row: int, column: int) -> str:
    return boards[gameId][row * 19 + column + 2]

def setSquare(gameId: int, row: int, column: int, newChar: str) -> None:
    idx = row * 19 + column + 2
    boards[gameId] = boards[gameId][:idx] + newChar + boards[gameId][idx + 1:]

def isInBounds(row: int, col: int) -> bool:
    if row < 0 or row >= 19:
        return False
    if col < 0 or col >= 19:
        return False
    return True

def getTurn(gameId: int) -> None:
    return boards[gameId][0]

def changeTurn(gameId: int) -> None:
    turn = getTurn(gameId)
    if turn == 'x':
        boards[gameId] = 'o' + boards[gameId][1:]
    else:
        boards[gameId] = 'x' + boards[gameId][1:]

def checkPattern(gameId: int, start: tuple[int, int], direction: tuple[int, int], pattern: list) -> bool:
    # key:
    # x and o: player characters
    # *: wildcard
    # |: border
    # -: empty
    # _: empty but the place to move in (center of the pattern)
    r, c = start
    dr, dc = direction
    l = len(pattern)
    if not isInBounds(r + (l-1)*dr, c + (l-1)*dc):
        if pattern[-1] == '|' and isInBounds(r + (l-2)*dr, c + (l-2)*dc):
            l -= 1
        else:
            return False
    elif pattern[-1] == '|':
        return False
    for i in range(l):
        if getSquare(gameId, r, c) != pattern[i] and pattern[i] != "*":
            return False
        r += dr
        c += dc
    return True
        

def getCaptures(gameId: int, player: str) -> int:
    if player == 'x':
        return int(boards[gameId][2 + 19 * 19 + 1])
    else:
        return int(boards[gameId][2 + 19 * 19 + 3])
    
def recordCapture(gameId: int, player: str) -> None:
    if player == 'x':
        newScore = str(int(boards[gameId][-3]) + 1)
        boards[gameId] = boards[gameId][:-3] + newScore + boards[gameId][-2:]
    else:
        newScore = str(int(boards[gameId][-1]) + 1)
        boards[gameId] = boards[gameId][:-1] + newScore

def checkCapture(gameId: int, row: int, col: int, direction: tuple[int, int], player: str, opponent: str) -> None:
    if checkPattern(gameId, (row, col), direction, [player, opponent, opponent, player]):
        dr, dc = direction
        setSquare(gameId, row + dr, col + dc, '-')
        setSquare(gameId, row + 2*dr, col + 2*dc, '-')
        recordCapture(gameId, player)

def doCaptures(gameId: int, row: int, col: int, player: str) -> None:
    opponent = 'o' if player == 'x' else 'x'
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0: continue
            checkCapture(gameId, row, col, (i, j), player, opponent)  
    if getCaptures(gameId, player) >= 5:
        displayWin(gameId, player)

    

def doMove(gameId: int, row: int, col: int) -> None:
    turn = getTurn(gameId)
    setSquare(gameId, row, col, turn)
    doCaptures(gameId, row, col, turn)
    checkForFiveInARow(gameId, row, col, turn)
    changeTurn(gameId)

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
                    if checkPattern(gameId, (r, c), (dr, dc), pattern):
                        captures.append((r + dr*moveIdx, c+dc*moveIdx))
    return captures

def findGoodMoves(gameId: int) -> list[tuple[int, int]]:
    p = getTurn(gameId)
    o = "x" if p == "o" else "o"

    # move patterns in order of how good they are
    patterns = [['-', p, p, p, p], # make five in a row
                    ['-', o, o, o, o], # block five in a row
                    ['-', p, p, p], # make four in a row
                    [o, o, '_', o], # block four in a row
                    ['-', o, o, o, '*'], # block four in a row away from the edge
                    ['-', o, o, p], # make a capture
                    ['-', p, p, '*'], # threaten a capture away from the edge
                    ['-', p, '-'], # make two in a row with space
                    ['-', o, '*'], # get in the way, away from the edge
                    ['-']] # any legal move
    
    for pattern in patterns:
        moves = searchForPattern(gameId, pattern)
        if len(moves) > 0:
            return moves
    
    raise NotImplementedError
    
    

def doComputerMove(gameId: int) -> None:
    moveChoices = findGoodMoves(gameId)
    move = moveChoices[random.randint(0, len(moveChoices)-1)]
    doMove(gameId, move[0], move[1])

def getFormattedBoard(gameId: int) -> str:
    squares = boards[gameId][2:-4].replace("-", "_")
    lines = [" ".join(list(squares[19 * i: 19 * i + 19]) + [str(i+1)]) for i in range(19)]
    lines.append("0 " * 9 + "1 " * 10)
    lines.append(" ".join([str(i % 10) for i in range(1, 20)]))
    return "<br>".join(lines)

def displayWin(gameId: int, player: str):
    raise NotImplementedError

def checkForFiveInARow(gameId: int, row: int, col: int, player: str) -> None:
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0: continue
            if checkPattern(gameId, (row, col), (i, j), [player] * 5):
                displayWin(gameId, player)
 
@app.route("/nextmove/<int:gameId>/<int:row>/<int:column>")
def nextmove(gameId: int, row: int, column: int) -> str:
    row -= 1
    column -= 1
    global boards
    if gameId not in boards or row < 0 or row >= 19 or column < 0 or column >= 19 or getSquare(gameId, row, column) != "-":
        return nextmoveHelp()
    doMove(gameId, row, column)
    doComputerMove(gameId)
    return json.dumps({'ID': gameId, 'row': row, 'column': column, 'state': boards[gameId]}) + "<br>" + getFormattedBoard(gameId)


if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)