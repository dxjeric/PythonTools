import random, time


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

    def random_password(self, psw_len=8, n=True, o=False):
        _all_chars = self.Chars
        if n:
            for one in self.Nums:
                _all_chars.append(one)

        if o:
            for one in self.Others:
                _all_chars.append(one)

        all_chars_size = len(_all_chars)
        new_ps_str = ""
        for _ in range(psw_len):
            r = random.randint(0, all_chars_size - 1)
            one = _all_chars[r]
            new_ps_str += one

        _all_chars.clear()
        return new_ps_str


# 密文数据
class EnCryptData():

    def __init__(self):
        self.md5_check = ""  # 明文秘钥转为MD5后存储使用
        self.rsa_public_key = ""  # 这里为密文
        self.rsa_private_key = ""  # 这里为密文
        self.encrypte_json = None  # json数据


# 测试
def test():
    pwr = PassWordRandom()
    print(pwr.random_password(8, True, True))
    print(pwr.random_password(8, True, False))
    print(pwr.random_password(8, True))


if __name__ == "__main__":
    test()
