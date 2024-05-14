import random, time, os, hashlib, json


# 密码随机
class PassWordRandom():

    def __init__(self):
        random.seed(time.time())
        self.Nums = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        self.Chars = [
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
            'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
            'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
        ]
        self.Others = [
            '~', '!', '@', '#', '$', '%', '^', '&', '*', '?', '_', '-'
        ]

    def randomPassword(self, psw_len=8, n=True, o=False):
        _all_chars = self.Chars.copy()
        new_ps_array = []
        if n:
            r = random.randint(0, len(self.Nums) - 1)
            new_ps_array.append(self.Nums[r])
            for one in self.Nums:
                _all_chars.append(one)

        if o:
            r = random.randint(0, len(self.Others) - 1)
            new_ps_array.append(self.Others[r])
            for one in self.Others:
                _all_chars.append(one)

        all_chars_size = len(_all_chars)
        # print("new_ps_array: ", new_ps_array)
        for _ in range(psw_len):
            r = random.randint(0, all_chars_size - 1)
            new_ps_array.append(_all_chars[r])

        _all_chars.clear()
        # print("new_ps_array 2: ", new_ps_array)
        random.shuffle(new_ps_array)
        new_ps_str = ''.join(new_ps_array)
        return new_ps_str


# 密文数据
class EnCryptData():

    def __init__(self):
        self.md5_check = ""  # 明文秘钥转为MD5后存储使用
        self.rsa_public_key = ""  # 这里为密文
        self.rsa_private_key = ""  # 这里为密文
        self.encrypte_json = None  # json数据

    def loadEnCrypteFile(file_path=""):
        if file_path == "":
            return False, "请选择数据文件!"

        if os.path.isfile(file_path):
            return False, "错误的文件路径, 请重新选择!"

    def checkMd5():
        return True


# 测试
def test():
    # md5 = hashlib.md5()
    # md5.update("1".encode())
    # md5_str = md5.hexdigest()
    # print("1: ", md5.hexdigest())
    # f = open("./test.ecdb", "wb")
    # if f:
    #     f.seek(32)
    #     f.write("1".encode())
    #     f.seek(0)
    #     f.write(md5_str.encode())
    #     f.close()

    # f = open("./test.ecdb", "rb")
    # if f:
    #     md5_str = f.read(32)
    #     data_str = f.read()
    #     md5.update(data_str)
    #     print("md5_str: ", md5_str.decode())
    #     print("md5.hexdigest(): ", md5.hexdigest())
    #     f.close()

    pwr = PassWordRandom()
    print(pwr.randomPassword(8, True, True))
    print(pwr.randomPassword(8, True, False))
    print(pwr.randomPassword(8, True))


if __name__ == "__main__":
    test()
