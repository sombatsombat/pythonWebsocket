###############################################################################
#
# The MIT License (MIT)
#
# Copyright (c) Tavendo GmbH
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
###############################################################################

from autobahn.twisted.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory
import json
import psycopg2
import psycopg2.extras
import ast




class MyServerProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))
            self.processMessage( payload, isBinary )

        # echo back message verbatim
        #aString = "Hello " + payload
        #self.sendMessage(aString, isBinary)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))

    def processMessage (self, payload, isBinary ):
        
        if ( payload == "Sombat") :
            self.sendMessage("Hello " + payload, isBinary)
        else:
            self.sendMessage("You are not Sombat",isBinary)
        aSql = """
            select "remoteName" as remotename, "buttonData"->'button'->>'volup' as avolup,"buttonData" 
            from "infraredRF_data"
            where "remoteName" = """
            
        aSql = aSql + "'" + payload + "'"

        print aSql
        cur.execute(aSql)
    
        for row in cur.fetchall():
             print row['remotename'],row['buttonData'],row['avolup'],type(row['avolup'])
             aList = ast.literal_eval(row['avolup'])
             for element in aList:
                 print element 

    

if __name__ == '__main__':

    import sys

    from twisted.python import log
    from twisted.internet import reactor

    #conn = psycopg2.connect("dbname=uniart4_pr host=localhost user=user password=password")
    conn = psycopg2.connect('dbname=infraredRF')
    #cur = conn.cursor()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("""
    select "remoteName", "buttonData"->'button'->>'volup' as avolup,"buttonData" from "infraredRF_data"
    """)

    #for row in cur.fetchall():
    #     print row['remoteName'],row['buttonData'],row['avolup']


    log.startLogging(sys.stdout)

    factory = WebSocketServerFactory(u"ws://127.0.0.1:9111", debug=True)
    #factory = WebSocketServerFactory(u"ws://192.168.1.161:9111", debug=True)
    factory.protocol = MyServerProtocol
    # factory.setProtocolOptions(maxConnections=2)

    reactor.listenTCP(9111, factory)
    reactor.run()

