# 
# Mingzhe Huang, 4044090
# CS 456/656 Assginment 1
# This is the file for server side
#

import sys,os
import socket

class Server():
    
    # TCP use SOCK_STREAM, UDP use SOCK_DGRAM
    def __init__(self,req_code):
        self.message = ""
        self.req_code = req_code
        self.tcp_negotiation_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.udp_transaction_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
        # use parameter ('',0) to bind tcp socket and udp socket to free ports.
        # get the tcp port number and assign that to n_port
        self.tcp_negotiation_socket.bind(('', 0))  
        self.tcp_negotiation_socket.listen(1)
        self.udp_transaction_socket.bind(('', 0))
        self.n_port = self.tcp_negotiation_socket.getsockname()[1]
        self.r_port = self.udp_transaction_socket.getsockname()[1]
        # print the server_port message
        print("SERVER_PORT=" + str(self.n_port))
    
    def negotiate(self):
        while True:
            client_socket, address = self.tcp_negotiation_socket.accept()
            client_req_code = int(client_socket.recv(1024))
            # if req_codes do not match, set the port to be reserved 0
            # client will terminate after receiving it.
            if client_req_code != self.req_code:
                client_socket.send("0".encode('utf-8'))
            # if req_code matches, send the client r_port. call function receive_reverse_send_message.
            else:
                print('r_port: ', self.r_port)
                client_socket.send(str(self.r_port).encode('utf-8'))
                self.receive_reverse_send_message()
            # close this tcp socket
            client_socket.close()
            
    def receive_reverse_send_message(self):
        # receive msg from client
        msg, client_address = self.udp_transaction_socket.recvfrom(1024)
        msg = msg.decode('utf-8')
        client_address = client_address
        # reverse the message
        reversed_msg = msg[::-1]
        # print("send reversed message: ",reversed_msg)
        # send reversed msg to client
        self.udp_transaction_socket.sendto(reversed_msg.encode('utf-8'),client_address)
        exit(1)

    

def main():
    """Negotiates a random port with clients to transact messages.
    Checks if request code was determined in a command line argument.
    Listens for client requests for negotiations.
    Negotiates a TCP port with a client over UDP, and then conducts a
    transaction with the client over said TCP port.
    Command Line Args:
        req_code: the request code that client requests will be checked
            against.
    Raises:
        IndexError: If no request code was determined in the command line
            argument.
        ValueError: If the request code determined is not an integer.
    """
    # use try - except to throught errors
    try:
        req_code = int(sys.argv[1])
    except IndexError:
        print("MISSING PARAMETER: <req_code>")
        sys.exit(1)
    except ValueError:
        print("<req_code> MUST BE INTEGER, TRY AGAIN")
        sys.exit(1)
    # n_socket = create_socket(socket.SOCK_DGRAM, "SERVER_PORT")
    # while True:
    server = Server(req_code)
    server.negotiate()



        

if __name__ == "__main__":
    main()