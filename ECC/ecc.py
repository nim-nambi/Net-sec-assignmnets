import collections
import random

elliptic_c = collections.namedtuple('elliptic_c', 'name p a b g n h')
# here we define our elliptic curve

curve = elliptic_c(
    'secp256k1', # curve type
    p=0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f,
    # Curve coefficients.
    a=0,
    b=7,
    g=(0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798, 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8),
    n=0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141,
    h=1,
)

def _inverse_mod(k, p):
    
    if k == 0:
        raise ZeroDivisionError('division by zero') 

    if k < 0:
       return p - _inverse_mod(-k, p) 

    # Extended Euclidean algorithm
    s, o_s = 0, 1
    t, o_t = 1, 0
    r, o_r = p, k

    while r != 0:
        quotient = o_r // r
        o_r, r = r, o_r - quotient * r
        o_s, s = s, o_s - quotient * s
        o_t, t = t, o_t - quotient * t

    gcd, x, y = o_r, o_s, o_t

    assert gcd == 1
    assert (k * x) % p == 1

    return x % p

def _is_on_curve(point):
    
    if point is None:
        return True

    x, y = point

    return (y * y - x * x * x - curve.a * x - curve.b) % curve.p == 0

def _point_neg(point):
    
    assert _is_on_curve(point)

    if point is None:
        # -0 = 0
        return None

    x, y = point
    result = (x, -y % curve.p)

    assert _is_on_curve(result)

    return result

def _point_add(point1, point2):
    
    assert _is_on_curve(point1)
    assert _is_on_curve(point2)

    if point1 is None:
        return point2
    if point2 is None:
        return point1

    x1, y1 = point1
    x2, y2 = point2

    if x1 == x2 and y1 != y2:
        return None

    if x1 == x2:
        m = (3 * x1 * x1 + curve.a) * _inverse_mod(2 * y1, curve.p)
    else:
        m = (y1 - y2) * _inverse_mod(x1 - x2, curve.p)

    x3 = m * m - x1 - x2
    y3 = y1 + m * (x3 - x1)
    result = (x3 % curve.p,
              -y3 % curve.p)

    assert _is_on_curve(result)

    return result

def _scalar_mult(k, point):
    
    assert _is_on_curve(point)

    if k % curve.n == 0 or point is None:
        return None

    if k < 0:
        return _scalar_mult(-k, _point_neg(point))

    result = None
    addend = point

    while k:
        if k & 1:
            result = _point_add(result, addend)

        addend = _point_add(addend, addend)

        k >>= 1

    assert _is_on_curve(result)

    return result

# Keypair generation and ECDHE
def _make_keypair():
    # Generate random private-public key pair
    private_key = random.randrange(1, curve.n)
    public_key = _scalar_mult(private_key, curve.g)

    return private_key, public_key

print('Curve:', curve.name)

# Nirmal generates his own key-pair.
Nirmal_private_key, Nirmal_public_key = _make_keypair()
print("Nirmal's private key:", hex(Nirmal_private_key))
print("Nirmal's public key: (0x{:x}, 0x{:x})".format(*Nirmal_public_key))

# Arhum generates his own key-pair.
Arhum_private_key, Arhum_public_key = _make_keypair()
print("Arhum's private key:", hex(Arhum_private_key))
print("Arhum's public key: (0x{:x}, 0x{:x})".format(*Arhum_public_key))

# Nirmal and Arhum now exchange their public keys and verify the shared secret
s1 = _scalar_mult(Nirmal_private_key, Arhum_public_key)
s2 = _scalar_mult(Arhum_private_key, Nirmal_public_key)
assert s1 == s2

print('Shared secret: (0x{:x}, 0x{:x})'.format(*s1))