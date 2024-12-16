from websockets.sync.client import connect
import json
import time
import threading
import concurrent.futures

# Une connexion permise par compte, donc laissez a 1 thread
THREADS = 1

# VOS COORDONNÉES
X_INIT = -694
Y_INIT = -699

TOKEN_JWT = "VOTRE_TOKEN_ICI"
WS_TIMEOUT = 4  # timeout operations websocket
MESSAGE_DELAY_SECOND = 0.05

ASCII_ART = """
        _
    __-/ \_                   _________
   /       \                _/   \  \  \\_
  /         |/\            /              \
 /             \          /|               \
 /   _          |         |                 |
|   / \_   /--\ \         \                 |
|  /    \//   \ |          \|_\_\\\         /
\ /            \|           /      \       |
 \|   -_   _-   H          /        \      |
 \|   -=  |=-   |          |    _   \      /
  C    _  \_    D          |  _/    |     |
  |   (n| |h)  |           |\/%/    |     /
   \    \_/    /           k|Y       \/\ |
   |          /            /_         '% /
    \ (--==-) |           /_>}          \|
     \       /              |____/^|    /
      \  __ /              __ii++-/     |
       |    |               \     _     /
       |    |               |___-- \    |
       |    |                       |   |"""

index_counter = 0
index_lock = threading.Lock()


def get_ascii_vals():
    """
    Retourne les prochaines valeurs a envoyer
    x, y, value
    """
    ascii_lines = ASCII_ART.strip().split("\n")
    global index_counter

    with index_lock:
        current_index = index_counter
        index_counter += 1

        total_chars = sum(len(line) for line in ascii_lines)
        index_counter %= total_chars

    char_count = 0
    for y, line in enumerate(ascii_lines):
        if char_count + len(line) > current_index:
            x = current_index - char_count
            return x, y, ascii_lines[y][x]
        char_count += len(line)

    raise RuntimeError("Index calculation error. This should never happen.")


def substract_counter():
    with index_lock:
        index_counter -= 1


def wait_response(websocket):
    """
    Attendre une reponse du serveur websocket
    """
    response = websocket.recv()
    print(f"Received: {response}")


def send_hello(websocket):
    """
    Faire le handshake websocket
    """
    stomp_message = f"CONNECT\nAuthorization:{TOKEN_JWT}\naccept-version:1.2,1.1,1.0\nheart-beat:10000,10000\n\n\0"

    websocket.send(stomp_message)
    print("sent hello!")


def send_message(websocket, x, y, msg):
    """
    Envoyer un message websocket
    """
    payload = {"x": x, "y": y, "value": msg}
    payload_str = json.dumps(payload, separators=(",", ":"), ensure_ascii=False)
    content_len = len(payload_str.encode("utf-8"))

    message = f"SEND\ndestination:/app/map/set\ncontent-length:{content_len}\n\n{payload_str}\0"

    print(f"\n{message}\n")
    websocket.send(message)


def connect_and_send():
    burp0_url = "wss://aywenito.textboard.fr:25555/ws"

    while True:
        try:
            with connect(burp0_url, open_timeout=WS_TIMEOUT) as websocket:
                websocket.socket.settimeout(WS_TIMEOUT)
                send_hello(websocket)
                wait_response(websocket)

                while True:
                    x, y, val = get_ascii_vals()
                    x += X_INIT
                    y += Y_INIT
                    send_message(websocket, x, y, val)
                    time.sleep(MESSAGE_DELAY_SECOND)
        except KeyboardInterrupt:
            exit()
        except Exception as e:
            substract_counter()
            print(f"thread error. {str(e)}")
            time.sleep(0.01)
            continue


def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=THREADS) as executor:
        futures = [executor.submit(connect_and_send) for _ in range(THREADS)]

        for future in futures:
            future.result()


while True:
    try:
        main()
    except KeyboardInterrupt:
        exit()

    except Exception as e:
        print(f"Program error. {str(e)}")
        continue
