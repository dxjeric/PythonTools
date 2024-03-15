# encoding: utf8

import sys,os,ftplib,socket

def main():
    shape2name = {1: "方", 2: "梅", 3: "红", 4: "黑", 5: "王",}
    num2name = {3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9", 10: "10", 11: "J", 12: "Q", 13: "K", 14: "A", 15: "X", 16: "Y", 17: "东", 18: "南", 19: "西", 20: "北", 21: "中"}
    all_cards = [[518,1295,260,261,264,259,788,262,788,265], [1295,523,519,260,519,523,523,519,260,519],[521,525,1296,517,517,268,515,515,515,517],[1296,520,520,265,1045,265,520,520,1045,1045]]
    for cards in all_cards:
        card_str = ""
        for seq in cards:
            s = seq >> 8
            n = seq & ((1 << 8) -1)
            card_str += (shape2name[s] + num2name[n] + ", ")
        print("cards: ", cards, "card_str: ", card_str)


if __name__ == "__main__":
	main()
