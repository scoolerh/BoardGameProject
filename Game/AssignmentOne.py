
import flask
import json
import random
import Alice
import Baab

app = flask.Flask(__name__)

boards = {}
gameId = 0

@app.route("/")
def homepage():
    """Landing page of website. Shows user how to play game."""
    return newGameHelp()

@app.route("/alice/")
def evaluator():
    newgame("x")
    row = random.randint(0,18)
    column = random.randint(0,18)
    setSquare(gameId-1,row,column,'x')
    while(getSquare(gameId-1, row, column) == 'x'):
        row = random.randint(0,18)
        column = random.randint(0,18)
    setSquare(gameId-1,row,column,'o')
    while(boards[gameId-1][-1] != 'c'):
        alicemove = Alice.makeMove(gameId-1)
        doMove(gameId-1, alicemove[0], alicemove[1])
    return 'x' if boards[gameId-1][0] == 'o' else 'o'

@app.route("/alicevbaab/")
def evaluateBaab():
    newgame("x")
    whoIsX = random.randint(0,1)
    x = None
    xIs = "Alice"
    if (whoIsX == 0):
        x = Alice.makeMove
        o = Baab.makeMove
    else:
        x = Baab.makeMove
        o = Alice.makeMove
        xIs = "Baab"
    while(boards[gameId-1][-1] != 'c'):
        xmove = x(gameId-1)
        doMove(gameId-1, xmove[0], xmove[1])
        if(boards[gameId-1][-1] != 'c'):
            omove = o(gameId-1)
            doMove(gameId-1, omove[0], omove[1])
    return xIs if boards[gameId-1][0] == 'o' else ("Alice" if xIs == "Baab" else "Baab")

@app.route("/newgame")
def newGameHelp() -> str:
    """Returns instructions to play the game"""
    return "Usage: http://localhost:7555/newgame/player, where player is x or o"

@app.route("/newgame/<player>")
def newgame(player: str) -> str:
    """Takes input, player, which is either x or o and initializes game with that property"""
    player = player.lower()
    if player not in ['x', 'o']:
        return newGameHelp()
    global boards
    global gameId
    newBoard = '-' * 19 * 19
    boards[gameId] = f"x#{newBoard}#0#0"
    if player == 'o':
        computerMove = Alice.makeMove(gameId)
        doMove(gameId, computerMove[0], computerMove[1])
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
    """start represents the starting position and direction represents which way this algorithm will scan.
    It searches for the pattern found in the pattern parameter."""
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
    caps = boards[gameId].split('#')
    if player == 'x':
        return int(caps[2])
    else:
        return int(caps[3])
    
def recordCapture(gameId: int, player: str) -> None:
    gameState = boards[gameId].split("#")
    if player == 'x':
        gameState[2] = str(int(gameState[2]) + 1)
        boards[gameId] = "#".join(gameState)
    else:
        gameState[3] = str(int(gameState[2]) + 1)
        boards[gameId] = "#".join(gameState)

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
            if i == 0 and j == 0:
                continue
            checkCapture(gameId, row, col, (i, j), player, opponent)  
    if getCaptures(gameId, player) >= 5:
        displayWin(gameId, player)

    

def doMove(gameId: int, row: int, col: int) -> None:
    turn = getTurn(gameId)
    setSquare(gameId, row, col, turn)
    doCaptures(gameId, row, col, turn)
    checkForFiveInARow(gameId, row, col, turn)
    changeTurn(gameId)


def getFormattedBoard(gameId: int) -> str:
    squares = boards[gameId][2:-4].replace("-", "_")
    lines = [" ".join(list(squares[19 * i: 19 * i + 19]) + [str(i+1)]) for i in range(19)]
    lines.append("0 " * 9 + "1 " * 10)
    lines.append(" ".join([str(i % 10) for i in range(1, 20)]))
    return "<br>".join(lines)

def displayWin(gameId: int, player: str):
    boards[gameId] = boards[gameId] + 'c'
    return "hello"

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
    computerMove = Alice.makeMove(gameId)
    doMove(gameId, computerMove[0], computerMove[1])
    return json.dumps({'ID': gameId, 'row': row, 'column': column, 'state': boards[gameId]}) + "<br>" + getFormattedBoard(gameId)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8095, debug=True)