import random


class PointOnCurve(object):
    def __init__(self, x, y, curve):
        self.x = x
        self.y = y
        self.curve = curve

    def __neg__(self):
        return PointOnCurve(self.x, -self.y % self.curve.p, self.curve)

    def __add__(self, other):
        if other is None:
            return self
        if self.x != other.x:
            # Regular
            m = (self.y - other.y) * pow(self.x - other.x, -1, self.curve.p)
        else:
            # Two points are the same
            m = (self.x * self.x * 3 + self.curve.a) * pow(self.y * 2, -1, self.curve.p)
        new_x = (m * m - self.x - other.x) % self.curve.p
        new_y = (self.y + m * (new_x - self.x)) % self.curve.p
        return PointOnCurve(new_x, new_y, self.curve)


class EllipticCurve(object):
    def __init__(self, p, a, b, g, n, h):
        self.p = p
        self.a = a
        self.b = b
        self.g = PointOnCurve(g[0], g[1], self)
        self.n = n
        self.h = h

    def scalar_multiply(self, scalar, point):
        if scalar < 0:
            # if scalar < 0, we need to inverse the calculation by -scalar * -point
            return self.scalar_multiply(-scalar, -point)
        prev_point = point
        final_point = None
        while scalar:
            if scalar & 1:
                # Odd
                final_point = prev_point + final_point
            prev_point = prev_point + prev_point
            scalar >>= 1
        return final_point


class ECDSA(object):
    def __init__(self, curve):
        self.curve = curve

    def keygen(self):
        # [1, n - 1]
        new_private_key = random.randrange(1, self.curve.n)
        new_public_key = self.curve.scalar_multiply(new_private_key, self.curve.g)
        return new_private_key, new_public_key

    def sign(self, message):
        # TODO
        pass

    def verify(self, r, s, message, public_key):
        # TODO
        pass


# Start Testing
secp256k1 = EllipticCurve(
    p=0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f,
    a=0,
    b=7,
    g=(0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,
       0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8),
    n=0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141,
    h=1,
)
ecdsa = ECDSA(secp256k1)

my_private_key, my_public_key = ecdsa.keygen()
print('Private key: {private_key}'.format(private_key=hex(my_private_key)))
print('Public key: ({x}, {y})'.format(x=hex(my_public_key.x), y=hex(my_public_key.y)))

# m = 'Hello world!'
# r, s = ecdsa.sign(m)
#
# print('Signature of message: "{message}" generated.\nr: {r}\ns: {s}'.format(message=m, r=hex(r), s=hex(s)))
# verification_result = ecdsa.verify(r, s, m, my_public_key)
# print(f'Result of signature verification: {verification_result}.')
