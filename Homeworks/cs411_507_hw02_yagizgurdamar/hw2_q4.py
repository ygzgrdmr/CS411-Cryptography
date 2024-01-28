import math
import random
import warnings

def gcd(a, b):
    while b:
        a, b = b, a%b
    return a

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
        return None
    else:
        return x % m


n1 = 2163549842134198432168413248765413213216846313201654681321666
a1 = 790561357610948121359486508174511392048190453149805781203471
b1 = 789213546531316846789795646513847987986321321489798756453122

n2 = 3213658549865135168979651321658479846132113478463213516854666
a2 = 789651315469879651321564984635213654984153213216584984653138
b2 = 798796513213549846121654984652134168796513216854984321354987

n3 = 5465132165884684652134189498513211231584651321849654897498222
a3 = 654652132165498465231321654946513216854984652132165849651312
b3 = 987965132135498749652131684984653216587986515149879613516844

n4 = 6285867509106222295001894542787657383846562979010156750642244
a4 = 798442746309714903987853299207137826650460450190001016593820
b4 = 263077027284763417836483408268884721142505761791336585685868

z1=modinv(a1,n1)
z2=modinv(a2,n2)
z3=modinv(a3,n3)
z4=modinv(a4,n4)

print(z1)
print(z2)
print(z3)
print(z4)

x1=(b1*z1)% n1

print(x1)


exp= "For n1, a1 and b1, I found a modular inverse z1, and subsequently calculated  x1 as (b1 times z1) % n1. This resulted in a specific solution x1. For the next two equations with n2, a2, b2 and n3, a3, b3, the modular inverses (`z2` and `z3`) do not exist. This implies that a2  and  a3 are not coprime with  n2 and n3 respectively, and hence, no solutions exist for these equations. For n4, a4, and b4, the modular inverse (`z4`) does not exist, indicating no solution for this equation either."
print(exp)