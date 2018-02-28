import logging
import json

from socketcc import SocketCC

logging.basicConfig(format="%s(levelname)s:%(message)s", level=logging.DEBUG)

api_credentials = {"apiKey": "YOUR_API_KEY", "apiSecret": "SECRET"}

COINIGY_SC_ENDPOINT = "wss://sc-02.coinigy.com/socketcluster/"


def your_code_starts_here(socket: SocketCC):
    # Code for subscription
    socket.subscribe('WSTRADE-BTRX--BTC--USDT')  # Channel to be subscribed

    def channel_message(key, data):  # Messages will be received here
        print(f"Data {data} from channel {key}")

    socket.on_channel('WSTRADE-BTRX--BTC--USDT', channel_message)  # This is used for watching messages over channel

    # Code for emit
    def exchanges_response(event_name, error, data):
        print(f"Got ack data {data} and event_name is '{event_name}'")

    socket.emit("exchanges", None, exchanges_response)
    socket.emit("channels", "OK", exchanges_response)


def on_connect(socket: SocketCC):
    logging.info(f"Connected to {socket.url}")


def on_disconnect(socket: SocketCC):
    logging.info(f"Disconnected from {socket.url}")


def on_connection_error(socket: SocketCC, error):
    logging.error(f"Connection error:{error}")


def on_set_auth(socket: SocketCC, token):
    logging.info(f"Received auth token:{token}")
    socket.set_auth_token(token)


def on_auth(socket: SocketCC, is_authenticated):
    logging.info("Authenticated is " + str(is_authenticated))

    def after_authenticated(eventname, error, data):
        print("token is " + json.dumps(data, sort_keys=True))
        your_code_starts_here(socket)

    socket.emit("auth", api_credentials, after_authenticated)


if __name__ == "__main__":
    scc = SocketCC(COINIGY_SC_ENDPOINT)
    scc.set_basic_listener(on_connect, on_disconnect, on_connection_error)
    scc.set_auth_listener(on_set_auth, on_auth)
    scc.set_reconnection(False)
    scc.connect_thread()

    while True:
        if input("Enter 'q' to quit:") == "q":
            break

    scc.disconnect()
