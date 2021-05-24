from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from myrsaV2 import myRSA

#generate a new instance of the myrsaV2class class
rsa = myRSA()
#generate a public/private key pair and then store them
rsa.storeKeyPair()
# Now let's load those keys
#this gives us our public and private key
rsa.loadKeyPair()

def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            """
            #determine whether the message is a key or an actual message
            if msg != None:#TODO add the condition that checks for it being a key
                #it is a symmetric key
                #decrypt the key
                decodedKey = rsa.decKey(msg)
                #save the key to the myrsaV2class instance
                rsa.setKey(decodedKey)
                pass
            else:
                #it is a normal message
                #decrypt the message
                decodedText = rsa.decrypt(msg)
                msg = decodedText
                pass
            """
            print(msg)
            #return msg
        except OSError:  # Possibly client has left the chat.
            break

def send(msg):  # event is passed by binders.
    """Handles sending of messages."""
    #encrypt the message
    #ciphertext = rsa.encrypt(msg)
    if msg == "{quit}":
        client_socket.send(bytes(msg, "utf8"))
        client_socket.close()
    else:
        client_socket.send(bytes(msg, "utf8"))

def on_closing(event=None):
    """This function is to be called when the window is closed."""
    send("{quit}")

# Using Localhost as default IP and port 8000
HOST = "127.0.0.1"
PORT = "8000"
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()

# Send credentials to server for verification
username = input("Enter username: ")
password = input("Enter password: ")

enable_dsa = ''
# Send RSA or DSA choice of encryption to server
while(not("yes" in enable_dsa or "no" in enable_dsa)):
    enable_dsa = input("Enable DSA (yes or no): ")

send("{},{}".format(username,password))
send("{}".format(enable_dsa.lower()))
#send("public key")

while True:
    send(input())
