#!python3
#-*-coding:utf-8-*-
import socket,argparse

def recvall(sock,length):
    data = b''
    while len(data) <length:
        more = sock.recv(length - len(data))
        if not more:
            raise EOFError('%d %d'%(length,len(data)))
        data += more
    return data

def server(interface,port):
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    sock.bind((interface,port))
    sock.listen(1)
    print('listen at ',sock.getsockname)
    while True:
        sc,sockname = sock.accept()
        print('we have accept a connection from',sockname)
        print('socket name:',sc.getsockname())
        print('socket peer:',sc.getpeername())
        message = recvall(sc,16)
        print('incoming 16 message:',repr(message))
        sc.sendall(b'hello my friend~')
        sc.close()
        print('socket closed')

def client(host,port):
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect((host,port))
    print('socket name:',sock.getsockname())
    sock.sendall(b'hello server~~~~')
    reply = recvall(sock,16)
    print('server said:',repr(reply))
    sock.close()

if __name__ == '__main__':
    choise = {'client':client,'server':server}
    parser = argparse.ArgumentParser(description = 'Send and receive over TCP')#创建一个命令行解析处理器
    parser.add_argument('role',choices = choise,help = 'which role to play')#定义了一个必选参数role
    parser.add_argument('host',help = 'interface the server listens at;''host the client sends to')#定义了一个必选参数host
    parser.add_argument('-p',metavar = 'PORT',type = int,default = 1060,help = 'TCP port (default 1060)')#定义了一个可选参数p(-x --xxxx都代表可选参数，只不过前者只能单个字母，后者是长单词)
    args = parser.parse_args()
    function = choise[args.role]
    function(args.host,args.p)
