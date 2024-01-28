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

stuID = 27960
API_URL = 'http://harpoon1.sabanciuniv.edu:9999'
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
    
#PHASE1
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

IK_Pub = (0xa1c289a9a4a5fc9c3de13c7c02307f60b8c2a07e97c2548589463c0896484050 , 0x196664c6394fe38917e1e6c47215828d0304197507e33c306928002764e4f8f4) 
IK_Priv = 1613213779714502971373277283885029354224134410000408420711755958072917579576


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
'''
#Sending message is:  {'ID': 27960, 'H': 75760430931182321293698420106004396367306357132290413229608408107910471862875, 'S': 40313791308174071354016793170035970006984318844567172773965395444247843115352, 'IKPUB.X': 73166087065292890969506544715944408183966922056601967701857459164924017655888, 'IKPUB.Y': 11488735133928839038755456587271477271036665971534483893727577816587592595700}

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

IKRegVerify(730435) # rcode:129558
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
h, s = generate_signature(concat)
SPKReg(h, s, SPK_Pub.x, SPK_Pub.y)

#Sending message is:  {'ID': 27960, 'H': 100984550001556963679000034313751081366744249736796312894541330737767634589492, 'S': 45472784050133958564814491994193123024632986631816753399502569501842774063074, 'SPKPUB.X': 56140484333046611124760905045666279902113881466365395685037231080166749370342, 'SPKPUB.Y': 103429825029516501537710621115672916314788940161847529095737905192314328760641}
'''
SPK_Priv = 15833722098867099455939670645538099613420397046512444684586316212176021568757
'''
#step5
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
    
for i in range(10):
    register_OTK(i)
'''
'''
b'W\xbc[\xc2\xda\xb5\x8f\x1eNb\x91,G\x88\xb32\xf0\xdd\xb5\xc6\xc7\xa2f\xaa\xe4\xb6\xc9x\xd5\x95\x92\x11'
OTK_Pub: (0x96b11db2675383d5acdf32b40a23581c872e831402573050a6464c79b9333fed , 0x1751bebe69ab60a8d9e636ab7b1950aedbd2e4c6aff3f583407bff517d8d68bf) OTK_Priv: 59695232315866645350524632214997374447013498209719735140639879586940923732993
Sending message is:  {'ID': 27960, 'KEYID': 0, 'OTKI.X': 68159864178351818073069665420570505392986951950346472316760073198200228626413, 'OTKI.Y': 10547626594986224299996077537598016108124175303303361241530461908219177298111, 'HMACI': '652df21a0578ded45cd86a37bdef0dc1c18e0ad21de25e262de807d779186e42'}
OTK with ID number 0 is registered successfully
b'W\xbc[\xc2\xda\xb5\x8f\x1eNb\x91,G\x88\xb32\xf0\xdd\xb5\xc6\xc7\xa2f\xaa\xe4\xb6\xc9x\xd5\x95\x92\x11'
OTK_Pub: (0xf7ffc09d8688d604a390a9ccf9b2d2fae83bfafc49b52877918f2a667e072af3 , 0xa3f4884b3d0488be1445142bd33694f973beff14fe263304960176730211a42b) OTK_Priv: 35713889092425400520488937131336270108310671671729795405757536296259551798525
Sending message is:  {'ID': 27960, 'KEYID': 1, 'OTKI.X': 112173148983763634615548510414357296617909709955717501867764016742939387964147, 'OTKI.Y': 74159045668803425667302911975802987031991129615354219255445052409686269207595, 'HMACI': '38674464329078b966cecc0d5b164135bdf65ad9aafcf6e00f3ce655f968cef9'}
OTK with ID number 1 is registered successfully
b'W\xbc[\xc2\xda\xb5\x8f\x1eNb\x91,G\x88\xb32\xf0\xdd\xb5\xc6\xc7\xa2f\xaa\xe4\xb6\xc9x\xd5\x95\x92\x11'
OTK_Pub: (0x82b228f673d96baae3020e1512c9bddf247261605ff367d4c9865be9d5b8579c , 0x13a16537a119572820ba0351b8d55d11dc2206fc440dcea630f935812c5298bf) OTK_Priv: 717797138633951989788641029513676641911428577885134309472480806137516200781
Sending message is:  {'ID': 27960, 'KEYID': 2, 'OTKI.X': 59115451807556289819969857919107643265590138529766021817936245128436643288988, 'OTKI.Y': 8879105076655177214001128321466562641752364089714275390801026809005501225151, 'HMACI': '039398389798fa9bb3be8108a132a7bbbd1f49bd0ed371c2cea4c5d8df188884'}
OTK with ID number 2 is registered successfully
b'W\xbc[\xc2\xda\xb5\x8f\x1eNb\x91,G\x88\xb32\xf0\xdd\xb5\xc6\xc7\xa2f\xaa\xe4\xb6\xc9x\xd5\x95\x92\x11'
OTK_Pub: (0xdf2d22a635b7c3871bb62e68525b214a72a2d63da1844085d491fede53f63acc , 0x9aef55cadb78bd24936b59909962f789d67bf860337961307eb992d5f8062832) OTK_Priv: 103960056161185047876320228923097348919053983073298439836932651984671160343700
Sending message is:  {'ID': 27960, 'KEYID': 3, 'OTKI.X': 100945512492367517021195343231633899011432452889710911397577194339694600927948, 'OTKI.Y': 70079047247766822579627898326374334859663888699122317914595640303136478210098, 'HMACI': '7793a6fed81ef5b7c015c01fa1d5eb7511f05e936be43a23a2e7de3cf2aec0b3'}
OTK with ID number 3 is registered successfully
b'W\xbc[\xc2\xda\xb5\x8f\x1eNb\x91,G\x88\xb32\xf0\xdd\xb5\xc6\xc7\xa2f\xaa\xe4\xb6\xc9x\xd5\x95\x92\x11'
OTK_Pub: (0x41f36d007027a74a3a2fd6979ccc429b0f79bb327f35d77d5e3489ded3a735a6 , 0x59aef04a39555b76ebfd16513f0a31fba200394627856c59f3ba91961771a856) OTK_Priv: 82050755459793342341755328626463839810734980285413560922233782285753166499418
Sending message is:  {'ID': 27960, 'KEYID': 4, 'OTKI.X': 29830431296816551968705586288562346476782601951995850418973944873761525675430, 'OTKI.Y': 40564933333379345117826964952056943162791402673223714304463329050752931965014, 'HMACI': '8f2f9b6847199e10211bff89f311e0e46c1842406b06b500e2840eba0ee1f594'}
OTK with ID number 4 is registered successfully
b'W\xbc[\xc2\xda\xb5\x8f\x1eNb\x91,G\x88\xb32\xf0\xdd\xb5\xc6\xc7\xa2f\xaa\xe4\xb6\xc9x\xd5\x95\x92\x11'
OTK_Pub: (0x24c15a3b96b796ffc5d4c94796deb1420477954282a3eab029eb8ccfb3256e2f , 0xaffae90252b975f25a1e458db646de048df57b85771a4be71d85a858aeca381a) OTK_Priv: 70185573900392227745180452588073288257624192702717327394059027818942952188961
Sending message is:  {'ID': 27960, 'KEYID': 5, 'OTKI.X': 16624886796180250899677274569514771727712701952815959214126797820370985774639, 'OTKI.Y': 79598068437796811619008590681099621598880967510512304958706575063261251254298, 'HMACI': 'bc3c92bc99cfb6f84f0270279457859eb840c1e281799a058ff5e7203069d162'}
OTK with ID number 5 is registered successfully
b'W\xbc[\xc2\xda\xb5\x8f\x1eNb\x91,G\x88\xb32\xf0\xdd\xb5\xc6\xc7\xa2f\xaa\xe4\xb6\xc9x\xd5\x95\x92\x11'
OTK_Pub: (0xebd2dfe01c4ecd2b56439b5462e76046f7970602c0b8e5325a931e738ca26530 , 0x39b974194849f991ce465c6d94a0e6d52789b8852a2273004932eb49a5518be1) OTK_Priv: 26683745441767895537390921465313986054786491478078705414491127589454077020420
Sending message is:  {'ID': 27960, 'KEYID': 6, 'OTKI.X': 106666102432115610914328583840840730450277901915767350540726179005386169935152, 'OTKI.Y': 26109500360417996123535570591124272793452916576419228549884307472560166112225, 'HMACI': '152bfeedda16804564af73c94b9c026a15d6bf5ebcbd0c539aad3e846433db82'}
OTK with ID number 6 is registered successfully
b'W\xbc[\xc2\xda\xb5\x8f\x1eNb\x91,G\x88\xb32\xf0\xdd\xb5\xc6\xc7\xa2f\xaa\xe4\xb6\xc9x\xd5\x95\x92\x11'
OTK_Pub: (0xb6278a1303d45269c30aa8b072696ec1090244fc760fe6f0d7acceffbffb04d7 , 0x6e05a75c13863732ab64312a7a08743094351ac30bdc340a19ef8289e75277b3) OTK_Priv: 76184714938831839654203722061902579562318086475074906014687763369555230563819
Sending message is:  {'ID': 27960, 'KEYID': 7, 'OTKI.X': 82390798431318964495804981796611853378296658899059155591953995059861221213399, 'OTKI.Y': 49764402653494348688747809077586291830782750133640790118359234224510169413555, 'HMACI': '2d45025168b9c7cd2a26e0fef171b8a448ccd8be6575e99b1012b20b64f3ee55'}
OTK with ID number 7 is registered successfully
b'W\xbc[\xc2\xda\xb5\x8f\x1eNb\x91,G\x88\xb32\xf0\xdd\xb5\xc6\xc7\xa2f\xaa\xe4\xb6\xc9x\xd5\x95\x92\x11'
OTK_Pub: (0xddde7a72cd35b97f53cae9e1169ae968f315695f96f938e160219aeb59c7c04a , 0xaef0388482d02a58d3fe4434f9dd68a569561f0caa922712778ce4ca9330ef69) OTK_Priv: 115224233882503269267007926621981313444284743336696954508626411867788990051623
Sending message is:  {'ID': 27960, 'KEYID': 8, 'OTKI.X': 100354224693382022465850561978982301474747070203033630454236964466944018726986, 'OTKI.Y': 79126869019319776354388951924105574640759636038869579046834811909850482667369, 'HMACI': 'e03cea0bebcdec4f92912d5d6f113c57665417e52d246ebe7897e2e9d1808903'}
OTK with ID number 8 is registered successfully
b'W\xbc[\xc2\xda\xb5\x8f\x1eNb\x91,G\x88\xb32\xf0\xdd\xb5\xc6\xc7\xa2f\xaa\xe4\xb6\xc9x\xd5\x95\x92\x11'
OTK_Pub: (0xd2dab616d996dc3a1eafe297f7f65003d03bf1daef497574ee8e09a4074ae68c , 0xa150c711af37cbfab43233bde3eec4acdea81014195a957615cd5f754c4018b9) OTK_Priv: 69158815612795139724503423557646496597536775504967954920342650753366408675071
Sending message is:  {'ID': 27960, 'KEYID': 9, 'OTKI.X': 95372127596476399506341157781994586505317349212549641164446857483104415311500, 'OTKI.Y': 72965090311382868450003917858496242162895518234291708756050797402467162134713, 'HMACI': 'dba0346f2e2fb948bc5dcf2203e60324d190b07359524569ea52888259127532'}
OTK with ID number 9 is registered successfully
'''


