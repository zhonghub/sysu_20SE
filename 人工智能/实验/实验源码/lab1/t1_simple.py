#回文字符串: 不论是从左往右，还是从右往左，字符的顺序都是一样的（如aba,abcba,abba等）
#本题中的回文字符串只考虑数字和字母（不考虑大小写???），不考虑其他字符
def is_curcle(ss): #判断ss是否为回文字符串
    return ss == ss[::-1]


def num_or_char(s0): #判断s0是否为数字或字符
    key = ord(s0)
    if 48 <= key and key <= 57\
        or 65 <= key and key <= 90\
        or 97 <= key and key <= 122:
        return True
    else:
        return False


s0 = "s0"
while s0 != "": #当输入字符串为空时停止
    s0 = input()
    if s0 == "":
        break
    s0_len = len(s0)
    s1 = ""
    #将s0转化为只含数字和字母的字符串并保存在s1中
    for i in range(s0_len):
        if num_or_char(s0[i]):
            s1 = s1 + s0[i]
    #print(s1)
    if is_curcle(s1):
        print("True")
    else:
        print("False")

#A man, a plan, a canal: Panama - False
#race a car - False
#1111111111111111111121111111111111111111 - False
