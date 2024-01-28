import math
import time
import random
import warnings
from random import randint, seed
import sys
import Crypto
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
from Crypto.PublicKey import ECC
from Crypto.Signature import pkcs1_15
from Crypto.Util.number import bytes_to_long
from Crypto.Util.number import long_to_bytes
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

API_URL = 'http://harpoon1.sabanciuniv.edu:9999/'

stuID = 27960 # Enter your student ID
stuIDB = 18007
IKey_Ser = [0x1d42d0b0e55ccba0dd86df9f32f44c4efd7cbcdbbb7f36fd38b2ca680ab126e9, 0xce091928fa3738dc18f529bf269ade830eeb78672244fd2bdfbadcb26c4894ff ]
E = Curve.get_curve('secp256k1')

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
    
def generate_key():
    n = E.order
    P = E.generator
    random_generator = Random.new()
    secret_byte_length = (n - 1).bit_length() // 8 + 1
    random_bytes = random_generator.read(secret_byte_length)
    secret = int.from_bytes(random_bytes, byteorder='big') % (n - 1)
    public_key = secret * P
    return(public_key, secret)

def SignVer(message, h, s, E, QA):
    n = E.order
    P = E.generator
    V = s*P + h*QA
    v = V.x%n
    h_ = int.from_bytes(SHA3_256.new(v.to_bytes((v.bit_length()+7)//8, byteorder='big')+message).digest(), byteorder='big')%n
    if h_ == h:
        return True
    else:
        return False

IK_Pub = (0xa1c289a9a4a5fc9c3de13c7c02307f60b8c2a07e97c2548589463c0896484050 , 0x196664c6394fe38917e1e6c47215828d0304197507e33c306928002764e4f8f4) 
IK_Priv = 1613213779714502971373277283885029354224134410000408420711755958072917579576
SPK_Priv = 15833722098867099455939670645538099613420397046512444684586316212176021568757

IKS_Pub = [47152521721929048576835233048131082052837378382754191750807960678031815670051, 21607448093224984998827691156606805883380972680266521549245559135655451173805]
EKS_Pub = [87667642166793354522007699941182035073271754556576185236091474380992828102853, 44243311074133191299988586115323755733722982189892432091609384673666584608330]


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

def sign(a):
    signed = a.to_bytes((a.bit_length() + 7) // 8, byteorder='big')
    return signed
def IKRegReq(h,s,x,y):
    mes = {'ID': stuID, 'H': h, 'S': s, 'IKPUB.X': x, 'IKPUB.Y': y}
    print("Sending message is: ", mes)
    response = requests.put('{}/{}'.format(API_URL, "IKRegReq"), json = mes)		
    if((response.ok) == False): print(response.json())

def IKRegVerify(code):
    mes = {'ID': stuID, 'CODE': code}
    print("Sending message is: ", mes)
    response = requests.put('{}/{}'.format(API_URL, "IKRegVerif"), json = mes)
    if((response.ok) == False): raise Exception(response.json())
    print(response.json())

def SPKReg(h,s,x,y):
    mes = {'ID':stuID, 'H': h, 'S': s, 'SPKPUB.X': x, 'SPKPUB.Y': y}
    print("Sending message is: ", mes)
    response = requests.put('{}/{}'.format(API_URL, "SPKReg"), json = mes)
    print(response.json())


def ResetIK(rcode):
    mes = {'ID': stuID, 'RCODE': rcode}
    print("Sending message is: ", mes)
    response = requests.delete('{}/{}'.format(API_URL, "ResetIK"), json = mes)		
    print(response.json())
    if((response.ok) == False): return False
    else: return True

def ResetSPK(h,s):
    mes = {'ID': stuID, 'H': h, 'S': s}
    print("Sending message is: ", mes)
    response = requests.delete('{}/{}'.format(API_URL, "ResetSPK"), json = mes)		
    print(response.json())
    if((response.ok) == False): return False
    else: return True

def ResetOTK(h,s):
    mes = {'ID': stuID, 'H': h, 'S': s}
    print("Sending message is: ", mes)
    response = requests.delete('{}/{}'.format(API_URL, "ResetOTK"), json=mes)
    print(response.json())



############## The new functions of phase 2 ###############

def PseudoSendMsg(h,s):
    mes = {'ID':stuID, 'H': h, 'S': s}
    print("Sending message is: ", mes)
    response = requests.put('{}/{}'.format(API_URL, "PseudoSendMsg"), json = mes)
    print(response.json())

#Get your messages. server will send 1 message from your inbox
def ReqMsg(h,s):
    mes = {'ID':stuID, 'H': h, 'S': s}
    print("Sending message is: ", mes)
    response = requests.get('{}/{}'.format(API_URL, "ReqMsg"), json = mes)
    print(response.json())
    if((response.ok) == True):
        res = response.json()
        return res["IDB"], res["OTKID"], res["MSGID"], res["MSG"], res["IK.X"], res["IK.Y"], res["EK.X"], res["EK.Y"]


#Get the list of the deleted messages' ids.
def ReqDelMsg(h,s):
    mes = {'ID':stuID, 'H': h, 'S': s}
    print("Sending message is: ", mes)
    response = requests.get('{}/{}'.format(API_URL, "ReqDelMsgs"), json = mes)
    print(response.json())
    if((response.ok) == True):
        res = response.json()
        return res["MSGID"]

#If you decrypted the message, send back the plaintext for checking
def Checker(stuID, stuIDB, msgID, decmsg):
    mes = {'IDA':stuID, 'IDB':stuIDB, 'MSGID': msgID, 'DECMSG': decmsg}
    print("Sending message is: ", mes)
    response = requests.put('{}/{}'.format(API_URL, "Checker"), json = mes)
    print(response.json())


############## The new functions of phase 3 ###############

#Pseudo-client will send you 5 messages to your inbox via server when you call this function
def PseudoSendMsgPH3(h,s):
    mes = {'ID': stuID, 'H': h, 'S': s}
    print("Sending message is: ", mes)
    response = requests.put('{}/{}'.format(API_URL, "PseudoSendMsgPH3"), json=mes)
    print(response.json())

# Send a message to client idB
def SendMsg(idA, idB, otkID, msgid, msg, ikx, iky, ekx, eky):
    mes = {"IDA": idA, "IDB": idB, "OTKID": int(otkID), "MSGID": msgid, "MSG": msg, "IK.X": ikx, "IK.Y": iky, "EK.X": ekx, "EK.Y": eky}
    print("Sending message is: ", mes)
    response = requests.put('{}/{}'.format(API_URL, "SendMSG"), json=mes)
    print(response.json())    


# Receive KeyBundle of the client stuIDB
def reqKeyBundle(stuID, stuIDB, h, s):
    key_bundle_msg = {'IDA': stuID, 'IDB':stuIDB, 'S': s, 'H': h}
    print("Requesting party B's Key Bundle ...")
    response = requests.get('{}/{}'.format(API_URL, "ReqKeyBundle"), json=key_bundle_msg)
    print(response.json()) 
    if((response.ok) == True):
        print(response.json()) 
        res = response.json()
        return res['KEYID'], res['IK.X'], res['IK.Y'], res['SPK.X'], res['SPK.Y'], res['SPK.H'], res['SPK.s'], res['OTK.X'], res['OTK.Y']
        
    else:
        return -1, 0, 0, 0, 0, 0, 0, 0, 0


#Status control. Returns #of messages and remained OTKs
def Status(stuID, h, s):
    mes = {'ID': stuID, 'H': h, 'S': s}
    print("Sending message is: ", mes)
    response = requests.get('{}/{}'.format(API_URL, "Status"), json=mes)
    print(response.json())
    if (response.ok == True):
        res = response.json()
        return res['numMSG'], res['numOTK'], res['StatusMSG']


def OTKReg(keyID,x,y,hmac):
    mes = {'ID':stuID, 'KEYID': keyID, 'OTKI.X': x, 'OTKI.Y': y, 'HMACI': hmac}
    print("Sending message is: ", mes)
    response = requests.put('{}/{}'.format(API_URL, "OTKReg"), json = mes)		
    print(response.json())
    if((response.ok) == False): return False
    else: return True
    
def generate_HMAC():
    P = Point(IKey_Ser[0], IKey_Ser[1], E)
    T = SPK_Priv * P
    success = b'TheHMACKeyToSuccess'
    U = success  + T.y.to_bytes((T.y.bit_length() + 7) // 8, byteorder='big') + T.x.to_bytes((T.x.bit_length() + 7) // 8, byteorder='big')
    HMAC_key = SHA3_256.new(U)
    return HMAC_key

def generate_HMAC_OTK(KHMAC, myn):
    #U = myn.to_bytes((myn.bit_length() + 7) // 8, byteorder='big')
    h = HMAC.new(KHMAC, digestmod = SHA256)
    HMAC_value = h.update(myn).hexdigest()
    return HMAC_value

def register_OTK(i):
    HMAC_key = generate_HMAC()
    HMAC_key = HMAC_key.digest()
    print(HMAC_key)
    keyID = i
    OTK = generate_key()
    OTK_Priv = OTK[1]
    OTK_Pub = OTK[0]
    signed_otkx = sign(OTK_Pub.x)
    signed_otky = sign(OTK_Pub.y)
    concat = signed_otkx + signed_otky
    print("OTK_Pub:", OTK_Pub, "OTK_Priv:", OTK_Priv)
    hmac = generate_HMAC_OTK(HMAC_key, concat)
    OTKReg(keyID, OTK_Pub.x, OTK_Pub.y, hmac)
    return OTK_Priv


def generate_sk(otk_priv):
    IKS = Point(IKS_Pub[0], IKS_Pub[1], E)
    EKS = Point(EKS_Pub[0], EKS_Pub[1], E)
    T1 = SPK_Priv * IKS
    T2 = EKS * IK_Priv
    T3 = EKS * SPK_Priv
    T4 = EKS * otk_priv
    U = sign(T1.x) + sign(T1.y) + sign(T2.x) + sign(T2.y) + sign(T3.x) + sign(T3.y) + sign(T4.x) + sign(T4.y) + b'WhatsUpDoc'
    session_key = SHA3_256.new(U)
    return session_key.digest()

def generate_kdf(kdf):
    U = kdf + b'JustKeepSwimming'
    kenc = SHA3_256.new(U).digest()
    U2 = kdf + kenc + b'HakunaMatata'
    khmac = SHA3_256.new(U2).digest()
    U3 = kenc + khmac + b'OhanaMeansFamily'
    kdf_next = SHA3_256.new(U3).digest()
    return kenc, khmac, kdf_next

def encrypt_msg(msg, khmac, kenc, id):
    msg = sign(msg)
    nonce = msg[:8]
    mac = msg[-32:]
    ctext = msg[8:-32]
    hmac = HMAC.new(khmac, ctext, digestmod = SHA256).digest()
    if (mac == hmac):
        print("true!")
        ptext = AES.new(kenc, AES.MODE_CTR, nonce = nonce)
        ptext = ptext.decrypt(ctext)
        ptext = ptext.decode('utf-8')
        print(ptext)
        Checker(27960, 18007, id, ptext)
        return ptext
    else:
        print("false!")
        Checker(27960,18007,id,'INVALIDHMAC')
        return 'INVALIDHMAC'


P = E.generator
n = E.order

def AesEncrypt(ptext, key):

    ptext_bytes = ptext.encode('utf-8')
    

    cipher = AES.new(key, AES.MODE_CTR)

    ctext = cipher.nonce + cipher.encrypt(ptext_bytes)
    
    return ctext


def phs3_session_key_generator(KEYID, OTK_X, OTK_Y):

    print("KEYID: ", KEYID)
    print("OTK_X: ", OTK_X)
    print("OTK_Y: ", OTK_Y)

    OTK_server = Point(OTK_X,OTK_Y, E) 

    EKPriv_server = Crypto.Random.random.randint(1, n-2)

    EKPublic = EKPriv_server * P 

    T = EKPriv_server * OTK_server 

    U = (T.x).to_bytes(((T.x).bit_length()+7)//8, "big") + (T.y).to_bytes(((T.y).bit_length()+7)//8, "big") + b'WhatsUpDoc'

    generated_ks = SHA3_256.new(U).digest()
    return generated_ks, EKPublic

def phs3SendMessage(generated_ks, message, msgID, KEYID, IK_X, IK_Y, EKPublic):

    kenc1_p3, khmac1_p3, kkdf1_p3 = generate_kdf(generated_ks)

    ctext1 = AesEncrypt(message, kenc1_p3)

    def addHmac(ctext, hmac):
        hmac3 = HMAC.new(hmac, digestmod=SHA256)

        hmac3.update(ctext)

        hmac_final = hmac3.digest()

        fin = ctext + hmac_final

        fin = int.from_bytes(fin, byteorder='big')
        return fin

    finalMessage = addHmac(ctext1, khmac1_p3)

    SendMsg(stuID, stuIDB, KEYID, msgID, finalMessage, IK_X, IK_Y, EKPublic.x, EKPublic.y)
    return kenc1_p3, khmac1_p3, kkdf1_p3 

h, s = generate_signature(sign(stuID))
ResetOTK(h, s)

OTK_List = []
for i in range(10):
    priv = register_OTK(i)
    OTK_List.append(priv)


hB, sB = generate_signature(sign(stuIDB))
keyID, IKX, IKY, SPKX, SPKY, SPKH, SPKS, OTKX, OTKY = reqKeyBundle(stuID, stuIDB, hB, sB)

messagesDecrypted = []
PseudoSendMsgPH3(h, s)

reds = ReqMsg(h, s)
otkID = reds[1]
messageIn = reds[3]
msgID = reds[2]

session_key = generate_sk(OTK_List[otkID])
kenc, khmac, kdf_next = generate_kdf(session_key)

for i in range(5):
    if(i != 0):
        kenc, khmac, kdf_next = generate_kdf(kdf_next)
        reds = ReqMsg(h, s)
        messageIn = reds[3]
        msgID = reds[2]
        encrypted = encrypt_msg(messageIn, khmac, kenc, msgID)
        messagesDecrypted.append(encrypted)
    else:
        encrypted = encrypt_msg(messageIn, khmac, kenc, msgID)
        messagesDecrypted.append(encrypted)




generatedSK, EKPublicServer = phs3_session_key_generator(keyID, OTKX, OTKY)
kencSer, khmacSer, kkdfSer = phs3SendMessage(generatedSK, messagesDecrypted[0], 1, keyID, IKX, IKY, EKPublicServer)
for i in range(2, 6):
    kencSer, khmacSer, kkdfSer = phs3SendMessage(kkdfSer, messagesDecrypted[i - 1], i, keyID, IKX, IKY, EKPublicServer)

ReqDelMsg(h, s)

Status(stuID, h, s)