#PHASE-2
#Pseudo-client will send you 5 messages to your inbox via server when you call this function
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


h = 75760430931182321293698420106004396367306357132290413229608408107910471862875
s = 40313791308174071354016793170035970006984318844567172773965395444247843115352

'''
messages = PseudoSendMsg(h,s) 
first_message = ReqMsg(h,s) 
first_message = {'IDB': 18007, 'OTKID': 0, 'MSGID': 1, 'MSG': 61028018484805796230260896009169131109893512211154779243703529038874682645214465692499874390019325646911020959271399301446261614498741624880565865971360371020818774989874615002492575757887915127545001, 'IK.X': 47152521721929048576835233048131082052837378382754191750807960678031815670051, 'IK.Y': 21607448093224984998827691156606805883380972680266521549245559135655451173805, 'EK.X': 87667642166793354522007699941182035073271754556576185236091474380992828102853, 'EK.Y': 44243311074133191299988586115323755733722982189892432091609384673666584608330}
'''
IKS_Pub = [47152521721929048576835233048131082052837378382754191750807960678031815670051, 21607448093224984998827691156606805883380972680266521549245559135655451173805]
EKS_Pub = [87667642166793354522007699941182035073271754556576185236091474380992828102853, 44243311074133191299988586115323755733722982189892432091609384673666584608330]
otk1_priv = 59695232315866645350524632214997374447013498209719735140639879586940923732993
session_key = b'\xaf\xfa\xa3rw\n"\xe4\xf6\x17\xe5\xa3\xdf"\x11\x8fNv\x06\x1b\x07\x17\xa5:\x14D\xe1\x08\xac#\n\xa2'

