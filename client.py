import socket
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host=socket.gethostname()
port=5002
def print_board(board):
    print("\n   0   1   2")
    print("     |   |   ")
    print("0  "+board[0][0]+" | "+board[0][1]+" | "+board[0][2])
    print("  ---|---|---")
    print("1  "+board[1][0]+" | "+board[1][1]+" | "+board[1][2])
    print("  ---|---|---")
    print("2  "+board[2][0]+" | "+board[2][1]+" | "+board[2][2])
    print("     |   |   \n")
def start_game():
    invitation=s.recv(1024)
    print(invitation.decode())
    name=input("Enter your name:")
    s.send(name.encode())
    while True:
            data=s.recv(1024).decode()
            if data=="takeInput":
                check=True
                while check:
                    position=input("Enter the position: ")
                    a,b=map(int,position.split())
                    position=f"{a} {b}"
                    s.send(position.encode())
                    check=False
            elif data=="\tBoard":
                print(data)
                board=s.recv(1024).decode()
                print_board(eval(board))
            elif data=="":
                break
            else:
                print(data)
def start_player():
    s.connect((host,port))
    print("Connected to:",host,":",port)
    start_game()
    s.close()
start_player()