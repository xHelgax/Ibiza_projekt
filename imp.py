from random import *

def KibEuk(a, b):
    x0, x1, y0, y1, s = 1, 0, 0, 1, 1
    while(b != 0):
        r = a%b
        q = a//b
        x, y = x1, y1
        x1 = q*x1+x0
        y1 = q*y1+y0
        x0, y0 = x, y
        s = -s
        a, b = b, r
    x = s*x0
    y = -s*y0
    d, x, y = a, x, y
    return(d, x, y)
    

'''def GyorsHatvany(a, x, m):
    a = a%m
    if x == 0:
        return 1
    elif x == 1:
        return a
    elif x%2==0:
        return GyorsHatvany(a*a%m, x//2, m)
    else:
        return a*GyorsHatvany(a, x-1, m)%m'''

def GyorsHatvany(a, x, m):
    eredmeny = 1
    a %= m
    while x > 0:
        if x % 2 == 1:       
            eredmeny = (eredmeny * a) % m
        a = (a * a) % m        
        x //= 2                
    return eredmeny

def KinaiMaradek(p, q, c, d):
    m = p*q
    cp = GyorsHatvany(c, d % (p - 1), p)
    cq = GyorsHatvany(c, d % (q - 1), q)
    [d, yp, yq] = KibEuk(q, p)
    a = (cp*yp*q)+(cq*yq*p)
    return a%m

def MillerRabin(n, a)-> bool:
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    x = GyorsHatvany(a, d, n)
    if x == 1 or x == n - 1:
        return True
    for _ in range(s - 1):
        x = (x * x) % n
        if x == n - 1:
            return True
    return False


#RSA
#1. lépés
p = 0
q = 0
while not MillerRabin(p, 29):
    p = randint(100, 10000)
while (not MillerRabin(q,29)) or (q==p):
    q = randint(100, 10000)
#2. lépés
n = p*q
fn = (p-1)*(q-1)
#3. lépés
e = 65537
g, xk, yk = KibEuk(e, fn)
if g != 1:
    while True:
        e = randint(3, fn - 1)
        if e % 2 == 0:
            e += 1
        g, xk, yk = KibEuk(e, fn)
        if g == 1:
            break
w, x_inv, y_tmp = KibEuk(e, fn)
d = x_inv % fn

#Titkosítás
m = 18
c = GyorsHatvany(m, e, n)
print('Titkos üzenet:', c)
vissza = KinaiMaradek(p, q, c, d)
print('A nyílt üzenet:', vissza)
#Aláírás
dp = d % (p - 1)
dq = d % (q - 1)
sp = GyorsHatvany(m, dp, p)
sq = GyorsHatvany(m, dq, q)
g, yp, yq = KibEuk(q, p)
sign = (sp * yp * q + sq * yq * p) % n
print('Az aláírás:', sign)
ver = GyorsHatvany(sign, e, n)
print('Ellenőrzés:', ver)
if ver == m:
    print("True")
else:
    print("False")


