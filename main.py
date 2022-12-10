from MessageParser import MessageParser
from OrderBook import OrderBook
import websockets
import asyncio
import json

# url to connect to the websocket
socketURL = 'wss://ws-feed.exchange.coinbase.com'

# create the orerbook and message parser
ob = OrderBook()
mp = MessageParser()

# main event loop to subscribe to the websocks and recieve messages
async def eventLoop(ticker = "BTC-USD"):
    async with websockets.connect(socketURL) as websocket:
        subscriptionMessage = json.dumps(
                { 
                  "type": "subscribe", 
                  "product_ids": [ticker],
                  "channels": ["full"] 
                })

        # subscribe to orderbook
        await websocket.send(subscriptionMessage)

        # check that subscription was a success, else exit
        confResp = json.loads(await websocket.recv())
        if confResp["type"] == "error":
            print(confResp["message"])
            print(confResp["reason"])
            return

        # receive a message, parse it into an order, execute the order
        while True:
            msgJson = await websocket.recv()
            msg = json.loads(msgJson)
            order = mp(msg)

            # if we have a valid order
            if order != None:
                ob.processMessage(order)

if __name__ == "__main__":
    try:
        asyncio.run(eventLoop())
    except:
        print("Exiting Orderbook")
        
