# Import socket module
import socket            
Diffie_Hellman = __import__('1805061_Diffie_Hellman')  
AES = __import__('1805061_AES')          


# Create a socket object
s = socket.socket()        

# Define the port on which you want to connect
port = 12369            
 
# connect to the server on local computer
s.connect(('127.0.0.1', port))
 
# receive data from the server and decoding to get the string.
k = int((s.recv(1024).decode()))
s.send("Recieved".encode())

p = int((s.recv(1024).decode()))
s.send("Recieved".encode())

g = int((s.recv(1024).decode()))
s.send("Recieved".encode())

A = int((s.recv(1024).decode()))
s.send("Recieved".encode())


b = Diffie_Hellman.get_private_key(k)
B = Diffie_Hellman.get_public_key(g, b, p)

s.send(str(B).encode())
s.recv(1024).decode()

# Calculating key
key = Diffie_Hellman.get_key(A, b, p)
AES.make_round_key(key)
s.send("Ready".encode())

# Recieving encrypted file
file = open('receiver.txt' , 'w')
print("Receiving File...")
while True:
    chunk = s.recv(1024).decode()
    if len(chunk) == 0:
        break
    chunk = AES.get_plain_text(chunk)
    file.write(chunk)
print("Receiving File Done...")
file.close()

# Close the connection with the server
s.close()  