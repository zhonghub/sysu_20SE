import sys

from Game import *
from Dot import *
from ChessBoard import *
import ChessAI as He
import MyAI as Me


def main():
    # 初始化pygame
    pygame.init()
    # 创建用来显示画面的对象（理解为相框）
    screen = pygame.display.set_mode((750, 667))
    # 游戏背景图片
    background_img = pygame.image.load("images/bg.jpg")
    # 游戏棋盘
    # chessboard_img = pygame.image.load("images/bg.png")
    # 创建棋盘对象
    chessboard = ChessBoard(screen)
    # 创建计时器
    clock = pygame.time.Clock()
    # 创建游戏对象（像当前走棋方、游戏是否结束等都封装到这个对象中）
    game = Game(screen, chessboard)
    game.back_button.add_history(chessboard.get_chessboard_str_map())
    # 创建AI对象
    # ai = ChessAI(game.computer_team)
    game.computer_team = 'b'  # 电脑先手改为r,我方AI先手改为b
    game.user_team = 'b' if game.computer_team == 'r' else 'r'  # 根据电脑先手/后手，改变我方的先后手
    ai = He.ChessAI(game.computer_team)
    my_ai = Me.ChessAI(game.user_team)

    # 主循环
    step = 0
    while True:
        # AI行动
        if not game.show_win and not game.show_draw and game.AI_mode and game.get_player() == ai.team:
            print(ai.team, '电脑方动： 第', step, '步')
            if game.back_button.is_repeated():
                print("重复走子，电脑方获胜...")
                game.set_win(game.get_player())
            else:
                # AI预测下一步
                cur_row, cur_col, nxt_row, nxt_col = ai.get_next_step(chessboard)
                # 选择棋子
                ClickBox(screen, cur_row, cur_col)
                # 下棋子
                chessboard.move_chess(nxt_row, nxt_col)
                # 清理「点击对象」
                ClickBox.clean()
                # 检测落子后，是否产生了"将军"功能
                if chessboard.judge_attack_general(game.get_player()):
                    print("将军....")
                # 检测对方是否可以挽救棋局，如果能挽救，就显示"将军"，否则显示"胜利
                    if chessboard.judge_win(game.get_player()):
                        print("电脑方获胜...")
                        game.set_win(game.get_player())
                    else:
                        # 如果攻击到对方，则标记显示"将军"效果
                        game.set_attack(True)
                else:
                    if chessboard.judge_win(game.get_player()):
                        print("电脑方获胜...")
                        game.set_win(game.get_player())
                    game.set_attack(False)
                if chessboard.judge_draw():
                    print("和棋...")
                    game.set_draw()
                # 落子之后，交换走棋方
            game.back_button.add_history(chessboard.get_chessboard_str_map())
            game.exchange()
        else:
            print(my_ai.team, '我方动： 第', step, '步')
            if game.back_button.is_repeated():
                print("重复走子，我方获胜...")
                game.set_win(game.get_player())
            else:
                # AI预测下一步
                cur_row, cur_col, nxt_row, nxt_col = my_ai.get_next_step(chessboard)
                # 选择棋子
                # 如果是我方后手，需要将位置映射到b黑色方，对称的(x1,y1)(x2,y2)-> x1+x2=9,y1+y2=8
                ClickBox(screen, cur_row, cur_col)
                # 下棋子
                chessboard.move_chess(nxt_row, nxt_col)
                # 清理「点击对象」
                ClickBox.clean()
                # 检测落子后，是否产生了"将军"功能
                if chessboard.judge_attack_general(game.get_player()):
                    print("将军....")
                    # 检测对方是否可以挽救棋局，如果能挽救，就显示"将军"，否则显示"胜利
                    if chessboard.judge_win(game.get_player()):
                        print("我方获胜...")
                        game.set_win(game.get_player())
                    else:
                        # 如果攻击到对方，则标记显示"将军"效果
                        game.set_attack(True)
                else:
                    if chessboard.judge_win(game.get_player()):
                        print("我方获胜...")
                        game.set_win(game.get_player())
                        game.set_attack(False)
                if chessboard.judge_draw():
                    print("和棋...")
                    game.set_draw()
                # 落子之后，交换走棋方
                game.back_button.add_history(chessboard.get_chessboard_str_map())
                game.exchange()
        step += 1
        # 显示游戏背景
        screen.blit(background_img, (0, 0))
        screen.blit(background_img, (0, 270))
        screen.blit(background_img, (0, 540))

        # # 显示棋盘
        # # screen.blit(chessboard_img, (50, 50))
        # chessboard.show()
        #
        # # 显示棋盘上的所有棋子
        # # for line_chess in chessboard_map:
        # for line_chess in chessboard.chessboard_map:
        #     for chess in line_chess:
        #         if chess:
        #             # screen.blit(chess[0], chess[1])
        #             chess.show()

        # 显示棋盘以及棋子
        chessboard.show_chessboard_and_chess()

        # 标记点击的棋子
        ClickBox.show()

        # 显示可以落子的位置图片
        Dot.show_all()

        # 显示游戏相关信息
        game.show()

        # 显示screen这个相框的内容（此时在这个相框中的内容像照片、文字等会显示出来）
        pygame.display.update()

        # FPS（每秒钟显示画面的次数）
        clock.tick(60)  # 通过一定的延时，实现1秒钟能够循环60次
        # if game.show_win:
        #    break


if __name__ == '__main__':
    main()
