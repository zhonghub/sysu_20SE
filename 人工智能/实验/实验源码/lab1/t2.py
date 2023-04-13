"""
石头：Rock，剪刀：Scissors，布：Paper）
Player1 input: Rock
Player2 input: Paper
Congratulate Player2!
Try new game?
"""
keep = True
while keep:
    # print("Player1 input:")
    p1 = input("Player1 input: ")
    # print("Player2 input:")
    p2 = input("Player2 input: ")
    if (p1 == "Rock" and p2 == "Scissors")\
            or (p1 == "Scissors" and p2 == "Paper") \
            or (p1 == "Paper" and p2 == "Rock"):
        print("Congratulate Player1!")
    elif p1 == p2:
        print("No Winner!")     # 两人平局
    else:
        print("Congratulate Player2!")
    print("Try new game?")
    new_game = input()
    if new_game == "y":
        keep = True
    elif new_game == "n":
        keep = False
