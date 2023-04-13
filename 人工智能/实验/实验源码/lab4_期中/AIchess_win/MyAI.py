import copy
from ChessBoard import *

max_depth = 3


class Evaluate(object):
    # 棋子棋力得分
    single_chess_point = {
        'c': 989,   # 车 989
        'm': 439,   # 马,439
        'p': 442,   # 炮，442
        's': 226,   # 士
        'x': 210,   # 象
        'z': 55,    # 卒
        'j': 65536  # 将
    }
    # 红兵（卒）位置得分
    red_bin_pos_point = [
        [1, 3, 9, 10, 12, 10, 9, 3, 1],
        [18, 36, 56, 95, 118, 95, 56, 36, 18],
        [15, 28, 42, 73, 80, 73, 42, 28, 15],
        [13, 22, 30, 42, 52, 42, 30, 22, 13],
        [8, 17, 18, 21, 26, 21, 18, 17, 8],
        [3, 0, 7, 0, 8, 0, 7, 0, 3],
        [-1, 0, -3, 0, 3, 0, -3, 0, -1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
    # 红车位置得分
    red_che_pos_point = [
        [185, 195, 190, 210, 220, 210, 190, 195, 185],
        [185, 203, 198, 230, 245, 230, 198, 203, 185],
        [180, 198, 190, 215, 225, 215, 190, 198, 180],
        [180, 200, 195, 220, 230, 220, 195, 200, 180],
        [180, 190, 180, 205, 225, 205, 180, 190, 180],
        [155, 185, 172, 215, 215, 215, 172, 185, 155],
        [110, 148, 135, 185, 190, 185, 135, 148, 110],
        [100, 115, 105, 140, 135, 140, 105, 115, 110],
        [115, 95, 100, 155, 115, 155, 100, 95, 115],
        [20, 120, 105, 140, 115, 150, 105, 120, 20]
    ]
    # 红马位置得分
    red_ma_pos_point = [
        [80, 105, 135, 120, 80, 120, 135, 105, 80],
        [80, 115, 200, 135, 105, 135, 200, 115, 80],
        [120, 125, 135, 150, 145, 150, 135, 125, 120],
        [105, 175, 145, 175, 150, 175, 145, 175, 105],
        [90, 135, 125, 145, 135, 145, 125, 135, 90],
        [80, 120, 135, 125, 120, 125, 135, 120, 80],
        [45, 90, 105, 190, 110, 90, 105, 90, 45],
        [80, 45, 105, 105, 80, 105, 105, 45, 80],
        [20, 45, 80, 80, -10, 80, 80, 45, 20],
        [20, -20, 20, 20, 20, 20, 20, -20, 20]
    ]
    # 红炮位置得分
    red_pao_pos_point = [
        [190, 180, 190, 70, 10, 70, 190, 180, 190],
        [70, 120, 100, 90, 150, 90, 100, 120, 70],
        [70, 90, 80, 90, 200, 90, 80, 90, 70],
        [60, 80, 60, 50, 210, 50, 60, 80, 60],
        [90, 50, 90, 70, 220, 70, 90, 50, 90],
        [120, 70, 100, 60, 230, 60, 100, 70, 120],
        [10, 30, 10, 30, 120, 30, 10, 30, 10],
        [30, -20, 30, 20, 200, 20, 30, -20, 30],
        [30, 10, 30, 30, -10, 30, 30, 10, 30],
        [20, 20, 20, 20, -10, 20, 20, 20, 20]
    ]
    # 红将位置得分
    red_jiang_pos_point = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 9750, 9800, 9750, 0, 0, 0],
        [0, 0, 0, 9900, 9900, 9900, 0, 0, 0],
        [0, 0, 0, 10000, 10000, 10000, 0, 0, 0],
    ]
    # 红相或士位置得分
    red_xiang_shi_pos_point = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 60, 0, 0, 0, 60, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [80, 0, 0, 80, 90, 80, 0, 0, 80],
        [0, 0, 0, 0, 0, 120, 0, 0, 0],
        [0, 0, 70, 100, 0, 100, 70, 0, 0],
    ]

    red_pos_point = {
        'z': red_bin_pos_point,
        'm': red_ma_pos_point,
        'c': red_che_pos_point,
        'j': red_jiang_pos_point,
        'p': red_pao_pos_point,
        'x': red_xiang_shi_pos_point,
        's': red_xiang_shi_pos_point
    }

    def __init__(self, team):
        self.team = team

    def get_single_chess_point(self, chess: Chess):
        if chess.team == self.team:
            return self.single_chess_point[chess.name]
        else:
            return -1 * self.single_chess_point[chess.name]

    def get_chess_pos_point(self, chess: Chess):
        red_pos_point_table = self.red_pos_point[chess.name]
        if chess.team == 'r':
            pos_point = red_pos_point_table[chess.row][chess.col]
        else:
            pos_point = red_pos_point_table[9 - chess.row][chess.col]
        if chess.team != self.team:
            pos_point *= -1
        return pos_point

    def evaluate(self, chessboard: ChessBoard):
        point = 0
        for chess in chessboard.get_chess():
            point += self.get_single_chess_point(chess)
            point += self.get_chess_pos_point(chess)
        return point


