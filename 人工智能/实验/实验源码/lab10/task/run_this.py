"""
Reinforcement learning maze example.

Red rectangle:          explorer.
Black rectangles:       hells       [reward = -1].
Yellow bin circle:      paradise    [reward = +1].
All other states:       ground      [reward = 0].

This script is the main part which controls the update method of this example.
"""

from maze_env import Maze
from RL_q_learning import QLearning
from RL_sarsa import Sarsa

import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


def update():
    for episode in range(episodes):
        # initial observation
        observation = env.reset()
        step = 0
        while True:
            # 记录步数
            step += 1
            # fresh env
            '''Renders policy once on environment. Watch your agent play!'''
            env.render()
            # RL根据观察选择动作
            action = RL.choose_action(str(observation))
            # RL采取行动并获得下一次观察和奖励
            observation_, reward, done = env.step(action)
            # 更新Q值
            RL.learn(str(observation), action, reward, str(observation_))
            # swap observation
            observation = observation_

            # break while loop when end of this episode
            if done:
                # 如果找到了目标
                if reward == 1:
                    print("episode = ", episode, ",  steps = ", step, "\n")
                    steps.append(step)
                else:
                    steps.append(steps[-1])
                break
    # end of game
    print('game over')
    env.destroy()


if __name__ == "__main__":
    env = Maze()

    '''
    build RL Class
    RL = QLearning(actions=list(range(env.n_actions)))
    RL = Sarsa(actions=list(range(env.n_actions)))
    '''
    ############################
    # YOUR IMPLEMENTATION HERE #
    choice = input("请选择使用Q-learning/Sarsa：1/2\n")
    episodes = 100
    steps = [100]
    if choice == "1":
        print("使用Q-learning")
        RL = QLearning(actions=list(range(env.n_actions)))
    else:
        print("使用Sarsa")
        RL = Sarsa(actions=list(range(env.n_actions)))
    ############################
    env.after(100, update)
    env.mainloop()

    # 输出最终的q表
    print(RL.q_table)
    # 画图
    plt.plot(np.linspace(0, episodes, len(steps)), steps)
    plt.xlabel("迭代次数episode", fontsize=18)
    plt.ylabel("步数", rotation=0, fontsize=18)
    plt.title('达到目标的步数和训练Epoch数', fontsize=18)
    plt.show()

