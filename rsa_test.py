import base64, random, time
from Crypto import Random
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES

AES_BLOCK_SIZE = AES.block_size
AES_KEY_SIZE = 16


# 补足到定长数据
def AES_PadValue(val: str):
    byte_val = val.encode()
    while len(byte_val) % AES_KEY_SIZE != 0:
        byte_val += ''.encode()
    return byte_val


# 获取制定长度的秘钥
def AES_PadKey(ps_key: str):
    byte_key = ps_key.encode()
    if len(byte_key) > AES_KEY_SIZE:
        return byte_key[:AES_KEY_SIZE]

    while len(byte_key) % AES_KEY_SIZE != 0:
        byte_key += ''.encode()
    return byte_key


# 加密
def AES_EnCrypt(ps_key: str, psw: str):
    byte_key = AES_PadKey(ps_key)
    aes_cipher = AES.new(byte_key, AES.MODE_ECB)
    ase_val = AES_PadValue(psw)
    out_psw = aes_cipher.encrypt(ase_val)
    return out_psw


# 解密
def AES_DeCrypt(ps_key: str, aes_byte_psw: bytes):
    byte_key = AES_PadKey(ps_key)
    aes_cipher = AES.new(byte_key, AES.MODE_ECB)
    out_src_val = aes_cipher.decrypt(aes_byte_psw)
    return out_src_val


def r_key(size: int) -> bytes:
    str = ""
    for i in range(size):
        i = random.randrange(0, 6)
        str += all_char[i]
    str = Random.new().read(size)
    print("size: ", size, "str: ", str)
    return str


def test(key=None):
    f = None
    if key is None:
        random.seed(time.time())
        # f = open("time.txt", "w")
    else:
        random.seed(key)
        # f = open(r"{}.txt".format(key), "w")

    random_generator = Random.new().read
    rsa = RSA.generate(1024, r_key)
    rsa_private_key = rsa.exportKey()
    rsa_public_key = rsa.publickey().exportKey()
    # f.write(rsa_private_key.decode())
    # f.write(rsa_public_key.decode())
    # f.close()
    print(rsa_private_key.decode())
    # print(rsa_public_key.decode())

    # message = b"hello world!"
    # rsakey = RSA.importKey(rsa_public_key)
    # cipher = Cipher_pkcs1_v1_5.new(rsakey)
    # cipher_text = base64.b64encode(cipher.encrypt(message))
    # print(cipher_text)

    # rsakey = RSA.importKey(rsa_private_key)
    # cipher = Cipher_pkcs1_v1_5.new(rsakey)
    # random_generator = Random.new().read
    # text = cipher.decrypt(base64.b64decode(cipher_text), None)
    # print(text.decode('utf8'))


def main():
    test()


main()
