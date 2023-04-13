import numpy as np
import pandas as pd


class QLearning:
    def __init__(self, actions, learning_rate=0.01, reward_decay=0.9, e_greedy=0.9):  # e_greedy=0.1
        self.actions = actions  # a list
        # self.n_actions = len(self.actions)
        self.lr = learning_rate
        self.gamma = reward_decay
        self.epsilon = e_greedy

        ''' build q table'''
        ############################
        # YOUR IMPLEMENTATION HERE #
        # 构建Q表
        self.q_table = pd.DataFrame(columns=self.actions, dtype=np.float64)
        ############################

    def choose_action(self, observation):
        ''' choose action from q table '''
        ############################
        # YOUR IMPLEMENTATION HERE #
        self.check_state_exist(observation)
        # 动作选择
        if np.random.uniform() < self.epsilon:
            # 选择最佳动作
            state_action = self.q_table.loc[observation, :]
            # 有些动作可能有相同的值，在这些动作中随机选择
            action = np.random.choice(state_action[state_action == np.max(state_action)].index)
        else:
            # 随机选取一个动作
            action = np.random.choice(self.actions)
        return action
        ############################

    def learn(self, s, a, r, s_):
        ''' update q table '''
        ############################
        # YOUR IMPLEMENTATION HERE #
        self.check_state_exist(s_)
        q_predict = self.q_table.loc[s, a]
        if s_ != 'terminal':
            q_target = r + self.gamma * self.q_table.loc[s_, :].max()  # next state is not terminal
        else:
            q_target = r  # next state is terminal
        self.q_table.loc[s, a] += self.lr * (q_target - q_predict)  # update

        ############################

    def check_state_exist(self, state):
        ''' check state '''
        ############################
        # YOUR IMPLEMENTATION HERE #
        if state not in self.q_table.index:
            # 将新状态附加到Q表
            self.q_table = self.q_table.append(
                pd.Series(
                    [0] * len(self.actions),
                    index=self.q_table.columns,
                    name=state,
                )
            )
        ##########################

