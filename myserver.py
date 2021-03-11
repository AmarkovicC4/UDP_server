#!/usr/bin/python

import socket 
import datetime as dat
import threading as thread
import time

class UDPServer( object ):
    def __init__( self , ip ,  port , bufSize ):
        self.sock = socket.socket( socket.AF_INET  , socket.SOCK_DGRAM , socket.IPPROTO_UDP )
        self.sock.setsockopt( socket.SOL_SOCKET , socket.SO_REUSEPORT , 1 )
        self.sock.setsockopt( socket.SOL_SOCKET , socket.SO_BROADCAST , 1 )
        self.port = port
        self.ip = ip
        self.bufSize = bufSize
        self.serverThread = None
        self.clientQ = { }

    def listen( self ):
        self.sock.bind( ( self.ip , self.port ) )
        self.serverThread = thread.Thread( name=( 'conversation' + str( self.port ) ) , target=self.conversation )
        self.serverThread.start( )

    def newClient( self , clientID ):
        if self.serverThread:
            self.serverThread.join( )
        
        self.clientQ[ clientID ] = Client( )
        
        if self.serverThread:
            self.serverThread.start( )

    def addMsg( self , clientID , msg , callback ):
        if self.serverThread:
            self.serverThread.join( )
        
        self.clientQ[ clientID ].addMessage( msg , callback )
        
        if self.serverThread:
            self.serverThread.start( )

    def conversation( self ):
        print( "In server conversation" )
        while True:
            name , addr = self.sock.recvfrom( self.bufSize )
            pwd , addr = self.sock.recvfrom( self.bufSize )

            name = name.decode( )
            pwd = pwd.decode( )

            msg = ''
            if name not in self.clientQ:
                msg = "client does not exists"
                print( msg )
                continue

            if pwd not in self.clientQ[ name ].messageQ:
                msg = "pwd not valid"
                print( msg )
                continue

            if not self.clientQ[ name ].clientAddr:
                self.clientQ[ name ].clientAdd = addr

            self.clientQ[ name ].messageQ[ pwd ]( )

    def __del__( self ):
        if self.serverThread:
            self.serverThread.join( )
        self.sock.close( )

class Client( object ):
    def __init__( self ):
        date = dat.datetime.now( )
        self.messageQ = { }
        self.clientName = None
        self.clientAddr = None

    def addMessage( self , msg , callback ):
        self.messageQ[ msg ] = callback

    def close( self ):
        self.clientAddr = "closed"
        date = dat.datetime.now( )

def printCallback(  ):
    print( "Hello World" )

def main( ):
    server = UDPServer( "" , 5005 , 1024 )
    server.newClient( "control4" )
    server.addMsg( "control4" , "Hello C4 + SnapAV" , printCallback )
    server. listen( )
    while True:
        print( "In main function" )
        time.sleep( 1 )

if __name__ == "__main__":
    main( )
