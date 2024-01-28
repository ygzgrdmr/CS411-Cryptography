

a1  = 2700926558
b1  = 967358719
q1  = 3736942861

a2  = 1759062776
b2  = 1106845162
q2  = 3105999989

a3  = 2333074535
b3  = 2468838480
q3  = 2681377229

# Function to calculate modular inverse
def modinv(a, m):
    """ Compute the modular inverse of a modulo m """
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise Exception('Modular inverse does not exist')
    else:
        return x % m

def extended_gcd(a, b):
    """ Extended Euclidean Algorithm """
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = extended_gcd(b % a, a)
        return (g, x - (b // a) * y, y)

# Compute Q
Q = q1 * q2 * q3

# Perform the unified multiplication and calculate R
R = (a1 * b1 * a2 * b2 * a3 * b3) % Q
print(Q,R)
# Calculating r1, r2, and r3
Q_div_q1 = Q // q1
Q_div_q2 = Q // q2
Q_div_q3 = Q // q3

modinv_q1 = modinv(Q_div_q1, q1)
modinv_q2 = modinv(Q_div_q2, q2)
modinv_q3 = modinv(Q_div_q3, q3)

r1 = (R * Q_div_q1 * modinv_q1) % q1
r2 = (R * Q_div_q2 * modinv_q2) % q2
r3 = (R * Q_div_q3 * modinv_q3) % q3

print(r1, r2, r3)
