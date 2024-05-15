import json


def main():
    file_path = r"F:\迅雷下载\books.json"
    f = open(file_path, "r")
    json_root = json.load(f)

    left_size = 0
    for i in range(len(json_root) - 1, -1, -1):
        left_size += json_root[i]["size"]
        json_root[i]["left"] = int(left_size * 100) / 100
        # print("item: ", type(json_root[i]), json_root[i])

    # print("json_root: ", type(json_root), json_root)
    f = open(file_path, "w")
    json.dump(json_root, f)
    print("finish!")


if __name__ == "__main__":
    main()
