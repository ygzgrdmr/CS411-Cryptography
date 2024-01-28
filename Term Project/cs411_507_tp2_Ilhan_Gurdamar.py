import math
import time
import random
import sympy
import warnings
from random import randint, seed
import sys
from ecpy.curves import Curve,Point
from Crypto.Hash import SHA3_256, HMAC, SHA256
import requests
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
import random
import re
import json

stuID = 22534
API_URL = 'http://harpoon1.sabanciuniv.edu:9999'
IKey_Ser = [0x1d42d0b0e55ccba0dd86df9f32f44c4efd7cbcdbbb7f36fd38b2ca680ab126e9, 0xce091928fa3738dc18f529bf269ade830eeb78672244fd2bdfbadcb26c4894ff ]
E = Curve.get_curve('secp256k1')

#step1
def generate_key():
    n = E.order
    P = E.generator
    random_generator = Random.new()
    secret_byte_length = (n - 1).bit_length() // 8 + 1
    random_bytes = random_generator.read(secret_byte_length)
    secret = int.from_bytes(random_bytes, byteorder='big') % (n - 1)
    public_key = secret * P
    return(public_key, secret)

'''
IK_Pub = generate_key()
IK_Priv = IK_Pub[1]
IK_Pub = IK_Pub[0]
print("IK_Pub:", IK_Pub, "IK_Priv:", IK_Priv)
'''
IK_Pub = (0xae2fb750b79f7b250c45505465b64e5946780e9344f44c633af64d55c3835599 , 0x1526d64e04afe4a4865b1141e2e379024a7107ff0c690be9eeffe28c6a754a5) 
IK_Priv = 1543896032916106760346604607429596123935279822749430729401681684064237002197


#step2
def generate_signature(m):
    n = E.order
    P = E.generator

    k_bytes = Random.new().read(int(math.log(n,2)))
    k = int.from_bytes(k_bytes, byteorder='big')%n
    
    R = k*P
    r = R.x%n

    r_bytes = r.to_bytes((r.bit_length() + 7) // 8, byteorder='big')
    concatenated_bytes = r_bytes + m
    h = int.from_bytes(SHA3_256.new(concatenated_bytes).digest(), byteorder='big') % n
    s = (k - h * IK_Priv) % n
    return(h, s)

'''
signed_ID = stuID.to_bytes((stuID.bit_length() + 7) // 8, byteorder='big')
h, s = generate_signature(signed_ID)
print("h:", h, "s:", s)

def IKRegReq(h,s,x,y):
    mes = {'ID':stuID, 'H': h, 'S': s, 'IKPUB.X': x, 'IKPUB.Y': y}
    print("Sending message is: ", mes)
    response = requests.put('{}/{}'.format(API_URL, "IKRegReq"), json = mes)		
    print(response.json())

IKRegReq(h, s, IK_Pub[0], IK_Pub[1])

#Sending message is:  {'ID': 22534, 'H': 45015586454498973722632311832829889671118987502740260940691121278956184907951, 'S': 4669056507246141728529955536889210786974378499877821103054613773684467785991, 'IKPUB.X': 78786742661247887753105672246083800718682023279022816498278733643447259059609, 'IKPUB.Y': 597949317862364586527161738743216439693679072405172950199248119085180343461}
'''
'''
#step3
def IKRegVerify(code):
    mes = {'ID':stuID, 'CODE': code}
    print("Sending message is: ", mes)
    response = requests.put('{}/{}'.format(API_URL, "IKRegVerif"), json = mes)
    if((response.ok) == False): raise Exception(response.json())
    else:
        print(response.json())
        f = open('Identity_Key.txt', 'w')
        f.write("IK.Prv: "+str(IK_Priv)+"\n"+"IK.Pub.x: "+str(IK_Pub[0])+"\n"+"IK.Pub.y: "+str(IK_Pub[1]))
        f.close()

IKRegVerify(931152) # rcode:949029
'''

def sign(a):
    signed = a.to_bytes((a.bit_length() + 7) // 8, byteorder='big')
    return signed

'''
#step4
def SPKReg(h,s,x,y):
    mes = {'ID':stuID, 'H': h, 'S': s, 'SPKPUB.X': x, 'SPKPUB.Y': y}
    print("Sending message is: ", mes)
    response = requests.put('{}/{}'.format(API_URL, "SPKReg"), json = mes)
    print(response.json())

SPK = generate_key()
SPK_Priv = SPK[1]
SPK_Pub = SPK[0]

print("SPK_Pub:", SPK_Pub, "SPK_Priv:", SPK_Priv)

signed_X = sign(SPK_Pub.x)
signed_Y = sign(SPK_Pub.y)
concat = signed_X + signed_Y
print(concat)

h, s = generate_signature(concat)

print("h:", h, "s:", s)

SPKReg(h, s, SPK_Pub.x, SPK_Pub.y)

#SPK_Priv: 94602756615425578667537335092655233161050007550996685330695502996118783070902
#Sending message is:  {'ID': 22534, 'H': 19999582383324447991793018477135363709056378354624216266130030243597722364756, 'S': 85206786855365501313790906839476395761667335762893276255209264195474275230919, 'SPKPUB.X': 91454539758165751973916517960780619286296889665007884764532551740722360426664, 'SPKPUB.Y': 101423231227881222586311174248103728695631842448834407015040678004292957475563}
'''
SPK_Priv = 94602756615425578667537335092655233161050007550996685330695502996118783070902

#step5
def OTKReg(keyID,x,y,hmac):
    mes = {'ID':stuID, 'KEYID': keyID, 'OTKI.X': x, 'OTKI.Y': y, 'HMACI': hmac}
    print("Sending message is: ", mes)
    response = requests.put('{}/{}'.format(API_URL, "OTKReg"), json = mes)		
    print(response.json())
    if((response.ok) == False): return False
    else: return True
    
def generate_HMAC():
    T_x = SPK_Priv * IKey_Ser[0]
    T_y = SPK_Priv * IKey_Ser[1]
    success = b'TheHMACKeyToSuccess'
    U = success  + T_y.to_bytes((T_y.bit_length() + 7) // 8, byteorder='big') + T_x.to_bytes((T_x.bit_length() + 7) // 8, byteorder='big')
    HMAC_key = SHA3_256.new(U)
    HMAC_key = HMAC_key.hexdigest()
    return HMAC_key

def generate_HMAC_OTK(KHMAC, myn):
    U = myn.to_bytes((myn.bit_length() + 7) // 8, byteorder='big')
    HMAC_value = HMAC.new(KHMAC.encode('utf-8'), U, SHA256).hexdigest()
    return HMAC_value

def register_OTK(i):
    HMAC_key = generate_HMAC()
    print(HMAC_key)
    keyID = i
    OTK = generate_key()
    OTK_Priv = OTK[1]
    OTK_Pub = OTK[0]
    concat = OTK_Pub.x + OTK_Pub.y
    print("OTK_Pub:", OTK_Pub, "OTK_Priv:", OTK_Priv)
    hmac = generate_HMAC_OTK(HMAC_key, concat)
    OTKReg(keyID, OTK_Pub.x, OTK_Pub.y, hmac)
    
for i in range(10):
    register_OTK(i)
