import base64
from Crypto.Cipher import AES

AES_BLOCK_SIZE = AES.block_size
AES_KEY_SIZE = 16


# 补足到定长数据
def AES_PadValue(val: str):
    byte_val = val.encode()
    while len(byte_val) % AES_KEY_SIZE != 0:
        byte_val += ' '.encode()
    return byte_val


# 获取制定长度的秘钥
def AES_PadKey(ps_key: str):
    byte_key = ps_key.encode()
    if len(byte_key) > AES_KEY_SIZE:
        return byte_key[:AES_KEY_SIZE]

    while len(byte_key) % AES_KEY_SIZE != 0:
        byte_key += ' '.encode()
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


# 测试
def test():
    ps_key = "hello world!"
    ps_val = "hi every body!"

    encrypt_val = AES_EnCrypt(ps_key, ps_val)
    decrypt_val = AES_DeCrypt(ps_key, encrypt_val)
    print("encrypt_val: ", encrypt_val)
    print("decrypt_val: ", decrypt_val.decode())

    encrypt_val = base64.b64encode(encrypt_val)
    decrypt_val = AES_DeCrypt(ps_key, base64.b64decode(encrypt_val))
    print("encrypt_val: ", encrypt_val.decode())
    print("decrypt_val: ", decrypt_val.decode())


print("__name__", __name__)
if __name__ == "__main__":
    test()
