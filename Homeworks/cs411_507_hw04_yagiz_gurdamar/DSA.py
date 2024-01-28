# use "pip install sympy" if pyprimes is not installed
# use "pip install pycryptodome" if pycryptodome is not installed
import random
import sympy
import warnings
from Crypto.Hash import SHA3_256
from Crypto.Hash import SHAKE128

def egcd(a, b):
    x,y, u,v = 0,1, 1,0
    while a != 0:
        q, r = b//a, b%a
        m, n = x-u*q, y-v*q
        b,a, x,y, u,v = a,r, u,v, m,n
    gcd = b
    return gcd, x, y

def modinv(a, m):
    if a < 0:
        a = a+m
    gcd, x, y = egcd(a, m)
    if gcd != 1:
        return None  # modular inverse does not exist
    else:
        return x % m
    
def random_prime(bitsize):
    warnings.simplefilter('ignore')
    chck = False
    while chck == False:
        p = random.randrange(2**(bitsize-1), 2**bitsize-1)
        chck = sympy.isprime(p)
    warnings.simplefilter('default')    
    return p

def large_DL_Prime(q, bitsize):
    warnings.simplefilter('ignore')
    chck = False
    while chck == False:
        k = random.randrange(2**(bitsize-1), 2**bitsize-1)
        p = k*q+1
        chck = sympy.isprime(p)
    warnings.simplefilter('default')    
    return p

def Param_Generator(qsize, psize):
    q = random_prime(qsize)
    p = large_DL_Prime(q, psize-qsize)
    tmp = (p-1)//q
    g = 1
    while g == 1:
        alpha = random.randrange(1, p)
        g = pow(alpha, tmp, p)
    return q, p, g

# Generating private-public key pair
def Key_Gen(q, p, g):
    s = random.randint(1, q) # private key
    h = pow(g, s, p)         # public key
    return s, h

# Signature generation
def Sig_Gen(message, a, k, q, p, g):
    shake = SHAKE128.new(message)
    h = int.from_bytes(shake.read(q.bit_length()//8), byteorder='big')
    r = pow(g, k, p)%q
    s = (modinv(k, q)*(h+a*r))%q
    return r, s

# Signature verification
def Sig_Ver(message, r, s, beta, q, p, g):
    shake = SHAKE128.new(message)
    h = int.from_bytes(shake.read(q.bit_length()//8), byteorder='big')
    u1 = (modinv(s, q)*h)%q
    u2 = (modinv(s, q)*r)%q
    v1 = (pow(g, u1, p)*pow(beta, u2, p)%p)%q

    if v1 == r:
        return True
    else:
        return False

# Test
print("Testing the DSA signature generation and verification")
# Generate domain parameters (q, p, g)
q, p, g = Param_Generator(224, 2048)
print("q =", q)
print("p =", p)
print("g =", g)

# Generate private-public key pairs for a user
a, beta = Key_Gen(q, p, g)
print("secret key (a):", a)
print("public key (beta):", beta)

message = b'Hello World!'
k = random.randint(0, q-1)
r, s = Sig_Gen(message, a, k, q, p, g)

if Sig_Ver(message, r, s, beta, q, p, g):
    print("signature verifies:) ")
else:
    print("invalid signature:( ")    




from Crypto.Hash import SHAKE128

def hash_message(message, q):
    shake = SHAKE128.new(message)
    return int.from_bytes(shake.read(q.bit_length()//8), byteorder='big')

# Given values
q = 18055003138821854609936213355788036599433881018536150254303463583193
r1 = 16472915699323317294511590995572362079752105364898027834238409547851
s1 = 959205426763570175260878135902895476834517438518783120550400260096
r2 = 14333708891393318283285930560430357966366571869986693261749924458661
s2 = 9968837339052130339793911929029326353764385041005751577854495398266
message1 = b'The grass is greener where you water it.'
message2 = b'Sometimes you win, sometimes you learn.'

# Hash the messages
h1 = hash_message(message1, q)
h2 = hash_message(message2, q)

# Solve for a
# (s1 * s2^(-1)) * h1 + (s1 * s2^(-1)) * a * r1 = h2 + a * r2
# rearrange for a
a = ((h2 - (s1 * modinv(s2, q) * h1) % q) * modinv((r2 - (s1 * modinv(s2, q) * r1) % q) % q, q)) % q

print("Recovered secret key (a):", a)

