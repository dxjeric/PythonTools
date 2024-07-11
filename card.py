# encoding: utf8

import sys, os, ftplib, socket
import base64, logging


def main():
    shape2name = {
        1: "方",
        2: "梅",
        3: "红",
        4: "黑",
        5: "王",
    }
    num2name = {
        3: "3",
        4: "4",
        5: "5",
        6: "6",
        7: "7",
        8: "8",
        9: "9",
        10: "10",
        11: "J",
        12: "Q",
        13: "K",
        14: "A",
        15: "X",
        16: "Y",
        17: "东",
        18: "南",
        19: "西",
        20: "北",
        21: "中"
    }
    all_cards = [[777]]
    for cards in all_cards:
        card_str = ""
        for seq in cards:
            s = seq >> 8
            n = seq & ((1 << 8) - 1)
            print("cards: ", cards, "s: ", s, "n: ", n)
            # card_str += (shape2name[s] + num2name[n] + ", ")
        print("cards: ", cards, "card_str: ", card_str)


def tranMoney(bean):
    dws = ["", "万", "亿", "兆", "京"]
    beans = []
    qiuyu = 10000
    for i in range(5):
        dw = dws[i]
        v = bean % 10000
        if v > 0:
            beans.append("{}{}".format(v, dw))
        bean = int(bean / 10000)
        if bean <= 0:
            break

    beans.reverse()
    print("out: ", " ".join(beans))


if __name__ == "__main__":
    # main()
    tranMoney(1000000000)
