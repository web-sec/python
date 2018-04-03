import socket
if __name__ == '__main__':
    hostname = 'www.wufan.com'
    addr = socket.gethostbyname(hostname)
    print('the IP address of {} is {}'.format(hostname,addr))