class ChessMap(object):
    def __init__(self, chessboard: ChessBoard):
        self.chess_map = copy.deepcopy(chessboard.chessboard_map)


class ChessAI(object):
    def __init__(self, computer_team):
        self.team = computer_team
        self.my_team = computer_team    # 用于保存我方的队伍r/b
        self.his_team = 'b' if computer_team == 'r' else 'r'    # 根据我方棋子(r/b)判断对手棋子(b/r)
        self.evaluate_class = Evaluate(self.team)
        self.best_move = (-1, -1, -1, -1)  # 最好的走步

    def get_sons(self, chessboard: ChessBoard):
        # 得到己方当前局面所有的可以移动的棋子的前后位置
        all_chess = chessboard.get_chess()
        all_sons = []
        for chess in all_chess:
            if chess.team == self.team:     # my_team
                for it in chessboard.get_put_down_position(chess):
                    all_sons.append((chess.row, chess.col, it[0], it[1]))
        return all_sons

    def alpha_beta(self, depth, alpha, beta, player, chessboard: ChessBoard):
        # alpha_beta剪枝，以局面值为评估值
        # 搜索到了对应深度或者没有可移动棋子
        if depth == 0:
            return self.evaluate_class.evaluate(chessboard)
        if player:  # 我方，alpha剪枝,或中取大
            self.team = self.my_team  # 我方，alpha剪枝,或中取大
            son_list = self.get_sons(chessboard)  # 儿子节点
            v = float("-inf")  # 负无穷
            for move in son_list:  # 遍历所有子节点，这里子节点是移动棋子步
                old_row, old_col, new_row, new_col = move
                father = chessboard.chessboard_map[new_row][new_col]    # 保存被覆盖的棋子（如果有的话）,即父节点
                chessboard.move_chess2(old_row, old_col, new_row, new_col)  # 产生一个儿子节点
                score = self.alpha_beta(depth - 1, alpha, beta, not player, chessboard)  # 对儿子节点进行剪枝并得到递推值
                if v < score:  # 取最大的score，我方或中取大
                    if depth == max_depth:
                        self.best_move = move
                    v = score
                if v > alpha:
                    alpha = v
                chessboard.back(new_row, new_col, old_row, old_col, father)  # 返回父亲节点
                if alpha >= beta:  # 进行alpha剪枝
                    break
            return v  # 返回递推值
        else:   # 对手，beta剪枝,与中取小
            self.team = self.his_team  # 对手，beta剪枝,与中取小
            move_list = self.get_sons(chessboard)  # 儿子节点
            v = float("inf")  # 正无穷
            for move in move_list:
                old_row, old_col, new_row, new_col = move
                father = chessboard.chessboard_map[new_row][new_col]    # 保存被覆盖的棋子（如果有的话）,即父节点
                chessboard.move_chess2(old_row, old_col, new_row, new_col)  # 产生一个儿子节点
                score = self.alpha_beta(depth - 1, alpha, beta, not player, chessboard)  # 对儿子节点进行剪枝并得到递推值
                if v > score:  # 取最小的score，对方与中取小，和
                    if depth == max_depth:  # 达到最大深度
                        self.best_move = move
                    v = score
                chessboard.back(new_row, new_col, old_row, old_col, father)  # 返回父亲节点
                if alpha >= beta:  # 进行beta剪枝
                    break
            return v

    def get_next_step(self, chessboard: ChessBoard):
        team = self.team
        # 默认先动的是r方
        max_val = float("inf")  # 正无穷
        min_val = float("-inf")  # 负无穷
        value = self.alpha_beta(max_depth, min_val, max_val, True, chessboard)  # 开始我方先走，True
        print('该步移动的评估值为：', value)
        self.team = team  # 避免更改了队伍信息
        return self.best_move

