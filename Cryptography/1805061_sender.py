# first of all import the socket library
import socket 
Diffie_Hellman = __import__('1805061_Diffie_Hellman')  
AES = __import__('1805061_AES')

print("Input k, min, max (in separate lines):")
k = int(input())
min = int(input())
max = int(input())


p = Diffie_Hellman.get_safe_mod(k)
g = Diffie_Hellman.get_base(min, max, p)
a = Diffie_Hellman.get_private_key(k)
A = Diffie_Hellman.get_public_key(g, a, p)

# next create a socket object
soc = socket.socket()        
print ("Socket successfully created")
 
# reserve a port on your computer
port = 12369             
 
# Next bind to the port
# we have not typed any ip in the ip field
# instead we have inputted an empty string
# this makes the server listen to requests
# coming from other computers on the network
soc.bind(('', port))        
print ("socket binded to %s" %(port))
 
# put the socket into listening mode
soc.listen(5)    
print ("socket is listening")           
 
# a forever loop until we interrupt it or
# an error occurs
while True:
    # Establish connection with client.
    s, addr = soc.accept()    
    print ('Got connection from', addr )
    # Breaking once connection closed
    break


s.send(str(k).encode())
s.recv(1024).decode()

s.send(str(p).encode())
s.recv(1024).decode()

s.send(str(g).encode())
s.recv(1024).decode()

s.send(str(A).encode())
s.recv(1024).decode()

B = int((s.recv(1024).decode()))
s.send("Recieved".encode())

# Calculating key
key = Diffie_Hellman.get_key(B, a, p)
AES.make_round_key(key)
s.recv(1024).decode()

# Sending encrypted file
print("Sending File...")
file = open('sender.txt' , 'r')
while True:
    chunk = file.read(16)
    if len(chunk) == 0 :
        s.send(''.encode())
        break
    s.send(AES.get_cipher_text(chunk).encode())
print("Sending File Done...")
file.close()

# Close the connection with the client
s.close()