import socket
import time
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host=socket.gethostname()
port=5002
board=[[' ']*3 for _ in range(3)]
players=[[None,None,None] for _ in range(2)]
def check_input(a,b,c):
    if a>2 or b>2 or a<0 or b<0:
        print("The player's input is out of bound! Try again.")
        c.send("Your input is out of bound! Try again.".encode())
        return False
    elif board[a][b]!=' ':
        print("The player's input is already entered! Try again.")
        c.send("This position is already entered! Try again.".encode())
        return False
    return True
def send_both(message):
    for player in players:
        player[0].send(message.encode())
    time.sleep(0.01)
def take_input(currentPlayer):
    player=f"Player {currentPlayer}'s ({players[currentPlayer-1][1]}) turn to play"
    c,name,a=players[currentPlayer-1]
    print(player)
    send_both(player)
    check=True
    while check:
        c.send("takeInput".encode())
        data=c.recv(1024).decode().split(" ")
        a=int(data[0])
        b=int(data[1])
        if check_input(a,b,c):
            board[a][b]='X' if currentPlayer==1 else 'O'
            check=False
            send_both("\tBoard")
            send_both(str(board))
def check_winner():
    for row in board:
        if all(cell=='X' for cell in row) or all(cell=='O' for cell in row):
            return True
    for col in range(3):
        if all(board[row][col]=='X' for row in range(3)) or all(board[row][col]=='O' for row in range(3)):
            return True
    if board[0][0]==board[1][1]==board[2][2]=='X' or board[0][2]==board[1][1]==board[2][0]=='X' or board[0][0]==board[1][1]==board[2][2]=='O' or board[0][2]==board[1][1]==board[2][0]=='O':
        return True
    return False
def start_game():
    result=False
    i=0
    while i<=8 and not result:
        take_input(i%2+1)
        result=check_winner()
        i+=1
    if result:
        players[((i%2)+1)%2][0].send(f"You ({players[((i%2)+1)%2][1]}) are the winner of the match".encode())
        players[i%2][0].send(f"Your opponent ({players[((i%2)+1)%2][1]}) is the winner of the match".encode())
        if i%2:
            message=f"Player One ({players[0][1]}) is the winner of the match"
        else:
            message=f"Player Two ({players[1][1]}) is the winner of the match"
    else:
        message = "It is a Draw"
        send_both(message)
    print(message)
    for player in players:
        player[0].close()
def accept_players():
    invitation="Welcome to the Tic Tac Toe Game"
    for i in range(2):
        c,a=s.accept()
        c.send(invitation.encode())
        name=c.recv(1024).decode()
        players[i]=[c,name,a]
        print(f"Player {i + 1} ({name}) joined [{a[0]}:{str(a[1])}]")
        c.send(f"Hey {name}, you are player {i + 1}".encode())
        if(i==0):
            c.send("Your symbol is X".encode())
        else:
            c.send("Your symbol is O".encode())
    start_game()
    s.close()
def start_server():
    s.bind((host,port))
    s.listen(2)
    print("Tic Tac Toe Game server started")
    print("Binded to port",port)
    accept_players()
start_server()