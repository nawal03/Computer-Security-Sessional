import random
import time

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

def get_safe_mod(k):
    """
     - returns at least k bit prime number p, where (p-1)/2 is also a prime
    """
    p = (1<<(k-1))+1
    while not (is_prime(p) and is_prime((p-1)//2)):
        p+=2
    return p

def get_base(min, max, p):
    """
        - returns a primitive root of p in the range [min, max]
        - if not found, returns -1 
    """
    for g in range(min, max+1):
        if pow(g, 2, p) != 1 and pow(g, (p-1)//2, p) != 1:
            return g
    return -1

def get_private_key(k):
    """
        - returns a prime of at least k/2 bits
    """
    a = (1<<(k>>1)) + random.randrange(1, 100000)     # (k+1)>>1 ----> ceil(k/2) 
    while not is_prime(a):
        a+=1
    return a

def get_public_key(g, a, p):
    return pow(g, a, p)

def get_key(A, b, p):
    num = pow(A, b, p)
    # dec to bin to char
    key = ''
    ch = 0
    shift = 0
    while num != 0:
        ch *= 2
        ch += (num%2)
        num//=2
        shift += 1
        if shift == 8:
            key+=chr(ch)
            shift = 0
            ch = 0

    if ch != 0:
        key+=chr(ch)

    return key


# #Input
# print("Input k, min, max : ")
# k = int(input())
# min = int(input())
# max = int(input())


# #Generate a large prime p which is at least k bits long, take k as parameter.
# mod_finding_time = 0
# for i in range(5):
#     start_time = time.time()
#     p = get_safe_mod(k)
#     mod_finding_time += time.time()-start_time
# mod_finding_time/=5


# #Find a primitive root g for mod p. Take two parameters – min and max – both less than p. 
# # Then g should be in the range [min,max].
# base_finding_time = 0
# for i in range(5):
#     start_time = time.time()
#     g = get_base(min, max, p)
#     base_finding_time += time.time()-start_time
# base_finding_time/=5


# #Take two more primes – a and b – both at least (k/2) bits long. 
# private_key_finding_time = 0

# for i in range(5):
#     start_time = time.time()
#     a = get_private_key(k)
#     private_key_finding_time += time.time()-start_time

# for i in range(5):
#     start_time = time.time()
#     b = get_private_key(k)
#     private_key_finding_time += time.time()-start_time

# private_key_finding_time/=10

    
# #Compute A = g^a (mod p) and B = g^b (mod p).
# public_key_finding_time = 0

# for i in range(5):
#     start_time = time.time()
#     A = get_public_key(g, a, p)
#     public_key_finding_time += time.time()-start_time
    
# for i in range(5):
#     start_time = time.time()
#     B = get_public_key(g, b, p)
#     public_key_finding_time += time.time()-start_time

# public_key_finding_time/=10


# #Compute A^b (mod p) and B^a (mod p). Verify that they are equal.
# key_finding_time = 0

# for i in range(5):
#     start_time = time.time()
#     key1 = get_key(A, b, p)
#     key_finding_time += time.time()-start_time
    
# for i in range(5):
#     start_time = time.time()
#     key2 = get_key(B, a, p)
#     key_finding_time += time.time()-start_time

# key_finding_time/=10

# print("Computation Time Summary")
# print("k = ", k)
# print("p = ", p, " time = ", mod_finding_time, " s")
# print("g = ", g, " time = ", base_finding_time, " s")
# print("a = ", a, " b = ", b, " time = ", private_key_finding_time, " s")
# print("A = ", A, " B = ", B, " time = ", public_key_finding_time, " s")
# print("key1 = ", key1, " key2 = ", key2, " time = ", key_finding_time, " s")



