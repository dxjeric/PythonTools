import base64, traceback, logging
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
def AES_PadKey(aes_key: str):
    byte_key = aes_key.encode()
    if len(byte_key) > AES_KEY_SIZE:
        return byte_key[:AES_KEY_SIZE]

    while len(byte_key) % AES_KEY_SIZE != 0:
        byte_key += ' '.encode()
    return byte_key


# 加密
def AES_EnCrypt(aes_key: str, val: str):
    try:
        byte_key = AES_PadKey(aes_key)
        aes_cipher = AES.new(byte_key, AES.MODE_ECB)
        ase_val = AES_PadValue(val)
        out_val_text = base64.b64encode(aes_cipher.encrypt(ase_val))
        return True, out_val_text.decode()
    except Exception as e:
        logging.exception(e)
        return False, ""


# 解密
def AES_DeCrypt(aes_key: str, ase_val: str):
    try:
        byte_key = AES_PadKey(aes_key)
        aes_cipher = AES.new(byte_key, AES.MODE_ECB)
        ase_val = ase_val.encode()
        ase_val_byte = base64.b64decode(ase_val)
        out_src_val = aes_cipher.decrypt(ase_val_byte)
        return True, out_src_val.decode()
    except Exception as e:
        logging.exception(e)
        return False, ""


# 测试
def test():
    logging.basicConfig(
        level=logging.INFO,
        filename="demo.log",
        filemode="w",
        format=
        "[%(asctime)s] [%(levelname)s] %(message)s - %(filename)s:%(lineno)s",
        datefmt="%Y-%m-%d %H:%M:%S")
    aes_key = "hello world!"
    aes_val = "hi every body!"

    ok, encrypt_val = AES_EnCrypt(aes_key, aes_val)
    ok, decrypt_val = AES_DeCrypt(aes_key, encrypt_val)
    print("encrypt_val: {}".format(encrypt_val))
    print("decrypt_val: ", decrypt_val)


if __name__ == "__main__":
    test()