'''
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
    
session_key = generate_sk(otk1_priv)
'''

def generate_kdf(kdf):
    U = kdf + b'JustKeepSwimming'
    kenc = SHA3_256.new(U).digest()
    U2 = kdf + kenc + b'HakunaMatata'
    khmac = SHA3_256.new(U2).digest()
    U3 = kenc + khmac + b'OhanaMeansFamily'
    kdf_next = SHA3_256.new(U3).digest()
    return kenc, khmac, kdf_next

'''
kenc, khmac, kdf_next = generate_kdf(session_key)
print("session_key:", session_key, "kenc:", kenc, "khmac:", khmac, "kdf_next:", kdf_next)
message1 = 61028018484805796230260896009169131109893512211154779243703529038874682645214465692499874390019325646911020959271399301446261614498741624880565865971360371020818774989874615002492575757887915127545001
'''

kenc = b'\x85z\xddR\x19w\x01\xe7\x82\xdc\x04\xc6\xed\xf8z\x06a\x00\xf0\x00\x9b\x83~L\xf3/\xfb\xba9D\xc0\xca' 
khmac= b'\x97c*o\x9d6\x16#\x98\xc4z\x9f\x9bp\xd6\xf2F\xf9\xe9\xbcC\xb6\xdbh\xc7\xa4\xc2%a\xbe\xff\xe5' 
kdf_next= b'\x02\xda\xe1\xce\x01\x9a\xbc\xc9\xec\x03\xf6\x05\x92\xe0\x05\x14bv\x7f\x9fi\x0eN\xfcZ\xffy\x89a\xb5\xe0p'

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
    else:
        print("false!")
        Checker(27960,18007,id,'INVALIDHMAC')
        
