import random, time, os, hashlib, json, logging
import AES_Interface
import RSA_Interface


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
        self.secret_key = ""  # 秘钥
        self.secret_key_changed = True  # 秘钥是否变化
        self.rsa_public_key = ""  # 这里为密文
        self.rsa_private_key = ""  # 这里为密文
        # encrypte_json: 数据结构 {
        # "rsa":{"pk": publick_key, "rk": private_key}, 使用秘钥加密(aes)
        # "checks": {校验密码字符串1, 校验密码字符串2}, 字符串1使用秘钥加密， 字符串2使用非对称加密(ras)
        # "account_pw":[{"l":地址, "a":账号, "p": 密码, "o":其他数据}]}
        self.encrypte_json = None  # json数据
        self.encrypte_file_path = ""  # 文件路径
        self.encrypte_file_path_changed = True  # 文件名是否修改过
        self.checks = ["i96z5~13&o1W&Sv4gD",
                       "B#6@RdZmQUW?nxKdqJ"]  # 这个只能增加不能修改, 并且顺序不能变

    # 校验文件数据是否正确
    def checkFileMd5(self, md5_str: str, file_data: bytes):
        md5 = hashlib.md5()
        md5.update(file_data)
        check_str = md5.hexdigest()
        return (md5_str == check_str)

    def checkSecretKey(self):
        first_str = self.checks[0]
        second_str = self.checks[1]
        if self.encrypte_json is None or self.encrypte_json[
                "checks"] is None or len(self.encrypte_json["checks"]) != 2:
            return False, "数据文件异常!"

        first_check_str = AES_Interface.AES_DeCrypt(
            self.secret_key, self.encrypte_json["checks"][0])
        if first_str != first_check_str:
            return False, "秘钥校验失败"

        self.rsa_public_key = AES_Interface.AES_DeCrypt(
            self.secret_key, self.encrypte_json["rsa"]["pk"])
        self.rsa_private_key = AES_Interface.AES_DeCrypt(
            self.secret_key, self.encrypte_json["rsa"]["rk"])
        second_check_str = RSA_Interface.RSA_DeCrypt(
            self.secret_key, self.encrypte_json["checks"][1])
        if first_str == first_check_str and second_str == second_check_str:
            return True
        else:
            return False, "秘钥校验失败"

    # 解析数据
    def parseEncrypteData(self, data_bytes: bytes):
        try:
            json_root = json.loads(data_bytes)
            self.encrypte_json = json_root

        except Exception as e:
            print("except Exception:", e)
            logging.exception(e)
        return False, "配置数据解析失败"

    # 加密文件加载
    def loadEncrypteFileData(self, force_load: False):
        if self.encrypte_file_path_changed or force_load:
            if self.encrypte_file_path == "":
                return False, "请选择数据文件!"

            if os.path.isfile(self.encrypte_file_path):
                return False, "错误的文件路径, 请重新选择!"
            self.encrypte_file_path_changed = False
            ef = open(self.encrypte_file_path, "rb")
            if ef:
                file_md5_bytes = ef.read(32)  # md5码校验数据
                data_bytes = ef.read()  # 数据块
                if self.checkMd5(file_md5_bytes.decode(), data_bytes):
                    return self.parseEncrypteData(data_bytes)
                else:
                    return False, "加密文件数据被修改"
            else:
                return False, "文件打开失败"

    def changeEncrypteFile(self, file_path):
        if file_path != self.encrypte_file_path:
            self.encrypte_file_path = file_path
            self.encrypte_file_path_changed = True

    def changeSecretkey(self, new_sk):
        if new_sk != self.secret_key:
            self.secret_key = new_sk
            self.secret_key_changed = True

    def saveAccountInfo(self, addr: str, account: str, password: str,
                        other: str):
        if self.encrypte_file_path_changed:
            ok, err = self.loadEncrypteFileData()
            if not ok:
                return ok, err
            ok, err = self.checkFileMd5()
            if not ok:
                return ok, err
            ok, err = self.checkSecretKey()
            if not ok:
                return False, err
            self.encrypte_file_path_changed = False
            self.secret_key_changed = False

        if self.secret_key_changed:
            ok, err = self.checkSecretKey()
            if not ok:
                return False, err


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
