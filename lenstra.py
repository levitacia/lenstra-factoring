import random
import math

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def modular_inverse(a, m):
    m0, x0, x1 = m, 0, 1
    if m == 1:
        return 0
    while a > 1:
        if m == 0:
            return 0
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += m0
    return x1 if gcd(a, m0) == 1 else 0

class EllipticCurve:
    def __init__(self, a, b, n):
        self.a = a
        self.b = b
        self.n = n

    def add(self, P, Q):
        if P == "infinity":
            return Q
        if Q == "infinity":
            return P
        if P[0] == Q[0] and P[1] != Q[1]:
            return "infinity"
        if P == Q:
            num = (3 * P[0]**2 + self.a) % self.n
            denom = (2 * P[1]) % self.n
        else:
            num = (Q[1] - P[1]) % self.n
            denom = (Q[0] - P[0]) % self.n

        if denom == 0 or gcd(denom, self.n) > 1:
            return gcd(denom, self.n)

        inv_denom = modular_inverse(denom, self.n)
        if inv_denom == 0:
            return gcd(denom, self.n)
        
        slope = (num * inv_denom) % self.n
        x_r = (slope**2 - P[0] - Q[0]) % self.n
        y_r = (slope * (P[0] - x_r) - P[1]) % self.n
        return (x_r, y_r)

    def multiply(self, P, k):
        Q = "infinity"
        while k:
            if k % 2 == 1:
                Q = self.add(Q, P)
                if isinstance(Q, int):
                    return Q
            P = self.add(P, P)
            if isinstance(P, int):
                return P
            k //= 2
        return Q

def lenstra_ecm(n, attempts=100):
    for _ in range(attempts):
        a = random.randint(0, n-1)
        x = random.randint(0, n-1)
        y = random.randint(0, n-1)
        b = (y**2 - x**3 - a*x) % n
        curve = EllipticCurve(a, b, n)
        P = (x, y)
        k = math.prod(range(1, 100))  # factorial of 9
        factor = curve.multiply(P, k)
        if isinstance(factor, int) and factor > 1 and factor < n:
            return factor
    return None


factor = lenstra_ecm(4453)
if factor is not None:
    print(f"Found factor: {factor}")
else:
    print("No factor found")
