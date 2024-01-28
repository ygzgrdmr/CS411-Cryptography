# use "pip install sympy" if sympy is not installed
import random
import sympy
import warnings

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

# Encryption
def Enc(message, h, q, p, g): # m is the message
    m = int.from_bytes(message, byteorder='big')
    k = random.randint(1, 2**16-1)
    r = pow(g, k, p)
    t = (pow(h, k, p)*m)%p
    return r, t

# Decryption
def Dec(r, t, s, q, p, g):
    m = (pow(r, q-s, p)*t)%p
    return m.to_bytes((m.bit_length()+7)//8, byteorder='big')

q = 20229678282835322453606583744403220194075962461239010550087309021811
p = 12515043909394803753450411022649854273721537251011107748826811168459680628351391154487041320595006736239332192492236943966523053744476127728797963808151142506595330120621663371518281181204797831707349436558443139355672347825267728879376289677517268609959671235059224994785463608330669494457163250373581380036247652030969481046772013799271268710104487022164865004802864076066974153012125551060906054112920469869045223329577015935824864428612446723942040465300185917923305042033306319809712618872063796904132788285518497999327485929730921202745935936913834577610254298809205575162005025170878200786590751850006857921419
g = 2256483143741433163413007675067934542893022968337437312283381964942344365449719628255630752397325376452002398784394008507857025386943645437696558240874471345442532398588406749907930002481624160959132193798842426822193910104962138845873425590946341754334144292886002962901550160578482452138075339294826241799645761655320983735381974177635207208471824667516956679913974643342159550037320378814445802296879470561504511689460916200417902612323039671250567503846175990654512915878143201233050978046269551126178155060158781645062181955781969136435905570787457855530003987887049118699525033120811790739590564684316550493132
h =  1265126138933377994348793193477342224736956600354964713945582205290651827674605003741290400826146165752452701594226002213036650208863340321329798489264160728930653315907521926136642928347549825144026262035747350182493795559385070130959552499813885202334575993642935128132458545523498489490586883187848396314164874056757696154989511633927620869557222556876855999079308839417416012746206040455611002092520255736121673298963050693639916367968280807028975614596114022230524360150581344884219834519025619777858430431159461562871537004523472161672182851052258466610762884570310894027628303901161674783788320479747219000276

r = 3813677439444837990381281624769265484071989883494833765363155214071727573627590213038823018054653614040833306533736593789523636716088751609591517852868217052905415751457961942309213803782661174042131067555996860094296315483087375444362454092891960492098796234624392186112659124915872546640723139762874453050592110272036917039293020539724872406856066252779419482651672320132092421939867392668795959155312634804888215300607725584330531720210355201550529764936881761210810883102986464111409096572364185502722477587178710137175828696000683028806920671859797982157383943866111320227830105178421690303627627943337128795446
t = 6879085872532883496679637289827758044388493592192276485018420467127175692447676225327570450845191312409829734608730732636786181351723791499758734679978259974439564271116431478559920406924286698115291434529879801947864012484928324116410562713859998987659607317050575329142948832616264096105332977657905567987590712241261025634719542322903245193802690474499323009626862853070359755324776198222903161231737321083180819484704533141360402185872920868401635784923300080366065601626511550338585716446732854372219141954019480903146819295527105219685774367349234762081116514728907468721241055649461751711410066128218786241602




for k in range(1,2**16-1):
    if r == pow(g, k, p):
        print("K is found:",k)
        break


k = 31659 # found in the for loop above.
m = (t * modinv(pow(h, k, p), p)) % p
print(m)

m_bytes = m.to_bytes((m.bit_length() + 7) // 8, 'big')
print("Answer:",m_bytes)


