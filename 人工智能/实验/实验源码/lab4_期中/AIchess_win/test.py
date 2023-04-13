def alphabeta(node, depth, a, b, player):
    # 达到最深搜索深度或胜负已分
    if depth == 0:
        return v(node)
    if Player == MaxPlayer:  # 极大节点
        for child in all_child:  # 子节点是极小节点
            a = max(α, alphabeta(child, depth-1, a, b, not player))
            if b <= a:
                # 该极大节点的值>=α>=β，该极大节点后面的搜索到的值肯定会大于β，因此不会被其上层的极小节点所选用了。对于根节点，β为正无穷
                break  # beta剪枝
        return a
    else:
        # 极小节点
        for child in all_child:     # 子节点是极大节点
            b = min(b, alphabeta(child, depth-1, a, b, not player))     # 极小节点
            if b <= a:    # 该极大节点的值<=β<=α，该极小节点后面的搜索到的值肯定会小于α，因此不会被其上层的极大节点所选用了。对于根节点，α为负无穷
                break   # alpha剪枝
        return b


class Sb:
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
                father = chessboard.chessboard_map[new_row][new_col]
                chessboard.move_chess2(old_row, old_col, new_row, new_col)  # 产生一个儿子节点
                # father = chessboard.my_move_chess(old_row, old_col, new_row, new_col, None)
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
            v0 = 0  # 上一个beta值
            for move in move_list:
                old_row, old_col, new_row, new_col = move
                father = chessboard.chessboard_map[new_row][new_col]
                chessboard.move_chess2(old_row, old_col, new_row, new_col)  # 产生一个儿子节点
                # father = chessboard.my_move_chess(old_row, old_col, new_row, new_col, None)
                score = self.alpha_beta(depth - 1, alpha, beta, not player, chessboard)  # 对儿子节点进行剪枝并得到递推值
                if v > score:  # 取最小的score，对方与中取小，和
                    if depth == max_depth:  # 达到最大深度
                        self.best_move = move
                    v0 = v
                    v = score
                chessboard.back(new_row, new_col, old_row, old_col, father)  # 返回父亲节点
                if alpha >= beta:  # 进行beta剪枝
                    break
            return v

    def my_move_chess(self, old_row, old_col, new_row, new_col, father_chess):
        # 将棋子移动到指定位置,这个chess是曾经位置的棋子，用于返回上一步(父亲节点)
        save = self.chessboard_map[new_row][new_col]
        # 移动位置
        self.chessboard_map[new_row][new_col] = self.chessboard_map[old_row][old_col]
        # 修改棋子的属性
        self.chessboard_map[new_row][new_col].update_position(new_row, new_col)
        self.chessboard_map[old_row][old_col] = father_chess    #
        if self.chessboard_map[old_row][old_col]:
            # 修改棋子的属性
            self.chessboard_map[old_row][old_col].update_position(old_row, old_col)
        return save


class move(object):
    def __init__(self, x0, y0, x1, y1, value=0):
        self.row = x0
        self.col = y0
        self.new_row = x1
        self.new_col = y1
        self.score = value

    def pos(self):
        return self.row, self.col, self.new_row, self.new_col