for i in range(num_episodes):

    ## 初始化状态
    state = env.reset()

    ## 设置ε递减
    # epsilon = np.linspace(0.9, 0.1, num=num_episodes)[i]
    alpha = 0.1
    gama = 0.9
    ## 记录本次循环的累积奖励
    r = 0

    ## 进行循环
    while True:

        ## 根据?-greedy选择动作
        action = epsilon_greedy(state, epsilon)

        ## 在状态下执行动作，返回奖励和下一状态
        next_state, reward, done, _ = env.step(action)

        ## 更新Q值
        q_table_learning[state, action] += alpha * (
                    reward + gamma * max(q_table_learning[next_state]) - q_table_learning[state, action])

        ## 更新当前状态
        state = next_state

        ## 记录本次循环的奖励
        r += reward

        ## 若达到终止状态，结束循环
        if done:
            break

    # 记录本次迭代的累积奖励
    reward_list_qlearning.append(r)