
import random
def LFSR(C, S):
    L = len(S)
    fb = 0
    out = S[L-1]
    for i in range(0,L):
        fb = fb^(S[i]&C[i+1])
    for i in range(L-1,0,-1):
        S[i] = S[i-1]

    S[0] = fb
    return out

def FindPeriod(s):
    n = len(s)
    for T in range(1,n+1):
        chck = 0
        for i in range(0,n-T-1):
            if (s[i] != s[i+T]):
                chck += 1
                break
        if chck == 0:
            break
    if T > n/2:
        return n
    else:
        return T

def PolPrune(P):
    n = len(P)
    i = n-1
    while (P[i] == 0):
        del P[i]
        i = i-1
    return i

def PolDeg(P):
    n = len(P)
    i = n-1
    while (P[i] == 0):
        i = i-1
    return i

# P gets Q
def PolCopy(Q, P):
    degP = len(P)
    degQ = len(Q)
    if degP >= degQ:
        for i in range(0,degQ):
            Q[i] = P[i]
        for i in range(degQ, degP):
            Q.append(P[i])
    else: # degP < deqQ
        for i in range(0,degP):
            Q[i] = P[i]
        for i in range(degP, degQ):
            Q[i] = 0
        PolPrune(Q)

def BM(s):
    n = len(s)

    C = []
    B = []
    T = []
    L = 0
    m = -1
    i = 0
    C.append(1)
    B.append(1)

    while(i<n):
        delta = 0
        clen = len(C)
        for j in range(0, clen):
            delta ^= (C[j]*s[i-j])
        if delta == 1:
            dif = i-m
            PolCopy(T, C)
            nlen = len(B)+dif
            if(clen >= nlen):
                for j in range(dif,nlen):
                    C[j] = C[j] ^ B[j-dif]
            else: # increase the degree of C
                for j in range(clen, nlen):
                    C.append(0)
                for j in range(dif, nlen):
                    C[j] = C[j] ^ B[j-dif]
            PolPrune(C)
            if L <= i/2:
                L = i+1-L
                m = i
                PolCopy(B, T)
        i = i+1
    return L, C

def example_usage():
    length = 256
    ##########################
    print("LFSR: **************")

    # Define the polynomials
    polynomials = [
        [7, 5, 3, 1],  # p1(x) = x^7 + x^5 + x^3 + x + 1
        [6, 5, 2],  # p2(x) = x^6 + x^5 + x^2 + 1
        [5, 4, 3, 1]  # p3(x) = x^5 + x^4 + x^3 + x + 1
    ]

    for poly in polynomials:
        # Initialize the LFSR configuration
        L = max(poly)  # Length of the LFSR is the highest power
        C = [0] * (L + 1)  # Create the tap configuration array

        # Set the tap positions based on the polynomial
        for tap in poly:
            C[tap] = 1  # Set the taps

        # Ensure the 0th coefficient is set (for the feedback tap)
        C[0] = 1

        # Random initial state of the LFSR
        S = [random.randint(0, 1) for _ in range(L)]
        print("Testing polynomial:", poly)
        print("Initial state: ", S)

        # Generate the keystream
        keystream = [LFSR(C, S) for _ in range(length)]

        # Check and print the period
        period = FindPeriod(keystream)
        print("Period: ", period)
        print("Is maximum period:", period == 2 ** L - 1)

        # Find and print the L and C(x) using Berlekamp-Massey
        L, Cx = BM(keystream)
        print("L and C(x): ", (L, Cx))
        print("keystream: ", keystream[:50])  # Print the first 50 bits of keystream
        print()  # Empty line for readability between tests


# Call the example usage function
example_usage()

exp="For p1(x): Generated a sequence with a period of 127. his is a maximum period since 2^7-1=127. The LFSR length and polynomial confirmed by the BM algorithm are L=7 and x7 + x5 + x3 + x + 1. For p2(x): Generated a sequence with a period of 21. This is not a maximum period since 2^6-1=63. The LFSR length and polynomial from the BM algorithm are L=6 and x6 + x5 + x2 + 1. For p3(x): Generated a sequence with a period of 31. This is a maximum period since 2^5-1=31. The LFSR length and polynomial from the BM algorithm are L=5 and x5 + x4 + x3 + x + 1. Polynomial p1(x) and p3(x) generate maximum period sequences. However Polynomial p2(x) does not generate a maximum period sequence."

print(exp)