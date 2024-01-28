

# RSA parameters
N = 9244432371785620259
e = 2**16 + 1
"""
def trial_division_factorize(n):
    Factorize n using trial division method 
    # Start with the smallest prime
    factor = 2
    while factor * factor <= n:
        if n % factor:
            factor += 1
        else:
            # Found a factor
            return factor, n // factor
    return n, 1

# Factorize N using trial division
"""
import sympy

# RSA parameters
N = 9244432371785620259
e = 2**16 + 1

# Factorize N
p, q = sympy.factorint(N).keys()
#p, q = trial_division_factorize(N)
#when I tried the function it took soo long that I could not compile but when I used this library it was very short
print(p)
print(q)

# Calculate the totient of N
phi_N = (p - 1) * (q - 1)

# Calculate the private exponent d
d = pow(e, -1, phi_N)

# RSA parameters for decryption
C = 655985469758642450

# Decrypt C to find the plaintext M
M = pow(C, d, N)
print(M)