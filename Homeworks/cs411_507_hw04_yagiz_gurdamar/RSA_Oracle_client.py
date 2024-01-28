import random
import requests
from random import randint
import math

API_URL = 'http://harpoon1.sabanciuniv.edu:9999'
my_id = 22534


def egcd(a, b):
    x,y, u,v = 0,1, 1,0
    while a != 0:
        q, r = b//a, b%a
        m, n = x-u*q, y-v*q
        b,a, x,y, u,v = a,r, u,v, m,n
    gcd = b
    return gcd, x, y

def modinv(a, m):
    gcd, x, y = egcd(a, m)
    if gcd != 1:
        return None  # modular inverse does not exist
    else:
        return x % m

def RSA_Oracle_Get():
  response = requests.get('{}/{}/{}'.format(API_URL, "RSA_Oracle", my_id)) 	
  c, N, e = 0,0,0 
  if response.ok:	
    res = response.json()
    print(res)
    return res['c'], res['N'], res['e']
  else:
    print(response.json())

def RSA_Oracle_Query(c_):
  response = requests.get('{}/{}/{}/{}'.format(API_URL, "RSA_Oracle_Query", my_id, c_)) 
  print(response.json())
  m_= ""
  if response.ok:	m_ = (response.json()['m_'])
  else: print(response)
  return m_

def RSA_Oracle_Checker(m):
  response = requests.put('{}/{}/{}/{}'.format(API_URL, "RSA_Oracle_Checker", my_id, m))
  print(response.json())

## THIS IS ONLY AN EMPTY CLIENT CODE, YOU HAVE TO EXTRACT M
## THEN CHECK IT USING THE CHECKING ORACLE.


# Step 1: Get the original ciphertext
c, N, e = RSA_Oracle_Get()

def find_relatively_prime_number(N):
    while True:
        r = random.randint(2, N - 1)
        if math.gcd(r, N) == 1:
            return r

def decode_to_unicode(m):
    length = (m.bit_length() + 7) // 8
    m_bytes = m.to_bytes(length, byteorder='big')
    return m_bytes.decode()

# Step 2: Choose a random number r
r = find_relatively_prime_number(N)

# Step 3: Create a modified ciphertext C'
c_ = (pow(r, e, N) * c) % N

# Step 4: Query the oracle
m_ = RSA_Oracle_Query(c_)

# Step 5: Compute the original plaintext
r_inv = modinv(r, N)
m = (m_ * r_inv) % N

# Decode m into a Unicode string
m_decoded = decode_to_unicode(m)

# Step 6: Check the answer
RSA_Oracle_Checker(m_decoded)


