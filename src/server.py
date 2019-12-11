

from twisted.internet import protocol, reactor, endpoints
from twisted.internet.protocol import ServerFactory, connectionDone
from twisted.protocols.basic import LineOnlyReceiver


class ServerProtocol(LineOnlyReceiver):
    factory: 'Server'
    login: str = None

    def connectionMade(self):
        self.factory.clients.append(self)

    def connectionLost(self, reason=connectionDone):
        self.factory.clients.remove(self)

    def lineReceived(self, line: bytes):
        content = line.decode()

        if self.login is not None:

            content = f"Message from {self.login}: {content}"
            for user in self.factory.clients:
                if user is not self:
                    user.sendLine(content.encode())
        else:
            # login:admin -> admin
            if content.startswith("login:"):
                self.login = content.replace("login:", "")
                self.sendLine("Welcome!".encode())
            else:
                self.sendLine("Invalid login".encode())


class Server(ServerFactory):
    protocol = ServerProtocol
    clients: list

    def startFactory(self):
        self.clients = []
        print("Server Started")

    def stopFactory(self):
        print("Server stopped")


reactor.listenTCP(1234, Server())
reactor.run()
