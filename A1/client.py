# -*- coding: utf-8 -*-
# 
# Mingzhe Huang, 4044090
# CS 456/656 Assginment 1
# This is the file for client side
#


import os, sys
import socket


class Client:
    def __init__(self, server_address, n_port, req_code):
        self.tcp_negotiation_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.udp_transaction_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # port 0 is reserved in TCP/IP. If the port isnot changed, terminate the program
        self.r_port = 0
        try:
            self.tcp_negotiation_socket.connect((server_address, n_port))
        except:
            print("UNABLE TO NEGOTIATE WITH SERVER")
            exit(1)
        self.r_port = self.negotiation(req_code)

    # Negotiate with the server. Using the req_code to validate the connection.
    # If the req_code doesn't match, then client should terminate.
    def negotiation(self, req_code):
        self.tcp_negotiation_socket.send(req_code.encode())
        r_port = self.tcp_negotiation_socket.recv(1024).decode()
        r_port = int(r_port)
        # r_port is 0 means req_code doesn't match
        
        if r_port == 0:
            print("INVALID <req_code>")
            self.tcp_negotiation_socket.close()
            self.udp_transaction_socket.close()
            sys.exit(1)
        else:
            # close TCP connection after receiving r_port
            return int(r_port)
            self.tcp_negotiation_socket.close()

    # Retrieve and print all existing stored msg from the server through UDP.
    def send_and_receive_msg(self, server_address,msg):
        self.udp_transaction_socket.sendto(msg.encode('utf-8'), (server_address, self.r_port))
        reversed_msg, addr = self.udp_transaction_socket.recvfrom(2048)
        reversed_msg = reversed_msg.decode('utf-8')
        # close the udp connection and print result after receiving reversed msg
        self.udp_transaction_socket.close()
        print(str(reversed_msg))
        sys.exit(1)


def main():
    """
    Stage 1:
    Negotiation using TCP sockets. If the req_code matches with server's req_code, server will send r_port to client and close tcp connection.
    Otherwise, server will terminate TCP connection

    Stage 2:
    Transaction using UDP sockets. Client creates a UDP socket to the server in <r_port> and sends the <msg> containing a string.
    When the server receives the string it sends the reversed string back to the client. Once received, the client prints out the reversed string and exits.
    """

    if len(sys.argv) != 5:          # Valid the number of input arguments.
        print("There should be 4 parameters: <server_address>, <n_port>, <req_code>, and <msg>")
        sys.exit(1)
    else:
        # read variables from argv
        server_address = sys.argv[1]
        n_port = int(sys.argv[2])
        req_code = sys.argv[3]
        msg = sys.argv[4]

        # create an object of client and call send_and_reveive_msg function
        client = Client(str(server_address), n_port, req_code)
        client.send_and_receive_msg(str(server_address),msg)
        sys.exit(1)


if __name__ == '__main__':
    main()