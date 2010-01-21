import socket

class irc:
    def __init__(self, host, port, nickname, ident="pyB", realname="pyB", autojoinchans="#night_bar,#sliven,#hades", debug = False):
        self.host = host
        self.port = int(port)
        self.ident = ident
        self.nickname = nickname
        self.realname = realname
        self.autojoinchans = autojoinchans
        self.clientsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ping_count = 0
        self.data_received_handler = None
        self.debug = debug
    def srvsend(self, servermsg):
        self.clientsock.send(servermsg)
    def server_send(self, servermsg):
        self.clientsock.send(servermsg)

    def ircinit(self):
        self.clientsock.send('NICK ' + self.nickname + '\r\n')
        self.clientsock.send('USER ' + self.ident + ' 8 * : ' + self.realname + ' \r\n')

    def connect(self):
        self.clientsock.connect((self.host, self.port))
        self.ircinit()
        self.connLoop()

    def disconnect(self):
        self.clientsock.close()

    def connLoop(self):
        while 1:
            replytosrv = ""
            data = self.clientsock.recv(1024)
            if not data: break
            replytosrv = self.onEvent(data)
            if self.debug:
                print replytosrv

    def pongToServer(self, pongstring):
        self.clientsock.send('PONG '+ pongstring +' \n')
        if self.debug:
            print "PONG"
        if self.ping_count == 0:
            self.autojoin()
        self.ping_count = self.ping_count + 1

    def onEvent(self, data):
        arrdata = []
        for word in data.split(' '):
            arrdata.append(word)
        if arrdata[0] == 'PING':
            self.pongToServer(arrdata[1])
        if self.data_received_handler:
            self.data_received_handler(data)
        if self.debug:
            print data

        return "ok"
    def autojoin(self):
        for chan in self.autojoinchans.split(','):
            self.server_send('JOIN '+ chan + " \n")


