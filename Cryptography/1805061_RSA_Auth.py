import random

def pow(n, x, p):
    """
        - calculated n^x mod p in O(logx) 
    """
    if x == 0: 
        return 1
    ret = pow(n, x>>1, p)%p
    ret = (ret * ret)%p

    if x % 2 == 1:
        ret = (ret * n)%p
    return ret

def miller_test(n, d, a):
    """
        - return true maybe prime
        - return false composite
    """
    x = pow(a, d, n)
    
    if x == 1 or x == n-1:
        return True
    while d != n-1:
        x = (x*x) % n
        if x == 1: 
            return False
        if x == n-1:
            return True
        d<<=1
    return False

def is_prime(n):
    """
        - Miller Rabin primality test
    """
    if n < 2:
        return False
    if n == 2:
        return True
    if  n % 2 == 0:
        return False
    
    d = n-1

    while d % 2 == 0:
        d>>=1

    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]

    for a in primes:
        if not miller_test(n, d, a):
            return False
        
    return True

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = extended_gcd(b % a, a)
        return gcd, y - (b // a) * x, x

def inverse_mod(a, mod):
    g, x, y = extended_gcd(a, mod)
    if g != 1:
        raise Exception('modular inverse is non existent')
    else:
        return x % mod

def get_factor(k):
    n = (1<<k)+random.randrange(1, (1<<(k//2)))
    while not is_prime(n):
        n+=1
    return n

def get_keys(p, q):
    n = p * q
    phi = (p-1) * (q-1)

    g = -1
    while g != 1:
        e = random.randrange(2,phi)
        g = gcd(e, phi)
    
    d = inverse_mod(e, phi)
    return (e,n),(d,n)  # public_key, private_key

def encrypt(text, keys, type):
    key, n = keys
    cipher_text = []
    for c in text:
        if type == 0:
            cipher_text.append(pow(ord(c), key, n))
        else:
            cipher_text.append(pow(c, key, n))
    return cipher_text

def decrypt(cipher_text, keys, type):
    key, n = keys
    if type == 0:
        deciphered_text = ''
    else:
        deciphered_text = []
    for c in cipher_text:
        if type == 0:
            deciphered_text += chr(pow(c, key, n))
        else:
            deciphered_text.append(pow(c, key, n))
    return deciphered_text

####start####

print("Input k : ")

k = int(input())

# Alice is sender, Bob is receiver
# For Alice
p_a = get_factor(k//2)
q_a = get_factor(k//2)

public_key_a , private_key_a = get_keys(p_a, q_a)

# For Bob
p_b = get_factor(k//2)
q_b = get_factor(k//2)

public_key_b , private_key_b = get_keys(p_b, q_b)

print("Input text : ")

text = input()

# Text will be encrypted twice, one with Bob's public key (for security), another with Alice's private key (for authentication)
cipher_text = encrypt(encrypt(text, public_key_b, 0), private_key_a, 1)
deciphered_text = decrypt(decrypt(cipher_text, public_key_a, 1), private_key_b, 0)

print("Cipher text : ", cipher_text)
print("Deciphered text : ", deciphered_text)


