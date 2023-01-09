import json
import socket
from websocket import create_connection

coinbase_url = "wss://ws-feed.exchange.coinbase.com"

HOST = "127.0.0.1"
PORT = 9090

local_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
local_socket.bind((HOST, PORT))
local_socket.listen(1)

ws = create_connection(coinbase_url)
subscribe_message = {
    "type": "subscribe",
    "product_ids": [
        "ETH-USD",
        "ETH-EUR"
    ],
    "channels": [
        "level2",
        "heartbeat",
        {
            "name": "ticker",
            "product_ids": [
                "ETH-BTC",
                "ETH-USD"
            ]
        }
    ]
}

ws.send(json.dumps(subscribe_message))

conn, addr = local_socket.accept()
print("Connected by", addr)

while True:
    data = ws.recv()
    conn.send(bytes(data + "\n", "ascii"))

ws.close()
local_socket.close()