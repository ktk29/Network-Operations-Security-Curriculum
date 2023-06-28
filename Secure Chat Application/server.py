import socket
import threading
import rsa

# connection oriented connections
public_key, private_key = rsa.newkeys(1024)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 9090))
# ready to accept user join requests
server.listen()

users = []
keys = []
names = []


# sends a message to all users, encrypting each with the individual key
def broadcast(message):
    for user, key in zip(users, keys):
        user.send(rsa.encrypt(message.encode(), key))


# add new user
def add_new_user():
    # keep looking
    while True:
        user, _ = server.accept()
        # print user just joined the chatroom
        users.append(user)
        # exchange user keys
        user.send(public_key.save_pkcs1("PEM"))
        keys.append(rsa.PublicKey.load_pkcs1(user.recv(1024)))

        # get users name
        user.send(rsa.encrypt("name".encode(), keys[-1]))
        names.append(rsa.decrypt(user.recv(1024), private_key).decode())

        # let users know that a new user has been added to the chat
        broadcast(f"{names[-1]} has just joined the chatroom\n")

        threading.Thread(target=handle, args=(user,)).start()


def handle(user):
    index = users.index(user)
    while True:
        try:
            message = rsa.decrypt(user.recv(1024), private_key).decode()
            broadcast(message)

        # if no connection is possible, remove user
        except:
            users.remove(user)
            user.close()
            keys.remove(keys[index])
            broadcast(f"{names[index]} has left the chat")
            names.remove(names[index])

add_new_user()
