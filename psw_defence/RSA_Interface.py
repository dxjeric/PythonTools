import base64, logging
from Crypto import Random
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES


# 加密
def RSA_EnCrypt(rsa_public_key: str, val: str):
    try:
        rsa_public_key = rsa_public_key.encode()
        rsakey = RSA.importKey(rsa_public_key)
        cipher = Cipher_pkcs1_v1_5.new(rsakey)
        val = val.encode()
        cipher_text = base64.b64encode(cipher.encrypt(val))
        return True, cipher_text.decode()
    except Exception as e:
        logging.exception(e)
        return False, ""


# 解密
def RSA_DeCrypt(rsa_private_key: str, aes_val: str):
    try:
        rsa_private_key = rsa_private_key.encode()
        rsakey = RSA.importKey(rsa_private_key)
        cipher = Cipher_pkcs1_v1_5.new(rsakey)
        aes_val = aes_val.encode()
        text = cipher.decrypt(base64.b64decode(aes_val), None)
        return True, text.decode()
    except Exception as e:
        logging.exception(e)
        return False, ""


# 生成新key
def RSA_RandomKey():
    rsa = RSA.generate(1024)
    rsa_private_key = rsa.exportKey()
    rsa_public_key = rsa.publickey().exportKey()
    return rsa_private_key.decode(), rsa_public_key.decode()


# 测试
def test():
    logging.basicConfig(
        level=logging.INFO,
        filename="demo.log",
        filemode="w",
        format=
        "[%(asctime)s] [%(levelname)s] %(message)s - %(filename)s:%(lineno)s",
        datefmt="%Y-%m-%d %H:%M:%S")

    rsa_val = "hi every body!"

    rsa_private_key, rsa_public_key = RSA_RandomKey()
    ok, encrypt_val = RSA_EnCrypt(rsa_public_key, rsa_val)
    ok, decrypt_val = RSA_DeCrypt(rsa_private_key, encrypt_val)

    print("rsa_private_key:\n{}\n".format(rsa_private_key))
    print("rsa_public_key:\n{}\n".format(rsa_public_key))
    print("encrypt_val: {}".format(encrypt_val))
    print("decrypt_val: {}".format(decrypt_val))
    print(rsa_val == decrypt_val)


if __name__ == "__main__":
    test()