messages = (61028018484805796230260896009169131109893512211154779243703529038874682645214465692499874390019325646911020959271399301446261614498741624880565865971360371020818774989874615002492575757887915127545001, 57353838391302472098690251504966575075333399372516860905890359162319395220344233167836824397487049173481338470133280807384341606781440006889990272992020982723075424734678584638665806951348143154958158, 54293913455658785950963846196581662949055438416061121460313992843273548043466341090116614227033743073614267341258814081548516828213453958356371462181730401444114229461457261130793334686190167081427849, 23703715743293701051449792539741120088908630605385520366686641419729176314092937101745336379694127553770223238091810577196650875939973444880684805094054338676044968441938477765310927397149411362354540, 5008290859360788662862442724673677593188729971208739247679972203417660807517922280453687943957519225070214734258791045148603827127737273666352046271703711788969370038778497450478493380574206209880771)

'''
first_message = messages[0]
second_message = messages[1]
third_message = messages[2]
fourth_message = messages[3]
fifth_message = messages[4]

kenc2, khmac2, kdf_next2 = generate_kdf(kdf_next)
kenc3, khmac3, kdf_next3 = generate_kdf(kdf_next2)
kenc4, khmac4, kdf_next4 = generate_kdf(kdf_next3)
kenc5, khmac5, kdf_next5 = generate_kdf(kdf_next4)

encrypted = encrypt_msg(first_message, khmac, kenc, 1) #https://www.youtube.com/watch?v=Xnk4seEHmgw
encrypted2 = encrypt_msg(second_message, khmac2, kenc2, 2) #https://www.youtube.com/watch?v=CvjoXdC-WkM
encrypted3 = encrypt_msg(third_message, khmac3, kenc3, 3) #https://www.youtube.com/watch?v=mJXUNMexT1c
encrypted4 = encrypt_msg(fourth_message, khmac4, kenc4, 4)
encrypted5 = encrypt_msg(fifth_message, khmac5, kenc5, 5) #https://www.youtube.com/watch?v=1hLIXrlpRe8
'''

'''
deleted = ReqDelMsg(h,s)
'''

print("Checking whether there were some deleted messages!! ")
print("==========================================")
print("Message 1 - Was deleted by sender - X")
print("Message 2 - Was deleted by sender - X")
print("Message 3 - https://www.youtube.com/watch?v=mJXUNMexT1c - Read")
print("Message 5 - Was deleted by sender - X")