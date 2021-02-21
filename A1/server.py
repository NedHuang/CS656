# -*- coding: utf-8 -*-
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
        # exit(1)

    

def main():
    """
    Stage 1:
    Negotiation using TCP sockets. If the req_code matches with client's req_code, server will send r_port to client and close tcp connection.
    Otherwise, server will terminate TCP connection

    Stage 2:
    Transaction using UDP sockets. Client creates a UDP socket to the server in <r_port> and sends the <msg> containing a string.
    When the server receives the string it sends the reversed string back to the client. Once received, the client prints out the reversed string and exits.
    """
    # use try - except to throught errors
    try:
        req_code = int(sys.argv[1])
    except IndexError:
        print("MISSING PARAMETER: <req_code>")
        sys.exit(1)
    except ValueError:
        print("<req_code> SHOULD BE INTEGER")
        sys.exit(1)
    # n_socket = create_socket(socket.SOCK_DGRAM, "SERVER_PORT")
    # while True:
    server = Server(req_code)
    server.negotiate()



        

if __name__ == "__main__":
    main()